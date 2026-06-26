# 混元生图 提交任务 API 文档

> 原始文档链接：https://cloud.tencent.com/document/product/1668/124632

## 接口信息

- **接口域名**：aiart.tencentcloudapi.com
- **Action**：SubmitTextToImageJob
- **Version**：2022-12-29
- **HTTP 请求方法**：POST
- **功能说明**：混元生图（异步）接口基于混元大模型，将根据输入的文本描述快速生成 AI 图像。支持垫图引导、分辨率控制、prompt 改写等。异步接口返回任务 ID，需通过 QueryTextToImageJob 查询结果。

## 输入参数

| 参数名称       | 必选  | 类型              | 描述                                                                                                   |
| ---------- | --- | --------------- | ---------------------------------------------------------------------------------------------------- |
| Prompt     | 是   | String          | 文本描述。算法将根据输入的文本智能生成与之相关的图像。建议详细描述画面主体、细节、场景等，文本描述越丰富，生成效果越精美。不能为空，推荐使用中文。最多可传 8192 个 utf-8 字符。       |
| Images     | 否   | Array of String | 垫图 URL 列表。用于引导生成方向，base64 后大小不超过 10MB。支持 jpg、jpeg、png、webp 格式，最多 3 张图。示例值：`["https://xxx.jpeg"]`     |
| Resolution | 否   | String          | 生成图分辨率，默认 `1024:1024`。格式为 `宽:高`，宽高维度均在 [512, 2048] 像素范围内，宽高乘积（即图像面积）不超过 1024×1024 像素。示例值：`1024:1024` |
| Seed       | 否   | Integer         | 随机种子，默认随机。不传：随机种子生成。正数：固定种子生成。                                                                       |
| Revise     | 否   | Integer         | 是否开启 prompt 改写。为空时默认开启，改写预计会增加 20s 左右耗时。0：关闭改写。1：开启改写。建议默认开启，如果关闭改写，需要调用方自己接改写，否则对生图效果有较大影响。         |

## 输出参数

| 参数名称      | 类型     | 描述                       |
| --------- | ------ | ------------------------ |
| JobId     | String | 任务 ID。                   |
| RequestId | String | 唯一请求 ID，由服务端生成，每次请求都会返回。 |

## 分辨率说明

分辨率格式为 `宽:高`，约束条件：

- **宽高范围**：均在 [512, 2048] 像素内
- **面积限制**：宽 × 高 ≤ 1024 × 1024 = 1,048,576 像素
- **默认值**：`1024:1024`

常用组合示例：

| 分辨率       | 比例  | 说明     |
| --------- | --- | ------ |
| 1024:1024 | 1:1 | 默认值，方图 |
| 768:1024  | 3:4 | 竖版     |
| 1024:768  | 4:3 | 横版     |
| 512:1024  | 1:2 | 竖版长图   |
| 1024:512  | 2:1 | 横版长图   |

## 垫图（Images）说明

- 垫图用于引导生图方向，让生成结果更贴近参考图的风格或内容
- 每张图片 base64 编码后大小不超过 **10MB**
- 支持格式：**jpg、jpeg、png、webp**
- 最多传 **3 张** 图片
- 传入的是图片 URL 列表

## 错误码

| 错误码                                        | 描述          |
| ------------------------------------------ | ----------- |
| FailedOperation.GenerateImageFailed        | 图片生成失败      |
| FailedOperation.RateLimit                  | 请求过快，超出频率限制 |
| FailedOperation.InnerError                 | 内部错误        |
| FailedOperation.ImageDecodeFailed          | 图片解码失败      |
| FailedOperation.ImageDownloadError         | 图片下载错误      |
| InvalidParameterValue.ParameterValueError  | 参数取值错误      |
| InvalidParameter.InvalidParameter          | 参数无效        |
| ResourceUnavailable.NotExist               | 资源不存在       |
| ResourceUnavailable.InArrears              | 欠费停服        |
| ResourceUnavailable.LowBalance             | 余额不足        |
| UnsupportedOperation.UnauthorizedOperation | 未授权操作       |
