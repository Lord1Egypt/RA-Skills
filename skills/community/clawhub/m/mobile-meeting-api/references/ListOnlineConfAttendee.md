# 查询在线会议与会者信息 - ListOnlineConfAttendee<a name="ZH-CN_TOPIC_0000002112516106"></a>

## 描述<a name="section1320411065418"></a>

该接口用于查询指定会议的在线与会者信息。


## URI<a name="section379619558285"></a>

GET /v1/mmc/management/conferences/online/conf-attendee

## 请求参数<a name="section220581045418"></a>

**表 1**  参数说明

<a name="table120571013547"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| conf_id | 是 | String | Query | 会议ID。 |
| offset | 否 | Integer | Query | 记录数偏移.默认为0。 |
| limit | 否 | Integer | Query | 返回的与会者记录数。默认是20, 最大500条。 |
| search_key | 否 | Integer | Query | 查询条件,支持name、call_number、third_account查询。 |


## 状态码<a name="section149720335114"></a>

**表 2**  状态码说明

<a name="table102780442391"></a>

| HTTP状态码 | 描述 |
|---|---|
| 200 | 操作成功。 |
| 400 | 参数异常。 |
| 401 | 未鉴权或鉴权失败。 |
| 403 | 权限受限。 |
| 500 | 服务端异常。 |


## 响应参数<a name="section920651085413"></a>

**表 3**  响应参数

<a name="table1420618109547"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| data | Array of OnlineAttendeeRecordInfo objects | 在线与会者信息列表 。 |
| offset | Integer | 记录数偏移,第几条。 |
| limit | Integer | 每页的记录数。 |
| count | Integer | 总记录数 |


**表 4**  OnlineAttendeeRecordInfo 数据结构

<a name="table637344121814"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| participant_id | String | 与会者标识。 |
| name | String | 与会者名称。 |
| call_number | String | 呼叫号码。 |
| role | Integer | 会议中的角色,枚举值如下: 1:会议主席 0:普通与会者。 |
| third_account | String | 开放性场景标识第三方账号信息。 |
| account | String | 用户账号。 |
| user_id | String | 用户UUID。 |


## 请求消息示例<a name="section32075107547"></a>

```
GET /v1/mmc/management/conferences/online/conf-attendee?conf_id=964138987&search_key=wu
Connection: keep-alive
X-Access-Token: *******
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)
```

## 响应消息示例<a name="section19208410165412"></a>

```
HTTP/1.1 200 OK
X-Request-Id: 0905d26b-8de3-42f3-8a35-e8cff505ea74
Pragma: no-cache
Cache-Control: no-cache
Expires: Thu, 01 Jan 1970 00:00:00 GMT
X-Xss-Protection: 1; mode=block
X-Download-Options: noopen
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: connect-src 'self' *.125339.com ;style-src 'self' 'unsafe-inline' 'unsafe-eval';object-src 'self'; font-src 'self' data:;
Vary: Origin,Access-Control-Request-Method,Access-Control-Request-Headers
Etag: "0765cdce0f557b279da32b567609d4ba5"
Content-Type: application/json;charset=UTF-8
Content-Length: 17
Date: Thu, 14 Nov 2024 02:19:47 GMT
X-Envoy-Upstream-Service-Time: 123
Server: istio-envoy

{
  "data": [
    {
      "participant_id": "afa4157fa71611ef8f3fc33c80df3afd",
      "name": "test",
      "call_number": "+8657135*****769",
      "role": 1,
      "third_account": "testAccount",
      "account": "Auto-5ee7fc8cc06d470db323f1c4ca4f914e",
      "user_id": "17486137a62f47138b01ca53e9e1de79"
    }
  ],
  "offset": 0,
  "limit": 20,
  "count": 1
}
```

## 错误码<a name="section1208110135417"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section3208810175415"></a>

```
curl -k -i -X GET  -H "X-Access-Token:******"  https://apigw.125339.com.cn/v1/mmc/management/conferences/online/conf-attendee?conf_id=964138987&search_key=wu
```

