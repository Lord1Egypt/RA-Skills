---
name: unittest-doctor
description: >
  诊断并修复组件单测报错。当用户提到测试失败、测试报错、单测不通过、修复测试、测试错误、act()警告、快照不匹配、snapshot失败、运行单测报错、调试测试时触发。
  支持全量检查或指定组件名，自动诊断失败原因并提供修复方案。
allowed-tools: Read, Edit, MultiEdit, Bash, Glob
---

# 单测医生 (Component Test Doctor)

你的任务是运行组件单测，诊断并报告测试失败和 console 警告/错误，然后根据用户意愿自动修复问题。

## 前置：读取配置

脚本会自动校验配置和环境。如果返回 `error` 字段，根据 `type` 处理：`config_error` 按 `hint` 配置 `source.json`（路径见 `sourceJsonPath`）后执行 `node ../../scripts/reload.cjs` 重试；`env_error` 根据 `error` 排查环境后重试。

从配置中获取以下变量，后续步骤中使用：
- `componentDir` + 组件名 → 拼接得到 `$PATH`（如 `src/views/_components/button`）
- `testDir` → 测试目录名 `$testDir`（如 `__tests__`）
- `updateSnapshotCommand` → 更新快照的命令

获取方式：运行 `node ../../scripts/reload.cjs`，从其输出的 JSON 中读取上述字段。如果配置已存在（脚本运行不报错），则直接使用。

## 执行流程

### Step 1: 确定检查范围

- 如果用户指定了某个组件名（如 "mask"、"button"），则传入 `--name=<组件名>` 仅检查该组件
- 如果用户没有指定，则不传参数，检查所有组件

### Step 2: 运行诊断脚本

使用 Bash 工具运行以下命令，超时设置 600 秒：

- 全量检查：`node scripts/test-error-reporter/index.cjs`
- 指定组件：`node scripts/test-error-reporter/index.cjs --name=<组件名>`

脚本会自动完成：运行测试 → 捕获完整输出（含 stderr） → 去除 ANSI 码 → 解析测试结果和 console 输出 → 输出结构化 JSON。

如果脚本返回 `error` 字段，根据 `type` 处理：
- `config_error` → 按 `hint` 帮用户配置 `source.json`，执行 `node ../../scripts/reload.cjs`，然后重试
- `env_error` → 根据 `error` 信息排查环境问题，解决后重试
- 其他 → 继续往下执行

### Step 3: 解析输出

脚本返回的 JSON 包含以下关键字段：

- `hasErrors` (boolean): 是否有测试失败（exit code !== 0）
- `hasWarnings` (boolean): 是否有 console.error/console.warn 输出
- `summary`: 测试统计（testSuites 和 tests 的 passed/failed/total）
- `failures[]`: 真正失败的测试用例，每个包含：
  - `testFile`: 测试文件路径
  - `component`: 组件名
  - `testName`: 失败的测试用例名
  - `error`: 完整错误信息（含堆栈）
  - `suggestion`: 修复建议
- `warnings[]`: console.error/warn 信息（已去重，附带出现次数），每个包含：
  - `type`: "console.error" 或 "console.warn"
  - `component`: 组件名
  - `message`: 警告消息摘要
  - `detail`: 完整警告内容（含源码片段和堆栈）
  - `sourceLocation`: 源码位置
  - `count`: 出现次数

### Step 4: 展示诊断结果

根据 `hasErrors` 和 `hasWarnings` 分三种情况展示：

**情况 1: 有测试失败 (`hasErrors: true`)**

优先展示 `failures` 列表，以表格形式列出每个失败用例：
- 组件名 | 测试用例名 | 错误摘要 | 修复建议

然后如果有 `warnings`，也列出 console 警告。

**情况 2: 测试全通过但有 console 警告 (`hasWarnings: true`)**

以表格形式列出 `warnings`：
- 组件名 | 类型 | 消息摘要 | 出现次数 | 源码位置

告知用户这些 console 警告虽然不影响测试通过，但代表代码中存在潜在问题。

**情况 3: 全部通过且无警告**

简洁告知用户：所有测试通过，无错误无警告。**流程结束。**

---

### Step 5: 询问是否修复

**仅当 `hasErrors` 或 `hasWarnings` 为 true 时**，进入此步骤。

展示完诊断结果后，立即询问用户是否需要自动修复。根据诊断情况提供选项：

- 如果同时有 failures 和 warnings：
  - "修复全部（失败 + 警告）"
  - "仅修复失败的测试"
  - "仅修复 console 警告"
  - "不修复"
- 如果只有 failures：
  - "修复失败的测试"
  - "不修复"
- 如果只有 warnings：
  - "修复 console 警告"
  - "不修复"

**用户选择"不修复"时，流程结束。**

### Step 6: 执行修复

根据用户选择，逐个修复问题。修复流程如下：

#### 6.1 修复前准备

对于每个待修复的问题：
1. 使用 Read 工具读取报错的测试文件（`$testDir/*.test.js`，目录名从配置的 `testDir` 获取）
2. 根据错误信息中的行号和堆栈定位问题代码
3. 分析错误原因，确定修复方案

#### 6.2 修复策略

**核心原则：优先修改测试文件（`$testDir/*.test.js`），不修改组件源文件。**

只有当问题**明确源于源文件 bug**（如类型错误、逻辑错误导致断言失败）时，才考虑修改源文件，且需先告知用户。

以下是常见问题的修复策略：

| 错误类型 | 修复位置 | 修复方式 |
|---------|---------|---------|
| `act()` 警告 | 测试文件 | 将 state 更新操作包裹在 `act(async () => { ... })` 或使用 `waitFor` |
| 异步超时 (Exceeded timeout) | 测试文件 | 增加 `jest.setTimeout(15000)` 或优化异步等待逻辑 |
| 快照不匹配 | 运行命令 | 终端执行配置中的 `updateSnapshotCommand` 更新快照 |
| jsdom 未实现 API | 测试文件 | 在 `beforeAll`/`beforeEach` 中添加 mock，如 `window.scrollTo = jest.fn()` |
| 断言失败 (expect) | 测试文件 | 分析 expected vs received 的差异，修正测试断言或 mock 数据 |
| 模块找不到 | 测试文件 | 修正 import 路径或添加模块 mock |
| 未包裹 act() 的 state 更新 | 测试文件 | 使用 `await act(async () => { ... })` 包裹触发 state 更新的操作 |
| unmounted component 警告 | 测试文件 | 在 `afterEach` 中 cleanup，或使用 `AbortController` 取消异步操作 |

#### 6.3 修复执行

对每个问题：
1. 使用 Edit 或 MultiEdit 工具修改测试文件
2. 如果修复失败（如无法定位代码、修改逻辑复杂），**跳过此项，继续修复下一个问题**
3. 记录每个修复的结果（成功/跳过/失败）

### Step 7: 验证修复

修复完成后，**重新运行诊断脚本**（与 Step 2 相同的命令）验证修复效果。

对比修复前后的结果：
- 修复前：X 个失败，Y 个警告
- 修复后：X' 个失败，Y' 个警告
- 修复成功率

### Step 8: 输出修复报告

以清晰的格式展示修复结果：

```
修复报告
────────────────────────────
修复前: X 个测试失败, Y 个警告
修复后: X' 个测试失败, Y' 个警告

成功修复:
  [组件名] 测试用例名 - 修复方式描述

未能修复（需手动处理）:
  [组件名] 测试用例名 - 原因 + 手动修复建议
────────────────────────────
```

**如果仍有未修复的问题**，给出每个问题的手动修复建议，包括需要修改的文件、行号、具体改动方向。
