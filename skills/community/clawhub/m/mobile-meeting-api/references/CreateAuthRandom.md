# 获取会议鉴权随机数 - CreateAuthRandom<a name="ZH-CN_TOPIC_0000002003833272"></a>

## 描述<a name="section1320411065418"></a>

该接口用于获取会议鉴权随机数。根据会议ID + 密码鉴权返回鉴权随机数，如果是小程序调用时，需要企业支持小程序功能。


## URI<a name="section379619558285"></a>

GET /v2/mms/ncms/conferences/auth/random

## 请求参数<a name="section220581045418"></a>

**表 1**  参数说明

<a name="table120571013547"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| conf_id | 是 | String | Query | 会议ID。 |
| guest_waiting | 否 | Interger | Query | 0-不支持来宾会前等待页能力（默认）、1-支持来宾会前等待页能力 |
| X-Password | 是 | String | Header | 会议密码。 |


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
| random | String | 鉴权随机数 |
| subject | String | 会议主题 |
| conf_mode | String | 会议类型模型: COMMON：MCU会议 RTC：MMR会议 |
| webinar | Boolean | 是否为网络研讨会 |
| need_password | Boolean | 是否需要密码 |
| support_applets | Boolean | 是否支持小程序 |


## 请求消息示例<a name="section32075107547"></a>

```
GET /v2/mms/ncms/conferences/auth/random?conf_id=914047175
Connection: keep-alive
X-Access-Token: *******
X-Password: *******
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)
```

## 响应消息示例<a name="section19208410165412"></a>

```
HTTP/1.1 200 OK
X-Request-Id: 01ab6499-db00-4029-9600-82046297767c
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
Etag: "03eb377e7dedca62136c5db551858b5f6"
Content-Type: application/json;charset=UTF-8
Content-Length: 134
Date: Thu, 29 Aug 2024 09:24:48 GMT
X-Envoy-Upstream-Service-Time: 34
Server: istio-envoy
Requestid: 01ab6499-db00-4029-9600-82046297767c

{
    "random": "397381479198454",
    "subject": "zhang的会议",
    "conf_mode": "RTC",
    "webinar": false,
    "need_password": false,
    "support_applets": true
}
```

## 错误码<a name="section1208110135417"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section3208810175415"></a>

```
curl -k -i -X GET -H "X-Password:******" -H "X-Access-Token:******"  https://apigw.125339.com.cn/v2/mms/ncms/conferences/auth/random?conf_id=914047175
```

