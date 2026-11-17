---
name: jiedan-platform-suite
description: 接单平台 Skill 套件汇总入口（9 平台）。
---

# 接单平台套件

汇总入口（一键安装全部 9 平台）：`openclaw skills install jiedan-platform-suite`

注意：`skills install` 只接受纯 slug（ClawHub 技能名）；`@rascalagnt001/...`
作用域名与 `clawhub:` 前缀是 `plugins install` 的语义，传入 skills 命令会报
`Invalid skill slug`。也可用 ClawHub CLI：`clawhub install @rascalagnt001/jiedan-platform-suite`。

指定 skill 应用：jiedan-suite.json 机器可读声明全部接单 skill；每个平台包内嵌
影院列表（cinemas.json），安装即完成 接单渠道 ↔ 出票渠道 影院预绑定。
按需安装单个接单平台包；每个包只含数据声明（协议配置），运行时由 Cinema Agent
本地订单中心消费（原生适配器复用 / 通用声明式适配器），不执行任何市场包代码。

| 平台 | platformTag | 包内影院数 | 安装 |
| --- | --- | --- | --- |
| 麻花 | `mahua` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-mahua` |
| 秘密洋葱 | `secretonion` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-secretonion` |
| 哈哈 | `hahapiao` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-hahapiao` |
| 芒果 | `mango` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-mango` |
| 猎人 | `lieren` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-lieren` |
| 守兔 | `shoutu` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-shoutu` |
| 蚂蚁 | `mayiufu` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-mayiufu` |
| 鱼票 | `ticketsmalls` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-ticketsmalls` |
| 影划算 | `yhs` | 0 | `openclaw plugins install clawhub:@rascalagnt001/jiedan-platform-yhs` |

安装后自动完成：平台清单热装载 → 适配器路由 → 影院预绑定 → 接单/市场分析轮询生效。
