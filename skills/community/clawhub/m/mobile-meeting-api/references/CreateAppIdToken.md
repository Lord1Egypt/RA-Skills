# 执行App ID鉴权 - CreateAppIdToken<a name="ZH-CN_TOPIC_0277183540"></a>

## 描述<a name="section698218449183"></a>

该接口使用App ID方式进行鉴权，鉴权通过后生成一个Access Token。App ID鉴权的原理介绍请参考https://www.125339.com.cn/developerCenter/ReBar/63/191

>![](public_sys-resources/icon-note.gif) **说明：** 
>-   当clientType取值为72时，同一个userId，同时最多能创建64个Token。比如已经创建了64个Token，并且Token都在有效期内，再用同一个userId创建一个Token，前64个Token中最早创建的Token将失效。
>-   当clientType取值为非72时，同一个userId，同时最多能创建1个Token。
>-   Token有效期是12\~24小时。


## URI<a name="section1089982010481"></a>

POST /v2/usg/acs/auth/appauth

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| Authorization | 是 | String | Header | 携带应用鉴权信息。 规则：HMAC-SHA256 signature=HexEncode(HMAC256((appId + ":" + userId + ":" + expireTime + ":" + nonce), appKey)),access=base64(appId) 样例：HMAC-SHA256 signature=07f31aa9eafb06652c6899248b145c1a3264242e2ccf4c81b1b6eb99bb5c,access=ZmRiOGU0Njk5NTg2NDU4YmJkMTBjODM0ODcyZGNjNjI= 说明： 如携带了userId信息，则Body中，也需填写对应的userId信息。 （必填）鉴权头域携带access内容为对应颁发应用id进行base64编码。 |
| X-Token-Type | 是 | String | Header | Token类型设置为：LongTicket |
| Content-Type | 是 | String | Header | Body的媒体格式。 样例：application/json; charset=UTF-8 |
| X-Request-ID | 否 | String | Header | 请求requestId，用来标识一路请求，用于问题跟踪定位，建议使用UUID，若不携带，则后台自动生成。 |
| Accept-Language | 否 | String | Header | 语言参数，默认为中文zh-CN，英文为en-US。 |
| appId | 是 | String | Body | App ID。如何获取App ID请参考“ App ID的申请 ”“ App ID的申请 ”。 |
| clientType | 是 | Integer | Body | 登录账号类型。 72：API调用类型 登录客户端类型。 50：手机客户端 51：PAD客户端 52：PC客户端 53：电视客户端 54：大屏客户端 55：WEB客户端 72：API类型（Token不互踢） |
| corpId | 否 | String | Body | 企业ID。 说明： 当SP应用场景携带，如果corpId和userId字段未携带或值为空字符串时，当作SP默认管理员登录。 仅在SP模式下需要填写，单企业模式不要填写，否则会鉴权失败。 |
| expireTime | 是 | Long | Body | 应用鉴权信息过期时间戳，单位秒。 说明： 当收到App ID鉴权请求时服务端的Unix时间戳大于expireTime时，本次鉴权失败。 样例：如果要求App ID鉴权信息10分钟后过期，expireTime = 当前Unix时间戳 + 60*10。 如果要求应用鉴权信息始终不过期，expireTime = 0。 |
| nonce | 是 | String | Body | 随机字符串，用于计算应用鉴权信息。 minLength：32 maxLength：64 |
| userEmail | 否 | String | Body | email地址。 |
| userId | 否 | String | Body | 第三方用户ID。 说明： 当userId字段未携带或值为空字符串时，当作企业默认管理员登录。 |
| userName | 否 | String | Body | 用户名称。 |
| userPhone | 否 | String | Body | 手机号，例如中国大陆手机+86xxxxxxx |
| deptCode | 否 | String | Body | 部门编码。通过“ 查询部门及其一级子部门列表 ”接口获取。 |


## 状态码<a name="section94280449413"></a>

**表 2**  状态码说明

<a name="table18118135764112"></a>

| HTTP状态码 | 描述 |
|---|---|
| 200 | 操作成功。 |
| 400 | 参数异常。 |
| 401 | 鉴权失败。 |
| 403 | 没有权限。 |
| 412 | 账号被停用。 |
| 423 | 账号已被锁定。 |
| 500 | 服务端异常。 |


## 响应参数<a name="section1957919610182"></a>

**表 3**  响应参数

<a name="table1110424213369"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| accessToken | String | Access Token字符串。 |
| clientType | Integer | 登录账号类型。 72：API调用类型 登录客户端类型。 50：手机客户端 51：PAD客户端 52：PC客户端 53：电视客户端 54：大屏客户端 55：WEB客户端 72：API类型（Token不互踢） |
| createTime | Long | Access token的创建时间戳，单位：毫秒。 |
| daysPwdAvailable | Integer | 密码有效天数。 |
| delayDelete | Boolean | 是否延时删除状态。 |
| expireTime | Long | Access Token的失效时间戳，单位：秒。 |
| firstLogin | Boolean | 是否首次登录。 说明： 首次登录表示尚未修改过密码。首次登录时，系统会提醒用户需要修改密码。 默认值：false。 |
| forceLoginInd | Integer | 抢占登录标识。 0：非抢占 1：抢占（未启用） |
| proxyToken | ProxyTokenDTO object | 代理鉴权信息。 |
| pwdExpired | Boolean | 密码是否过期。 默认值：false。 |
| refreshCreateTime | Long | Refresh Token的创建时间戳，单位：毫秒。 |
| refreshExpireTime | Long | Refresh Token的失效时间戳，单位：秒。 |
| refreshToken | String | Refresh Token字符串。 |
| refreshValidPeriod | Long | Refresh Token有效时长，单位：秒。 |
| tokenIp | String | 用户IP。 |
| tokenType | Integer | Token类型。 0：用户ACCESS TOKEN 1：会控TOKEN 2：一次性TOKEN |
| user | UserInfo object | 用户鉴权信息。 |
| validPeriod | Long | Access Token的有效时长，单位：秒。 |


