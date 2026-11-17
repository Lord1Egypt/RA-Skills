# Agent JSON 协议与错误处理

## 信封

成功：

```json
{
  "schema_version": "1",
  "ok": true,
  "operation": "asr",
  "result": {},
  "meta": {"modelcli_version": "0.3.0", "elapsed_ms": 123}
}
```

失败：

```json
{
  "schema_version": "1",
  "ok": false,
  "operation": "ocr",
  "error": {
    "code": "INVALID_IMAGE",
    "message": "Input is not a readable image",
    "retryable": false
  },
  "meta": {"modelcli_version": "0.3.0", "elapsed_ms": 4}
}
```

stdout 只包含一个换行结尾的 JSON 文档。进度、安装日志和 traceback 只在 stderr。即使退出码非零，也优先解析 stdout 的错误信封。

## 退出码

| 退出码 | 含义 |
| ---: | --- |
| `0` | 成功 |
| `2` | 参数或用法错误 |
| `3` | 输入无效 |
| `4` | 模型缺失、安装、下载或校验失败 |
| `5` | 推理、内部或包装器协议错误 |
| `6` | 输出冲突或写入失败 |
| `124` | 包装器墙钟超时 |
| `130` | SIGINT / Ctrl-C |

## 稳定错误处理

- `MODEL_NOT_INSTALLED`：包装器已允许隐式下载；若仍出现，报告模型安装失败上下文。
- `MODEL_BUSY`：`retryable: true`，等待短暂间隔后最多重试一次。
- `MODEL_DOWNLOAD_FAILED`、网络类模型错误：仅在 `retryable: true` 时最多重试一次。
- `OUTPUT_EXISTS`：不要自动加入 `--force`；询问用户。
- `INVALID_IMAGE`、`INVALID_AUDIO`、`INVALID_PROMPT_AUDIO`：要求用户提供可读输入。
- `INVALID_CLASS`：改用 COCO 英文标准类别名。
- `OUTPUT_REQUIRED`：为 TTS 生成合理的绝对 `.wav` 输出路径。
- `CONFIRMATION_REQUIRED`：说明敏感操作，得到确认后传包装器 `--approve-sensitive`。
- `TIMEOUT`：报告超时；只有用户要求时才用更大的 `--timeout` 重试。
- `PROTOCOL_ERROR`：报告 CLI 输出不符合 schema，不要猜测业务结果。
- `MODELCLI_INSTALL_FAILED`：显示 stderr 中的安装诊断和手动安装命令。

包装器生成的错误也使用 schema v1，并在 `meta.wrapper` 中标记 `modelcli-skill`。
