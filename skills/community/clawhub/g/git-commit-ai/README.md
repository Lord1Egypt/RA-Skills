# git-commit-ai

<div align="center">

**根据 git diff 自动生成符合规范的 commit message**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node: >=16](https://img.shields.io/badge/Node-%3E%3D16-brightgreen.svg)](https://nodejs.org/)

**一个 Claude Code CLI Skill**

</div>

---

## 特性

- **详细描述** - 从 diff 中提取具体信息（函数名、组件名、注释等）
- **智能语言检测** - 根据代码注释自动选择中文/英文
- **符合规范** - 完全符合 Angular commit 规范
- **敏感信息检测** - 自动检测 diff 中的密码、API 密钥等敏感信息
- **Git Hook 支持** - 可安装 prepare-commit-msg hook（支持 `--force` 强制覆盖）

---

## 效果对比

### 优化前

```
feat: add new feature
fix: fix bug
refactor: update code
```

### 优化后

**中文代码**:
```
feat(auth): 添加用户登录验证功能，支持邮箱格式校验
fix(api): 修复 getUser 接口的空指针异常
refactor(utils): 提取邮箱验证逻辑到独立函数
```

**英文代码**:
```
feat(auth): add user login validation with email format check
fix(api): resolve null pointer exception in getUser endpoint
refactor(utils): extract email validation to reusable function
```

---

## 使用方法

### 基本使用

```bash
# 自动检测语言（推荐）
/git-commit-ai

# 强制使用中文
/git-commit-ai --language zh

# 强制使用英文
/git-commit-ai --language en

# 显示帮助
/git-commit-ai --help

# 显示版本
/git-commit-ai --version

# 安装 Git hook（如已存在会自动备份）
/git-commit-ai --install

# 强制覆盖现有 Git hook
/git-commit-ai --install --force
```

### 完整工作流程

```bash
# 1. 暂存改动
git add .

# 2. 生成 commit message
/git-commit-ai

# 3. 复制生成的 message 并提交
git commit -m "feat(auth): 添加用户登录验证功能"
```

---

## 多语言支持

### 自动检测（默认）

Skill 会根据代码注释的语言自动选择生成相应语言的 commit message。

**中文代码示例**:
```javascript
// 添加用户登录验证
export function validateLogin(email, password) {
  // 验证邮箱格式
  if (!email.includes('@')) {
    throw new Error('邮箱格式不正确');
  }
}
```
**生成**: `feat(auth): 添加用户登录验证，支持邮箱格式校验`

**英文代码示例**:
```javascript
// Add user login validation
export function validateLogin(email, password) {
  // Validate email format
  if (!email.includes('@')) {
    throw new Error('Invalid email format');
  }
}
```
**生成**: `feat(auth): add user login validation with email format check`

---

## 支持的 Commit 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | feat(auth): 添加用户登录验证 |
| `fix` | Bug 修复 | fix(api): 修复空指针异常 |
| `docs` | 文档变更 | docs(readme): 更新安装说明 |
| `style` | 代码格式 | style: 格式化代码 |
| `refactor` | 重构 | refactor(utils): 提取公共函数 |
| `perf` | 性能优化 | perf(db): 优化查询性能 |
| `test` | 测试 | test: 添加单元测试 |
| `chore` | 构建/工具 | chore: 更新依赖版本 |

---

## 使用示例

### 新增功能
```diff
+// 添加用户认证模块
+export function authenticateUser(email, password) {
+  // 验证用户信息
+  return validateCredentials(email, password);
+}
```
**生成**: `feat(auth): 添加用户认证模块，支持邮箱密码验证`

### Bug 修复
```diff
-  const user = await getUser(userId);
+  const user = await getUser(userId);
+  if (!user) {
+    throw new Error('User not found');
+  }
```
**生成**: `fix(api): 修复 getUser 的空指针异常`

### 重构
```diff
+export function validateEmail(email) {
+  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
+  return regex.test(email);
+}
```
**生成**: `refactor(utils): 提取邮箱验证逻辑到独立函数`

---

## Git Hook 功能

### 安装 Hook
```bash
/git-commit-ai --install
```
这会在 `.git/hooks/` 目录下创建 `prepare-commit-msg` hook，每次执行 `git commit` 时都会提醒你使用本工具生成 commit message。

### 卸载 Hook
```bash
rm .git/hooks/prepare-commit-msg
```

---

## 工作原理

1. **获取 Git diff** - 读取 `git diff --cached` 的内容
2. **分析变更** - 识别类型、提取函数名、注释、文件路径等
3. **智能检测** - 根据代码注释语言自动选择
4. **生成 message** - 使用 Claude AI 生成详细的描述

---

## 分析能力

### 从 diff 中提取的信息

- **函数名和组件名** - `validateLogin()` → "用户登录验证"
- **代码注释** - `// 添加用户认证` → 理解意图 + 语言检测
- **文件路径** - `src/auth/login.js` → scope: auth
- **API 端点** - `/api/users` → "users API"
- **具体改动** - 新增/删除/修改的代码行

---

## 注意事项

1. **需要暂存的改动** - 运行前请先 `git add`
2. **Git 仓库** - 必须在 Git 仓库中运行
3. **语言检测** - 基于代码注释，建议添加清晰的注释

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

[MIT License](./LICENSE)