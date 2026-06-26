# 工具与脚本设计

本文件描述 `organize-folders` 在执行过程中可能使用的脚本和命令能力。默认先设计能力边界，不要求一次性全部实现。

## 设计原则

```text
扫描脚本只读
分析脚本只判断
计划脚本只生成方案
校验脚本负责拦截风险
执行脚本默认 dry-run
日志记录所有改动
删除永远只进候选清单
```

## 推荐脚本结构

```text
scripts/
├─scan_folder.py
├─classify_files.py
├─generate_plan.py
├─validate_plan.py
├─execute_plan.py
├─find_duplicates.py
├─generate_directory_guide.py
└─export_report.py
```

## 1. 扫描类

### `scan_folder.py`

状态：已实现。

用途：

- 扫描目录结构
- 统计顶层目录体量
- 统计文件数量
- 统计主要文件类型
- 查找最大文件
- 查找最近文件
- 查找最近 N 天新文件
- 输出扫描错误

要求：

- 只读
- 不打开文件内容
- 不移动、不删除、不重命名

后续可拆分或扩展：

- `scan_new_files.py`：专门扫描收件箱和下载目录的新文件。
- `scan_empty_dirs.py`：查找空目录。
- `scan_large_files.py`：查找大文件。
- `scan_stale_projects.py`：查找长期未活跃项目。

## 2. 分析类

### `classify_files.py`

状态：已实现。

用途：

根据文件名、路径、扩展名、修改时间和所在目录生成分类判断。

输出字段：

- 路径
- 识别类型
- IRK 类型：Information / Resource / Knowledge
- PARA 类型：Projects / Areas / Resources / Archives
- 生命周期：inbox / active / completed / archive / backup / delete-candidate
- 建议目录
- 原因
- 置信度
- 是否需要人工确认

要求：

- 不移动文件
- 不删除文件
- 不把低置信度判断当成可执行动作

## 3. 计划类

### `generate_plan.py`

状态：已实现。

用途：

根据扫描结果、分类结果和整理规则生成整理计划。

输出文件：

```text
organize-plan.json
organize-plan.md
move-plan.csv
```

计划项字段：

- action
- source
- target
- reason
- risk
- confidence
- requires_confirmation

支持动作：

- create_dir
- create_sandbox
- move
- rename
- copy
- archive
- backup
- skip
- manual-review
- delete-candidate

要求：

- 删除只能生成 `delete-candidate`
- 不生成覆盖型操作
- 不生成系统目录移动操作

## 4. 校验类

### `validate_plan.py`

状态：已实现。

用途：

执行前检查整理计划是否安全。

检查项：

- 目标路径是否已存在
- 是否会覆盖文件
- 是否跨盘移动
- 是否包含系统目录
- 是否包含高风险目录
- 是否有重复目标路径
- 是否有删除动作
- 是否包含无法解析的路径

要求：

- 执行计划前必须先校验
- 校验失败时不得执行
- 高风险项必须进入人工确认清单

## 5. 执行类

### `execute_plan.py`

状态：已实现。

用途：

执行用户确认过的整理计划。

默认模式：

```text
--dry-run
```

真正执行必须显式使用：

```text
--apply
```

支持动作：

- create_dir
- create_sandbox
- move
- rename
- copy
- archive
- backup
- skip

禁止默认支持：

- delete
- overwrite
- clear

要求：

- 默认 dry-run
- 不覆盖文件
- 遇到冲突停止
- 每项操作都写日志
- 高风险动作必须显式确认
- 首次整理优先建议沙盒整理模式，但必须由用户确认

## 6. 日志类

日志可以由 `execute_plan.py` 内置，也可以独立为 `write_log.py`。

状态：已在 `execute_plan.py` 中实现。

推荐日志文件：

```text
organize-log_YYYY-MM-DD_HHMM.md
organize-log_YYYY-MM-DD_HHMM.csv
```

日志字段：

| 时间 | 操作 | 原路径 | 目标路径 | 结果 | 备注 |
|---|---|---|---|---|---|

必须记录：

- 成功
- 失败
- 跳过
- 错误信息
- 用户确认状态
- 是否为沙盒整理

## 7. 回滚类

### `generate_rollback.py`

状态：已实现。

用途：

根据执行日志生成回滚计划。

输出文件：

```text
rollback-plan.md
rollback-plan.json
```

要求：

- 只生成回滚计划
- 不自动回滚
- 标记无法安全回滚的操作
- 对覆盖、合并、复制等情况给出人工确认提示

## 8. 去重类

### `find_duplicates.py`

状态：已实现。

用途：

查找疑似重复文件。

模式：

- 快速模式：文件名 + 大小
- 精确模式：文件哈希

输出文件：

```text
duplicate-candidates.md
```

要求：

- 只生成候选清单
- 默认不删除
- 精确删除也必须由用户逐项确认

## 9. 新目录说明表

### `generate_directory_guide.py`

状态：已实现。

用途：

整理完成后生成新目录说明表。

输出文件：

```text
directory-guide.md
```

字段：

| 目录 | 中文名称 | 用途 | 放什么 | 不放什么 | 维护周期 |
|---|---|---|---|---|---|

要求：

- 整理完成后必须输出
- 如果未执行整理，也可作为规则文档的一部分输出

## 10. 报告导出

### `export_report.py`

状态：已实现。

用途：

整合扫描结果、规则、整理计划、执行日志和目录说明表。

输出文件：

```text
folder-organization-report.md
```

建议章节：

1. 概览
2. 扫描结果
3. 主要问题
4. 采用模型
5. 新目录结构
6. 整理计划
7. 执行日志
8. 新目录说明表
9. 待确认事项
10. 维护建议

## PowerShell 命令边界

允许用于只读扫描和检查：

```powershell
Get-ChildItem
Measure-Object
Sort-Object
Select-Object
Get-Item
Test-Path
Get-FileHash
```

允许在用户确认后使用：

```powershell
New-Item
Move-Item
Rename-Item
Copy-Item
```

高风险或默认禁止：

```powershell
Remove-Item
Clear-Content
Move-Item 批量移动
Rename-Item 批量重命名
覆盖已有文件的复制或移动
```

## 执行前检查清单

执行前必须确认：

1. 是否已有整理计划。
2. 是否已 dry-run。
3. 是否已通过计划校验。
4. 是否会覆盖文件。
5. 是否包含删除动作。
6. 是否包含系统目录。
7. 是否包含高风险个人资料。
8. 是否准备好日志文件。
9. 首次整理时是否询问过用户要不要使用沙盒整理模式。
