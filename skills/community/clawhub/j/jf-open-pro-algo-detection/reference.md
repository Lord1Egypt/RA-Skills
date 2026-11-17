# 杰峰开放平台 AI 算法参考

端点：`https://api.jftechws.com`（可在 config 中改 endpoint）。所有接口 POST，Header 统一传 `uuid / appKey / timeMillis / signature`（脚本自动处理）。成功码 `code=2000`。

## 场景速查（推荐起点，模型可在此基础上自行判断）

| 业务场景 | 推荐算法 |
| --- | --- |
| 明厨亮灶/后厨监管 | 口罩检测、厨师帽检测、吸烟检测、员工进食检测、明火离人、门店清台检测 |
| 工地/车间安全生产 | 安全帽检测、静电服检测、玩手机监视、睡岗检测、离岗检测、吸烟检测 |
| 消防安全 | 室内火情检测、室外火情检测、烟火检测、明火离人、消防车道占用、灭火器检测 |
| 周界安防/园区 | 区域闯入、区域离开、攀爬识别、翻越栏杆识别、聚众识别、偷盗识别（视频版）、人形检测 |
| 门禁/访客管理 | 跌倒检测 |
| 车辆与停车管理 | 中国车牌识别、车辆识别、电动车检测、跨位停车检测、化学危险品车辆检测、渣土车检测、特种工程车检测 |
| 零售门店运营 | 门店清台检测、队列管理、广告屏未开检测、吊旗遮挡检测、物流箱占道检测、包裹检测、客情分析 |
| 环卫/园区环境 | 垃圾检测、垃圾满溢检测、过道垃圾检测、植物枯萎检测、鸟识别 |
| 宠物场景 | 宠物检测、宠物行为识别 |
| 视频质量与内容理解 | 图像质量检测、视图摘要、视觉问答、时光缩影(一日快放)、人体打码、车牌打码 |

> 注意：本技能只覆盖免底库的检测类算法（52 个）。平台另有 4 个比对类算法——智能门锁（a1000036）、陌生人识别（a1000065）、猫脸识别（s1000001）、多宠识别（a1000069）——需先在开放平台控制台维护底库并在请求体传 openSearchId，不在本技能支持范围内；用户提出这些需求时，说明须先在控制台配置底库，本技能暂不支持调用。

## 算法清单（52 个，均为免底库检测类算法）

