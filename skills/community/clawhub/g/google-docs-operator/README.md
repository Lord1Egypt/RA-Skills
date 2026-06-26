# 📄 Google Docs Operator (OpenClaw Skill)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)

Google Docs Operator 是一款专为 OpenClaw 打造的原生办公自动化技能。本项目通过集成 [Maton.ai](https://maton.ai) 网关，**免去了繁琐的本地 Google Cloud OAuth 配置**，让 AI 助理和终端用户仅需一个 API Key 即可全功能操控 Google Docs。

## ✨ 核心特性 (Features)

- 📝 **文档全生命周期管理**：支持一键创建新文档、读取提取纯文本、追加内容、以及清空并覆写全文。
- 🎨 **精细化排版与编辑**：支持全局批量搜索替换、设置段落标题样式（H1~H6），以及局部文本加粗格式化。
- 📥 **多格式极速导出**：无缝对接 Google Drive API，支持将文档一键导出为 `PDF`, `DOCX`, `TXT`, `HTML`, `EPUB` 等多种格式。
- 💻 **自带强大 CLI 工具**：内置 `gdocs_driver.py`，即便脱离 AI Agent 环境，也可作为独立的终端命令行工具使用。

## ⚙️ 前置准备 (Prerequisites)

本项目依赖 `requests` 库与 Maton 授权网关。

1. **安装依赖**：
 ```bash
pip install requests
```

2. **获取 API Key**：
   - 注册并登录 [maton.ai](https://maton.ai) 获取你的 `MATON_API_KEY`。

3. **配置环境变量**：
 ```bash
export MATON_API_KEY="your_api_key_here"
```

## 🚀 命令行快速上手 (CLI Usage)

项目中包含的 `gdocs_driver.py` 提供了一套完整的命令行接口。

### 1. 账号连接与授权

```bash
# 新建 Google 账号授权连接（会返回一个 URL 供浏览器验证）
python3 gdocs_driver.py connections create

# 查看已绑定的账号列表
python3 gdocs_driver.py connections list
```

### 2. 核心操作指令

```bash
# 创建新文档
python3 gdocs_driver.py create --title "My New Document"

# 读取文档纯文本 (支持 URL 或 Document ID)
python3 gdocs_driver.py get --id DOCUMENT_ID

# 追加内容到文档末尾
python3 gdocs_driver.py append --id DOCUMENT_ID --content "这里是追加的新内容"

# 搜索并替换文本
python3 gdocs_driver.py replace --id DOCUMENT_ID --find "旧词" --replace "新词"

# 格式化：设置标题与粗体
python3 gdocs_driver.py heading --id DOCUMENT_ID --text "第一章" --level 1
python3 gdocs_driver.py bold --id DOCUMENT_ID --text "关键数据"

# 导出为 PDF
python3 gdocs_driver.py export --id DOCUMENT_ID --format pdf --output ./report.pdf
```

## 🤖 OpenClaw 技能集成 (Agent Integration)

作为 OpenClaw 技能加载后，AI Agent 将拥有强大的文档处理能力。你可以通过自然语言下达指令：

- "帮我创建一个名为《本周工作总结》的谷歌文档。"
- "读取一下指定的 Google 文档，帮我提取出里面的核心行动项（Action Items）。"
- "把刚才总结的日报追加写入到我的 Google Docs 中，并把标题设为 H1，加粗重点词汇，最后导出成 PDF 发给我。"

## 🔐 隐私与安全说明

本插件所有的 Google API 请求均通过带有 SSL 证书加密的 `https://gateway.maton.ai` 代理。请妥善保管您的 `MATON_API_KEY`，切勿将其提交或硬编码至公开的 GitHub 仓库中。

---

**Developed by tankeito** | Open Source under MIT License
