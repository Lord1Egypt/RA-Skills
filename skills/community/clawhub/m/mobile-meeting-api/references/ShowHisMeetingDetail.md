# 查询历史会议详情 - ShowHisMeetingDetail<a name="ZH-CN_TOPIC_0212714501"></a>

## 描述<a name="section17948858131615"></a>

该接口用户查询指定历史会议的详情。管理员可以查询本企业内所有的历史会议详情，普通用户仅能查询自己创建或者被邀请的历史会议详情。


## URI<a name="section1392764619274"></a>

GET /v1/mmc/management/conferences/history/confDetail

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| confUUID | 是 | String | Query | 会议UUID。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。针对 PageParticipant 中的与会者分页。 |
| limit | 否 | Integer | Query | 查询数量。默认值20。 |
| searchKey | 否 | String | Query | 查询条件 。会议主题、会议预约人和会议ID等可作为搜索内容。长度限制为1-128个字符。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Type | 否 | Integer | Header | 默认值为0。 0：不区分会议室和与会人。 1：分页查询区分会议室和与会人，结果合并返回。 2：单独查询会议室与与会人，结果也是单独返回。 |
| X-Query-Type | 否 | Integer | Header | 当 “X-Type” 为 “2” 时，该字段有效。默认值为 “0” 。 0：查询与会人。 1：查询终端。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section18795183024715"></a>

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

<a name="table4990175112163"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| conferenceData | ConferenceInfo object | 会议信息。 |
| data | PageParticipant object | 被邀请的与会者信息。包含预约会议时邀请的与会者。 说明： 不返回会中主动加入的与会者信息。 |


## 请求消息示例<a name="section1498763918202"></a>

```
GET /v1/mmc/management/conferences/history/confDetail?confUUID=9a0fa6d10a5b11eaae5e191763c22c0e
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
Content-Length: 1816
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: b74350ba75078e9ad1ec3610f2ec5550
Server: api-gateway
X-Request-Id: e71ece483fad1f909dd45c796af8360

{
    "conferenceData": {
        "conferenceID": "914083388",
        "mediaTypes": "Data,Voice,Video",
        "subject": "user8001测试会议",
        "size": 1,
        "timeZoneID": "56",
        "startTime": "2019-11-18 23:31",
        "endTime": "2019-11-18 23:32",
        "accessNumber": "+991117",
        "language": "zh-CN",
        "passwordEntry": [
            {
                "conferenceRole": "chair",
                "password": "******"
            },
            {
                "conferenceRole": "general",
                "password": "******"
            }
        ],
        "userUUID": "ff8080816a024f05016a4e2342480a60",
        "scheduserName": "test008",
        "multiStreamFlag": 1,
        "conferenceType": 0,
        "confType": "IMMEDIATELY",
        "isAutoMute": 1,
        "isAutoRecord": 0,
        "chairJoinUri": "https://c.meeting.125339.com/#/j/914083388/69a5b84756d19dc9a222805819ec68945f8d86369d966d43",
        "guestJoinUri": "https://c.meeting.125339.com/#/j/914083388/1f215673e636444b55845ee1d1af630e8d8ca0235e491972",
        "recordType": 0,
        "recordAuxStream": 0,
        "recordAuthType": 0,
        "confConfigInfo": {
            "prolongLength": 15,
            "isGuestFreePwd": false,
            "isSendNotify": true,
            "isSendSms": true,
            "isAutoMute": true,
            "isSendCalendar": true,
            "callInRestriction": 0,
            "allowGuestStartConf": true,
            "isHardTerminalAutoMute": true,
            "enableWaitingRoom": true
        },
        "vmrFlag": 0,
        "scheduleVmr": false,
        "isHasRecordFile": false,
        "partAttendeeInfo": [
            {
                "phone": "+99111****380",
                "name": "user8002",
                "type": "normal"
            }
        ],
        "terminlCount": 0,
        "normalCount": 1,
        "deptName": "wangyue"
    },
    "data": {
        "offset": 0,
        "limit": 20,
        "count": 1,
        "data": [
            {
                "participantID": "+991116004380",
                "name": "user8002",
                "role": 1,
                "state": "MEETTING",
                "attendeeType": "normal",
                "accountId": "user8002@corpnew",
                "sms": "+8612*****5965",
                "deptName": "wangyue",
                "userUUID": "ff808081699b56cb0169be103500012b"
            }
        ]
    }
}
```

## 错误码<a name="section11516235143011"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section4952152111818"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/history/confDetail?confUUID=9a0fa6d10a5b11eaae5e191763c22c0e'
```

