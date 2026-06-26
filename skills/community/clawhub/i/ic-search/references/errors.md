# IC Search 错误代码说明

## 业务错误码

| 错误码 | 说明 | 处理提示 |
|--------|------|----------|
| 4004 | 无权操作 | "您无权操作" |
| null | data 为空 | "查询失败" |

## 错误处理规则

### 1. 无权操作（code = 4004）

**响应示例**：
```json
{
  "code": 4004,
  "msg": "您无权操作",
  "data": null,
  "supply": "nkwd"
}
```

**处理方式**：
直接返回给用户："您无权操作"

### 2. 查询失败（data = null）

**响应示例**：
```json
{
  "code": 200,
  "msg": "success",
  "data": null,
  "supply": "nkwd"
}
```

**处理方式**：
直接返回给用户："查询失败"（库存/报价失败）

### 3. 查询成功

**响应示例**：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "string": "元器件型号：STM32F103C8T6\n库存量：5000\n价格：￥2.50\n供应商：深圳市 XX 电子"
  },
  "supply": "nkwd"
}
```

**处理方式**：
返回 `data` 字段的内容给用户

## 错误处理代码示例

```python
def process_api_response(response):
    """
    处理 API 响应
    """
    # 检查是否无权操作
    if response.get('code') == 4004:
        return "您无权操作"
    
    # 检查 data 是否为 null
    if response.get('data') is None:
        return "查询失败"
    
    # 返回 data 内容
    data = response.get('data')
    if isinstance(data, dict) and 'string' in data:
        return data['string']
    return str(data)
```

## 常见错误场景

### 场景 1：账号无权限

**用户请求**：
```
查 STM32F103 库存
```

**API 返回**：
```json
{
  "code": 4004,
  "msg": "您无权操作",
  "data": null
}
```

**技能回复**：
"您无权操作"

### 场景 2：型号不存在或无数据

**用户请求**：
```
查 ABC123 报价
```

**API 返回**：
```json
{
  "code": 200,
  "msg": "success",
  "data": null
}
```

**技能回复**：
"查询失败"

### 场景 3：查询成功

**用户请求**：
```
查 STM32F103 现货
```

**API 返回**：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "string": "库存：5000  pcs\n价格：￥2.50/pcs\n供应商：深圳 XX 电子\n批号：23+45"
  }
}
```

**技能回复**：
```
库存：5000  pcs
价格：￥2.50/pcs
供应商：深圳 XX 电子
批号：23+45
```

## 调试建议

1. **验证 API 地址**：确保 `http://ip.icsdk.com:2022` 可以正常访问
2. **检查权限**：确认 API 账号有足够的操作权限
3. **验证数据**：测试有效的元器件型号，确认有数据返回
4. **查看日志**：记录请求参数和响应内容，便于排查问题
