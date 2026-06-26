---
name: huo15-openclaw-security-review
displayName: 火一五安全评审技能
description: 对当前分支的 pending changes 做安全评审，命中密钥泄露 / SQL 注入 / XSS / SSRF / 权限绕过 / 危险依赖 六大类漏洞后出分级报告，再在用户批准下修复。用于 PR 合并前、对外开源前、线上事故后复盘。触发词：安全评审、security review、漏洞检查、密钥扫描、我的代码有没有安全问题。
version: 1.0.0
aliases:
  - 火一五安全评审
  - 安全评审
  - security review
  - 安全审查
  - 漏洞检查
  - 密钥扫描
license: MIT
---

# 火一五安全评审技能 v1.0

> 六类漏洞矩阵 + 严重度分级 + 修复建议 — 青岛火一五信息科技有限公司

---

## 一、触发场景

- "帮我做个 security review"
- "这个 PR 有没有安全问题"
- "扫一下密钥泄露"
- "合并前做安全检查"
- "看看有没有 SQL 注入"

**范围**：默认 `git diff main...HEAD`（当前分支相对主干的全部改动）；用户可指定文件或 commit 范围。

**产出**：六类漏洞清单 + CVSS-like 严重度 + 每条修复建议 + 与 CWE 对照。

---

## 二、六类漏洞矩阵

### 类别 1：**敏感信息泄露（Secrets Leak）**

| 检查项 | 信号 |
|--------|------|
| 硬编码 API key / token | `/api[_-]?key\s*[:=]\s*["']([A-Za-z0-9_\-]{20,})["']/i` |
| 硬编码密码 / JWT secret | `password\s*[:=]\s*["'][^"']{6,}["']`、`jwt.*secret.*=` |
| `.env` 被提交 | `git log --all -- .env` 有记录 |
| 日志打印敏感字段 | `console\.log.*password`、`logger.*token` |
| 提交信息含密钥 | 扫 `git log --all --oneline` 的 message |
| Cloud 密钥格式特征 | AKIA...（AWS）/ ya29....（Google）/ ghp_... / npm_... |

### 类别 2：**注入（Injection）**

| 检查项 | 信号 |
|--------|------|
| SQL 拼接 | `` `SELECT ... ${...}` ``、`+ userInput +` |
| NoSQL 注入 | 未校验的 `$where` / `$regex` |
| 命令注入 | `exec(userInput)` / 模板字符串传 shell |
| 路径遍历 | `path.join(root, userInput)` 未 `path.normalize` + 边界校验 |
| LDAP / XPath / 模板注入 | 同样是拼接 |

### 类别 3：**跨站脚本（XSS）**

| 检查项 | 信号 |
|--------|------|
| `dangerouslySetInnerHTML` | React 直接接用户输入 |
| `innerHTML = userInput` | 原生 DOM |
| `v-html` 未过滤 | Vue |
| 邮件 / 短信模板直接插值 | 出站 XSS（钓鱼）|
| 未设 CSP header | 响应头缺失 |

### 类别 4：**服务端请求伪造（SSRF）**

| 检查项 | 信号 |
|--------|------|
| `fetch(userURL)` 无白名单 | 可被打到 169.254.169.254（云 metadata）|
| 允许 `file://` / `gopher://` 协议 | scheme 未校验 |
| DNS rebinding 窗口 | 二次解析 |

### 类别 5：**权限 / 认证绕过**

| 检查项 | 信号 |
|--------|------|
| 路由缺鉴权中间件 | Express / Next API route 裸接 |
| 水平越权 | 查询时没带 `userId = currentUser.id` |
| 直接对象引用（IDOR）| `GET /api/order/:id` 不校验归属 |
| JWT 不校验 signature | `jwt.decode` 代替 `jwt.verify` |
| 弱密码 / 默认账号残留 | grep `admin/admin123` |

### 类别 6：**危险依赖 / 供应链**

| 检查项 | 信号 |
|--------|------|
| 已知 CVE 依赖 | 建议用户跑 `npm audit` / `pnpm audit` |
| 从 git / tarball 装的依赖 | `package.json` 有 `git+https://...` |
| postinstall 脚本 | 可执行任意代码 |
| `typosquatting` 风险包 | `lodas` / `requets` 之类 |

---

## 三、工作流

1. **确定范围**
   - 默认 `git diff main...HEAD --name-only`
   - 允许用户指定：`commit 范围` / `特定文件` / `整个项目`
2. **只读扫描**
   - Grep 六类信号模式
   - Read 命中文件具体上下文
   - **不执行 `npm audit`** — 返回命令让用户跑（避免长时间阻塞）
3. **严重度评级**
   - 🔴 **Critical**：密钥已泄露到公共仓库 / 可远程代码执行 / 可绕过鉴权
   - 🟠 **High**：SQL 注入 / XSS 反射点 / 可越权读
   - 🟡 **Medium**：缺 CSP / 错误信息外泄 / 路径遍历有部分防御
   - 🟢 **Low**：硬编码但仅 demo / 依赖有 low CVE
4. **产出报告**（见 §四）
5. **修复流程**
   - 🔴 必须用户确认才改（防止误删 legit 用法）
   - 🟠/🟡 列出修复建议，等用户决定
   - 🟢 仅提示

---

## 四、报告模板

```markdown
## 安全评审报告 — <branch> vs main

**扫描范围**：12 个文件变更 · 扫描时间 2s

### 🔴 Critical（1 项，必须修）
1. **[Secrets]** `src/config.ts:18` — 硬编码 OpenAI API key
   - 信号：`sk-proj-...` 匹配
   - CWE-798（硬编码凭据）
   - 修复：移入 `.env`；**立刻在 OpenAI 后台 revoke 此 key**
   - 若已推送：`git filter-repo` 清历史 + force push

### 🟠 High（2 项）
2. **[Injection]** `src/api/search.ts:45` — SQL 拼接用户输入
3. **[Auth]** `src/api/order/[id].ts:12` — 缺归属校验（IDOR）

### 🟡 Medium（1 项）
4. **[XSS]** `components/Post.tsx:33` — dangerouslySetInnerHTML 渲染用户 markdown，未跑 DOMPurify

### 🟢 Low（1 项）
5. **[Dependency]** `package.json` — `lodash@4.17.15` 有 2 个 low CVE；建议升 4.17.21

### 建议跑（用户执行）
```bash
npm audit --production        # 完整依赖漏洞
git log --all -p | grep -E "AKIA|ghp_|sk-proj" | head  # 历史密钥扫描
```
```

---

## 五、硬红线（绝不触碰）

1. **不自动 revoke 线上密钥** — 只提醒用户去后台操作
2. **不自动 `git filter-repo` 改历史** — 返回命令让用户自己执行（破坏性）
3. **不自动 `npm audit fix --force`** — 可能大版本跳跃，给命令让用户决定
4. **不 exec `npm audit`** — 禁 child_process 铁律，返回命令
5. **不把密钥明文打印在报告里** — 脱敏为 `sk-proj-***...last4`
6. **不私自连外网验证密钥是否生效** — 只做静态扫描

---

## 六、与 huo15-openclaw-simplify 的边界

| 场景 | 用哪个 |
|------|--------|
| 只看安全 | **本技能** |
| 只看代码质量 | `huo15-openclaw-simplify` |
| 两者都看 + 给 PR 评论 | `huo15-openclaw-code-review` |

---

## 七、参考 CWE 速查

- CWE-798 硬编码凭据
- CWE-89 SQL 注入
- CWE-79 XSS
- CWE-918 SSRF
- CWE-639 IDOR
- CWE-937 已知漏洞组件
