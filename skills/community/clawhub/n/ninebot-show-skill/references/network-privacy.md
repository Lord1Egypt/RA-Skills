# 网络请求与隐私

本 Skill 自身不直连九号业务 API；车辆数据由本机已经登录的 `ninecli` 获取。以下是 Skill 代码直接访问的第三方网络服务。

| 服务 | 地址 | 运行时参数/路径 | 可能包含的信息 |
|---|---|---|---|
| 高德逆地理编码 | `https://restapi.amap.com/v3/geocode/regeo` | `key`, `location`, `output`, `radius`（`locate.py` 另含 `extensions`） | 高德 Web Service Key、车辆精确坐标 |
| 高德静态地图 | `https://restapi.amap.com/v3/staticmap` | `key`, `location`, `zoom`, `size`, `scale`；位置图还含 `markers`, `traffic` | 高德 Web Service Key、车辆坐标或骑行区域中心 |
| 高德 marker URI | `https://uri.amap.com/marker` | `position`, `name`, `callnative` | 精确坐标；默认不输出，仅显式 `--include-map-link` 时生成 |
| wttr.in | `https://wttr.in/<location>` | `format=j1` | 配置中的天气地点（默认是城市名，不使用车辆 GPS） |
| OpenStreetMap 瓦片 | `https://tile.openstreetmap.org/<z>/<x>/<y>.png` | URL 路径中的瓦片坐标 | 可推断所请求地图区域；服务端也可看到客户端 IP |

## 保护措施

- 公开 Skill 文件不包含真实 Key、Token、Cookie、SN、骑行 ID 或私人坐标。
- 高德请求失败时不回显完整 URL，避免 Key 和坐标进入 Agent 日志。
- `privacy=district` 的 JSON 只返回省/市/区县，不再附带原始坐标、详细 POI、街道信息或精确地图 URL。
- `privacy=off` 不读取/展示车辆位置，也不调用高德逆地理编码。
- `privacy=coordinates` 会输出坐标，但不会调用高德逆地理编码；地图截图属于单独显式操作，会向地图服务发送位置。
- `privacy=district` 会在请求高德前把 GCJ-02 坐标圆整到 2 位小数（约公里级），不再发送米级精确坐标；如不希望向第三方地图服务发送任何位置，请使用 `privacy=off`。
