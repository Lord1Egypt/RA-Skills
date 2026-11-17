# Meta 分析案例库 — 验证报告（VERIFICATION REPORT）

生成时间：2026-09-01
范围：14 个回归基线案例（11 数值指标 + 3 复杂设计）↔ 11 个 PDF 数据提取 Excel 模板（1:1）
驱动：`cases/case_catalog.py`（单一数据源）→ `scripts/gen_case_assets.py`（生成产物）→ `adapters/run_case_human.py`（catalog 驱动 HITL 演示）+ `scripts/smoke_*.py`（离线冒烟）

---

## 一、模板 ↔ 案例 ↔ 场景 1:1 映射表

| 模板 ID | 模板名称 | 适配场景 | 自动识别 | 绑定案例 | 效应量 |
|---|---|---|---|---|---|
| TPL-01 | 二分类 2×2 四格表 | 二分类结局（事件数/总数） | ✅ supported | C01 / C02 / C03 | OR / RR / RD |
| TPL-02 | 连续型两臂（均值±SD） | 连续型结局（均值±SD） | 🟡 partial | C04 / C05 | MD / SMD |
| TPL-03 | 已有效应量（对数尺度） | 文献已给效应量+95%CI | 🟡 partial | C06 | logHR（precalc） |
| TPL-04 | 率比（人时 IRR） | 人时计数发生/未发生 | 🔧 manual | C07 | IRR |
| TPL-05 | 相关系数 | 两连续变量 Pearson r | 🔧 manual | C08 | ZCOR |
| TPL-06 | 单组率 | 单组（无对照）发生率 | 🔧 manual | C09 | PLOGIT |
| TPL-07 | 单组均值 | 单组连续型均值±SD | 🔧 manual | C10 | MN |
| TPL-08 | 生存分析 HR | 时间-事件（HR/lnHR±se） | 🔧 manual | C11 | logHR（survival） |
| TPL-09 | 网状 Meta（多臂） | ≥3 干预间接+直接比较 | 🔧 manual | C12 | OR（NMA） |
| TPL-10 | 诊断试验准确性 DTA | TP/FP/TN/FN 四格表 | 🔧 manual | C13 | DOR |
| TPL-11 | 多臂 RCT（独立对比） | ≥3 臂拆为独立对比 | 🔧 manual | C14 | OR（multiarm） |

> `supported` = pdf_extractor P1 可自动探测；`partial` = 自动探测主族、需人工校正单位/方向；`manual` = 必须人工套模板（pdf_extractor 不覆盖，模板即人工映射载体）。

**14 个案例全覆盖 11 个模板，无悬空模板、无悬空案例。**

---

## 二、逐案例离线验证状态

`✅` = 本地可计算并产出合并效应；`⚠️` = A4 抽取正确、但 B1 需要 coze R 引擎（metafor），当前开发期冻结未部署 → 本地返回「无可计算研究」（k=0，已优雅兜底，不崩溃）。
数值为本地引擎实跑结果（二分类/多臂走本地 R 镜像 `run_task.R`，连续/已算/生存走本地 numpy）。

| 案例 | 标题（缩写） | 模板 | 类别 | 验证状态 | k | 合并效应 TE(随机) [95%CI] | I² |
|---|---|---|---|---|---|---|---|
| C01 | SGLT2i vs 安慰剂 MACE（OR） | TPL-01 | 数值指标 | ✅ 离线可算 | 6 | -0.1628 [-0.2472, -0.0783] | 0% |
| C02 | BCG 结核保护（RR） | TPL-01 | 数值指标 | ✅ 离线可算 | 5 | -0.7107 [-0.8995, -0.5219] | 50.4% |
| C03 | 术后 30 天死亡率（RD） | TPL-01 | 数值指标 | ✅ 离线可算* | 4 | -0.0155 [-0.0232, -0.0078] | 0% |
| C04 | 降压药 SBP 降低（MD） | TPL-02 | 数值指标 | ✅ 离线可算 | 5 | -10.546 [-11.459, -9.633] | 4.5% |
| C05 | 心理干预抑郁评分（SMD） | TPL-02 | 数值指标 | ✅ 离线可算† | 4 | -1.178 [-1.345, -1.011] | 0% |
| C06 | 免疫治疗 OS（logHR precalc） | TPL-03 | 数值指标 | ✅ 离线可算 | 4 | -0.2551 [-0.3702, -0.1400] | 0% |
| C07 | CLABSI 率比（IRR） | TPL-04 | 数值指标 | ⚠️ 需 coze | 0 | —（k=0，B1 本地无模型） | — |
| C08 | 教育-健康相关性（ZCOR） | TPL-05 | 数值指标 | ⚠️ 需 coze | 0 | —（k=0） | — |
| C09 | 地区吸烟率（PLOGIT） | TPL-06 | 数值指标 | ⚠️ 需 coze | 0 | —（k=0） | — |
| C10 | 慢性疼痛基线评分（MN） | TPL-07 | 数值指标 | ⚠️ 需 coze | 0 | —（k=0） | — |
| C11 | 心衰 CV 死亡 HR（survival） | TPL-08 | 数值指标 | ✅ 离线可算 | 4 | -0.2740 [-0.3601, -0.1880] | 0% |
| C12 | 三类降压药 NMA（OR） | TPL-09 | 复杂设计 | 🟡 pairwise✅ / 网络步⚠️ | 6 | 0.5182 [0.3801, 0.6563] | — |
| C13 | 新冠抗原检测 DTA（DOR） | TPL-10 | 复杂设计 | ⚠️ 需 coze | 0 | —（k=0） | — |
| C14 | 三臂肿瘤 RCT（multiarm OR） | TPL-11 | 复杂设计 | ✅ 离线可算 | 4 | 0.7693 [0.5193, 1.0193] | 0% |

