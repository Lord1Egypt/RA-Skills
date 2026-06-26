---
name: jianying-auto-editor
description: Automate Jianying draft generation from local media plus a cloud editing API. Use when Codex needs to scan a material folder, request editing decisions, and write Jianying-oriented draft output for short-form video workflows.
metadata: {"openclaw":{"emoji":"🎬","homepage":"https://github.com/imfengziaaa/video-auto-editor-skills","requires":{"bins":["node"]},"skillKey":"jianying-auto-editor"}}
---

# Jianying Auto Editor

使用这个 skill 时，按下面顺序执行：

1. 读取 `examples/config.example.json` 同结构的配置文件。
2. 校验 `api_base_url`、`api_key`、`material_path`、`template_id`、`jianying_draft_path` 等关键参数。
3. 递归扫描素材目录，只收集常见视频、音频、图片素材。
4. 调用云端 API 创建任务、上报素材索引、获取剪辑计划。
5. 在本地生成剪映草稿输出，不要承诺 GUI 点击或桌面 RPA。
6. 将执行结果写入输出目录，并向云端回传执行报告。

## 输入参数

至少提供这些字段：

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
- `jianying_draft_path`
- `draft_version`
- `export_mode`

可选字段：

- `task_timeout_ms`
- `poll_interval_ms`
- `request_timeout_ms`
- `task_name`
- `webhook_url`
- `extra_metadata`

## 输出结果

默认输出到 `jianying_draft_path` 指向的目录，包含：

- `draft-meta.json`：任务与导出元信息
- `draft-content.json`：草稿时间线和片段描述
- `execution-report.json`：本地执行报告

## 推荐工作流

- 先用示例配置复制出一份真实配置。
- 保持 `material_path` 只放本次任务素材，避免无关文件进入索引。
- 先验证云端 `/v1/tasks/create` 和 `/v1/tasks/{id}/plan` 可用，再跑正式任务。
- 若云端未返回细粒度分镜，允许回退到“按素材顺序串接”的保底草稿。

## 依赖要求

- Node.js 18 或更高版本
- 可访问云端 API 的网络环境
- 本地可写的剪映草稿输出目录

## 错误处理原则

- 缺少配置、素材目录不存在、API 调用失败时立即停止并返回非 0 退出码。
- 本地始终尽量写出 `execution-report.json`，便于排查。
- 对云端返回的未知字段保持容忍，只消费已知字段。
- 明确提示第一版不覆盖复杂 GUI 自动化和全部剪映版本兼容性。
