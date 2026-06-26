# IC Search - 电子元器件搜索技能

## Frontmatter

```yaml
name: ic-search
description: 电子元器件询价、库存查询、求购现货搜索工具。当用户查询元器件价格、库存、报价、求购现货、找现货或提及 PCS 单位时触发此技能。自动调用 API 接口返回 JSON 格式的搜索数据。
```

## 技能说明

这是一个用于电子元器件搜索的专用技能。当用户进行以下操作时会自动触发：

- **询价** - 查询某个元器件的价格
- **查库存** - 查询某个元器件的库存情况
- **查报价** - 查询元器件的市场报价
- **求购** - 寻找电子元器件的求购渠道
- **找现货** - 搜索现货库存
- **PCS 单位** - 商品单位"个"的表述

## 使用方法

当需要搜索电子元器件信息时，直接使用以下命令格式：

```
搜索：[元器件型号/名称]
询价：[元器件型号]
查库存：[元器件型号]
查报价：[元器件型号]
求购：[元器件型号] 或 [元器件型号] [数量] 求购
找现货：[元器件型号] 或 [元器件型号] [数量] 现货
带 PCS：[元器件型号] [数量]pcs
```

## API 配置

### 请求地址
```
http://ip.icsdk.com:2022/api/v1/raw
```

### 请求方式
**GET 请求**，参数通过 URL 查询字符串传递

### 完整请求格式
```
GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=[URL 编码的搜索内容]
```

### 请求参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `supply` | string | 固定鉴权 token，固定值 `nkwd` 不可修改 | `nkwd` |
| `msg` | string | 搜索内容（元器件型号、数量、需求等），需 URL 编码 | `5601230200%20270%20 求购现货` |

### 请求示例
```bash
# 查询 5601230200 270 个求购现货
curl "http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=5601230200%20270%20%E6%B1%82%E8%B4%AD%E7%8E%B0%E8%B4%A7"

# 查询 430452000 648pcs
curl "http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=430452000%20648pcs"
```

### 请求参数 JSON 格式说明
```json
{
  "supply": "nkwd",
  "msg": "5601230200 270 求购现货"
}
```
实际调用时会将上述 JSON 中的值转换为 URL 查询参数。

### 返回格式

**成功返回格式**：
```json
{
  "code": 2000,
  "msg": "success",
  "data": "350218-1 库存 555 个 2-3 天 发\n时间:2026-03-17 12:50:18\nDC:\t22+\n500+ \t0.1427/PCS 含税\n1000+ \t0.0988/PCS 含税\n\n",
  "supply": "宁克沃德"
}
```

**无权操作返回格式**：
```json
{
  "code": 4004,
  "msg": "您无权操作",
  "data": null,
  "supply": "宁克沃德"
}
```

### 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 状态码，2000 表示成功，4004 表示无权操作 |
| `msg` | string | 状态消息 |
| `data` | string/null | 查询结果字符串，失败时为 null |
| `supply` | string | **供应商信息**（宁克沃德） |

### 错误处理规则

1. **当 `code` = 4004 时**：返回"您无权操作"
2. **当 `data` = null 时**：表示查询失败（库存/报价失败）
3. **当查询成功 (code=2000) 时**：返回 `data` 字段的内容给用户
4. **supply 字段**：始终显示供应商信息"宁克沃德"

## 工具配置

需要配置以下工具以支持技能运行：

### 1. HTTP 请求工具

```yaml
tools:
  - name: http_request
    description: 发送 HTTP 请求到指定的 API 接口
    parameters:
      url: string - 请求地址（包含 query 参数）
      method: string - HTTP 方法 (GET)
      headers: object - 请求头
    returns: object - 响应数据
```

### 2. JSON 解析工具

```yaml
tools:
  - name: json_parse
    description: 解析 JSON 数据并提取指定字段
    parameters:
      json: string - JSON 字符串
      path: string - 字段路径（如 data）
    returns: any - 提取的值
```

## 执行流程

1. **解析用户请求**，识别搜索意图和元器件信息
   - 检测关键词：询价、查库存、报价、求购、找现货、pcs
2. **构建 GET 请求 URL**：`http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=<URL 编码的搜索内容>`
3. **URL 编码** `msg` 参数（特别是包含空格和中文时）
4. **发送 GET 请求**
5. **解析返回的 JSON 数据**
6. **检查错误码并返回结果**：
   - code = 4004 → 返回"您无权操作"
   - data = null → 返回"查询失败"
   - code = 2000 → 返回 data 字段内容给用户（包含库存、价格、供应商信息）

## 示例

### 示例 1：查询 STM32 芯片现货
```
用户："STM32F103C8T6 找现货"
技能动作：调用 API
请求：GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=STM32F103C8T6
返回：{"data": "搜索结果..."}
```

### 示例 2：查找库存
```
用户："查 STM32F407 库存"
技能动作：调用 API
请求：GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=STM32F407
返回：{"data": {"string": "库存信息..."}}
```

### 示例 3：无权操作
```
用户："查 TP5430 报价"
技能动作：调用 API
返回：{"code": 4004, "msg": "您无权操作", "data": null, "supply": "nkwd"}
结果：返回"您无权操作"
```

### 示例 4：data 为 null
```
用户："查 ABC123 库存"
技能动作：调用 API
返回：{"code": 200, "data": null}
结果：返回"查询失败"
```

### 示例 5：带空格的搜索内容
```
用户："5601230200 270 求购现货"
技能动作：调用 API
请求：GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=5601230200%20270%20 求购现货
返回：{"data": {"string": "库存：1000 pcs\n价格：￥2.50"}}
```

## 注意事项

1. **supply 固定值**：supply 参数固定为 `nkwd`，作为鉴权 token 不可修改
2. **URL 编码**：msg 参数需要 URL 编码，特别是包含空格和中文时
3. **错误处理**：
   - 返回 code=4004 时，提示"您无权操作"
   - 返回 data=null 时，提示"查询失败"
4. **数据返回**：只返回 `data` 字段的内容，不包含 code/msg 等元数据
5. **GET 请求**：使用 GET 方法，参数在 URL 中传递
6. **频率限制**：避免短时间内大量请求

## 测试记录

**2026-03-17 13:44**: API 测试成功
```
请求：http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=5601230200%20270%20%E6%B1%82%E8%B4%AD%E7%8E%B0%E8%B4%A7

返回：
{
  "code": 2000,
  "msg": "success",
  "data": "560123-0200 库存 36510 个 1-2 天 发\n时间:2026-03-17 13:44:16\n10+ \t0.4977/PCS 含税\n100+ \t0.3988/PCS 含税\n300+ \t0.3494/PCS 含税\n1500+ \t0.3124/PCS 含税\n4500+ \t0.2827/PCS 含税\n10500+ \t0.2679/PCS 含税\n\n",
  "supply": "宁克沃德"
}
```

**查询结果**：
- 产品：560123-0200
- 库存：36510 个（1-2 天发货）
- 价格阶梯：
  - 10+ 个：¥0.4977/PCS（含税）
  - 100+ 个：¥0.3988/PCS（含税）
  - 300+ 个：¥0.3494/PCS（含税） ← **满足 270 个需求**
  - 1500+ 个：¥0.3124/PCS（含税）
  - 4500+ 个：¥0.2827/PCS（含税）
  - 10500+ 个：¥0.2679/PCS（含税）

## 参考资源

- [API 文档](references/api.md) - 详细的 API 接口文档
- [搜索示例](references/examples.md) - 常见搜索场景示例
- [错误代码](references/errors.md) - 常见错误码说明
