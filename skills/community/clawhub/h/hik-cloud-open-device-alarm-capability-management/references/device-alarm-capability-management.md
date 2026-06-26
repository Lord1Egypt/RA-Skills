# 设备报警能力管理文档摘要

本文件是设备报警能力管理 Skill 的自包含参考摘要，整理自海康云眸开放平台原始页面：

- [设备报警能力管理](https://pic.hik-cloud.com/opencustom/apidoc/online/open/f8cbf864c4ca4395909dad225902a6ee.html)

本技能覆盖以下接口：

- `list`：获取设备常规报警能力列表，`GET /api/v1/open/basic/abilities/list`
- `update-status`：修改报警能力状态，`POST /api/v1/open/basic/abilities/updateStatus`
- `intelligence-switch`：设备智能检测开关状态，`POST /v1/carrier/charon/storage/open/setIntelligenceDetectionSwitch`

关键返回字段：

- `list`：顶层 `code`、`message`、`data`；`data[]` 重点看 `deviceId`、`channelId`、`abilityCode`、`status`
- `update-status`：顶层 `code`、`message`
- `intelligence-switch`：顶层 `code`、`success`；`message` 为可选提示字段

字段语义：

- `abilityCode` = 常规报警能力编码，只适用于 `list` / `update-status`
- `status` = 常规报警能力状态，只适用于 `list` / `update-status`，`0` 关/撤防、`1` 开/布防、`-1` 未知
- `type` = 智能检测开关类型，只适用于 `intelligence-switch`，`302` 人形过滤、`304` 人脸抠图，不传默认人形过滤
- `abilityCode` 和 `type` 不是同一套枚举，不要混用

常见 `abilityCode` 值：

- `10600` 移动侦测
- `10602` 视频遮挡
- `10610` 客流统计
- `10627` 区域入侵
- `10620` 红外探测
- `10621` 双鉴探测
- `10622` 震动探测
- `10623` 玻璃探测
- `10624` 门磁开关探测
- `10625` 紧急按钮
- `10626` 红外对射探测
- `-1` 未知

参数要点：

- `list` 仅需要 `deviceSerial`
- `update-status` 需要 `channelId`、`abilityCode`、`status`
- `intelligence-switch` 需要 `deviceSerial` 和 `enable`，`channelNo`、`type` 为可选项
- 智能检测开关接口仅适用于萤石设备
