# Report Template / 报告模板（通用外壳 · Generic Shell）

> **🌐 Output language / 输出语言 (configurable, opt-in / 可配置、按需):**
> Output language follows the user's stated preference and is **not mandated**.
> - Default recommendation: bilingual `English / 中文` (both shown side by side) for ct- skills that follow the bilingual policy.
> - Single-language output (English-only or Chinese-only) is fully supported — just set the user's requested language.
> - In regulated clinical workflows where output language must be tightly controlled, use the user's single requested language only.
> / 输出语言**遵循使用者指定偏好，不做强制**。默认推荐双语 `English / 中文`（并列展示），对套用双语策略的技能；也完全支持单语输出（仅英文或仅中文），只需按使用者要求的语言即可；在输出语言须严格管控的受监管临床试验场景中，仅使用使用者指定的单一语言。
>
> **English / 中文:** By default, end every analysis with this structure + results; include the standalone R code block ONLY when the user explicitly asks for it. / 默认每次分析以该结构 + 结果收尾；仅当使用者明确要求时，才附上完整可运行的 R 代码块。

---

## Structure / 报告结构

> This is a **generic analysis-report skeleton** shared by every ct- skill.
> Replace the bracketed placeholders with your domain content; add or drop
> sections as the analysis requires. / 这是**全库通用的分析报告骨架**。把方括号占位符替换为你的领域内容；按分析需要增删章节。

### 1. Title / 标题
```
## 📊 [Analysis Type] Report / [分析类型] 报告
```

### 2. Context / 背景与设定
```
- **Scope / 范围**: [what is being analyzed]
- **Method / 方法**: [approach / engine used]
- **Data Source / 数据来源**: [input files / public registries / ...]
```

### 3. Input Parameters / 输入参数
```
- **Parameter 1 / 参数 1**: [value]
- **Parameter 2 / 参数 2**: [value]
```

### 4. Results / 计算结果
```
- **Primary result / 主要结果**: [value]
- **Secondary result / 次要结果**: [value]
```

### 5. Interpretation / 结果解释
```
[Plain-language explanation of what the result means]
[用通俗语言解释结果]
```

### 6. Assumptions / 前提假设
```
[model / distribution / independence assumptions, etc.]
```

### 7. Methodological Limits / 方法学限制
```
[approximation conditions / fallback simplifications]
```

### 8. Sensitivity / 敏感性建议
```
[how results change if a key input moves]
```

---

## ⚠️ On Request: Reproducible R Code / 按需提供：可复现的 R 代码

> **EN/CN:** Include this block ONLY when the user explicitly asks for the reproducible R code; it is hidden by default.

```markdown
---

## 📋 Reproducible R Code / 可复现的 R 代码

> Copy to R Studio or save as `.R` and run with `Rscript` to reproduce.

```r
# ============================================================
# [Analysis Title] — Standalone R Script
# [分析标题] - 可独立运行的 R 脚本
# Generated / 生成时间: [YYYY-MM-DD]
# Path / 计算路径: [engine used]
# ============================================================

# ---- 0. Setup (uncomment first run) / 环境准备 ----
# install.packages(c("[pkg1]", "[pkg2]"))

# ---- 1. Load packages / 加载包 ----
# library([pkg1])

# ---- 2. Parameters / 参数设置 ----
param1 <- [value]

# ---- 3. Calculate / 计算 ----
[core function calls with hardcoded values]

# ---- 4. Output / 输出 ----
cat("\n===== Result / 计算结果 =====\n")
```

**Run / 运行方式**:
- R Studio: paste into script window
- CLI / 命令行: `Rscript analysis.R`
```

---

## R Code Generation Rules / R 代码生成规则

| Rule 规则 | Description 说明 |
|:---------|:----------------|
| **Complete 完整** | install.packages / library / calc / output |
| **Hardcoded 硬编码** | Actual values, no placeholders |
| **Runnable 可复现** | Copy-paste executable in R |
| **Sanitized 脱敏** | Paths stripped, no subject data in output |
