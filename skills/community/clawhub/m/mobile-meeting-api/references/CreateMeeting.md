# 创建会议 - CreateMeeting<a name="ZH-CN_TOPIC_0212714557"></a>

## 描述<a name="section698218449183"></a>

该接口用于创建立即会议和预约会议。


## URI<a name="section1822710121015"></a>

POST /v1/mmc/management/conferences

## 请求参数<a name="section1997124142020"></a>

**表 1**  参数说明

<a name="table958712610276"></a>

| 参数 | 是否必须 | 类型 | 位置 | 描述 |
|---|---|---|---|---|
| userUUID | 否 | String | Query | 用户的UUID。 说明： 该参数将废弃，请勿使用。 |
| X-Access-Token | 是 | String | Header | 授权令牌。获取“ 执行App ID鉴权 ”响应的accessToken。 |
| X-Authorization-Type | 否 | String | Header | 标识是否为第三方portal过来的请求。 说明： 该参数将废弃，请勿使用。 |
| X-Site-Id | 否 | String | Header | 用于区分到哪个HCSO站点鉴权。 说明： 该参数将废弃，请勿使用。 |
| startTime | 否 | String | Body | 会议开始时间（UTC时间）。格式：yyyy-MM-dd HH:mm。 说明： 创建预约会议时，如果没有指定开始时间或填空串，则表示会议马上开始 时间是UTC时间，即0时区的时间 |
| length | 否 | Integer | Body | 会议持续时长，单位分钟。默认30分钟。 最大1440分钟（24小时），最小15分钟。 |
| subject | 否 | String | Body | 会议主题。最多128个字符。 |
| mediaTypes | 是 | String | Body | 会议的媒体类型。 Voice：语音会议 HDVideo：视频会议 |
| groupuri | 否 | String | Body | 软终端创建即时会议时在当前字段带临时群组ID，由服务器在邀请其他与会者时在或者conference-info头域中携带。 长度限制为31个字符。 |
| attendees | 否 | Array of Attendee objects | Body | 与会者列表。 |
| cycleParams | 否 | CycleParams object | Body | 周期会议的参数，当会议是周期会议的时候该参数必须填写。 |
| isAutoRecord | 否 | Integer | Body | 会议是否自动启动录制，在录播类型为：录播、录播+直播时才生效。默认为不自动启动。 1：自动启动录制 0：不自动启动录制 |
| encryptMode | 否 | Integer | Body | 会议媒体加密模式。默认值由企业级的配置填充。 0：自适应加密 1 : 强制加密 2 : 不加密 |
| language | 否 | String | Body | 会议通知短信或邮件的语言。默认中文。 zh-CN：中文 en-US：英文 |
| timeZoneID | 否 | String | Body | 会议通知中会议时间的时区信息。时区信息，参考 时区映射关系 。 说明： 举例：“timeZoneID”:"26"，则通过移动会议发送的会议通知中的时间将会标记为如“2021/11/11 星期四 00:00 - 02:00 (GMT) 格林威治标准时间:都柏林, 爱丁堡, 里斯本, 伦敦”。 非周期会议，如果会议通知是通过第三方系统发送，则这个字段不用填写。 |
| recordType | 否 | Integer | Body | 录播类型。默认为禁用。 0: 禁用 1: 直播 2: 录播 3: 直播+录播 说明： 当录播类型含有直播属性（recordType为1或3），则liveAddress或者auxAddress至少填一个，否则会中无直播功能。 |
| liveAddress | 否 | String | Body | 主流直播推流地址，在录播类型为 :直播、直播+录播时有效。最大不超过255个字符。 |
| auxAddress | 否 | String | Body | 辅流直播推流地址，在录播类型为 :直播、直播+录播时有效。最大不超过255个字符。 |
| recordAuxStream | 否 | Integer | Body | 是否录制辅流，在录播类型为：录播、录播+直播时有效。默认只录制视频主流，不录制辅流。 0：不录制 1：录制 |
| confConfigInfo | 否 | ConfConfigInfo object | Body | 会议其他配置信息。 |
| recordAuthType | 否 | Integer | Body | 录播观看鉴权方式，在录播类型为:录播、直播+录播时有效。 0：可通过链接观看/下载 1：企业用户可观看/下载 2：与会者可观看/下载 |
| vmrFlag | 否 | Integer | Body | 是否使用云会议室或者个人会议ID召开预约会议。默认0。 0：不使用云会议室或者个人会议ID 1：使用云会议室或者个人会议ID |
| vmrID | 否 | String | Body | 绑定给当前创会账号的VMR ID。通过 查询云会议室及个人会议ID 接口获取。 说明： vmrID取上述查询接口中返回的id，不是vmrId 创建个人会议ID的会议时，使用vmrMode=0的VMR；创建云会议室的会议时，使用vmrMode=1的VMR vmrID使用个人会议ID占用并发资源，使用云会议室ID占用云会议室资源；vmrID既不使用个人会议ID也不使用云会议室ID（vmrflag=0，vmrID=null）占用并发资源 |
| concurrentParticipants | 否 | Integer | Body | 会议方数，会议最大与会人数限制。 0：无限制 大于0：会议最大与会人数 |
| supportSimultaneousInterpretation | 否 | Boolean | Body | 会议是否支持同声传译 true：支持 false：不支持 |
| confResType | 否 | Integer | Body | 会议资源类型,此参数创建后不支持修改: 0: 并发 1: 云会议室 2: 网络研讨会 3: 预留模式,暂未开放 |


