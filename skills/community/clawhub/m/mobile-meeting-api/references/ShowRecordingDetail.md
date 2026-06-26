# 查询录制详情 - ShowRecordingDetail<a name="ZH-CN_TOPIC_0212714575"></a>

## 描述<a name="section17948858131615"></a>

该接口用于查询某个会议录制的详情。


## URI<a name="section3464194610267"></a>

GET /v1/mmc/management/conferences/record/files

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| confUUID | 是 | String | Query | 会议UUID(通过 查询录制列表 获取)。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section12277182184211"></a>

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

<a name="table6981112405218"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| confUUID | String | 会议UUID。 |
| confID | String | 会议ID。 |
| url | String[] | 录播观看地址。 |
| rcdTime | Integer | 录制时长（单位秒）。 |
| rcdSize | Integer | 录制文件大小（MB）。 |
| subject | String | 会议主题。 |
| scheduserName | String | 会议预订者名称。 |
| startTime | String | 会议开始时间。 |
| isDecodeFinish | Boolean | 录制文件是否转码完成。 |
| decodeEndTime | long | 录制文件预计转码完成时间。 |
| available | Boolean | 录播文件是否可观看。 |
| recordAuthType | Integer | 观看/下载录播的鉴权方式。 0: 可通过链接观看/下载 1: 企业用户可观看/下载 2: 与会者可观看/下载 |


## 请求消息示例<a name="section1498763918202"></a>

```
GET /v1/mmc/management/conferences/record/files?confUUID=51adf610220411eaaae03f22d33cc26b
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
Content-Length: 505
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: 4556e88832e5990723d1712395f5bee8
Server: api-gateway
X-Request-Id: 629891c82bb852d8796e2f6acc74721e

{
    "confUUID": "51adf610220411eaaae03f22d33cc26b",
    "confID": "912049654",
    "url": [
        "https://114.116.237.2/rse/rse/html/play/Mediaxplay.html?rseid=00030&recordId=000301fa-0512-412f-b363-cb9f76063628&token=24e4f6d9850a42365783c88ceb36701bb87f5393a595af82&confID=51adf610220411eaaae03f22d33cc26b&isSecure=true"
    ],
    "rcdTime": 71,
    "rcdSize": 0,
    "subject": "user8002的会议",
    "scheduserName": "user8002",
    "startTime": "2019-12-19 02:07",
    "isDecodeFinish": true,
    "decodeEndTime": 1576721412885,
    "available": true,
    "recordAuthType":2
}
```

## 错误码<a name="section288814321256"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section4952152111818"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/record/files?confUUID=51adf610220411eaaae03f22d33cc26b'
```

