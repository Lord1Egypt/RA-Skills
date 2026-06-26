# Git Commit Helper 🚀

智能 Git Commit Message 生成器 - 让提交记录更专业，节省时间！

## ✨ 功能亮点

- 🤖 **AI 智能分析**：自动理解代码变更内容
- 📝 **规范输出**：符合 Conventional Commits 规范
- 🌍 **中英双语**：支持中文和英文
- ⚡ **一键生成**：复制即用，可自定义修改
- 🎯 **类型识别**：自动识别 feat/fix/docs 等类型

## 🎯 适用场景

- 日常代码提交
- 团队协作开发
- 开源项目贡献
- 代码审查准备
- Git 提交规范化

## 📦 安装

```bash
# 从 ClawHub 安装
npx clawhub@latest install git-commit-helper

# 或从本地安装
npx clawhub@latest install ./skills/git-commit-helper
```

## 💬 使用示例

### 基础用法
```
帮我生成 commit message
```

### 指定语言
```
生成英文 commit message
```

### 完整流程
```bash
git add .
# 然后让 AI 生成 commit message
# 复制输出，粘贴到 git commit -m "..."
```

## 📝 输出示例

```
feat(auth): 添加用户登录验证功能

- 新增 login.js
- 新增 auth.test.js
- 更新 config.json
```

## 🎨 支持的提交类型

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| `feat` | 新功能 | 添加新功能 |
| `fix` | 修复 | 修复 bug |
| `docs` | 文档 | 文档更新 |
| `style` | 格式 | 代码格式调整 |
| `refactor` | 重构 | 代码重构 |
| `test` | 测试 | 添加/修改测试 |
| `chore` | 杂项 | 构建/配置/工具 |

## 💡 最佳实践

1. **先 git add，再生成**：确保分析的是暂存区变更
2. **检查生成结果**：AI 可能不完全理解业务逻辑
3. **适当修改**：根据需要调整描述
4. **保持一致**：团队内统一语言风格

## 🛠️ 技术栈

- Node.js
- Git CLI
- 规则引擎

## 📄 许可证

MIT License

## 👨‍💻 作者

倒里牢数 · 严谨专业版

---

**让 Git 提交更专业！** 💪