| 算法名称 | appUuid | appName | 告警label | 底库 | 输入 | 区域 | 功能简介 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 玩手机监视 | `a1000004` | play_phone_monitoring | playing_phone | 无 | 视频流/图片 | 支持 | 检测出在工作时间玩手机的员工，支持视频流和图片检测。 |
| 口罩检测 | `a1000007` | mask_detection | no mask | 无 | 视频流/图片 | 支持 | 检测出目标区域内未戴口罩的人员，支持视频流和图片检测。 |
| 吸烟检测 | `a1000009` | smoking_detection | smoking | 无 | 视频流/图片 | 支持 | 检测出在目标区域内抽烟的人员，支持视频流和图片检测。算法支持环境：人至少漏出三分之二人体，烟需要白色外壳的烟。 |
| 睡岗检测 | `a1000010` | sleeping_detection | sleeping | 无 | 视频流/图片 | 支持 | 检测出员工上班期间在岗位睡觉的行为，支持视频流和图片检测。 |
| 离岗检测 | `a1000016` | off_duty_detection | off duty | 无 | 视频流/图片 | — | 检测出员工上班期间离岗的行为，支持视频流和图片检测。 |
| 安全帽检测 | `a1000021` | hardhat_detection | no_hardhat | 无 | 视频流/图片 | 支持 | 检测出目标区域内未穿戴安全帽的人员，支持视频流和图片检测。 |
| 厨师帽检测 | `a1000083` | chef_hat_detection | no head covering | 无 | 视频流/图片 | — | 检测出目标区域内所有未佩戴任何头部防护装备或帽子的人员目标，支持视频流和图片检测 |
| 静电服检测 | `a1000089` | anti_static_clothing_detection | anti static clothing | 无 | 图片/视频流 | — | 检测智慧能源、工业工作人员是否穿戴静电服，防止静电引发火灾 / 爆炸，适用于易燃易爆场景。 |
| 员工进食检测 | `a1000093` | office_snacking_detection | eating | 无 | 图片/视频流 | — |  |
| 室内火情检测 | `a1000013` | indoor_fire_detection | indoor_fire | 无 | 视频流 | — | 对视频场景中室内的火情进行检测，支持视频流。 |
| 室外火情检测 | `a1000017` | outdoor_fire_detection | outdoor_fire | 无 | 视频流/图片 | 支持 | 对视频场景中室外的火情进行检测，支持视频流和图片检测。 |
| 烟火检测 | `a1000064` | fire_smoke_detection | fire | 无 | 视频流/图片 | — | 对场景中火情和烟雾进行检测，支持视频流和图片检测。 |
| 消防车道占用 | `a1000085` | fire_lane_occupied | fire lane occupied | 无 | 图片/视频流 | — | 检测建筑地产、智慧工业、园区消防通道是否被占用，保障通道畅通，满足应急救援需求。 |
| 灭火器检测 | `a1000086` | fire_extinguisher_detection | 灭火器 | 无 | 图片/视频流 | — | 识别建筑地产、智慧工业、油站灭火器位置、数量及完好度，确保设备可用，辅助应急管理与安全检查。 |
| 明火离人 | `a1000095` | fire_near_detection | middle risk | 无 | 图片/视频流 | — |  |
| 区域闯入 | `a1000026` | area_invasion | area_invasion | 无 | 视频流/图片 | 支持 | 检测区域内是否有人员闯入，支持视频流和图片检测。 |
| 区域离开 | `a1000027` | area_departure | area departure | 无 | 视频流/图片 | 支持 | 检测区域内是否有人员离开，支持视频流和图片检测。 |
| 攀爬识别 | `a1000088` | climbing_wall_detection | climbing wall | 无 | 图片/视频流 | — | 检测智慧园区、建筑地产人员攀爬外墙、围栏、脚手架等行为，阻止违规攀爬，防范坠落与非法入侵。 |
| 翻越栏杆识别 | `a1000101` | railing_crossing_detection | railing crossing | 无 | 图片/视频流 | — |  |
| 聚众识别 | `a1000104` | crowd_gathering_detection | crowd gathering | 无 | 图片/视频流 | — | 检测智慧城市、园区、零售区域人员聚集情况，聚集超阈值时触发预警，辅助人群管控与客流疏导。 |
| 偷盗识别（视频版） | `a1000110` | theft_detection | thief | 无 | 图片/视频流 | — |  |
| 人形检测 | `a1000025` | human_detection | human | 无 | 视频流/图片 | 支持 | 检测出目标区域内出现的人，支持视频流和图片检测。 |
| 客情分析 | `a1000029` | gender_age | age:old \n gender:woman | 无 | 图片/视频流 | — | 检测出目标区域内出现的顾客年龄和性别。 |
| 跌倒检测 | `a1000048` | fall_detection_image | down | 无 | 图片 | — | 检测目标区域内是否有人跌倒，支持图片检测。应用场景：独居老人跌倒检测。算法要求：跌倒人体全部露出且少量遮挡（<30%）。 |
| 人形ReID | `a1000078` | human_reid | human | 无 | 视频流/图片 | — | > 检测出目标区域内出现的人（ReID、朝向、完整度），支持视频流和图片检测。 > ReID：行人重识别 |
| 电动车检测 | `a1000015` | motorcycle_detection | motorcycle | 无 | 视频流/图片 | 支持 | 检测出目标区域内出现的电动摩托车，支持视频流和图片检测。 |
| 中国车牌识别 | `a1000037` | china_lpr | 京000000 | 无 | 视频流/图片 | 支持 | 检测车牌并识别车牌号码，支持视频流和图片检测。 |
| 车辆识别 | `a1000042` | vehicle_recognition | Car | 无 | 图片/视频流 | 支持 | 车辆识别。 |
| 化学危险品车辆检测 | `a1000087` | chemical_vehicles_detection | chemical vehicles | 无 | 图片/视频流 | — | 识别智慧工业、交通、园区内的危化品车辆，实现实时监控、路径追踪与违规预警，保障公共安全。 |
| 特种工程车检测 | `a1000091` | engineering_vehicles_detection | engineering vehicles | 无 | 图片/视频流 | — |  |
| 渣土车检测 | `a1000092` | dump_truck_detection | dump truck | 无 | 图片/视频流 | — |  |
| 跨位停车检测 | `a1000102` | cross_parking_detection | cross_parking | 无 | 图片/视频流 | — |  |
| 宠物检测 | `a1000024` | pet_detection | dog | 无 | 视频流/图片 | 支持 | 检测出目标区域内出现的猫、狗、鸟，支持视频流和图片检测。 |
| 宠物行为识别 | `a1000070` | pet_action_recognition | eating | 无 | 图片/视频流 | — | 检测出宠物（猫、狗）的行为（躺卧、走动、跳跃、进食）。 |
| 包裹检测 | `a1000020` | package_detection | package | 无 | 视频流/图片 | 支持 | 检测出目标区域内出现的包裹，支持视频流和图片检测。 |
| 门店清台检测 | `a1000094` | table_uncleared_detection | messy table | 无 | 图片/视频流 | — |  |
| 广告屏未开检测 | `a1000096` | screen_play_detection | off add screen | 无 | 图片/视频流 | — |  |
| 吊旗遮挡检测 | `a1000098` | banner_block_detection | banner block | 无 | 图片/视频流 | — |  |
| 物流箱占道检测 | `a1000099` | cargo_box_detection | obstructive cargo box | 无 | 图片/视频流 | — | 支持各类物流箱检测服务，可应用于零售、餐饮等需要经常上货、补货的场景，能及时检出物流箱、并对零售门店堆积情占道况进行告警 |
| 队列管理 | `a1000100` | queue_vision_manager | in queue | 无 | 图片/视频流 | — |  |
| 垃圾检测 | `a1000005` | garbage_detection | garbage | 无 | 视频流/图片 | 支持 | 检测出目标区域内出现的垃圾，支持视频流和图片检测。 |
| 鸟识别 | `a1000030` | bird_identification | Purple_Finch | 无 | 视频流/图片 | 支持 | 识别出目标区域内出现的鸟种类，支持视频流和图片检测。 |
| 过道垃圾检测 | `a1000097` | aisle_garbage_detection | garbage | 无 | 图片/视频流 | — |  |
| 垃圾满溢检测 | `a1000103` | trash_fullness_detection | full trash | 无 | 图片/视频流 | — |  |
| 植物枯萎检测 | `a1000118` | plant_wilt_detection | wilt | 无 | 图片/视频流 | — | 检测植物是否枯萎。 |
| 时光缩影(一日快放) | `a1000031` | — | — | 无 | 图片/视频流 | — | 24小时片段浓缩，将24小时的视频浓缩成1分钟的视频，快速浏览一日的精彩片段。 |
| 图像质量检测 | `a1000035` | image_quality_detection | snow | 无 | 图片/视频流 | — | 检测摄像头的全黑、全白、偏色、条纹、雪花、模糊等质量问题。 |
| 视觉问答 | `a1000040` | jf_vqa | — | 无 | 图片 | — | 给定一张图片提出与该图片相关的问题，能返回一个正确的回答。 |
| 人体打码 | `a1000045` | human_obfuscation_image | — | 无 | 视频流/图片 | — | 对画面中的人体进行实时打码，支持视频流和图片，输出的是打码后的人体图片。 |
| 车牌打码 | `a1000046` | license_plate_obfuscation_image | — | 无 | 视频流/图片 | — | 对视频中的车牌进行实时打码，支持视频流和图片，输出的是打码后的人体图片。 |
| 视图摘要 | `jf000009` | — | person | 无 | 图片 | — | 基于视频文件或图片将所处的场景提取相关重点事件信息，以文本方式输出。 |
| 人车宠物包检测 | `a1000032` | pcpp_combined_detection | person | 无 | 视频流/图片 | 支持 | 检测出目标区域内出现的人、车、宠物、包裹，支持视频流和图片检测。 |

