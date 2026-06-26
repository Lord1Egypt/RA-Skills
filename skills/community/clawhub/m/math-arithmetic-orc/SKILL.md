---
name: math-arithmetic-ocr
description: |
  识别图片中的K12算式（加减乘除、竖式计算、分数、方程等），返回结构化文本结果。
  支持手写体和印刷体，可拒绝非算式图片。
  触发条件：用户要求识别算式、数学题、计算题图片，或上传数学题图片时调用。
  关键词：算式识别、数学题、OCR、竖式计算、ArithmeticOCR
---

# 数学算式识别技能

使用腾讯云 ArithmeticOCR API，精准识别图片中的数学算式，返回识别出的文本内容和结构化信息。

## 使用场景

✅ **适用：**
- 用户上传数学题图片（如竖式计算、分数方程、四则运算）
- 用户说“识别这张图里的算式”、“帮我读出这道数学题”
- 需要将手写或印刷的数学题转为可编辑文本

❌ **不适用：**
- 识别普通文档文字（请用通用OCR）
- 识别非数学内容的图片（风景、人物等，除非开启拒绝模式）

## 执行流程

### 1. 获取图片

从用户输入中获取图片：
- 优先使用 `imageBase64` 参数（图片的 Base64 编码）
- 其次使用 `imageUrl` 参数（图片的 URL 地址）

### 2. 调用腾讯云 API

使用 Node.js 脚本 `index.js` 调用腾讯云 `ArithmeticOCR` 接口，传入：
- 图片数据
- 可选参数：`rejectNonArithmetic`（是否拒绝非算式图）
- 可选参数：`enableDispMidResult`（是否显示竖式中间结果）

### 3. 处理返回结果

API 返回包含以下信息：
- `TextDetections`：识别的文本区域列表（每个区域包含文本内容、置信度、位置坐标）
- `Angle`：图片旋转角度
- `RequestId`：请求ID

### 4. 向用户返回结果

- 如果成功：返回所有识别出的文本（拼接成一句）和详细检测信息
- 如果失败：返回错误信息（如“图片中未检测到文本”、“API调用失败”等）

## 权限要求

此技能需要以下权限：
- `network.request`：访问腾讯云 API
- `file.read`：如果用户提供本地图片路径（需先读取文件）

## 配置说明

使用前需要在 OpenClaw 中配置腾讯云密钥：

**方式一：环境变量**

- TENCENTCLOUD_SECRET_ID=你的SecretId
- TENCENTCLOUD_SECRET_KEY=你的SecretKey


**方式二：OpenClaw 配置**

- openclaw config set tencentcloud.secretId "你的SecretId"
- openclaw config set tencentcloud.secretKey "你的SecretKey"


