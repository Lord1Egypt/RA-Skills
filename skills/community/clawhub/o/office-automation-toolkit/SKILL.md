---
name: office-automation-toolkit
description: |
  办公自动化工具注册表：零配置可用的 CLI/Python 工具清单。
  当 sop-extractor 生成 Skill 需要工具时，从这里查找。
  触发词：「工具清单」「有哪些工具」「toolkit」「安装工具」。
---

# 办公自动化工具注册表

> 核心原则：零配置可用。需要账号授权的工具列为"扩展工具"，按需配置。

## 基础工具（零配置，安装即用）

### Office 文档

| 工具 | 安装 | 能力 | WPS |
|------|------|------|-----|
| openpyxl | `pip install openpyxl` | Excel 读写，公式/图表/样式 | ✅ |
| pandas | `pip install pandas` | 数据分析/透视表/筛选 | ✅ |
| python-docx | `pip install python-docx` | Word 读写，段落/表格/样式 | ✅ |
| python-pptx | `pip install python-pptx` | PPT 创建/编辑 | ✅ |
| markitdown | `pip install markitdown` | Office 全格式→Markdown | ✅ |
| pywpsrpc | `pip install pywpsrpc` | 直接调用本地 WPS（Linux） | ✅原生 |

### PDF

| 工具 | 安装 | 能力 |
|------|------|------|
| pymupdf | `pip install pymupdf` | 读取/提取文字图片表格 |
| pypdf | `pip install pypdf` | 合并/拆分/加密 |
| pdfplumber | `pip install pdfplumber` | 精确表格提取 |
| reportlab | `pip install reportlab` | 生成 PDF |

### 浏览器 & 网络

| 工具 | 安装 | 能力 |
|------|------|------|
| playwright | `pip install playwright && playwright install chromium` | 无头浏览器自动化 |
| requests | `pip install requests` | HTTP 请求 |
| beautifulsoup4 | `pip install beautifulsoup4` | HTML 解析 |
| httpx | `pip install httpx` | 异步 HTTP |

### 系统 CLI

| 工具 | 安装 | 能力 |
|------|------|------|
| jq | `apt/brew install jq` | JSON 处理 |
| pandoc | `apt/brew install pandoc` | 万能格式转换 |
| ffmpeg | `apt/brew install ffmpeg` | 音视频处理 |
| tesseract | `apt/brew install tesseract` | OCR 文字识别 |

### 飞书（已配置 ✅）

| 工具 | 能力 |
|------|------|
| lark-cli | 飞书官方 CLI，200+ 命令，覆盖消息/文档/表格/日历/邮件/任务/审批 |
| lark-oapi | Python SDK |

凭证由 Hermes 预配，lark-cli 通过 `config bind --source hermes` 自动绑定。

### 企业微信 & 钉钉

| 平台 | 工具 | 配置 |
|------|------|------|
| 企业微信 | Webhook 机器人 | 🟡 仅需 Webhook URL |
| 企业微信 | wecom-cli | 🟡 需 Corp ID |
| 钉钉 | dingtalk-cli | 🟡 需 App Key |

## 扩展工具（需 IT 配置 Token/Key）

| 域 | 工具 | 需要配置 |
|----|------|---------|
| 消息 | lark-oapi / wecom / dingtalk | App ID + Secret |
| 日历 | gcalcli / msal / lark-oapi | OAuth2 或 App 凭证 |
| 邮件 | himalaya / google-api | IMAP 账号或 OAuth2 |
| 数据库 | mysql/psql/redis-cli | 连接信息 |

## 工具选择速查

- **Excel** → openpyxl（读写）/ pandas（分析）/ csvkit（CLI）
- **Word** → python-docx（读写）/ markitdown（提取）/ pywpsrpc（控制WPS）
- **PPT** → python-pptx / powerpoint skill
- **PDF** → pymupdf（提取）/ pypdf（合并）/ reportlab（生成）
- **浏览器** → Playwright（零配置，首次有头扫码→保存 auth.json 后续无头）
- **发消息** → 飞书 lark-cli / 企微 Webhook / 钉钉
- **抓网页** → 动态页面 Playwright / 静态页面 requests+BS4

> 工具能力矩阵详见 `references/tool-quick-reference.md`
