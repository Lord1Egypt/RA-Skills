# [量表名称] 标准化研究报告

> **检索日期**：{retrieval_date}  
> **文档版本**：v{version}  
> **最后更新**：{last_updated}

---

## 一、量表简介

### 1.1 背景及发展历程

**开发背景**：
{background_description}

**开发团队**：
- 主要作者：{authors}
- 开发年份：{year}
- 所属机构：{institution}

**理论基础**：
{theoretical_basis}

### 1.2 版本历史

| 版本 | 发布日期 | 更新内容摘要 |
|------|---------|-------------|
| {version_latest} | {date_latest} | {changes_latest} |
| {version_prev} | {date_prev} | {changes_prev} |

> **当前最新版本**：{version_latest}（{date_latest}）

### 1.3 应用领域

**科研领域**：
- 临床试验：{clinical_trial_usage}
- 观察性研究：{observational_usage}

**临床实践**：
{clinical_practice_usage}

**监管认可**：
- FDA：{fda_status}
- EMA：{ema_status}
- NMPA：{nmpa_status}

**指南推荐**：
{guideline_recommendations}

### 1.4 量表内容

**基本信息**：
- 条目数量：{item_count}
- 维度结构：{dimensions}
- 评分等级：{rating_scale}
- 数据类型：{data_type}

**评分公式**：
```
{scoring_formula}
```

**得分解读**：
| 得分范围 | 严重程度 | 临床意义 |
|---------|---------|---------|
| {range_1} | {severity_1} | {interpretation_1} |
| {range_2} | {severity_2} | {interpretation_2} |

### 1.5 官方量表全文 ⚠️

**获取状态**：{full_text_status}

**PDF 下载**：
- 下载链接：[{scale_name} Official PDF]({pdf_url})
- 本地路径：`/Users/wangyafei/Downloads/scales/{scale_name}_official.pdf`
- 文件大小：{file_size}

**量表条目预览**：
（如为截图，此处插入图片）

| 部分 | 条目示例 | 评分方式 |
|------|---------|---------|
| {section_1} | {item_example_1} | {scoring_1} |
| {section_2} | {item_example_2} | {scoring_2} |

> **注意**：完整量表请下载上方 PDF 文件。量表版权归 {copyright_owner} 所有，仅限学术研究使用。

---

## 二、版权与授权信息

### 2.1 版权方信息

**版权所有者**：{copyright_owner}

**授权类型**：
- 学术研究：{academic_license}
- 商业用途：{commercial_license}

**联系方式**：
- 机构：{contact_organization}
- 邮箱：{contact_email}
- 网站：{contact_website}

**申请流程**：
{license_process}

### 2.2 中文版信息

**翻译版本**：
- 翻译团队：{translation_team}
- 翻译年份：{translation_year}
- 文化调适：{cultural_adaptation}

**信效度数据**：
| 指标 | 数值 | 评价标准 |
|------|------|---------|
| Cronbach's α | {cronbach_alpha} | >0.7 可接受 |
| 结构效度 | {construct_validity} | CFI>0.9, RMSEA<0.08 |
| 重测信度 | {test_retest} | ICC>0.7 |

---

## 三、CDISC 编程

### 3.1 标准 aCRF 与受控术语

**推荐 Domain**：
| 标准 | 推荐 Domain | 置信度 | 依据 |
|------|-----------|--------|------|
| SDTM | {sdtm_domain} | {confidence_sdtm} | {basis_sdtm} |
| ADaM | {adam_domain} | {confidence_adam} | {basis_adam} |

**变量命名建议**：
```
QSCAT = "{category}"
QSTESTCD = "{test_code}"
QSTEST = "{test_name}"
QSSTRESN = {score_variable}
```

**受控术语**：
{controlled_terminology}

### 3.2 SDTM 实现

**Domain 选择**：{sdtm_domain}

**变量映射**：
| 量表条目 | SDTM 变量 | 说明 |
|---------|----------|------|
| {item_1} | QSSTRESN1 | {desc_1} |
| {item_2} | QSSTRESN2 | {desc_2} |

**数据集示例**：
```sas
data QS;
  length USUBJID $20 QSCAT $30 QSTESTCD $8 QSTEST $40 QSSTRESN 8;
  label QSCAT = "Questionnaire Category"
        QSTESTCD = "Question Short Name"
        QSTEST = "Question Name"
        QSSTRESN = "Numeric Result";
datalines;
;
run;
```

### 3.3 ADaM 实现

**分析数据集**：{adam_dataset}

**衍生变量**：
| 变量名 | 衍生逻辑 | 说明 |
|--------|---------|------|
| {var_1} | {derivation_1} | {desc_1} |
| {var_2} | {derivation_2} | {desc_2} |

**访视/观测 Flag**：
```sas
/* 基线 Flag */
ABLFL = (VISITN = 1);

/* 分析 Flag */
AVALFL = (MISSING_COUNT <= &max_missing);
```

---

## 四、统计分析

### 4.1 数据类型与分布特征

**数据类型**：{data_type}

**分布特征**：
- 正态性检验：{normality_test}
- 偏度/峰度：{skewness_kurtosis}
- 建议处理方法：{distribution_handling}

### 4.2 缺失值处理

