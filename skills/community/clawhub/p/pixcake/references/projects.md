# Projects

## Overview

该 reference 负责建立 PixCake 的项目上下文，覆盖：

- 创建项目
- 查找项目
- 导入图片
- 读取项目图片

## Tools

- `get_project_list`
- `create_projects`
- `import_images_to_projects`
- `get_project_images`

## Working Rules

- 如果后续还要修图或导出，先把项目上下文收口清楚
- 路径必须真实，不猜测桌面、下载目录或相对文件夹名
- 用户说“这些图片”但没给路径时，先用 shell / command 定位，再执行
- 用户说“某个项目”但匹配不唯一时，先给候选或追问一句

## Common Flows

### 创建项目并导入图片

> `create_projects` 支持在创建时通过 `image_paths` 一步导入图片。
> 如果创建和导入需要分步处理（如图片来源不同），再单独调用 `import_images_to_projects`。

1. 确认图片来源
2. 路径不明确时先定位真实目录
3. 调用 `create_projects`（可通过 `image_paths` 同时导入图片）
4. 如需分步导入，再调用 `import_images_to_projects`

### 导入到已有项目

1. 先用 `get_project_list` 确认目标项目
2. 如果结果不唯一，让用户选择
3. 再调用 `import_images_to_projects`

### 读取项目图片

1. 先确认目标项目或项目列表
2. 调用 `get_project_images`
3. 默认先返回当前任务需要的范围，不盲目全量展开

## Clarifications

- “打开昨天那个项目”但没有唯一结果时，不要猜
- “导入这些图”但缺少路径、附件或目录时，先追问图片来源
- “桌面那个文件夹”如果无法唯一定位，先追问具体目录名或路径

## Guardrails

- 不假设存在未声明的项目工具
- 不把图片 ID 当作导入路径
- 不在没有项目上下文时直接进入依赖项目的修图或导出步骤
