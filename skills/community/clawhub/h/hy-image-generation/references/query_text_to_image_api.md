# 混元生图 查询任务 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1668/124633

## 接口信息

- **接口域名**：aiart.tencentcloudapi.com
- **Action**：QueryTextToImageJob
- **Version**：2022-12-29
- **HTTP 请求方法**：POST
- **功能说明**：查询混元生图（异步）任务。根据 SubmitTextToImageJob 返回的 JobId 查询生图任务状态和结果。

## 输入参数

| 参数名称 | 必选 | 类型 | 描述 |
|----------|------|------|------|
| JobId | 是 | String | 任务 ID。由 SubmitTextToImageJob 接口返回。 |

## 输出参数

| 参数名称 | 类型 | 描述 |
|----------|------|------|
| JobStatusCode | String | 任务状态码。1: 排队中、2: 运行中、4: 生成失败、5: 生成完成。 |
| JobStatusMsg | String | 任务状态信息。 |
| JobErrorCode | String | 任务错误码。 |
| JobErrorMsg | String | 任务错误信息。 |
| ResultImage | String | 生成图 URL。图片有效期为 1 小时，请及时保存。 |
| ResultDetails | Array of String | 生成图 URL 列表。当生成多图时返回多个 URL。 |
| RevisedPrompt | String | 修正后的 Prompt（如果开启了 Revise）。 |
| RequestId | String | 唯一请求 ID。 |

## 任务状态码说明

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 1 | 排队中 | 任务排队等待中 |
| 2 | 运行中 | 任务正在生成图像 |
| 4 | 生成失败 | 任务执行失败，查看 JobErrorCode 和 JobErrorMsg |
| 5 | 生成完成 | 图像生成成功，结果在 ResultImage / ResultDetails 中 |

## 轮询建议

- 首次查询建议在提交任务后 **5~10 秒** 开始
- 轮询间隔建议 **3~5 秒**
- 普通生图一般 **10~30 秒** 完成
- 开启 Prompt 改写（Revise=1）会额外增加约 **20 秒**
- 建议设置最大轮询时间为 **5 分钟**

## 错误码

| 错误码 | 描述 |
|--------|------|
| FailedOperation.JobNotFound | 任务不存在 |
| FailedOperation.InnerError | 内部错误 |
| InvalidParameterValue.ParameterValueError | 参数取值错误 |
| ResourceUnavailable.NotExist | 资源不存在 |
| ResourceUnavailable.InArrears | 欠费停服 |
