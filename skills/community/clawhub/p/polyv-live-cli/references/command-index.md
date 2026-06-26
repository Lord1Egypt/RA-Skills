# 命令索引

本文件由发布版 CLI help 生成，用于快速定位命令路径。执行前仍必须运行对应 `--help` 校验参数。

CLI 前缀：`<CLI>` = `npx --yes polyv-live-cli@latest`

生成时间：2026-06-23T00:00:00.000Z

## 一级命令

共 40 个一级命令，不含 Commander 内置 `help`。

- `account`: Manage PolyV account configurations
- `ai`: Manage AI features for live streaming (管理AI功能)
- `card-push`: Manage card push for live streaming (管理直播卡片推送)
- `channel`: Manage live streaming channels
- `chat`: Manage live streaming chat messages
- `checkin`: Manage live streaming checkin interactions
- `coupon`: Manage coupons
- `custom-field`: Manage user custom fields
- `document`: 课件管理命令
- `donate`: Manage live streaming donate interactions
- `finance`: Manage finance, billing, and moderation APIs
- `global`: Manage global account settings
- `group`: Manage group account resources
- `interaction`: Manage cross-cutting live interaction APIs
- `invite-sales`: Manage user invite sales
- `lottery`: Manage live streaming lottery interactions
- `material`: Manage material library
- `monitor`: Start live streaming monitoring dashboard
- `partner`: Manage partner account tools
- `platform`: Platform account info management commands
- `playback`: 回放管理命令
- `player`: Manage channel player settings
- `product`: Manage live streaming channel products
- `promotion`: Manage marketing promotion channels (管理营销推广渠道)
- `qa`: Manage live streaming QA question cards
- `questionnaire`: Manage live streaming questionnaires
- `record`: 录制设置管理命令
- `robot`: Manage global robots
- `session`: 场次管理命令
- `setup`: Initialize a scene with predefined resources
- `statistics`: View live streaming statistics data
- `stream`: Manage live streaming operations
- `transmit`: Manage transmit channels for live streaming
- `use`: 管理当前终端会话的账号设置
- `user`: Manage user account settings, templates,
- `viewer`: Manage viewer information queries
- `watch-condition`: 观看条件配置管理
- `web`: Manage watch page configuration
- `webapp`: Manage WebApp roles and permissions
- `whitelist`: 白名单管理

## 直接子命令

### account

Manage PolyV account configurations

- `account add`: Add a new account configuration
- `account api`: Manage server-side account APIs
- `account current`: Show current account information
- `account list`: List all configured accounts
- `account migrate`: Migrate legacy configuration to new account system
- `account remove`: Remove an account configuration
- `account set-default`: Set an account as the default account
- `account unset-default`: Remove the current default account setting

### ai

Manage AI features for live streaming (管理AI功能)

- `ai digital-human`: Manage AI Digital Humans (管理AI数字人)
- `ai video-produce`: Manage AI video production tasks, PPT files, and TTS voices

### card-push

Manage card push for live streaming (管理直播卡片推送)

- `card-push cancel`: Cancel a pushing card (取消正在推送的卡片)
- `card-push create`: Create a new card-push (创建新的卡片推送)
- `card-push delete`: Delete a card-push (删除卡片推送)
- `card-push list`: List all card-pushes (列出所有卡片推送)
- `card-push push`: Push a card to viewers (推送卡片到观众)
- `card-push share`: Manage channel share settings (管理频道分享设置)
- `card-push update`: Update an existing card-push (更新现有卡片推送)

### channel

Manage live streaming channels

