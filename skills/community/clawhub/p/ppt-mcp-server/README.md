# PPT Master MCP Skill

一个 OpenClaw / ClawHub Skill，让 AI 自动生成专业 PowerPoint 演示文稿。

## 安装

在 OpenClaw 中安装：

    openclaw skill install janson1983/ppt-master-mcp

手动安装：

    git clone https://github.com/janson1983/ppt-master-mcp.git
    cd ppt-master-mcp
    pip install -r requirements.txt

## 功能

- execute_pptx_code：执行 python-pptx 代码生成 PPT
- list_templates：列出可用模板
- list_output_files：列出已生成文件

## 使用方式

安装后在 OpenClaw 中直接对话：

    "帮我做一个 10 页的年终工作总结 PPT"

AI 会自动调用工具生成 PPT 文件。
