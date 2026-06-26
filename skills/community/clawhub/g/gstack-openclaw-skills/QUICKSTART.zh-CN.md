# 快速开始指南

<div align="center">

**5 分钟开始使用 GStack-Skills**

[English](QUICKSTART.md) | 简体中文

</div>

---

## 🎯 你将学到

1. 如何在 1 分钟内安装 GStack-Skills
2. 如何使用最常用的命令
3. 如何通过对话与 AI 交互
4. 如何在 2 分钟内完成代码审查

---

## ⏱️ 时间估算

- 安装：1 分钟
- 第一次使用：30 秒
- 完成第一个任务：2 分钟
- **总计**：3-4 分钟

---

## 📦 前提条件

在开始之前，确保你已经：

- ✅ 安装了 OpenClaw 或 WorkBuddy
- ✅ 可以运行命令行终端
- ✅ 有基本的 Git 知识

如果没有安装 OpenClaw/WorkBuddy，请先访问 [openclaw.dev](https://openclaw.dev) 下载安装。

---

## 🚀 第一步：安装（1 分钟）

### 方法 1：对话式安装（推荐）⭐

只需与 OpenClaw/WorkBuddy 对话：

```
User: 请帮我安装 gstack-skills
```

AI 会自动：
1. 克隆仓库
2. 检测你的平台
3. 复制技能到正确位置
4. 验证安装
5. 告诉你已完成

**就这么简单！**

---

### 方法 2：一键脚本安装

#### macOS/Linux

```bash
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
./install.sh
```

#### Windows

```batch
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
install.bat
```

---

### 验证安装

重启 OpenClaw/WorkBuddy，然后说：

```
User: /gstack
```

如果你看到帮助信息，说明安装成功！

---

## 💬 第二步：第一次使用（30 秒）

### 尝试基本命令

在 OpenClaw/WorkBuddy 中输入：

```
User: /gstack
```

你会看到所有可用命令：

```
可用命令：
/review           - 代码审查
/qa               - 测试
/ship             - 部署
/office-hours     - 产品验证
/investigate      - 调试
... 以及更多
```

---

### 尝试自然语言

你也可以使用自然语言：

```
User: 帮我审查代码
```

AI 会理解你的意思并执行 `/review` 命令。

---

## ⚡ 第三步：完成第一个任务（2 分钟）

### 场景：审查当前代码

假设你刚刚完成了一些代码修改，现在要审查：

```
User: /review
```

AI 会：

1. 检查你的代码
2. 找到问题
3. 提供修复建议
4. 告诉你结果

**整个过程自动完成，你不需要做任何事！**

---

### 完整示例

让我们看一个完整的对话示例：

```
User: /review

AI: 正在审查当前分支...

📋 审查结果
分支：feature/user-authentication
文件：3 个
新增：+127 行，删除：-45 行

🐛 发现的问题
❌ 1. src/db/queries.py:42 - SQL 注入风险
⚠️ 2. src/utils/logger.js:23 - 使用过时的 API

✅ 自动修复
1. 修复 SQL 注入
2. 替换为 winston 日志库

状态：✅ 完成
建议：运行 /qa 测试
```

**完成！** 只需要 2 分钟。

---

## 🎓 第四步：尝试更多命令

### 测试代码

```
User: /qa
```

AI 会运行测试并修复 bug。

### 部署代码

```
User: /ship
```

AI 会部署到生产环境。

### 调试问题

```
User: /investigate 登录失败
```

AI 会找到根本原因并修复。

---

## 💡 实用技巧

### 技巧 1：链式命令

一次执行多个任务：

```
User: 审查、测试并部署
```

AI 会按顺序执行所有步骤。

---

### 技巧 2：使用自然语言

你不需要记住命令：

```
User: 我刚写完代码，帮我检查一下

AI: 我来审查你的代码...
[执行 /review]
```

---

### 技巧 3：查看详细输出

如果需要更多信息：

```
User: /review --verbose
```

---

### 技巧 4：获取帮助

随时可以问：

```
User: /gstack help
```

或：

```
User: 我该怎么用 /qa？
```

---

## 📚 最常用的命令

| 命令 | 描述 | 使用频率 |
|------|------|---------|
| `/review` | 代码审查 | ⭐⭐⭐⭐⭐ |
| `/qa` | 测试 | ⭐⭐⭐⭐⭐ |
| `/ship` | 部署 | ⭐⭐⭐⭐ |
| `/gstack` | 帮助 | ⭐⭐⭐ |
| `/investigate` | 调试 | ⭐⭐⭐ |

建议从这些命令开始！

---

## 🎯 快速参考

### 日常开发流程

```
1. 审查代码
   /review

2. 运行测试
   /qa

3. 部署
   /ship
```

---

### 问题解决流程

```
1. 调试问题
   /investigate 描述问题

2. 修复后测试
   /qa

3. 验证并部署
   /ship
```

---

### 新功能开发流程

```
1. 验证想法
   /office-hours 描述想法

2. 审查架构
   /plan-eng-review 架构设计

3. 开发...

4. 审查代码
   /review

5. 测试
   /qa

6. 部署
   /ship
```

---

## 🚨 常见问题快速解决

### 问题：命令没有响应

**解决**：
1. 检查是否安装成功：`/gstack`
2. 重启 OpenClaw/WorkBuddy
3. 查看 [INSTALL.md](INSTALL.md)

---

### 问题：不知道该用哪个命令

**解决**：
```
User: /gstack help
```

或直接描述你要做的事：

```
User: 我想检查代码质量
```

---

### 问题：测试失败

**解决**：
```
User: /qa --verbose
```

查看详细错误信息。

---

## 📖 下一步

恭喜！你已经掌握了基础知识。现在可以：

### 1. 查看详细文档

- [对话指南](CONVERSATION_GUIDE.md) - 20+ 真实对话示例
- [使用指南](USAGE.md) - 完整功能详解
- [使用示例](EXAMPLES.md) - 6 个完整案例

### 2. 尝试高级功能

- 自定义技能配置
- 链式命令
- 团队协作

### 3. 深入学习

- 阅读源代码
- 贡献代码
- 加入社区

---

## 🎉 总结

你现在可以：

✅ 使用 GStack-Skills 自动化开发流程
✅ 通过对话与 AI 交互
✅ 2 分钟完成 30 分钟的工作
✅ 专注于创造性的任务

**下一步**：开始你的第一个项目！

---

## 💬 获得帮助

如果遇到问题：

- 📖 查看 [CONVERSATION_GUIDE.md](CONVERSATION_GUIDE.md)
- 📖 查看 [USAGE.md](USAGE.md)
- 🐛 提交 Issue：https://github.com/AICreator-Wind/gstack-openclaw-skills/issues
- 💬 加入社区讨论

---

## 🌟 开始使用

现在就开始使用 GStack-Skills：

```
User: /review
```

**让 AI 为你工作！** 🚀

---

<div align="center">

**3 分钟，从新手到专家**

[返回主页](README.zh-CN.md) • [对话指南](CONVERSATION_GUIDE.md) • [使用示例](EXAMPLES.md)

</div>
