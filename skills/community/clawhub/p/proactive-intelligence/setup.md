# Proactive Intelligence v2.3.1 - 安装指南

## 快速安装（1分钟）

### 方式一：从 ClawHub 安装（推荐）

```bash
clawhub install proactive-intelligence
```

**安装后必须运行初始化脚本**：

```bash
# Windows
powershell -ExecutionPolicy Bypass -File skills/proactive-intelligence/init.ps1

# Python（跨平台）
python skills/proactive-intelligence/init.py
```

### 方式二：手动安装

1. 下载技能包并解压到 `skills/proactive-intelligence/`
2. 运行初始化脚本（同上）

---

## 初始化脚本做了什么

| 步骤 | 说明 |
|------|------|
| 1 | 创建 `~/proactive-intelligence/` 目录结构 |
| 2 | 创建核心文件（memory.md, corrections.md, session-state.md, patterns.md） |
| 3 | 创建 `.learnings/` 结构化日志目录 |
| 4 | **同步工作区 .md 路径**（旧路径 → 新路径） |

### 不运行初始化会怎样

- `~/proactive-intelligence/` 目录不存在 → 技能无法存储数据
- `.learnings/` 不存在 → 结构化日志无法使用
- 工作区 .md 文件路径未同步 → AI 读不到正确的记忆文件

---

## 目录结构

初始化完成后：

```
~/proactive-intelligence/
├── memory.md                 # HOT: 核心规则和偏好 (≤100行)
├── session-state.md          # 当前任务、决策、下一步
├── corrections.md            # 纠正记录和教训
├── patterns.md               # 可复用的主动策略
├── domains/                  # 领域知识 (WARM)
│   └── trading.md
├── projects/                 # 项目知识 (WARM)
└── archive/                  # COLD: 归档旧模式

~/.openclaw/workspace/.learnings/
├── LEARNINGS.md              # 纠正、洞察、知识缺口
├── ERRORS.md                 # 命令失败、异常
└── FEATURE_REQUESTS.md       # 用户请求功能
```

---

## 验证安装

```bash
# 检查目录是否存在
ls ~/proactive-intelligence/

# 检查 .learnings 是否创建
ls ~/.openclaw/workspace/.learnings/

# 预期输出应包含所有核心文件
```

---

## 日常使用

### 接收纠正时
自动记录到 `~/proactive-intelligence/corrections.md`

### 开始新任务时
更新 `~/proactive-intelligence/session-state.md`

### 完成任务后
自我反思，更新 `~/proactive-intelligence/patterns.md`

### 结构化日志
根据场景记录到 `.learnings/` 对应文件：
- 学习/纠正 → `LEARNINGS.md`（LRN-XXX 编号）
- 命令失败 → `ERRORS.md`（ERR-XXX 编号）
- 功能请求 → `FEATURE_REQUESTS.md`（FEAT-XXX 编号）

---

## 包含的工具

| 工具 | 用途 |
|------|------|
| `init.py` | Python 初始化脚本（跨平台） |
| `init.ps1` | PowerShell 初始化脚本（Windows） |
| `skill-evolver.py` | 技能分析和进化器 |
| `skill-manager.py` | 技能健康检查和管理 |

---

## 故障排除

### 问题：初始化脚本报错
**解决**：检查 PowerShell 执行策略
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题：路径未同步
**解决**：手动替换工作区 .md 文件中的 `~/self-improving/` → `~/proactive-intelligence/`

### 问题：.learnings 目录不存在
**解决**：手动创建
```bash
mkdir -p ~/.openclaw/workspace/.learnings
```
