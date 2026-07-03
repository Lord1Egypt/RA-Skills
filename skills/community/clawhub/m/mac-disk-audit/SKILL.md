---
name: mac-disk-audit
slug: mac-disk-audit
displayName: Mac磁盘清理顾问
description: >-
  Mac 磁盘空间盘点与清理建议技能。当用户说「硬盘不够用」「空间不足」「磁盘快满了」「帮我清理 Mac」「扫描大文件」「哪些可以删」时触发。
  自动扫描系统、用户目录、开发项目中的空间占用，生成三级清理建议（立即清 / 确认后清 / 保留），提供可直接复制执行的命令。
  绝不自动删除任何文件，只出报告和命令，执行前必须用户确认。
user-invocable: true
version: "1.0.0"
xiaping_trigger:
  - "硬盘不够用"
  - "磁盘快满了"
  - "帮我清理Mac"
  - "扫描大文件"
  - "哪些文件可以删"
  - "释放磁盘空间"
  - "git占用太大"
  - "node_modules太大"
  - "Mac存储空间不足"
  - "盘点存储"
xiaping_category:
  - "效率工具"
  - "系统维护"
xiaping_tags:
  - "Mac"
  - "磁盘清理"
  - "存储空间"
  - "git"
  - "开发者工具"
  - "系统优化"
metadata:
  {
    "openclaw": {
      "emoji": "🧹",
      "requires": {
        "bins": ["du", "find", "git"]
      }
    }
  }
---

# Mac 磁盘盘点清理技能

## 一、触发场景

用户说以下任意一类词时，立即启动本技能：

- 「硬盘不够用」「存储空间不足」「磁盘快满了」「Mac 卡了可能是空间不足」
- 「帮我清理 Mac」「扫描大文件」「哪些文件可以删」「释放磁盘空间」
- 「git 占用太大」「archive 太多」「venv 可以删吗」
- 「整理一下我的电脑」「盘点一下存储」

---

## 二、执行流程

### Step 1：快速盘点（全局视图）

先用两条命令摸清总体情况：

```bash
# 查看磁盘总容量和可用空间
df -h /

# 查看家目录各子目录大小（前15大）
du -sh ~/*/  2>/dev/null | sort -rh | head -15
```

同时扫描以下**高频占用大户**，直接给出数字：

```bash
# 废纸篓
du -sh ~/.Trash/ 2>/dev/null

# 系统缓存
du -sh ~/Library/Caches/ 2>/dev/null

# 应用支持（常含大体积数据）
du -sh ~/Library/Application\ Support/ 2>/dev/null

# iOS 设备备份（往往几十 GB）
du -sh ~/Library/Application\ Support/MobileSync/Backup/ 2>/dev/null

# 日志
du -sh ~/Library/Logs/ 2>/dev/null

# Downloads
du -sh ~/Downloads/ 2>/dev/null
```

---

### Step 2：精准扫描（找大文件）

```bash
# 查找家目录下超过 500MB 的文件（排除系统目录）
find ~ -type f -size +500M \
  ! -path "*/Library/Mail/*" \
  ! -path "*/.Trash/*" \
  -exec ls -lh {} + 2>/dev/null \
  | sort -k5 -rh | head -30
```

```bash
# 查找家目录下超过 100MB 的文件（更细粒度）
find ~ -type f -size +100M \
  ! -path "*/Library/Mail/*" \
  ! -path "*/.Trash/*" \
  -exec ls -lh {} + 2>/dev/null \
  | sort -k5 -rh | head -30
```

---

### Step 3：开发者专项扫描

如果用户是开发者（有 `~/Developer`、`~/code`、`~/projects` 等目录，或有任何 git 仓库），追加以下扫描：

```bash
# 扫描 .git 目录大小（git 历史膨胀是重灾区）
find ~ -maxdepth 6 -type d -name ".git" \
  ! -path "*/node_modules/*" \
  -exec du -sh {} + 2>/dev/null \
  | sort -rh | head -20

# 扫描 node_modules（前端项目常见垃圾）
find ~ -maxdepth 6 -type d -name "node_modules" \
  -exec du -sh {} + 2>/dev/null \
  | sort -rh | head -20

# 扫描 Python venv（量化/AI项目常见）
find ~ -maxdepth 6 -type d -name "venv" -o -type d -name ".venv" \
  -exec du -sh {} + 2>/dev/null \
  | sort -rh | head -20

# 扫描 Docker（如果有）
du -sh ~/Library/Containers/com.docker.docker/ 2>/dev/null

# 扫描 Xcode 缓存（iOS 开发者）
du -sh ~/Library/Developer/Xcode/DerivedData/ 2>/dev/null
du -sh ~/Library/Developer/CoreSimulator/ 2>/dev/null
```

---

### Step 4：应用重复检测

检查是否有同一 App 存在多个副本（如桌面 + Applications 各一份）：

