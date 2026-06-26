# openclaw-flutter-testing

Flutter 测试全面指导 - 适配 OpenClaw

## 简介

本 Skill 提供全面的 Flutter 测试指导，涵盖单元测试、Widget 测试和集成测试。

## 原作者与来源

- **原作者**: madteacher (from skills.sh)
- **原始来源**: https://skills.sh/madteacher/mad-agents-skills/flutter-testing
- **GitHub**: https://github.com/madteacher/mad-agents-skills

## 改编说明

本 skill 是将 skills.sh 上的 flutter-testing skill 转换为 OpenClaw 格式的版本。

**改编内容**:
- 将原始 skill 内容适配到 OpenClaw 的 SKILL.md 格式
- 添加 OpenClaw 所需的 metadata 配置
- 保留完整的测试指导内容（测试金字塔、Mocking、CI集成等）

## 内容概览

- **单元测试** - 业务逻辑、数据转换、状态管理测试
- **Widget 测试** - UI 渲染、用户交互、状态变化测试
- **集成测试** - 端到端流程、多页面导航、性能分析
- **插件测试** - 平台通道 Mock、Native 代码测试
- **常见错误** - Overflow、viewport、setState 等错误解决方案
- **最佳实践** - 测试金字塔、AAA 模式、CI 集成

## 使用方法

### 在 OpenClaw 中使用

当需要编写 Flutter 测试时，OpenClaw 会自动加载此 skill。你可以直接询问：

- "如何编写 Flutter 单元测试？"
- "Widget 测试怎么写？"
- "如何进行集成测试？"
- "测试中遇到 overflow 错误怎么办？"

### 运行测试命令

```bash
# 运行所有测试
flutter test

# 运行特定测试文件
flutter test test/widget_test.dart

# 运行集成测试
flutter test integration_test/

# 运行带覆盖率
flutter test --coverage
```

## 目录结构

```
openclaw-flutter-testing/
├── SKILL.md           # 主 Skill 文件
├── README.md          # 本文件
└── references/        # 参考文档目录
    ├── unit-testing.md
    ├── widget-testing.md
    ├── integration-testing.md
    ├── mocking.md
    ├── common-errors.md
    └── plugin-testing.md
```

## 依赖要求

- **Flutter SDK**: 已安装 Flutter 环境
- **Dart**: 包含在 Flutter SDK 中

## 参考资源

- [Flutter 官方测试文档](https://docs.flutter.dev/cookbook/testing)
- [flutter_test 包](https://pub.dev/packages/flutter_test)
- [Mockito 包](https://pub.dev/packages/mockito)
- [Integration Test 包](https://pub.dev/packages/integration_test)

## License

本 skill 内容基于原 madteacher/mad-agents-skills 的 MIT License。
