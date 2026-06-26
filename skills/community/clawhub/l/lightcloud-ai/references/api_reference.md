# 轻云开放API参考文档

## API概览

轻云开放API提供四个主要接口：
1. 获取访问令牌（Access Token）
2. 批量获取单据数据
3. 批量删除单据数据
4. 新增或更新多条无流程单据

## 1. 获取Access Token

### 请求信息

- **协议**: HTTPS
- **URL**: `https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken`
- **方法**: POST
- **Content-Type**: application/json

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appId | String | 是 | 轻应用id |
| eid | String | 是 | 团队id |
| secret | String | 是 | 轻应用secret |
| timestamp | long | 是 | 当前北京时间，Unix格式13位时间戳，精确到毫秒，3分钟内有效 |
| scope | String | 是 | 授权级别：team |

### 请求示例

```json
{
    "appId": "xxxxxx",
    "eid": "xxxxxx",
    "secret": "轻应用secret",
    "timestamp": 1522305194157,
    "scope": "team"
}
```

### 响应示例

```json
{
    "data": {
        "accessToken": "accessToken",
        "expireIn": 有效时间(秒),
        "refreshToken": "token刷新令牌"
    },
    "errorCode": 0,
    "success": true
}
```

## 2. 批量获取单据

### 请求信息

- **URL**: `https://www.yunzhijia.com/gateway/lightcloud/data/list?accessToken=xxx`
- **方法**: POST
- **Content-Type**: application/json

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| eid | String | 是 | 工作圈eid |
| formCodeId | String | 是 | 表单codeId |
| oid | String | 否 | 查询人openid |
| formInstIds | Array[String] | 是 | 单据id字符串数组 |

### 请求示例

```json
{
    "eid": "6822727",
    "formCodeId": "043c4167942e4f47b4bba46f0ee01f05",
    "formInstIds": [
        "6512748a72f7be0001e6d4fc"
    ]
}
```

### 响应示例

```json
{
    "data": [
        {
            "id": "637c76fd45365700016a2862",
            "important": {
                "流水号": "QYQKJYXSCS-20221110-001",
                "提交人": "王振宇",
                "所属部门": "研发中心"
            },
            "fieldContent": [
                {
                    "codeId": "Te_0",
                    "rawValue": "哪里",
                    "parentCodeId": "",
                    "sum": false,
                    "title": "单行文本框1",
                    "type": "textWidget",
                    "value": "哪里"
                }
            ]
        }
    ],
    "error": "success",
    "errorCode": 200,
    "success": true
}
```

## 单据字段类型

### 常见字段类型

- `textWidget`: 单行文本框
- `radioWidget`: 单选框
- `personSelectWidget`: 人员选择
- `departmentSelectWidget`: 部门选择
- `dateWidget`: 日期
- `serialNumWidget`: 流水号

### 系统保留字段

- `_S_APPLY`: 提交人
- `_S_DATE`: 申请日期
- `_S_DEPT`: 所属部门
- `_S_SERIAL`: 流水号
- `_S_TITLE`: 标题

## 使用注意事项

1. **时间戳有效性**: timestamp必须在3分钟内，否则请求会被拒绝
2. **Access Token有效期**: token有有效期限制（expireIn字段），过期需重新获取
3. **单据ID**: formInstIds是字符串数组，支持批量查询
4. **错误处理**: 检查响应中的success字段来判断请求是否成功

## 3. 批量删除单据

### 请求信息

- **URL**: `https://www.yunzhijia.com/gateway/lightcloud/data/batchDelete?accessToken=xxx`
- **方法**: POST
- **Content-Type**: application/json

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| eid | String | 是 | 工作圈eid |
| formCodeId | String | 是 | 表单codeId |
| oid | String | 否 | 删除人openid（有流程单据必传） |
| formInstIds | Array[String] | 是 | 单据id字符串数组 |

### 请求示例

```json
{
    "eid": "6822727",
    "formCodeId": "043c4167942e4f47b4bba46f0ee01f05",
    "oid": "6437a246e4b01c2909637004",
    "formInstIds": [
        "6512748a72f7be0001e6d4fc"
    ]
}
```

### 响应示例

```json
{
    "data": [""],
    "errorCode": 0,
    "success": true
}
```

## 4. 新增或更新多条无流程单据

### 请求信息

- **URL**: `https://www.yunzhijia.com/gateway/lightcloud/data/batchSave?accessToken=xxx`
- **方法**: POST
- **Content-Type**: application/json

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| eid | String | 是 | 工作圈eid |
| formCodeId | String | 是 | 表单codeId |
| oid | String | 是 | 新增人openid |
| data | JsonArray | 是 | 单据实例数组 |

### 数据结构说明

#### data数组中的对象结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| formInstId | String | 否 | 单据id，更新单据时必传，新增时不传 |
| widgetValue | Object | 是 | 主表单控件字段 |
| details | Object | 否 | 明细控件字段 |

#### widgetValue结构

主表单字段对象，key为控件codeId，value为控件值：

```json
{
    "_S_TITLE": "我是标题111",
    "Te_0": "单行文本框内容",
    "Ra_0": "单选框选项值"
}
```

#### details结构

明细表字段对象，key为明细控件codeId，value为明细表行数组：

```json
{
    "Dd_0": {
        "widgetValue": [
            {
                "_id_": "1",  // 行id，必填
                "Te_0": "明细字段1",
                "Te_1": "明细字段2"
            }
        ]
    }
}
```

### 请求示例

```json
{
    "eid": "6822727",
    "formCodeId": "e638244f8931481a98897e16674adfbf",
    "oid": "6437a246e4b01c2909637004",
    "data": [
        {
            "formInstId": "6392c76ee3232e50382ea9a6",
            "widgetValue": {
                "_S_TITLE": "我是标题111",
                "Te_0": "文本框内容",
                "Ra_0": "选项A"
            },
            "details": {
                "Dd_0": {
                    "widgetValue": [
                        {
                            "_id_": "1",
                            "Te_0": "明细行1字段1",
                            "Te_1": "明细行1字段2"
                        },
                        {
                            "_id_": "2",
                            "Te_0": "明细行2字段1",
                            "Te_1": "明细行2字段2"
                        }
                    ]
                }
            }
        }
    ]
}
```

### 响应示例

```json
{
    "data": ["6392c76ee3232e50382ea9a6", "6392c76ee3232e50382ea9a7"],
    "errorCode": 0,
    "success": true
}
```

### 使用说明

1. **新增单据**: 不传formInstId字段，系统会自动生成新的单据ID
2. **更新单据**: 必须传formInstId字段，系统会更新对应单据的数据
3. **批量操作**: data数组支持同时新增/更新多条单据
4. **明细表**: details字段用于明细表控件，可包含多行数据
5. **系统字段**: _S_TITLE等系统字段会自动处理，也可以手动指定
