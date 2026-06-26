---
name: mobile-meeting-api
description: 提及移动会议/云视讯、视频会议、会议API集成时,自动激活本技能, 也可使用手动加载本技能（ use_skill mobile-meeting-api）。涵盖登录鉴权、会议管理（创建/编辑/取消/查询）、会议控制（会中操作）、网络研讨会管理等模块。
homepage: https://www.125339.com.cn/developerCenter/ReBar/63/222
version: 1.0.0 
tags: [API, 会议, 集成开发]
---

# 移动会议服务端API集成指导

## 概述

本skill基于`./references`文件夹中的接口文档，提供移动会议API集成的完整集成指导。

**API基本信息：**
- 协议：HTTPS/RESTful API
- 生产环境：`apigw.125339.com.cn`
- 鉴权方式：App ID鉴权（SDK用户及鉴权）+ 标准账号鉴权（高清、App账号及鉴权）

## 参考文档及执行脚本

- 完整API文档位于`./references`文件夹中。如需全量接口文档，可以从[云视讯/移动会议-开发者中心下载](https://www.125339.com.cn/developerCenter/ReBar/63/197)，或联系云视讯/移动会议集成开发支撑团队获取

## 触发原则

- 会议管理场景：创建会议、修改会议、查询历史会议、查询会议详情
- 录像管理：查询录制列表、查询会议录制详情、查询录制详情
- 会议控制场景：获取会控token、查询会议实时信息、挂断与会者、删除与会者
- 会议事件推送：会议级事件推送、企业级会议事件推送、事件推送设置


## 不触发边界
不要在以下场景使用此技能：

- 用户进行聊天、打电话、PSTN通话、视频剪辑等
- 用户要查询日历日程但不涉及云视讯/移动会议
- 用户要预约线下会议室（非线上会议）
- 用户询问的是其他视频会议平台（如 Zoom、Teams、腾讯会议、飞书会议、钉钉）


## 使用原则

### 1. 严格基于文档回答

**重要：** 回答用户问题时，必须：
1. 先读取`./references`文件夹中文档中的相关章节
2. 严格按照文档中的参数定义、字段说明、枚举值回答
3. **不要参考其他信息源或通用知识**
4. 如果未找到相关接口说明，提示从[云视讯/移动会议-开发者中心下载](https://www.125339.com.cn/developerCenter/ReBar/63/197)下载，或联系云视讯/移动会议集成开发支撑团队获取


### 2. 模块快速索引

根据用户问题，定位到对应模块查阅：

| 用户问题类型 | 查阅文件 | 关键词 |
|:---|:---|:---|
| 如何登录/获取Token | app_auth.html, CreateAppIdToken.md | `appauth`、`getToken` |
| 创建会议 | CreateMeeting.md | `创建会议` |
| 取消会议 | CancelMeeting.md | `取消预约` |
| 编辑会议 | UpdateMeeting.md | `修改会议` |
| 开始会议 | StartMeeting.md | `开始会议` |
| 查询会议列表/详情 | SearchMeetings.md, ShowMeetingDetail.md, SearchHisMeetings.md, ShowHisMeetingDetail.md | `查询会议` |
| 会中操作（静音/邀请/挂断等） | InviteParticipant.md, ListOnlineConfAttendee.md, SearchCtlRecordsOfHisMeeting.md | `会控`、`invite` |
| 参会记录 | SearchAttendanceRecordsOfHisMeeting.md | `参会记录` |
| 录制相关 | SearchRecordings.md, ShowRecordingDetail.md, ShowRecordingFileDownloadUrls.md, DeleteRecordings.md | `录制`、`download` |


## 工作流程

### 回答API问题

```
1. 理解用户问题（哪个功能模块）
2. 读取文档对应章节或文件
3. 提取准确的接口信息：
   - 请求方法（GET/POST/PUT/DELETE）
   - URL路径
   - 请求头要求（如Authorization签名）
   - 请求参数（必填/可选、类型、说明）
   - 响应字段
4. 按文档组织回答，不添加文档外内容
```

### 生成代码示例

如果用户需要代码示例：

```
1. 询问用户使用的编程语言（支持Python、JavaScript、Java等）
2. 读取文档中对应接口的完整参数定义
3. 生成代码，包含：
   - 完整的请求构造
   - 所有必填参数（按文档要求）
   - 请求头设置（特别是Authorization签名）
   - 错误处理
4. 添加注释说明参数来源（来自文档第X章或对应文件）
```

## 关键接口速查

### 登录鉴权

#### App ID鉴权 - 获取Token
```
POST /v2/usg/acs/auth/appauth
```
**关键参数：**
- `Authorization`: HMAC-SHA256签名 `appId:userId:expireTime:nonce`。签名可以使用`./scripts/app_auth.html`验证是否正确。
- `X-Token-Type`: 固定值 `LongTicket`
- `clientType`: 72（API调用类型）

**响应：**
- `accessToken`: 访问令牌（12-24小时有效）
- `refreshToken`: 刷新令牌（30天有效）

### 会议管理

- 创建会议: ` POST /v1/mmc/management/conferences `
- 查询会议列表: `GET /v1/mmc/management/conferences`
- 取消预约会议: `DELETE /v1/mmc/management/conferences`
- 查询会议详情: `GET /v1/mmc/management/conferences/confDetail`  
- 查询录制文件下载链接: ` GET /v1/mmc/management/record/downloadurls`

### 会议控制

- 获取会控Token ` GET /v1/mmc/control/conferences/token `
- 邀请与会者 ` POST /v1/mmc/control/conferences/participants`
- 静音与会者 ` PUT /v1/mmc/control/conferences/participants/mute `
- 全场静音 ` PUT /v1/mmc/control/conferences/mute `

### 打开移动会议app

```
ysx://com.zhongtai.ysx/app/callup?num=375xxx389&random=mnaibtK0wChtuoV8gPZDcpV99n2nARqge 
```

## 脚本工具

为方便用户快速测试API，本skill提供可执行Python脚本。脚本位于`./scripts/`文件夹，支持核心接口调用。

**使用前准备：**
1. 安装Python 3和requests库：`pip install requests`
2. 获取APP_ID、APP_KEY、USER_ID（从开发者中心获取）
3. 运行脚本时按提示输入参数

**可用脚本：**
- [获取Token](./scripts/get_token.py)：获取API访问令牌
- [创建会议](./scripts/create_meeting.py)：创建新会议
- [查询会议](./scripts/search_meetings.py)：查询会议列表
- [取消会议](./scripts/cancel_meeting.py)：取消预约会议

**签名调试工具：**
- [app_auth.html](./scripts/app_auth.html)：浏览器端交互式 HMAC-SHA256 签名生成器，**无需任何服务器或依赖**，直接用浏览器打开即可使用。输入 App ID、App Key、User ID，自动生成 Authorization 签名，适合在对接初期排查鉴权问题。

**注意：** 脚本仅用于测试，请勿在生产环境直接使用。确保网络安全，避免泄露密钥。

## 注意事项

1. **Token有效期**：accessToken 12-24小时，refreshToken 30天
2. **clientType固定值**：API调用时固定为72
3. **Authorization签名**：必须使用HMAC-SHA256，格式严格按文档。可以通过返回错误码或使用`./scripts/app_auth.html`，确定签名是否正确。
4. **错误处理**：参考错误码处理异常情况


## 常见问题

- **如何处理鉴权失败？**：检查App ID和Token是否正确，参考app_auth.html和CreateAppIdToken.md。
- **会议创建失败的原因？**：确认必填参数，如会议主题、开始时间等，参考CreateMeeting.md。
- **如何获取录制文件？**：使用ShowRecordingFileDownloadUrls.md中的接口获取下载链接。
- **事件推送如何配置？**：参考接口文档中的推送章节，设置Webhook或WebSocket。

最后更新日期：2026年4月27日