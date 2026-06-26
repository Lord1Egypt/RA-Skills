---
name: macmini-knowledge-base
version: 1.3.0
description: |
  在 Mac Mini (M4) 上快速搭建本地知识库 + RAG 自然语言搜索系统。
  适用场景：
  - 新 Mac 配置知识库：从零开始安装配置 Ollama、embedding模型、定时任务、文档解析
  - 遇到 PDF 提取乱码、定时任务超时、skill 加载失败等问题
  - 想要建立每日自动分析文档 + 08:00发送摘要到飞书的流程
  - 迁移或复现知识库：打包整个 knowledge 目录和配置到新电脑
  本 skill 会引导完成：目录结构创建、依赖安装、脚本部署、定时任务注册、OpenClaw 配置。
---

# Knowledge Base Setup

在 Mac Mini 上快速搭建本地知识库 + RAG 搜索系统。

## 核心功能（v2.0）

- **kreuzberg 统一提取层**：PDF / DOCX / XLSX / PPTX / MD / 图片 OCR 全自动路由
- **antiword 极速专线**：.doc 文件专用提取，成功率 85%，169MB 文件 0.02 秒完成
- **智能兜底**：antiword 失败自动走 soffice 转换，60 秒硬超时无误判
- **自动分类**：关键词匹配驱动，中英文双语标签
- **定时任务**：每天 23:00 分析新文档，08:00 发送摘要到飞书

## 快速开始

### 一键安装

```bash
cd ~/.openclaw/workspace/skills/knowledge-base-setup/scripts
bash setup.sh <飞书用户ID>
```

### 手动分步安装

**Step 1: 系统依赖**
```bash
brew install antiword tesseract pandoc
```

**Step 2: Python 依赖**
```bash
pip3 install kreuzberg pytesseract pymupdf docx openpyxl python-pptx
```

**Step 3: Ollama + embedding 模型**
```bash
# 安装 Ollama: https://ollama.com/download
ollama pull nomic-embed-text
```

**Step 4: 创建目录结构**
```bash
mkdir -p ~/.openclaw/workspace/knowledge/.analysis/summaries/archives
mkdir -p ~/.openclaw/workspace/knowledge/temp_docs
touch ~/.openclaw/workspace/knowledge/文章目录/文章目录.md
```

**Step 5: 部署脚本**
```bash
cp ~/.openclaw/workspace/skills/knowledge-base-setup/scripts/*.py \
   ~/.openclaw/workspace/knowledge/.analysis/
chmod +x ~/.openclaw/workspace/knowledge/.analysis/*.py
```

**Step 6: 配置 OpenClaw**

编辑 `~/.openclaw/openclaw.json`，加入：
```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434",
        "api": "ollama",
        "models": [
          {"id": "nomic-embed-text", "name": "Nomic Embed Text"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text"
      }
    }
  }
}
```

确保 tools 区块有：
```json
"tools": {
    "alsoAllow": ["exec", "process"]
}
```

然后重启：`openclaw gateway restart`

**Step 7: 注册定时任务**
```bash
# 23:00 分析新文档
openclaw cron add \
  --name "23:00分析新文档" \
  --cron "0 23 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --timeout-seconds 600 \
  --message "cd ~/.openclaw/workspace/knowledge/.analysis && python3 run_analysis.py && python3 generate_catalog.py" \
  --announce --channel feishu --to "user:<飞书用户ID>"

# 08:00 发送文档摘要
openclaw cron add \
  --name "08:00发送文档摘要" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --timeout-seconds 120 \
  --message "读取 summaries/ 目录发送摘要到飞书" \
  --announce --channel feishu --to "user:<飞书用户ID>"
```

## 文档解析架构（v2.0）

### 架构图

```
                    ┌──────────────────────────────────────┐
                    │         kreuzberg 统一提取层           │
                    │  (pypdfium2 / python-calamine / pandoc) │
                    └───┬────────────────────────────────┬───┘
                        │                              │
                自动判断 │                              │
                        ▼                              ▼
              ┌─────────────────┐           ┌─────────────────────┐
              │  kreuzberg 直提  │           │  antiword 极速专线  │
              │ PDF/DOCX/XLSX/  │           │   (.doc 文件专用)    │
              │ PPTX/MD/图片OCR │           │   成功率 85%，<1秒   │
              └─────────────────┘           └─────────────────────┘
                        │                              │
                        │         ┌──────────────────────────────┐
                        │         │     soffice 兜底转换          │
                        │         │ (.doc/.xls/.ppt antiword失败) │
                        │         │  60秒硬超时（消除误判watchdog）│
                        │         └──────────────────────────────┘
                        ▼                              │
              ┌──────────────────────────────────────────────┐
              │              文本输出（content）              │
              │  → summaries/ 摘要文件 → generate_catalog.py  │
              └──────────────────────────────────────────────┘
```

### 文件类型 × 提取方式

