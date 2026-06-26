# Marketplace 索引更新 | Marketplace Index Publishing

> 本文档供 AI Agent 在**首次发布一个全新 skill** 时执行。版本更新（已存在于 marketplace 的 skill 升级 vX.Y.Z）**不需要**读取或执行本文档。

## 触发条件 | When to Run

| 场景 | 是否更新 marketplace 索引 |
|------|--------------------------|
| **从 0 发布一个新 skill**（marketplace 中尚无该 skill 条目） | ✅ 必须更新 |
| 已发布 skill 的版本升级（PATCH/MINOR/MAJOR） | ❌ 不需要 |
| 仅改文档 / 修 bug / 重构 | ❌ 不需要 |

判断方法：在 marketplace 索引的 `plugins` 数组中检索目标 skill 的 `name`。
- **不存在** → 新 skill 首发，执行本文档。
- **已存在** → 版本更新，跳过本文档，按 SKILL.md 的 Five-Way Sync 走即可。

## Step 1: 定位 Marketplace 仓库 | Locate the Marketplace Repo

**不要硬编码路径。** Marketplace 仓库可能在不同 workspace 或组织位置，运行时动态定位：

1. 在当前 workspace 内检索包含 `marketplace` 关键字的仓库/目录：
   ```bash
   # 查找 Claude Code marketplace 索引文件
   find . -path '*/.claude-plugin/marketplace.json' 2>/dev/null
   # 或按仓库名检索
   ls -d */ | grep -i marketplace
   ```
2. 若 workspace 内未找到，检索所属 GitHub 组织内是否存在 marketplace 仓库：
   ```bash
   gh repo list <org> --limit 100 | grep -i marketplace
   ```
   找到后 clone 到本地再操作。
3. 标志性文件：`.claude-plugin/marketplace.json`（核心索引）+ `README.md`（人类可读列表）。

> 若仓库/组织内**完全不存在** marketplace 仓库，向用户确认是否需要新建，不要擅自创建。

## Step 2: 追加 plugin 条目 | Add Plugin Entry

编辑 `.claude-plugin/marketplace.json`，在 `plugins` 数组末尾追加：

```json
{
  "name": "<skill-name>",
  "displayName": "<displayName>",
  "description": "<一句话功能描述>",
  "source": {
    "source": "github",
    "repo": "<org>/<skill-repo>"
  },
  "strict": false
}
```

| 字段 | 来源 / 要求 |
|------|------------|
| `name` | 与 skill 仓库的 `SKILL.md` 中 `name` 一致（kebab-case） |
| `displayName` | 与 `SKILL.md` 中 `displayName` 一致 |
| `description` | 简短功能描述，建议与 SKILL.md description 首句一致 |
| `source.repo` | `<org>/<repo>` 形式的 GitHub 仓库路径 |
| `strict` | 一般为 `false` |

注意 JSON 语法：追加条目时为前一条目补上逗号。

## Step 3: 同步更新 README 表格 | Sync README Table

在 marketplace 仓库 `README.md` 的 "包含的 Skill" 表格中追加一行，保持与 `marketplace.json` 一致：

```markdown
| [<skill-name>](https://github.com/<org>/<skill-repo>) | <功能描述> |
```

## Step 4: 提交并推送 | Commit & Push

```bash
cd <marketplace-repo>
git add .claude-plugin/marketplace.json README.md
git commit -m "feat: add <skill-name> to marketplace index"
git push origin master
```

推送后，用户即可通过以下命令安装新 skill：

```
/plugin install <skill-name>@<marketplace-name>
```

## 验证 | Verify

- [ ] `marketplace.json` 中存在该 skill 条目，且 JSON 合法（`name`/`displayName`/`source.repo` 正确）
- [ ] README 表格已同步对应行
- [ ] marketplace 仓库已 push
- [ ] `marketplace.json` 与 README 表格的 skill 列表一致
