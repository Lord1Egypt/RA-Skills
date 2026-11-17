# meta-analysis 案例库总览

> 由 `cases/case_catalog.py` 生成。案例库 = 技能最便宜的回归基准：每次改 block_a/b/c、pdf_extractor、run_stage 都跑一遍全套案例比对信封/数值是否漂移。
>
> 📋 离线验证结果见 **[VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md)**（14 案例全链路 A4 抽取 + 11 模板 1:1 映射 + 本地可算/需 coze 状态）。

## 案例清单（14 个）

| 案例 | 标题 | 类别 | 设计 | 效应量 | 模板 |
|---|---|---|---|---|---|
| C01 | SGLT2 抑制剂 vs 安慰剂对 T2DM 患者 MACE 的影响（二分类 OR） | 数值指标 | 干预性 RCT，二分类结局，pairwise | OR | TPL-01 |
| C02 | 卡介苗（BCG）疫苗对结核病发病的保护效力（二分类 RR） | 数值指标 | 干预性 RCT，二分类结局，pairwise（RR） | RR | TPL-01 |
| C03 | 某干预对术后 30 天死亡率的影响（二分类 RD） | 数值指标 | 干预性 RCT，二分类结局，pairwise（RD） | RD | TPL-01 |
| C04 | 降压药对收缩压（SBP）降低的均数差（连续型 MD） | 数值指标 | 干预性 RCT，连续型结局，pairwise（MD） | MD | TPL-02 |
| C05 | 心理干预对抑郁量表评分的影响（连续型 SMD） | 数值指标 | 干预性 RCT，连续型结局异量纲，pairwise（SMD） | SMD | TPL-02 |
| C06 | 肿瘤免疫治疗对总生存期（OS）的 HR 合并（已有效应量 logHR） | 数值指标 | 干预性 RCT，时间-事件结局，已有效应量 pairwise（logHR） | logHR | TPL-03 |
| C07 | 中心静脉导管相关血流感染（CLABSI）率比（IRR，人时数据） | 数值指标 | 前后对照/队列，率比，pairwise（IRR） | IRR | TPL-04 |
| C08 | 教育年限与健康评分的相关性合并（ZCOR） | 数值指标 | 观察性，相关系数，pairwise（ZCOR） | ZCOR | TPL-05 |
| C09 | 不同地区成人吸烟率合并（单组率 PLOGIT） | 数值指标 | 流行病学调查，单组率，pairwise（PLOGIT） | PLOGIT | TPL-06 |
| C10 | 慢性疼痛患者基线疼痛评分合并（单组均值 MN） | 数值指标 | 观察性/基线，单组均值，pairwise（MN） | MN | TPL-07 |
| C11 | 心衰治疗对心血管死亡风险的 HR（生存分析，O-E/V 法） | 数值指标 | 干预性 RCT，时间-事件结局，pairwise（logHR via O-E/V） | logHR | TPL-08 |
| C12 | 三类降压药对 SBP 降低的网状 Meta（NMA，≥3 干预） | 复杂设计 | 干预性 RCT，多臂，网状 Meta（直接+间接比较） | OR | TPL-09 |
| C13 | 新冠抗原检测准确性的诊断 Meta（DTA，TP/FP/TN/FN） | 复杂设计 | 诊断准确性研究，2×2 四格表，pairwise（DOR/Sens/Spec） | DOR | TPL-10 |
| C14 | 三臂肿瘤 RCT（2 活性药 + 安慰剂）独立对比 Meta（多臂拆分） | 复杂设计 | 干预性多臂 RCT，按对比拆分，pairwise（OR） | OR | TPL-11 |

## 模板清单（11 个）↔ 对应案例

| 模板 | 情境 | 效应量 | PDF表型 | 自动识别 | 演示案例 |
|---|---|---|---|---|---|
| TPL-01 | 二分类 2×2 四格表 | OR/RR/RD | T_DICHOT | ✅ 已自动识别 | C01, C02, C03 |
| TPL-02 | 连续型两臂（均值±SD） | MD/SMD | T_CONTINUOUS / T_CONT_TWOARM | ⚠️ 部分自动 | C04, C05 |
| TPL-03 | 已有效应量（对数尺度） | lnOR/SMD/logHR/ROM/ZCOR | T_EFFECT_TABLE / T_MD_CI | ⚠️ 部分自动 | C06 |
| TPL-04 | 率比（人时数据 IRR） | IRR | （暂无自动，需人工映射） | ✋ 需人工映射 | C07 |
| TPL-05 | 相关系数 | ZCOR | （暂无自动，需人工映射） | ✋ 需人工映射 | C08 |
| TPL-06 | 单组率 | PLOGIT/PRAW | （暂无自动，需人工映射） | ✋ 需人工映射 | C09 |
| TPL-07 | 单组均值 | MN | （暂无自动，需人工映射） | ✋ 需人工映射 | C10 |
| TPL-08 | 生存分析 HR | logHR | （暂无自动，需人工映射） | ✋ 需人工映射 | C11 |
| TPL-09 | 网状 Meta（多臂） | OR/RR/MD | （暂无自动，需人工映射） | ✋ 需人工映射 | C12 |
| TPL-10 | 诊断试验准确性（DTA） | DOR/Sens/Spec | （暂无自动，需人工映射） | ✋ 需人工映射 | C13 |
| TPL-11 | 多臂 RCT（独立对比） | OR/RR/RD/MD | （暂无自动，需人工映射） | ✋ 需人工映射 | C14 |

## 1:1 对应关系说明

- 每个**数据形状/研究情境**有且仅有一个 Excel 提取模板（`TPL-xx`）。
- 每个模板的「数据录入」sheet 列定义与 `references/data_templates.md` 完全一致，并追加 `PDF来源(页/表)` 与 `备注` 两列用于溯源。
- `pdf_extractor` 当前 P1 仅自动识别 T_DICHOT / T_CONTINUOUS 系列；其余形状标注「需人工映射」，模板即人工映射的落地载体。
- 运行：`python adapters/run_case_human.py --case <案例ID>`（默认 C01）。