# 错误处理规范

## 可重试错误

`error.retryable=true` 时可以提示用户网络或服务暂时异常。

- 查询目录、模板等 GET 请求由脚本自动有限重试。
- 咨询题答案、计算题答案、合同审核和文书生成不自动重复提交。
- 合同审核结果不确定时，使用错误详情中的任务编号调用一次 `resume`。

## 用户输入错误

- `OPTION_NOT_FOUND`：重新展示有效选项。
- `NO_MATCHING_ANSWERS`：按当前 `interaction.fields[].key` 重新组装答案。
- `FILE_TOO_LARGE`、`UNSUPPORTED_FILE_TYPE`：说明文件限制并请用户重新提供。
- `UNSUPPORTED_CASE_MATERIAL_TYPE`、`TOO_MANY_CASE_MATERIALS`：说明案件材料支持格式或数量限制。
- `stage=needs_material_extraction`：先用宿主真实可用的 PDF、文档、表格或图像工具提取 `data.unresolvedFiles`，将文字放入 `extractedTexts` 后重试；不得忽略附件直接继续。
- `PLEADING_MATERIAL_REQUIRED`：请用户描述案情或上传图片。
- `QUESTION_NOT_FINISHED`：继续当前题目，不提前生成报告。

## 服务限制错误

登录、验证码、付费、下载限制或服务端配置错误都应原样说明。不要尝试绕过校验，也不要自行生成一个看似成功的结果。

## 会话错误

- `SESSION_NOT_FOUND`：任务不存在或已经清理，重新开始。
- `SESSION_CORRUPTED`：状态文件损坏，重新开始。
- `SESSION_CAPABILITY_MISMATCH`：不要把一个能力的任务编号用于另一个能力。
