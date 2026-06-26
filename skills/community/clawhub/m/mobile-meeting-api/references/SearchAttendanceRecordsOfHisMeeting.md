# 查询历史会议的与会者记录 - SearchAttendanceRecordsOfHisMeeting<a name="ZH-CN_TOPIC_0212714385"></a>

## 描述<a name="section17948858131615"></a>

该接口用于查询指定历史会议的与会者记录。


## URI<a name="section379619558285"></a>

GET /v1/mmc/management/conferences/history/confAttendeeRecord

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| confUUID | 是 | String | Query | 会议UUID。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。 |
| limit | 否 | Integer | Query | 查询数量。默认值20，最大500条。 |
| searchKey | 否 | String | Query | 查询条件 。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |
| Accept-Language | 否 | String | Header | 语言 。默认简体中文。 zh-CN：简体中文。 en-US：美国英文。 |


## 状态码<a name="section11564745135220"></a>

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

<a name="table6214171810123"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| offset | Integer | 查询偏移量。 |
| limit | Integer | 每页的记录数。 |
| count | Integer | 总记录数。 |
| data | Array of data objects | 与会者列表。 |


**表 4**  data数据结构说明

<a name="table1281264113140"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| displayName | String | 与会者名称。 |
| callNumber | String | 号码。 |
| deviceType | String | 设备类型。 |
| joinTime | long | 入会时间（UTC时间，单位毫秒）。 |
| leftTime | long | 离会时间（UTC时间，单位毫秒）。 |
| mediaType | String | 媒体类型。 |
| deptName | String | 部门名称。 |


## 请求消息示例<a name="section1498763918202"></a>

```
GET /v1/mmc/management/conferences/history/confAttendeeRecord?confUUID=9a0fa6d10a5b11eaae5e191763c22c0e
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
Content-Length: 337
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
            "displayName": "user8002",
            "callNumber": "+991116004380",
            "deviceType": "软终端",
            "joinTime": 1574119917872,
            "leftTime": 1574119956881,
            "mediaType": "视频",
            "deptName": "wangyue"
        },
        {
            "displayName": "+991116005905",
            "callNumber": "+991116005905",
            "deviceType": "软终端",
            "joinTime": 1574119935467,
            "leftTime": 1574119947620,
            "mediaType": "视频",
            "deptName": "wangyue"
        }
    ],
    "offset": 0,
    "limit": 20,
    "count": 2
}
```

## 错误码<a name="section1648691953419"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section4952152111818"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/history/confAttendeeRecord?confUUID=9a0fa6d10a5b11eaae5e191763c22c0e'
```

