# 查询历史会议列表 - SearchHisMeetings<a name="ZH-CN_TOPIC_0212714401"></a>

## 描述<a name="section17948858131615"></a>

该接口用于查询已经结束的会议。管理员可以查询本企业内所有的历史会议，普通用户仅能查询自己创建或者被邀请的历史会议。不带查询参数时，默认查询权限范围内的历史会议。

>![](public_sys-resources/icon-note.gif) **说明：** 
>-   普通用户如果只是通过会议ID或者会议链接接入会议，不是预定者会前邀请或者会中主持人邀请的，则历史会议中无法查到
>-   如果同一个会议召开并结束多次，则会产生多条历史会议（会议ID相同，会议UUID不同）
>-   历史会议记录默认保留6个月，最长保留12个月。保留时间管理员可在“会议设置”的“历史会议留存时间”中修改


## URI<a name="section1392764619274"></a>

GET /v1/mmc/management/conferences/history

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| userUUID | 否 | string | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。 |
| limit | 否 | Integer | Query | 查询数量。默认是20，最大500条。 |
| searchKey | 否 | string | Query | 查询条件。会议主题、会议预约人和会议ID等可作为搜索内容。 |
| scheduledUUID | 否 | string | Query | 预约会议的UUID |
| queryAll | 否 | Boolean | Query | 是否查询企业下所有用户的历史会议。 true：查询所有用户的历史会议 false：仅查询管理员自己的历史会议 说明： 仅对企业管理员生效。 |
| startDate | 是 | long | Query | 查询的起始时间戳（单位毫秒）。 |
| endDate | 是 | long | Query | 查询的截止时间戳（单位毫秒）。 |
| sortType | 否 | String | Query | 查询结果排序类型。 ASC_StartTIME：根据会议开始时间升序排序 DSC_StartTIME：根据会议开始时间降序排序 ASC_RecordTYPE：根据是否具有录播文件排序，之后默认按照会议开始时间升序排序 DSC_RecordTYPE：根据是否含有录播文件排序，之后默认按照会议开始时间降序排序 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section11547950134517"></a>

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
| offset | Integer | 查询偏移量。 |
| limit | Integer | 每页的记录数。 |
| count | Integer | 总记录数。 |
| data | Array of ConferenceInfo objects | 会议列表。 |


## 请求消息示例<a name="section1498763918202"></a>

```
GET /v1/mmc/management/conferences/history?startDate=1574092800000&endDate=1574179199999
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
Content-Length: 2420
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: 43bee1151af8115d90358994a7c14cfc
Server: api-gateway
X-Request-Id: 53c883710d86aebf01e92ce7bcea1984

{
    "data": [
        {
            "conferenceID": "914083388",
            "mediaTypes": "Voice,Video,Data",
            "subject": "user8001测试会议",
            "size": 1,
            "timeZoneID": "56",
            "startTime": "2019-11-18 23:31",
            "endTime": "2019-11-18 23:32",
            "conferenceState": "Destroyed",
            "accessNumber": "+991117",
            "language": "zh-CN",
            "passwordEntry": [
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
            "deptName": "wangyue",
            "confUUID": "9a0fa6d10a5b11eaae5e191763c22c0e"
        },
        {
            "conferenceID": "914088193",
            "mediaTypes": "Voice,Video,Data",
            "subject": "user8001的会议",
            "size": 1,
            "timeZoneID": "56",
            "startTime": "2019-11-18 23:31",
            "endTime": "2019-11-18 23:31",
            "conferenceState": "Destroyed",
            "accessNumber": "+991117",
            "language": "zh-CN",
            "passwordEntry": [
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
            "guestJoinUri": "https://c.meeting.125339.com/#/j/914088193/5b00be0e5121eb2f6f865162a4bc7f1f7f05d37cd802dded",
            "recordType": 2,
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
                    "phone": "+991116004380",
                    "name": "user8002",
                    "type": "normal"
                }
            ],
            "terminlCount": 0,
            "normalCount": 1,
            "deptName": "wangyue",
            "confUUID": "7c421ac60a5b11eaa5e83b30677ab12b"
        },
        {
            "conferenceID": "914085971",
            "mediaTypes": "Voice,Video,Data",
            "subject": "user8001的会议",
            "size": 1,
            "timeZoneID": "56",
            "startTime": "2019-11-18 23:30",
            "endTime": "2019-11-18 23:31",
            "conferenceState": "Destroyed",
            "accessNumber": "+991117",
            "language": "zh-CN",
            "passwordEntry": [
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
            "guestJoinUri": "https://c.meeting.125339.com/#/j/914085971/40300b325ad71ad1ff2c1dbdda1250328ccd8ec9ff45bd03",
            "recordType": 2,
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
            "deptName": "wangyue",
            "confUUID": "6d2a6cd90a5b11eaa5e8f14973e50d03"
        }
    ],
    "offset": 0,
    "limit": 20,
    "count": 3
}
```

## 错误码<a name="section10417115102813"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section4952152111818"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/history?startDate=1574092800000&endDate=1574179199999'
```

