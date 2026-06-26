# Git Commit Helper

智能 Git Commit Message 生成器 - 根据代码变更自动生成规范的 commit message。

## 功能

- 🤖 **智能分析**：分析 git diff，理解代码变更内容
- 📝 **规范生成**：生成符合 Conventional Commits 规范的 message
- 🌍 **多语言**：支持中文和英文 commit message
- 🎯 **类型识别**：自动识别 feat/fix/docs/style/refactor/test/chore 等类型
- ⚡ **一键使用**：复制即可用，支持自定义修改

## 使用方式

```
帮我生成 commit message
```

或在 git 仓库中：
```
git add .
分析当前变更并生成 commit message
```

## 输出示例

```
feat(user): 添加用户登录验证功能

- 实现 JWT token 生成和验证
- 添加登录接口 /api/auth/login
- 添加密码加密处理
- 编写单元测试

Closes #123
```

## 支持的类型

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具/配置

## 作者

倒里牢数 · 严谨专业版

## 版本

1.0.0
