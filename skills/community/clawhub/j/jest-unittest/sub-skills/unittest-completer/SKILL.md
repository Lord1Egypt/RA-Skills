---
name: unittest-completer
description: >
  自动补充组件单测至100%覆盖率。当用户提到补充测试、补全单测、写单测、覆盖率100%、让覆盖率达标、
  自动写测试、提升覆盖率时触发。输入组件名后自动运行检测、分析未覆盖代码、编写补充用例，循环迭代直到
  Statements/Branches/Functions/Lines 四项全部100%。
allowed-tools: Read, Edit, MultiEdit, Write, Bash, Glob, Grep, TaskCreate, TaskUpdate, TaskList
---

# 组件测试覆盖率完善工具

你是一个专业的前端测试工程师。你的任务是将指定组件的单测覆盖率提升到 100%。

## 前置：读取配置

脚本会自动校验配置和环境。如果返回 `error` 字段，根据 `type` 处理：`config_error` 按 `hint` 配置 `source.json`（路径见 `sourceJsonPath`）后执行 `node ../../scripts/reload.cjs` 重试；`env_error` 根据 `error` 排查环境后重试。

从配置中获取以下变量，后续步骤中使用：
- `componentDir` + 组件名 → 拼接得到 `$PATH`（如 `src/views/_components/button`）
- `testDir` → 测试目录名 `$testDir`（如 `__tests__`）
- `updateSnapshotCommand` → 更新快照的命令

获取方式：运行 `node ../../scripts/reload.cjs`，从其输出的 JSON 中读取上述字段。如果配置已存在（脚本运行不报错），则直接使用。

## 参数

组件名称：**$ARGUMENTS**

## 执行流程

严格按照以下流程执行，不要跳过任何步骤。

### Step 1: 验证组件

!`ls -la $PATH/ 2>&1`

1. 检查以上输出，确认组件目录存在
2. 如果目录不存在（输出包含 "No such file" 等错误），告诉用户组件名称无效并停止

### Step 2: 判断测试现状

!`ls -la $PATH/$testDir/ 2>&1`

检查以上输出，判断是否已有测试文件：

- **如果测试目录下没有 `.test.js` 文件**（目录不存在、为空、或仅包含 `__snapshots__/` 子目录），说明该组件尚无单测，直接跳到 Step 4 从零编写测试。
- **如果测试目录下已有测试文件**，使用 Bash 工具运行覆盖率检测命令：
  ```
  node scripts/check-coverage-100/index.cjs $ARGUMENTS 2>&1
  ```
  解析返回的 JSON，根据 `status` 字段判断状态：
  - **`success`**：覆盖率已达 100%，跳到 Step 6
  - **`test_error`**：测试运行报错，进入 Step 3
  - **`not_covered`**：覆盖率未达 100%，进入 Step 4

**重要约束：** 脚本执行失败时应排查报错原因，不要绕过脚本自行拼接命令。

### Step 3: 修复测试错误

当 `status === "test_error"` 时：

1. 读取 `error` 字段，分析报错原因
2. 读取对应的测试文件（`$PATH/$testDir/` 下的文件）
3. 读取组件源代码（`$PATH/` 下的 tsx、ts 文件）
4. 如果报错是快照不匹配（snapshot mismatch），运行配置中的 `updateSnapshotCommand` 更新快照
5. 回到 Step 5 重新检测

### Step 4: 分析未覆盖代码并编写补充测试

本步骤有两种进入方式，操作流程不同：

**A) 从 Step 2 跳转而来（尚无测试文件）：**

此时没有 `uncoveredDetails` 数据可用，需要从零编写测试：

1. 读取组件所有源代码（`$PATH/` 下的 tsx、ts 文件）
2. 读取组件类型定义文件（如 `types.ts`），了解所有 props
3. 在 `$PATH/$testDir/` 目录下创建测试文件，命名为 `$ARGUMENTS.test.js`
4. 编写覆盖组件全部代码路径的测试用例
5. 进入 Step 5 运行覆盖率检测

