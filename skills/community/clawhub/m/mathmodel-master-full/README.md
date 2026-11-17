# Mathmodel Master - 数模大师

精通数学建模竞赛全流程的 AI 专家，覆盖读题分析、模型构建、算法编程与 LaTeX 论文撰写。

## 类型

Agent 型（单个 AI 专家）

## 功能

- **问题分析与建模**：快速理解题目背景，提取关键变量与约束条件，选择合适的数学模型
- **算法实现与求解**：Python/MATLAB 完整可运行代码，规范注释与结果展示
- **LaTeX 论文撰写**：基于 cumcmthesis.cls（XeLaTeX），生成 8 章结构完整国赛论文
- **数据预处理与可视化**：缺失值处理、异常值检测、专业图表绘制
- **敏感性分析与模型检验**：灵敏度分析、结果合理性讨论与模型创新提炼

## 使用示例

- "帮我分析这道数学建模题目，给出完整建模思路、算法实现和 LaTeX 论文"
- "根据以下模型和结果，生成一篇 LaTeX 格式的数学建模竞赛论文"
- "帮我编写 Python/MATLAB 代码实现这个数学模型并求解优化问题"

## 安装

将专家包目录放到专家目录下：

```
~/.workbuddy/plugins/marketplaces/my-experts/plugins/mathmodel-master/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir> --session-id <your-session-id>
```

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir>
```
