# R Package Guide & Installation / R 包功能详解与安装指南

> ⚠️ 本技能**不会自动安装**任何 R 包。所有依赖均需用户在自己的 R 环境中**手动安装**。下文仅说明各包用途与所需清单。

## 核心包对比 / Core Package Comparison

### 1. metafor (Core Engine, Required) / metafor（统计引擎，必装）

**安装**：手动在 R 控制台安装 `metafor` 包（本技能不自动安装）。

**核心函数**：

| 函数 | 功能 | 参数要点 |
|------|------|----------|
| `escalc()` | 计算效应量 | `measure="OR"/"RR"/"SMD"/"ROM"/"IRR"/"ZCOR"` |
| `rma()` | 元分析主模型 | `method="FE"/"REML"/"HK"/"ML"/"EB"/"DL"/"SJ"/"HS"/"GENQ"/"PMM"` |
| `rma.mv()` | 多水平/多元元分析 | `random = ~ 1 | study/outcome` |
| `forest()` | 森林图（基础） | `smlab`, `xlab`, `refline` |
| `funnel()` | 漏斗图 | `yvi`, `sei` |
| `bubble()` | 元回归气泡图 | `xlim`, `ylim` |
| `regtest()` | Egger 回归检验 | `model="lm"/"rma"` |
| `ranktest()` | Begg 秩相关检验 | 非参数 |
| `trimfill()` | 剪补法 | 自动补全缺失研究 |
| `leave1out()` | 逐一剔除法 | 敏感性分析 |
| `gosh()` | GOSH 图 | 全子集诊断 |
| `fsn()` | 失安全系数 | Rosenberg/Hunter |
| `robust()` | 稳健方差估计 | 多元元分析 |

**效应量 measure 参数对照表**：

| measure | 含义 | 输入数据格式 |
|---------|------|-------------|
| `OR` | 比值比(对数) | `ai, bi, ci, di` 四格表 |
| `RR` | 风险比(对数) | `ai, bi, ci, di` |
| `RD` | 风险差 | `ai, bi, ci, di` |
| `AS` | 反正弦差 | `ai, bi, ci, di` |
| `PETO` | Peto 法 | `ai, bi, ci, di` |
| `SMD` | 标准化均值差 | `n1i, m1i, sd1i, n2i, m2i, sd2i` |
| `SMDH` | Hedges' g (小样本校正) | 同上 |
| `SMCC` | 标准化均值变化 | `n, m1i, m2i, sd1i, sd2i, ri` |
| `ROM` | 均数比对数 | 连续型 |
| `BCOR` | 二列相关 | `ri, ni` |
| `ZCOR` | Fisher's Z 转换相关 | `ri, ni` |
| `HR` | 风险比 | 生存分析 |
| `IRR` | 发生率比(对数) | `xi, ti` |

### 2. meta (RevMan Compatible, Required) / meta（RevMan 兼容，必装）

**安装**：手动在 R 控制台安装 `meta` 包（本技能不自动安装）。

**核心函数**：

| 函数 | 功能 |
|------|------|
| `metabin()` | 二分类数据元分析 |
| `metacont()` | 连续型数据元分析 |
| `metagen()` | 通用倒方差法 |
| `metacor()` | 相关系数元分析 |
| `metaprop()` | 比例单组元分析 |
| `metarate()` | 发病率元分析 |
| `metaadd()` | 追加研究到现有分析 |
| `update.meta()` | 更新/修改分析 |
| `forest()` | RevMan 风格森林图 |
| `funnel()` | 漏斗图 |
| `metabias()` | 偏倚检验汇总 |
| `trimfill()` | 剪补法 |
| `fsn()` | 失安全系数 |
| `labbe()` | L'Abbé 图 |
| `bubble()` | 气泡图 |
| `forest.meta(addcols)` | 自定义森林图列 |

**meta 特有功能**：
- RevMan 文件导入/导出
- 自动计算效应量
- Cochrane Review 兼容输出

### 3. dmetar — 已移除非必需依赖 / dmetar — removed as non-essential

> **变更说明**：dmetar 体积大（依赖整套 easystats 生态 + metafor/meta/netmeta/robvis/ggplot2），
> 且本技能核心统计全部由底层包实现，故**不再依赖** dmetar，缺失时也不再提示安装。
> 原 dmetar 便捷封装函数的底层等价替代（无需安装 dmetar）：

| dmetar 函数 | 底层替代 | 实现 |
|------|------|------|
| `GOSH_plot()` | `metafor::gosh()` | `g <- gosh(res); plot(g)` |
| `InfluenceAnalysis()` | `metafor::influence()` | `plot(influence(res))` |
| `SubgroupAnalysis()` | `metafor::rma(mods=)` / `meta::metareg()` | 亚组分析 |
| `BubblePlot()` | `metafor::bubble()` | `bubble(res, mods=~cov)` |
| `MultiLevelMeta()` | `metafor::rma.mv()` | 多水平 Meta |
| `RiskOfBias()` (RoB 2.0) | `robvis` 包 | `robvis::rob_traffic_light(df, "ROB2")` |
| `TreatmentCoding()` | `netmeta::netmeta()` | 直接吃长表数据框 |
| `SingleArmMissing()` | `meta::metaprop()` | 单臂率；缺失用 `mice` |
| `power.analysis()` | `metapower` / 自写模拟 | 见 advanced_analysis.md |

