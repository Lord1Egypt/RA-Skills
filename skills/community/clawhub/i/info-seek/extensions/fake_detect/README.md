# FakeDetect — 账号深度取证扩展包（extensions/fake_detect）

> infoseek 身份归因验证层的**深度取证二级引擎**（AccountTrustScorer 的升级，非 Maigret/Sherlock 替代）
> 融入版本：infoseek 1.6.0（对外版本号保持，不 bump）· 引擎版本：v1.0.0

## 能力

四层对抗级检测（评估报告_P0P1P2 收口基线）：

| 层 | 方法 | 依赖数据 | 说明 |
|----|------|---------|------|
| L1 统计规则 | Benford chi2 + ER 分档 + 增长导数 + 关注比 + 互惠率 | 元表 + likes/growth 时序（+图） | 阈值参数化（l1_thresholds.json 可重训） |
| L2 图结构 | Louvain 社区密度(d>0.25) + PPR 种子富集（种子=L1 红旗） | 关系图 | 无图自动降级 |
| 时序同步 | spike 二值化 + min-覆盖准团 + 同步后验 | growth 时序 | ≤10人@≤0.25 小集群唯一可行信号（P1.5） |
| L3 ML | RandomForest 5 折 CV + CAP 阈值（FPR≤2% 最大 recall） | 标注 label | 无标注/单类自动跳过 |

## 使用

```python
# 1) 数据接入（任意格式 → 标准化 Dataset）
from data_adapter import load_dataset
ds = load_dataset(source="accounts.csv", ts_path="ts/", graph_src="graph.edgelist")

# 2) 深度取证
from fake_detect_engine import detect, assess_sufficiency
assert assess_sufficiency(ds)["sufficient"], "信号不足（缺数据≠水军），降级 AccountTrustScorer"
report = detect(ds)
```

CLI：

```bash
python fake_detect_engine.py --demo            # 内置合成数据全链自检
python fake_detect_engine.py --json data.json  # 任意数据接入检测
```

## 输出契约（对齐 AccountTrustScorer）

`detect() -> Report`：

```jsonc
{
  "status": "ok|degraded|failed",
  "sufficiency": {"sufficient": bool, "deep_score": float, "signals": {...}, "missing": [...]},
  "verdicts": {"<account_id>": {
      "trust_score": 0-100, "verdict": "real|likely_real|suspicious|bot|unknown",
      "verdict_cn": "...", "flags": [...], "layers": {"l1_flags": n, "l2_susp": bool, "sync_member": bool, "risk": n}}},
  "coord_clusters": [{"cluster_id", "members", "size", "density", "behav_entropy"}],
  "sync_groups": [{"group_id", "members", "size"}],
  "summary": {"l1": {...}, "l2": {...}, "sync": {...}, "l3": {...}, "verdict_dist": {...}, "gate": {...}},
  "degradation": "none|no_graph|no_labels|insufficient_signals|...",
  "blindspots": [...],
  "meta": {"engine": "fake_detect", "version": "1.0.0", "routed_infoseek": "1.6.0"}
}
```

## 数据契约

- **meta 元表**：`id`（必填，索引）、`followers/following/posts/er`（可缺省，缺省按中性）
  - 列名自动映射：`map_schema`（中英文/多平台别名 → 标准字段，见 `data_adapter.META_ALIASES`）
- **时序**：`likes`（每日点赞）/ `growth`（每日涨粉）dict[int, ndarray]，长度自动适配
- **图**：edgelist 路径 / DataFrame / 边列表 / nx.Graph，端点归一化 + 坏边记录
- **标注（L3 可选）**：`group_label / label / is_fake / group` 列（>0=水军）
- 支持 CSV / JSON / parquet / NPZ / NPY 自动探测（`load_dataset`）

## 充分性门控（命门）

`assess_sufficiency`：`deep_score = ts覆盖*0.5 + ER覆盖*0.25 + 图谱*0.25 >= 0.5`
- 达标 → 深度取证；不达标 → **降级 AccountTrustScorer**（缺数据 ≠ 水军，绝不硬跑）
- pipeline 自动路径（Maigret/Sherlock 只有 username）天然不足 → 自动走轻量规则层
- 深度取证由 B 模式 `account_forensics` MCP 工具**显式投喂数据**触发

## 盲区边界（诚实声明，评估报告 P0 实证）

- **G0-G2 攻击面**（笨水军/伪装 ER/伪装增长）：检测全灭 ✅
- **G3 伪装 Benford**：漏检 ~75%（统计指纹被规避，仅剩行为/图谱弱信号聚合）
- **G4 全伪装**：漏检 ~67%（单层指纹全失效，需行为时序跨期或外部证据）
- 引擎输出 `blindspots` 字段如实声明；不承诺对对抗级对手的覆盖

## 合规

- `kind: account_forensics`（行为取证新族，区别于 `identity_attribution`）
- 涉个人行为画像：`INFOSEEK_ENABLE_FAKE_DETECT=1` ∩ consent 双闸，未满足 → **blocked 显式报错**
- 审计落盘：经 `_audit_identity` 通道，`[account_forensics]` 前缀
- 默认关闭（registry `enabled: false`）

## 文件清单

| 文件 | 说明 |
|------|------|
| `fake_detect_engine.py` | 主引擎（函数化 `detect(dataset)->Report` + 充分性门控 + CLI 自检） |
| `l1_engine.py` | L1 参数化规则引擎（阈值可配置 + 互惠率前移） |
| `data_adapter.py` | 通用数据接入层（格式探测/schema 归一化/质量校验） |
| `sync_detect.py` | 时序同步检测（从 sync_test.py 函数化提取） |
| `l1_thresholds.json` | L1 重训阈值资产（trained/dirty_demo/candidates） |
| `fake-detect-manifest.json` | 扩展包清单（与 qcm-collab-manifest 同构） |
| `requirements.txt` | 重依赖隔离（numpy/pandas/scipy/networkx/scikit-learn） |
| `README.md` | 本文件 |

## 重训管道（B3）

- L1 阈值重训：`train_l1_thresholds`（坐标下降，FPR≤2% 约束）→ 覆盖 `l1_thresholds.json`
- 对抗训练：`adv_train`（G0-G4 对抗样本混合，OOD→ID 化，CAP@FPR≤2% 三级指标）
- 管道入口在 infoseek 侧 `scripts/forensics_retrain.py`（真实数据接入后执行，见 ROADMAP §6.7 B3）