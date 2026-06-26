---
name: paper2diagram
description: 论文 PDF → 方法/结构抽取 → 学术评审式总结 → 多张论文风格配图（依托 Gemini + nano_banana 网关）。
homepage: https://clawhub.ai/
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["python3"],"env":["GEMINI_API_KEY","BANANA_PRO_API_KEY"],"config":[]},"primaryEnv":"GEMINI_API_KEY"}}
---

## 简介

Paper2diagram 是一个面向科研工作者的「论文图文解析与可视化」技能，适合处理方法类/架构类论文（尤其是 CV / 医学图像 / 表征学习方向）。

它可以帮助代理完成：

- 读取本地论文 PDF；
- 自动聚焦到 Method / Architecture 章节；
- 抽取主干网络结构与训练流程；
- 用「资深学术评审」的口吻生成结构化总结（研究背景 / 核心创新点 / 实验结论 / 局限性等）；
- 调用网关中的 nano_banana 图像模型，自动生成多张论文风格配图（背景图、方法图、创新点示意图、实验结果条形图等），并保存在 `outputs/` 目录。

## 快速上手（给最终用户看的示例）

当你的代理已经启用了本技能后，可以直接在对话里说：

> 请帮我分析这篇论文 `/absolute/path/to/paper.pdf`，用学术评审的方式总结研究背景、方法和创新点，并按照医学图像论文的风格自动画出结构图和实验对比图。

代理预期会：

1. 调用本地 Python 工作流处理指定的 PDF；
2. 输出结构化总结：研究背景 / 核心创新点 / 方法与结构 / 实验结论 / 局限性；
3. 生成 3–5 张配图（方法主结构、创新点 callout、实验结果柱状图等），并返回：
   - 在线图片链接（由你的网关返回）；
   - 本地保存路径（`outputs/论文名__fig*.jpg`），方便直接写入报告或幻灯片。

## 环境与依赖

- **必须安装**：Python 3（命令为 `python3`）
- **需要网络访问**：连接到你自己配置的 LLM / 图像网关（例如 dongli gateway）
- **环境变量**（可以在 OpenClaw 的 `skills.entries.paper2diagram.env` 中配置，也可以在 shell 中设置）：
  - `GEMINI_API_KEY`
  - `GEMINI_BASE_URL`（示例：`https://api.dongli.work/v1beta`）
  - `GEMINI_MODEL`（示例：`gemini-3-pro`）
  - `BANANA_PRO_API_KEY`
  - `BANANA_PRO_BASE_URL`（示例：`https://api.dongli.work`）
  - `BANANA_MODEL`（示例：`nano_banana_pro-1K`）
  - `ENABLE_BANANA=true`

> 安全提示：本技能只会将你提供的 PDF 通过你自己配置的网关（Gemini + nano_banana）进行处理，不会上传到其他第三方服务；  
> 请仅在你信任的网关和私有环境中使用本技能，并在使用前阅读源代码。

## 本地部署（开发者 / 自托管）

ClawHub 只托管技能说明与元数据，实际的工作流逻辑在本仓库中实现，需要在本地拉取代码：

1. 克隆项目并安装依赖：

```bash
git clone <YOUR_REPO_URL> paper2diagram-agent
cd paper2diagram-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 按需填入 KEY
```

2. 确认 `.env` 中的 KEY 与 gateway 地址正确可用。

## 在 OpenClaw 中的典型调用流程

1. 代理收到用户指令（示例见「快速上手」）。
2. 代理通过本技能的工具，调用：

```bash
python -m app.openclaw_main local "<ABSOLUTE_PATH_TO_PDF>" 30
```

3. 工具返回：
   - `paper_analysis`：论文结构化总结；
   - `final_prompt`：为绘图模型生成的英文 Prompt 信息；
   - `render_results[]`：每张图的在线链接与 `local_image_path`。

## 其他说明

- 图像链接可能是短期有效的临时 URL，建议优先使用 `outputs/` 目录下的本地图片。
- 若出现 `403` 或 `503` 之类的错误，多半与网关额度、权限或模型名配置相关，本技能本身不会绕过网关安全策略。

