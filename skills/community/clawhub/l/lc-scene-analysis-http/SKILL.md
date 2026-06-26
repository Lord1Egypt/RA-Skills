---
name: lc_scene_analysis_http
description: 工地隐患分析模型技能，默认处理施工现场静态图片的隐患识别；仅在用户明确要求时调用数据采集或交叉验证接口。
version: 1.0.0
homepage: https://clawhub.ai/chenqu108/lc-scene-analysis-http
user-invocable: true
metadata:
  openclaw:
    os:
      - windows
      - linux
    requires:
      bins:
        - curl
      config:
        - auth profile: lc_scene_http:default
---

# LC Scene Analysis HTTP

这是一个**工地隐患分析模型**技能，用于处理施工现场静态图片的安全隐患识别任务。

## 何时使用

当用户提供施工现场图片或图片 URL，并希望：

- 识别图片中的安全隐患
- 获取模型分析结果
- 输出隐患结论或简要说明

此时使用本技能。

## 不要使用

以下情况不要调用本技能：

- 视频流分析
- 摄像头实时拉流
- 本地模型推理
- PLC、机器人、设备控制
- 非施工现场图片分析
- 与工地隐患识别无关的任务

## 前置要求

需要存在 auth profile：

- `lc_scene_http:default`

该 profile 需提供以下字段：

- `api_base`：服务基地址
- `api_key`：接口认证信息
- `flow_id`：默认 flowId
- `algorithm_id`：默认 algorithmId，可为空

如果用户本次请求显式提供了 `flow_id` 或 `algorithm_id`，优先使用用户输入；否则使用默认配置。

不要向用户展示任何密钥、token、profile 内容或本地认证文件内容。

## 接口说明

### 1. 默认接口：智能巡检
接口：

`POST /api/chat/agent/chatOnceNew`

用途：

- 默认图片隐患分析
- 工地安全隐患识别
- 普通分析请求优先走该接口

### 2. 数据采集接口
接口：

`POST /api/chat/agent/chatOnceRaw`

用途：

- 用户明确要求数据采集
- 用户明确要求结构化结果、原始结果、JSON 结果时调用

### 3. 交叉验证接口
接口：

`POST /api/chat/agent/crossVerify`

用途：

- 用户明确要求交叉验证、复核、二次校验时调用
- 当前会结合 CV 小模型对输出结果进行二次校验

## 选择规则

按以下规则选择接口：

- 用户明确要求“交叉验证 / 复核 / 二次校验 / 再确认” → `crossVerify`
- 用户明确要求“数据采集 / 原始结果 / 结构化结果 / JSON 结果” → `chatOnceRaw`
- 其他普通工地隐患分析请求 → `chatOnceNew`

如果无法判断，默认使用 `chatOnceNew`。

## 输入要求

优先接受以下输入：

- 单张图片 URL
- 多张图片 URL
- 用户额外提供的 `flow_id`
- 用户额外提供的 `algorithm_id`

如果没有图片或图片 URL，不要调用接口，应明确告知缺少输入。

## 请求要求

调用时：

- 从 `lc_scene_http:default` 读取默认配置
- 使用其中的 `api_base`、`api_key`、`flow_id`、`algorithm_id`
- 若用户显式传入 `flow_id` / `algorithm_id`，则覆盖默认值
- 默认调用 `chatOnceNew`
- 仅在用户明确要求时调用 `chatOnceRaw` 或 `crossVerify`

## 输出要求

- 默认返回核心隐患识别结果
- 如用户要求原始结果或结构化结果，尽量保留关键字段
- 可以做简洁总结，但不要篡改关键结论
- 不确定内容不要说成确定事实

## 错误处理

以下情况要明确报错，不要伪造结果：

- auth profile 不存在
- profile 缺少必要字段
- 图片输入缺失
- 服务返回 4xx / 5xx
- 服务超时
- 返回结构异常

## 安全要求

- 不要输出密钥、token、Authorization 信息
- 不要输出认证文件内容
- 对外部图片 URL 保持谨慎
- 如果任务明显超出工地隐患分析范围，不要强行调用本技能

## 示例

### 示例 1：默认分析
用户：
“帮我分析这张施工现场图片有哪些隐患：https://example.com/a.jpg”

处理：
- 调用 `chatOnceNew`

### 示例 2：数据采集
用户：
“把这张图按结构化结果返回：https://example.com/b.jpg”

处理：
- 调用 `chatOnceRaw`

### 示例 3：交叉验证
用户：
“这张图再帮我做一次交叉验证：https://example.com/c.jpg”

处理：
- 调用 `crossVerify`