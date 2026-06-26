---
name: unittest-checker
description: >
  检测组件单测覆盖率是否达标。当用户提到查看单测覆盖率、检查覆盖率、覆盖率报告、哪些组件未达标、覆盖率统计、Statements/Branches/Functions/Lines 覆盖率时触发。支持全量检查或指定组件名查询。
allowed-tools: Read, Bash, Glob
---

# 检测组件覆盖率

你的任务是运行组件单测，分析覆盖率报告，输出未达到 100% 覆盖率的组件列表。

## 前置：确保配置存在

脚本依赖配置文件。如果是首次使用，先运行 `node ../../scripts/reload.cjs` 生成配置。如果返回 `error`，按 `hint` 帮用户配置 `source.json`（路径见 `sourceJsonPath`）后重试。

## 执行流程

### Step 1: 确定检查范围

- 如果用户指定了某个组件名（如 "button"、"avatar"），则传入 `--name=<组件名>` 仅检查该组件
- 如果用户没有指定，则不传参数，检查所有组件

### Step 2: 运行分析脚本

使用 Bash 工具运行以下命令，超时设置 600 秒：

- 全量检查：`node scripts/analyze-coverage/index.cjs`
- 指定组件：`node scripts/analyze-coverage/index.cjs --name=<组件名>`

脚本会自动完成：清理旧报告 → 运行测试 → 解析覆盖率数据 → 输出结果 JSON。

如果脚本返回 `error` 字段，根据 `type` 处理：
- `config_error` → 按 `hint` 帮用户配置 `source.json`，执行 `node ../../scripts/reload.cjs`，然后重试
- `env_error` → 根据 `error` 信息排查环境问题，解决后重试
- `test_error` → 告知用户错误信息并停止

**重要约束：** 脚本执行失败时应排查报错原因，不要绕过脚本自行拼接命令。

### Step 3: 输出结果

将脚本的 JSON 输出直接展示给用户，格式清晰地列出：

1. 总组件数、已达 100% 的组件数及组件名、未达 100% 的组件数
2. 每个未达 100% 的组件名称及其四项覆盖率数值（Statements / Branches / Functions / Lines）

以表格形式展示未达标组件，方便用户快速查看。
