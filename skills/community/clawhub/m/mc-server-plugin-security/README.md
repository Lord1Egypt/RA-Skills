# mc-server-plugin-security

**我的世界（Minecraft）服务器插件安全经验库——AuthMe 0day、登录绕过、session 劫持、ForceOp、插件消息伪造、权限漏洞、jar 静态检查、插件版本比对与升级选型，全部脱敏。**

**A Minecraft server plugin security vault — AuthMe 0-days, login bypasses, session takeover, ForceOp, plugin-message forgery, permission holes, jar static analysis, and version/upgrade selection. Fully desensitized.**

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么

从真实 MC 服务器（AuthMe 0day 漏洞排查与修复）实战中沉淀的插件安全经验库，适合 Bukkit / Spigot / Paper / Leaf / Folia / Arclight / NeoForge 各类服务端的插件漏洞排查、加固与升级选型。

- **§0 持续更新协议**：活文档强制协议 + 按问题快速索引 + 章节主题地图 + 脱敏核查与修改后自查清单（更新前必过）。
- **§1 插件漏洞专题**：AuthMe pre-join session takeover（2026 高危）、插件消息伪造绕过登录、Wurst ForceOP / 弱密码爆破、Galactifun 停更迁移、Slimefun 皮肤 429、ServerHangWatchdog 崩溃（Xmx 超物理内存）、Sinytra Connector 两个崩溃坑、主线程同步区块加载 → ASM 字节码修复等 11 个实战小节。
- **§2 排查方法论**：遇 0day 情报的完整排查流程、版本安全判定核心技巧（看编译时间/关键类/官方时间线，别只看文件名）、按服务端核心选 jar、依赖判断。
- **§3 常用命令**：`jar tf` 静态检查、GitHub API 版本核对、可疑条目扫描等直接可用的命令。
- **§4 铁律**：先核官方再信传言、版本新旧看时间线不看文件名、先问清架构再动手、升级前必备份、安全修复版优先于花哨 fork、配置文件即安全边界。

### 安装

```bash
git clone https://github.com/mowenQWQ/mc-server-plugin-security.git
cp mc-server-plugin-security/SKILL.md /path/to/your/agent/skills/mc-server-plugin-security/
```

适用于支持 Skill 格式的 AI 编码助手（Claude Code / CodeBuddy / OpenClaw 等），按 description 关键词自动触发；搭建或维护 MC 服务器前先查看，可避免重蹈覆辙。

---

## English

### What is this

A plugin-security vault distilled from real MC server incidents (including an AuthMe 0-day investigation and fix). Built for plugin vulnerability hunting, hardening, and upgrade selection across Bukkit / Spigot / Paper / Leaf / Folia / Arclight / NeoForge servers.

- **§0 Living-document protocol**: mandatory update rules + symptom-based quick index + topic map + desensitization & self-review checklists.
- **§1 Plugin incident vault**: AuthMe pre-join session takeover (2026 high severity), plugin-message forgery login bypass, Wurst ForceOp / weak-password cracking, Galactifun unmaintained-migration, Slimefun skin 429, ServerHangWatchdog crashes (Xmx over physical RAM), two Sinytra Connector crash traps, and a main-thread chunk-load → ASM bytecode fix, across 11 battle-tested sections.
- **§2 Investigation methodology**: full pipeline for 0-day claims, version-safety judgment (compile timestamps / key classes / official timelines — never trust filenames), jar selection by server core, and dependency checks.
- **§3 Commands**: ready-to-use `jar tf` static checks, GitHub API version comparisons, and suspicious-entry scans.
- **§4 Iron rules**: official sources before rumors; timeline over filename; know the architecture before acting; back up before upgrading; security-fixed releases over fancy forks; config is a security boundary.

### Install

```bash
git clone https://github.com/mowenQWQ/mc-server-plugin-security.git
cp mc-server-plugin-security/SKILL.md /path/to/your/agent/skills/mc-server-plugin-security/
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## 🤖 AI 使用声明 / AI Usage Disclosure

本项目在开发与维护过程中使用了 AI 编程助手（Claude / Anthropic）辅助代码编写、文档整理与问题排查；核心决策、内容审核与最终发布由维护者完成。

This project was developed and maintained with the assistance of an AI coding assistant (Claude / Anthropic) for coding, documentation, and troubleshooting. Core decisions, content review, and final releases are made by the maintainer.