---
name: skill-manager
description: 管理来自 GitHub 仓库的技能。用户要安装技能、检查技能更新、更新已安装技能、卸载技能，或提到注册技能、GitHub 技能、REGISTRY.yaml 时，优先使用此技能。
---

# Skill Manager

帮助管理来自 GitHub 仓库的技能安装、检查更新、更新和卸载。

技能安装到 `skills/{skill-name}/`，并通过 `skills/skill-manager/REGISTRY.yaml` 记录来源与 commit SHA。

## 前置条件

所有 GitHub 操作都依赖已认证的 `gh` CLI。

执行前运行：

```bash
gh auth status
```

如果失败，提示：`请先运行 gh auth login。` 并停止。

## 输入

从来源中提取这 4 个字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| `owner` | 仓库所有者 | `openai` |
| `repo` | 仓库名称 | `skills` |
| `branch` | 分支名，默认 `main` | `main` |
| `path` | 仓库内技能目录路径 | `skills/example-skill` |

技能名称取 `path` 的最后一段目录名。

## 沟通

检查更新时，用表格输出结果：

```text
| 技能名称      | 本地 commit SHA | 远程 commit SHA | 状态 |
|---------------|-----------------|-----------------|------|
| example-skill | abc1234         | def5678         | 需要更新 |
| web-search    | 9f8e7d6         | 9f8e7d6         | 已是最新 |
```

安装、更新或卸载完成后，明确告诉用户受影响的技能名称和结果。

## 安装

安装指定来源的技能，并写入 `REGISTRY.yaml`。

步骤：
1. 解析来源，提取 `owner`、`repo`、`branch`、`path`
2. 下载仓库归档并提取目标目录
3. 将技能保存到 `skills/{skill-name}/`
4. 在 `REGISTRY.yaml` 中追加条目，记录 `owner`、`repo`、`branch`、`path`、`commit` 和 `updated`

使用：

```bash
gh api "repos/{owner}/{repo}/tarball/{branch}" > archive.tar.gz
# 解压后将 {path} 复制到 skills/{skill-name}/
```

如果目标目录已存在，停止安装，不覆盖现有目录。

## 检查更新

扫描 `REGISTRY.yaml`，检查已注册技能的远程 commit SHA 是否发生变化。

使用：

```bash
gh api "repos/{owner}/{repo}/contents/{path}?ref={branch}" --jq '.sha'
```

默认检查全部已注册技能；如果用户指定技能名，只检查对应条目。

检查失败时，跳过该技能，并保持本地文件和注册表不变。

## 更新

更新已注册技能中有变化的条目。

步骤：
1. 先运行更新检查
2. 对每个需要更新的技能，重新下载并替换 `skills/{skill-name}/`
3. 更新对应注册表条目的 `commit` 和 `updated`

未指定技能名时，更新全部过期技能；指定技能名时，只更新对应条目。

如果技能未注册，先告诉用户该技能不在 `REGISTRY.yaml` 中，不执行更新。

更新前如果发现本地有未保存的修改，先提示冲突风险。

任何下载或更新失败时，不覆盖本地文件，不修改对应注册表条目。

## 卸载

删除技能目录，并从 `REGISTRY.yaml` 中移除对应条目。

步骤：
1. 确认技能名称
2. 删除 `skills/{skill-name}/`
3. 从 `REGISTRY.yaml` 中移除对应条目

如果技能目录不存在但注册表条目存在，只移除注册表条目。

## 注册表

位置：`skills/skill-manager/REGISTRY.yaml`

```yaml
skills:
  - owner: openai
    repo: skills
    branch: main
    path: skills/example-skill
    commit: abc123def456
    updated: 2026-01-01
```

规则：
- 安装时追加新条目
- 更新时只修改目标条目的 `commit` 和 `updated`
- 不重新排序，不删除无关条目

## 行为约束

- 仅管理来自 GitHub 仓库的技能
- 默认以 `branch=main` 处理未显式指定分支的来源
- 不覆盖现有技能目录，除非当前操作就是更新该技能
- 不覆盖失败的下载结果或半成品目录
