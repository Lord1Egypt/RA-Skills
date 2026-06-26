# 视频云录制文档摘要

本文件是视频云录制 Skill 的自包含参考摘要，整理自海康云眸开放平台原始页面：

- [视频云录制](https://pic.hik-cloud.com/opencustom/apidoc/online/open/b6f980108b8242258716079c118d5702.html)

本技能覆盖以下命令：

- `project-create`：创建项目
- `project-get`：查询项目
- `project-update`：更新项目
- `project-delete`：删除项目
- `project-list`：查询项目列表
- `record-replay`：回放视频转码录制
- `record-preview`：预约视频转码录制
- `record-instant`：即时视频转码录制
- `frame-interval`：按时间间隔抽帧
- `frame-timing`：按时间点抽帧
- `frame-instant`：实时抽帧
- `task-stop`：终止任务
- `task-get`：根据任务 ID 查询任务详情
- `task-list`：根据项目 ID 查询任务列表
- `file-task-list`：根据任务 ID 获取文件列表
- `file-get`：查询单个文件
- `file-list`：分页查询文件
- `file-delete`：删除文件
- `file-download`：获取文件下载地址
- `flow-update`：更新项目流量限制
- `tenant-info`：获取租户流量信息
- `upload-address`：获取上传地址
- `save-file`：保存文件
- `clip`：视频剪辑
- `clip-file-query`：视频剪辑文件查询

参数要点：

- 项目管理以 `projectId` / `projectName` / `expireDays` / `flowLimit` 为主
- 录制任务通常依赖 `projectId`、`deviceSerial`、`channelNo`、时间范围和录制类型
- 文件管理和流量管理都围绕项目和文件 ID 展开
- 资源上传需要先取到上传地址，再把文件通过返回的 `url` 和 `fields` 上传到对象存储
- 剪辑接口通过 `timeLines` 描述一组素材时间线

关键枚举说明：

- `recType` = `local` 本地录像、`cloud` 云存储录像、`live` 实时录像/实时抽帧；只用于录制和抽帧接口，不要和 `timeLines[].type` 混用
- `streamType` = `1` 高清主码流、`2` 标清子码流；不传默认 `1`
- `devProto` = 不传默认萤石协议，`gb28181` 表示国标设备
- `voiceSwitch` = `0` 关、`1` 开、`2` 自动；仅 `record-instant` 使用
- `frameModel` = `0` 普通、`1` 错峰、`2` 抽 I 帧；`frame-interval` 支持 0/1/2，`frame-timing` 页面仅列 0/1
- `fileType` = `0` 图片、`1` 视频、`2` 音频；`fileChildType` = `00` jpg、`10` mp4、`20` mp3
- `timeLines[].type` = `1` 视频文件、`3` 图片文件；`type=1` 取云录制文件 ID，`type=3` 取图片上传返回的文件 ID
