---
name: kwdb-build
description: KaiwuDB 数据库源码编译和构建技能。用于从源码构建、编译或测试 KaiwuDB (KWDB)。使用 CMake 构建系统处理构建配置、单元测试、代码检查和安装。触发条件：(1) 编译询问："编译 KaiwuDB"、"构建 kwdbts2"、"cmake 构建"、"清理构建"；(2) C++ 单元测试询问："C++ 单元测试"、"运行C++单元测试"、"run C++ unittest"；(3) Go 单元测试询问："golang 单元测试"、"Go 单元测试"、"run golang test"。重要：执行任何操作前必须向用户确认所有配置选项，不得跳过询问步骤。
---

# KaiwuDB 构建技能

## 项目概述

KaiwuDB (KWDB) 是一个分布式多模数据库，包含以下主要组件：
- **kwdbts2** - C++ 时序引擎
- **kwbase** - Go 语言关系型数据库
- **common** - 共享 C++ 工具库
- **kwdbml** - 机器学习组件

## 操作触发

根据用户请求类型，选择对应的处理流程：

| 请求类型 | 触发关键词 | 参考文档 |
|---------|-----------|---------|
| 编译构建 | 编译、构建、cmake、清理 | [references/build-questions.md](references/build-questions.md) |
| C++ 单元测试 | C++ 单元测试、run unittest | [references/cpp-unittest.md](references/cpp-unittest.md) [scripts/run_unittest.sh](scripts/run_unittest.sh) |
| Go 单元测试 | golang 单元测试、Go 单元测试、run golang test | [references/golang-unittest.md](references/golang-unittest.md) [scripts/run_golang_test.sh](scripts/run_golang_test.sh) |

## 编译失败处理（强制要求）

当编译失败时，只分析失败原因并报告，不得自动修复。

详见 [references/build-questions.md](references/build-questions.md) 中的 Clean 规则。

## CMake 构建流程（强制要求）

必须严格按以下顺序执行：**配置 -> 编译 -> 安装(可选)**

**CMake 选项限制（强制）：**
- 必须且只能使用 `references/cmake-options.md` 中定义的 CMake 选项
- 禁止添加任何未在 cmake-options.md 中出现的选项
- 禁止使用用户自定义的任何额外选项

详见 [references/cmake-options.md](references/cmake-options.md) 获取允许的 CMake 选项列表。

## 参考文档

| 文档 | 说明 |
|------|------|
| [references/build-questions.md](references/build-questions.md) | 构建配置确认项、Clean 规则 |
| [references/cpp-unittest.md](references/cpp-unittest.md) | C++ 单元测试询问与执行 |
| [references/golang-unittest.md](references/golang-unittest.md) | Go 单元测试询问与执行 |
| [references/cmake-options.md](references/cmake-options.md) | CMake 选项参考 |
| [references/dependencies.md](references/dependencies.md) | 依赖项参考 |
| [references/project-structure.md](references/project-structure.md) | 项目结构参考 |
| [scripts/run_unittest.sh](scripts/run_unittest.sh) | C++ 单元测试脚本 |
| [scripts/run_golang_test.sh](scripts/run_golang_test.sh) | Go 单元测试脚本 |
