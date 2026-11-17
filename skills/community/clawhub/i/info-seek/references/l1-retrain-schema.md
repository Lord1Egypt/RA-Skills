# L1 阈值重训数据格式 (l1-retrain-schema)

> 配套脚本：`scripts/train_l1_thresholds.py` (mod-v1.0.0) / `scripts/forensics_retrain.py` 阶段 1
> 检测引擎：`extensions/fake_detect/l1_engine.py` (apply_l1_rules / compute_l1_features / DEFAULT_THRESHOLDS)
> 数据接入：`extensions/fake_detect/data_adapter.py` (Dataset / load_dataset / from_raw)
> 约束：FPR_CAP=0.02，评分 `rec - 10*max(0, fpr-cap)`，坐标下降 3 轮，60/40 分层 + holdout。

---

## 1. 输入样本契约 (data_adapter.Dataset)

### 1.1 元表 meta_df（必填）
- `index` = 账号 id（int/str，与 likes/growth 字典 key 一致；`_clean_meta` 自动别名归一）
- 必填列：`id` `followers` `following` `posts` `er`
- 标注列（四选一，retrain_l1 自动探测）：`group_label` / `label` / `is_fake` / `group`
  - 值 >0 → 水军(label=1)；==0 → 正常(normal_mask)
- HF-R1 可选扩展列（缺省中性，不影响既有判定）：`template_similarity` `follower_quality` `zombie_follower_ratio`

### 1.2 时间序列
- `likes: Dict[id, np.ndarray(T)]` — 每日点赞序列（Benford L1a，样本<50 不判）
- `growth: Dict[id, np.ndarray(T)]` — 每日涨粉序列（L1c 尖峰）

### 1.3 关系图 / 时段（可选，缺失自动降级）
- `G: nx.DiGraph` — 互惠率 L1e（缺省全 0 不触发）
- `timing: Dict[id, List[24]]` — 活跃时段熵 L1f（缺省 1.0 不触发）

---

## 2. 合成样本生成器 (make_synthetic_accounts)

无真实样本时 `train_l1_thresholds.py --demo` 自造对齐契约的合成数据：
- 正常(group_label=0)：likes 幂律(首位近似 Benford 友好) + 平滑 growth + 中性 ER
- 水军(group_label>=1)：likes 首位集中(1/2 开头, 破坏 Benford) + 末段 growth 尖峰 + 极端 ER

默认规模：`n_normal=400, n_fake=120, T=120`。

---

## 3. 重训报告 (retrain_l1 输出 → l1_retrain_report.json)

```json
{
  "trained_thresholds": { "benford_alpha": 0.01, "er_low": 1e-4, ... },
  "metrics": {
    "train": { "recall": 0.95, "fpr": 0.01 },
    "holdout_default": { "recall": 0.93, "fpr": 0.015 },
    "holdout_trained": { "recall": 0.96, "fpr": 0.012 }
  },
  "candidates": { "benford_alpha": [0.001,0.005,0.01,0.05], ... },
  "fpr_cap": 0.02,
  "mod_version": "mod-v1.0.0"
}
```

- `trained_thresholds`：坐标下降收敛后的新阈值（覆盖 DEFAULT_THRESHOLDS 候选键）
- `holdout_default` vs `holdout_trained`：默认阈值 vs 重训阈值在 40% holdout 的 Recall/FPR 对比
- 验收：重训后 `fpr <= FPR_CAP(0.02)` 且 `recall >= holdout_default.recall`（不退化）

---

## 4. 资产写回 (--write 原子写回 l1_thresholds.json)

```json
{ "DEFAULT_THRESHOLDS": { ... }, "retrained_by": "train_l1_thresholds", "mod_version": "mod-v1.0.0" }
```
- 默认只读（仅出报告）；`--write` 才原子写回（旧文件备份 `.bak`）
- l1_engine 注释明确"可由 train_l1_thresholds.py 重训覆盖"

---

## 5. CLI
```bash
python scripts/train_l1_thresholds.py --demo                 # 合成样本 self-check
python scripts/train_l1_thresholds.py --data accounts.csv --write   # 真实数据重训+写回
python scripts/train_l1_thresholds.py --demo --json          # JSON 报告
```
