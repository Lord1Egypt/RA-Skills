# 查询会议列表 - SearchMeetings<a name="ZH-CN_TOPIC_0212714510"></a>

## 描述<a name="section698218449183"></a>

该接口用于查询尚未结束的会议。

-   管理员可以查询本企业内所有的会议，普通用户仅能查询自己创建或者需要参加的会议。不带查询参数时，默认查询权限范围内正在召开或还未召开的会议。
-   只能查询尚未结束的会议（既正在召开的会议和已预约还未召开的会议）。如果需要查询历史会议列表，请参考[查询历史会议列表 - SearchHisMeetings](查询历史会议列表---SearchHisMeetings.md)。


## URI<a name="section1228394174"></a>

GET /v1/mmc/management/conferences

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table1285113481520"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| userUUID | 否 | String | Query | 用户的UUID。 说明： 仅管理员有权限查询本企业其他用户的会议列表；普通账号该字段无效，只能查询自己的。 |
| offset | 否 | Integer | Query | 查询偏移量。默认为0。 |
| limit | 否 | Integer | Query | 查询数量。默认是20，最大500条。 |
| queryAll | 否 | Boolean | Query | 是否查询企业下所有用户的会议记录。默认值为false。 true：查询所有用户的会议 false：仅查询管理员自己创建的会议 说明： 仅对企业管理员生效。 |
| searchKey | 否 | String | Query | 查询条件 。会议主题、会议预约人和会议ID等可作为搜索内容。长度限制为1-128个字符。 |
| queryConfMode | 否 | String | Query | 查询时间范围。 ADAY：一天 AWEEK：一周 AMONTH：一个月 ALL：查询所有 |
| sortType | 否 | String | Query | 查询结果排序。 ASC_StartTIME：按会议开始时间升序排序 DSC_StartTIME：按会议开始时间降序排序 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |


## 状态码<a name="section9243191618122"></a>

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
GET /v1/mmc/management/conferences
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
Content-Length: 2450
Connection: keep-alive
Expires: 0
Pragma: No-cache
Cache-Control: no-cache
http_proxy_id: 6fba0eff9f832b463580fb06c5b0ff9c
Server: api-gateway
X-Request-Id: ac9f75ec3c97c823f128526a924532b2

{
    "data": [
        {
            "conferenceID": "914083136",
            "mediaTypes": "Data,Video,Voice",
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
                    "phone": "+99111*****815",
                    "name": "user01",
                    "role": 0,
                    "isMute": 0,
                    "type": "normal"
                }
            ],
            "terminlCount": 0,
            "normalCount": 1,
            "deptName": "wangyue",
            "confUUID": "050c7898216811eaa6958bf3bb9ac167"
        }
    ],
    "offset": 0,
    "limit": 20,
    "count": 1
}
```

## 错误码<a name="section7638934101419"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -X GET -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' https://apigw.125339.com.cn/v1/mmc/management/conferences
```

