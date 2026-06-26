# 设备校时

来源链接：

- [海康云眸开放平台原始页面](https://pic.hik-cloud.com/opencustom/apidoc/online/open/7093bbc2db7a427ca5b60001caff338d.html)

接口：

- `获取设备校时配置`
- `配置设备校时`
- `获取NTP服务器配置`
- `配置NTP服务器`
- `获取指定NTP服务器配置`
- `配置指定NTP服务器参数`

API：

- `GET /api/v1/device/isapi/system/time`
- `POST /api/v1/device/isapi/system/time`
- `GET /api/v1/device/isapi/system/time/ntpServers`
- `POST /api/v1/device/isapi/system/time/ntpServers`
- `GET /api/v1/device/isapi/system/time/ntpServers/config`
- `POST /api/v1/device/isapi/system/time/ntpServers/config`

关键参数：

- `deviceSerial`
- `timeMode`：`manual` 或 `NTP`
- `ntpServerId`
- `ntpServer.id`
- `ntpServer.addressingFormatType`
- `ntpServer.hostName`
- `ntpServer.ipAddress`
- `ntpServer.ipv6Address`
- `ntpServer.portNo`
- `ntpServer.synchronizeInterval`

说明：

- `timeMode` 决定设备采用手动校时还是 NTP 校时
- `ntpServer.addressingFormatType` 为 `hostname` 时主要使用 `hostName`
- `ntpServer.addressingFormatType` 为 `ipaddress` 时主要使用 `ipAddress`，IPv6 场景可使用 `ipv6Address`
- `hostName`、`ipAddress`、`ipv6Address` 要跟 `addressingFormatType` 配套，尽量不要混填
- `synchronizeInterval` 的单位是分钟
