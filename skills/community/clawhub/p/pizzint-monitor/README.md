# PizzINT Monitor - Pentagon Pizza Index 披萨指数监测

实时监测 PizzINT (Pentagon Pizza Index) 指数，生成地缘政治威胁报告。

## 什么是 PizzINT？

PizzINT 是一个 OSINT（开源情报）工具，通过监测华盛顿特区五角大楼周边披萨店的外卖订单活跃度来推断美军活动水平。DOUGHCON 等级越高，说明军方相关活动越频繁。

## 功能特性

- **NEH 指数**：Nothing Ever Happens Index，实时末日时钟（0-100）
- **DOUGHCON 等级**：1-5 级披萨订单活跃度指标
- **披萨店异常监控**：Domino's / Extreme Pizza / Pizzato / Papa John's 等
- **PolyPulse 双边威胁**：USA/伊朗 🔴 CRITICAL、俄乌 🟠 HIGH 等
- **Polymarket 预测市场**：实时市场情绪
- **OSINT 动态摘要**：6 个情报账号的实时推文聚合

## 数据来源

- 🌐 https://pizzint.watch/

## ⚠️ 数据获取限制

pizzint.watch 为纯前端渲染（JavaScript 加载数据），需要浏览器工具访问。curl/requests 无法直接获取。

## 安装

```bash
cd ~/workspace/agent/skills/pizzint-monitor
python3 pizzint.py
```

## NEH 指数阈值

| 指数区间 | 状态 |
|----------|------|
| 0–30 | 🟢 Nothing Ever Happens（平静期） |
| 30–65 | 🟡 Something Might Happen（密切关注） |
| 65–99 | 🟠 Something is Happening（高风险） |
| 99–100 | 🔴 It Happened（重大事件） |

## DOUGHCON 等级

| 等级 | 信号 |
|------|------|
| 1 | NORMAL - Baseline Activity |
| 2 | ELEVATED - Increased Orders |
| 3 | HIGH - Multiple Spikes |
| 4 | ⚠️ DOUBLE TAKE - Intelligence Watch |
| 5 | 🚨 CRISIS - Military Operation Imminent |

## 风险提示

⚠️ 披萨指数是 OSINT 开源情报工具，相关性≠因果性，仅供参考，不构成任何投资或行动建议。

## License

MIT
