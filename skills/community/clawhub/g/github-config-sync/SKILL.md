---
name: github-config-sync
description: 一键同步Hermes配置和数据到GitHub，支持多设备间无缝切换。每次修改后只需一句命令就能同步所有内容。
version: 1.1.0
author: Zhang Wenhao
license: MIT
metadata:
  hermes:
    tags: [同步, github, git, 备份, sync, backup]
    triggers: [同步, github, git, 备份, sync, backup, 上传, 下载]
    scenarios:
      - 用户想在Mac和Windows之间同步Hermes配置
      - 用户想备份重要数据
---

# GitHub配置同步 - 简单清晰版

把Mac上的配置同步到Windows，或把GitHub上的配置同步下来。

## 快速开始

### 第一次使用（在一台新电脑上）

```bash
# 1. 安装GitHub CLI
winget install GitHub.cli  # Windows
brew install gh            # Mac

# 2. 登录GitHub
gh auth login
# 选择 HTTPS，登录方式选 GitHub CLI

# 3. 克隆仓库
git clone https://github.com/zhangwenhao66/hermes-config.git ~/hermes-sync
```

---

## 两种同步模式

### 模式A：把Mac的配置上传到GitHub（只在Mac上操作）

```bash
# 1. 进入同步目录
cd ~/hermes-sync

# 2. 拉取最新（确保不冲突）
git pull

# 3. 复制要同步的文件
cp ~/.hermes/config.yaml .
cp -r ~/.hermes/memories .
cp -r ~/.hermes/skills .
cp ~/.hermes/.env .           # 可选，包含API密钥
cp ~/.hermes/auth.json .      # 可选，包含认证信息
cp -r ~/.hermes/sessions .    # 可选，对话历史

# 4. 提交并推送
git add .
git commit -m "更新配置"
git push
```

### 模式B：把GitHub的配置下载到当前电脑（只在Windows上操作）

```bash
# 1. 进入同步目录
cd ~/hermes-sync

# 2. 拉取最新
git pull

# 3. 复制到Hermes目录
cp config.yaml ~/.hermes/config.yaml
cp -r memories/* ~/.hermes/memories/
cp -r skills/* ~/.hermes/skills/
cp .env ~/.hermes/.env           # 可选
cp auth.json ~/.hermes/auth.json # 可选
cp -r sessions/* ~/.hermes/sessions/  # 可选

# 4. 重启Hermes
hermes restart
```

---

## 同步内容清单

| 内容 | 说明 | 是否敏感 |
|------|------|----------|
| config.yaml | 主配置文件 | 否 |
| memories/ | 个人记忆和偏好 | 否 |
| skills/ | 所有技能 | 否 |
| .env | API密钥（可选） | ⚠️ 是 |
| auth.json | 认证信息（可选） | ⚠️ 是 |
| sessions/ | 对话历史（可选） | 否 |
| reddit_research/ | 创业研究数据 | 否 |

---

## 完整流程图

```
┌─────────────────────────────────────────────────────────┐
│                    第一次设置                              │
├─────────────────────────────────────────────────────────┤
│  1. 创建GitHub仓库（私有）                                │
│     https://github.com/new                               │
│     仓库名: hermes-config                                │
│                                                          │
│  2. 安装GitHub CLI                                       │
│     Mac:     brew install gh                            │
│     Windows: winget install GitHub.cli                  │
│                                                          │
│  3. 登录                                                │
│     gh auth login                                        │
│                                                          │
│  4. 克隆仓库                                            │
│     git clone https://github.com/zhangwenhao66/         │
│     hermes-config.git ~/hermes-sync                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Mac → Windows 同步（上传）                   │
├─────────────────────────────────────────────────────────┤
│  在Mac上执行:                                            │
│                                                          │
│  cd ~/hermes-sync                                       │
│  git pull                                               │
│  cp ~/.hermes/config.yaml .                             │
│  cp -r ~/.hermes/memories .                             │
│  cp -r ~/.hermes/skills .                               │
│  git add .                                              │
│  git commit -m "更新配置"                                │
│  git push                                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Windows ← GitHub 同步（下载）                │
├─────────────────────────────────────────────────────────┤
│  在Windows上执行:                                        │
│                                                          │
│  cd ~/hermes-sync                                       │
│  git pull                                               │
│  cp config.yaml ~/.hermes/config.yaml                   │
│  cp -r memories/* ~/.hermes/memories/                   │
│  cp -r skills/* ~/.hermes/skills/                       │
│  hermes restart                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 常见问题

### Q: 为什么同步后技能没有更新？
A: 确保把整个skills目录复制过去，覆盖旧文件。

### Q: .env要同步吗？
A: 可以同步（私有仓库相对安全），但建议熟悉后用1Password等工具管理。

### Q: 冲突了怎么办？
A: 先 `git stash`，再 `git pull`，然后处理冲突。

### Q: 想同步其他文件怎么办？
A: 直接复制到 ~/hermes-sync/ 目录下，然后提交即可。

---

## 维护

### 查看状态
```bash
cd ~/hermes-sync
git status
```

### 查看历史
```bash
git log --oneline
```

### 回滚
```bash
# 回滚到上一个版本
git reset --hard HEAD^
git push --force
```