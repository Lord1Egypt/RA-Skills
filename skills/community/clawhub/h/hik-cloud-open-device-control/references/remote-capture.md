# 远程抓图

接口：

- `POST /api/v1/open/basic/channels/actions/capture`

关键参数：

- `deviceSerial`
- `channelNo`
- `quality`（仅 NVR 支持）

说明：

- 仅适用于 IPC 或关联 IPC 的 NVR
- 不同设备或通道可并发抓图，但同一通道建议抓图间隔不低于 5 秒
- 返回值中的 `data.picUrl` 图片有效期约 2 小时
