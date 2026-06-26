# ITSM 工单自动提交技能 v2.1.0

> **版本:** 2.1 (轻量级架构)
> **作者:** OpenClaw Community
> **许可:** MIT

## 技能说明

自动提交 ITSM 工单到企业 IT 服务管理系统。支持以下工单类型：
- 头程询价
- 尾程询价
- 批次查询
- 问题反馈

## 🎯 轻量级架构

**技术栈：**
- **系统自带 chromium-browser**（零依赖下载）
- **Python + Selenium**（通过 CDP 连接）

**优势：**
- ✅ **零依赖** - 不需要安装 Playwright（150MB）
- ✅ **中文正常** - 使用系统字体
- ✅ **快速启动** - 无需下载浏览器
- ✅ **稳定可靠** - 成熟的 CDP 方案

## 使用方法

### 在 OpenClaw 中说

- "提交 ITSM 工单"
- "帮我提交头程询价工单，SKU 是 ABC-123"
- "创建 ITSM 工单"

### 参数

可通过以下方式提供：
- **环境变量**: `ITSM_USERNAME`, `ITSM_PASSWORD`, `ITSM_SKU`, `ITSM_REMARK`, `ITSM_WAREHOUSE`
- **对话提供**: 直接在 OpenClaw 中说明
- **默认值**: 用户名 500525，密码 Xy@123456，SKU 11

## 首次使用

第一次运行时，脚本会自动：
1. ✅ 检查并安装 chromium-browser（如果需要）
2. ✅ 安装 Python 依赖（selenium、requests）
3. ✅ 启动浏览器并提交工单

## 技术架构

```
itsm-ticket/
├── start.sh              # ⭐ 主入口（启动浏览器+提交工单）
├── submit-itsm.py        # Python 提交脚本（Selenium + CDP）
├── close.sh              # 关闭浏览器脚本
├── SKILL.md              # 本文档
├── screenshots/          # 截图保存目录
└── package.json          # npm 配置（保留）
```

## 运行方式

### 方式 1：一键启动（推荐）

```bash
cd ~/.openclaw/skills/itsm-ticket
bash start.sh
```

### 方式 2：分步执行

```bash
# 1. 启动浏览器
bash start.sh

# 2. 只提交工单（浏览器已运行）
python3 submit-itsm.py

# 3. 关闭浏览器
bash close.sh
```

## 依赖说明

**系统依赖：**
- chromium-browser（自动安装）
- Python 3（WSL 自带）

**Python 依赖：**
- selenium
- requests

**首次运行自动安装：**
```bash
pip install selenium requests --break-system-packages
```

## 特性

- ✅ **完全自动化** - 一键启动并提交
- ✅ **零大文件下载** - 使用系统浏览器
- ✅ **中文正常显示** - 系统字体支持
- ✅ **操作日志** - 每步截图保存
- ✅ **浏览器保持运行** - 可多次提交工单

## 关闭浏览器

```bash
pkill -f 'chromium.*--remote-debugging-port=9222'
```

或运行：
```bash
bash close.sh
```

## 版本历史

- **2.1** - 轻量级架构（chromium-browser + CDP）
- **2.0** - 重构为独立技能包
- **1.0** - 初始版本

## 故障排除

### chromium-browser 未安装

脚本会自动安装，或手动运行：
```bash
sudo apt-get update
sudo apt-get install -y chromium-browser
```

### Python 依赖缺失

```bash
pip install selenium requests --break-system-packages
```

### 中文乱码

不会出现！使用系统 chromium-browser，自带中文支持。

### 浏览器无法启动

检查 WSLg：
```bash
export DISPLAY=:0
```