## 请求消息示例<a name="section1498763918202"></a>

```
POST /v2/usg/acs/auth/appauth
Connection: keep-alive
Content-Type: application/json
X-Request-ID: 5162fa32dc7e47afafeee39a72a2eec3
Accept-Language: zh-CN
Host: apigw.125339.com.cn
X-Token-Type: LongTicket
Authorization: HMAC-SHA256 signature=3eca3f0f1e90ed55de38388066d02f1b7a86571a8ce30823af1df7c4edd7e086,access=ZmRiOGU0Njk5NTg2NDU4YmJkMTBjODM0ODcyZGNjNjI=
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)

{
    "appId": "fdb8e4699586458bbd10c834872dcc62",
    "clientType": 72,
    "expireTime": 1627722929,
    "nonce": "EycLQsHwxhzK9OW8UEKWNfH2I3CGR2nINuU1EBpv162d42d92s",
    "userEmail": "******",
    "userId": "testuser@mycorp.com",
    "userName": "testuser",
    "userPhone": "173****9092"
}
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 
 "X-Envoy-Upstream-Service-Time": "230",
 "Server": "api-gateway",
 "X-Request-Id": "085d1f96cd9ddd6f3c50d70a0b2eb239",
 "X-Content-Type-Options": "nosniff",
 "Connection": "keep-alive",
 "X-Download-Options": "noopen",
 "Pragma": "No-cache",
 "Date": "Sat, 31 Jul 2021 06:18:07 GMT",
 "X-Frame-Options": "SAMEORIGIN",
 "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
 "Cache-Control": "no-cache",
 "X-Xss-Protection": "1; mode=block",
 "Content-Security-Policy": "connect-src 'self' *.huaweicloud.com ;style-src 'self' 'unsafe-inline' 'unsafe-eval';object-src 'self'; font-src 'self' data:;",
 "Expires": "Thu, 01 Jan 1970 00:00:00 GMT",
 "Content-Length": "1250",
 "Content-Type": "application/json"

{
    "accessToken":"cnr1316vcp2ceIkbfko3z13Y2J8UdioOw0ER4kTK",
    "tokenIp":"49.4.112.60",
    "validPeriod":56326,
    "expireTime":1627768613,
    "createTime":1627712287360,
    "user":{
        "realm":"huaweicloud.com",
        "userId":"53e2759d388e413abf6a56743a2694c5",
        "ucloginAccount":"Auto-53e2759d388e413abf6a56743a2694c5",
        "serviceAccount":"sip:+99111283523475338@huaweicloud.com",
        "numberHA1":"065eb94e5b090f70c77d4d1439f35b8e",
        "alias1":null,
        "companyId":"651543334",
        "spId":"8a8df0a174a1c6680174a26f578b0000",
        "companyDomain":null,
        "userType":2,
        "adminType":2,
        "name":"testuser@mycorp.com",
        "nameEn":"",
        "isBindPhone":null,
        "freeUser":false,
        "thirdAccount":"testuser@mycorp.com",
        "visionAccount":null,
        "headPictureUrl":null,
        "password":null,
        "status":0,
        "paidAccount":null,
        "paidPassword":null,
        "weLinkUser":false,
        "appId":"fdb8e4699586458bbd10c834872dcc62",
        "tr069Account":null,
        "corpType":5,
        "cloudUserId":"",
        "grayUser":true
    },
    "clientType":72,
    "forceLoginInd":null,
    "firstLogin":false,
    "pwdExpired":false,
    "daysPwdAvailable":-19678,
    "proxyToken":null,
    "tokenType":0,
    "refreshToken":"cnr13168neNyRDfomYEIci7zVjBBybZQG90fYdX2",
    "refreshValidPeriod":2592000,
    "refreshExpireTime":1630304287,
    "refreshCreateTime":1627712287360
}
```

## 错误码<a name="section111851469514"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -H 'content-type: application/json' -X POST  -H 'Content-Type: application/json,Accept-Language: zh-CN,X-Token-Type: LongTicket,Authorization: HMAC-SHA256 signature=3eca3f0f1e90ed55de38388066d02f1b7a86571a8ce30823af1df7c4edd7e086,access=ZmRiOGU0Njk5NTg2NDU4YmJkMTBjODM0ODcyZGNjNjI=' -d '{"appId": "fdb8e4699586458bbd10c834872dcc62","clientType": 72,"corpId": "807074304","expireTime": 1597824907000,"nonce": "EycLQsHwxhzK9OW8UEKWNfH2I3CGR2nINuU1EBpQ","userEmail": "******","userId": "alice@ent01","userName": "alice","userPhone": "173****9092"}' 'https://apigw.125339.com.cn/v2/usg/acs/auth/appauth'
```

