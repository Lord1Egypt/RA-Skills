# git-commit-ai

根据 git diff 自动生成符合规范的 commit message

## 功能说明

这个 skill 会分析当前 Git 仓库的暂存改动，使用 AI 生成详细、准确的 commit message。

**主要特性**:
- 📝 从 diff 中提取具体信息（函数名、组件名、注释等）
- 🌐 智能语言检测（根据代码注释自动选择中文/英文）
- ✅ 符合 Angular commit 规范
- 🎯 详细的描述，不再只说"新增功能"

## 使用方法

### 基本使用

```bash
/git-commit-ai
```

### 带参数使用

```bash
# 强制使用中文
/git-commit-ai --language zh

# 强制使用英文
/git-commit-ai --language en

# 自动检测（默认）
/git-commit-ai --language auto
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--language` | commit message 语言 (auto/zh/en) | auto |

## 使用示例

### 示例 1: 中文代码

**Git Diff**:
```diff
+// 添加用户登录验证
+export function validateLogin(email, password) {
+  // 验证邮箱格式
+  if (!email.includes('@')) {
+    throw new Error('邮箱格式不正确');
+  }
+}
```

**生成结果**:
```
feat(auth): 添加用户登录验证功能，支持邮箱格式校验
```

### 示例 2: 英文代码

**Git Diff**:
```diff
+// Add user login validation
+export function validateLogin(email, password) {
+  // Validate email format
+  if (!email.includes('@')) {
+    throw new Error('Invalid email format');
+  }
+}
```

**生成结果**:
```
feat(auth): add user login validation with email format check
```

## 工作原理

1. **获取 Git diff** - 读取暂存区的改动
2. **分析变更内容** - 识别变更类型、提取关键信息
3. **智能语言检测** - 根据代码注释语言自动选择
4. **生成 message** - 使用 AI 生成详细的 commit message

## 分析能力

### 从 diff 中提取的信息

- ✅ 函数名和组件名
- ✅ 代码注释（用于语言检测和意图理解）
- ✅ 文件路径（用于确定 scope）
- ✅ API 端点和路由
- ✅ 具体的改动内容

### 支持的 commit 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档变更
- `style`: 代码格式
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试
- `chore`: 构建/工具

## 输出格式

生成的 commit message 符合 Angular commit 规范：

```
<type>(<scope>): <description>
```

**示例**:
- `feat(auth): 添加用户登录验证功能`
- `fix(api): 修复 getUser 接口的空指针异常`
- `refactor(utils): 提取邮箱验证逻辑到独立函数`

## 注意事项

1. **需要有暂存的改动** - 运行前请先 `git add`
2. **自动语言检测** - 根据代码注释智能选择语言
3. **详细描述** - 会从代码中提取具体信息，不会只说"新增功能"

## 常见问题

### Q: 为什么没有暂存的改动时会报错？

A: 工具需要分析 git diff --cached 的内容，所以需要先 `git add` 暂存改动。

### Q: 如何强制使用特定语言？

A: 使用 `--language zh` 或 `--language en` 参数。

### Q: 生成的 message 不够准确怎么办？

A: 可以尝试添加更多代码注释，帮助 AI 理解改动的意图。

## 技术实现

- 使用 Git 命令获取 diff
- 通过 Claude AI 分析内容
- 智能提取代码信息
- 生成符合规范的 message

## 相关资源

- [Angular Commit 规范](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Git diff 文档](https://git-scm.com/docs/git-diff)

## 更新日志

### v1.0.0
- ✅ 初始版本
- ✅ 支持中英文自动检测
- ✅ 详细的 diff 分析
- ✅ 符合 Angular commit 规范
