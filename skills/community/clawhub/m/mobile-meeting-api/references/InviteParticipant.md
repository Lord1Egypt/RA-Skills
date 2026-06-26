# 邀请与会者 - InviteParticipant<a name="ZH-CN_TOPIC_0212714376"></a>

## 描述<a name="section698218449183"></a>

该接口用于邀请与会者加入会议。


## URI<a name="section148819213215"></a>

POST /v1/mmc/control/conferences/participants

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table476284317292"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| conferenceID | 是 | String | Query | 会议ID。 |
| X-Conference-Authorization | 是 | String | Header | 会控Token，通过 获取会控token 接口获得。 |
| attendees | 是 | Array of attendee objects | Body | 邀请的与会者列表。 |


**表 2**  attendee数据结构说明

<a name="table862782215199"></a>

| 参数 | 是否必须 | 类型 | 描述 |
|---|---|---|---|
| userUUID | 否 | String | 与会者的用户UUID。 |
| accountId | 否 | String | 与会者的移动会议账号。 |
| name | 是 | String | 与会者名称，长度限制为96个字符。 |
| role | 否 | Integer | 会议中的角色。默认为普通与会者。 0：普通与会者 1：会议主持人 |
| phone | 是 | String | 号码。支持SIP号码或者手机号码。 说明： 号码可以通过 查询企业通讯 接口录获取。返回的number是SIP号码，phone是手机号码 填SIP号码系统会呼叫对应的软终端或者硬终端；填手机号码系统会呼叫手机 呼叫手机需要开通PSTN权限，否则无法呼叫 |
| phone2 | 否 | String | 预留字段，取值类型同参数 “phone” 。 |
| phone3 | 否 | String | 预留字段，取值类型同参数 “phone” 。 |
| email | 否 | String | 邮件地址。 说明： 会中邀请不发会议通知，不用填写。 |
| sms | 否 | String | 短信通知的手机号码。 说明： 会中邀请不发会议通知，不用填写。 |
| type | 是 | String | 终端类型，类型枚举如下： normal：软终端 terminal：硬终端 outside：外部与会人 mobile：用户手机号码 ideahub：ideahub board: 电子白板（SmartRooms）。含Maxhub、海信大屏、IdeaHub B2 hwvision：华为智慧屏TV |
| deptUUID | 否 | String | 部门编码。 |
| deptName | 否 | String | 部门名称。 |


## 状态码<a name="section2836452597"></a>

**表 3**  状态码说明

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

## 请求消息示例<a name="section1498763918202"></a>

```
POST /v1/mmc/control/conferences/participants?conferenceID=914083136
Connection: keep-alive
X-Conference-Authorization:stbaf8fa2ea8a1b0e3ab2e007a85a75f88c55d5f6d5c1912dfb
Content-Type: application/json
user-agent: WeLink-desktop
Content-Length: 175
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)

{
    "attendees": [
    {
        "name": "上海分会场",
        "role": 1,
        "phone": "+8657*******",
        "type": "normal"
    }]
}
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 39
Connection: keep-alive
http_proxy_id: b77bb5478e0b1fc0dbbb4e8d4e26ba65
Server: api-gateway
X-Request-Id: 479fdc1d80e2e7ae19c4a08c28821822
```

## 错误码<a name="section2083618812462"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -H 'content-type: application/json' -X POST -H 'X-Conference-Authorization:stb39b3f21898d4972fed86b3f22ac70914a77303def15e126a' -d '{"attendees":[{"name":"user01","role":0,"phone":"+8657*******"}]}' https://apigw.125339.com.cn/v1/mmc/control/conferences/participants?conferenceID=914083136
```