**表 2**  Attendee 数据结构

<a name="table862782215199"></a>

| 参数 | 是否必须 | 类型 | 描述 |
|---|---|---|---|
| userUUID | 否 | String | 与会者的用户UUID。 |
| accountId | 否 | String | 与会者的账号。 如果是账号/密码鉴权场景: 选填，表示移动会议账号ID 如果是APP ID鉴权场景：必填，表示第三方的User ID，同时需要携带参数appId |
| appId | 否 | String | App ID。如果是APP ID鉴权场景，此项必填。参考“ App ID的申请 ”“ App ID的申请 ”。 |
| name | 否 | String | 与会者名称。长度限制为96个字符。 |
| role | 否 | Integer | 会议中的角色。默认为普通与会者。 0：普通与会者 1：会议主持人 |
| phone | 否 | String | 号码。支持SIP号码或者手机号码。 如果是账号/密码鉴权场景：必填 如果是APP ID鉴权场景：选填 说明： 号码可以通过 查询企业通讯 接口录获取。返回的number是SIP号码，phone是手机号码 填SIP号码系统会呼叫对应的软终端或者硬终端；填手机号码系统会呼叫手机 呼叫手机需要开通PSTN权限，否则无法呼叫 |
| phone2 | 否 | String | 预留字段，取值类型同参数 “phone” 。 |
| phone3 | 否 | String | 预留字段，取值类型同参数 “phone” 。 |
| email | 否 | String | 邮件地址。需要发邮件通知时填写。 |
| sms | 否 | String | 短信通知的手机号码。需要发短信通知时填写。 |
| isMute | 否 | Integer | 用户入会时是否需要自动静音 。默认不静音。 0： 不需要静音 1： 需要静音 说明： 仅会中邀请与会者时才生效。 |
| isAutoInvite | 否 | Integer | 会议开始时是否自动邀请该与会者。默认值由企业级配置决定。 0：不自动邀请。 1：自动邀请。 说明： 仅并发会议资源的随机会议ID会议才生效。 |
| type | 否 | String | 终端类型，类型枚举如下： normal：软终端 terminal：硬终端 outside：外部与会人 mobile：用户手机号码 ideahub：ideahub board: 电子白板（SmartRooms），含Maxhub、海信大屏、IdeaHub B2 hwvision：华为智慧屏TV customnumber： 自定义呼叫号码(包括级联会议号、手机号码、硬终端SIP号码等) |
| address | 否 | String | 预留字段，终端所在会议室信息。 |
| deptUUID | 否 | String | 部门ID。 |
| deptName | 否 | String | 部门名称。最大不超过128个字符。 |
| uniqueType | 否 | Integer | 企业内唯一会场标识, 0标识为普通与会者，1标识为企业内唯一会场 说明： 创建级联会议时，uniqueType 为1， 同时type为customnumber |


