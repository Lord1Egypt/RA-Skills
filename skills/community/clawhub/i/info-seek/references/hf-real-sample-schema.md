# HF-P1 真实样本接入契约（Real Sample Schema）

> 版本：v1.0.0 ｜ 日期：2026-09-21 ｜ 归属：HF-P1（协同簇融合权重校准 + FPR ≤ 2% 基线）
> 配套：`scripts/hf_sample_kit.py`（校验 / 打样 / 校准）；`scripts/identity_confidence_fusion.py`（四因子融合）

## 0. 目的与边界

HF-P1 中「融合权重校准」与「误报率（FPR ≤ 2%）基线」**依赖带人工标注的真实样本**。
沙箱环境不具备真实环境（无真机 / 无真实账号授权），故本文件先行固化**样本接入契约**，
使真实样本到位后**零改造接入**；在此之前用 `hf_sample_kit` 的半合成样本（`source=synthetic`）
演练全链（打样 → 校验 → 校准）。

> **合规红线（不可逾越）**：样本**仅采集账号公域内容属性**（平台交叉、人因评分、站点权威、
> 协同簇规模/密度）与**人工标注标签**；**不采集**任何设备 / 客户端指纹（UA / 屏幕 /
> Canvas·WebGL / 字体 / 时区 / JA3·JA4），不采集个人身份信息（实名、手机号、证件、私密地址）。
> 详见 `PRIVACY.md §4/§6`、`references/network-boundary-report.md §4`。

## 1. 样本格式

支持 JSON 与 CSV 两种；JSON 顶层结构：

```json
{
  "schema": "infoseek-hf-sample/1",
  "source": "real",
  "created": "2026-09-21",
  "records": [
    {
      "label": 0,
      "username": "alice",
      "platform": "GitHub",
      "url": "https://github.com/alice",
      "cross_platform_matches": 3,
      "trust_score": 84.5,
      "site_rank": 18,
      "coord_cluster_size": 0,
      "coord_cluster_density": 0.0,
      "sync_group_size": 0
    }
  ]
}
```

CSV 首行为表头，列名同上（`label` 整数，数值列可带小数）。

## 2. 字段契约

| 字段 | 必填 | 类型 | 取值范围 | 说明 |
|---|---|---|---|---|
| `label` | ✅ | int | 0 / 1 | **人工标注真值**：1 = 可疑（水军 / 机器人 / 协同簇），0 = 正常 |
| `cross_platform_matches` | ✅ | int | ≥ 0 | 发现层：同名账号跨平台命中数（A 因子） |
| `trust_score` | ✅ | float | 0–100 | 验证层：AccountTrustScorer 五维人因评分（B 因子） |
| `site_rank` | ✅ | int | ≥ 0（0=无数据） | 站点权威排名（C 因子，越小越权威） |
| `coord_cluster_size` | 建议 | int | ≥ 0 | 协同簇成员数（D 因子，FakeDetect `coord_clusters.size`） |
| `coord_cluster_density` | 建议 | float | 0–1 | 协同簇密度（D 因子） |
| `sync_group_size` | 建议 | int | ≥ 0 | 时序同步组规模（D 因子，`sync_groups.size`） |
| `username` / `platform` / `url` | 可选 | str | — | 归因辅助（`url` 命中 `core/trust_sources` 白名单时用于 C 因子） |

> `label` 必须**人工独立标注**（不来自被测模型自身输出），否则校准无意义（循环论证）。
> D 因子字段缺失时该记录**不参与校准**（`hf_sample_kit` 仅用四因子齐全记录）。

## 3. 采集清单（真实样本来源）

| # | 来源 | 产出字段 | 合规要点 |
|---|---|---|---|
| S1 | 公开账号人工抽样 + 人工判读 | `label` + `url` + `platform` | 仅公域可见信息；不登录、不抓私密 |
| S2 | `identity_attribution`（Maigret/Sherlock）产物 | `cross_platform_matches` / `site_rank` / `url` | 授权 CLI + consent 闸（`infoseek_consent_cli.py`） |
| S3 | `AccountTrustScorer`（五维） | `trust_score` | 本地规则，零网络 |
| S4 | `account_forensics`（FakeDetect，双闸） | `coord_cluster_size` / `coord_cluster_density` / `sync_group_size` | `INFOSEEK_ENABLE_FAKE_DETECT=1` ∩ consent ∩ 注册表 |
| S5 | 已脱敏的第三方标注集（若有授权） | 全部 | 需授权凭证 + 脱敏证明 |

**建议样本量**：≥ 200 条（正负比约 1:3～1:5），覆盖 CN / 全局分区；跨分区分别报告 FPR。

## 4. 校准流程

```bash
# 1) 校验真实样本契约（字段/类型/范围/标签）
python scripts/hf_sample_kit.py --validate my_sample.json     # 退出码 0=通过

# 2) 校准四因子（a:b:c 比例固定，搜 D 权重）→ 推荐 D 权重 + 判定阈值 + FPR
python scripts/hf_sample_kit.py --calibrate my_sample.json

# 3) 应用推荐权重（示例：d=0.20 → a/b/c 按 7:8:5 分配）
export INFOSEEK_FUSION_WEIGHTS=0.28,0.32,0.20,0.20
```

校准目标：在 **FPR ≤ 2%** 约束下最大化 recall；输出 `best.{d,weights,threshold,recall,fpr}`
与全 `d` 网格的 `curve`（可追溯权衡）。

## 5. 半合成打样（无真实样本时的替代）

```bash
python scripts/hf_sample_kit.py --demo
```

打样集（`source=synthetic`，固定 seed 可复现）含三类：正常账号、**笨水军**（三因子即暴露）、
**伪装水军**（G3/G4 型：三因子接近正常，**仅协同簇暴露**）。打样已实测 D 因子增益：
`d=0 → recall 0.52`；`d=0.20 → recall 1.00 @ FPR 0.6%`。**打样结论不得直接作为生产阈值**，
仅用于校准管线演练与 D 因子方向的定性验证。

## 6. 真实样本到位后的收尾步骤

1. `hf_sample_kit --validate` 通过（0 退出码）；
2. `hf_sample_kit --calibrate` 得推荐权重与阈值；
3. 以推荐值更新 `INFOSEEK_FUSION_WEIGHTS`（或改 `identity_confidence_fusion.DEFAULT_WEIGHTS` 默认值时
   须**保持 a:b:c 比例 7:8:5** 以免破坏零回归，并同步守护测试期望值）；
4. 分区（CN / IN / 全局）分别报告 FPR，写入 `references/real-env-evidence-log.md`；
5. 回归全绿后按 v2.2.0 发布收尾流程归档。

## 7. 局限（如实声明）

- 本文件为**接入契约**，非真实样本集；沙箱不具备真实环境，真实样本须由你方提供或授权采集。
- 半合成打样与真实分布存在差距，**不得**据此宣称生产 FPR / recall。
- D 因子方向（协同强 → 身份置信下调）为设计决策，须以真实样本复核；若校准显示反向，需重新评估。
