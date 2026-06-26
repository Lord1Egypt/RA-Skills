# check-coverage-100 使用文档

## 概述

检测指定组件的单测覆盖率是否达到 100%（Stmts / Branch / Funcs / Lines 四项）。

## 用法

```bash
node scripts/check-coverage-100/index.cjs <组件名>
```

## 返回值

通过 stdout 输出 JSON 对象，exit code 0 表示通过，1 表示失败。

根据 `status` 字段判断当前状态，再读取对应字段获取信息：

| status | success | 含义 | 需要关注的字段 |
|---|---|---|---|
| `success` | `true` | 单测通过且覆盖率 100% | 无 |
| `test_error` | `false` | 单测运行报错 | `error` |
| `not_covered` | `false` | 单测通过但覆盖率未达 100% | `uncoveredDetails` |

## 各状态输出结构

### success — 全部通过

```json
{
  "success": true,
  "status": "success"
}
```

无需额外处理。

### test_error — 单测运行报错

```json
{
  "success": false,
  "status": "test_error",
  "error": "<stderr 报错信息>"
}
```

`error` 字段包含 Jest 的完整错误输出（编译错误、断言失败、运行时异常等），可直接用于定位问题。

### not_covered — 覆盖率未达 100%

```json
{
  "success": false,
  "status": "not_covered",
  "uncoveredDetails": [
    {
      "file": "src/views/_components/button/index.tsx",
      "uncoveredLines": "14-17, 46-47",
      "uncoveredStatements": [
        { "line": 14, "location": "14:15 - 14:23" }
      ],
      "uncoveredBranches": [
        { "line": 14, "type": "cond-expr", "branchIndex": 1, "location": "14:23 - 14:null" }
      ],
      "uncoveredFunctions": [
        { "name": "(anonymous_10)", "line": 45, "location": "45:28 - 48:3" }
      ]
    }
  ]
}
```

`uncoveredDetails` 是数组，每个元素对应一个未完全覆盖的源文件，包含：

| 字段 | 说明 |
|---|---|
| `file` | 文件相对路径 |
| `uncoveredLines` | 未覆盖行号范围汇总，如 `"1-3, 5, 7-8"` |
| `uncoveredStatements` | 未覆盖的语句列表 |
| `uncoveredBranches` | 未覆盖的分支列表 |
| `uncoveredFunctions` | 未覆盖的函数列表 |

#### uncoveredStatements 单项

| 字段 | 说明 |
|---|---|
| `line` | 语句所在行号 |
| `location` | 精确位置 `起始行:列 - 结束行:列` |

#### uncoveredBranches 单项

| 字段 | 说明 |
|---|---|
| `line` | 分支所在行号 |
| `type` | 分支类型（`cond-expr` 三元表达式 / `if` 条件语句 / `binary-expr` 二元表达式等） |
| `branchIndex` | 分支索引（0 = 第一个分支，1 = 第二个分支） |
| `location` | 精确位置 `起始行:列 - 结束行:列` |

#### uncoveredFunctions 单项

| 字段 | 说明 |
|---|---|
| `name` | 函数名（匿名函数显示为 `(anonymous)` 或 `(anonymous_N)`） |
| `line` | 函数声明所在行号 |
| `location` | 函数体位置 `起始行:列 - 结束行:列` |
