---
name: github-skill-updater
description: 检查并更新通过 GitHub git clone 安装的 OpenClaw skills。适用于用户提到“更新skill”“更新 skill”“检查 skill 是否有新版本”“GitHub 安装的 skill 有没更新”“帮我检查本地 skills 是否落后”“更新 git clone 装的 skill”“拉取 skill 最新代码”“批量检查 workspace/skills 里的仓库技能”这类需求。仅适用于保留 .git 元数据的 skill 目录。
---

# GitHub Skill Updater

用于检查和更新“通过 GitHub `git clone` 安装”的 OpenClaw skills。

## 触发条件

当用户表达下面这类意图时，应触发这个 skill：

- 更新 skill
- 更新某个 GitHub 安装的 skill
- 检查 skill 是否有新版本
- 拉取某个 skill 的最新代码
- 看看 workspace 里的 skills 哪些落后了
- 批量更新 git clone 安装的 skills

## 适用范围

- 适用：
  - skill 目录里保留 `.git`
  - skill 有 `origin` 远端
  - skill 在 branch 或精确 tag 上
- 不适用：
  - 下载 zip 后手工拷贝的 skill
  - 没有 `.git` 的普通目录
  - detached HEAD 且不在精确 tag 上的仓库

## 默认流程

1. 先做检查，不直接更新。
2. 发现 `dirty`、`ahead`、`diverged` 时默认停止，向用户说明原因。
3. 只有 `update-available` 才执行更新。

## 推荐命令

如果当前目录就是 OpenClaw workspace 根目录，推荐直接用包装命令：

```bash
./skills/github-skill-updater/scripts/github-skill-updater check skills
```

更新单个 skill：

```bash
./skills/github-skill-updater/scripts/github-skill-updater update skills/<skill-name>
```

也可以直接调用 Python 主脚本：

```bash
python3 skills/github-skill-updater/scripts/manage_github_skill.py check skills
```

批量输出 JSON：

```bash
./skills/github-skill-updater/scripts/github-skill-updater check skills --json
```

## 输出解释

- `up-to-date`: 已是最新
- `update-available`: 有可更新内容
- `dirty`: 有未提交改动，默认不更新
- `ahead`: 本地领先远端，默认不更新
- `diverged`: 本地与远端分叉，默认不更新
- `unsupported`: 目录不满足自动判断条件

## 实施要求

- 使用脚本 `scripts/manage_github_skill.py`
- 更新前必须先执行检查
- branch 模式仅允许 fast-forward 更新
- tag 模式只切换到更新的 tag，不做强制重置

## 失败兜底

如果脚本返回 `unsupported`：

- 检查该 skill 是否真的是 `git clone` 安装
- 确认目录里是否保留 `.git`
- 确认是否存在 `origin`
- 如无 git 元数据，只能手工重新安装或手工替换
