# Kinema's Skill Making Pipeline

KinemaClaw 生态中 Skill 的开发、版本管理和跨平台发布规范，覆盖 Codex、Claude Code、GitHub Release 与 ClawHub。

## 平台支持

| 平台 | 状态 | 入口 |
| --- | --- | --- |
| Codex | ✅ | `.codex-plugin/plugin.json` + `skills/kinema-skill-making-pipeline/SKILL.md` |
| Claude Code | ✅ | `.claude-plugin/plugin.json` + 根 `SKILL.md` |
| OpenClaw / ClawHub | ✅ | 根 `SKILL.md` |

完整规范见 [SKILL.md](SKILL.md)，环境配置见 [references/ONBOARDING.md](references/ONBOARDING.md)。

## Codex 安装

Codex 插件不需要 Node.js。添加 Kinema marketplace：

```powershell
codex plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace.git
```

安装插件：

```powershell
codex plugin add kinema-skill-making-pipeline@kinema-skills-marketplace
```

安装或升级后请新开一个 Codex 对话，使新的 skill 内容生效。

## Claude Code 安装

```text
/plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace
/plugin install kinema-skill-making-pipeline@kinema-skills-marketplace
```

## OpenClaw 安装

ClawHub CLI 需要 Node.js：

```bash
openclaw skills install kinema-skill-making-pipeline
```

## 核心原则

| 原则 | 说明 |
| --- | --- |
| Git First | 所有修改必须在 Git 仓库中管理 |
| Atomic Commits | 每个 commit 是独立且有意义的变更 |
| Versioned Releases | 发布前创建 Git tag |
| No In-Place Publishing | 不直接发布工作目录中的原位 skill |
| Onboarding Required | 每个 skill 都有安装与配置引导 |
| Cross-Platform Sync | 同步源码、GitHub Release、ClawHub、Claude Code 与 Codex |
| Marketplace on First Publish | 新 skill 在所有支持平台的 marketplace 首次登记，版本升级不重复登记 |

## 跨平台 Skill 结构

```text
<skill-name>/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── skills/<skill-name>/SKILL.md
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
└── references/
    └── ONBOARDING.md
```

根 `SKILL.md` 是方法论的单一事实来源；Codex wrapper 只提供发现元数据和平台差异，避免维护两份完整规范。

## 发布流程

1. 提交功能变更。
2. 同步根 `SKILL.md` 和 Claude/Codex 两份 manifest 的版本。
3. 校验、提交并创建 Git tag。
4. 推送并创建 GitHub Release。
5. 发布 ClawHub 包。
6. 更新已安装的 Claude Code 与 Codex 插件。
7. 输出所有已启用平台的版本校验报告。

完整步骤见 [references/release-process.md](references/release-process.md)。首次发布新 skill 时，另见 [references/marketplace-publishing.md](references/marketplace-publishing.md)。

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)
