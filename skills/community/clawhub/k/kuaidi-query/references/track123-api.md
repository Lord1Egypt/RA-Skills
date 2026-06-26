# Track123 API 文档

## 基础信息

- **API 地址**: `https://api.track123.com/gateway/open-api/tk/v2.1`
- **认证方式**: API Key (通过 `app_key` 参数)
- **支持语言**: 支持多语言返回

## 认证

### 获取 API Key

访问 [Track123 官网](https://www.track123.com/) 注册账号并获取 API Key。

### 配置方式

在 `config.json` 中配置：

```json
{
  "track123": {
    "app_key": "your_track123_app_key"
  }
}
```

## API 接口

### 1. 实时查询 (Instant Tracking)

**接口**: `POST /tk/v2.1/track/query-realtime`

**功能**: 一次性创建并获取物流结果，立即返回最新物流状态。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_key` | string | 是 | API 密钥 |
| `number` | string | 是 | 运单号 |
| `carrier_code` | string | 否 | 快递公司代码，留空自动识别 |
| `language` | string | 否 | 返回语言：`zh` (中文), `en` (英文), `ru` (俄语) |

**请求示例**:

```bash
curl -X POST https://api.track123.com/gateway/open-api/tk/v2.1/track/query-realtime \
  -H "Content-Type: application/json" \
  -d '{
    "app_key": "your_app_key",
    "number": "SF1234567890123",
    "carrier_code": "sfex",
    "language": "zh"
  }'
```

**响应示例**:

```json
{
  "code": 200,
  "data": {
    "number": "SF1234567890123",
    "carrier_code": "sfex",
    "carrier_name": "顺丰速运",
    "status": "delivered",
    "status_description": "已签收",
    "origin_info": {
      "city": "深圳",
      "state": "广东",
      "country": "中国"
    },
    "destination_info": {
      "city": "北京",
      "state": "",
      "country": "中国"
    },
    "weight": "1.5kg",
    "signed_by": "本人",
    "track_info": [
      {
        "checkpoint_time": "2024-03-14 08:30:00",
        "tracking_detail": "【北京转运中心】已发出，下一站【上海转运中心】",
        "location": "北京"
      },
      {
        "checkpoint_time": "2024-03-13 22:15:00",
        "tracking_detail": "【北京转运中心】已到达",
        "location": "北京"
      }
    ]
  }
}
```

### 2. 自动识别快递公司

**接口**: `POST /tk/v2.1/courier/detection`

**功能**: 根据运单号自动识别快递公司。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_key` | string | 是 | API 密钥 |
| `number` | string | 是 | 运单号 |

**响应示例**:

```json
{
  "code": 200,
  "data": [
    {
      "carrier_code": "sfex",
      "carrier_name": "顺丰速运",
      "probability": 0.95
    }
  ]
}
```

### 3. 获取快递公司列表

**接口**: `GET /tk/v2.1/courier/list`

**功能**: 获取所有支持的快递公司列表。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `app_key` | string | 是 | API 密钥 |
| `language` | string | 否 | 返回语言 |

**响应示例**:

```json
{
  "code": 200,
  "data": [
    {
      "carrier_code": "sfex",
      "carrier_name": "顺丰速运",
      "carrier_name_en": "SF Express"
    },
    {
      "carrier_code": "yto",
      "carrier_name": "圆通速递",
      "carrier_name_en": "YTO Express"
    }
  ]
}
```

## 快递公司代码映射

### 国内快递

| 快递公司 | carrier_code |
|---------|-------------|
| 顺丰速运 | `sfex` |
| 圆通速递 | `yto` |
| 中通快递 | `zto` |
| 韵达速递 | `yunda` |
| 申通快递 | `sto` |
| 邮政 EMS | `ems` |
| 邮政平邮 | `youzheng` |
| 京东快递 | `jd` |
| 极兔速递 | `jt` |
| 菜鸟直送 | `cs` |

### 国际快递

| 快递公司 | carrier_code |
|---------|-------------|
| DHL | `dhl` |
| FedEx | `fedex` |
| UPS | `ups` |
| TNT | `tnt` |
| 顺丰国际 | `sfint` |

## 物流状态码

| 状态码 | 说明 |
|-------|------|
| `unknown` | 未知 |
| `pending` | 待揽收 |
| `picked_up` | 已揽收 |
| `in_transit` | 运输中 |
| `out_for_delivery` | 派送中 |
| `delivered` | 已签收 |
| `exception` | 异常 |
| `returned` | 已退回 |

## 错误码

| 错误码 | 说明 |
|-------|------|
| `200` | 成功 |
| `400` | 请求参数错误 |
| `401` | API Key 无效 |
| `403` | 权限不足 |
| `429` | 请求过于频繁 |
| `500` | 服务器错误 |

## 使用示例

### Node.js

```javascript
const axios = require('axios');

async function queryTracking(trackingNumber, carrierCode, language = 'zh') {
  const response = await axios.post(
    'https://api.track123.com/gateway/open-api/tk/v2.1/track/query-realtime',
    {
      app_key: 'your_app_key',
      number: trackingNumber,
      carrier_code: carrierCode,
      language: language
    }
  );
  
  return response.data;
}
```

### Python

```python
import requests

def query_tracking(tracking_number, carrier_code, language='zh'):
    response = requests.post(
        'https://api.track123.com/gateway/open-api/tk/v2.1/track/query-realtime',
        json={
            'app_key': 'your_app_key',
            'number': tracking_number,
            'carrier_code': carrier_code,
            'language': language
        }
    )
    return response.json()
```

## 注意事项

1. **API 配额**: 免费额度 100 次/天，详细配额请查看 [Rate Limit](/reference/rate-limit)
2. **缓存策略**: 建议对相同运单号进行缓存，避免重复查询
3. **错误处理**: 检查返回的 `code` 字段判断是否成功
4. **语言支持**: 支持中文、英文、俄语等多语言

## 参考链接

- [Track123 官网](https://www.track123.com/)
- [API 文档中心](https://docs.track123.com/)
- [Rate Limit](/reference/rate-limit)
- [错误码](/reference/status-code)