**表 3**  CycleParams 数据结构

<a name="table977474913540"></a>

| 参数 | 是否必须 | 类型 | 描述 |
|---|---|---|---|
| startDate | 是 | String | 周期会议的开始日期，格式：YYYY-MM-DD。 开始日期不能早于当前日期。 说明： 日期是timeZoneID指定的时区的日期，非UTC时间的日期。 |
| endDate | 是 | String | 周期会议的结束日期，格式：YYYY-MM-DD。 开始日期和结束日期间的时间间隔最长不能超过1年。开始日期和结束日期之间最多允许50个子会议，若超过50个子会议，会自动调整结束日期。 说明： 日期是timeZoneID指定的时区的日期，非UTC时间的日期。 |
| cycle | 是 | String | 周期类型。 Day：天 Week：星期 Month：月 |
| interval | 否 | Integer | 子会议间隔。 “cycle” 选择了 “Day” ，表示每几天召开一次，取值范围[1,15] “cycle” 选择了 “Week” ，表示每几周召开一次，取值范围[1,5] “cycle” 选择了 “Month” ，Interval表示隔几月，取值范围[1,3] |
| point | 否 | Array of integers | 周期内的会议召开点。仅当按周和月时有效。 “cycle” 选择了 “Week” ，point中填入了两个元素1和3，则表示每个周一和周三召开会议，0表示周日 “cycle” 选择了 “Month” ，point中填入了12和20则表示每个月的12号和20号召开会议，取值范围为[1,31]，若当月没有该值，则为月末 |
| preRemindDays | 是 | Integer | 提前通知天数。所有与会者在每个子会议开始前N天收到会议通知。取值范围[0,30]。 默认值是1。 |


**表 4**  ConfConfigInfo 数据结构

<a name="table193021239133"></a>

| 参数 | 是否必须 | 类型 | 描述 |
|---|---|---|---|
| isSendNotify | 否 | Boolean | 是否需要发送会议邮件通知。默认值由企业级配置决定。 true：需要 false：不需要 |
| isSendSms | 否 | Boolean | 是否需要发送会议短信通知。 true：需要 false：不需要 说明： 保留字段，暂不提供短信通知能力。 |
| isSendCalendar | 否 | Boolean | 是否需要发送会议邮件日历通知。默认值由企业级配置决定。 true：需要 false：不需要 |
| isAutoMute | 否 | Boolean | 来宾入会，软终端是否自动静音。默认值由企业级配置决定。 true：自动静音 false：不自动静音 |
| isHardTerminalAutoMute | 否 | Boolean | 来宾入会，硬终端是否自动静音。默认值由企业级配置决定。 true：自动静音 false：不自动静音 |
| isGuestFreePwd | 否 | Boolean | 是否来宾免密。 true：免密 false：需要密码 说明： 仅随机会议ID的会议生效。 |
| callInRestriction | 否 | Integer | 允许加入会议的范围。 0：所有用户 2：企业内用户 3：被邀请用户 |
| allowGuestStartConf | 否 | Boolean | 是否允许来宾启动会议。 true：允许来宾启动会议 false：禁止来宾启动会议 说明： 仅随机会议ID的会议生效。 |
| guestPwd | 否 | String | 来宾密码（4-16位长度的纯数字）。 |
| vmrIDType | 否 | Integer | 云会议室的会议ID模式。 0：固定会议ID 1：随机会议ID |
| prolongLength | 否 | Integer | 自动延长会议时长（取值范围0-60）。 0：表示会议到点自动结束，不延长会议。 其他：表示自动延长的时长。 说明： 自动结束会议是按照会议时长计算。比如预定的会议是9:00开始11:00结束，会议时长2个小时，如果与会者8:00就加入会议了，那会议在10:00就会自动结束 设置成其他值时，只要会中还有与会者，会议自动多次延长 |
| enableWaitingRoom | 否 | Boolean | 是否开启等候室(只对MMR企业生效)。 true：开启 false：不开启 |
| isHostCameraOn | 否 | Boolean | 主持人入会是否开启摄像头。 true：开启 false：不开启 |
| isGuestCameraOn | 否 | Boolean | 来宾入会是否开启摄像头。 true：开启 false：不开启 |


