# 设备布撤防

接口：

- 设置布撤防：`POST /api/v1/ezviz/devices/actions/setDefence/deviceSerial`
- 查询布撤防状态：`GET /api/v1/ezviz/devices/queryDeviceDefenceStatus`

关键参数：

- `deviceSerial`
- `isDefence`

状态取值：

- 具有防护能力设备：`0-睡眠`、`8-在家`、`16-外出`
- 普通 IPC：`0-撤防`、`1-布防`

说明：

- 设备报警消息只会在布防状态下上报
