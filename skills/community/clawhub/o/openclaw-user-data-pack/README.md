# openclaw-user-data-pack

An OpenClaw skill that exports user-owned data (workspace memory, persona, skills, and more) into a single zip with a manifest, and can apply that zip onto a new OpenClaw home or workspace. Optional layers such as managed skills, session transcripts, and config snapshots are opt-in on both export and import so secrets and large logs are not moved by accident.

**Behavior:** pack/apply are **overwrite-by-path** filesystem operations; they do **not** merge conflicting memory or skills. Use `--dry-run`, inspect `EXPORT_MANIFEST.txt` inside the zip, back up the destination before apply, and only enable session/config flags if you understand transcripts and secrets—see `SKILL.md` for the full operator checklist.

Usage and agent instructions live in `SKILL.md`. Chinese readme: [README_CN.md](README_CN.md).

## Copy and send to OpenClaw

**ClawHub (recommended, international)**

```text
Please run clawhub install openclaw-user-data-pack to install this skill, and help me export or apply my OpenClaw user data (zip with manifest, optional managed skills / sessions / config).
```

**npm**

```text
Please run npm i openclaw-user-data-pack to install this skill, and help me export or apply my OpenClaw user data (zip with manifest, optional managed skills / sessions / config).
```

## Bai Xia Da Zhan

A tongue-in-cheek roster of “lobster-adjacent” names in the wild (for fun; no affiliation with this project):

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

## License

MIT
