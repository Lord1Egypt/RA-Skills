# OpenClaw Flutter Expert Skill

## 简介

这是一个为 OpenClaw 适配的 Flutter 专家技能，基于 skills.sh 上的 [flutter-expert](https://skills.sh/jeffallan/claude-skills/flutter-expert) 改编。

## 原作者

- **原作者**: jeffallan (from skills.sh)
- **原始技能**: https://skills.sh/jeffallan/claude-skills/flutter-expert

## 改编说明

本技能保留了原 skill 的核心内容，并针对 OpenClaw 做了以下适配：

1. 使用 OpenClaw 标准 YAML 头部格式
2. 添加了 OpenClaw 集成说明
3. 更新了技术栈版本至最新稳定版
4. 增强了中文注释和说明

## 技术栈

- Flutter 3.19+
- Riverpod 2.0+
- GoRouter
- 代码生成工具 (freezed, json_serializable)

## 安装

本技能已安装到 OpenClaw workspace，可直接使用：

```
~/.openclaw/workspace/skills/openclaw-flutter-expert/
```

## 使用方法

在 OpenClaw 中，当用户请求 Flutter 相关帮助时，此技能会自动激活，提供：

- Flutter 项目架构建议
- Riverpod 状态管理最佳实践
- GoRouter 路由配置
- 代码质量优化建议
- 性能调优方案
- 测试策略

## 目录结构

```
openclaw-flutter-expert/
├── SKILL.md          # 技能定义文件
├── README.md         # 本文件
└── references/       # 参考文档目录
```

## 贡献

如有问题或改进建议，欢迎提交 Issue 或 PR。

## 许可证

遵循原 skill 的许可证。