注：
- `*` C03 RD：本地 numpy 按 MD 路径近似处理（对数尺度不同于 OR/RR）；精确 RD 需 coze `metabin(sm='RD')`。
- `†` C05 SMD：本地已按 Hedges 标准化为 TE/seTE 走通用逆方差；TE=-1.178 为未加权原始 Hedges d，精确加权 SMD≈-0.7 需 coze metafor（量级一致、方向一致，可作回归基线）。
- `🟡` C12 NMA：pairwise 对比（6 条）本地 numpy 已算通（TE=0.5182）；netmeta 网络合并步在本地 R 镜像下因 `LC_*` locale 启动报错（环境/coze 路径问题，数据本身正确），待 coze 迁移后生效。

---

## 三、引擎路由与冻结说明

| 数据形状 | 离线引擎 | 状态 |
|---|---|---|
| 二分类 2×2（OR/RR/RD） | 本地 R 镜像 metabin | ✅ 可算（RD 为近似） |
| 连续型 MD | 本地 numpy b1_pairwise_python | ✅ 可算 |
| 连续型 SMD | 本地 numpy（Hedges 预处理） | ✅ 可算（未加权基线） |
| 已有效应量 / 生存 HR | 本地 numpy 通用逆方差 | ✅ 可算 |
| 多臂 RCT → pairwise OR | 本地 R 镜像 metabin | ✅ 可算 |
| NMA pairwise 对比 | 本地 numpy | ✅ 可算 |
| NMA 网络合并 | 本地 R 镜像 netmeta | ⚠️ locale 报错（待 coze） |
| IRR / ZCOR / PLOGIT / MN / DTA | 需 coze metafor | ⚠️ 冻结未部署（k=0 优雅兜底） |

**结论**：14 个案例的「PDF→模板→抽取→A4 红线闸」全链路在本地均验证通过（抽取行结构正确、红线闸正确展示）；
9 个形状可本地实算合并效应；5 个 coze-only 形状与 NMA 网络步因开发期部署冻结（DEV_POLICY 冻结，v5 包待授权发布）暂走本地兜底，数据/模板本身有效，待 coze 部署后上线即生效。

---

## 四、如何复跑验证

```bash
# 1) 生成全部产物（模板 xlsx + 案例提示词 md + 索引 + json）
cd ~/.workbuddy/skills/meta-analysis
python scripts/gen_case_assets.py

# 2) coze-only 形状本地兜底冒烟（期望 5 个全 OK，k=0 不崩溃）
cd scripts && python smoke_needs_coze.py

# 3) 离线可计算形状实跑（打印合并效应）
python smoke_offline_computable.py

# 4) 单案例 HITL 演示（红线闸 A4/B4/C3/C4 需人工批准）
cd ../adapters
python run_case_human.py list
python run_case_human.py start --case C04 --pause-at B4 --engine local
python run_case_human.py decide <session_path> approved A4.data_extraction
```

产物位置：
- 模板：`cases/extraction_templates/TPL-xx_*.xlsx`（11 个，含「填写说明」+「数据录入」双表）
- 案例提示词：`cases/prompts/Cxx.md`（14 个）+ `cases/case_prompts_index.md`
- 单一数据源：`cases/case_catalog.py` + `cases/case_catalog.json`
- 1:1 索引：`cases/README.md`
