---
name: pc-control
description: PC控制工具，远程操控Windows电脑。当需要操作主人电脑时使用，如截屏、键鼠控制、文件操作、进程管理、浏览器自动化、Shell命令执行等。触发词：控制电脑、操作PC、截图、键盘、鼠标、文件管理、浏览器。
---

# PC Control

Windows电脑控制工具，开箱即用，带完整安全防护。

## 快速安装

```bash
# 1. 安装 skill
clawhub install pc-control-luken

# 2. 安装依赖（Windows环境）
pip install -r skills/pc-control/scripts/requirements.txt

# 3. 配置 API Key（可选，推荐）
cd skills/pc-control/scripts
python generate_key.py   # 生成新的 API Key
# 或直接编辑 security_config.json 设置你自己的 key

# 4. 启动 API 服务
python api.py
```

## 安全认证

API 默认需要认证。调用时需要在 Header 中携带：
```
Authorization: Bearer <your_api_key>
```

未携带 key 或 key 错误将返回 `401/403`。

## 代码文件

| 文件 | 说明 |
|------|------|
| `scripts/pc.py` | CLI 命令行入口 |
| `scripts/api.py` | HTTP API 服务 |
| `scripts/generate_key.py` | API Key 生成器 |
| `scripts/security_config.json` | 安全配置文件 |
| `scripts/modules/` | 功能模块（含安全沙箱） |
| `scripts/requirements.txt` | Python 依赖 |

## 安全功能

- **API Key 认证** — 全局 token 验证
- **Shell 黑名单** — 拦截危险命令（del/shutdown/reg add等）
- **文件沙箱** — 禁止访问系统目录和危险文件类型
- **进程保护** — 系统关键进程无法被操作
- **操作日志** — 每次操作详细记录到 `security.log`

## 常用功能速查

| 功能 | 命令 |
|------|------|
| 截图 | `GET /screenshot` |
| 键盘按键 | `POST /key/press {"key":"enter"}` |
| 输入文本 | `POST /key/type {"text":"..."}` |
| 鼠标移动 | `POST /mouse/move {"x":100,"y":200}` |
| 鼠标点击 | `POST /mouse/click {"x":100,"y":200}` |
| 剪贴板读/写 | `GET /clipboard/read` / `POST /clipboard/write` |
| 进程列表 | `GET /process/list` |
| 结束进程 | `POST /process/kill {"name":"notepad"}` |
| 窗口列表 | `GET /window/list` |
| 关闭窗口 | `POST /window/close {"title":"..."}` |
| Shell执行 | `POST /shell/run {"command":"...","shell":"powershell"}` |
| 浏览器导航 | `POST /browser/navigate {"url":"..."}` |
| 浏览器点击 | `POST /browser/click {"text":"按钮文字"}` |

## 详细文档

- [完整API文档](references/api-doc.md)
