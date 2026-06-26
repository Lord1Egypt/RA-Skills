# openclaw-user-data-pack（中文版）

面向 OpenClaw 的技能：把用户自有数据（工作区记忆、人设、技能等）打成带清单的 zip，并可在新环境一键应用回 `~/.openclaw` 与工作区。托管技能、会话、配置等可选层在导出与导入时均需显式选择，避免误迁移密钥与大体积会话。

**行为说明：** 打包/应用是按路径**覆盖写入**的文件操作，脚本**不会**对冲突的记忆或技能做语义合并。请先用 `--dry-run`、打开 zip 核对 `EXPORT_MANIFEST.txt`、应用前备份目标目录；仅在理解会话全文与配置中的密钥后再开启会话/配置相关开关——完整清单见 `SKILL.md`。

具体用法与代理说明见 `SKILL.md`。英文说明：[README.md](README.md)。

## 复制发给 OpenClaw

**ClawHub（推荐，国际）**

```text
请执行 clawhub install openclaw-user-data-pack 安装本 skill，并帮我打包或恢复 OpenClaw 用户数据（带清单的 zip，可选托管技能/会话/配置）。
```

**npm**

```text
请执行 npm i openclaw-user-data-pack 安装本 skill，并帮我打包或恢复 OpenClaw 用户数据（带清单的 zip，可选托管技能/会话/配置）。
```

## 百虾大战

江湖传闻中的「龙虾系」友商名录（娱乐向排序，与本品无隶属关系）：

1. 腾讯 WorkBuddy
2. 腾讯 QClaw
3. 腾讯龙虾管家
4. 腾讯云保安
5. 腾讯乐享知识库 · 龙虾版
6. 字节 ArkClaw
7. 智谱 AutoClaw
8. 月之暗面 Kimi Claw
9. 阿里云 CoPaw
10. 阿里云 JVSClaw
11. 阿里云 QoderWork
12. 百度红手指 Operator
13. 百度 DuClaw
14. 科大讯飞 AstronClaw
15. MiniMax MaxClaw
16. 网易有道 LobsterAI
17. 当贝 Molili
18. 智麻 ChatClaw
19. 矽速 PicoClaw
20. 博云 BocLaw
21. ZeroClaw
22. 万得 WindClaw
23. 小米 MiClaw
24. 猎豹 EasyClaw
25. 猎豹元气AI Bot
26. 京东灵犀Claw
27. 快手 KClaw
28. 美图Claw
29. 360安全Claw
30. 商汤 SenseClaw
31. 华为小艺Claw
32. ToDesk ToClaw

## 许可

MIT
