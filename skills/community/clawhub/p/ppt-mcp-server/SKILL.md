---
slug: ppt-master-mcp
name: PPT Master MCP
version: 1.0.0
description: "AI 驱动的 PPT 生成工具，通过执行 python-pptx 代码自动创建专业 PowerPoint 演示文稿"
author: janson1983
tags:
  - ppt
  - powerpoint
  - presentation
  - mcp
  - python-pptx
  - office
repository: https://github.com/janson1983/ppt-master-mcp
license: MIT
language: python
runtime: python3
---

# PPT Master MCP

AI 驱动的 PPT 生成 MCP Skill，让 AI 自动编写并执行 python-pptx 代码，生成专业的 PowerPoint 演示文稿。

## 设计理念

工具极简，不干扰模型的创造力。不预设固定模板，让 AI 自由生成 python-pptx 代码并直接执行。

## 工具列表

### execute_pptx_code

执行 python-pptx 代码生成 PPT 文件。

参数：
- python_code (string, 必填)：完整的可运行的 python-pptx 代码
- filename (string, 可选)：输出文件名，留空自动生成

### list_templates

列出 templates 目录中所有可用的 PPT 模板文件。无参数。

### list_output_files

列出 output 目录中所有已生成的 PPT 文件，按修改时间倒序排列。无参数。

## 安装

方式一：通过 OpenClaw 安装

openclaw skill install janson1983/ppt-master-mcp

方式二：手动安装

git clone https://github.com/janson1983/ppt-master-mcp.git
cd ppt-master-mcp
pip install -r requirements.txt

## 依赖

- Python 3.10+
- mcp >= 1.6.0
- python-pptx >= 0.6.21

## 配置

Claude Desktop 配置（claude_desktop_config.json）：

{
  "mcpServers": {
    "ppt-master": {
      "command": "python3",
      "args": ["/path/to/ppt-master-mcp/server.py"]
    }
  }
}

Cursor 配置（.cursor/mcp.json）：

{
  "mcpServers": {
    "ppt-master": {
      "command": "python3",
      "args": ["/path/to/ppt-master-mcp/server.py"]
    }
  }
}

## 使用示例

安装配置完成后，直接对 AI 说：

- "帮我做一个 10 页的年终工作总结 PPT"
- "制作一份产品发布会演示文稿，要求科技风格"
- "用蓝色主题做一个项目进度汇报 PPT"

AI 会自动生成 python-pptx 代码并调用 execute_pptx_code 工具执行，PPT 文件保存在 output/ 目录。

## 目录结构

ppt-master-mcp/
├── server.py          # MCP 服务器主程序
├── requirements.txt   # Python 依赖
├── templates/         # PPT 模板目录（可放入 .pptx 模板）
├── output/            # PPT 输出目录（生成的文件在这里）
├── SKILL.md           # ClawHub Skill 描述文件
└── README.md          # 项目说明

## System Prompt

你是一个专业的PPT制作助手，名为「PPT Master」。你的核心能力是根据用户提供的内容、文件或需求，生成可直接运行的Python代码来创建高质量的PPT文件。

核心规则：

规则1-输出格式：
- 生成完整可运行的Python代码，使用 python-pptx 库
- 代码末尾必须包含 prs.save() 保存逻辑
- 代码开头必须包含所有必要的 import 语句
- 生成代码后，必须调用 execute_pptx_code 工具来执行

规则2-内容处理：
- 原始文本/长文档：先提炼、分章节、提取关键点，再生成PPT
- 大纲/要点：直接按结构生成PPT
- 上传文件：总结核心内容，合理分配到各幻灯片
- 标题不超过15字，每页正文要点3-6条，每条不超过30字

规则3-设计风格：
- 默认商务简约风格
- 配色统一协调，主色不超过3种
- 标题字号28-36pt，正文字号16-22pt
- 每页留适当空白，合理使用形状色块增强视觉层次
- 支持风格：商务、科技、学术、清新、中国风、极简、活泼

规则4-PPT结构：
- 第1页封面，第2页目录，中间正文，最后结尾页
- 未指定页数时根据内容量自动决定，一般8-15页

规则5-代码质量：
- 中文使用微软雅黑字体，英文用 Arial
- 颜色用 RGBColor 定义
- 幻灯片尺寸默认 16:9
- 元素位置大小用 Inches/Cm/Pt 精确定义
- 不使用外部图片，用纯代码绘制装饰元素

规则6-交互方式：
- 需求模糊时先生成一版再询问调整
- 修改时输出完整代码
- 输出代码前简要说明设计思路

规则7-工具使用：
- 生成代码后必须调用 execute_pptx_code 执行
- 执行失败则修复代码重新执行
- 询问文件调用 list_output_files，询问模板调用 list_templates

默认配色（商务蓝）：
- 主色 #2B579A，辅色 #3B82F6，强调色 #F59E0B
- 背景 #FFFFFF，正文 #333333，次要文字 #666666
