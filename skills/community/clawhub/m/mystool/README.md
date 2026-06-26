# mystool - 米游社工具 (OpenClaw Skill)

米游社自动化工具，支持短信登录、扫码登录、Cookie 登录三种方式。

## 功能

- 🔐 **账号管理**：短信/扫码/Cookie 三种登录方式，支持跨平台账号绑定
- 📅 **每日任务**：自动完成米游币任务（打卡、浏览、点赞、分享）
- 🗓️ **游戏签到**：原神、星穹铁道、崩坏3、崩坏学园2、未定事件簿、绝区零（国服）
- 📊 **实时便笺**：查看树脂、开拓力等游戏状态
- 🛒 **商品兑换**：米游币兑换游戏周边，支持预约抢购
- 🔗 **跨平台绑定**：Telegram / QQ 共享米游社账号数据
- 🌐 **代理配置**：支持移动端 IP 池代理，绕过短信频率限制

## 安装

```bash
# 基础依赖
pip3 install httpx

# 短信登录需要
pip3 install pycryptodome

# 可选（终端二维码显示）
pip3 install qrcode
```

## 使用

### 指令列表

| 指令 | 说明 |
|------|------|
| `米游社登录` | 选择登录方式（短信/扫码/Cookie） |
| `米游社账号` | 查看已绑定账号 |
| `米游社解绑 [uid]` | 解绑账号 |
| `米游社任务` | 执行每日米游币任务 |
| `米游社签到 [游戏]` | 游戏签到（原神/星铁/崩3等） |
| `原神便笺` | 查看原神状态 |
| `星铁便笺` | 查看星铁状态 |
| `米游币商品 [游戏]` | 查看可兑换商品 |
| `米游社兑换 <ID> [数量]` | 兑换商品 |
| `预约兑换 <商品ID>` | 预约定时抢购 |
| `预约列表` | 查看预约列表 |
| `取消预约 <商品ID>` | 取消预约 |
| `生成识别码` | 获取跨平台绑定识别码 |
| `链接账号 <识别码>` | 使用识别码链接账号 |
| `设置代理 <URL>` | 设置 IP 池代理地址 |
| `查看代理` | 查看代理配置和剩余次数 |
| `米游社帮助` | 显示完整帮助 |

### 跨平台账号绑定

Telegram 和 QQ 用户可共享米游社账号数据：

**Telegram → QQ**：
1. Telegram 用户发送 `生成识别码` → 获得 6 位识别码
2. QQ 用户发送 `链接账号 XXXXXX` → 共享数据

**QQ → Telegram**：
1. QQ 用户发送 `生成识别码` → 获得 6 位识别码
2. Telegram 用户发送 `链接账号 XXXXXX` → 共享数据

识别码有效期 10 分钟。

### 短信登录代理

短信登录需要移动端 IP 池代理来绕过频率限制：

1. 注册代理服务（如 https://www.xkdaili.com）
2. 获取 API 提取链接
3. 发送 `设置代理 <API_URL>` 配置

代理配置自动管理：
- 每小时最多提取 20 次
- 每次提取间隔 30 秒冷却
- 配置存储在 `data/proxy_config.json`

### 定时任务

每天 **07:20 (Asia/Shanghai)** 自动执行：

```bash
# 每日米游币任务
python3 skills/mystool/runner.py tasks

# 游戏签到
python3 skills/mystool/runner.py sign
```

执行日志保存到 `log/` 目录，文件名格式：`YYYY-MM-DD_HH-MM-SS.log`

### 商品兑换预约

当商品库存不足时，自动显示下次补货时间并支持预约：

1. 发送 `米游社兑换 <商品ID>` → 兑换商品
2. 库存不足时显示补货时间
3. 发送 `预约兑换 <商品ID>` → 预约定时抢购
4. 发送 `预约列表` → 查看全部预约

## 文件结构

```
mystool/
├── plugin.py          # 主入口 handle(message, user_id)
├── runner.py          # cron 入口，带日志记录
├── channel.py         # 渠道工具
├── SKILL.md           # OpenClaw Skill 配置
├── README.md          # 本文件
├── data/              # 用户数据目录
│   ├── accounts.json       # 账号数据
│   ├── link_codes.json     # 跨平台绑定识别码
│   ├── proxy_config.json   # 代理配置
│   ├── sms_sessions.json   # 短信登录会话
│   └── exchange_schedules.json  # 预约抢购列表
├── log/               # 执行日志目录
└── src/
    ├── api.py         # 米游社 API（仅国服）
    ├── login.py       # 旧版扫码登录（兼容）
    ├── qr_login.py    # 扫码登录模块
    ├── sms_login.py   # 短信登录模块（含代理支持）
    ├── stoken_qr_login.py  # stoken 补全扫码模块
    ├── store.py       # 数据存储（含跨平台绑定）
    └── formatter.py   # 消息格式化
```

## 参考

- 短信登录：https://github.com/NuoManDai/mihoyo_sms_login
- MihoyoBBSTools：https://github.com/Womsxd/MihoyoBBSTools
- nonebot-plugin-mystool：https://github.com/Ljzd-PRO/nonebot-plugin-mystool
- Mys_Goods_Tool：https://github.com/Ljzd-PRO/Mys_Goods_Tool

## License

MIT
