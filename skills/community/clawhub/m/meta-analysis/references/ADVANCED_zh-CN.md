# 进阶参考 / Advanced Reference

> 本文件面向**开发者与高级用户**。普通用户只需阅读[对话使用指南](interactive_menu.md)即可。
>
> This file is for **developers and advanced users**. Ordinary users only need the [How to Use in a Chat](interactive_menu.md) section.

---

## 1. CLI 调用示例 / CLI Invocation Examples

### 通过 Python helper（技能侧）
```bash
cd meta-analysis
# 探测 coze 端点可达性（不发起分析请求）
python adapters/coze_client.py --health

# 运行分析（委派给 coze R 引擎）
python adapters/run_analysis.py ...

# 走生产路径冒烟一次完整请求（自动带归因 + 去重）
python scripts/run_meta.py <request.json>
```

> **coze 项目 R 引擎维护命令**（包安装、分发器运行、模块帮助等）**不在此发布**——它们位于
> `adapters/coze/DEV.md`（已被 git/clawhub 忽略，不进入发布包），仅供 coze 项目维护者使用。

### 直接调用 R（仅作参考——计算在 coze 端进行）
```r
library(metafor)
# 二分类 Meta
res <- metabin(event.e, n.e, event.c, n.c, sm="OR", method="DL", data=my_data)
forest(res)
funnel(res)
```

---

## 2. 双向求解模式 / Bidirectional Solving

当用户只有部分信息时，技能可双向求解：

| 已知 | 求解 |
|---|---|
| n, power, α, 效应量 → | 验证 power |
| power, α, 效应量, n → | 验证 n |
| 观测 I², k, n → | 评估异质性水平 |

---

## 3. 曲线模式 / Curve 模式

- **功效曲线**：效应量 → 不同 α 下的 power
- **异质性曲线**：I² vs. 剔除每个研究（leave-one-out）
- **NMA 排序曲线**：各治疗排序概率分布

---

## 4. 核心公式推导 / Core Formulas

### 4.1 随机效应模型 (DL)
```
θ̂_DL = Σ(w_i · θ_i) / Σ(w_i)
w_i = 1 / (v_i + τ̂²)
τ̂² = (Q - (k-1)) / (Σw_i - Σw_i²/Σw_i)
```

### 4.2 效应量转换
```
Cohen's d → logOR: logOR = d × π / √3
d → Hedges' g: g = J × d, J = 1 - 3/(4df - 1)
r → Fisher's z: z = 0.5 · ln((1+r)/(1-r))
OR → logOR: logOR = ln(OR), SE = (ln(upper) - ln(lower)) / (2 × 1.96)
```

### 4.3 异质性
```
I² = 100% × (Q - df) / Q
H² = Q / df
τ² = (Q - (k-1)) / (Σw_i - Σw_i²/Σw_i)  [DL 估计量]
```

### 4.4 贝叶斯 NMA (Stan)
```
y_i ~ Normal(θ_i, σ_i²)
θ_i = μ + τ · η_i
η_i ~ Normal(0, 1)
```

---

## 5. 系统与环境要求 / System & Environment Requirements

### R 包（必需）
| 包 | 版本 | 用途 |
|---|---|---|
| metafor | ≥3.0 | 核心 Meta 分析 (rma, escalc, forest, funnel) |
| meta | ≥5.0 | Metabin, metacont, metaprop 等 |
| netmeta | ≥2.0 | 频率学派 NMA |
| bayesmeta | ≥3.0 | 贝叶斯两组 Meta |
| multinma | ≥0.8 | 贝叶斯 NMA (Stan，可选后端) |
| gemtc | ≥2.0 | 贝叶斯 NMA (JAGS) |
| esc | ≥0.5 | 效应量转换 |
| clubSandwich | ≥0.5 | CR2 稳健标准误 |
| robumeta | ≥2.0 | RVE 处理依赖效应 |
| dosresmeta | ≥2.0 | 剂量反应 Meta |
| ~~survmeta~~ | — | 已下架，改用 metafor 逆方差合并 logHR |
| mada | ≥1.0 | 诊断 Meta |
| metagear | ≥0.7 | PRISMA 2020 流程图 (plot_PRISMA；仅 prisma_flow 任务用) |
| ggplot2 | ≥3.0 | 可视化 |
| gridExtra | ≥2.0 | 多面板图 |
| forestploter | ≥1.1 | 出版级森林图（替代 ggforestplot） |
| svglite | ≥2.0 | 可编辑 SVG 导出 |