- `channel advert-list`: List channel adverts
- `channel auth`: Manage channel auth tokens
- `channel basic-list`: List V4 channel basic information
- `channel batch-create`: Batch create V4 live channels
- `channel batch-delete`: Delete multiple live streaming channels at
- `channel callback`: Manage channel callback settings
- `channel ccb-focus-reset`: Reset CCB focus channels
- `channel children-list`: List channels owned by a child account
- `channel copy`: Copy a channel
- `channel create`: Create a new live streaming channel
- `channel create-init`: Create and initialize a V4 channel
- `channel danmu-batch-update`: Batch update channel danmu settings
- `channel delete`: Delete a single live streaming channel with
- `channel distribute`: Manage V4 cloud distribution
- `channel follow`: Manage follow-public-account settings
- `channel get`: Get detailed information for a specific
- `channel list`: List live streaming channels with pagination
- `channel live-status-list`: Batch query V4 channel live status
- `channel marquee-url-set`: Set custom URL marquee protection
- `channel max-viewer-set`: Set max viewer count
- `channel mr-create`: Create a V4 MR channel
- `channel password-update`: Update channel password
- `channel ppt-record`: Manage PPT record remake tasks and settings
- `channel pull-bitrate-set`: Set V4 channel pull bitrate
- `channel questionnaire-stop`: Stop questionnaires for channels
- `channel role`: Manage historical channel role accounts
- `channel simple-list`: List V4 channel compact information
- `channel status-valid`: Check whether channel statuses are valid
- `channel submeeting-batch-add`: Batch save submeeting channels
- `channel subtitle`: Manage V4 realtime subtitle settings
- `channel template-update`: Update V4 channel live template
- `channel token`: Manage channel historical tokens
- `channel update`: Update an existing live streaming channel
- `channel v4-update`: Update V4 channel basic information
- `channel viewer`: Manage channel-owned viewers and viewer

### chat

Manage live streaming chat messages

- `chat badword`: Manage account and channel badwords
- `chat ban`: Ban users from chat (channel or global)
- `chat banned`: Manage banned items
- `chat censor`: Manage chat censor settings
- `chat delete`: Delete a chat message or clear all messages
- `chat enabled`: Manage channel chat switch
- `chat group-login-times`: Get group login times for a channel
- `chat kick`: Kick users from channel or globally
- `chat kicked`: Manage kicked users
- `chat list`: List chat history with pagination
- `chat message`: Manage advanced chat messages
- `chat notice`: Manage channel notices
- `chat qa`: Manage chat Q&A records
- `chat robot`: Manage channel chat robots
- `chat role`: Manage chat role information
- `chat send`: Send an admin message to the channel chat
- `chat unban`: Unban users from chat (channel or global)
- `chat unkick`: Unkick users (cancel kick status)
- `chat viewer-logout`: Log out a viewer from the channel watch page

### checkin

Manage live streaming checkin interactions

