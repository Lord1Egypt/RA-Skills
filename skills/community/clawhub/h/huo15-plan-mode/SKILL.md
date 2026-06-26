---
name: huo15-plan-mode
description: 火一五计划模式 - 危险操作二次确认机制。检测到危险操作时自动暂停，等待用户确认后再执行。触发词：Plan Mode、危险操作确认、二次确认、火一五计划模式、火一五计划模式技能。
dependencies:
  optional: ["huo15-memory-evolution"]
---

# 🛡️ 火一五计划模式 (huo15-plan-mode)

> **作者**: 火一五信息科技有限公司  
> **版本**: v1.1.0  
> **依赖**: 可选依赖 huo15-memory-evolution

---

## 一、简介

Plan Mode 是一种危险操作确认机制。当 Agent 检测到危险操作时，会暂停执行并向用户确认，只有用户同意后才继续执行。

### 核心特性

| 特性 | 说明 |
|------|------|
| ⚠️ **危险操作检测** | 自动识别危险命令 |
| ⏸️ **操作暂停** | 危险操作前暂停 |
| ✅ **用户确认** | 发送确认消息给用户 |
| 🔄 **继续/取消** | 用户决定是否执行 |
| 📝 **操作日志** | 记录所有确认操作 |

---

## 二、危险操作分类

### 🔴 高危（必须确认）

| 操作 | 命令示例 |
|------|---------|
| 删除文件 | `rm`, `trash`, `unlink` |
| 删除目录 | `rmdir`, `rm -rf` |
| 覆盖文件 | `>`, `cp` 覆盖 |
| Git 强制推送 | `git push --force` |
| 终止进程 | `kill`, `pkill` |
| 系统配置 | 修改系统文件 |
| 卸载技能 | `clawhub uninstall` |

### 🟡 中危（可选确认）

| 操作 | 命令示例 |
|------|---------|
| 网络请求 | `curl`, `wget` |
| 执行脚本 | `./script.sh` |
| 安装依赖 | `npm install`, `pip install` |
| Git 提交 | `git commit`, `git push` |

### 🟢 低危（自动执行）

| 操作 | 命令示例 |
|------|---------|
| 读取文件 | `cat`, `read`, `grep` |
| 查看状态 | `ls`, `pwd`, `git status` |
| 查询操作 | `find`, `search` |

---

## 三、工作原理

```
检测危险操作
    ↓
发送确认消息给用户
    ↓
暂停等待用户回复
    ↓
用户确认？
    ↓ 是 → 执行操作
    ↓ 否 → 取消操作，记录日志
```

---

## 四、使用方式

### 4.1 自动检测

安装后自动启用，检测到危险操作时自动暂停。

### 4.2 手动触发

用户可以说"Plan Mode on"开启严格模式，"Plan Mode off"关闭。

### 4.3 查看日志

```bash
# 查看确认日志
cat ~/.openclaw/workspace/memory/activity/plan-mode-log.md
```

---

## 五、确认消息格式

当检测到危险操作时，发送以下格式的消息给用户：

```
⚠️ 危险操作检测

操作: rm -rf /tmp/test/*
文件数: 3 个
风险: 高

是否确认执行？

回复 "是" 执行
回复 "否" 取消
```

---

## 六、配置说明

### 6.1 危险操作列表

配置文件：`config/dangerous-operations.json`

```json
{
  "high": ["rm", "trash", "git push --force", "kill"],
  "medium": ["curl", "wget", "npm install"],
  "low": ["cat", "ls", "git status"]
}
```

### 6.2 确认模式

```json
{
  "mode": "strict",
  "autoConfirmLowRisk": true,
  "notifyOnCancel": true
}
```

| 配置 | 说明 |
|------|------|
| `mode` | strict=严格, normal=普通 |
| `autoConfirmLowRisk` | 低危操作自动执行 |
| `notifyOnCancel` | 取消时通知用户 |

---

## 七、集成 HEARTBEAT

Plan Mode 可以集成到 HEARTBEAT.md：

```markdown
## ⚠️ Plan Mode 检查

### 危险操作关键词
- rm -rf, trash, delete
- git push --force
- kill, pkill

### 确认流程
1. 检测到关键词
2. 发送确认消息
3. 等待用户回复
4. 根据用户回复执行/取消
```

---

## 八、脚本清单

| 脚本 | 功能 |
|------|------|
| `check-operation.sh` | 检测操作是否危险 |
| `confirm.sh` | 发送确认消息 |
| `execute.sh` | 执行已确认的操作 |
| `log-action.sh` | 记录操作日志 |
| `setup.sh` | 初始化配置 |
| `enable.sh` | 开启 Plan Mode |
| `disable.sh` | 关闭 Plan Mode |

---

## 九、安装

```bash
# 方式1: clawhub 安装
clawhub install huo15-plan-mode

# 方式2: 手动安装
cd ~/.openclaw/workspace/skills
git clone <repo> huo15-plan-mode

# 初始化
cd huo15-plan-mode
./scripts/setup.sh
```

---

## 十、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2026-04-05 | 初始版本 |
