# Capability Map

## Supported Tools

当前 PixCake skill 只使用以下正式工具：

- 项目：`get_project_list` / `create_projects` / `import_images_to_projects`
- 图片：`get_project_images`
- 修图：`get_preset_suit_list` / `apply_preset_suit`
- 导出：`batch_export_images` / `get_task_status`

本地路径定位、文件夹判断和文件筛选，优先使用 agent 自身的 shell / command 能力。

## Supported Workflows

- 创建新项目
- 查看最近项目或按条件筛选项目
- 向项目导入图片
- 查看一个或多个项目的图片
- 获取预设列表并匹配预设
- 对指定图片应用预设
- 提交导出任务
- 查询导出任务状态和进度

## Out Of Scope

当前不要介绍、不要暗示、不要尝试以下产品域：

- 联机拍摄
- AI 挑图
- AI 修图
- AI 追色
- 滤镜 / 换背景 / 去路人
- 智能裁剪

## Tool Selection

- 需要找项目或让用户选项目时，用 `get_project_list`
- 需要新建项目时，用 `create_projects`
- 需要导入图片或目录时，用 `import_images_to_projects`
- 需要读取项目图片时，用 `get_project_images`
- 需要处理修图诉求时，先用 `get_preset_suit_list`
- 只有选定预设后，才用 `apply_preset_suit`
- 导出统一用 `batch_export_images`
- 需要查询导出是否完成、当前进度或任务状态时，用 `get_task_status`

## Boundary Response

如果用户请求超出当前能力面：

- 直接说明当前 PixCake skill 未暴露该能力
- 如果请求里同时包含受支持动作，只继续处理受支持部分
- 不假设客户端里存在隐藏工具