> 仅需 RoB 交通灯图与功效分析两个常用便捷功能时，装两个轻量包即可：
> `install.packages(c("robvis", "metapower"))`

### 4. netmeta (Network Meta, Required) / netmeta（网状meta，必装）

**安装**：手动在 R 控制台安装 `netmeta` 包（本技能不自动安装）。

**核心函数**：

| 函数 | 功能 |
|------|------|
| `netmeta()` | 频率学派 NMA |
| `netgraph()` | 网络图 |
| `netleague()` | 联赛表 |
| `netrank()` | SUCRA/P-score 排序 |
| `netsplit()` | 节点拆分（一致性检验） |
| `netheat()` | 网络热图 |
| `netposet()` | 干预偏序 |
| `mnp()` | 多参数 NMA |

### 5. bayesmeta (Bayesian, Optional) / bayesmeta（贝叶斯，可选）

**安装**：手动在 R 控制台安装 `bayesmeta` 包（本技能不自动安装）。

**核心函数**：

| 函数 | 功能 |
|------|------|
| `bayesmeta()` | 贝叶斯随机效应模型 |
| `forest.bayesmeta()` | 森林图 |
| `forestplot.bayesmeta()` | 出版级森林图 |

### 6. Optional Enhancement Packages / 可选增强包

> **变更说明**：`survmeta`（CRAN 已下架）不再依赖，生存 HR 合并改由 `run_surv_meta()` 内部调用 `metafor::rma.uni` 逆方差法实现；`ggforestplot` 不再依赖，出版级森林图改由 `forestploter` 承接；`multinma` 从核心依赖降级为可选后端（需手动装 Stan 工具链），贝叶斯 NMA 主后端为 `gemtc`(JAGS)。

| 包 | 用途 | 来源 |
|----|------|------|
| `forestploter` | 出版级森林图（替代 ggforestplot；R4.6 适配） | CRAN 手动安装 |
| `metasens` | 敏感性分析（上限/下限法） | CRAN 手动安装 |
| `ggplot2` | 高级图形 | CRAN 手动安装 |
| `gridExtra` | 多图组合 | CRAN 手动安装 |
| `robumeta` | 稳健方差估计 | CRAN 手动安装 |
| `clubSandwich` | 稳健推断 | CRAN 手动安装 |
| `metaviz` | 交互式可视化 | CRAN 手动安装 |
| `metaDigitise` | 图表数字化 | CRAN 手动安装 |
| `robvis` | RoB 可视化 | CRAN 手动安装 |
| `gt` | 出版级表格 | CRAN 手动安装 |
| `multinma` | 贝叶斯 NMA（Stan，可选后端；需手动装 Stan 工具链） | CRAN 手动安装 |

---

## 安装说明 / Installation Notes

本技能**不自动安装**任何 R 包。所有依赖请用户在自己的 R 环境中手动安装。

**推荐安装清单**：
- 核心（必装）：`metafor`、`meta`、`netmeta`、`svglite`
- 推荐：`bayesmeta`（贝叶斯）、`forestploter`（出版级森林图）、`robvis` + `metapower`（替代原 dmetar 的 RoB 图 / 功效分析）
- 可选增强：`metasens`、`ggplot2`、`gridExtra`、`robumeta`、`clubSandwich`、`metaviz`、`metaDigitise`、`robvis`、`gt`

**辅助脚本（coze 项目维护者）**：包检测 / 安装清单脚本 `setup_packages.R` 位于 coze 项目 `src/r_engine/`，其运行方式见 `adapters/coze/DEV.md`（不随技能发布，仅供维护者）。

> ⚠️ 所有安装均为用户手动操作。本技能在任何运行路径下都不会调用包安装函数。

---

## 诊断与故障排除 / Diagnostics & Troubleshooting

| 问题 | 原因 | 解决 |
|------|------|------|
| `rma()` 奇异拟合 | 研究数 < 3 或异质性极大 | 检查数据，考虑 Peto 法或减少协变量 |
| `metacont()` NA 值 | 输入数据缺失 | 用 `na.omit()` 清洗或插补 |
| `netmeta()` 网络不连通 | 干预措施间缺少连接 | 验证干预编码，添加共同对照组 |
| I² = 100% | 真实异质性或模型问题 | 检查数据单位一致性 |
| 漏斗图不对称 | 发表偏倚 | 用 `trimfill()` 校正 |
| `bayesmeta` 收敛失败 | 先验过于分散 | 缩小 half-normal 先验尺度 |
