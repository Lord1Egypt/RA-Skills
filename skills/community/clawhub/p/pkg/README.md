# apple-calpal

个人日程管家 skill：导入课表/排班等固定日程 + 对话规划行程 + 直写 iPhone 日历
（iCloud CalDAV）。为 OpenClaw 设计，纯 Python 标准库，零第三方依赖。

## 部署到 NAS（OpenClaw 网关所在机器）

1. 把整个 `apple-calpal/` 文件夹拷到 OpenClaw 的 skills 目录，常见位置二选一：
   - `~/.openclaw/skills/apple-calpal`
   - OpenClaw workspace 下的 `skills/apple-calpal`（以你网关配置里的 workspace 为准）
2. 确认 NAS 上有 `python3`（`python3 --version`，≥3.9 即可，无需 pip 装任何东西）。
3. 重启网关或让 OpenClaw 重载 skills，然后在对话里直接说人话测试：
   - 「我周六想去香山看日落」（触发规划）
   - 「帮我看看周四有什么安排」（触发查询）
   - 「这是我新学期的课表」+ 丢文件（触发导入）

## 文件结构

```
apple-calpal/
├── SKILL.md               agent 读的说明书（流程 + 红线）
├── scripts/
│   ├── cal.py             iCloud CalDAV：calendars / query / push / cancel
│   ├── env_tools.py       地理编码 / 日出日落 / 天气（Open-Meteo，免 key）
│   └── route.py           高德路径规划（可选，没 key 时 agent 自行估算）
└── data/                  个人数据，不要提交到公开仓库
    ├── profile.json       凭据、家坐标、日历名、可选高德 key
    └── commitments/       承诺库（课表等 spec JSON）
```

## 安全

`data/profile.json` 里需要填 Apple ID 的**App 专用密码**（不是登录密码，
在 appleid.apple.com 生成），权限仅限日历，随时可撤销。这个文件只应存在
于你自己的 NAS 和本机上，**不要把填了真实凭据的 profile.json 提交或分享**；
公开仓库请使用仓库里的空模板。

## 从旧管道迁移（可选）

如果你之前用旧课表管道（build_ics.py / push_icloud.py 之类）写过 `cumtb-` 前缀的
事件：本 skill 的 cancel 只碰 `calpal-` 前缀，旧事件不会被误删。若想把旧课表
换成新 UID 体系重推，先手动清空旧课表日历再推，避免重复。
