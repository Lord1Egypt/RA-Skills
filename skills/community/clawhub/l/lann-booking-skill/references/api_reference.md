# Lann Booking API 参考文档

## 概述

本文档详细说明蘭泰式按摩预约系统的 API 接口规范，包括直连 API 模式和 MCP 协议模式。

## 直连 API 模式

### 创建预约接口

**Endpoint**: `https://open.lannlife.com/mcp/book/create`

**Method**: `POST`

**Content-Type**: `application/json`

#### 请求参数

| 参数名 | 类型 | 必填 | 校验规则 | 说明 | 示例 |
|--------|------|------|----------|------|------|
| mobile | string | 是 | `/^1[3-9]\d{9}$/` | 11 位中国大陆手机号 | `"13812345678"` |
| storeName | string | 是 | 必须与门店数据中的 name 完全一致 | 门店名称 | `"淮海店"` |
| serviceName | string | 是 | 必须与服务数据中的 name 完全一致 | 服务项目名称 | `"传统古法全身按摩-90分钟"` |
| count | number | 是 | `1 <= count <= 20` | 预约人数 | `2` |
| bookTime | string | 是 | ISO 8601 格式，且晚于当前时间 | 预约开始时间 | `"2024-01-15T14:00:00"` |

#### 请求示例

```bash
curl -X POST "https://open.lannlife.com/mcp/book/create" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "13812345678",
    "storeName": "淮海店",
    "serviceName": "传统古法全身按摩-90分钟",
    "count": 2,
    "bookTime": "2024-01-15T14:00:00"
  }'
```

#### 成功响应 (HTTP 200)

```json
{
  "success": true,
  "bookingId": "BOOK123456",
  "message": "预约成功！",
  "startTime": "2024-01-15T14:00:00",
  "endTime": "2024-01-15T15:30:00",
  "storeInfo": {
    "name": "淮海店",
    "address": "上海市黄浦区进贤路216号（近陕西南路）",
    "telephone": "021-62670235",
    "traffic": "地铁1号线陕西南路1号口出，沿陕西南路走到进贤路右转约100m"
  },
  "serviceInfo": {
    "name": "传统古法全身按摩-90分钟",
    "desc": "通过独特的推、拉、蹬、摇、踩等手法，还有大量被动瑜伽的动作，打开韧带，释放疲劳，让肌肉的疼痛与紧绷得到真正缓解，实现从身到心的全面放松。"
  }
}
```

#### 响应字段说明

| 字段名 | 类型 | 说明 | 出现条件 |
|--------|------|------|----------|
| success | boolean | 预约是否成功 | 总是返回 |
| bookingId | string | 预约唯一标识符 | 成功时返回 |
| message | string | 响应消息 | 总是返回 |
| startTime | string | 预约开始时间（ISO 8601） | 成功时返回 |
| endTime | string | 预约结束时间（ISO 8601） | 成功时返回 |
| storeInfo | object | 门店详细信息 | 成功时返回 |
| serviceInfo | object | 服务详细信息 | 成功时返回 |

#### 错误响应

**参数校验失败 (HTTP 400)**:
```json
{
  "success": false,
  "message": "请输入正确的11位中国大陆手机号"
}
```

**资源不存在 (HTTP 404)**:
```json
{
  "success": false,
  "message": "未找到匹配的门店"
}
```

**时间冲突 (HTTP 409)**:
```json
{
  "success": false,
  "message": "该时段已被预约，请选择其他时间"
}
```

**服务器错误 (HTTP 500)**:
```json
{
  "success": false,
  "message": "内部服务器错误，请稍后重试"
}
```

#### 常见错误码

| HTTP 状态码 | 错误类型 | 错误消息示例 | 处理建议 |
|------------|---------|-------------|---------|
| 400 | 参数校验失败 | "请输入正确的11位中国大陆手机号" | 修正参数后重试 |
| 400 | 参数校验失败 | "预约人数必须在1-20人之间" | 调整人数 |
| 400 | 参数校验失败 | "预约时间格式不正确" | 使用 ISO 8601 格式 |
| 400 | 参数校验失败 | "预约时间必须晚于当前时间" | 选择未来时间 |
| 404 | 资源不存在 | "未找到匹配的门店" | 重新选择门店 |
| 404 | 资源不存在 | "未找到匹配的服务项目" | 重新选择服务 |
| 409 | 时间冲突 | "该时段已被预约" | 选择其他时间 |
| 500 | 服务器错误 | "内部服务器错误" | 稍后重试 |
| 504 | 网关超时 | "请求超时" | 检查网络后重试 |

## MCP 协议模式

### 连接配置

#### 本地 stdio 模式

```json
{
  "mcpServers": {
    "lann-booking": {
      "command": "npx",
      "args": ["-y", "lann-mcp-server"]
    }
  }
}
```

#### 远程 streamableHttp 模式

```json
{
  "mcpServers": {
    "lann-booking": {
      "url": "https://open.lannlife.com/mcp",
      "type": "streamableHttp"
    }
  }
}
```

### MCP 工具定义

#### query_stores - 查询门店

**描述**: 查询蘭泰式按摩门店信息

