---
name: qax-hunter-use
description: 用于调用奇安信 Hunter OpenAPI 进行资产批量导出。用户提到 Hunter、资产测绘、批量导出、task_id 下载文件等需求时优先加载本 skill。
---

# QAX Hunter Use

## First

- 默认走 API 模式，不使用文件上传。
- 查询语法由用户输入，脚本自动做 RFC 4648 base64url 编码。
- 批量任务流程固定为：
  1) 创建任务 `/openApi/search/batch`
  2) 查询进度 `/openApi/search/batch/{task_id}`
  3) 下载结果 `/openApi/search/download/{task_id}`

## 入口脚本

- 主脚本：`scripts/hunter_batch_cli.py`
- 运行方式：
  - AI 无交互推荐：
    - `python3 scripts/hunter_batch_cli.py --no-interactive --api-key "$HUNTER_API_KEY" --search 'web.title="test"' --check-delay 10 --json-output`
  - 兼容交互：
    - `python3 scripts/hunter_batch_cli.py`

## 参数说明

- 必填：`api-key`
- 常用可选：`search`、`start_time`、`end_time`、`is_web`、`status_code`、`fields`、`assets_limit`
- AI 友好参数：
  - `--no-interactive`：禁止交互输入，缺参即报错
  - `--check-delay`：创建任务后等待 N 秒（默认 10）再首次尝试下载
  - `--poll-interval` / `--poll-timeout`：轮询控制
  - `--output-file`：指定下载文件名
  - `--json-output`：最后输出一行 JSON 结果，便于机器解析

## 安全注意事项

- 不要将真实 `api-key` 写入仓库文件。
- 推荐使用环境变量注入：`HUNTER_API_KEY`。
- 若必须持久化，请使用系统密钥环或加密配置文件，不要明文存储。
