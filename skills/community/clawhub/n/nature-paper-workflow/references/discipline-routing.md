# 学科识别决策树与分支路由

> 配套主 skill: [SKILL.md](../SKILL.md)
> 版本: 2.0.0 新增

## 设计目标

`nature-paper-workflow` v2.0.0 起支持多学科路由。在主工作流之前增加 **Pre-Phase 学科识别** 步骤，将任务分流到 STEM 分支（默认）或 Econ 分支（可选），避免不同学科写作哲学混淆。

## 学科识别决策树

```
用户输入
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 1: 学科信号扫描                            │
├─────────────────────────────────────────────────┤
│ 扫描以下三类信号：                              │
│  ① 关键词（学术词汇 / 期刊名 / 方法名）         │
│  ② 文件类型（.dta / .do / .R / .pdf / .csv）    │
│  ③ 上下文（系数 / 标准误 / 蛋白 / 细胞 / n 值）  │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 2: 信号计数与分流                          │
├─────────────────────────────────────────────────┤
│ • Econ 信号 ≥ 2 且 STEM 信号 = 0 → Econ 分支   │
│ • STEM 信号 ≥ 1 且 Econ 信号 = 0 → STEM 分支   │
│ • 两类信号都有 → 信号冲突，问 1 个问题确认      │
│ • 两类信号都没有 → 默认 STEM 分支               │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 3: 分支可用性校验                          │
├─────────────────────────────────────────────────┤
│ • Econ 分支：检查 ~/.claude/skills/econ-write/  │
│   是否存在。不存在 → 提示用户安装 econ-* 扩展包 │
│ • STEM 分支：默认可用，无需校验                 │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Step 4: 路由到对应分支                          │
├─────────────────────────────────────────────────┤
│ • STEM 分支 → 走 12 阶段工作流（Phase 0a-7b）   │
│ • Econ 分支 → 走 6 阶段经济学工作流（E-0~E-5）  │
└─────────────────────────────────────────────────┘
```

## 学科信号清单

### 经济学信号（Econ Signals）

#### 关键词信号
- **方法名**：DiD / 双重差分 / IV / 工具变量 / RDD / 断点回归 / RCT / 随机对照试验 / event study / 事件研究 / synthetic control / 合成控制 / panels / 面板数据 / binscatter
- **统计概念**：基准回归 / 稳健性检验 / 机制检验 / 异质性分析 / 平行趋势 / 安慰剂 / 工具变量外生性 / 弱工具变量 / 第一阶段 / F 统计量 / 聚类标准误 / 固定效应 / 时间固定效应 / 个体固定效应
- **期刊名**：经济研究 / 管理世界 / 中国工业经济 / 经济学季刊 / AER / American Economic Review / QJE / Quarterly Journal of Economics / JPE / Journal of Political Economy / Econometrica / REStud / Review of Economic Studies / AEJ / Journal of Finance / Journal of Public Economics
- **学术角色**：Cochrane / McCloskey / Shapiro / Bellemare / Goldin / Glaeser / Kremer

#### 文件类型信号
- `.dta`（Stata 数据文件）
- `.do` / `.dofile`（Stata 脚本）
- `.R` / `.Rmd`（R 脚本，需配合经济学上下文）
- `.log` 含 Stata/R 输出（含 coef / se / p-value 表格）

#### 上下文信号
- "系数"、"显著性"、"标准误"、"p 值"、"样本量"、"固定效应"、"聚类"
- "main table"、"robustness table"、"heterogeneity table"、"mechanism table"
- "三线表"、"回归表"
- 提及"主回归"、"稳健性"、"机制"、"异质性"四类表
- 提及"事件研究图"、"平行趋势图"、"地图"

### STEM 信号（STEM Signals）

#### 关键词信号
- **期刊名**：Nature / Science / Cell / Nature Methods / Nature Neuroscience / Nature Biotechnology / Nature Physics / Nature Chemistry / Nature Materials / PNAS / Nature Communications
- **方法名**：IMRAD / 蛋白印迹 / 免疫荧光 / CRISPR / RNA-seq / 单细胞 / 膜片钳 / fMRI / 质谱 / 冷冻电镜 / 同步辐射 / 第一性原理 / DFT / 分子动力学
- **结构名**：Abstract / Introduction / Methods / Results / Discussion / Conclusion / Figures / Tables / Extended Data / Supplementary
- **统计概念**：n 值 / 重复数 / 多重比较校正 / Bonferroni / FDR / ANOVA / t 检验 / 卡方 / p 值校正 / 效应量 / 置信区间