## 状态码<a name="section11407328568"></a>

**表 5**  状态码说明

<a name="table102780442391"></a>

| HTTP状态码 | 描述 |
|---|---|
| 200 | 操作成功。 |
| 400 | 参数异常。 |
| 401 | 未鉴权或鉴权失败。 |
| 403 | 权限受限。 |
| 500 | 服务端异常。 |


## 响应参数<a name="section498722842014"></a>

**表 6**  响应参数

<a name="table4990175112163"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| [数组元素] | Array of ConferenceInfo | 会议信息列表。 |


**表 7**  ConferenceInfo 数据结构

<a name="table1022474182320"></a>

| 参数名称 | 参数类型 | 描述 |
|---|---|---|
| conferenceID | String | 会议ID。 |
| subject | String | 会议主题。 |
| size | Integer | 会议预约时添加的会议者数量。 |
| timeZoneID | String | 会议通知中会议时间的时区信息。时区信息，参考 时区映射关系 。 说明： 举例：“timeZoneID”:"26"，则通过移动会议发送的会议通知中的时间将会标记为如“2021/11/11 星期四 00:00 - 02:00 (GMT) 格林威治标准时间:都柏林, 爱丁堡, 里斯本, 伦敦”。 |
| startTime | String | 会议起始时间 (YYYY-MM-DD HH:MM )。 |
| endTime | String | 会议结束时间 (YYYY-MM-DD HH:MM )。 |
| mediaTypes | String | 会议的媒体类型。 由1个或多个枚举String组成，多个枚举时，每个枚举值之间通过”,”逗号分隔。如：mediaTypes：“Voice,Data,HDVideo” “Voice”：语音 “Video”：标清视频 “HDVideo”：高清视频 “Data”：数据 |
| conferenceState | String | 会议状态。 “Schedule”：预定状态 “Creating”：正在创建状态 “Created”：会议已经被创建，并正在召开 “Destroyed”：会议已经关闭 |
| language | String | 会议通知短信或邮件的语言。默认中文。 zh-CN：中文 en-US：英文 |
| accessNumber | String | 会议接入的SIP号码。 |
| passwordEntry | Array of PasswordEntry objects | 会议密码。 说明： 创建会议时，返回主持人密码和来宾密码 主持人查询会议时，返回主持人密码和来宾密码 来宾查询会议时，返回来宾密码 |
| userUUID | String | 会议预订者的用户UUID。 |
| scheduserName | String | 会议预订者名称。 |
| conferenceType | Integer | 会议类型。 0 : 普通会议。 2 : 周期性会议。 |
| confType | String | 会议类型。 FUTURE：将来开始的会议（创建时） IMMEDIATELY：立即开始的会议（创建时） CYCLE：周期会议 |
| cycleParams | CycleParams object | 周期会议参数。当会议是周期会议的时候携带该参数。 |
| isAutoMute | Integer | 是否入会自动静音。 0 : 不自动静音 1 : 自动静音 |
| isAutoRecord | Integer | 是否自动开启云录制。 0 : 不自动启动 1 : 自动启动 |
| chairJoinUri | String | 主持人会议链接地址。 |
| guestJoinUri | String | 普通与会者会议链接地址。 |
| audienceJoinUri | String | 网络研讨会观众会议链接地址。 |
| recordType | Integer | 录播类型。 0: 禁用 1: 直播 2: 录播 3: 直播+录播 |
| auxAddress | String | 辅流直播推流地址。 |
| liveAddress | String | 主流直推流播地址。 |
| recordAuxStream | Integer | 是否录制辅流。 0：否 1：是 |
| recordAuthType | Integer | 录播观看鉴权方式。 0：可通过链接观看/下载 1：企业用户可观看/下载 2：与会者可观看/下载 |
| liveUrl | String | 直播观看地址。 |
| confConfigInfo | ConfConfigInfo object | 会议其他配置信息。 |
| vmrFlag | Integer | 是否使用云会议室或个人会议ID召开预约会议。 0：不使用云会议室或个人会议ID 1：使用云会议室或个人会议ID |
| isHasRecordFile | Boolean | 是否有会议录制文件。仅历史会议查询时返回。 true：有录制文件。 false：没有录制文件。 |
| vmrConferenceID | String | 云会议室会议ID或个人会议ID。如果 “vmrFlag” 为 “1” ，则该字段不为空。 |
| confUUID | String | 会议的UUID。 说明： 只有创建立即开始的会议才返回UUID，如果是预约未来的会议，不会返回UUID 可以通过 查询历史会议列表 获取历史会议的UUID |
| partAttendeeInfo | Array of PartAttendee objects | 被邀请的部分与会者信息。 说明： 只返回被邀请的前20条软终端与会者信息和前20条硬终端与会者信息 不返回会中主动加入的与会者信息 “ 查询会议列表 ”和“ 查询会议详情 ”接口，返回预约会议时邀请的与会者和会中主持人邀请的与会者 “ 查询在线会议列表 ”、“ 查询在线会议详情 ”、“ 查询历史会议列表 ”和“ 查询历史会议详情 ”接口返回预约会议时邀请的与会者。不返回会中主持人邀请的与会者 |
| terminlCount | Integer | 硬终端个数，如IdeaHub，TE30等。 |
| normalCount | Integer | 软终端个数，如PC端、手机端App等。 |
| deptName | String | 会议预定者的企业名称。 |
| role | String | 与会者角色。 chair ：主持人 general ：来宾 audience ： 观众 说明： 仅在查询会议详情时返回 返回查询者本身的角色 |
| multiStreamFlag | Integer | 标识是否为多流视频会议。 1 ：多流会议 |
| webinar | Boolean | 是否是网络研讨会。 |
| onlineAttendeeAmount | Integer | 当前在线与会人数。包含被邀入会和主动入会的与会者。 说明： 仅在“ 查询在线会议列表 ”接口中返回。 |
| confMode | String | 会议模型。 COMMON ：MCU会议 RTC ：MMR会议 |
| scheduleVmr | Boolean | VMR预约记录。 true ：VMR会议 false ：普通会议 说明： 该参数将废弃，请勿使用。 |
| vmrID | String | 云会议室ID。 |
| concurrentParticipants | Integer | 会议最大与会人数。默认值0。 0：无限制 大于0：会议最大与会人数 |
| supportSimultaneousInterpretation | Boolean | 会议是否支持同声传译 true ：支持 false ：不支持 |
| picDisplay | MultiPicDisplayDO object | 多画面信息。 |
| subConfs | Array of Subconfs objects | 周期子会议列表。 |
| cycleSubConfID | String | 第一个周期子会议的UUID。 |


