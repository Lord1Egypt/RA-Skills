---
name: permission-guard
description: 分层权限守卫系统。基于 Claude Code Permission System 设计，包含危险命令拦截、规则优先级链、自动模式白名单和拒绝追踪。
---

# permission-guard

**分层权限守卫 — 基于 Claude Code Permission System。**

让 AI 在执行敏感操作前进行安全检查，防止意外破坏用户系统。

---

## 核心问题

AI 执行命令时，怎么保证不干坏事？

**错误做法：**
- 直接执行（危险）
- 所有都问（烦人）

**正确做法：**
分层权限 + 智能分类 + 自动拦截危险操作

---

## 权限模式

### 五种模式

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| **default** | 每个命令确认一次 | 初始学习阶段 |
| **auto** | 信任的自动，不信任的询问 | 日常开发 |
| **plan** | 每次都问（Plan Mode） | 审查阶段 |
| **bypass** | 完全不确认 | ⚠️ 危险，仅测试用 |
| **dontAsk** | 直接拒绝 | 受限环境 |

### 规则优先级（高覆盖低）

```
cliArg（命令行参数）
    ↓
session（当前会话）
    ↓
localSettings（本地配置）
    ↓
projectSettings（项目配置）
    ↓
userSettings（用户配置）
    ↓
policySettings（企业策略）
```

**企业策略 > 用户设置**，企业可以锁定权限配置。

---

## 危险命令拦截

### 立即拦截（自动拒绝）

```typescript
// 代码执行解释器
python, python3, node, deno, ruby, perl, php
npx, npm run, yarn run, pnpm run, bun run, bunx

// Shell
bash, sh, zsh, fish, ssh
eval, exec, xargs, sudo

// 管道执行
curl | bash, wget | sh
```

### 危险模式检测

```typescript
// 自动拒绝宽泛规则
Bash(python:*)    → 拦截，等于允许任意代码执行
Bash(node:*)      → 拦截
Bash(curl:*)     → 拦截，可能用于下载恶意脚本
```

### 自定义黑名单

可在配置中添加：

```json
{
  "dangerousCommands": [
    "rm -rf /",
    "dd if=* of=/dev/*",
    ":(){ :|:& };:"  // Fork bomb
  ]
}
```

---

## 自动模式白名单

**auto 模式下自动允许的安全命令：**

```typescript
// Git 读取操作
git status, git diff, git log, git show, git branch
git diff --staged, git diff HEAD, git remote -v

// 文件读取
ls, ll, cat, head, tail, grep, find, pwd

// 目录操作
cd, mkdir -p, tree, stat, file

// 开发工具
npm --version, node --version, git --version
python3 --version, docker ps, docker images

// 网络检查
ping, curl -I, wget --spider
```

---

## 规则格式

### 精确匹配

```json
{
  "tool": "Bash",
  "command": "git push origin main",
  "behavior": "allow"
}
```

### 前缀匹配（`:*` 语法）

```json
{
  "tool": "Bash",
  "command": "git:*",
  "behavior": "ask"
}
```

### 通配符匹配

```json
{
  "tool": "Bash",
  "command": "git commit *",
  "behavior": "allow"
}
```

### 路径限制

```json
{
  "tool": "Bash",
  "command": "rm *",
  "cwd": "/Users/julian/project",
  "behavior": "allow"
}
```

---

## 拒绝追踪

### 追踪逻辑

```typescript
// 追踪每个命令被拒绝的次数
denialTracking = {
  'rm -rf node_modules': { denyCount: 3, lastDeny: timestamp },
  'git push': { denyCount: 5, lastDeny: timestamp }
}

// 如果 denyCount > 阈值 → 给出建议
if (denyCount >= 3) {
  suggest("建议将此命令加入白名单或调整规则")
}
```

### Circuit Breaker

```typescript
// 连续失败 3 次 → 降级到询问模式，不阻塞
if (consecutiveFailures >= 3) {
  fallbackToAsk()
}
```

---