#### 文件类型信号
- `.pdf`（论文 PDF）
- `.csv` / `.tsv`（实验数据）
- `.fasta` / `.fastq` / `.pdb` / `.cif`（生物/结构数据）
- `.tif` / `.png` 含显微镜图像

#### 上下文信号
- "claim"、"panel"、"图注"、"一图一主张"
- "实验组"、"对照组"、"重复次数"、"生物学重复"、"技术重复"
- "数据可用性声明"、"FAIR"、"accession number"
- 提及"引言"、"方法"、"结果"、"讨论"四段

## 信号冲突仲裁

当输入同时包含 STEM 信号和 Econ 信号时（如"用经济学方法分析医学数据"），按以下规则仲裁：

1. **数据/方法 vs 应用领域**：以方法为主导。例如"用 DiD 分析医疗政策"→ Econ 分支（方法是 DiD，应用是医疗政策）
2. **期刊导向 vs 内容**：以期刊为导向。例如"投 Nature Methods 讲 DiD 方法学"→ STEM 分支（投 Nature 系列）
3. **显式学科声明**：用户明示学科时，直接采用，不做信号计数
4. **冲突无法仲裁**：问 1 个问题确认 ——"这篇论文主要投稿 Nature 系列（理工科）还是经济管理类期刊？"

## 分支映射表

### STEM 分支（默认）
- **工作流**：12 阶段（Phase 0a-7b）+ 5 衍生场景
- **子技能数**：35 个
- **核心写作 skill**：`nature-writing`（IMRAD + 投稿包）
- **核心表图 skill**：`nature-figure`（科研图）
- **核心润色 skill**：`nature-polishing`（SCI 英文 + LaTeX）
- **核心期刊 skill**：`nature-portfolio-playbook`（Nature 系列定位）

### Econ 分支（可选）
- **工作流**：6 阶段（E-0~E-5），详见 [econ-workflow.md](econ-workflow.md)
- **子技能数**：5 个 econ-* + 共享基础设施
- **核心写作 skill**：`econ-write`（英文）/ `cn-top-econ-writing`（中文）
- **核心表图 skill**：`econ-table-figure-design`（三线表 + 回归图）
- **核心路由 skill**：`econ-writing-workflow`（11 类任务分类）
- **多代理升级**：`econ-writing-workflow-multiagent`（复杂项目）

## 跨学科共享基础设施

以下子技能跨学科通用，两个分支都可调用：

| 功能 | 共享子技能 | 说明 |
|---|---|---|
| 项目初始化 | `paper-bootstrap` | 目录结构 + 状态文件，跨学科适用 |
| 引用核验 | `nature-ref-verifier` + `citation-verifier` + `reference-audit-guide` | 引用准确性 + BibTeX 格式，跨学科适用 |
| 投稿预检 | `submission-audit` | 通用投稿预检清单 |
| 审稿模拟 | `nature-reviewer` | 按学科视角调整审稿维度 |
| 返修回复 | `nature-response` | 逐点回复 + cover letter + 标红修改 |

## 分支切换规则

- **STEM → Econ**：用户中途转向经济学任务时，重新走 Pre-Phase 学科识别
- **Econ → STEM**：用户中途转向 STEM 任务时，重新走 Pre-Phase 学科识别
- **不混合**：单次任务不跨学科分支，避免写作哲学混淆（如 IMRAD 与经济学论证逻辑不兼容）

## 边界情况

### 跨学科论文（如经济政策 + 流行病学数据）
- 优先看投稿目标：投经济学期刊 → Econ 分支；投医学/公共卫生期刊 → STEM 分支
- 若用户未明示投稿目标，问 1 个问题确认

### 计量经济学方法学论文（投 Econometrica）
- 走 Econ 分支，主要用 `econ-write` 的 Theory 模式

### 实验经济学论文（RCT 投 AER）
- 走 Econ 分支，主要用 `econ-write` 的 Empirical 模式 + `econ-table-figure-design` 的 RCT 表

### 神经经济学论文（投 Nature Neuroscience）
- 走 STEM 分支，主要用 `nature-writing` + `nature-figure`

## 安装校验

### STEM 模式（默认）
- 无需额外校验，35 个 STEM 子技能已安装即可

### Econ 模式
- 检查 `~/.claude/skills/econ-write/SKILL.md` 是否存在
- 不存在时提示用户：
  ```
  ⚠️ 经济学分支需要 econ-* 扩展包（5 个子技能）

  安装命令：
  git clone https://github.com/juliaError/econ-TopJournal-writing-Skill.git
  # 然后将 skills/ 下的 5 个子目录复制到 ~/.claude/skills/

  注意：econ-* 扩展包采用 CC BY-NC 4.0 许可（非商用）
  ```

### 全科学模式
- STEM + Econ 都装，自动学科识别