**表 8**  PasswordEntry 数据结构

<a name="table94617321319"></a>

| 参数 | 参数类型 | 描述 |
|---|---|---|
| conferenceRole | String | 会议角色。 chair：会议主持人 general：普通与会者 |
| password | String | 会议中角色的密码（明文）。 |


**表 9**  PartAttendee 数据结构

<a name="table132851410183118"></a>

| 参数 | 参数类型 | 描述 |
|---|---|---|
| name | String | 与会者名称。 |
| phone | String | 号码。SIP号码或者手机号码。 |
| phone2 | String | 预留字段，取值类型同参数 “phone” 。 |
| phone3 | String | 预留字段，取值类型同参数 “phone” 。 |
| type | String | 终端类型，类型枚举如下： normal：软终端 terminal：硬终端 outside：外部与会人 mobile：用户手机号码 ideahub：ideahub board: 电子白板（SmartRooms）。含Maxhub、海信大屏、IdeaHub B2 hwvision：华为智慧屏TV |
| role | Integer | 会议中的角色。默认为普通与会者。 0：普通与会者 1：会议主持人 |
| isMute | Integer | 用户入会时是否需要自动静音 。默认不静音。 0： 不需要静音 1： 需要静音 说明： 仅会中邀请与会者时才生效。 |


**表 10**  MultiPicDisplayDO 数据结构

