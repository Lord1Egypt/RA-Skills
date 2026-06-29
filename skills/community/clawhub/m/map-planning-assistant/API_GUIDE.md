# 高德地图API调用指南

## 个人地图创建API

### 接口说明

- **接口名称**：个人地图创建
- **接口路径**：`maps_schema_personal_map`
- **请求方式**：HTTPS GET
- **功能**：批量导入POI点位，生成高德可识别的个人地图，并输出二维码

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| key | string | 是 | 高德API密钥 |
| sceneType | string | 是 | 场景类型，固定为 `2`（仅创建资源点） |
| points | string | 是 | POI坐标集合，JSON格式字符串 |

### points参数格式

```json
[
  {
    "name": "点位名称",
    "location": "经度,纬度",
    "address": "详细地址",
    "poiid": "高德POI ID（可选）",
    "type": "点位类型（可选）"
  }
]
```

### 请求示例

```
https://restapi.amap.com/v3/maps_schema_personal_map?key=YOUR_API_KEY&sceneType=2&points=[{"name":"朝阳公园","location":"116.473,39.942","address":"北京市朝阳区"},{"name":"奥林匹克森林公园","location":"116.385,40.015","address":"北京市朝阳区"}]
```

### 返回结果

```json
{
  "status": "1",
  "info": "OK",
  "url": "https://a.amap.com/xxx",
  "qr_code": "https://a.amap.com/qr/xxx"
}
```

### 返回参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| status | string | 状态码，`1`表示成功 |
| info | string | 状态信息 |
| url | string | 地图链接，可在浏览器中打开 |
| qr_code | string | 二维码链接，扫码可在高德App中打开 |

### 使用方式

1. **扫码访问**：使用手机扫描二维码，自动打开高德App查看地图
2. **链接访问**：点击链接，在浏览器中打开地图
3. **分享功能**：可将链接或二维码分享给好友
4. **导航功能**：在高德App中可一键导航到任意点位

### 注意事项

1. **点位限制**：单次请求最多支持50个点位
2. **坐标格式**：经纬度用逗号分隔，如 `116.473,39.942`
3. **坐标范围**：
   - 经度：73°E - 135°E（中国范围）
   - 纬度：3°N - 53°N（中国范围）
4. **sceneType参数**：固定为 `2`，表示仅创建资源点（打卡点位标记模式）

### 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 10000 | 正常 | - |
| 10001 | 用户key不正确 | 检查API密钥 |
| 10003 | 日调用量超限 | 稍后重试 |
| 10004 | 并发量超限 | 降低请求频率 |
| 10005 | IP白名单限制 | 检查IP白名单配置 |
| 20000 | 请求参数错误 | 检查参数格式 |
| 20001 | 请求参数值错误 | 检查参数值 |

### 代码示例

#### Node.js

```javascript
const https = require('https');
const querystring = require('querystring');

async function createPersonalMap(apiKey, points) {
  const params = {
    key: apiKey,
    sceneType: '2',
    points: JSON.stringify(points)
  };

  const queryString = querystring.stringify(params);
  const url = `https://restapi.amap.com/v3/maps_schema_personal_map?${queryString}`;

  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.status === '1') {
            resolve({
              success: true,
              url: result.url,
              qrCode: result.qr_code
            });
          } else {
            reject(new Error(result.info));
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

// 使用示例
const points = [
  {
    name: '朝阳公园',
    location: '116.473,39.942',
    address: '北京市朝阳区'
  },
  {
    name: '奥林匹克森林公园',
    location: '116.385,40.015',
    address: '北京市朝阳区'
  }
];

createPersonalMap('YOUR_API_KEY', points)
  .then(result => {
    console.log('地图链接:', result.url);
    console.log('二维码:', result.qrCode);
  })
  .catch(error => {
    console.error('创建失败:', error.message);
  });
```

#### Python

```python
import requests
import json

def create_personal_map(api_key, points):
    url = 'https://restapi.amap.com/v3/maps_schema_personal_map'
    params = {
        'key': api_key,
        'sceneType': '2',
        'points': json.dumps(points)
    }

    response = requests.get(url, params=params)
    result = response.json()

    if result['status'] == '1':
        return {
            'success': True,
            'url': result['url'],
            'qr_code': result['qr_code']
        }
    else:
        raise Exception(result['info'])

# 使用示例
points = [
    {
        'name': '朝阳公园',
        'location': '116.473,39.942',
        'address': '北京市朝阳区'
    },
    {
        'name': '奥林匹克森林公园',
        'location': '116.385,40.015',
        'address': '北京市朝阳区'
    }
]

try:
    result = create_personal_map('YOUR_API_KEY', points)
    print('地图链接:', result['url'])
    print('二维码:', result['qr_code'])
except Exception as e:
    print('创建失败:', str(e))
```

### 最佳实践

1. **分批创建**：超过50个点位时，分批创建多张地图
2. **坐标验证**：创建前验证坐标有效性
3. **错误重试**：网络错误时自动重试1次
4. **缓存结果**：相同点位集合可缓存地图链接
5. **用户提示**：提示用户扫码查看完整地图

### 相关API

- **行政区划查询**：`config/district`
- **地理编码**：`geocode/geo`
- **POI关键字搜索**：`place/text`
- **POI周边搜索**：`place/around`
- **POI详情查询**：`place/detail`
- **天气查询**：`weather/weatherInfo`
- **路况查询**：`traffic/status/rectangle`

## 其他常用API

### 行政区划查询

```
https://restapi.amap.com/v3/config/district?key=YOUR_KEY&keywords=北京&subdistrict=2
```

### 地理编码

```
https://restapi.amap.com/v3/geocode/geo?key=YOUR_KEY&address=朝阳公园&city=北京
```

### POI关键字搜索

```
https://restapi.amap.com/v3/place/text?key=YOUR_KEY&keywords=公园&city=北京&offset=20&page=1
```

### POI周边搜索

```
https://restapi.amap.com/v3/place/around?key=YOUR_KEY&location=116.473,39.942&radius=3000&types=110000
```

### POI详情查询

```
https://restapi.amap.com/v3/place/detail?key=YOUR_KEY&id=B000A7BD6C
```

### 天气查询

```
https://restapi.amap.com/v3/weather/weatherInfo?key=YOUR_KEY&city=110000&extensions=all
```

### 路况查询

```
https://restapi.amap.com/v3/traffic/status/rectangle?key=YOUR_KEY&rectangle=116.351,39.912|116.451,40.012
```

## API调用限制

- **个人开发者**：每日调用次数充足
- **请求超时**：建议设置8秒
- **重试策略**：失败后重试1次
- **并发限制**：避免短时间内高频调用
- **IP限制**：可配置IP白名单

## 常见问题

### Q: 二维码无法在高德App打开

A: 检查以下几点：
1. `sceneType`参数是否为`2`
2. 点位经纬度格式是否正确
3. 坐标是否在中国范围内

### Q: 地图链接无法访问

A: 可能原因：
1. API密钥无效
2. 请求参数错误
3. 网络连接问题

### Q: 如何获取POI ID

A: 使用POI搜索接口获取，返回结果中的`id`字段即为POI ID

### Q: 点位数量超过限制怎么办

A: 分批创建多张地图，每批最多50个点位

## 技术支持

- 高德开放平台：https://lbs.amap.com/
- API文档：https://lbs.amap.com/api/webservice/guide/api/map/
- 开发者社区：https://lbsbbs.amap.com/
