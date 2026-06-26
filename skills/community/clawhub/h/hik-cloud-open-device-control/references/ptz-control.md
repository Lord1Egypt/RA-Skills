# 云台控制

接口：

- 开始云台控制：`POST /api/v1/open/basic/channels/actions/ptz/start`
- 停止云台控制：`POST /api/v1/open/basic/channels/actions/ptz/stop`

关键参数：

- `deviceSerial`
- `channelNo`
- `direction`
- `speed`
- `mode`

取值关系：

- `mode` 默认是 `0`
- `mode=0` 时，`speed` 只能取 `0-慢`、`1-适中`、`2-快`
- `mode=1` 时，`speed` 只能取 `0~7`
- `mode` 和 `speed` 要配套理解，不能只看其中一个字段

方向枚举：

- `0-上`、`1-下`、`2-左`、`3-右`
- `4-左上`、`5-左下`、`6-右上`、`7-右下`
- `8-放大`、`9-缩小`、`10-近焦距`、`11-远焦距`

说明：

- 开始云台控制之后，必须先调用停止云台控制接口，才能继续执行其他方向操作