<a name="table1375715395424"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| manualSet | Integer | 是否为手工设置多画面。 0 ：系统自动多画面 1 ：手工设置多画面 |
| imageType | String | 画面类型。取值范围: Single: 单画面 Two: 二画面 Three: 三画面， Three-2: 三画面-2， Three-3: 三画面-3， Three-4: 三画面-4 Four: 四画面， Four-2: 四画面-2， Four-3: 四画面-3 Five: 五画面， Five-2: 五画面-2 Six: 六画面， Six-2: 六画面-2， Six-3: 六画面-3， Six-4: 六画面-4， Six-5: 六画面-5 Seven: 七画面， Seven-2: 七画面-2， Seven-3: 七画面-3， Seven-4: 七画面-4 Eight: 八画面， Eight-2: 八画面-2， Eight-3: 八画面-3， Eight-4: 八画面-4 Nine: 九画面 Ten: 十画面， Ten-2: 十画面-2， Ten-3: 十画面-3， Ten-4: 十画面-4， Ten-5: 十画面-5， Ten-6: 十画面-6 Thirteen: 十三画面， Thirteen-2: 十三画面-2， Thirteen-3: 十三画面-3，Thirteen-4: 十三画面-4， Thirteen-5: 十三画面-5， ThirteenR: 十三画面R， ThirteenM: 十三画面M Sixteen: 十六画面 Seventeen: 十七画面 Twenty-Five: 二十五画面 Custom: 自定义多画面（当前不支持） |
| subscriberInPics | Array of PicInfoNotify objects | 子画面列表。 |
| switchTime | Integer | 表示轮询间隔，单位：秒。当同一个子画面中包含有多个视频源时，此参数有效。 |
| picLayoutInfo | PicLayoutInfo object | 自定义多画面布局信息。预留字段，当前不支持。 |


**表 11**  PicInfoNotify 数据结构

<a name="table1321955012914"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| index | Integer | 多画面中每个画面的编号，编号从1开始。 |
| id | Array of strings | 每个画面中的与会者SIP号码。SIP号码可以通过 查询企业通讯 接口录获取。 |
| share | Integer | 是否为辅流 0： 不是辅流 1： 是辅流 |


**表 12**  PicLayoutInfo 数据结构

<a name="table176947316228"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| x | Integer | 横向小格子数。 |
| y | Integer | 纵向小格子数。 |
| subPicLayoutInfoList | Array of SubPicLayoutInfo objects | 多画面信息。 |


**表 13**  SubPicLayoutInfo 数据结构

<a name="table1529643635110"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| id | Integer | 子画面索引。 |
| left | Integer | 子画面从左到右的索引。 |
| top | Integer | 子画面从上到下的索引。 |
| xSize | Integer | 子画面横向尺寸。 |
| ySize | Integer | 子画面纵向尺寸。 |


**表 14**  CycleParams 数据结构

<a name="table128225874014"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| startDate | String | 周期会议的开始日期，格式：YYYY-MM-DD。 开始日期不能早于当前日期。 说明： 日期是timeZoneID指定的时区的日期，非UTC时间的日期。 |
| endDate | String | 周期会议的结束日期，格式：YYYY-MM-DD。 开始日期和结束日期间的时间间隔最长不能超过1年。开始日期和结束日期之间最多允许50个子会议，若超过50个子会议，会自动调整结束日期。 说明： 日期是timeZoneID指定的时区的日期，非UTC时间的日期。 |
| cycle | String | 周期类型。 Day：天 Week：星期 Month：月 |
| interval | Integer | 子会议间隔。 “cycle” 选择了 “Day” ，表示每几天召开一次，取值范围[1,15] “cycle” 选择了 “Week” ，表示每几周召开一次，取值范围[1,5] “cycle” 选择了 “Month” ，Interval表示隔几月，取值范围[1,3] |
| point | Array of integers | 周期内的会议召开点。仅当按周和月时有效。 “cycle” 选择了 “Week” ，point中填入了两个元素1和3，则表示每个周一和周三召开会议，0表示周日 “cycle” 选择了 “Month” ，point中填入了12和20则表示每个月的12号和20号召开会议，取值范围为[1,31]，若当月没有该值，则为月末 |
| preRemindDays | Integer | 提前通知天数。所有与会者在每个子会议开始前N天收到会议通知。取值范围[0,30]。 默认值是1。 |


**表 15**  ConfConfigInfo 数据结构

<a name="table58585814406"></a>

