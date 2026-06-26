---
name: lark-invoice-bot
description: |
  飞书发票识别→费用报销机器人管理技能。用于启动、停止、监控基于飞书CLI+Python OCR的发票报销Agent。
  当用户需要管理发票识别机器人、调试OCR、修改配置、查看审批模板时使用。
  触发关键词：发票机器人、费用报销bot、lark invoice、invoice bot、发票OCR测试、报销配置
version: 1.0.0
agent_created: true
metadata:
  openclaw:
    requires:
      env:
        - BOT_DIR
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
        - APPROVAL_CODE
      bins:
        - python3
        - lark-cli
        - tmux
    envVars:
      - name: BOT_DIR
        required: true
        description: 发票报销机器人项目路径（包含 invoice_orchestrator.py 的目录）
      - name: FEISHU_APP_ID
        required: true
        description: 飞书应用 App ID（从 open.feishu.cn 获取）
      - name: FEISHU_APP_SECRET
        required: true
        description: 飞书应用 App Secret（从 open.feishu.cn 获取）
      - name: APPROVAL_CODE
        required: true
        description: 费用报销审批模板 Code（从飞书审批模板 URL 获取）
    emoji: "🧾"
    homepage: https://github.com/larksuite/cli
---

# 飞书发票报销机器人管理技能

## 概述

管理运行在本地的飞书发票识别→费用报销 Agent。该 Agent 通过飞书 WebSocket 接收用户发送的发票图片/PDF，使用 PaddleOCR+EasyOCR 双引擎本地识别，发送交互确认卡片让用户选择报销类型，确认后自动提交飞书审批实例。

## 使用场景

| 用户意图 | 执行操作 |
|---------|---------|
| 启动/停止/重启发票机器人 | `scripts/manage.py start/stop/restart` |
| 查看机器人运行状态 | `scripts/manage.py status` |
| 查看最近日志 | `scripts/manage.py logs --lines 50` |
| 测试单张发票 OCR | `scripts/test_ocr.py <image_or_pdf_path>` |
| 修改配置 | 编辑 `$BOT_DIR/.env` |
| 查看审批模板字段映射 | 读取 `references/approval_template.md` |
| 查询飞书 CLI 连接状态 | `lark-cli auth status` |

## 前置准备

### 1. 配置环境变量

```bash
export BOT_DIR=/path/to/invoice-approval-bot
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
export APPROVAL_CODE=6FD315B4-...
```

各凭证获取方式详见 `references/env_guide.md`。

### 2. 安装依赖

```bash
# Python 依赖
pip install paddlepaddle paddleocr easyocr lark-oapi pdf2image pyzbar Pillow python-dotenv

# 飞书 CLI
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g
lark-cli config init

# 系统依赖（macOS）
brew install poppler zbar
```

## 系统架构

```
飞书平台
  │ WebSocket (lark-oapi SDK)
  ▼
$BOT_DIR/invoice_orchestrator.py  ← 核心编排器
  ├── 事件监听: im.message.receive_v1, card.action.trigger
  ├── lark-cli → 图片下载 / 消息发送 / 附件上传 / 审批创建
  ├── invoice_ocr.py → PaddleOCR + EasyOCR 双引擎
  ├── invoice_qr_verify.py → pyzbar 二维码验真
  ├── pdf_preprocessor.py → PDF→图片转换 (pdf2image + poppler)
  └── invoice_handler.py → 审批表单构建 (多行明细 + 报销类型)
```

## 管理操作

### 启动机器人

后台运行（tmux）：
```bash
tmux new-session -d -s invoice-bot \
  'cd $BOT_DIR && python3 invoice_orchestrator.py'
```

或通过管理脚本：
```bash
cd $BOT_DIR
python3 <skill-dir>/scripts/manage.py start
```

### 停止机器人

```bash
python3 <skill-dir>/scripts/manage.py stop
```

### 状态检查

```bash
python3 <skill-dir>/scripts/manage.py status
```

检查项：进程存活性、飞书 CLI 连接、最近日志。

## OCR 测试

对单张图片或 PDF 测试 OCR 识别效果，不提交审批：

```bash
python3 <skill-dir>/scripts/test_ocr.py /path/to/invoice.jpg
```

输出：JSON 格式的识别结果，包括发票号码、日期、金额、销售方、购买方、二维码验真状态。

## 配置管理

主要配置文件：`$BOT_DIR/.env`

关键配置项：
- `FEISHU_APP_ID` / `FEISHU_APP_SECRET`：飞书应用凭证
- `APPROVAL_CODE`：审批模板 Code
- `OCR_WORKERS`：OCR 线程池大小（默认 1）
- `PORT`：Webhook 模式监听端口

## 故障排查

| 问题 | 检查步骤 |
|------|---------|
| 机器人不响应消息 | `manage.py status` 检查进程；查看日志确认 WebSocket 连接 |
| OCR 识别不准 | 用 `test_ocr.py` 测试；检查 PaddleOCR 是否安装；更新模糊匹配表 |
| 审批创建失败 | `lark-cli auth status` 检查认证；确认 APPROVAL_CODE 正确 |
| lark-cli 命令超时 | 检查网络连接；重新 `lark-cli config init` |
| 中文 OCR 结果乱码 | 确认 PaddleOCR/EasyOCR 语言包已安装 |
| QR 扫描报 zbar 库找不到 | macOS Apple Silicon 上设置环境变量 `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` |
| 卡片 select_static 无选项 | option value 使用简短字符串（避免特殊字符），移除多余 `value` 字段 |
| 附件上传失败 (json decode) | 审批附件上传必须用 `www.feishu.cn` 域名（非 open.feishu.cn），直接用 requests 库 |
| lark-cli 拒绝绝对路径 | `--output` 和 `--file` 只接受相对路径，用 `cwd` 参数切换到临时目录 |

## 依赖

- **运行时**: Python 3.11+, Node.js 16+
- **Python**: paddlepaddle, paddleocr, easyocr, lark-oapi, pdf2image, pyzbar, Pillow, python-dotenv
- **系统**: poppler (`brew install poppler`), zbar (`brew install zbar`)
- **飞书 CLI**: `npm install -g @larksuite/cli` + `npx skills add larksuite/cli -y -g`
