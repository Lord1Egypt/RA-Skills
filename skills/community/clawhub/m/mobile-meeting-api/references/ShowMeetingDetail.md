# 查询会议详情 - ShowMeetingDetail<a name="ZH-CN_TOPIC_0212714393"></a>

## 描述<a name="section698218449183"></a>

该接口用于查询指定会议的详情。

-   管理员可以查询本企业内所有会议的详情，普通用户仅能查询自己创建或者需要参加的会议详情。
-   只能查询尚未结束的会议（既正在召开的会议和已预约还未召开的会议）。如果需要查询历史会议列详情，请参考[查询历史会议详情 - ShowHisMeetingDetail](查询历史会议详情---ShowHisMeetingDetail.md)。


## URI<a name="section18941101622013"></a>

GET /v1/mmc/management/conferences/confDetail

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| conferenceID | 是 | String | Query | 会议ID。 说明： 创建会议时返回的conferenceID。不是vmrConferenceID。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。针对 PageParticipant 中的与会者分页。 |
| limit | 否 | Integer | Query | 查询数量。默认值20。 |
| searchKey | 否 | String | Query | 查询条件。长度限制为1-128个字符。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Type | 否 | Integer | Header | 默认值为0。 0：不区分终端和与会人 1：分页查询区分终端和与会人，结果合并返回 2：单独查询终端和与会人，结果单独返回 |
| X-Query-Type | 否 | Integer | Header | 当 “X-Type” “2” 时，有效。默认为0。 0：查询与会人 1：查询终端 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section3250161841314"></a>

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
| data | PageParticipant object | 与会者列表。 |


**表 4**  PageParticipant 数据结构

<a name="table17895153518491"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| limit | Integer | 每页的记录数。 |
| count | Integer | 总记录数。 |
| offset | Integer | 查询偏移量。 |
| data | Array of ParticipantInfo objects | 被邀请的与会者信息。包含预约会议时邀请的与会者和会中主持人邀请的与会者。 说明： 不返回会中主动加入的与会者信息。 |


**表 5**  ParticipantInfo 数据结构

<a name="table166381555145215"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| participantID | String | 与会者的号码。 |
| name | String | 与会者的名称。 |
| subscriberID | String | 与会者的号码（预留字段）。 |
| role | Integer | 与会者的角色。 1：会议主持人 0：普通与会者 |
| state | String | 用户状态。目前固定返回MEETTING。 |
| address | String | 终端所在会议室信息（预留字段）。 |
| attendeeType | String | 与会者终端类型。 “normal”：软终端。 “terminal”：会议室或硬终端。 “outside”：外部与会人。 “mobile”：用户手机号码。 |
| accountId | String | 与会者的账号。 如果是账号/密码鉴权场景，表示移动会议账号 如果是APP ID鉴权场景，表示第三方的User ID |
| phone2 | String | 预留字段。 |
| phone3 | String | 预留字段。 |
| email | String | 邮件地址。 |
| sms | String | 短信通知的手机号码。 |
| deptName | String | 部门名称。 |
| userUUID | String | 预订者的用户UUID。 |
| appId | String | App ID。参考“ App ID的申请 ”“ App ID的申请 ”。 |
| isAutoInvite | Integer | 会议开始时是否自动邀请该与会者。默认值由企业级配置决定。 0： 不自动邀请 1： 自动邀请 说明： 仅对并发会议资源的随机会议ID的会议生效。 |
| isNotOverlayPidName | Boolean | 是否不叠加会场名（VDC场景下适用）。 true：不叠加 false：叠加 |


## 请求消息示例<a name="section754195281617"></a>

-   请求示例（普通会议）

```
GET /v1/mmc/management/conferences/confDetail?conferenceID=914083136
Connection: keep-alive
X-Access-Token: stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)
```

-   请求示例（周期会议）

```
GET /v1/mmc/management/conferences/confDetail?conferenceID=969304019
Connection: keep-alive
X-Access-Token: stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC
user-agent: WeLink-desktop
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)
```

## 响应消息示例<a name="section339419481201"></a>

-   响应示例（普通会议）

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 1811
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: acf5bd2cc7c7f90fe7ab6b95a8c753d5
Server: api-gateway
X-Request-Id: e2bc0a1429cb2fd52db88ba6fa2c44a8

