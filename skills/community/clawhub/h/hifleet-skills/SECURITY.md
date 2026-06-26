# 安全说明 / Security

本技能为 **HiFleet 船位、档案、航程、PSC、港口指南等查询** 的只读客户端，供 ClawHub 与用户合法查询船舶位置、档案、PSC 检查数据及港口信息。

## 行为说明

- **API 基址**：默认 `{base}` = `https://api.hifleet.com`；可通过环境变量 **`HIFLEET_API_BASE`** 覆盖（无末尾 `/`）。下文路径均相对于该基址。
- **唯一网络目标**：仅向 `{base}` 发起下列 **固定路径** 的 GET 或 POST（脚本在未设置 `HIFLEET_API_BASE` 时使用默认基址；设置后仅替换主机，**不扩大**路径范围）：
  - `{base}/position/shipSearch`（GET）
  - `{base}/position/position/get/token`（GET）
  - `{base}/position/getcallport/token`（GET/POST，航程-历史挂靠，需 `api_key`）
  - `{base}/position/getvoyagelist/token`（GET/POST，航程-历史航次简版，需 `api_key`）
  - `{base}/portofcall/getvoyages`（GET/POST，航程-历史航次详版，需 `api_key`）
  - `{base}/position/lastdeparture/token`（GET/POST，航程-上一港，需 `api_key`）
  - `{base}/position/getstop/token`（GET/POST，航程-当前停船，需 `api_key`）
  - `{base}/shiparchive/getShipArchiveWithEnginAndCompany`（GET）
  - `{base}/position/statisticzonetraffic`（海峡通航统计，**POST**，`api_key` 可选）
  - `{base}/routerisk/getAvoidRedSeaDetail/token`（集装箱红海饶航，**POST**，`api_key` 可选）
  - `{base}/position/areas/token`（区域清单，GET）
  - `{base}/position/gettraffic/token`（区域船舶，GET）
  - `{base}/pscapi/get`（船舶 PSC 检查数据，GET，需 `api_key`）
  - `{base}/pscapi/openclaw/anomalies`（PSC 统计异常列表，GET，需 `api_key`）
  - `{base}/pscapi/openclaw/anomalies/summary`（PSC 统计异常按严重度汇总，GET，需 `api_key`）
  - `{base}/pscapi/openclaw/anomalies/{id}`（PSC 统计异常单条详情，GET，需 `api_key`；`{id}` 为数字）
  - `{base}/pscapi/openclaw/stats/compare`（PSC 宏观区间对比，GET，需 `api_key`）
  - `{base}/pscapi/openclaw/stats/defects/top`（PSC 缺陷码 Top，GET，需 `api_key`）
  - `{base}/pscapi/openclaw/stats/mix/compare`（PSC 旗国/检查类型占比对比，GET，需 `api_key`）
  - `{base}/portguide/getPort/token`（港口列表/检索，GET，需 `api_key`）
  - `{base}/portguide/getPortDetail/token`（港口详情，GET，需 `api_key`）
- **无数据外传**：不向上述基址以外的地址发送数据，不上传用户文件或剪贴板。
- **api_key 用途**：环境变量 `HIFLEET_API_KEY` 中保存的值仅作为上述 API 的授权参数（海峡通航、红海饶航等为可选，用于扩展时间范围），由用户自行配置，脚本不写入、不转发至第三方。
- **无动态代码**：脚本仅使用 Python 标准库（`os`, `sys`, `argparse`, `urllib.request`, `urllib.parse`, `json` 等），无 `eval`/`exec`、无 base64 解码执行、无从网络加载代码。

## 脚本清单

| 文件 | 用途 |
|------|------|
| scripts/get_position.py | 按船名/MMSI 查船位，仅 GET 上述 position 接口；可选 `HIFLEET_API_BASE` |
| scripts/get_archive.py | 按 IMO/MMSI 查档案，仅 GET 上述 shiparchive 接口；可选 `HIFLEET_API_BASE` |
| scripts/get_strait_traffic.py | 红海/波斯湾海峡通航统计，POST statisticzonetraffic；可选 `HIFLEET_API_BASE` |
| scripts/get_avoidredsea_traffic.py | 集装箱红海饶航，POST getAvoidRedSeaDetail/token；可选 `HIFLEET_API_BASE` |
| scripts/get_areas.py | 区域清单，仅 GET position/areas/token；可选 `HIFLEET_API_BASE` |
| scripts/get_area_traffic.py | 区域船舶，仅 GET position/gettraffic/token，需 `api_key`；可选 `HIFLEET_API_BASE` |
| scripts/get_psc.py | 船舶 PSC，GET pscapi/get（及搜船时 GET position/shipSearch），需 `api_key`；可选 `HIFLEET_API_BASE` |
| scripts/get_psc_anomalies.py | PSC 统计异常，GET pscapi/openclaw/anomalies*，需 `api_key`；可选 `HIFLEET_API_BASE` |
| scripts/get_psc_openclaw_stats.py | PSC 宏观统计，GET pscapi/openclaw/stats/*，需 `api_key`；可选 `HIFLEET_API_BASE` |
| scripts/get_port.py | 港口指南，GET portguide/getPort/token、getPortDetail/token，需 `api_key`；可选 `HIFLEET_API_BASE` |

扫描或审核时可对照上述端点与行为；若需进一步说明可联系技能维护方。
