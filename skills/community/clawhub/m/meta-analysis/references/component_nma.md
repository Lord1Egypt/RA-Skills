# Component Network Meta-Analysis (CNMA) / 成分网络 Meta 分析

> 引擎：`netmeta::netcomb()`（加性/交互）/ `netmeta::discomb()`（断开网络）。
> coze 任务名 `cnma`；接口契约见 `coze_contract.md` §2（参数）/§3（task 枚举）/§4（出参字段）。
> **本文件只讲方法学选型与结果解读**，字段定义不重复。

---

## 1. 何时用 CNMA / When to use

普通 `nma` 把每个干预当作不可拆的**整体节点**。当干预本身是**多成分组合**（A+B、心理治疗+药物、
多药联合）时，若想知道**单个成分各自的贡献**、或想比较**没有直接研究过的组合**，才用 CNMA。

适用：
- 联合用药的**加性效应分解**（"在 P 之上加 X 能多降多少？"）
- 未直接比较的组合的间接外推（**以加性假设成立为前提**）
- 需要成分级证据汇总，而非干预级排序

不适用：
- 干预不可分解（"某品牌药 vs 安慰剂"没有成分结构）
- 已知存在明显**协同/拮抗**（先看 §4.3 的 `Q_diff`；被拒则加性解释不成立）
- 只想做干预排序 → 用 `nma_rank`

---

## 2. 数据格式：成分编码写进治疗标签

治疗名用 `sep_comps`（默认 `+`）拼接成分：`"P"` / `"P+X"` / `"P+X+Y"`。
**标签内空格自动 trim**（实测 `"Face-to-face CBT + SSRI"` → 成分 `Face-to-face CBT` 与 `SSRI`），
故 `"A + B"` 与 `"A+B"` 等价。

其余列与 `nma` 完全一致（arm-based：`treatment`/`event`/`n` 或 `treatment`/`te`/`sete`；
对比格式：`treat1`/`treat2` + 四格表或 `te`/`sete`）。

```
study   treatment   event   n
S1      P           10      50
S1      P+X         4       50
S2      P           12      60
S2      P+Y         5       60
...
```

---

## 3. 参数

| 参数 | 默认 | 作用 | 注意 |
|---|---|---|---|
| `sep_comps` | `+` | 成分分隔符 | **须为单个字符**；非法值回退 `+` 并告警 |
| `inactive` | 无 | 非活性/锚定成分（如 `["P"]`） | 声明后该成分不单独估计，**提升其余成分的可识别性**；有安慰剂臂时强烈建议声明 |
| `interaction` | `false` | 拟合成分交互模型（`C.matrix = createC(fit)`） | 成分数少时交互项不可识别、模型趋近标准 NMA；仅保留临床预设的少数交互 |
| `reference_group` | 无 | 参照干预 | 影响 `te_cnma`/`te_nma` 对照的基准 |
| `sm` | `OR` | 效应尺度 | 同 `nma`：二分类默认 OR，连续型须显式 `MD`/`SMD` |

---

## 4. 结果解读 / Reading the output

### 4.1 成分效应 `stats.extra.components`

每个成分的效应（相对参照/锚定）。`estimate`/`se`/`ci_low`/`ci_high`/`p` 为随机效应，
另附 `*_common`（固定效应）供参照。这是 CNMA 的**核心产出**——普通 NMA 给不出。

### 4.2 组合效应 `stats.pooled`

各**治疗**（含成分拼接名）在加性模型下的合并效应，标签见 `pooled.comparisons`。
尺度为**模型尺度**（如 logOR），与 `nma` 一致；展示层（forest）会做反转换。

### 4.3 加性假设检验 `stats.extra.additivity` —— **最关键**

| 字段 | 含义 |
|---|---|
| `Q_diff` / `df_diff` / `p_diff` | **标准 NMA 与加性 CNMA 的拟合差异检验**。`p ≥ 0.05` → 两者无显著差异，**加性解释可用**；`p < 0.05` → **加性假设被拒**，成分效应不可简单相加，需考虑交互或退回标准 NMA |
| `Q_additive` / `df_additive` / `p_additive` | 加性模型自身的异质性检验 |
| `additive` | 上述结论的布尔化（`p_diff > 0.05`） |

> ⚠️ **报告成分效应时必须同时报告 `Q_diff`。** 实测 `Linde2016` 真实网络（22 治疗 / 19 成分）
> 得 `Q_diff = 6.531, df = 2, p = 0.038` → 加性假设被拒；此时把成分效应直接相加会失真。
> 引擎在 `p_diff < 0.05` 时自动置 `cnma:additivity_violated` 告警。
> 自由度 ≤ 0（不可检验）时相关字段一律为 `null`，**不是 0**。

### 4.4 不可识别成分 `stats.extra.unidentifiable`

无锚点、或若干成分**总是同时出现**（如两臂恒为 `A+C` vs `B+C`，则 A/B 无法分离）时，
该成分效应**不可唯一识别**，返回 **`null`（绝不填 0）**，并置 `cnma:unidentifiable_components`。
处理：声明 `inactive` 锚点、合并为复合成分、或退回干预级 `nma`。

---

### 4.5 网络证据质量：CINeMA 六域（2026-09-14）

