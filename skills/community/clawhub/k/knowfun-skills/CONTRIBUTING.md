# Contributing to Knowfun Skills

[English](#english) | [简体中文](#简体中文)

---

## English

Thank you for your interest in contributing to Knowfun Skills! This document provides guidelines for contributing.

### 🤝 How to Contribute

We welcome contributions in many forms:
- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Code contributions
- 🌍 Translations
- ✨ Example additions

### 📋 Before You Start

1. Check existing [Issues](../../issues) to avoid duplicates
2. For major changes, open an issue first to discuss
3. Read our [Code of Conduct](CODE_OF_CONDUCT.md)

### 🐛 Reporting Bugs

When reporting bugs, please include:
- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**:
  - Platform (Claude Code / Cursor / Cline)
  - OS and version
  - API version
- **Logs**: Relevant error messages or logs

### 💡 Suggesting Features

Feature requests should include:
- **Use Case**: Why this feature is needed
- **Proposed Solution**: How it could work
- **Alternatives**: Other approaches you considered
- **Additional Context**: Screenshots, examples, etc.

### 🔧 Code Contributions

#### Setup Development Environment

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/knowfun-skills.git
cd knowfun-skills

# 3. Create a branch
git checkout -b feature/your-feature-name

# 4. Set up environment
cp .env.example .env
# Add your API key to .env

# 5. Test your changes
./scripts/test-api.sh
```

#### Coding Standards

**Shell Scripts**:
- Use `#!/bin/bash` shebang
- Include error handling with `set -e`
- Add comments for complex logic
- Use meaningful variable names
- Test with shellcheck if available

**Documentation**:
- Write in clear, simple English
- Provide examples
- Update both EN and CN versions if possible
- Use proper markdown formatting

**Commit Messages**:
```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat: add support for video tasks`
- `fix: correct API endpoint in CLI script`
- `docs: update installation guide for macOS`

#### Pull Request Process

1. **Update Documentation**: If you changed functionality, update docs
2. **Test Thoroughly**: Test on all supported platforms if possible
3. **Update Changelog**: Add entry to CHANGELOG.md
4. **Create PR**: Use a clear title and description
5. **Address Feedback**: Respond to review comments

**PR Title Format**:
```
[Type] Brief description
```

**PR Description Should Include**:
- What changed and why
- Related issue numbers (e.g., "Fixes #123")
- Testing done
- Screenshots (if UI-related)

### 📝 Documentation Contributions

Documentation improvements are highly valued! You can:
- Fix typos or clarify instructions
- Add examples
- Improve translations
- Create tutorials

### 🌍 Translation Guidelines

When translating:
- Maintain the same structure as English version
- Keep technical terms in English when appropriate
- Add language switcher links at the top
- Name Chinese files with `_CN.md` suffix

### ✅ Testing

Before submitting:
```bash
# Test API connectivity
./scripts/test-api.sh

# Test CLI commands
./scripts/knowfun-cli.sh credits
./scripts/knowfun-cli.sh list

# Check for shell script issues
shellcheck scripts/*.sh  # if shellcheck is installed
```

### 📦 Adding New Features

New features should:
- Be documented with examples
- Include error handling
- Work across all platforms (Claude Code, Cursor, Cline, OpenClaw)
- Be backward compatible when possible
- Not require additional dependencies

### 🔐 Security

**NEVER commit**:
- API keys
- Personal tokens
- Credentials
- `.env` files with real values

If you discover a security vulnerability:
- **DO NOT** open a public issue
- Follow our [Security Policy](SECURITY.md)

### 📞 Getting Help

- **Questions**: Open a [Discussion](../../discussions)
- **Bugs**: Open an [Issue](../../issues)
- **Chat**: Join our community (link TBD)

### 🎯 Good First Issues

Look for issues tagged with `good-first-issue` - these are great for new contributors!

### 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 简体中文

感谢您对 Knowfun Skills 的贡献兴趣！本文档提供贡献指南。

### 🤝 如何贡献

我们欢迎多种形式的贡献：
- 🐛 Bug 报告
- 💡 功能建议
- 📝 文档改进
- 🔧 代码贡献
- 🌍 翻译
- ✨ 示例添加

### 📋 开始之前

1. 检查现有的 [Issues](../../issues) 以避免重复
2. 对于重大更改，先开issue讨论
3. 阅读我们的[行为准则](CODE_OF_CONDUCT.md)

### 🐛 报告Bug

报告Bug时，请包含：
- **描述**：问题的清晰描述
- **复现步骤**：详细的复现步骤
- **预期行为**：您期望发生什么
- **实际行为**：实际发生了什么
- **环境**：
  - 平台 (Claude Code / Cursor / Cline)
  - 操作系统和版本
  - API 版本
- **日志**：相关错误消息或日志

### 💡 建议功能

功能请求应包含：
- **使用场景**：为什么需要此功能
- **建议方案**：如何实现
- **替代方案**：您考虑的其他方法
- **补充信息**：截图、示例等

### 🔧 代码贡献

#### 设置开发环境

```bash
# 1. Fork 仓库
# 2. 克隆您的 fork
git clone https://github.com/YOUR_USERNAME/knowfun-skills.git
cd knowfun-skills

# 3. 创建分支
git checkout -b feature/your-feature-name

# 4. 设置环境
cp .env.example .env
# 在 .env 中添加您的 API key

# 5. 测试更改
./scripts/test-api.sh
```

#### 编码规范

**Shell 脚本**：
- 使用 `#!/bin/bash` shebang
- 使用 `set -e` 包含错误处理
- 为复杂逻辑添加注释
- 使用有意义的变量名
- 如果可能，使用 shellcheck 测试

**文档**：
- 使用清晰简单的语言
- 提供示例
- 如果可能，更新中英文版本
- 使用正确的 markdown 格式

**提交消息**：
```
<类型>: <主题>

<正文>

<页脚>
```

类型：`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

示例：
- `feat: 添加视频任务支持`
- `fix: 修正CLI脚本中的API端点`
- `docs: 更新macOS安装指南`

#### Pull Request 流程

1. **更新文档**：如果更改了功能，更新文档
2. **彻底测试**：如果可能，在所有支持的平台上测试
3. **更新变更日志**：在 CHANGELOG.md 中添加条目
4. **创建PR**：使用清晰的标题和描述
5. **处理反馈**：回应审查意见

**PR 标题格式**：
```
[类型] 简短描述
```

**PR 描述应包含**：
- 更改了什么以及原因
- 相关issue编号（例如"Fixes #123"）
- 已完成的测试
- 截图（如果与UI相关）

### 📝 文档贡献

文档改进非常有价值！您可以：
- 修正错别字或澄清说明
- 添加示例
- 改进翻译
- 创建教程

### 🌍 翻译指南

翻译时：
- 保持与英文版本相同的结构
- 适当时保留技术术语的英文
- 在顶部添加语言切换链接
- 中文文件使用 `_CN.md` 后缀命名

### ✅ 测试

提交前：
```bash
# 测试 API 连接
./scripts/test-api.sh

# 测试 CLI 命令
./scripts/knowfun-cli.sh credits
./scripts/knowfun-cli.sh list

# 检查 shell 脚本问题
shellcheck scripts/*.sh  # 如果安装了 shellcheck
```

### 📦 添加新功能

新功能应该：
- 有文档和示例
- 包含错误处理
- 在所有平台上工作（Claude Code, Cursor, Cline, OpenClaw）
- 尽可能向后兼容
- 不需要额外的依赖

### 🔐 安全

**永远不要提交**：
- API keys
- 个人令牌
- 凭证
- 包含真实值的 `.env` 文件

如果您发现安全漏洞：
- **不要**开放公开 issue
- 遵循我们的[安全政策](SECURITY.md)

### 📞 获取帮助

- **问题**：开启[讨论](../../discussions)
- **Bug**：开启[Issue](../../issues)
- **聊天**：加入我们的社区（链接待定）

### 🎯 新手友好问题

寻找标记为 `good-first-issue` 的问题 - 这些非常适合新贡献者！

### 📜 许可证

通过贡献，您同意您的贡献将根据 MIT 许可证授权。

---

Thank you for contributing! 感谢您的贡献！
