# 编辑预约会议 - UpdateMeeting<a name="ZH-CN_TOPIC_0212714519"></a>

## 描述<a name="section698218449183"></a>

该接口用于修改已预约的会议。会议开始后，不能被修改。


## URI<a name="section5402174021111"></a>

PUT /v1/mmc/management/conferences

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1065133153514"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| conferenceID | 是 | String | Query | 会议ID。 说明： 创建会议时返回的conferenceID。不是vmrConferenceID。 |
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |
| conferenceType | 否 | Integer | Body | 创建会议类型（默认为普通会议）。 0 : 普通会议。 1：周期会议，此时 “cycleParams” 必须填写。 |
| startTime | 否 | String | Body | 会议开始时间（UTC时间）。格式：yyyy-MM-dd HH:mm。 说明： 如果没有指定开始时间或填空串，则表示会议马上开始 时间是UTC时间，即0时区的时间 |
| length | 否 | Integer | Body | 会议持续时长，单位分钟。默认30分钟。 最大1440分钟（24小时），最小15分钟。 |
| subject | 否 | String | Body | 会议主题。长度限制为128个字符。 |
| mediaTypes | 是 | String | Body | 会议的媒体类型。 Voice：语音会议 HDVideo：视频会议 |
| groupuri | 否 | String | Body | 软终端创建即时会议时在当前字段带临时群组ID，由服务器在邀请其他与会者时在或者conference-info头域中携带。 长度限制为31个字符。 |
| attendees | 否 | Array of Attendee objects | Body | 与会者列表。 |
| cycleParams | 否 | CycleParams object | Body | 周期会议的参数，当会议是周期会议的时候该参数必须填写。 |
| isAutoRecord | 否 | Integer | Body | 会议是否自动启动录制，在录播类型为：录播、录播+直播时才生效。默认为不自动启动。 1：自动启动录制 0：不自动启动录制 |
| encryptMode | 否 | Integer | Body | 会议媒体加密模式。默认值由企业级的配置填充。 0：自适应加密 1 : 强制加密 2 : 不加密 |
| language | 否 | String | Body | 会议通知短信或邮件的语言。默认中文。 zh-CN：中文 en-US：英文 |
| timeZoneID | 否 | String | Body | 会议通知中会议时间的时区信息。时区信息，参考 时区映射关系 。 说明： 举例：“timeZoneID”:"26"，则通过移动会议发送的会议通知中的时间将会标记为如“2021/11/11 星期四 00:00 - 02:00 (GMT) 格林威治标准时间:都柏林, 爱丁堡, 里斯本, 伦敦”。 非周期会议，如果会议通知是通过第三方系统发送，则这个字段不用填写。 |
| recordType | 否 | Integer | Body | 录播类型。默认为禁用。 0: 禁用 1: 直播 2: 录播 3: 直播+录播 |
| liveAddress | 否 | String | Body | 主流直播推流地址，在录播类型为 :直播、直播+录播时有效。最大不超过255个字符。 |
| auxAddress | 否 | String | Body | 辅流直播推流地址，在录播类型为 :直播、直播+录播时有效。最大不超过255个字符。 |
| recordAuxStream | 否 | Integer | Body | 是否录制辅流，在录播类型为：录播、录播+直播时有效。默认只录制视频主流，不录制辅流。 0：不录制 1：录制 |
| confConfigInfo | 否 | ConfConfigInfo object | Body | 会议其他配置信息。 |
| recordAuthType | 否 | Integer | Body | 录播观看鉴权方式，在录播类型为:录播、直播+录播时有效。 0：可通过链接观看/下载 1：企业用户可观看/下载 2：与会者可观看/下载 |
| vmrFlag | 否 | Integer | Body | 是否使用云会议室召开预约会议。默认不使用云会议室。 0：不使用云会议室 1：使用云会议室 说明： vmrFlag不支持修改。 |
| vmrID | 否 | String | Body | 绑定给当前创会账号的VMR ID。通过 查询云会议室及个人会议ID 接口获取。 说明： vmrID取上述查询接口中返回的id，不是vmrId。 创建个人会议ID的会议时，使用vmrMode=0的VMR；创建云会议室的会议时，使用vmrMode=1的VMR vmrID不支持修改。 |
| concurrentParticipants | 否 | Integer | Body | 会议方数，会议最大与会人数限制。 0：无限制 大于0：会议最大与会人数 |
| supportSimultaneousInterpretation | 否 | Boolean | Body | 会议是否支持同声传译 true：支持 false：不支持 |
| confResType | 否 | Integer | Body | 会议资源类型,此参数创建后不支持修改: 0: 并发 1: 云会议室 2: 网络研讨会 3: 预留模式,暂未开放 |


## 状态码<a name="section79356216109"></a>

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
| [数组元素] | Array of ConferenceInfo | 会议信息列表。 |


## 请求消息示例<a name="section1498763918202"></a>

```
PUT /v1/mmc/management/conferences?conferenceID=914087436
Connection: keep-alive
X-Access-Token: stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC
Content-Type: application/json
user-agent: WeLink-desktop
Content-Length: 372
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)

{
    "mediaTypes": "HDVideo",
    "startTime": "2022-08-30 12:00",
    "length": 120,
    "attendees": [
        {
            "accountId": "zhangshan@125339.com.cn",
            "appId": "caaab5a3e584497990f6a9b582a0ae42"
        }
    ],
    "subject": "例行会议"
}
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 1157
Connection: keep-alive
http_proxy_id: 462abfcfa8a41c2c5450eb7648bf5ad2
Server: api-gateway
X-Request-Id: 7ba6f742610c03a64262b126fb336a5d

[
{
        "conferenceID": "914673889",
        "mediaTypes": "Data,Voice,HDVideo",
        "subject": "例行会议",
        "size": 1,
        "timeZoneID": "56",
        "startTime": "2022-08-30 12:00",
        "endTime": "2022-08-30 13:00",
        "conferenceState": "Schedule",
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
        "userUUID": "ff80808167ef1edf0167f339533d05a6",
        "scheduserName": "金秘书",
        "conferenceType": 0,
        "confType": "FUTURE",
        "isAutoMute": 1,
        "isAutoRecord": 0,
        "chairJoinUri": "https://c.meeting.125339.com/#/j/914673889/6a30b8b5a325105da031442627828e496f91021ece36405f",
        "guestJoinUri": "https://c.meeting.125339.com/#/j/914673889/9505dc3349228b1ce0db8165590cc977bcff89785130fe0d",
        "recordType": 2,
        "confConfigInfo": {  
            "isSendNotify": false,
            "isSendSms": false,
            "isAutoMute": true
        },
        "vmrFlag": 0,
        "partAttendeeInfo": [
            {
                "phone": "+99111********4158",
                "name": "张三",               
                "type": "normal"
            }
        ],
        "terminlCount": 0,
        "normalCount": 1,
        "deptName": "企业协同云服务项目群"
    }
]
```

## 错误码<a name="section69831715181215"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -H 'content-type: application/json' -X PUT -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' -d '{"mediaTypes": "Voice","attendees": [{"name": "user02","role": 1,"phone": "+8657*******"}],"conferenceType": "0","subject": "user02 conference"}' 'https://apigw.125339.com.cn/v1/mmc/management/conferences?conferenceID=914087436'
```

