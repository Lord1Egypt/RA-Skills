# AI图表生成API参数说明

## 目录

- [接口概述](#接口概述)
- [基础参数](#基础参数)
- [核心参数](#核心参数)
- [严格模式专用参数](#严格模式专用参数)
- [高级参数](#高级参数)
- [生成模式说明](#生成模式说明)
- [返回结果](#返回结果)
- [使用示例](#使用示例)

## 接口概述

**接口路径**: `https://mcp.mysteel.com/mcp/info/genie-tool/v1/tool/ai-chart`
**请求方法**: `POST`

本接口提供智能图表生成能力，根据任务描述自动生成ECharts图表配置。

## 基础参数

| 参数名         | 类型     | 必填 | 说明             |
|-------------|--------|----|----------------|
| `requestId` | string | ✅  | 请求唯一标识符（脚本自动生成） |
| `sessionId` | string | ❌  | 会话标识符          |

## 核心参数

| 参数名    | 类型            | 必填 | 默认值       | 说明                                   |
|--------|---------------|----|-----------|--------------------------------------|
| `task` | string        | ✅  | -         | 任务描述，描述需要生成的图表需求                     |
| `data` | array/object  | ❌  | null      | 图表数据，可以是数组或对象                        |
| `type` | string        | ❌  | null      | 图表类型，如：折线图、柱状图、饼图等                  |
| `mode` | string        | ❌  | `FREEDOM` | 生成模式，可选值：`FREEDOM`、`STRICT`、`TEMPLATE`、`AUTO` |

**Header 参数**：

| 参数名       | 类型   | 必填 | 说明                   |
| ------------ | ------ | ---- | ---------------------- |
| `Content-Type` | string | ✅   | 固定值：application/json |
| `token`      | string | ✅   | 身份秘钥标识符         |

## 严格模式专用参数

| 参数名               | 类型   | 必填 | 说明                       |
|-------------------|------|----|--------------------------|
| `dataDescription` | string | ❌  | 数据描述，说明数据结构和字段含义（严格模式推荐使用）   |
| `dataExample`     | array/object | ❌  | 数据示例，提供小样本数据作为参考（严格模式推荐使用） |

## 高级参数

| 参数名            | 类型      | 必填 | 默认值    | 说明                                   |
|----------------|---------|----|--------|--------------------------------------|
| `option`       | object  | ❌  | null   | 自定义图表配置模板，会与生成的配置合并                |
| `asyncEnable`  | boolean | ❌  | `false` | 是否启用异步模式                             |
| `robustMode`   | boolean | ❌  | `false` | 是否开启健壮模式（仅严格模式下生效，提高容错性）            |

## 生成模式说明

### 1. FREEDOM（自由模式）- 默认模式

**适用场景**: 快速生成图表，数据量小或无需提供数据

**特点**:
- 只需提供任务描述即可
- AI 根据描述自动生成图表配置
- 适合原型设计和快速验证

**示例**:
```json
{
  "requestId": "req-001",
  "task": "生成一个展示2024年各月份销售额的折线图",
  "mode": "FREEDOM",
  "token": "your_api_key"
}
```

### 2. STRICT（严格模式）

**适用场景**: 大数据量可视化，需要高性能转换

**特点**:
- 必须提供 `data`（实际数据）和 `dataExample`（数据示例）
- 推荐提供 `dataDescription`（数据描述）
- AI 生成 Python 代码进行数据转换，性能更好
- 自动执行代码并生成图表配置

**示例**:
```json
{
  "requestId": "req-002",
  "task": "将销售数据转换为折线图",
  "mode": "STRICT",
  "data": [
    {"month": "1月", "sales": 1200},
    {"month": "2月", "sales": 1500},
    {"month": "3月", "sales": 1800}
  ],
  "dataExample": [
    {"month": "1月", "sales": 1200}
  ],
  "dataDescription": "数据结构包含月份和销售额两个字段",
  "token": "your_api_key"
}
```

### 3. TEMPLATE（模板模式）

**适用场景**: 使用预定义的图表模板快速生成标准图表

**特点**:
- 基于注册的图表类型生成
- 支持折线图（line）、柱状图（bar）、饼图（pie）等模板
- 通过 `type` 参数指定图表类型，系统自动匹配对应的模板
- 生成速度快，配置标准化

**支持的模板类型**:
- `line` / `折线图` / `折线` - 折线图模板
- `bar` / `柱状图` / `柱形图` / `条形图` - 柱状图模板

**示例**:
```json
{
  "requestId": "req-003",
  "task": "生成一个折线图展示销售趋势",
  "mode": "TEMPLATE",
  "type": "折线图",
  "data": [...],
  "token": "your_api_key"
}
```

### 4. AUTO（自动模式）

**适用场景**: 让系统智能选择最适合的模式

**特点**:
- 当前实现中，AUTO 模式默认使用自由模式（FREEDOM）的处理逻辑
- 适合不确定使用哪种模式的场景

## 返回结果

### 同步模式响应（asyncEnable=false）

#### 成功响应
```json
{
  "code": 200,
  "data": {
    "option": {
      "title": {...},
      "xAxis": {...},
      "yAxis": {...},
      "series": [...]
    },
    "optionUrl": "",
    "previewUrl": ""
  },
  "requestId": "req-001"
}
```

**字段说明**:
- `option`: 图表配置对象（ECharts 配置），直接可用
- `optionUrl`: 图表配置文件的远程 URL
- `previewUrl`: 图表预览页面的 URL

#### 错误响应
```json
{
  "code": 500,
  "message": "图表生成失败",
  "requestId": "req-001"
}
```

### 异步模式响应（asyncEnable=true）

#### 立即响应
```json
{
  "code": 200,
  "data": {
    "pollUrl": ""
  },
  "requestId": "req-001"
}
```

**字段说明**:
- `pollUrl`: 轮询任务结果的 URL，需要通过 GET 请求此 URL 获取任务状态和结果

#### 轮询任务结果

**任务运行中**:
```json
{
  "taskId": "req-001",
  "status": "running",
  "result": null,
  "startTime": 1704067200000,
  "endTime": null
}
```

**任务完成**:
```json
{
  "taskId": "req-001",
  "status": "completed",
  "result": {
    "title": {...},
    "xAxis": {...},
    "yAxis": {...},
    "series": [...]
  },
  "startTime": 1704067200000,
  "endTime": 1704067250000
}
```

**任务失败**:
```json
{
  "taskId": "req-001",
  "status": "failed",
  "result": "图表生成失败：数据格式错误",
  "startTime": 1704067200000,
  "endTime": 1704067210000
}
```

## 使用示例

### 示例1: 基础折线图（自由模式）

**请求**:
```json
{
  "requestId": "example-001",
  "task": "生成一个展示2024年1-12月销售额趋势的折线图，数据为：[1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3200, 3500, 3800, 4000]",
  "mode": "FREEDOM",
  "token": "your_api_key"
}
```

### 示例2: 大数据量柱状图（严格模式）

**请求**:
```json
{
  "requestId": "example-002",
  "task": "将销售数据转换为柱状图，展示各产品的销量对比",
  "mode": "STRICT",
  "data": [
    {"product": "产品A", "sales": 12000},
    {"product": "产品B", "sales": 15000},
    {"product": "产品C", "sales": 18000},
    {"product": "产品D", "sales": 20000}
  ],
  "dataExample": [
    {"product": "产品A", "sales": 12000}
  ],
  "dataDescription": "数据包含产品名称和销售额两个字段",
  "token": "your_api_key"
}
```

### 示例3: 模板模式生成饼图

**请求**:
```json
{
  "requestId": "example-003",
  "task": "生成一个展示市场份额的饼图",
  "mode": "TEMPLATE",
  "type": "饼图",
  "data": [
    {"name": "产品A", "value": 30},
    {"name": "产品B", "value": 25},
    {"name": "产品C", "value": 20},
    {"name": "产品D", "value": 15},
    {"name": "其他", "value": 10}
  ],
  "token": "your_api_key"
}
```

### 示例4: 异步模式

**请求**:
```json
{
  "requestId": "example-004",
  "task": "生成一个包含多个数据系列的复杂折线图",
  "asyncEnable": true,
  "token": "your_api_key"
}
```

返回轮询URL后，定期轮询获取结果。

## 注意事项

1. **模式选择**:
   - 快速原型：使用 `FREEDOM` 模式
   - 大数据量：使用 `STRICT` 模式，并提供 `data`、`dataExample`、`dataDescription`
   - 标准图表：使用 `TEMPLATE` 模式，配合 `type` 参数指定图表类型
   - 不确定场景：使用 `AUTO` 模式

2. **数据格式**:
   - `data` 可以是数组或对象
   - 严格模式下，`dataExample` 应与 `data` 结构一致

3. **健壮模式（robustMode）**:
   - 仅在严格模式下生效
   - 开启后，即使图表配置验证失败，只要检测到有效数据（series 中有数据），也会接受生成的配置

4. **异步模式**:
   - 适用于复杂图表生成或可能超时的场景
   - 设置 `asyncEnable=true` 后，立即返回 `pollUrl`
   - 建议轮询间隔：1-3 秒

5. **返回数据**:
   - 同步模式下，`option` 字段包含完整的图表配置
   - `optionUrl` 是配置文件的远程访问地址
   - `previewUrl` 是图表预览页面地址