## 接口说明

### 开通算法 POST /openai/algorithm/application/v3/open
Body: `{"algoAppUuid": "<appUuid>", "algoAppVersion": "v1.0"}`。调用任何算法的前提，幂等。

### 调用算法分析 POST /openai/algorithm/application/v3/callApp（同步）
Body 结构：
```json
{
  "appUuid": "a1000007",
  "image": { "url": "https://xx.jpg", "sn": "设备序列号" },
  "appConfig": { "confThreshold": 0.3, "apThreshold": 0.002,
                 "includeAreas": [{"percentThreshold":0.95,"includeAreas":[{"x":1,"y":2}]}] }
}
```
- `image`：`url`（图片云链接）或 `b64`（base64）二选一；`sn` 必填（设备序列号，纯图片可占位）
- `appConfig.confThreshold`：必填，置信度阈值，默认 0.3，越低结果越多
- `includeAreas/excludeAreas`：区域圈选，仅部分算法支持（见清单「区域」列）
- 异步接口为 `pushApp`，需额外传 `callbackUrl` 接收告警回调（本技能默认用同步）

### 返回结构
```json
{"code": 2000, "msg": "success", "data": [{"appName": "mask_detection",
  "objects": [{"label": "no mask", "bbox": {"xmin":715,"xmax":1824,"ymin":130,"ymax":1267}, "confidence":0.9}],
  "image": "https://xx.jpg"}]}
```
- `data` 为空数组 → 未检出目标
- `objects[].label` 对照清单中「告警label」列理解业务含义

### 其他管理接口（了解即可，脚本未封装）
- `getAlgoExperienceList`：查算法应用列表/开通状态（test 命令用它验证签名）
- `setAnalysisConfig` / `setPushConfig`：开/关分析能力、告警推送（开通后默认开启）
- `setRequestFrequencyConfig`：请求频率限制（15秒/30秒/1分/3分/5分/10分，默认不限）

## 错误处理

| 现象 | 处理 |
| --- | --- |
| 签名错误/鉴权失败 | 运行 `test`；核对 moveCard（默认2）与 uuid/appKey/appSecret |
| 算法未开通 | 先 `python scripts/jf_client.py open <appUuid>` |
| data 为空但预期有目标 | 调低 `--conf`（如 0.2）；核对画面是否满足算法要求（如吸烟检测需人体露出2/3、白色外壳烟） |
| 404/网络错误 | 检查 config 中 endpoint 是否为 `https://api.jftechws.com` |
| 用户要求底库类算法（智能门锁/陌生人识别/猫脸识别/多宠识别） | 说明不在本技能支持范围，需先在开放平台控制台维护底库 |

状态码详解参考开发者文档「OpenAPI 请求状态码」「AI能力错误码」章节。