# 激活会议 - StartMeeting<a name="ZH-CN_TOPIC_0000001220016280"></a>

## 描述<a name="section698218449183"></a>

该接口用于通过会议ID和会议密码激活会议。所有的会控接口都需要在会议激活后才能调用，可以通过该接口先激活会议。

>![](public_sys-resources/icon-note.gif) **说明：** 
>来宾密码是否可以激活会议取决于会议创建时是否设置了“是否允许来宾启动会议”（allowGuestStartConf=true）。


## URI<a name="section379619558285"></a>

POST /v1/mmc/management/conferences/start

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| conferenceID | 是 | String | Body | 会议ID。 |
| password | 是 | String | Body | 会议密码。 |


## 状态码<a name="section109461801032"></a>

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

<a name="table187113520490"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| uuid | String | uuid。 说明： 废弃参数，请勿使用。 |
| regionIP | String | 会议所在区域的公网IP地址。 |


## 请求消息示例<a name="section11143759102417"></a>

```
POST /v1/mmc/management/conferences/start HTTP/1.1
Connection: keep-alive
X-Access-Token: *******
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)

{
    "conferenceID": "986030665",
    "password": "******"
}
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 OK
Content-Length: 141
Cache-Control: no-store
Connection: keep-alive
Content-Type: application/json
Date: Thu, 24 Dec 2020 06:25:59 GMT
Server: api-gateway
X-APIG-Latency: 261
X-APIG-Ratelimit-Api: remain:99,limit:100,time:1 minute
X-APIG-Ratelimit-Api-Allenv: remain:199,limit:200,time:1 second
X-APIG-Upstream-Latency: 259
X-Envoy-Upstream-Service-Time: 210
X-Request-Id: f991eeec77df1692c74f253d765ca146

{
	"uuid": "stb7fe307f8971e44acc5cf8be2112575ff8387ff6ddea68a5e",
	"regionIP": "100.94.23.40"
}
```

## 错误码<a name="section1358132410353"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -H 'content-type: application/json' -X POST -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' -d '{"conferenceID": "986030665","password": "******"}' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/start'
```