| 参数 | 类型 | 描述 |
|---|---|---|
| isSendNotify | Boolean | 是否需要发送会议邮件通知。默认值由企业级配置决定。 true：需要 false：不需要 |
| isSendSms | Boolean | 是否需要发送会议短信通知。 true：需要 false：不需要 说明： 保留字段，暂不提供短信通知能力。 |
| isSendCalendar | Boolean | 是否需要发送会议日历通知。默认值由企业级配置决定。 true：需要 false：不需要 |
| isAutoMute | Boolean | 来宾入会，软终端是否自动静音。默认值由企业级配置决定。 true：自动静音 false：不自动静音 |
| isHardTerminalAutoMute | Boolean | 来宾入会，硬终端是否自动静音。默认值由企业级配置决定。 true：自动静音 false：不自动静音 |
| isGuestFreePwd | Boolean | 是否来宾免密（仅随机会议有效）。 true：免密 false：需要密码 说明： 仅随机会议ID的会议生效。 |
| callInRestriction | Integer | 允许加入会议的范围。 0：所有用户 2：企业内用户 3：被邀请用户 |
| allowGuestStartConf | Boolean | 是否允许来宾启动会议。 true：允许来宾启动会议。 false：禁止来宾启动会议。 说明： 仅随机会议ID的会议生效。 |
| guestPwd | String | 来宾密码（4-16位长度的纯数字）。 |
| vmrIDType | Integer | 云会议室的会议ID模式。 0：固定会议ID 1：随机会议ID |
| prolongLength | Integer | 自动延长会议时长（取值范围0-60）。 0：表示会议到点自动结束，不延长会议 其他：表示自动延长的时长 说明： 自动结束会议是按照会议时长计算。比如预定的会议是9:00开始11:00结束，会议时长2个小时，如果与会者8:00就加入会议了，那会议在10:00就会自动结束 设置成其他值时，只要会中还有与会者，会议可以多次延迟 |
| enableWaitingRoom | Boolean | 开启或者关闭等候室。 true：开启 false：不开启 |
| isHostCameraOn | Boolean | 主持人入会是否开启摄像头。 true：开启 false：不开启 |
| isGuestCameraOn | Boolean | 来宾入会是否开启摄像头。 true：开启 false：不开启 |


## 请求消息示例<a name="section1498763918202"></a>

```
POST /v1/mmc/management/conferences
Connection: keep-alive
X-Access-Token: stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC
Content-Type: application/json
user-agent: WeLink-desktop
Content-Length: 548
Host: apigw.125339.com.cn
User-Agent: Apache-HttpClient/4.5.3 (Java/1.8.0_191)

{
    "subject": "例行会议",
    "mediaTypes": "HDVideo",
    "startTime": "2022-08-30 12:00",
    "length": 60,
    "attendees": [
        {
            "accountId": "zhangshan@125339.com.cn",
            "appId": "caaab5a3e584497990f6a9b582a0ae42"
        }
    ],
   "confConfigInfo": {
       "isSendNotify": false,
       "isSendSms": false,
       "isSendCalendar": false
    }
}
```

## 响应消息示例<a name="section339419481201"></a>

```
HTTP/1.1 200 
Date: Wed, 18 Dec 2019 06:20:40 GMT
Content-Type: application/json;charset=UTF-8
Content-Length: 1153
Connection: keep-alive
http_proxy_id: 79ea4d8bdb461a4b811a117f9cf3dbde
Server: api-gateway
X-Request-Id: 1ccc1d7937dd0f66067aeecb9f1df241

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

## 错误码<a name="section222616171078"></a>

如果遇到"MMC"或者"USG"开头的错误码，请参考接口文档中错误码表

## CURL命令示例<a name="section2790610197"></a>

```
curl -k -i -H 'content-type: application/json' -X POST -H 'X-Access-Token:stbX5ElstO5QwOwPB9KGQWUZ1DHoFrTsQjjC' -d '{"conferenceType": "0","subject": "user01 conference","mediaTypes": "HDVideo","attendees": [{"name": "user01","role": 1,"phone": "+8657*******"}]}' 'https://apigw.125339.com.cn/v1/mmc/management/conferences'
```

