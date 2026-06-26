# Jianying Auto Editor

`jianying-auto-editor` 用于把本地素材目录和云端剪辑决策串起来，生成一份面向剪映草稿工作流的本地输出包。第一版聚焦“素材扫描 -> 云端任务 -> 草稿 JSON 产物 -> 执行结果回传”，不做复杂 GUI 自动化。

## 安装要求

- Node.js >= 18
- 能访问你的云端剪辑 API
- 本地具备可写输出目录

## 环境依赖

- Windows / macOS / Linux 均可运行 Node 主入口
- 若需要把结果进一步导入剪映，请自行确认草稿目录和目标剪映版本匹配

## API Key 配置方法

1. 复制 `examples/config.example.json` 为你自己的配置文件。
2. 将 `api_key` 替换成实际密钥。
3. 将 `api_base_url` 指向你的服务地址，例如 `https://api.example.com`。

## 调用方式

```bash
node scripts/index.js --config ./examples/config.example.json
```

也可以通过包入口调用：

```bash
npx jianying-auto-editor --config ./examples/config.example.json
```

## 运行过程

脚本会依次完成：

1. 读取并校验配置
2. 扫描 `material_path`
3. 调用 `/v1/tasks/create`
4. 调用 `/v1/tasks/{id}/material-index`
5. 调用 `/v1/tasks/{id}/plan`
6. 生成本地草稿数据
7. 调用 `/v1/tasks/{id}/execute-report`

## 输出内容

输出目录默认由 `jianying_draft_path` 决定；`export_mode=task-subdir` 时会为每个任务单独建子目录。

- `draft-meta.json`
- `draft-content.json`
- `execution-report.json`

## 配置说明

公共配置：

- `api_base_url`
- `api_key`
- `project_type`
- `aspect_ratio`
- `material_path`
- `template_id`
- `subtitle_mode`
- `music_policy`
- `pace_policy`
- `output_mode`

剪映专属配置：

- `jianying_draft_path`
- `draft_version`
- `export_mode`

可选增强配置：

- `task_name`
- `task_timeout_ms`
- `poll_interval_ms`
- `request_timeout_ms`
- `webhook_url`
- `extra_metadata`

## 常见问题

### 1. 云端没有返回分镜片段怎么办？

脚本会回退成按素材顺序生成的保底草稿结构，保证流程可继续联调。

### 2. 可以直接控制剪映桌面界面吗？

第一版不包含 GUI 点击、桌面 RPA 或版本特定的窗口自动化。

### 3. 输出一定能被所有剪映版本直接导入吗？

不能。当前实现更偏向“标准化草稿数据输出骨架”，具体兼容性仍需按你的目标版本验证。

## 限制说明

- 不提取真实媒体时长，默认用云端返回片段或保底片段长度占位。
- 不处理复杂转场、特效、调色、贴纸和高级字幕样式。
- 需要云端 API 按约定返回任务 ID 和计划数据。
