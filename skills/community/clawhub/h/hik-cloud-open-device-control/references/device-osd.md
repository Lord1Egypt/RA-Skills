# 设备 OSD

本页包含三类接口：

- 设置设备 OSD 名称：`POST /api/v1/ezviz/devices/actions/setOsdName`
- 查询设备 OSD 名称：`GET /api/v1/ezviz/devices/actions/getOsdName`
- 设备 OSD 配置：`POST /api/v1/ezviz/devices/osd/config`

关键参数：

- `deviceSerial`
- `channelNo`
- `osdName`
- `channelNameOsd.enabled`
- `channelNameOsd.positionX`
- `channelNameOsd.positionY`

说明：

- OSD 为画面叠加信息
- OSD 配置接口仅海康设备支持
