# GitHub Skill Updater

`GitHub Skill Updater` 是一个面向 OpenClaw 的实用型 skill，用于检查并更新通过 GitHub `git clone` 安装的本地 skills。

它适合以下场景：

- 检查某个 skill 是否落后于远端仓库
- 批量检查当前 workspace 中的 git 型 skills
- 安全更新通过 GitHub 安装的 skill
- 在更新前识别未提交改动、分叉或本地领先等风险状态

## 功能概览

本 skill 提供以下能力：

- 检测基于 branch 跟踪的 skill 是否有新提交
- 检测基于精确 tag 的 skill 是否存在更新版本
- 对 branch 型 skill 执行 fast-forward 更新
- 对 tag 型 skill 切换到最新可用 tag
- 在存在风险时停止更新并给出明确原因

## 适用范围

本 skill 仅适用于满足以下条件的 skill 目录：

- 目录中保留了 `.git`
- 仓库存在 `origin` 远端
- 当前处于 branch，或位于一个精确 tag 上

以下情况不在自动更新支持范围内：

- 通过 zip 下载后手工解压的 skill
- 没有 `.git` 元数据的普通目录
- `detached HEAD` 且不位于精确 tag 的仓库

## 安装

### 通过 ClawHub 安装

如果该 skill 已发布到 ClawHub，推荐使用以下方式安装：

```bash
clawhub install github-skill-updater
```

更新已安装版本：

```bash
clawhub update github-skill-updater
```

### 通过 GitHub 手工安装

如果你直接从 GitHub 获取源码，可将本目录复制到 OpenClaw workspace 的 `skills/` 目录下：

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -R github-skill-updater ~/.openclaw/workspace/skills/
```

## 使用方法

以下命令默认在 OpenClaw workspace 根目录执行。

### 检查当前 workspace 中的 skills

```bash
sh skills/github-skill-updater/scripts/github-skill-updater check skills
```

### 更新单个 skill

```bash
sh skills/github-skill-updater/scripts/github-skill-updater update skills/<skill-name>
```

### 以 JSON 格式输出结果

```bash
sh skills/github-skill-updater/scripts/github-skill-updater check skills --json
```

### 直接调用 Python 主脚本

如果你希望直接使用主脚本，也可以执行：

```bash
python3 skills/github-skill-updater/scripts/manage_github_skill.py check skills
```

## 输出状态说明

脚本会返回以下状态之一：

- `up-to-date`：当前已是最新版本
- `update-available`：检测到可更新内容
- `dirty`：存在未提交改动，默认拒绝更新
- `ahead`：本地提交领先远端，默认拒绝更新
- `diverged`：本地与远端已分叉，默认拒绝更新
- `unsupported`：当前目录不满足自动检测或自动更新条件

## 更新策略

为保证安全性，本 skill 默认遵循以下策略：

- 更新前先执行检查
- 对 branch 型仓库仅允许 fast-forward 更新
- 对 tag 型仓库仅切换到更新的 tag，不执行强制重置
- 遇到 `dirty`、`ahead`、`diverged` 等状态时停止更新

## 仓库结构

```text
github-skill-updater/
  SKILL.md
  README.md
  LICENSE
  .gitignore
  agents/
    openai.yaml
  scripts/
    github-skill-updater
    manage_github_skill.py
  tests/
    test_manage_github_skill.py
```

## 发布到 ClawHub

在仓库根目录执行以下命令即可发布：

```bash
clawhub login
clawhub publish . \
  --slug github-skill-updater \
  --name "GitHub Skill Updater" \
  --version 1.0.0 \
  --tags latest
```

后续发布新版本时，只需更新版本号后重新执行发布命令。

## 本地测试

```bash
python3 -m unittest tests/test_manage_github_skill.py
```

## 许可证

本项目采用 [MIT License](./LICENSE)。
