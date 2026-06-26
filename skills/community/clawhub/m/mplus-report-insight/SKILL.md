***

## name: mplus-deep-insight                           version: 1.0.1                                                   description: 自动解析 Mplus 输出文件，提取拟合指数与标准化参数，生成 APA 风格图表和可直接引用的 PDF 分析报告。专为心理学、管理学、教育学等社科研究者设计。                    trigger-keywords: Mplus, SEM, CFA, 结构方程, 验证性因子分析, 模型拟合, 路径系数, 报告生成 author: Your Name license: MIT tags: [Mplus, SEM, CFA, data-analysis, report-generation, psychology, research]

# 🔬 Mplus 深度洞察报告生成器

你是否每次打开 Mplus 的 `.out` 文件都要用肉眼找 χ²、CFI、RMSEA？ 是否手动将一堆数字复制到 Excel 里制图，只为给导师看模型拟合好不好？ 这个助手能自动完成这些机械工作，并为你生成**符合 APA 7 标准的完整分析报告**。

## 🎯 适用场景

* 验证性因子分析（CFA）/ 结构方程模型（SEM）结果解读

* 多模型拟合比较

* 学位论文、期刊论文的结果图表制作

* 组会汇报前的快速数据整理

## 🧠 它能做什么

上传 Mplus 的 `.out` 文本文件，自动执行：

1. **文件校验**：确认是否为有效 Mplus 输出，检测必要模块是否存在

2. **统计量提取**：无条件适配不同版本格式，提取 χ²/df、CFI、TLI、RMSEA（含 90% CI）、SRMR、AIC、BIC 及 STDYX 标准化参数

3. **可视化图表**：生成 **不少于 3 张** 学术图表（仅使用蓝/橙/青绿三色，色盲友好）

   * 拟合指数阈值对比图

   * 标准化估计森林图（显著性着色）

   * 参数载荷排序图

4. **PDF 报告**：整合元数据、图表与分级解读，可直接插入论文或发送导师

5. **智能解读**：基于 Hu & Bentler (1999) 阈值给出严谨的分级结论，不做“一刀切”判断

## ⚙️ 工作流程

1. 用户上传或指定 `.out` 文件路径

2. 运行 `python scripts/validate.py` 进行格式校验

3. 运行 `python scripts/main.py -i 你的文件.out -o 报告.pdf`

4. 工具自动解析 → 制图 → 生成 PDF → 控制台预览关键结果

## 📂 项目结构

mplus-deep-insight/
├── SKILL.md
├── demo-input.txt
├── scripts/
│ ├── main.py # 核心：解析、制图、报告
│ ├── validate.py # 文件合法性校验
│ └── utils.sh # 一键环境安装
├── references/
│ ├── background.md # Mplus 输出背景知识
│ ├── operating-rules.md # 统计阈值与图表规范
│ └── examples.md # 典型使用案例
└── assets/
├── output-template.md
└── schema.json

&#x23;# 🚀 快速开始

&#x60;``bash

&#x23; 环境准备（仅首次）

bash scripts/utils.sh

source mplus-env/bin/activate

 

&#x23; 校验文件（确保是 Mplus 输出）

python scripts/validate.py my_model.out

 

&#x23; 生成报告（输出为 analysis_report.pdf）

python scripts/main.py -i my_model.out -o analysis_report.pdf

## 📊 示例效果

输入一份典型的 CFA 输出，生成的报告包含：

* 📋 报告元数据表（文件来源、Mplus 版本、生成时间）

* 📈 拟合指数对比图（χ²/df、CFI、TLI、RMSEA、SRMR + 阈值线）

* 🌲 标准化路径系数森林图（p<0.05 为蓝色，否则橙色）

* 📊 前 15 大载荷/路径系数排序图

* 📝 每张图一段基于数值的分级解释（优秀/可接受/欠佳）

* ✅ 综合结论与后续建模建议

&#x23;# 脚本

* `scripts/main.py` — 主分析脚本：解析、制图、生成 PDF

* `scripts/validate.py` — 快速校验文件是否为合法 Mplus 输出

* `scripts/utils.sh` — 一键安装 Python 依赖（matplotlib, pandas, reportlab, numpy）

 

&#x23;# 参考资料

* `references/background.md` — Mplus 输出格式与关键模块说明

* `references/operating-rules.md` — 模型拟合阈值与图表设计原则

* `references/examples.md` — 典型使用案例与命令示例

* `assets/schema.json` — 解析后的数据结构描述

## ⚠️ 注意事项与学术规范

* 前提条件：输入文件必须包含 MODEL FIT INFORMATION 和 STDYX Standardization 模块，否则报告不完整。

* 阈值说明：工具使用 Hu & Bentler (1999) 的推荐标准，但用户需结合自身领域和样本量灵活判断。

* 显著性声明：自动判定 p<0.05 为显著，未进行多重比较校正；若模型参数较多，请自行使用 Bonferroni 或 FDR 方法。

* 后果声明：报告为 AI 辅助生成，仅供初步参考，最终统计审核应由研究者负责。

*

