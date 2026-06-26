# 设备基础管理文档摘要

本文件是设备基础管理 Skill 的自包含参考摘要，整理自海康云眸开放平台原始页面：

- [设备基础管理](https://pic.hik-cloud.com/opencustom/apidoc/online/open/d1856283d9d944719474b24b6374e351.html)

本技能覆盖以下接口：

- `create`：注册设备，`POST /api/v1/open/basic/devices/create`
- `delete`：删除设备，`POST /api/v1/open/basic/devices/delete?deviceSerial=...`
- `rename`：修改设备名称，`POST /api/v1/open/basic/devices/update`
- `get`：查询单个设备信息，`GET /api/v1/open/basic/devices/get`
- `list`：查询设备列表，`GET /api/v1/open/basic/devices/list`
- `count`：获取设备总数，`GET /api/v1/open/basic/devices/actions/deviceCount`
- `status`：查询设备状态，`GET /api/v1/ezviz/devices/queryDeviceStatus`
- `reboot`：设备重启，`POST /api/v1/open/basic/devices/actions/system/reboot`

参数要点：

- 注册设备需要 `deviceSerial`、`groupNo`、`validateCode`
- 查询单个设备信息可选 `needDefence=true`
- 查询设备列表要求 `groupNo`、`pageNo`、`pageSize`
- 设备状态查询目前仅支持萤石设备
- 设备重启是高风险操作，应确认业务影响

关键状态字段判读：

- `deviceStatus`：`0` 离线、`1` 在线，适用于 `get` / `list`
- `defence`：只在 `get + needDefence=true` 时返回；具防护能力设备是 `0` 睡眠、`8` 在家、`16` 外出，普通 IPC 是 `0` 撤防、`1` 布防
- `privacyStatus`：`0` 关闭、`1` 打开、`-1` 初始值、`2` 不支持、`-2` 未上报/不支持
- `pirStatus`：`1` 启用、`0` 禁用、`-1` 初始值、`2` 不支持、`-2` 未上报/不支持
- `alarmSoundMode`：`0` 短叫、`1` 长叫、`2` 静音、`3` 自定义语音、`-1` 未上报/不支持
- `cloudStatus`：`-2` 不支持、`-1` 未开通、`0` 未激活、`1` 激活、`2` 过期
- `diskState` / `nvrDiskState`：状态串按盘位拼接，`0` 正常、`1` 存储介质错、`2` 未格式化、`3` 正在格式化；`nvrDiskState` 额外支持 `-2` 未关联
