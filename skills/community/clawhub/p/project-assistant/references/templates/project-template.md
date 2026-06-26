# 项目文档模板

各子skill生成文档时使用此模板。

## 模板结构

```markdown
# 项目概览

> 自动生成于 {DATE}

## 基本信息

| 项目属性 | 值 |
|---------|-----|
| 项目名称 | {NAME} |
| 项目类型 | {TYPE} |
| 主要语言 | {LANGUAGE} |
| 框架/平台 | {FRAMEWORK} |
| 构建系统 | {BUILD_SYSTEM} |
| 目标平台 | {TARGET_PLATFORM} |

## 目录结构

```
{DIRECTORY_TREE}
```

## 模块划分

### 核心模块
| 模块名 | 路径 | 功能描述 |
|-------|------|---------|
{CORE_MODULES}

### 工具模块
| 模块名 | 路径 | 功能描述 |
|-------|------|---------|
{UTIL_MODULES}

## 入口点

- **主入口**: `{MAIN_ENTRY}`
{OTHER_ENTRIES}

## 核心功能

{CORE_FEATURES}

## 依赖关系

### 核心依赖
| 依赖 | 版本 | 用途 |
|-----|------|------|
{DEPENDENCIES}

## 构建指南

```bash
# 安装依赖
{INSTALL_CMD}

# 构建
{BUILD_CMD}

# 运行/部署
{RUN_CMD}

# 测试
{TEST_CMD}
```

## 配置文件

| 配置项 | 文件 | 说明 |
|-------|------|------|
{CONFIG_TABLE}

## 注意事项

{NOTES}

## 相关文件

- 配置文件: {CONFIG_FILES}
{EXTRA_FILES}
```

## 嵌入式项目扩展模板

```markdown
## 目标平台信息

| 属性 | 值 |
|-----|-----|
| MCU/SoC | {MCU} |
| 架构 | {ARCH} |
| 主频 | {FREQ} |
| Flash | {FLASH} |
| RAM | {RAM} |

## 内存布局

| 区域 | 起始地址 | 大小 | 用途 |
|-----|---------|------|------|
{MEMORY_LAYOUT}

## 外设使用

| 外设 | 配置 | 用途 |
|-----|------|------|
{PERIPHERALS}

## RTOS配置 (如有)

| 配置项 | 值 |
|-------|-----|
{RTOS_CONFIG}
```

## Android项目扩展模板

```markdown
## Android配置

| 属性 | 值 |
|-----|-----|
| minSdk | {MIN_SDK} |
| targetSdk | {TARGET_SDK} |
| compileSdk | {COMPILE_SDK} |

## Jetpack组件

{JETPACK_COMPONENTS}

## 第三方库

{THIRD_PARTY_LIBS}
```