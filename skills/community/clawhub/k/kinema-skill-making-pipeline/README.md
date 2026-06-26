# Kinema's Skill Making Pipeline | Kinema Skill 开发与发布规范

KinemaClaw 生态中 Skill 的开发、版本管理和发布的标准化流程。所有在 KinemaClaw 下开发的 Skill 必须遵循此规范。

## 安装

### 方法一：通过 Claude Code Marketplace

1. 添加 Marketplace：

```
/plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace
```

2. 安装 Skill：

```
/plugin install kinema-skill-making-pipeline@kinema-skills-marketplace
```

3. 查看已安装的 Skill：

```
/plugin list
```

### 方法二：通过 ClawHub OpenClaw

```bash
openclaw skills install kinema-skill-making-pipeline
```

## 核心原则

| 原则 | 说明 |
|------|------|
| Git First | 所有修改必须在 Git 仓库中管理 |
| Atomic Commits | 每次 commit 必须是有意义的独立变更 |
| Versioned Releases | 发布前必须打 Git tag |
| No In-Place Publishing | 禁止直接从 /app/skills/ 发布 |
| Onboarding Required | 每个 Skill 必须有安装/配置引导 |
| Five-Way Sync | 发版后同步五地版本 |
| Marketplace on First Publish | 全新 Skill 首发时登记 marketplace 索引；版本更新不需要 |

## 适用场景

- 创建新 Skill
- 发布 / 更新已有 Skill
- 规范化团队 Skill 开发流程

## 发布流程

```bash
# 1. commit 并打 tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# 2. 创建 GitHub Release（Release Notes 含「更新内容」+「更新指令」两个 section）
#    更新内容每行 = 一条新功能/bug 修复 + @commit-id
gh release create v1.2.0

# 3. 发布到 ClawHub
clawhub publish . --slug <name> --name "<displayName>" --version 1.2.0 --changelog "changes"

# 4. 同步本地 skills
clawhub update <skill-name>

# 5. 更新 Claude Code 插件（Agent 直接执行，随后提醒用户重开 CLI 或 /reload-plugins）
claude plugin update <skill-name>@<marketplace-name>

# 6. （仅全新 skill 首发）更新 marketplace 索引
#    详见 references/marketplace-publishing.md
```

> **版本更新不需要动 marketplace 索引**，仅在从 0 发布新 skill 时登记。
> 完整发版步骤（含 Release Notes 结构、Agent 自动更新与重载提示）见 [references/release-process.md](references/release-process.md)。

## Skill 目录结构

```
<skill-name>/
├── SKILL.md              # 必需: Skill 定义
├── README.md             # 推荐: 仓库说明
├── LICENSE               # 推荐: 开源协议
├── scripts/              # 可选: 自动化脚本
└── references/           # 必需: 参考资料与引导文档
    └── ONBOARDING.md     # 必需: 安装配置引导
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)