### Python（仅 helper）
- Python 3.10+，**无需第三方包**（仅 stdlib）
- 推荐 Anaconda：`C:\Tools\anaconda3\python.exe`

### 操作系统
- Windows 10/11（主要），macOS，Linux
- 大型 NMA 模型（Stan/JAGS）建议 8GB+ RAM

---

## 6. 常见错误排查 / Common Errors & Troubleshooting

| 错误 | 原因 | 修复 |
|---|---|---|
| `R package not found` | 缺少 R 包 | `install.packages("pkg")` |
| `Stan model compilation failed` | 缺少 C++ 工具链 | 安装 Rtools (Windows) 或 Xcode (macOS) |
| `MCMC did not converge` | 迭代次数不足或链混合差 | 增加 `iter`，检查 `Rhat > 1.01` |
| `Fisher scoring algorithm did not converge` | 稀疏数据或极端效应量；REMLE 无法收敛 | **数据问题，非引擎 bug**。尝试改用 `method="ML"` 或 `method="EB"`、剔除离群研究、用亚组降低异质性，或 k<5 时直接用固定效应模型 |
| 客户端输入校验类错误（`invalid 'pos'`、`NULL cov`、列长不匹配、`mean=NULL`） | 输入校验缺失：subset 位置越界、协变量为空、列长不等、缺少必填 `mean` | 检查输入：pos ≤ 研究数；协变量列必须在数据中；公式涉及列等长；必填参数补齐 |
| `I² = 0%` 但可见异质性 | 检测异质性功效低 | 用 Q 检验 p 值，考虑随机效应 |
| `Funnel plot asymmetry` | 真实发表偏倚或异质性 | 用 Egger 检验，考虑选择模型 |
| `netmeta inconsistency` | 违反可传递性假设 | 检查 node-split，考虑 meta-regression |
| `svglite output is raster` | 未安装 Cairo | 安装 Cairo R 包 |
| `UnicodeDecodeError` | 非 UTF-8 字符 | 用 `cp1252` 或 `utf-8 + errors='replace'` |

---

## 7. 完整文件结构 / Full File Structure

```
meta-analysis/
├── SKILL.md                       # 技能主定义（英文正文，ct-base 对齐）
├── AGENTS.md                      # 自改进约定（英文）
├── CHANGELOG.md                   # 版本/整改记录
├── README.md                      # 英文使用指南（顶部切换 README_zh-CN.md）
├── README_zh-CN.md                # 中文使用指南（顶部切换 README.md）
├── LICENSE                        # MIT
├── requirements.txt               # R 包清单
├── assets/
│   ├── icon.svg                   # 技能 Logo
│   └── icon.png                   # 位图版
├── scripts/
│   ├── i18n.py                    # 中英切换 helper（来自 ct-base）
│   ├── r_libs.py                  # R 调用 + 校验 + 脱敏（来自 ct-base）
│   ├── r_templates.py             # R 代码模板生成器
│   ├── r_meta_analysis_core.py    # 核心引擎模板
│   ├── r_effect_size_conversions.py
│   ├── r_network_meta_analysis.py
│   ├── r_stata_equivalents.py
│   ├── r_advanced_functions.py
│   ├── r_setup_packages.py
│   ├── check_integrity.sh         # 完整性自检
│   └── *.R                        # 生成的 R 脚本（via check_integrity.sh）
├── references/
│   ├── interactive_menu.md        # 对话使用指南
│   ├── ADVANCED.md                # 英文进阶参考
│   ├── ADVANCED_zh-CN.md          # 中文进阶参考
│   ├── language_policy.md         # 双语策略（来自 ct-base）
│   ├── report_template.md         # 报告骨架（来自 ct-base）
│   ├── units.md                   # 原子任务单元索引
│   ├── data_templates.md          # 分类型 CSV 模板
│   ├── revman_complete.md         # RevMan → R 1:1 代码映射
│   ├── stata_to_r_mapping.md      # Stata metareg/mvmeta → R 等价
│   ├── advanced_analysis.md       # 多元/多水平/IPD/剂量反应
│   ├── single_group_meta.md       # metaprop/metamean/metainc/metacor
│   ├── survival_meta.md           # metafor + KM 伪个体数据
│   ├── tsa_diagnostics.md         # TSA + Baujat + Drapery + 选择模型
│   ├── diagnosis_meta.md          # mada 双变量 + SROC
│   ├── bayesian_nma.md            # gemtc (主) / multinma (可选) 工作流
│   ├── esc_robust_meta.md         # esc 转换 + RVE
│   ├── review_workflow.md         # PRISMA 流程图 (metagear::plot_PRISMA) + agent 行为层筛选 + 数据提取
│   ├── r_packages.md              # 包清单
│   ├── citations.md               # 方法学引用
│   ├── references.md              # 引用列表
│   ├── advanced_api.md            # 复用接口
│   ├── svg_editing.md             # SVG 编辑工具与期刊格式转换
│   └── purpose_zh.md              # 中文 Purpose 文本镜像
```