网络 Meta **不要直接套用普通 GRADE**——GRADE 缺少网络层面的核心域，且「间接性 /
不一致性」在两范式下含义不同。本技能对 `nma` / `nma_rank` / `cnma` 一律按
**CINeMA 六域**评估（实现：`adapters/quality_advice.py: cinema_grade`）：

| 域 | 判据（取自 stats） | 升级阈值 |
|---|---|---|
| 研究内偏倚 | stats **无** RoB 数据 → 恒 `unclear` | 须人工按研究逐条评级 |
| 报告偏倚 | `stats.bias.egger_p`（网络 Meta 通常无 → `unclear`） | < 0.10 → major |
| 间接性 | `extra.network.prop_direct` 的最小值 | < 0.25 major / < 0.50 some |
| 不精确性 | 研究数 + 各对比 CI 是否跨无效值 | 全部跨 → major |
| 异质性 | `stats.heterogeneity.I2`（**百分数**） | ≥ 75 major / ≥ 50 some |
| 不一致性 | CNMA 用 `extra.additivity.p_diff`；NMA 用 `extra.inconsistency.p` | < 0.05 major / < 0.10 some |

三条必须守住的规则：

1. **`unclear` 不等于「无关切」**——它表示统计侧拿不到该域的数据，须人工补做。
   整体评级只由**可评估域**决定，`unclear` 域单独计数并列出，绝不静默归零。
2. **不可检验 ≠ 已证明一致**。网络只含一种设计时 `Q.inconsistency` 的 `df ≤ 0`，
   此时不一致性域为 `unclear`，而不是「no concern」。
3. **CNMA 的两层不一致性不可互替**：`extra.inconsistency` 是底层网络的
   design-by-treatment 检验，`extra.additivity` 是成分模型自身的加性假设检验；
   报告时分别陈述。

参考：Nikolakopoulou A, et al. CINeMA: An approach for assessing confidence in the
results of a network meta-analysis. *PLoS Med*. 2020;17(4):e1003082.

## 5. 常见坑 / Pitfalls

| 坑 | 现象 | 处理 |
|---|---|---|
| 治疗名不含分隔符 | 每个治疗自成一个成分 → CNMA 退化为普通 NMA | 引擎置 `cnma:no_combination_labels` 告警并提示改用 `nma` |
| 无锚点就解读绝对效应 | 成分效应全为 `null` | 声明 `inactive`（如安慰剂）；或只解读相对差异 |
| 忽略 `Q_diff` 直接相加 | 加性不成立时结论失真 | 先看 `Q_diff`；被拒则改交互模型或退回 `nma` |
| 非 ASCII 成分标签 | netmeta 网络构建期对 locale 敏感（`LC_CTYPE=C` 下报错） | 用 ASCII 短码 + 字典；引擎置 `cnma:non_ascii_labels` 告警 |
| 网络不连通 | `netmeta()` 直接拒绝（`Network consists of N separate sub-networks.`） | 引擎自动改走 `discomb()`，并置 `cnma:disconnected_network` 告警；此时成分常不可识别 |
| 成分数多于独立对比数 | 交互项不可识别 | 保持 `interaction=false`，只列临床预设交互 |
| **多臂研究的研究数被高估**（2026-09-14 已修） | 报告写「4 项研究」实为 2 项 | 引擎已改按 `studlab` 去重（`.k_studies()`）；`stats.k` 与 `extra.network.n_studies` 必定相等，若不等即为回归 |

> **研究数 / 对比数口径（2026-09-14 自审修正）**：`prep` 是**对比级**数据，arm-based 多臂研究会被展开为 C(n,2) 行，故 `nrow(prep)` **不是**研究数。`stats.k`、`extra.network.n_studies`（按 `studlab` 去重）与 `extra.network.n_comparisons`（按 treat-pair 去重）现均走去重口径。历史教训：Linde2016 曾报 `k = 124`（实为 93 项研究），并与其同产物中的 `n_studies` 互相矛盾——**同族指标互相打脸是最好用的自检信号**。

---

## 6. 最小复现 / Minimal repro

引擎会随每次响应返回 `repro.r`（可直接 `source`）。等价核心代码：

```r
suppressMessages(library(netmeta))
prep <- data.frame(TE = ..., seTE = ..., treat1 = ..., treat2 = ..., studlab = ...)

fit <- netmeta::netmeta(TE = TE, seTE = seTE, treat1 = treat1, treat2 = treat2,
                        studlab = studlab, data = prep, sm = "OR")
nc  <- netmeta::netcomb(fit, sep.comps = "+")          # 加性 CNMA

nc$Comp.random      # 成分效应
nc$Comb.random      # 组合效应
nc$Q.diff           # 加性 vs 标准模型的拟合差异（关键）
nc$pval.Q.diff
nc$comps.unident    # 不可识别成分
forest(nc)          # 成分效应森林图（S3 派发 forest.netcomb）
```

断开网络时改用：
```r
nc <- netmeta::discomb(TE = TE, seTE = seTE, treat1 = treat1, treat2 = treat2,
                       studlab = studlab, data = prep, sm = "OR", sep.comps = "+")
```

---

## 7. 引用 / Citation

Rücker G, Petropoulou M, Schwarzer G. (2020). Network meta-analysis of multicomponent
interventions. *Biometrical Journal*, 62(3), 808-821.
（`netmeta` 的 CNMA 实现；加性成分模型的加性假设检验即 `Q.diff` 的来源。）
