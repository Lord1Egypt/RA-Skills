---
name: openclaw-security-handbook-cn
description: 基于 ZAST.AI 安全手册的 OpenClaw 安全审计与加固技能。运行全面安全诊断（内置 audit + 手册补充项），生成结构化报告，提供交互式修复引导，支持定时审计调度。触发场景：安全审计、安全加固、漏洞检查、security audit、hardening、暴露检查。
---

# OpenClaw Security — 安全审计与加固

## 概述

运行全面安全诊断，生成结构化报告，提供交互式修复引导。核心信号来自 `openclaw security audit --json`，补充手册（ZAST.AI 安全研究团队）中的手动检查项。

**核心原则：**
- 所有修复操作需用户确认，不自动执行
- 安全默认值修复（`--fix`）可安全推荐
- 密钥/凭证操作、Skill 卸载、配置文件删除等为不可逆操作，必须人工决策
- 优先使用 JSON 输出（`--json`）做机器解析

## 工作流

### 0. 开始前确认

用中文询问用户意图（列出选项，回复数字）：

```
请选择操作模式：
1. 完整审计（推荐）：诊断 + 报告 + 修复引导
2. 快速诊断：仅运行 openclaw security audit --deep
3. 交互式修复：基于上次报告逐项修复
4. 调度审计：配置定时安全检查
```

### 1. 运行诊断（并行执行）

按顺序执行以下检查，结果汇总后统一呈现：

#### A. OpenClaw 内置审计（JSON 格式）

```bash
openclaw security audit --json
```

解析 JSON，提取 `findings[]`（severity/checkId/title/detail/remediation）。

#### B. 补充手动检查项

以下检查项内置 `--fix` 不覆盖，需手动扫描：

**B-1. 文件权限**
```bash
# 检查关键文件和目录权限
ls -la ~/.openclaw/
stat -c "%a %n" ~/.openclaw/openclaw.json
stat -c "%a %n" ~/.openclaw/.env
stat -c "%a %n" ~/.openclaw/credentials/
```

**B-2. 日志/会话密钥泄露扫描**
```bash
grep -rEn "sk-|AKIA-|password|secret|token|private.key" ~/.openclaw/sessions/ 2>/dev/null | grep -v ".jsonl:" | head -20
grep -rEn "sk-|password|secret|token" ~/.openclaw/logs/ 2>/dev/null | head -20
```

**B-3. 附件文件权限**
```bash
find ~/.openclaw/ -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.pdf" -o -name "*.doc*" \) -perm +044 2>/dev/null
```

**B-4. 端口暴露检查（本地）**
```bash
# 检查网关 + 沙盒浏览器端口
ss -ltnp 2>/dev/null | grep -E "18789|18790|9222|5900|6080" || netstat -tlnp 2>/dev/null | grep -E "18789|18790|9222|5900|6080"
```

**B-5. 记忆文件完整性**
```bash
cat ~/.openclaw/workspace/MEMORY.md 2>/dev/null | head -50
ls -lt ~/.openclaw/workspace/memory/ 2>/dev/null | head -10
```

**B-6. Skill 危险模式扫描**
```bash
# 检查可疑文件模式（低权限扫描，不执行）
find ~/.openclaw/skills/ -name "*.js" -o -name "*.ts" -o -name "*.py" 2>/dev/null | head -50
```

**B-7. Docker 沙箱网络模式（如使用）**
```bash
docker inspect openclaw-sandbox 2>/dev/null | grep -A5 NetworkMode || echo "无沙箱容器"
```

### 2. 生成报告

将所有发现分为三组，格式化输出：

**🔴 CRITICAL（必须立即处理）**
**🟡 WARN（建议处理）**
**ℹ️ INFO（供参考）**

每项输出格式：
```
[checkId] 标题
  当前状态: <实际值>
  建议: <修复方法>
  修复命令: <具体命令或 "需人工确认">
```

### 3. 交互式修复引导

按严重程度逐项处理。每项询问（数字选择）：

```
修复项：[标题]
当前: <当前值>
建议: <修复方法>
修复命令: <具体命令>

选择：
1. 执行此修复
2. 跳过
3. 详细信息
```

**可安全自动化的项目（直接推荐 `1`）**：
- `chmod 600/700` 文件权限
- `openssl rand -hex 32` 生成强令牌
- `DISABLE_TELEMETRY=1` 环境变量
- 日志密钥泄露（确认后 grep 删除）

**必须人工确认的项目（默认 `2` 跳过）**：
- `groupPolicy` 修改
- `sandbox.mode` 变更
- Skill 卸载/安装
- OAuth token revoke
- 清除 workspace/sessions

### 4. openclaw security audit --fix

推荐执行内置安全默认值修复：

```bash
openclaw security audit --fix
```

说明：`--fix` 只修复文件权限和配置默认值，不执行破坏性操作。

### 5. 调度审计（可选）

完成后询问（数字选择）：

```
是否需要调度定期安全审计？
1. 每天 09:00 自动审计（openclaw cron）
2. 每周一 09:00 审计
3. 不调度
```

如选择调度：
```bash
openclaw cron add --name "openclaw-security:daily" --command "openclaw security audit --json" --cron "0 9 * * *" --output ~/.openclaw/logs/security-audit-$(date +\%Y\%m\%d).json
```

## 安全检查清单（完整版）

详细检查项见 `references/checklist.md`。

## 修复命令参考

各类问题的修复命令见 `references/fix-commands.md`。

## 脚本说明

- `scripts/security-report.py` — 解析 `--json` 输出并格式化，支持 `--fix` 模式自动应用安全默认值
- `references/checklist.md` — 完整安全检查清单（手册第九章）
- `references/fix-commands.md` — 各类修复命令速查表

## 关于本 Skill

基于 [ZAST.AI OpenClaw Security Handbook](https://github.com/zast-ai/openclaw-security) 构建，集成 OpenClaw 内置 `security audit` 命令，补充手册中的手动检查项。
