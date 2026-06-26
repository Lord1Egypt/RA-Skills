---
name: mystool
description: 米游社工具插件。当用户消息包含以下任意关键词时触发：米游社登录、米游社绑定、米游社账号、米游社解绑、米游社任务、米游币任务、米游社签到、原神便笺、星铁便笺、开拓力、树脂、米游币商品、米游社兑换、米游社帮助、扫码补全stoken。支持短信登录、扫码登录、Cookie 登录三种方式。
metadata: {"openclaw":{"emoji":"🎮"}}
---

# mystool — 米游社工具

## 执行规则

收到触发关键词后，**必须**按以下步骤执行，不得直接用文字回复：

### Step 1：运行 plugin.py

```bash
python3 skills/mystool/plugin.py <用户消息>
```

或在 Python 中调用：

```python
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "skills" / "mystool"))
from plugin import handle

# sender_id: Telegram 用 chat_id，QQBot 用 openid，webchat 用 "webchat_user"
reply = asyncio.run(handle(
    message="<用户消息原文>",
    user_id="<sender_id>"
))
```

### Step 2：发送回复

- **handle() 返回字符串** → 将该字符串原样发送给用户（不要修改、不要翻译、不要加前缀）
- **handle() 返回 None** → 说明不是 mystool 指令，正常处理

### Step 3：渠道特殊处理

#### Telegram
```python
# sender_id = Telegram chat_id（从系统消息获取）
reply = asyncio.run(handle(message, user_id=str(chat_id)))
# 直接回复即可，OpenClaw 自动路由到 Telegram
```

#### QQBot
```python
# sender_id = QQ openid（从系统消息获取）
reply = asyncio.run(handle(message, user_id=openid))
# 直接回复即可，OpenClaw 自动路由到 QQBot
```

---

## 指令列表

| 指令 | 说明 |
|------|------|
| `米游社登录` | 选择登录方式（短信/扫码/Cookie） |
| `1` / `短信登录` | 短信验证码登录 |
| `2` / `扫码登录` | 扫码登录 |
| `3` / `Cookie登录` | 手动粘贴 Cookie |
| `扫码补全stoken` | Cookie 登录后补全 stoken |
| `米游社账号` | 查看已绑定账号 |
| `米游社解绑 [uid]` | 解绑账号 |
| `米游社任务` | 执行每日米游币任务 |
| `米游社签到 [游戏]` | 游戏签到（原神/星铁/崩3，仅国服） |
| `原神便笺` | 查看原神树脂等状态 |
| `星铁便笺` | 查看星穹铁道便笺 |
| `米游币商品 [游戏]` | 查看可兑换商品 |
| `米游社兑换 <ID> [数量]` | 兑换商品 |
| `预约兑换 <商品ID>` | 预约定时抢购 |
| `预约列表` | 查看预约列表 |
| `取消预约 <商品ID>` | 取消预约 |
| `预约兑换 <商品ID>` | 预约定时抢购 |
| `预约列表` | 查看预约列表 |
| `取消预约 <商品ID>` | 取消预约 |
| `生成识别码` | 获取跨平台绑定识别码 |
| `链接账号 <识别码>` | 使用识别码链接账号 |
| `设置代理 <URL>` | 设置 IP 池代理地址 |
| `查看代理` | 查看代理配置 |
| `米游社帮助` | 显示帮助 |

---

## 登录方式说明

### 1. 短信登录
- 输入手机号 → 接收验证码 → 自动获取完整 Cookie
- 参考实现：https://github.com/NuoManDai/mihoyo_sms_login

### 2. 扫码登录
- 生成二维码 → 用米游社App 扫码 → 自动获取完整 Cookie
- 提示文字："用米游社App 扫码，自动获取完整 Cookie"

### 3. Cookie 登录
- 直接粘贴 Cookie 字符串
- 如果缺少 stoken，系统会提示扫码补全

---

## 定时任务

每天 **07:20 (Asia/Shanghai)** 自动执行：

| 任务 | 命令 |
|------|------|
| 每日米游币任务 | `python3 skills/mystool/runner.py tasks` |
| 游戏签到 | `python3 skills/mystool/runner.py sign` |

结果通过 OpenClaw cron 系统推送到配置的通知渠道。
执行日志保存到 `log/` 文件夹，文件名格式：`YYYY-MM-DD_HH-MM-SS.log`

---

## 文件结构

```
skills/mystool/
├── plugin.py          # 主入口 handle(message, user_id)
├── runner.py          # cron 入口，带日志记录
├── channel.py         # 渠道工具
├── SKILL.md           # 本文件
├── README.md          # 使用说明
├── log/               # 执行日志目录
└── src/
    ├── api.py         # 米游社 API（仅国服签到）
    ├── login.py       # 旧版扫码登录（保留兼容）
    ├── qr_login.py    # 新版扫码登录模块
    ├── sms_login.py   # 短信登录模块
    ├── stoken_qr_login.py  # stoken 补全扫码模块
    ├── store.py       # 数据存储
    └── formatter.py   # 消息格式化
```

## 依赖

```bash
pip3 install httpx
# 可选（终端二维码）：
pip3 install qrcode
# 短信登录需要：
pip3 install pycryptodome
```