{
    "conferenceData": {
        "conferenceID": "914083136",
        "mediaTypes": "Voice,Data,Video",
        "subject": "user01的会议",
        "size": 1,
        "timeZoneID": "56",
        "startTime": "2019-12-18 07:28",
        "endTime": "2019-12-18 09:28",
        "conferenceState": "Created",
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
        "userUUID": "ff808081699b56cb0169be103500012b",
        "scheduserName": "user8002",
        "multiStreamFlag": 1,
        "conferenceType": 0,
        "confType": "IMMEDIATELY",
        "isAutoMute": 1,
        "isAutoRecord": 0,
        "chairJoinUri": "https://c.meeting.125339.com/#/j/914083136/6a30b8b5a325105da031442627828e496f91021ece36405f",
        "guestJoinUri": "https://c.meeting.125339.com/#/j/914083136/9505dc3349228b1ce0db8165590cc977bcff89785130fe0d",
        "recordType": 0,
        "recordAuxStream": 0,
        "confConfigInfo": {
            "isSendNotify": true,
            "isSendSms": true,
            "isAutoMute": true
        },
        "vmrFlag": 0,
        "scheduleVmr": false,
        "isHasRecordFile": false,
        "partAttendeeInfo": [
            {
                "phone": "+99111****815",
                "name": "user01",
                "type": "normal"
            }
        ],
        "terminlCount": 0,
        "normalCount": 1,
        "deptName": "wangyue",
        "confUUID": "050c7898216811eaa6958bf3bb9ac167"
    },
    "data": {
        "offset": 0,
        "limit": 20,
        "count": 1,
        "data": [
            {
                "participantID": "+991116003815",
                "name": "user01",
                "role": 0,
                "state": "MEETTING",
                "attendeeType": "normal",
                "accountId": "user01"
            }
        ]
    }
}
```

-   响应示例（周期会议）

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 1811
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: acf5bd2cc7c7f90fe7ab6b95a8c753d5
Server: api-gateway
X-Request-Id: e2bc0a1429cb2fd52db88ba6fa2c44a8

{
    "conferenceData": {
        "conferenceID": "969304019",
        "mediaTypes": "Voice,Data,Video",
        "subject": "user01的会议",
        "size": 1,
        "timeZoneID": "56",
        "startTime": "2019-12-18 07:28",
        "endTime": "2019-12-18 09:28",
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
        "userUUID": "ff808081699b56cb0169be103500012b",
        "scheduserName": "user8002",
        "multiStreamFlag": 1,
        "conferenceType": 2,
        "confType": "CYCLE",
        "cycleParams": {
            "startDate": "2019-12-18",
            "cycle": "Day",
            "endDate": "2019-12-19",
           "interval": 1
        },
        "isAutoMute": 1,
        "isAutoRecord": 0,
        "chairJoinUri": "https://c.meeting.125339.com/#/j/914083136/6a30b8b5a325105da031442627828e496f91021ece36405f",
        "guestJoinUri": "https://c.meeting.125339.com/#/j/914083136/9505dc3349228b1ce0db8165590cc977bcff89785130fe0d",
        "recordType": 0,
        "recordAuxStream": 0,
        "confConfigInfo": {
            "isSendNotify": true,
            "isSendSms": true,
            "isAutoMute": true
        },
        "vmrFlag": 0,
        "scheduleVmr": false,
        "subConfs": [
           {
              "cycleSubConfID": "84bfd3816e744b81a02d76a5537a49dc",
              "conferenceID": "969304019",
              "mediaType": "Voice,Data,HDVideo",
              "startTime": "2019-12-18 07:28",
              "endTime": "2019-12-18 09:28",
              "isAutoRecord": 0,
              "confConfigInfo": {
                  "callInRestriction": 0,
                  "audienceCallInRestriction": 0,
                  "allowGuestStartConf": true,
                  "joinBeforeHostTime": 0,
                  "enableWaitingRoom": true
              }
            },
           {
              "cycleSubConfID": "2e447d1e012c49d9b682ea6af73b6fa6",
              "conferenceID": "969304019",
              "mediaType": "Voice,Data,HDVideo",
              "startTime": "2019-12-18 07:28",
              "endTime": "2019-12-18 09:28",
              "isAutoRecord": 0,
              "confConfigInfo": {
                  "callInRestriction": 0,
                  "audienceCallInRestriction": 0,
                  "allowGuestStartConf": true,
                  "joinBeforeHostTime": 0,
                  "enableWaitingRoom": true
              }
          }],
        "isHasRecordFile": false,
        "partAttendeeInfo": [
            {
                "phone": "+99111****815",
                "name": "user01",
                "type": "normal"
            }
        ],
        "terminlCount": 0,
        "normalCount": 1,
        "deptName": "wangyue",
        "confUUID": "050c7898216811eaa6958bf3bb9ac167"
    },
    "data": {
        "offset": 0,
        "limit": 20,
        "count": 1,
        "data": [
            {
                "participantID": "+991116003815",
                "name": "user01",
                "role": 0,
                "state": "MEETTING",
                "attendeeType": "normal",
                "accountId": "user01"
            }
        ]
    }
}
```

## 错误码<a name="section1451618557175"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' 'https://apigw.125339.com.cn/v1/mmc/management/conferences/confDetail?conferenceID=914083136'
```

