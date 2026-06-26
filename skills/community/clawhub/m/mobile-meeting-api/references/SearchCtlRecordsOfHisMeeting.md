# 查询历史会议的会控记录 - SearchCtlRecordsOfHisMeeting<a name="ZH-CN_TOPIC_0212714423"></a>

## 描述<a name="section17948858131615"></a>

该接口用于查询指定历史会议的会控记录。


## URI<a name="section1392764619274"></a>

GET /v1/mmc/management/conferences/history/confCtlRecord

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| confUUID | 是 | String | Query | 会议UUID。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。 |
| limit | 否 | Integer | Query | 查询数量。默认值20，最大500条。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |
| Accept-Language | 否 | String | Header | 语言 。默认简体中文。 zh-CN：简体中文。 en-US：美国英文。 |


## 状态码<a name="section746264155116"></a>

**表 2**  状态码说明

<a name="table102780442391"></a>

| HTTP状态码 | 描述 |
|---|---|
| 200 | 操作成功。 |
| 400 | 参数异常。 |
| 401 | 未鉴权或鉴权失败。 |
| 403 | 权限受限。 |
| 500 | 服务端异常。 |


## 响应参数<a name="section498722842014"></a>

**表 3**  响应参数

<a name="table10381220417"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| offset | Integer | 查询偏移量。 |
| limit | Integer | 每页的记录数。 |
| count | Integer | 总记录数。 |
| data | Array of data objects | 会控操作列表。 |


**表 4**  data数据结构说明

<a name="table15981319111212"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| operateTime | long | 操作时间（UTC时间，单位毫秒）。 |
| operateSource | String | 操作来源。 |
| operator | String | 操作者。 |
| operateCode | String | 操作描述。 |
| operationObject | String | 被操作对象。 |
| operateResult | String | 操作结果。 |
| detail | String | 详情。 |


## 请求消息示例<a name="section1498763918202"></a>

```
GET /v1/mmc/management/conferences/history/confCtlRecord?confUUID=9a0fa6d10a5b11eaae5e191763c22c0e
Connection: keep-alive
X-Access-Token: stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 472
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: 2f3aa1fe64f6784b1eb6f75a67ef2b9d
Server: api-gateway
X-Request-Id: ba03d2ae3b805d8c545c83494c862b48

{
    "data": [
        {
            "operateTime": 1574119913464,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "启动声控",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119917864,
            "operateSource": "Conference System",
            "operator": "Conference System",
            "operateCode": "呼叫与会方",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119917870,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "关闭与会方麦克风",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119918064,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "打开与会方麦克风",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119917889,
            "operateSource": "Conference System",
            "operator": "Conference System",
            "operateCode": "设置主持人",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119932913,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "添加与会方",
            "operationObject": "**********905",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119935460,
            "operateSource": "Conference System",
            "operator": "Conference System",
            "operateCode": "呼叫与会方",
            "operationObject": "a5db36ce0a5b11eab313a52e57f34bda",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119935465,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "关闭与会方麦克风",
            "operationObject": "a5db36ce0a5b11eab313a52e57f34bda",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119944636,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "点名与会方",
            "operationObject": "a5db36ce0a5b11eab313a52e57f34bda",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119944857,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "停止声控",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119945099,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "打开与会方麦克风",
            "operationObject": "a5db36ce0a5b11eab313a52e57f34bda",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119945861,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "广播与会方",
            "operationObject": "a5db36ce0a5b11eab313a52e57f34bda",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119947619,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "挂断与会方",
            "operationObject": "a5db36ce0a5b11eab313a52e57f34bda",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119947859,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "取消广播与会方",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119948460,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "删除与会方",
            "operationObject": "**********905",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119949328,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "释放主持人",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119950672,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "关闭与会方麦克风",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119951805,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "取消全场静音",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119952067,
            "operateSource": "MCU",
            "operator": "MCU",
            "operateCode": "打开与会方麦克风",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        },
        {
            "operateTime": 1574119952954,
            "operateSource": "Portal",
            "operator": "Conference Operator",
            "operateCode": "申请发言",
            "operationObject": "9bd1c8b20a5b11eab31381603f51d3ae",
            "operateResult": "成功"
        }
    ],
    "offset": 0,
    "limit": 20,
    "count": 23
}
```

## 错误码<a name="section424714614336"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section4952152111818"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/history/confCtlRecord?confUUID=9a0fa6d10a5b11eaae5e191763c22c0e'
```

