# 机器学习工程师技能库

> AI Agent Skills for Machine Learning Engineers —— ML 全流程、深度学习、计算机视觉、PyTorch 工程

## 定位

为独立开发者和个人 ML 工程师提供一套 AI 技能，覆盖从传统机器学习到深度学习、从模型训练到工程部署的完整工作流。

## 核心理念

> ML 工程不分建模和工程——好模型需要好代码，好代码需要好流程。

- **从简单开始** — 先用传统 ML 建立基线，再考虑深度学习
- **可复现优先** — 固定随机种子、记录超参、版本化数据
- **关注数据，不只是模型** — 数据质量决定模型上限
- **工程标准不妥协** — 即使是研究代码也要有清晰的结构

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| ML 基础 | `machine-learning` | ML 全流程：JAX/Scikit-learn、特征工程、模型选择与评估 | [衍生](https://skills.sh/mindrally/skills/machine-learning) |
| 深度学习 | `deep-learning-pytorch` | PyTorch 深度学习：Transformers、扩散模型、Gradio 部署 | [衍生](https://skills.sh/mindrally/skills/deep-learning-pytorch) |
| 计算机视觉 | `computer-vision-opencv` | 图像处理、目标检测、视频分析、OpenCV+PyTorch | [衍生](https://skills.sh/mindrally/skills/computer-vision-opencv) |
| 工程实践 | `pytorch-patterns` | PyTorch 最佳实践：训练管线、数据加载、模型架构设计 | [衍生](https://skills.sh/affaan-m/everything-claude-code/pytorch-patterns) |
| AI 应用 | `claude-agent-sdk` | 用 Claude API / Agent SDK 构建 AI 应用与 Agent：Messages API、流式、工具调用、Agent 编排 | [衍生](https://skills.sh/bobmatnyc/claude-mpm-skills/anthropic-sdk) |
| AI 工程 | `mcp-server-generation` | 生成 Python MCP Server：stdio/streamable-http 脚手架、tool/resource/prompt 定义、MCP Inspector 调试 | [衍生](https://skills.sh/github/awesome-copilot/python-mcp-server-generator) |
| Agent 评测 | `agent-evaluation` | 评估 AI Agent 输出质量与行为：工具调用准确率、答案质量、回归评测（数据集+评分器+追踪） | [衍生](https://skills.sh/mlflow/skills/agent-evaluation) |

## 快速开始

整库安装：

```bash
npx skills add skills-repo/machine-learning-engineer -g -y
```

按需安装子技能：

```bash
npx skills add skills-repo/machine-learning-engineer@machine-learning -g -y
npx skills add skills-repo/machine-learning-engineer@deep-learning-pytorch -g -y
npx skills add skills-repo/machine-learning-engineer@computer-vision-opencv -g -y
npx skills add skills-repo/machine-learning-engineer@pytorch-patterns -g -y
npx skills add skills-repo/machine-learning-engineer@claude-agent-sdk -g -y
npx skills add skills-repo/machine-learning-engineer@mcp-server-generation -g -y
npx skills add skills-repo/machine-learning-engineer@agent-evaluation -g -y
```

## 推荐工作流

```
数据探索 → 基线建模 → 深度学习 → 模型部署
machine-     machine-     deep-        pytorch-
learning     learning     learning     patterns
                          pytorch
              computer-
              vision-opencv
```

## 许可

MIT
