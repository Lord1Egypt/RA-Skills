# 设备通道管理文档摘要

本文件是设备通道管理 Skill 的自包含参考摘要，整理自海康云眸开放平台原始页面：

- [设备通道管理](https://pic.hik-cloud.com/opencustom/apidoc/online/open/a5982b796d354b33b8b740ba3fb98c11.html)

本技能覆盖以下接口：

- `list`：查询设备下通道列表，`GET /api/v1/open/basic/channels/list`
- `sync`：同步设备下通道，`POST /api/v1/open/basic/channels/actions/sync`
- `rename`：修改通道名称，`POST /api/v1/open/basic/channels/update`
- `sync-names`：同步设备通道名称，`POST /api/v1/open/basic/channels/actions/name/sync`

参数要点：

- 通道列表查询需要 `deviceSerial`、`pageNo`、`pageSize`
- 修改通道名称需要 `deviceSerial`、`channelNo`、`channelName`
- `syncLocal=1` 时需要设备在线，且 `channelName` 最多 32 个字符；未开启时 `channelName` 普通情况下最多 50 个字符
- 通道状态 `-1` 通常表示通道未关联设备

字段说明：

- `channelType = 通道类型`，只在 `list` 返回里出现；`10300` 表示视频通道，`10302` 表示报警输入
- `channelStatus = 通道状态`，只在 `list` 返回里出现；`0` 离线、`1` 在线、`-1` 未上报/未关联设备
- `syncLocal = 是否同步到设备本地`，只在 `rename` 请求里使用；`0` 不同步，`1` 同步到本地；`channelName` 普通情况下最多 50 个字符，`syncLocal=1` 时最多 32 个字符