---

## 8. 方法论参考文献 / Methodological References

### 核心文献
- Harrer M, Cuijpers P, Furukawa TA, Ebert DD. (2021). *Doing Meta-Analysis with R: A Hands-On Guide*. CRC Press.
- Viechtbauer W. (2010). Conducting meta-analyses in R with the metafor package. *J Stat Softw*, 36(3), 1–48.
- Balduzzi S, Rücker G, Schwarzer G. (2019). How to perform a meta-analysis with R: a practical tutorial. *Evid Based Ment Health*, 22(4), 153–160.
- Rücker G, et al. (2016). netmeta: Network Meta-Analysis using Frequentist Methods. *BMC Med Res Methodol*, 16, 1–8.
- Salanti G. (2012). Network meta-analysis in mental health. *Evid Based Ment Health*, 15(1), 16–20.

### R 包引用
- metafor: `citation("metafor")`
- meta: `citation("meta")`
- netmeta: `citation("netmeta")`
- gemtc: `citation("gemtc")`
- multinma: `citation("multinma")`
- bayesmeta: `citation("bayesmeta")`
- esc: `citation("esc")`
- clubSandwich: `citation("clubSandwich")`
- robumeta: `citation("robumeta")`
- dosresmeta: `citation("dosresmeta")`
- survmeta: `citation("survmeta")`
- mada: `citation("mada")`
- metagear: `citation("metagear")`

---

## 9. 示例实测记录 / Example Test Records（§16.6 实测闸门留痕）

> 测试日期 2026-08-20，依据 ct-base §16.6 逐示例实测：**7/7 通过**。计算类示例 2/3/4/7 经 coze 端点（`https://ct-meta.coze.site/run`）真实返回 `stats` + `figures` + `repro`；行为类示例 1/5/6 与 SKILL.md Triage（§5.2）及 `references/topic-selection.md` / `references/interactive_menu.md` 一致。完整报告见 `meta_readme_test/README_EXAMPLES_TEST_REPORT.md`。

| 示例 | 类型 | 实测状态 |
|---|---|---|
| 1 选择候选方向 / 5 网络 Meta 路由菜单 / 6 Vague grill-me | 行为类（选题/路由） | ✅ 通过 |
| 2 二分类 OR 配对 / 3 效应量转换 / 4 SMD+亚组 / 7 PRISMA 流程图 | 计算类（coze） | ✅ 通过 |

**变更留痕（2026-08-24）：**
- **示例 1 文案更新**：原示例按"Meta 类型"切分候选、且把泛化配对 Meta 列为首选（新颖性 3）；经一手文献核查，该泛化方向 2024 年已被 ≥5–6 篇大型 Meta 覆盖，原"首选推荐"事实站不住。已重写为**按证据空白 / 新颖性分层**，并引入真实去重核查依据：首选改为"非糖尿病 CKD 专属 Meta"，候选含"RAS 停药机制桥接""晚期 CKD"。行为类判定逻辑（不替用户拍板、不调用 R）不变，7/7 通过结论仍然有效。
- **选题行为固化**：将"按证据空白分层 + 去重核查"从 README 范例提升为技能**固定规则**。`references/topic-selection.md` 新增 **R7 规则**（候选方向排序须基于真实去重核查，不得把已饱和泛化方向列为首选）并在 Traps 第 14 条同步；`references/interactive_menu.md` 示例 6 已与 README 示例 1 同步重写（按证据空白排 3 候选）。
- **README 结构重排**：将「对话中使用（7 个示例）」前置到第 1 节，使**使用便利性优先**；把原先散落在最前、互相交叉的三个出站披露块（分析数据 / 元数据 / 错误报告）收敛为 README 第 5 节「数据与隐私说明」，表格化、去重 `query_origin`+`locale` 的重复描述，并加一句总结。内容与强制披露语义（ct-base §5 / §20.3）零丢失。
- **实测记录迁移**：原位于 README 的「示例实测记录（§16.6 实测闸门留痕）」属开发/QA 视角，对普通使用者无意义，已从 README 移除并迁移至此（第 9 节）。

---

**版本**: v1.7 | **许可**: MIT | **作者**: medstatstar, phoe-zip
