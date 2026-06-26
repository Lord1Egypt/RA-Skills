# jest-unittest

基于 Jest 的组件单元测试管理 Skill，提供覆盖率检测、自动补全测试、诊断修复能力。

## 一、适用范围

- 使用 **Jest** 作为测试框架的前端项目

## 二、使用方式

首次使用时 AI 会自动引导配置，通常不需要手动操作。

| 用户Prompt | AI 做什么 |
|------|----------|
| 调用skill, 检查单测覆盖率 | 运行全量测试，输出未达 100% 的组件列表 |
| 调用skill, 补全 button 组件单测 | 自动编写测试用例直到四项覆盖率全部 100% |
| 调用skill, button单测报错, 修复 | 诊断失败原因，提供修复方案或自动修复 |
| jest-unittest reload | 重新读取 jest 配置并生成 config.json（修改了 jest 配置后使用） |

## 三、reload 机制详解

### 什么是 reload？

reload 是一个 **配置刷新流程**，作用是：
1. 读取 Jest 配置文件（从 `source.json` 指定的路径）
2. 计算生成 `config.json`

### 何时触发自动 reload

| 触发条件 | 说明 |
|---------|------|
| 首次使用 | AI 自动创建 `source.json`，然后执行 reload 生成 `config.json` |
| 缺少 `config.json` | 脚本检测到 `config.json` 不存在，自动执行 reload |
| `source.json` 为空 | Jest 配置路径未指定，reload 失败并提示用户 |
| Jest 配置文件不存在 | reload 无法找到配置文件，返回错误提示 |
| 项目切换 | 检测到项目根目录变化（git 哈希不同），自动为新项目执行 reload |

### 何时需要手动 reload

**场景 1：修改了 Jest 配置文件**

当你修改以下内容时，需要手动 reload：
- Jest 配置文件位置（例如从 `jest.config.js` 改为 `jest.config.ts`）
- Jest 配置内容（例如修改了 `collectCoverageFrom`、`testMatch` 等）
- 测试目录或组件目录的位置

**场景 2：切换 Jest 配置源**

从一个配置文件切换到另一个时需要 reload（例如从 `jest.config.components.ts` 切换到 `jest.config.cards.ts`）

**场景 3：重置配置**

需要重新生成 `config.json` 时手动 reload

### reload 失败排查

**错误：`Cannot find module 'jest'`**
- 原因：Jest 未安装
- 解决：运行 `pnpm install`

**错误：`Jest configuration not found at [path]`**
- 原因：`source.json` 中的 `jestConfigPath` 路径错误
- 解决：修改 `source.json` 的 `jestConfigPath`，然后重新 reload

**错误：`jestConfigPath is empty`**
- 原因：`source.json` 中没有指定配置文件路径
- 解决：手动编辑 `source.json`，添加正确的 `jestConfigPath`

**错误：`Cannot find component directory`**
- 原因：Jest 配置中无法识别组件目录
- 解决：确保 Jest 配置中有 `roots` 或 `collectCoverageFrom` 字段


## 四、.temp 目录详解

### 1、目录结构

```
.temp/
├── projects/
│   └── <project-hash>/          # 项目隔离目录（基于项目路径的 MD5 哈希前 8 位）
│       ├── source.json          # 用户配置文件（可编辑）
│       └── config.json          # 自动生成的配置（禁止手动编辑）
└── coverage/                    # 测试覆盖率报告
    ├── all/                     # 全量测试覆盖率
    │   ├── coverage-final.json  # 机器可读的覆盖数据
    │   ├── lcov.info           # LCOV 格式覆盖率数据
    │   └── lcov-report/        # HTML 覆盖率报告
    └── <component-name>/        # 单个组件的覆盖率报告
        ├── coverage-final.json
        ├── lcov.info
        └── lcov-report/
```

### 2、用途说明

#### （1）项目配置隔离

**source.json**（用户可编辑）：
```json
{
  "jestConfigPath": "jest.config.components.ts"
}
```
- 用户手动指定 Jest 配置文件路径
- 首次使用时由 AI 自动生成
- 修改后需要执行 `reload` 命令生效

**config.json**（自动生成，禁止手动编辑）：
```json
{
  "jestConfigPath": "jest.config.components.ts",
  "coverageDir": "····",
  // ···
}
```
- 从 Jest 配置文件自动提取的参数化信息
- 用于生成测试命令，所有脚本都依赖此文件
- 发生变化时自动覆盖（无需手动修改）

#### （2）多项目支持

- **隔离方式**：使用项目根目录路径的 MD5 哈希前 8 位作为标识
- **示例**：
  ```
  Project A: /Users/xxx/project-a → hash: abc123de
    .temp/projects/abc123de/config.json
  
  Project B: /Users/xxx/project-b → hash: def456gh
    .temp/projects/def456gh/config.json
  ```

### 何时清理 .temp

- ✅ 可以安全删除
- ✅ 首次使用或删除后会自动重新生成
- ✅ 清理后下次运行会自动恢复
- ❌ 不要手动编辑 `config.json`（会导致不一致）
- ❌ 不要删除 `source.json` 中的用户配置（使用 reload 重新生成）

---


## 注意

- `config.json` 由 AI 自动生成，**禁止手动编辑**
- `source.json` 可以手动编辑，修改后需要执行 `reload` 命令生效
- `.temp/`，不建议纳入git版本管理
- 删除 `.temp/` 后首次使用会自动重新生成，无需担心