**B) 由覆盖率检测返回 `status === "not_covered"` 进入：**

此时已有测试文件和 `uncoveredDetails` 数据：

1. 解析 `uncoveredDetails` 数组，获取每个文件的 `uncoveredStatements`、`uncoveredBranches`、`uncoveredFunctions`
2. 读取未覆盖文件的源代码，利用每项的 `location` 字段（格式 `起始行:列 - 结束行:列`）精确定位到未覆盖的代码
3. 结合 `type`、`branchIndex` 和源代码上下文，分析每处未覆盖需要什么测试条件才能触发
4. 读取现有测试文件，理解风格和结构
5. 读取组件类型定义文件（如 `types.ts`），了解所有 props
6. 在现有测试文件中补充测试用例

#### 测试编写规则

- 使用与现有测试一致的导入和风格
- 测试框架：Jest + React Testing Library + react-test-renderer
- 标准导入：
  ```javascript
  import React from 'react';
  import '@testing-library/jest-dom';
  import { render, fireEvent, screen } from '@testing-library/react';
  import renderer from 'react-test-renderer';
  ```

#### 覆盖策略
**未覆盖函数 (functions)**：
- 传入对应的回调 props（如 `onClick`、`onChange`）并触发事件
- 对于内部函数，构造触发该函数执行的条件

**未覆盖语句 (statements)**：
- 根据语句所在的上下文，构造合适的 props 或事件使代码执行到该语句

**未覆盖分支 (branches)**：

`uncoveredBranches` 的 `type` 是 Istanbul 分支类型，不一定和源码语法直接对应，需结合源码判断。常见映射：

| `type` | 可能对应的源码语法 | 覆盖要点 |
|---|---|---|
| `if` | `if` 语句 | `branchIndex=0` → true，`1` → false/else |
| `binary-expr` | `\|\|`、`&&` | `branchIndex=0` 短路，`1` 非短路 |
| `cond-expr` | 三元 `? :`、`?.`、`?.()`、解构默认值 `= {}` | Istanbul 把这些都报为 `cond-expr`。`?.`/`?.()` 需构造左侧为 `null`/`undefined` 覆盖短路分支；解构默认值需属性缺失或为 `undefined` 触发（`null` 不触发）；`useRef` 场景需构造 `ref.current` 为 `null` |
| `nullish-coalescing` | `??` | `''`/`0`/`false` 不触发右侧（与 `\|\|` 不同） |
| `default-arg` | 函数参数默认值 | 只有 `undefined` 触发，`null` 不触发 |

#### 注意事项
- 如果组件使用了 `window`、`document` 等浏览器 API，用 `jest.spyOn` 或 `Object.defineProperty` 模拟
- 如果组件有异步操作，使用 `act()` 和 `waitFor()` 等待
- 不要删除或修改现有的快照测试
- 新增的测试用例名称要有描述性，说明覆盖的场景


### Step 5: 重新运行覆盖率检测

使用 Bash 工具运行命令 `node scripts/check-coverage-100/index.cjs $ARGUMENTS`，超时设置 120 秒。

解析返回的 JSON：
- **`success`**：覆盖率已达 100%，进入 Step 6
- **`test_error`**：回到 Step 3 修复错误
- **`not_covered`**：回到 Step 4 继续分析并补充测试

### Step 6: 完成

当覆盖率检测返回 `status === "success"` 时：

向用户报告结果：
- 组件名称
- 覆盖率状态：全部 100%
- 修改的测试文件路径

## 循环控制

- 最多执行 **10 轮**循环（Step 5 → Step 3/4）
- 如果 10 轮后仍未达到 100%，向用户报告当前状态和剩余未覆盖的代码，请用户手动处理
- 每轮循环都要向用户简要汇报进度（当前第几轮、修复了什么、还剩什么）