**参数**:
```typescript
{
  keyword?: string;  // 可选，搜索关键词（门店名称、地址、地铁站）
  city?: string;     // 可选，城市名称（上海、杭州、成都等）
}
```

**返回**:
```typescript
{
  stores: Array<{
    name: string;
    address: string;
    telephone: string;
    traffic: string;
    longitude: number;
    latitude: number;
  }>;
}
```

#### query_services - 查询服务

**描述**: 查询可用的按摩和 SPA 服务项目

**参数**:
```typescript
{
  keyword?: string;   // 可选，搜索关键词（服务名称、描述）
  duration?: number;  // 可选，时长（分钟）
}
```

**返回**:
```typescript
{
  services: Array<{
    name: string;
    desc: string;
  }>;
}
```

#### create_booking - 创建预约

**描述**: 创建按摩服务预约

**参数**:
```typescript
{
  mobile: string;      // 必填，手机号
  storeName: string;   // 必填，门店名称
  serviceName: string; // 必填，服务名称
  count: number;       // 必填，人数（1-20）
  bookTime: string;    // 必填，预约时间（ISO 8601）
}
```

**返回**:
```typescript
{
  success: boolean;
  bookingId?: string;
  message: string;
  startTime?: string;
  endTime?: string;
  storeInfo?: object;
  serviceInfo?: object;
}
```

## 数据源参考

### 门店数据 (org_store.json)

**总数**: 75 家门店

**主要城市分布**:
- 上海市: ~60+ 家
- 杭州市: 7 家
- 成都市: 4 家
- 其他: 武汉、苏州、深圳、宁波各 1-2 家

**完整字段**:
```json
{
  "name": "门店名称（唯一标识）",
  "address": "详细地址",
  "telephone": "联系电话",
  "traffic": "交通指引（含地铁线路和出口）",
  "longitude": "经度坐标",
  "latitude": "纬度坐标"
}
```

### 服务数据 (prod_service.json)

**总数**: 28 项服务

**服务分类**:
1. 传统古法按摩系列: 6 项
2. 泰式精油护理系列: 7 项
3. 特色护理系列: 8 项
4. 快速/专项服务系列: 5 项
5. 其他: 2 项

**完整字段**:
```json
{
  "name": "服务名称（唯一标识）",
  "desc": "服务详细描述"
}
```

## 业务规则

### 预约规则

1. **人数限制**: 单次预约最多 20 人
2. **时间要求**: 预约时间必须晚于当前时间
3. **提前预约**: 建议至少提前 2 小时预约
4. **取消政策**: 需至少提前 1 小时联系门店取消或改期

### 匹配规则

1. **门店名称**: 必须与 `org_store.json` 中的 `name` 字段完全一致
2. **服务名称**: 必须与 `prod_service.json` 中的 `name` 字段完全一致
3. **模糊匹配**: 支持部分匹配，但最终提交前需用户确认完整名称

### 时间格式

- **输入格式**: ISO 8601 (`YYYY-MM-DDTHH:mm:ss`)
- **时区**: 默认北京时间 (UTC+8)
- **相对时间**: 支持自然语言解析（如"明天下午 2 点"）

## 安全与隐私

### 数据保护

1. **手机号脱敏**: 日志中应将手机号中间 4 位替换为 `****`
2. **不持久化存储**: Skill 不应本地存储用户敏感信息
3. **最小化原则**: 只收集完成预约所必需的信息

### 认证与授权

- **当前版本**: 无需特殊认证，直接调用 API
- **未来规划**: 可能引入 API Key 或 OAuth 认证

## 版本兼容性

- **API 版本**: v1（稳定）
- **MCP 协议**: 遵循最新 Model Context Protocol 规范
- **向后兼容**: API 接口保持稳定，新版本的客户端可调用旧版本服务端

## 故障排查

### 常见问题

**Q: 提示"未找到匹配的门店"怎么办？**
A: 请检查门店名称是否与 `org_store.json` 中的 `name` 完全一致，或使用 `query_stores` 工具获取准确的门店列表。

**Q: 预约时间格式应该如何填写？**
A: 使用 ISO 8601 格式，例如：`2024-01-15T14:00:00` 表示 2024 年 1 月 15 日 14:00。

**Q: 如何知道某个门店的具体位置？**
A: 使用 `query_stores` 工具并传入门店名称作为关键词，返回结果包含地址、电话、交通指引和经纬度坐标。

**Q: API 调用超时怎么办？**
A: 检查网络连接，确认 API Endpoint 是否正确，然后重试。如果持续失败，可能是服务器维护中，请稍后再试。

### 调试技巧

1. **启用详细日志**: 在 MCP 配置中设置 `logLevel: "debug"`
2. **测试连接**: 先调用 `query_stores` 验证连接是否正常
3. **参数验证**: 在调用 `create_booking` 前，先单独验证每个参数
4. **查看响应**: 记录完整的请求和响应内容，便于定位问题

## 更新日志

- **2026-04-09**: 更新 API 文档，增加 MCP 协议说明
- **2026-04-03**: 初始版本，定义基础 API 接口
