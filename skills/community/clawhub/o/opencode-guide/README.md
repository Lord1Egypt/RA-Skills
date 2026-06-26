# opencode-guide - OpenCode 使用指南

> 让 OpenClaw 正确调用 opencode 的完整工作流指南

## 🎯 功能特性

- ✅ **完整工作流指南** - 从任务创建到结果汇报的标准流程
- ✅ **自动回调系统** - 任务完成后自动通知 OpenClaw
- ✅ **防错指南** - 避免常见错误和陷阱
- ✅ **最佳实践** - 经过实战验证的使用技巧

## 📦 安装

```bash
clawhub install opencode-guide
```

安装后，脚本会自动复制到 `~/.openclaw/scripts/` 目录。

## 🚀 快速开始

### 调用 opencode 的标准命令

```bash
/home/root1/.openclaw/scripts/opencode-auto-callback.sh \
  "agent:main:qqbot:direct:1de7b85a1abc58fb6caebb5b9255a560" \
  "任务描述" \
  "opencode 参数"
```

### 示例

```bash
# 简单任务
./opencode-auto-callback.sh \
  "agent:main:qqbot:direct:xxx" \
  "修复登录 bug" \
  "修复登录问题"

# 指定模型
./opencode-auto-callback.sh \
  "agent:main:qqbot:direct:xxx" \
  "添加功能" \
  "-m opencode/mimo-v2-pro-free 添加用户认证"

# 继续会话
./opencode-auto-callback.sh \
  "agent:main:qqbot:direct:xxx" \
  "继续任务" \
  "-c 继续刚才的工作"
```

## 📋 核心原则

> **保持交流 > 完成任务**

### ❌ 禁止行为
1. 不自己分析代码
2. 不自己修改文件
3. 不自己执行命令
4. 不擅自行动
5. 不干活失联

### ✅ 正确做法
1. 先确认再执行
2. 分派给专业 agent
3. 使用自动回调脚本
4. 及时汇报保持交流

## 🔧 自动回调系统

### 脚本说明

| 脚本 | 用途 | 推荐度 |
|------|------|--------|
| `opencode-auto-callback.sh` | 简化版，直接调用 | ⭐⭐⭐ 推荐 |
| `opencode-run-with-callback.sh` | 包装器版，可包装任意命令 | ⭐⭐ 备用 |

### 工作流程

```
1. OpenClaw 调用自动回调脚本
2. 发送"任务开始"通知
3. 执行 opencode run
4. 任务完成后自动发送"任务完成"通知
5. OpenClaw 收到通知，继续工作
```

### 优势

- ✅ 异步执行，不阻塞 OpenClaw
- ✅ 自动发送开始/完成通知
- ✅ 自动提取结果摘要
- ✅ 支持超时处理

## 📖 详细文档

- **技能使用说明**：`SKILL.md`
- **脚本详细说明**：`scripts/README-opencode-callback.md`

## 🎓 使用技巧

### 1. 让 opencode 自我 review

```
完成后自我 review 代码：
- 检查 TypeScript 错误
- 检查 API 逻辑
- 检查安全问题
- 有问题修复，没问题报告"review 通过，可以测试"
```

### 2. 分阶段执行复杂任务

```
xxx-part1.txt - 第一阶段
xxx-part2.txt - 第二阶段
```

### 3. 使用 Plan 模式

```
请先分析现有实现，然后出一个详细的 Plan 供用户确认。
输出 Plan，等待用户确认后再开始修改。
```

## 📝 版本历史

### v1.0.0 (2026-04-02)
- ✅ 初始版本
- ✅ 完整工作流指南
- ✅ 自动回调系统
- ✅ 防错指南和最佳实践

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
