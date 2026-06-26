---
name: huo15-openclaw-code-review
displayName: 火一五代码评审技能
description: 对 GitHub / cnb.cool PR 做综合代码评审（设计 / 实现 / 测试 / 安全 / 可维护五维），借 gh CLI 拉 diff，产出可粘贴到 PR 的评论 markdown。触发词：评审 PR、code review、审一下这个 PR、帮我 review、看看这个合并请求。
version: 1.0.0
aliases:
  - 火一五代码评审
  - 代码评审
  - code review
  - PR 评审
  - 审 PR
  - review PR
license: MIT
---

# 火一五代码评审技能 v1.0

> 五维 PR 评审 + 可粘贴评论 — 青岛火一五信息科技有限公司

---

## 一、触发场景

- "帮我 review PR #123"
- "审一下这个合并请求"
- "code review 一下我的 PR"
- 用户贴 PR URL：`https://github.com/xxx/yyy/pull/123` 或 `https://cnb.cool/.../merge_requests/45`

**产出**：五维清单 + 行内评论建议 + 总评（批准/请改/阻断）+ 一段可直接粘贴到 PR 的 markdown。

---

## 二、评审五维

| 维度 | 关注点 | 不关注 |
|------|-------|-------|
| **1. 设计（Design）** | 方案是否对问题对症 / 抽象是否合适 / 与现有架构一致 | 风格偏好 |
| **2. 实现（Implementation）** | 逻辑正确 / 边界处理 / 错误处理 / 资源回收 | 次要优化 |
| **3. 测试（Tests）** | 关键路径有单测 / 边界 case / 回归 | 100% 覆盖率 |
| **4. 安全（Security）** | 代理 `huo15-openclaw-security-review` 做六类扫描 | — |
| **5. 可维护（Maintainability）** | 命名 / 文档 / 可读性 / 变更局部性 | 代码风格（交给 linter）|

---

## 三、工作流（严格按序）

### Step 1：拉取 PR 元信息

```bash
# GitHub
gh pr view <number> --json title,body,author,baseRefName,headRefName,files,commits,additions,deletions

# cnb.cool（如有 API / CLI）
curl .../merge_requests/<id>
```

**不 exec** — 返回命令让用户粘贴结果，或若上下文里已有就用。

### Step 2：拉取 diff

```bash
gh pr diff <number>
# 或
git diff <base>...<head>
```

### Step 3：分段阅读 + Grep 关键字

- 每个文件至少过一遍
- Grep 高危模式（密钥 / SQL 拼接 / `dangerouslySetInnerHTML`）转交 security-review 思路
- 对新增函数：检查命名、参数、返回值、错误处理

### Step 4：五维评分

对 5 维每个给：
- ✅ Pass
- ⚠️ Minor（可合但建议改）
- ❌ Blocker（必须改）

### Step 5：生成行内评论

每条评论格式：
```
`path/to/file.ts:line` — <简短标题>

<问题描述>
<建议>
```

### Step 6：总评

- **Approve** — 全 ✅ 或只有 🟢 minor
- **Request changes** — 有任何 ⚠️ 影响核心
- **Block** — 有 ❌ 安全 / 数据丢失 / 不兼容风险

---

## 四、报告模板

```markdown
## 📋 Code Review — PR #123 "<title>"

**作者**：@xxx · **变更**：12 文件 +340 -120 · **评审耗时**：5 min

### 五维评分
- Design：✅
- Implementation：⚠️ 2 处
- Tests：⚠️ 缺边界测试
- Security：✅（无新增攻击面）
- Maintainability：✅

### 总评：🟡 Request Changes

必改后合并：1 处 Implementation blocker + 1 处测试缺失。

---

### 行内评论

**`src/api/user.ts:45`** — 边界未处理
当 `userId` 为 `undefined` 时 `db.user.findById(userId)` 会返回所有用户。
建议：函数入口加 `if (!userId) throw new Error(...)`。

**`src/api/user.ts:88`** — 错误吞掉
`catch(e) { return null }` 掩盖了数据库连接错误。
建议：区分「找不到」和「出错」，至少记日志。

**`tests/user.test.ts`** — 缺边界用例
新增的 `mergeProfile` 没测 `null` / `undefined` / `{}` 空对象三种输入。
建议：补 3 条测试用例。

### 其他观察（不阻塞合并）
- 命名 `data` → `userProfile` 可读性更好（src/utils.ts:12）
- 可用 `Pick<User, 'id'|'name'>` 替代手写接口（types.ts:33）

---

🤖 Reviewed by huo15-openclaw-code-review
```

---

## 五、硬红线（绝不触碰）

1. **不 `gh pr review --approve` / `--request-changes`** — 评审意见由人提交（避免 AI 自己批自己的 PR）
2. **不 `gh pr merge`** — 合并决策权归人
3. **不自动 `gh pr comment`** — 除非用户明确说"直接发到 PR 上"
4. **不跑测试 / build** — 除非用户要求
5. **禁 child_process** — `gh` 命令走 return-cliCmd

---

## 六、与相邻技能的边界

| 场景 | 用哪个 |
|------|--------|
| PR 综合评审 | **本技能** |
| 只看安全 | `huo15-openclaw-security-review` |
| 只看代码质量 | `huo15-openclaw-simplify` |
| 只看设计稿 / UI | `huo15-openclaw-design-critique` |
