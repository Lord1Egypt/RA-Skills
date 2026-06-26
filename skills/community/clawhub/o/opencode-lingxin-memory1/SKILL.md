# OpenCode 灵芯派记忆守护者

## 名称
**opencode-lingxin-memory** | 灵芯派记忆守护者

---

## 一句话描述
为OpenCode AI助手提供记忆持久化，专为灵芯派低资源环境设计，支持Gitee云端同步。

---

## 详细介绍

### 问题
- 每次新对话，OpenCode忘记之前的工作和配置
- 灵芯派空间有限(仅2GB可用)，需要轻量化方案
- 没有自动备份，意外中断会导致进度丢失

### 解决方案
- 轻量化记忆系统，仅占用少量空间
- Git版本控制 + Gitee云端同步
- 新会话快速恢复上下文

---

## 使用方法

### 安装
```bash
# 1. 解压技能包
cd /home/zmrobo/Project
unzip opencode-memory-skill-v1.0.0.zip

# 2. 运行安装
cd opencode-memory-skill
./install.sh

# 3. 配置Gitee仓库（首次）
cd ~/.opencode-memory
git remote add origin https://gitee.com/你的用户名/仓库.git
git push -u origin master
```

### 新对话开始
```bash
# 恢复记忆
cat ~/.opencode-memory/MEMORY.md
cat ~/.opencode-memory/2026-04-30.md
```

### 对话结束
```bash
# 同步记忆
~/.opencode-memory/sync.sh
```

---

## 预置内容

| 文件 | 内容 |
|------|------|
| MEMORY.md | 灵芯派核心记忆、系统配置、已解决问题 |
| INDEX.md | 快速导航索引 |
| 2026-04-30.md | 今日工作日志模板 |

---

## 系统要求

- 灵芯派 (SmartPi) / ARM64设备
- Debian 10 或兼容系统
- 至少 100MB 可用空间
- Git
- Gitee 或 GitHub 账户

---

## 文件结构

```
~/.opencode-memory/
├── README.md              # 详细说明
├── MEMORY.md             # 长期核心记忆
├── INDEX.md              # 索引
├── YYYY-MM-DD.md        # 每日记忆
├── memory_index.json     # 索引数据
├── project_timeline.json # 项目时间线
├── sync.sh               # 同步脚本
└── .git/                 # 版本控制
```

---

**版本**: 1.0.0
**作者**: zmrobo
**许可**: MIT