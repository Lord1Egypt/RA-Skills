---
name: pdf-parser
description: 使用 MinerU API 将 PDF 解析为 Markdown，支持公式、表格、OCR。提供本地文件和在线 URL 两种解析方式。触发条件：(1) 用户说"解析 PDF [路径]"，(2) 用户说"将 PDF 转为 Markdown"，(3) 在 paper-workflow 中自动调用。使用场景：学术论文解析、文档提取、知识库构建。
homepage: https://mineru.net
metadata: {"clawdbot":{"emoji":"📄","requires":{"env":["MINERU_TOKEN"]},"primaryCredential":"MINERU_TOKEN"}}
---

# PDF Parser Skill

基于 [MinerU](https://github.com/opendatalab/MinerU) 提供 PDF 解析能力。

## 功能

- **PDF 解析**: 将 PDF 转换为 Markdown 格式
- **公式识别**: 支持 LaTeX 公式提取
- **表格识别**: 自动识别并转换表格结构
- **OCR**: 支持图片型 PDF 文字识别
- **多语言**: 支持中文、英文，日文、韩文等

## ⚠️ 安装前必读

**使用本技能即表示：**
1. 你愿意提供你的 MinerU API Token (`MINERU_TOKEN`)
2. Token 会被发送给 https://mineru.net/
3. 确认 MinerU 服务可信，接受其隐私政策
4. 已在本地源码中确认无额外意外行为

## 前提条件

### 1. 安装依赖

```bash
pip install requests
```

### 2. 获取 MinerU Token

访问 <https://mineru.net/> 注册并获取 API Token。

### 3. 设置环境变量

**Windows (PowerShell):**
```powershell
$env:MINERU_TOKEN = "your-token-here"
```

**macOS / Linux:**
```bash
export MINERU_TOKEN=your-token-here
```

## 支持的引擎

| 引擎 | 说明 |
|------|------|
| vlm | VLM 引擎（默认） |
| pipeline | 管道引擎 |
| MinerU-HTML | HTML 输出 |

## 快速开始

```bash
# 解析 PDF (默认 vlm 引擎)
python scripts/mineru_api.py -f <pdf路径> --wait

# 指定引擎
python scripts/mineru_api.py -f <pdf路径> --engine pipeline --wait
```

## 选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -f, --files | 本地 PDF 文件 | - |
| --engine | 解析引擎 | vlm |
| --lang | 语言 (ch/en/ja/ko) | ch |
| --wait | 等待解析完成 | 否 |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| MINERU_TOKEN | 是 | MinerU API Token |

## 输出

解析结果保存在 `~/.openclaw/MinerU_Results/` 目录下。

## 工作流

1. 设置 `MINERU_TOKEN` 环境变量
2. 执行解析命令
3. 等待解析完成
4. 读取 full.md 分析内容
5. 根据内容重命名目录
