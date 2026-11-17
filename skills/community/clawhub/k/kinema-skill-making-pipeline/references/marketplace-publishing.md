# Marketplace 索引更新 | Marketplace Index Publishing

> 仅在全新 skill 首次发布，或新增平台适配但对应 marketplace 尚无条目时执行。普通版本升级不得重复添加条目。

## 触发条件

分别检查 marketplace 仓库中的：

- Claude Code：`.claude-plugin/marketplace.json`
- Codex：`.agents/plugins/marketplace.json`

| 情况 | 动作 |
| --- | --- |
| 两边都不存在该 skill | 添加两种平台条目并同步 README |
| 仅一边缺失 | 只补缺失平台并更新 README 兼容表 |
| 两边都存在 | 跳过索引修改，执行常规版本发布 |

## Step 1: 定位 marketplace 仓库

不要硬编码工作区路径。优先在当前 workspace 搜索上述两个 manifest；未找到时再通过 `gh repo list <org>` 定位并 clone。若组织内完全不存在 marketplace 仓库，先向用户确认，不擅自创建。

## Step 2: 添加 Claude Code 条目

在 `.claude-plugin/marketplace.json` 的 `plugins` 末尾追加：

```json
{
  "name": "<skill-name>",
  "displayName": "<displayName>",
  "description": "<description>",
  "source": {
    "source": "github",
    "repo": "<org>/<skill-repo>"
  },
  "strict": false
}
```

`name` 必须与根 `SKILL.md` 和 `.claude-plugin/plugin.json` 一致。

## Step 3: 添加 Codex 条目

在 `.agents/plugins/marketplace.json` 的 `plugins` 末尾追加：

```json
{
  "name": "<skill-name>",
  "source": {
    "source": "url",
    "url": "https://github.com/<org>/<skill-repo>.git",
    "ref": "main"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Developer Tools"
}
```

规则：

- 每个条目必须包含 `policy.installation`、`policy.authentication` 和 `category`。
- 仓库根就是插件根时使用实测兼容的 `url` source；插件位于 monorepo 子目录时按当前 Codex 规范使用相应子目录 source。
- `ref: main` 允许普通版本升级不修改索引；如改用 tag 或 SHA 固定版本，后续发布必须明确更新 ref。
- 远程仓库必须已经包含有效 `.codex-plugin/plugin.json` 和其引用的所有文件，再发布 marketplace 条目。

## Step 4: 同步 README

更新 marketplace `README.md` 的兼容表，准确标注 Claude Code 与 Codex 支持状态。不要在 marketplace 仓库保存插件源码快照。

## Step 5: 校验、提交与推送

1. 解析两份 JSON，确认语法合法且无重复名称。
2. 使用隔离的 `CODEX_HOME` 添加 marketplace，并以 `codex plugin add <skill-name>@<marketplace-name>` 做安装冒烟测试。
3. 确认 Claude manifest 和 README 一致。
4. 只提交目标 manifest 与 README，然后推送 marketplace 仓库。

建议提交：

```bash
git add .claude-plugin/marketplace.json .agents/plugins/marketplace.json README.md
git commit -m "feat: add <skill-name> to marketplace index"
git push origin <default-branch>
```

## 用户安装命令

Claude Code：

```text
/plugin install <skill-name>@<marketplace-name>
```

Codex：

```bash
codex plugin marketplace upgrade <marketplace-name>
codex plugin add <skill-name>@<marketplace-name>
```

Codex 安装或升级后提醒用户新开对话。

## 验证清单

- [ ] 两种 manifest 中的 `name` 与插件仓库一致
- [ ] Codex 条目包含完整 source、policy 和 category
- [ ] 远程插件仓库已先于 marketplace 发布
- [ ] README 兼容表与两个 manifest 一致
- [ ] Codex Git source 安装冒烟测试通过
- [ ] marketplace commit 已推送