- `checkin list`: List checkin records (checked-in users only)
- `checkin result`: Get checkin result details (including checked and
- `checkin session-result`: Get checkin records by live session ID
- `checkin sessions`: List checkin sessions by time range
- `checkin start`: Start a checkin session in the channel

### coupon

Manage coupons

- `coupon add`: Create a new coupon (满减券 or 折扣券)
- `coupon channel`: Manage channel coupon associations
- `coupon delete`: Delete coupons in batch (max 200 IDs)
- `coupon list`: List coupons with pagination and status filter

### custom-field

Manage user custom fields

- `custom-field add`: Add a custom field
- `custom-field list`: List custom fields
- `custom-field value`: Manage custom field viewer values

### document

课件管理命令

- `document delete`: 删除课件文档
- `document list`: 获取频道课件文档列表
- `document media`: 管理频道关联音视频资源
- `document status`: 查询文档转码状态
- `document teacher-doc`: 管理讲师与文档关系
- `document upload`: 上传课件文档到频道

### donate

Manage live streaming donate interactions

- `donate config`: Manage donate configuration
- `donate likes`: List like reward records
- `donate list`: List donate records

### finance

Manage finance, billing, and moderation APIs

- `finance audio-moderation`: Audio moderation APIs
- `finance bill-detail-list`: List finance bill details
- `finance video-moderation`: Video moderation APIs

### global

Manage global account settings

- `global auth`: Global auth settings
- `global page-setting`: Global page settings

### group

Manage group account resources

- `group allocate-log`: List legacy group allocation logs
- `group billing-daily`: List group account daily billing
- `group health-check`: Check group backend health
- `group resource`: Legacy resource allocation APIs
- `group user`: Group sub-account APIs

### interaction

Manage cross-cutting live interaction APIs

- `interaction event`: Manage interaction listener events
- `interaction favor`: Send likes for a viewer
- `interaction invite-poster`: Manage invite poster interaction helpers
- `interaction reward`: Send a reward message
- `interaction script`: Manage pseudo-live disk video interaction scripts
- `interaction task-reward`: Manage task reward activities
- `interaction teacher-answer`: Send a teacher answer to a student question
- `interaction webhook`: Manage student question webhook

### invite-sales

Manage user invite sales

- `invite-sales add`: Add invite sales
- `invite-sales follow-viewer`: Manage invite sales follow viewers
- `invite-sales list`: List invite sales
- `invite-sales remove`: Remove invite sales
- `invite-sales update`: Update invite sales organization

### lottery

Manage live streaming lottery interactions

- `lottery blacklist`: Manage lottery viewer blacklist
- `lottery channel-records`: Get lottery records across channels
- `lottery create`: Create a lottery activity
- `lottery delete`: Delete lottery activity
- `lottery download-winners`: Download lottery winner details
- `lottery get`: Get lottery activity details
- `lottery group`: Manage lottery viewer whitelist groups
- `lottery group-viewer`: Manage lottery viewer whitelist group members
- `lottery legacy-records`: Get legacy V3 lottery records for a single channel
- `lottery list`: List lottery activities
- `lottery lucky-bag`: Manage lucky bag lottery data
- `lottery receive-info`: Add winner receive information
- `lottery records`: Get lottery activity records
- `lottery update`: Update lottery activity
- `lottery wait`: Manage condition lottery wait schedules
- `lottery winners`: Get winner list for a lottery

### material

Manage material library

- `material category`: Material category APIs
- `material delete`: Delete materials
- `material label`: Material label APIs
- `material list`: List materials

### monitor

Start live streaming monitoring dashboard

- `monitor config`: Manage monitoring configuration
- `monitor export`: Export monitoring configuration
- `monitor import`: Import monitoring configuration
- `monitor layouts`: List available dashboard layouts
- `monitor status`: Show monitoring dashboard status
- `monitor stream-info-list`: List V4 channel realtime stream
- `monitor tencent-stream-info-list`: List Tencent stream monitoring info
- `monitor test`: Test monitoring dashboard compatibility
- `monitor themes`: List available themes

### partner

Manage partner account tools

- `partner tencent-order`: Tencent order APIs
- `partner user-register`: Register a partner customer account

### platform

Platform account info management commands

- `platform anchor`: Anchor management (主播管理)
- `platform callback`: Callback settings management (回调设置管理)
- `platform content-group`: Content group management
- `platform coupon`: Platform coupon operations
- `platform get`: Get account info (获取账号信息)
- `platform label`: Label management (标签管理)
- `platform setting`: Global channel settings management (全局频道设置管理)
- `platform switch`: Switch configuration management (开关配置管理)

### playback

回放管理命令

- `playback add-vod`: 将点播视频添加到频道回放视频库
- `playback delete`: 删除回放视频
- `playback enabled`: 管理频道回放开关
- `playback get`: 获取单个回放视频详情
- `playback list`: 获取频道回放列表
- `playback merge`: 合并录制文件
- `playback setting-list`: 批量查询频道回放设置
- `playback sort`: 管理回放视频排序
- `playback subtitle`: 管理回放字幕
- `playback title`: 管理回放标题
- `playback video-info`: 批量查询频道单个回放信息

### player

Manage channel player settings

- `player advert`: Manage player adverts
- `player anti-record`: Manage anti-record settings
- `player config`: Manage channel player configuration
- `player logo-update`: Update player logo settings
- `player marquee-url`: Set marquee URL restriction
- `player skin`: Manage V4 player skin settings
- `player warmup`: Manage player warmup settings
- `player watch-feedback-list`: List watch feedback records

### product

Manage live streaming channel products

- `product add`: Add a new product to channel
- `product batch-add`: Batch add products to a channel
- `product batch-delete`: Batch delete channel products
- `product batch-shelf`: Batch update channel product shelf status
- `product cancel-push`: Cancel a pushed channel product
- `product channel-tag`: Manage channel product tags
- `product delete`: Delete a product from channel
- `product enabled`: Get channel product library enabled status
- `product library`: Manage user-level product library
- `product list`: List products with pagination
- `product order`: Manage user-level product orders
- `product push`: Push a channel product to viewers
- `product push-rule`: Manage channel product push rule
- `product rank`: Set channel product rank
- `product reference`: Reference a platform product into a channel product
- `product shelf`: Update one channel product shelf status
- `product sort`: Sort a channel product
- `product stats`: Query channel product statistics
- `product tag`: Manage user-level product tags
- `product topping`: Top a channel product
- `product untopping`: Cancel topping for a channel product
- `product update`: Update an existing product
- `product update-enabled`: Update channel product library enabled status

### promotion

Manage marketing promotion channels (管理营销推广渠道)

- `promotion create`: Batch create promotion channels (批量创建推广渠道)
- `promotion list`: List all promotion channels (列出所有推广渠道)

### qa

Manage live streaming QA question cards

- `qa add-edit`: Create or update a QA question card
- `qa answers`: List QA answer records
- `qa delete-question`: Delete a QA question card
- `qa list`: List QA question cards for the channel
- `qa question-list`: List student question records
- `qa send`: Send a QA question card to the channel
- `qa send-result`: Publish QA question result statistics
- `qa send-times`: List QA question card send times
- `qa stop`: Stop a QA question card and get answer statistics

### questionnaire

Manage live streaming questionnaires

- `questionnaire batch-create`: Batch create questionnaires
- `questionnaire create`: Create a new questionnaire
- `questionnaire detail`: Get questionnaire detail with questions
- `questionnaire legacy-list`: List questionnaires through the legacy V3 API
- `questionnaire list`: List questionnaires with pagination
- `questionnaire results`: List questionnaire answer records

### record

录制设置管理命令

- `record breakpoint`: 管理录制打点
- `record clip`: 裁剪录制文件
- `record convert`: 转存录制文件到点播
- `record file`: 管理历史录制文件
- `record material-list`: 分页查询素材库频道直播回放列表
- `record merge-mp4`: 合并直播录制文件并回调 MP4 下载地址
- `record merge-mp4-start`: 提交异步 MP4 合并任务
- `record outline`: 管理暂存视频大纲
- `record set-default`: 设置默认回放视频
- `record setting`: 回放设置管理
- `record subtitle`: 管理暂存视频字幕
- `record temp-list`: 查询频道单个直播暂存信息

### robot

Manage global robots

- `robot batch-delete`: Batch delete global robots
- `robot batch-save`: Batch save global robots
- `robot list`: List global robots

### session

场次管理命令

- `session create`: 创建频道新版场次
- `session data-list`: 查询频道场次数据列表
- `session delete`: 删除频道新版场次
- `session external`: 管理外部场次 ID 关联
- `session get`: 获取单个场次详情
- `session legacy-list`: 查询频道历史场次信息
- `session list`: 获取频道场次列表
- `session update`: 更新频道新版场次

### setup

Initialize a scene with predefined resources

无直接子命令；查看 `<CLI> setup --help`。

### statistics

View live streaming statistics data

- `statistics audience`: View audience statistics
- `statistics channel-play-summary`: Get multi-channel play summary statistics
- `statistics channel-session-stats`: Get channel session statistics
- `statistics channel-statistic`: Get channel statistic data
- `statistics channel-summary`: Get channel view summary statistics
- `statistics concurrency`: 查看历史并发数据
- `statistics export`: export statistics data
- `statistics invite-list`: List V4 invite statistics records
- `statistics inviter-poster-list`: List inviter poster statistics
- `statistics link-mic-list`: List channel link-mic detail logs
- `statistics live-data`: Get V4 channel live data summary
- `statistics live-session-list`: List V4 live session statistics
- `statistics lottery-list`: List V4 channel lottery statistics records
- `statistics max-concurrent`: 查看历史最高并发人数
- `statistics mic-list`: List channel mic detail statistics
- `statistics product-click`: List product click statistics
- `statistics product-list-click`: List product-list click statistics
- `statistics realtime-v1`: Get realtime viewers using the legacy V1
- `statistics realtime-viewers`: Get realtime viewer counts for channels
- `statistics redpack-list`: List redpack statistics
- `statistics session-summary-list`: List V4 session statistics summaries
- `statistics view`: View daily statistics for a channel
- `statistics viewlog-v1`: Get V1 viewlog records
- `statistics viewlog-v2`: Get V2 paged viewlog records
- `statistics weixin-booking-list`: List V4 WeChat booking records

### stream

Manage live streaming operations

- `stream ban-push`: Ban/cut off push stream
- `stream capture`: Get current live capture image
- `stream disk-video`: Manage pseudo-live disk videos
- `stream get-key`: Get RTMP URL and stream key for a live channel
- `stream hls-pull-url`: Get the channel monitor HLS pull URL
- `stream live-status`: Use historical live status APIs
- `stream monitor`: Monitor stream status in real-time with live
- `stream push`: Push a local video file to a live channel
- `stream resume`: Resume push stream
- `stream start`: Start live streaming for a channel
- `stream status`: Get real-time status information for a live channel
- `stream stop`: Stop live streaming for a channel
- `stream streams`: Get stream monitor info for channel IDs
- `stream type-update`: Update channel stream type
- `stream verify`: Verify stream quality and performance for a live

### transmit

Manage transmit channels for live streaming

- `transmit associate`: Add or cancel receive channel transmit associations
- `transmit create`: Batch create transmit channels (批量创建转播频道)
- `transmit list`: Get transmit associations (获取转播关联列表)

### use

管理当前终端会话的账号设置

无直接子命令；查看 `<CLI> use --help`。

### user

Manage user account settings, templates,

- `user bill`: Manage user billing details
- `user child`: Manage child accounts
- `user mic-duration`: Get user mic duration
- `user mr-concurrency`: Manage MR concurrency
- `user org`: Manage organizations
- `user setting`: Manage user global settings
- `user sms-send`: Send SMS notification
- `user template`: Manage default user templates
- `user viewlog`: Manage user watch logs

### viewer

Manage viewer information queries

- `viewer config`: Manage viewer user system config
- `viewer create`: Create a viewer record
- `viewer delete`: Delete a viewer record
- `viewer get`: Get single viewer details
- `viewer import-external`: Import external viewer records
- `viewer label`: Manage account labels and channel label refs
- `viewer list`: List viewers with pagination and filters
- `viewer lottery-wins`: List viewer lottery win records
- `viewer tag`: Manage viewer tags
- `viewer update`: Update a viewer record

### watch-condition

观看条件配置管理

- `watch-condition get`: 获取观看条件配置
- `watch-condition set`: 设置观看条件配置

### web

Manage watch page configuration

- `web auth`: Watch condition and authorization APIs
- `web donate`: Watch page donate APIs
- `web info`: Watch page basic info
- `web menu`: Watch page menu APIs
- `web setting`: Watch page common settings
- `web share`: Watch page share APIs

### webapp

Manage WebApp roles and permissions

- `webapp permission-list`: List WebApp permissions
- `webapp role`: WebApp role APIs

### whitelist

白名单管理

- `whitelist add`: 添加白名单项
- `whitelist list`: 获取白名单列表
- `whitelist remove`: 删除白名单项
- `whitelist update`: 更新白名单项
