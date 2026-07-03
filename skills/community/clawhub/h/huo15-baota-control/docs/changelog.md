# huo15-baota-control 版本历史

## v1.0.0 (2026-06-25)
- 首版：宝塔 BT-Panel HTTP API 控制能力。
- bt_api.py：token 签名(md5(time+md5(token)))+浏览器UA+通用 raw + 高层助手(sysinfo/disk/network/sites/site_stop/site_start/databases)。
- enable_api.py：在服务器上正式开启宝塔 API + 设白名单 + 取明文 token。
- 多面板配置 ~/.huo15/baota.json；references/endpoints.md 端点速查。
- 实测宝塔 11.8 通过(本地 + 经隧道远程)。
