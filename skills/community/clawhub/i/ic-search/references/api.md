# IC Search API 文档

## 接口信息

**地址**: `http://ip.icsdk.com:2022/api/v1/raw`

**方法**: `GET`

**Content-Type**: `application/json`（返回数据）

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| supply | string | 是 | 固定鉴权 token：`nkwd`（不可修改） |
| msg | string | 是 | 搜索内容：元器件型号、求购信息等（需要 URL 编码） |

## 请求示例

### 基本查询
```
GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=STM32F103C8T6
```

### 包含空格的查询
```
GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=5601230200%20270%20 求购现货
```

### URL 编码说明
- 空格 → `%20`
- 中文 → URL 编码后的字节序列
- 特殊字符 → 相应的编码

## 成功响应

```json
{
  "code": 200,
  "msg": "success",
  "data": "元器件型号：STM32F103C8T6\n库存量：5000\n价格：￥2.50\n供应商：深圳市 XX 电子",  
  "supply": "nkwd"
}
```

## 错误响应

### 无权操作（4004）

```json
{
  "code": 4004,
  "msg": "您无权操作",
  "data": null,
  "supply": "nkwd"
}
```

**处理方式**：返回"您无权操作"给用户

### 查询失败（data 为 null）

```json
{
  "code": 200,
  "msg": "success",
  "data": null,
  "supply": "nkwd"
}
```

**处理方式**：返回"查询失败"给用户

## 参数说明

| supply 值 | 说明 | 使用场景 |
|-----------|------|----------|
| `nkwd` | 固定鉴权 token | 所有查询都使用此值，不可修改 |
| - | - | - |

**注意**：supply 字段是固定鉴权 token，不是搜索类型。所有查询都使用 `nkwd`。

## 使用建议

1. **URL 编码**：msg 参数必须进行 URL 编码
2. **精确搜索**: 使用完整的元器件型号进行查询
3. **批量查询**: 支持多个型号的逗号分隔查询

## 错误处理逻辑

```python
def handle_response(response):
    # 无权操作
    if response.get('code') == 4004:
        return "您无权操作"
    
    # data 为 null，查询失败
    if response.get('data') is None:
        return "查询失败"
    
    # 返回 data 内容
    data = response.get('data')
    if isinstance(data, dict) in data:
        return data
    return str(data)
```

## 注意事项

- 使用 GET 方法，参数在 URL 中传递
- supply 参数固定为 `nkwd`
- msg 参数需要 URL 编码
- 当 `data` 为对象时，可能需要提取 `data.string`
- 建议对搜索结果进行适当的解析

## cURL 示例

```bash
# 基本查询
curl "http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=STM32F103C8T6"

# 包含空格的查询
curl "http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=5601230200%20270%20 求购现货"

# Python 自动编码
curl "http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=$(echo -n '5601230200 270 求购现货' | urllib.parse.quote)"
```