**条目级缺失规则**：
> {item_missing_rule}

**访视级缺失处理**：
| 方法 | 适用场景 | 优缺点 |
|------|---------|--------|
| LOCF | 短期研究 | 简单但可能低估变异 |
| 多重插补 | 缺失率>5% | 更准确但复杂 |
| 完整病例 | 缺失完全随机 | 简单但损失样本量 |

**核心程序（SAS）**：
```sas
/* 条目缺失处理 */
%macro handle_missing(data=, score_var=, max_missing=);
  data &data;
    set &data;
    missing_count = nmiss(of &score_var);
    if missing_count <= &max_missing then do;
      /* 计算平均分或插补 */
    end;
    else do;
      &score_var = .;
    end;
  run;
%mend;
```

**核心程序（R）**：
```r
# 条目缺失处理
handle_missing <- function(data, score_cols, max_missing = 2) {
  data$missing_count <- rowSums(is.na(data[, score_cols]))
  data$score <- ifelse(data$missing_count <= max_missing,
                       rowMeans(data[, score_cols], na.rm = TRUE),
                       NA)
  return(data)
}
```

### 4.3 常规分析模型

**描述性统计**：
```sas
proc means data=analysis n mean std median min max;
  var score baseline_change;
  class treatment_group;
run;
```

**组间比较**：
| 场景 | 推荐方法 | 核心程序 |
|------|---------|---------|
| 两组连续变量 | t 检验 | `proc ttest` |
| 多组连续变量 | ANOVA | `proc glm` |
| 非正态分布 | Wilcoxon/Kruskal-Wallis | `proc npar1way` |
| 分类变量 | Chi-square/Fisher | `proc freq` |

**纵向分析（MMRM）**：
```sas
proc mixed data=analysis method=ml;
  class usubjid visit treatment_group;
  model score = treatment_group visit treatment_group*visit baseline / solution ddfm=kr;
  repeated visit / type=un subject=usubjid;
  lsmeans treatment_group visit treatment_group*visit / diff;
run;
```

**协方差矩阵选择**：
| 矩阵类型 | 适用场景 | 选择依据 |
|---------|---------|---------|
| UN (无结构化) | 访视数少 (<5) | AIC/BIC 最小 |
| AR(1) (自回归) | 等间隔访视 | 相邻访视相关性高 |
| CS (复合对称) | 相关性恒定 | 简化模型 |

### 4.4 探索性分析

**二分类转换**：
```sas
/* 达标率分析 */
data analysis;
  set analysis;
  responder_50 = (baseline_change <= -0.5 * baseline);
  responder_75 = (baseline_change <= -0.75 * baseline);
run;

proc freq data=analysis;
  tables treatment_group * responder_75 / chisq;
run;
```

**时间 - 事件分析**：
```sas
/* 首次达标时间 */
proc phreg data=analysis;
  model time_to_response * censored(0) = treatment_group baseline;
  hazardratio treatment_group;
run;
```

**风险因素挖掘**：
```r
# LASSO 回归筛选预后因素
library(glmnet)
x <- model.matrix(~ age + sex + baseline + comorbidities, data)[,-1]
y <- data$response
cv_fit <- cv.glmnet(x, y, family = "binomial", alpha = 1)
coef(cv_fit, s = "lambda.min")
```

### 4.5 结果呈现

**Table 模板 - 基线特征**：
| 变量 | 治疗组 (N={n1}) | 对照组 (N={n2}) | P 值 |
|------|---------------|---------------|-----|
| 年龄 (岁) | {mean1} ± {sd1} | {mean2} ± {sd2} | {p1} |
| 性别 (男%) | {n1_male} ({pct1}%) | {n2_male} ({pct2}%) | {p2} |
| 基线评分 | {mean1} ± {sd1} | {mean2} ± {sd2} | {p3} |

**Table 模板 - 主要疗效**：
| 指标 | 治疗组 | 对照组 | 差异 (95%CI) | P 值 |
|------|--------|--------|-------------|-----|
| LS Mean 变化 | {lsmean1} | {lsmean2} | {diff} ({ci}) | {p} |
| 应答率 (%) | {rate1}% | {rate2}% | {or} ({ci}) | {p} |

**Figure 模板 - 趋势图**：
```
各访视点评分变化趋势
│
│  ● 治疗组
│  ▲ 对照组
│
└────────────────────────→ 访视
```

---

## 五、参考文献

1. {reference_1}
2. {reference_2}
3. {reference_3}

---

## 附录

### A. 检索策略记录
| 维度 | 检索词 | 数据源 | 命中数 |
|------|--------|--------|--------|
| 背景 | {search_bg} | PubMed | {hits_bg} |
| 版权 | {search_copyright} | Mapi | {hits_copyright} |
| CDISC | {search_cdisc} | CDISC 官网 | {hits_cdisc} |

### B. 量表全文获取记录
**获取方式**：{full_text_method}（PDF 下载 / 屏幕截图）

**检索来源**：
1. {source_1}
2. {source_2}

**文件信息**：
- 文件名：{file_name}
- 大小：{file_size}
- 路径：{file_path}

---

*本报告由医学量表 Skill 自动生成，仅供参考。关键信息（如版权、CDISC 映射）需人工确认。*
