# 批量删除录制 - DeleteRecordings<a name="ZH-CN_TOPIC_0212714572"></a>

## 描述<a name="section698218449183"></a>

该接口用于批量删除会议的录制。


## URI<a name="section1331211304272"></a>

DELETE /v1/mmc/management/record/files

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| confUUIDs | 是 | String | Query | 会议UUID列表，多个会议UUID之间以英文逗号隔开。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section15337174804411"></a>

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

无

## 请求消息示例<a name="section11143759102417"></a>

```
DELETE /v1/mmc/management/record/files?confUUIDs=51adf610220411eaaae03f22d33cc26b
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
Content-Length: 39
Connection: keep-alive
http_proxy_id: 91e7ab61cb9d601d27d7d6d6490e7eee
Server: api-gateway
X-Request-Id: 0f01f95bf9c4b4235226d93c19f42396
```

## 错误码<a name="section1779215942712"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -X DELETE -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' https://apigw.125339.com.cn/v1/mmc/management/record/files?confUUIDs=51adf610220411eaaae03f22d33cc26b
```

