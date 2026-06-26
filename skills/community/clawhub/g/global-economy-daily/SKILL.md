# 全球经济每日洞察日报（Global Economy Daily Insight）

## 功能

每日自动生成并推送全球经济洞察日报，支持以下推送渠道：

- **QQ**（主要渠道）
- **飞书（Feishu）**

日报包含以下板块：

1. **全球股指** — 美股、欧股、亚太主要指数，含当日涨跌幅 + 归因分析
2. **大宗商品** — WTI原油、布伦特、黄金、白银，含归因分析
3. **外汇与债券** — 美元指数、美债10Y、离岸人民币、欧元/美元，含归因分析
4. **加密货币** — 比特币等，含归因分析
5. **时政要闻** — 近期重大地缘政治事件时间线 + 各方立场 + 影响研判
6. **综合展望** — 一句话市场研判

## 推送格式

```
🌏 全球经济每日洞察
📅 {日期}（{星期}）{时间}
📡 数据来源：Yahoo Finance（实时）

━━━━━━━━━━━━━━━━━━━━

📊 全球股指
🇺🇸 美股（隔夜）：
├ 标普500　 {price}　 {arrow} {change}%
📌 归因：{analysis}

🌏 亚太：
├ 日经225　 {price}　 {arrow} {change}%
📌 归因：{analysis}

...（各板块同理）

🌐 时政要闻 · {事件名称}
📌 事件时间线：
🗓️ {日期1}
  · {事件}
🗓️ {日期2}
  · {事件}
...
📌 各方立场：
🇺🇸 美国：{position}
🇮🇷 伊朗：{position}
...
📌 影响研判：
{analysis}

💡 综合展望：
{outlook}

━━━━━━━━━━━━━━━━━━━━
🤖 由 OpenClaw 自动生成 | 明日 07:00 准时推送
```

## 手动发送

```bash
python3 global_economy_daily.py
```

或直接对话中发送 "发送每日洞察" 即可手动触发。

## 定时任务配置

### macOS（LaunchAgents）

创建 `~/Library/LaunchAgents/com.qclaw.global-economy-daily.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.qclaw.global-economy-daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{SKILL_PATH}/scripts/global_economy_daily.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>7</integer>
        <key>Minute</key><integer>0</integer>
    </dict>
    <key>RunAtLoad</key><true/>
</dict>
</plist>
```

```bash
# 加载定时任务
launchctl load ~/Library/LaunchAgents/com.qclaw.global-economy-daily.plist
```

## 配置文件

修改 `scripts/config.py` 来自定义：
- 推送渠道（channel = "qqbot" 或 "feishu"）
- 推送时间
- 自定义归因分析逻辑
- 数据源偏好

## 依赖

- Python 3.x
- 无需额外 pip 包（使用标准库 urllib 请求 Yahoo Finance API）

## 文件结构

```
global-economy-daily/
├── SKILL.md
├── _meta.json
├── scripts/
│   ├── global_economy_daily.py   # 主脚本
│   └── config.py                  # 配置文件
└── templates/
    └── report_template.md         # 报告模板（参考）
```

## 注意事项

- 时政板块默认监控美伊霍尔木兹危机，可扩展为多个地缘事件并行追踪
- Yahoo Finance API 偶尔返回 None 历史数据，脚本有容错处理
- 飞书推送使用卡片消息格式，QQ使用纯文本富媒体格式