## 阴影规则检测

**问题：** 高优先级规则可能"遮住"低优先级规则。

```typescript
// 用户设置了: git push → allow
// 项目设置了: git * → deny
// 结果：git push 被 deny，但用户不知道为什么

// 检测并警告
shadowedRules = detectShadowedRules(userRules, projectRules)
if (shadowedRules.length > 0) {
  warn("以下规则被覆盖：\n" + shadowedRules.map(...).join("\n"))
}
```

---

## 敏感信息检测

### 自动拦截的敏感内容

```typescript
// 执行前扫描命令
scanForSecrets(command) → {
  detected: [
    { type: 'api_key', pattern: 'sk-[a-zA-Z0-9]{20,}', value: '***' },
    { type: 'password', pattern: '-p\\s+\\S+', value: '***' },
    { type: 'private_key', pattern: '-----BEGIN.*PRIVATE KEY-----', value: '***' }
  ]
}

// 如果检测到 → 拒绝执行并警告
```

---

## 权限检查流程

```
用户请求执行命令
         ↓
    解析命令和工具
         ↓
    检查危险命令黑名单
    ├── 是 → 自动拒绝 + 警告
    └── 否 → 继续
         ↓
    匹配规则（按优先级）
    ├── 有匹配规则 → 按规则执行
    └── 无匹配 → 进入自动模式
         ↓
    自动模式分类
    ├── 白名单 → 自动允许
    ├── 黑名单 → 自动拒绝
    └── 其他 → 询问用户
         ↓
    用户响应 → 记录到规则/拒绝追踪
```

---

## Hook 集成

### 执行前检查

```typescript
// Pre-execution hooks
preCheck = [
  dangerousPatternHook,   // 危险模式检测
  ruleMatchingHook,       // 规则匹配
  secretScanningHook,    // 敏感信息扫描
  sandboxHook           // 沙箱检查
]
```

### 执行后记录

```typescript
// Post-execution hooks
postCheck = [
  logPermissionResult,   // 记录到日志
  updateAutoModeRules,   // 更新自动模式规则
  denialTracking        // 更新拒绝计数
]
```

---

## 配置示例

### 用户配置（~/.openclaw/permissions.json）

```json
{
  "defaultMode": "auto",
  "dangerousCommands": [
    "rm -rf /",
    "rm -rf /home/*",
    ":(){ :|:& };:"
  ],
  "autoAllow": [
    "git status",
    "git diff",
    "npm test"
  ],
  "autoDeny": [
    "curl | bash",
    "wget -O- | sh"
  ],
  "rules": [
    {
      "tool": "Bash",
      "command": "git push",
      "behavior": "ask"
    },
    {
      "tool": "Bash",
      "command": "npm run deploy",
      "behavior": "ask"
    }
  ]
}
```

---

## 使用时机

**必须进行权限检查的场景：**

1. 执行任何 Shell 命令（Bash/PowerShell）
2. 删除、修改文件
3. 网络请求（curl/wget）
4. 系统配置修改
5. 安装依赖（npm install / pip install）
6. Git push / force push
7. Docker 操作
8. 任何涉及 `sudo` 的命令

---

## 响应格式

### 询问用户

```
🔐 Permission required

Tool: Bash
Command: git push origin main
Reason: 即将推送到远程仓库

[Allow] [Deny] [Don't ask again] [Configure rules]
```

### 自动允许

```
✅ Auto-allowed: git status
（匹配自动模式白名单）
```

### 自动拒绝

```
🚫 Auto-denied: rm -rf /*
Reason: 危险命令，已拦截
```

---

## 禁止事项

❌ **不要**在未检查权限的情况下执行删除操作
❌ **不要**执行包含敏感信息（API keys、密码）的命令
❌ **不要**忽略危险命令拦截
❌ **不要**在 `bypass` 模式下执行非测试操作
❌ **不要**让 `curl | bash` 类型的命令通过
❌ **不要**执行 `eval` 类型的动态代码命令