| 格式 | 主方案 | 依赖 | 成功率 | 单文件速度 |
|------|--------|------|--------|-----------|
| PDF | kreuzberg (pypdfium2) | 无 | ~100% | 0.05-0.7s |
| DOCX | kreuzberg + pandoc | pandoc 3.9+ | 100% | 0.12-3s |
| XLSX | kreuzberg (python-calamine) | 无 | 100% | 0.1-0.5s |
| PPTX | kreuzberg + pandoc | pandoc 3.9+ | 100% | 0.02-0.2s |
| MD | kreuzberg + pandoc | pandoc 3.9+ | 100% | <0.01s |
| **.doc** | **antiword 优先** | antiword | **85%**，<1秒 | <0.02s |
| .doc（失败） | soffice 兜底 | LibreOffice | ~15% | 2-21s |
| .xls | soffice → XLSX | LibreOffice | ~95% | 2-10s |
| .ppt | soffice → PPTX | LibreOffice | ~95% | 2-10s |
| 图片 | kreuzberg 内置 OCR | tesseract | ~90% | 3-10s |

### antiword 极速专线

```python
# 实测数据：
# 169MB 超大文件 → 26万字符，0.02秒完成
# 正常 .doc（0.1-15MB）→ <1秒
# 成功率 85%，覆盖绝大多数 .doc 文件
result = subprocess.run(['antiword', filepath], capture_output=True, timeout=10)
```

### kreuzberg 统一提取层

kreuzberg 是专业的非结构化文档文本提取库（支持 20+ 格式），内部自动路由：
- PDF → pypdfium2
- XLSX → python-calamine
- DOCX/PPTX/MD → pandoc
- 图片 → 内置 OCR（tesseract）

## 关键词库（中英双语）

**中文（47个）：** 房产、房价、房地产、居民、消费、股市、经济、政策、利率、通胀、人民币、A股、美联储、PBOC、GDP、股票、资产、投资、债券、银行、PPI、CPI、PMI、M2、就业、失业、汽车、新能源、AI 等

**英文（70+个）：** property、real estate、GDP、inflation、CPI、PPI、PMI、PBOC、Fed、consumer、economy、growth、housing、stock market、EV、AI 等

**标签输出语言：** 自动判断——英文内容匹配英文关键词输出英文标签，中文内容匹配中文关键词输出中文标签

## 定时任务兼容性

| 任务 | ID | 调用方式 | 结论 |
|------|------|---------|------|
| 23:00分析新文档 | f3536e18 | 绝对路径 `python3 run_analysis.py` | ✅ 无需修改 |
| 07:00生成财经早报 | b741c6d5 | Node.js 脚本 | ❌ 不相关 |
| 08:00发送财经早报 | a7cbaacc | 读取文件发送 | ❌ 不相关 |
| 09:00发送文档摘要 | 89b4cf75 | 读取 summaries 目录 | ❌ 不相关 |

## 迁移到新电脑

1. 复制整个目录：
   ```bash
   scp -r ~/.openclaw/workspace/knowledge user@new-mac:~/.openclaw/workspace/
   ```
2. 在新电脑运行 `bash setup.sh <飞书用户ID>`
3. 重新注册定时任务（Job ID 会变）

## 避坑指南

| 问题 | 原因 | 解决 |
|------|------|------|
| LibreOffice 超时 | watchdog 误判大文件为卡死 | v2.0 移除 watchdog，60秒硬超时 |
| .doc 提取慢 | 统一走 LibreOffice | antiword 专线，169MB 文件 0.02秒 |
| DOCX/PPTX 处理失败 | pandoc 未安装 | `brew install pandoc` |
| PDF 提取乱码 | 自定义字体无 ToUnicode | kreuzberg(pypdfium2) + tesseract OCR |
| 飞书无 exec 工具 | tools 策略限制 | 添加 `alsoAllow: [exec, process]` |
| BGE-M3 卡顿 | 16GB 内存不足 | 继续用 nomic-embed-text |

## 关键路径

| 内容 | 路径 |
|------|------|
| Skill 目录 | `~/.openclaw/workspace/skills/knowledge-base-setup/` |
| 知识库 | `~/.openclaw/workspace/knowledge/` |
| 分析脚本 | `~/.openclaw/workspace/knowledge/.analysis/` |
| 目录缓存 | `~/.openclaw/workspace/knowledge/.analysis/.catalog_cache.json` |
| 摘要输出 | `~/.openclaw/workspace/knowledge/.analysis/summaries/` |
| 文章目录 | `~/.openclaw/workspace/knowledge/文章目录/文章目录.md` |
| OpenClaw 配置 | `~/.openclaw/openclaw.json` |

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-05-10 | 初始版本，PyMuPDF + LibreOffice 链路 |
| 1.1.0 | 2026-05-13 | 三步 PDF 处理，关键词库，双语标签 |
| 1.2.0 | 2026-05-21 | 分批处理优化，280秒断点 |
| 1.2.1 | 2026-05-22 | utils.py 共享模块重构，LibreOffice 熔断机制 |
| **1.3.0** | **2026-05-28** | **kreuzberg 统一提取层 + antiword 专线 + pandoc** |