```bash
# 查找桌面上的 .app 文件
ls ~/Desktop/*.app 2>/dev/null

# 查找下载文件夹里的 .app 文件（安装完没删的安装包）
ls ~/Downloads/*.app ~/Downloads/*.dmg ~/Downloads/*.pkg 2>/dev/null | head -20
```

---

### Step 5：生成三级清理建议报告

根据扫描结果，输出结构化报告，格式如下：

```
━━━━━━━━━━━━━━━━━━━━━━━━━
📊 磁盘盘点报告 [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━

💽 磁盘总览
  总容量：XXX GB | 已用：XXX GB | 剩余：XXX GB（XX%）

🔴 立即可清（无需确认，风险极低）
  - 废纸篓：X GB → 建议：右键「清空废纸篓」
  - ~/Downloads/ 中超过 30 天的 .dmg/.pkg 文件：X GB
  - ~/Library/Caches/：X GB → 建议：命令见下方
  - Xcode DerivedData：X GB（如不在开发则可清）

🟡 确认后清（需逐一确认，清后不可还原）
  - 路径：X GB → 说明：xxx → 清理命令：xxx
  - Python venv（若项目暂停）：X GB
  - node_modules（可随时 npm install 重建）：X GB
  - iOS 设备备份（旧设备或已在 iCloud 备份）：X GB

🟢 建议保留（扫描到但不推荐删）
  - 路径：原因说明

⚙️ 开发者专项
  - .git 历史膨胀：建议执行 git gc --aggressive（可节省 XX GB）
  - 具体命令：xxx
```

---

## 三、执行辅助命令速查

### 清理系统缓存（安全，重启后自动重建）
```bash
# 清空用户 Caches（安全）
rm -rf ~/Library/Caches/*

# 清空系统日志
sudo rm -rf /Library/Logs/*
rm -rf ~/Library/Logs/*
```

### 废纸篓彻底清空（命令行版）
```bash
osascript -e 'tell application "Finder" to empty trash'
```

### 清理 npm / node_modules
```bash
# 找出所有 node_modules 并列出（确认后再删）
find ~/code ~/Developer ~/projects -type d -name "node_modules" 2>/dev/null

# 逐个删除（用 trash 命令更安全，需先安装：brew install trash）
trash ~/path/to/node_modules
```

### git 历史瘦身
```bash
# 压缩 pack 文件（安全，不删历史）
git gc --aggressive --prune=now

# 查看 git 历史中的大文件（排查误提交）
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | sed -n 's/^blob //p' \
  | sort -nrk2 \
  | awk '{ if ($2 > 10485760) print $0 }' \
  | head -20
```

### 清理 Python venv（项目代码不受影响）
```bash
# 删除 venv，保留代码（之后用 pip install -r requirements.txt 重建）
rm -rf ./venv
```

### Xcode 清理
```bash
# 清理 DerivedData（编译缓存，可自动重建）
rm -rf ~/Library/Developer/Xcode/DerivedData/

# 清理模拟器（谨慎，会删除所有模拟器数据）
xcrun simctl delete unavailable
```

### Docker 清理
```bash
# 清理悬空镜像和无用容器
docker system prune

# 更彻底（包含 volumes）
docker system prune -a --volumes
```

---

## 四、安全铁律（绝对不可违反）

1. **只出报告，不自动删**：扫描完成后，所有清理操作必须列出路径等待用户确认，绝不自动执行 `rm -rf`
2. **走垃圾桶不走永久删除**：推荐用 `trash` CLI 或 `osascript` 调 Finder 删除，而非 `rm`
3. **逐条列出再删**：如果用户同意清理，必须逐条列出文件路径，说明大小和风险，批量最多 10 条
4. **代码目录不碰工作文件**：只清理 `node_modules/`、`venv/`、`.git/objects/` 等可重建目录，绝不碰源代码
5. **误删恢复提示**：每次删除前告知用户恢复方式（废纸篓可还原 / git restore / requirements.txt 重建）

---

## 五、常见场景速查

| 用户说 | 优先扫描 | 快速清理方向 |
|--------|---------|-------------|
| Mac 系统只剩几 GB | 全局扫描 + 废纸篓 + Caches + Downloads | 废纸篓 → 缓存 → 安装包 |
| AI 工作台目录越来越大 | .git + archive + venv | git gc → 清 venv → 归档迁移 |
| 前端项目太大 | node_modules | npm ci 替代本地缓存 |
| iOS 开发空间不够 | Xcode DerivedData + 模拟器 | DerivedData 清空 |
| 做量化/AI 的磁盘告急 | Python venv + 数据集 + 模型文件 | venv 重建 + 数据迁移到外盘 |

---

## 📝 版本迭代记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v1.0 | 2026-06-21 | 创建技能，覆盖系统级+开发者场景，三级清理建议框架 | Kyle |

---

## 关于作者

**桂皮 AI 实战**——专注 AI 效率工具与超级个体方法论。

关注公众号「桂皮AI实战」，获取更多 AI 提效技巧 + 实战案例。
