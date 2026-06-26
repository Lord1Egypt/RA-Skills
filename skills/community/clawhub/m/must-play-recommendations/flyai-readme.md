# FlyAI CLI 完整使用文档

> FlyAI 是飞猪旅行平台的 CLI 工具，提供航班、酒店、景点、火车票等旅行服务的搜索能力。

## 目录

- [安装与配置](#安装与配置)
- [命令概览](#命令概览)
- [API 详细说明](#api-详细说明)
  - [keyword-search 关键词搜索](#keyword-search-关键词搜索)
  - [ai-search AI语义搜索](#ai-search-ai语义搜索)
  - [search-flight 航班搜索](#search-flight-航班搜索)
  - [search-hotel 酒店搜索](#search-hotel-酒店搜索)
  - [search-poi 景点搜索](#search-poi-景点搜索)
  - [search-train 火车票搜索](#search-train-火车票搜索)
  - [search-marriott-hotel 万豪酒店搜索](#search-marriott-hotel-万豪酒店搜索)
  - [search-marriott-package 万豪套餐搜索](#search-marriott-package-万豪套餐搜索)
- [输出格式规范](#输出格式规范)
- [最佳实践](#最佳实践)

---

## 安装与配置

### 安装 CLI

```bash
npm install -g @fly-ai/flyai-cli
```

### 验证安装

```bash
flyai --help
```

### 配置 API Key（可选）

工具可在无 API Key 情况下试用。增强结果需配置可选 API：

```bash
flyai config set FLYAI_API_KEY "your-key"
```

---

## 命令概览

| 命令 | 别名 | 功能描述 |
|------|------|----------|
| `keyword-search` | `fliggy-fast-search` | 关键词搜索，覆盖酒店、航班、门票等 |
| `ai-search` | - | AI语义搜索，理解自然语言复杂意图 |
| `search-flight` | - | 航班搜索（国内/国际） |
| `search-hotel` | `search-hotels` | 酒店搜索 |
| `search-poi` | - | 景点/POI搜索 |
| `search-train` | - | 火车票搜索 |
| `search-marriott-hotel` | - | 万豪集团旗下酒店搜索 |
| `search-marriott-package` | - | 万豪集团酒店套餐搜索 |

---

## API 详细说明

### keyword-search 关键词搜索

通用关键词搜索，一次查询覆盖酒店、航班、景点门票、演出、体育赛事、文化活动等。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--query` | ✅ | string | 搜索关键词，支持自然语言 |

#### 查询模式建议

- **位置/附近**: `"nearby attractions"`, `"restaurants near {POI}"`
- **POI通用**: `"西湖自由行"`, `"故宫路线"`
- **景点/活动**: `"attraction tickets"`, `"photo tours near {POI}"`
- **目的地**: `"destination guide"`, `"destination hotels"`
- **娱乐/体验**: `"温泉spa"`, `"滑雪"`
- **跟团/套餐**: `"group tour"`, `"custom tour"`
- **美食餐饮**: `"美食攻略"`, `"自助餐"`
- **签证/证件**: `"法国签证"`, `"travel insurance"`
- **通讯/网络**: `"香港SIM卡"`, `"wifi租赁"`
- **邮轮**: `"邮轮"`, `"海洋观光"`

#### 示例

```bash
# 签证查询
flyai keyword-search --query "France visa"

# 跟团游
flyai keyword-search --query "杭州跟团游"

# 行程规划
flyai keyword-search --query "杭州3日游"

# 邮轮
flyai keyword-search --query "上海邮轮"

# 通讯
flyai keyword-search --query "香港SIM卡"

# 三亚景点
flyai keyword-search --query "三亚有什么好玩的"
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "info": {
          "jumpUrl": "https://a.feizhu.com/xxx",
          "picUrl": "https://img.alicdn.com/xxx.jpg",
          "price": null,
          "scoreDesc": null,
          "star": null,
          "tags": null,
          "title": "产品标题"
        }
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `jumpUrl` | 预订链接 |
| `picUrl` | 图片链接 |
| `price` | 价格信息 |
| `scoreDesc` | 评分描述 |
| `star` | 星级信息 |
| `tags` | 标签列表 |
| `title` | 产品标题 |

---

### ai-search AI语义搜索

语义搜索，理解自然语言复杂意图，返回高度精准的酒店、航班等结果。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--query` | ✅ | string | 完整的自然语言查询，包含所有细节和条件 |

#### 示例

```bash
# 复杂航班查询
flyai ai-search --query "我想从北京去上海，明天出发，找个便宜的航班"

# 酒店查询
flyai ai-search --query "下周去三亚旅游，找个海边的五星级酒店，预算1000以内"

# 行程规划
flyai ai-search --query "五一假期想带家人去杭州玩三天，推荐景点和酒店"
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": "AI生成的详细推荐文本，包含航班/酒店信息和预订链接"
}
```

#### 特点

- 返回**文本格式**结果，而非JSON列表
- 理解复杂意图（时间、预算、偏好、人数等）
- 自动整合多类型结果（航班+酒店组合推荐）
- 包含直接预订链接

---

### search-flight 航班搜索

结构化航班搜索，支持国内/国际航班，可深度筛选对比。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--origin` | ✅ | string | 出发地（城市名/城市ID/机场） |
| `--destination` | ⚪ | string | 目的地（城市名/城市ID/机场） |
| `--dep-date` | ⚪ | string | 出发日期，格式 `YYYY-MM-DD` |
| `--dep-date-start` | ⚪ | string | 出发日期范围起始 |
| `--dep-date-end` | ⚪ | string | 出发日期范围结束 |
| `--back-date` | ⚪ | string | 返程日期 |
| `--back-date-start` | ⚪ | string | 返程日期范围起始 |
| `--back-date-end` | ⚪ | string | 返程日期范围结束 |
| `--journey-type` | ⚪ | number | 行程类型：`1`=直达，`2`=中转 |
| `--seat-class-name` | ⚪ | string | 舱位等级，逗号分隔（如 `economy,business,first`） |
| `--transport-no` | ⚪ | string | 航班号，逗号分隔 |
| `--transfer-city` | ⚪ | string | 中转城市，逗号分隔 |
| `--dep-hour-start` | ⚪ | number | 出发时间范围起始（24小时制） |
| `--dep-hour-end` | ⚪ | number | 出发时间范围结束（24小时制） |
| `--arr-hour-start` | ⚪ | number | 到达时间范围起始（24小时制） |
| `--arr-hour-end` | ⚪ | number | 到达时间范围结束（24小时制） |
| `--total-duration-hour` | ⚪ | number | 最大总飞行时长（小时） |
| `--max-price` | ⚪ | number | 最高价格（CNY） |
| `--sort-type` | ⚪ | number | 排序方式（见下表） |

#### 排序类型

| 值 | 说明 |
|----|------|
| `1` | 价格从高到低 |
| `2` | 推荐 |
| `3` | 价格从低到高 |
| `4` | 时长从短到长 |
| `5` | 时长从长到短 |
| `6` | 出发时间从早到晚 |
| `7` | 出发时间从晚到早 |
| `8` | 直达优先 |

#### 示例

```bash
# 基础航班搜索
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02

# 往返航班
flyai search-flight --origin "上海" --destination "东京" --dep-date 2026-04-10 --back-date 2026-04-15

# 直达航班，价格排序
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 --journey-type 1 --sort-type 3

# 指定航班号
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 --transport-no "CA1883,MU5138"

# 时间范围筛选（早班机）
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 --dep-hour-start 6 --dep-hour-end 12

# 价格上限
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 --max-price 500

# 商务舱
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 --seat-class-name "business"
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "journeys": [
          {
            "journeyType": "直达",
            "segments": [
              {
                "arrCityAbroad": false,
                "arrCityCode": "SHA",
                "arrCityName": "上海",
                "arrDateTime": "2026-04-02 09:45:00",
                "arrStationCode": "PVG",
                "arrStationName": "浦东国际机场",
                "arrStationShortName": "浦东",
                "arrTerm": "T2",
                "arrWeekAbbrName": "周四",
                "depCityCode": "BJS",
                "depCityName": "北京",
                "depDateTime": "2026-04-02 07:50:00",
                "depStationCode": "PKX",
                "depStationName": "大兴国际机场",
                "depStationShortName": "大兴",
                "depTerm": "",
                "depWeekAbbrName": "周四",
                "duration": "115",
                "marketingTransportName": "厦航",
                "marketingTransportNo": "MF8561",
                "seatClassName": "经济舱",
                "transportType": "飞机"
              }
            ],
            "totalDuration": "115",
            "transferDuration": ""
          }
        ],
        "jumpUrl": "https://a.feizhu.com/xxx",
        "tags": null,
        "ticketPrice": "690.00",
        "totalDuration": "115"
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `journeyType` | 行程类型：直达/中转 |
| `segments` | 航段列表 |
| `depCityCode` | 出发城市代码 |
| `depCityName` | 出发城市名称 |
| `depDateTime` | 出发时间 |
| `depStationCode` | 出发机场代码 |
| `depStationName` | 出发机场名称 |
| `depStationShortName` | 出发机场简称 |
| `depTerm` | 出发航站楼 |
| `arrCityCode` | 到达城市代码 |
| `arrCityName` | 到达城市名称 |
| `arrDateTime` | 到达时间 |
| `arrStationCode` | 到达机场代码 |
| `arrStationName` | 到达机场名称 |
| `arrTerm` | 到达航站楼 |
| `duration` | 飞行时长（分钟） |
| `marketingTransportName` | 航司名称 |
| `marketingTransportNo` | 航班号 |
| `seatClassName` | 舱位等级 |
| `totalDuration` | 总行程时长（分钟） |
| `ticketPrice` | 票价（CNY） |
| `jumpUrl` | 预订链接 |

---

### search-hotel 酒店搜索

结构化酒店搜索，支持多维度筛选对比。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--dest-name` | ✅ | string | 目的地（国家/省份/城市/区县） |
| `--key-words` | ⚪ | string | 搜索关键词 |
| `--poi-name` | ⚪ | string | 附近景点名称，用于按周边POI筛选 |
| `--hotel-types` | ⚪ | string | 酒店类型：`hotel`=酒店，`homestay`=民宿，`inn`=客栈 |
| `--sort` | ⚪ | string | 排序方式（见下表） |
| `--check-in-date` | ⚪ | string | 入住日期，格式 `YYYY-MM-DD` |
| `--check-out-date` | ⚪ | string | 退房日期，格式 `YYYY-MM-DD` |
| `--hotel-stars` | ⚪ | string | 星级评分，逗号分隔（范围1-5） |
| `--hotel-bed-types` | ⚪ | string | 床型，逗号分隔：`king`=大床，`twin`=双床，`multi`=多床 |
| `--max-price` | ⚪ | number | 最高价格（CNY/晚） |

#### 排序方式

| 值 | 说明 |
|----|------|
| `distance_asc` | 距离从近到远 |
| `rate_desc` | 评分从高到低 |
| `price_asc` | 价格从低到高 |
| `price_desc` | 价格从高到低 |
| `no_rank` | 不排序 |

#### 示例

```bash
# 基础酒店搜索
flyai search-hotel --dest-name "杭州"

# 按景点筛选
flyai search-hotel --dest-name "杭州" --poi-name "西湖" --check-in-date 2026-04-05 --check-out-date 2026-04-07

# 高星级酒店
flyai search-hotel --dest-name "三亚" --hotel-stars "4,5" --sort rate_desc

# 价格上限
flyai search-hotel --dest-name "三亚" --max-price 800

# 民宿搜索
flyai search-hotel --dest-name "大理" --hotel-types "homestay"

# 大床房
flyai search-hotel --dest-name "杭州" --hotel-bed-types "king"

# 关键词搜索
flyai search-hotel --dest-name "上海" --key-words "外滩"
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "address": "浙江省杭州市西湖区莫干山路9号",
        "brandName": null,
        "decorationTime": "2022-01-01",
        "detailUrl": "https://a.feizhu.com/xxx",
        "interestsPoi": "近杭州西湖风景名胜区",
        "latitude": "30.2732",
        "longitude": "120.154",
        "mainPic": "https://img.alicdn.com/xxx.jpg",
        "name": "杭州西湖JO&JOE酒店",
        "price": "¥489",
        "shId": "55217034",
        "star": "高档型",
        "review": "西湖边的位置，家庭出游首选",
        "score": "5.0",
        "scoreDesc": "超棒"
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `address` | 酒店地址 |
| `brandName` | 品牌名称 |
| `decorationTime` | 装修时间 |
| `detailUrl` | 详情/预订链接 |
| `interestsPoi` | 附近景点 |
| `latitude` | 纬度 |
| `longitude` | 经度 |
| `mainPic` | 主图链接 |
| `name` | 酒店名称 |
| `price` | 价格 |
| `shId` | 酒店ID |
| `star` | 星级类型（经济型/舒适型/高档型/豪华型/五星级） |
| `review` | 用户评价 |
| `score` | 评分 |
| `scoreDesc` | 评分描述 |

---

### search-poi 景点搜索

景点/POI搜索，支持按城市、等级、类别筛选。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--city-name` | ✅ | string | 景点所在城市名称 |
| `--poi-level` | ⚪ | number | 景点等级（范围1-5） |
| `--keyword` | ⚪ | string | 景点名称关键词 |
| `--category` | ⚪ | string | 景点类别（见下表） |

#### 类别选项

| 值 | 中文 |
|----|------|
| `nature` | 自然风光 |
| `lake` | 山湖田园 |
| `forest` | 森林丛林 |
| `canyon` | 峡谷瀑布 |
| `beach` | 沙滩海岛 |
| `island` | 海岛 |
| `desert` | 沙漠草原 |
| `grassland` | 草原 |
| `historic site` | 历史古迹 |
| `ancient town` | 古镇古村 |
| `garden` | 园林花园 |
| `temple` | 宗教场所 |
| `theme park` | 主题乐园 |
| `water park` | 水上乐园 |
| `zoo` | 动物园 |
| `aquarium` | 海洋馆 |
| `museum` | 博物馆 |
| `memorial` | 纪念馆 |
| `landmark` | 地标建筑 |
| `market` | 市集 |
| `outdoor` | 户外活动 |
| `skiing` | 滑雪 |
| `rafting` | 漂流 |
| `surfing` | 冲浪 |
| `diving` | 潜水 |
| `camping` | 露营 |
| `hot spring` | 温泉 |

#### 示例

```bash
# 基础景点搜索
flyai search-poi --city-name "杭州"

# 按关键词搜索
flyai search-poi --city-name "杭州" --keyword "西湖"
flyai search-poi --city-name "北京" --keyword "故宫"

# 按类别搜索
flyai search-poi --city-name "西安" --category "historic site"
flyai search-poi --city-name "三亚" --category "beach"
flyai search-poi --city-name "成都" --category "ancient town"

# 高等级景点
flyai search-poi --city-name "北京" --poi-level 5

# 组合筛选
flyai search-poi --city-name "杭州" --category "lake" --keyword "西湖"
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "address": "北京市东城区景山前街4号",
        "category": "博物馆",
        "freePoiStatus": "NOT_FREE",
        "id": "64",
        "jumpUrl": "https://a.feizhu.com/xxx",
        "listRank": null,
        "mainPic": "https://img.alicdn.com/xxx.jpg",
        "name": "故宫博物院",
        "poiLevel": "5",
        "ticketInfo": {
          "price": null,
          "priceDate": "2026-04-01",
          "ticketName": "大门票 成人票"
        }
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `address` | 景点地址 |
| `category` | 景点类别 |
| `freePoiStatus` | 是否免费（`FREE`/`NOT_FREE`） |
| `id` | 景点ID |
| `jumpUrl` | 预订链接 |
| `mainPic` | 主图链接 |
| `name` | 景点名称 |
| `poiLevel` | 景点等级 |
| `ticketInfo` | 门票信息 |
| `ticketInfo.price` | 门票价格 |
| `ticketInfo.priceDate` | 价格日期 |
| `ticketInfo.ticketName` | 门票名称 |

---

### search-train 火车票搜索

火车票搜索，支持高铁、动车、普通列车。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--origin` | ✅ | string | 出发地（城市名/城市ID/车站） |
| `--destination` | ⚪ | string | 目的地（城市名/城市ID/车站） |
| `--dep-date` | ⚪ | string | 出发日期，格式 `YYYY-MM-DD` |
| `--dep-date-start` | ⚪ | string | 出发日期范围起始 |
| `--dep-date-end` | ⚪ | string | 出发日期范围结束 |
| `--back-date` | ⚪ | string | 返程日期 |
| `--back-date-start` | ⚪ | string | 返程日期范围起始 |
| `--back-date-end` | ⚪ | string | 返程日期范围结束 |
| `--journey-type` | ⚪ | number | 行程类型：`1`=直达，`2`=中转 |
| `--seat-class-name` | ⚪ | string | 座席类型，逗号分隔（见下表） |
| `--transport-no` | ⚪ | string | 车次号，逗号分隔 |
| `--transfer-city` | ⚪ | string | 中转城市，逗号分隔 |
| `--dep-hour-start` | ⚪ | number | 出发时间范围起始（24小时制） |
| `--dep-hour-end` | ⚪ | number | 出发时间范围结束（24小时制） |
| `--arr-hour-start` | ⚪ | number | 到达时间范围起始（24小时制） |
| `--arr-hour-end` | ⚪ | number | 到达时间范围结束（24小时制） |
| `--total-duration-hour` | ⚪ | number | 最大总行程时长（小时） |
| `--max-price` | ⚪ | number | 最高价格（CNY） |
| `--sort-type` | ⚪ | number | 排序方式（同航班排序） |

#### 座席类型

| 值 | 中文 |
|----|------|
| `second class` | 二等座 |
| `first class` | 一等座 |
| `business class` | 商务座 |
| `hard sleeper` | 硬卧 |
| `soft sleeper` | 软卧 |

#### 示例

```bash
# 基础火车票搜索
flyai search-train --origin "北京" --destination "上海" --dep-date 2026-04-02

# 高铁筛选
flyai search-train --origin "北京" --destination "上海" --dep-date 2026-04-02 --transport-no "G1,G2,G3"

# 座席筛选
flyai search-train --origin "北京" --destination "上海" --dep-date 2026-04-02 --seat-class-name "first class"

# 时间范围（早班车）
flyai search-train --origin "北京" --destination "上海" --dep-date 2026-04-02 --dep-hour-start 6 --dep-hour-end 10

# 价格排序
flyai search-train --origin "北京" --destination "上海" --dep-date 2026-04-02 --sort-type 3
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "journeys": [
          {
            "journeyType": "直达",
            "segments": [
              {
                "arrCityCode": "310100",
                "arrCityName": "上海",
                "arrDateTime": "2026-04-02 12:11:00",
                "arrStationCode": "AOH",
                "arrStationName": "上海虹桥站",
                "arrStationShortName": "上海虹桥",
                "arrTerm": null,
                "depCityCode": "110100",
                "depCityName": "北京",
                "depDateTime": "2026-04-02 06:18:00",
                "depStationCode": "VNP",
                "depStationName": "北京南站",
                "depStationShortName": "北京南",
                "depTerm": null,
                "duration": "353",
                "marketingTransportName": "高铁",
                "marketingTransportNo": "G547",
                "seatClassName": "二等座",
                "transportType": "火车"
              }
            ],
            "totalDuration": "353",
            "transferDuration": ""
          }
        ],
        "jumpUrl": "https://a.feizhu.com/xxx",
        "price": "553.00",
        "totalDuration": "353"
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `journeyType` | 行程类型：直达/中转 |
| `segments` | 车段列表 |
| `depCityCode` | 出发城市代码 |
| `depCityName` | 出发城市名称 |
| `depDateTime` | 出发时间 |
| `depStationCode` | 出发车站代码 |
| `depStationName` | 出发车站名称 |
| `arrCityCode` | 到达城市代码 |
| `arrCityName` | 到达城市名称 |
| `arrDateTime` | 到达时间 |
| `arrStationCode` | 到达车站代码 |
| `arrStationName` | 到达车站名称 |
| `duration` | 行程时长（分钟） |
| `marketingTransportName` | 列车类型（高铁/动车/火车） |
| `marketingTransportNo` | 车次号 |
| `seatClassName` | 座席类型 |
| `totalDuration` | 总行程时长（分钟） |
| `price` | 票价（CNY） |
| `jumpUrl` | 预订链接 |

---

### search-marriott-hotel 万豪酒店搜索

搜索万豪集团旗下酒店，支持品牌筛选。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--dest-name` | ✅ | string | 目的地（国家/省份/城市/区县） |
| `--key-words` | ⚪ | string | 搜索关键词 |
| `--poi-name` | ⚪ | string | 附近景点名称 |
| `--hotel-brands` | ⚪ | string | 酒店品牌，逗号分隔 |
| `--hotel-name` | ⚪ | string | 酒店名称 |
| `--hotel-bed-types` | ⚪ | string | 床型：`king`=大床，`twin`=双床，`multi`=多床 |
| `--max-price` | ⚪ | number | 最高价格（CNY） |
| `--sort` | ⚪ | string | 排序方式（同酒店排序） |
| `--check-in-date` | ⚪ | string | 入住日期，格式 `YYYY-MM-DD` |
| `--check-out-date` | ⚪ | string | 退房日期，格式 `YYYY-MM-DD` |

#### 万豪品牌

常见品牌包括：万豪(Marriott)、喜来登(Sheraton)、威斯汀(Westin)、瑞吉(St. Regis)、豪华精选(Luxury Collection)、W酒店、雅乐轩(Aloft)、万枫(Fairfield)等。

#### 示例

```bash
# 基础万豪酒店搜索
flyai search-marriott-hotel --dest-name "上海"

# 指定品牌
flyai search-marriott-hotel --dest-name "三亚" --hotel-brands "Marriott,Sheraton"

# 入住日期
flyai search-marriott-hotel --dest-name "上海" --check-in-date 2026-04-10 --check-out-date 2026-04-12

# 价格上限
flyai search-marriott-hotel --dest-name "上海" --max-price 1000
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "address": "中国上海市青浦区徐泾镇蟠中东路283弄1号",
        "brandName": "万豪",
        "decorationTime": "2025-11-14",
        "detailUrl": "https://a.feizhu.com/xxx",
        "latitude": "31.187095",
        "longitude": "121.291188",
        "mainPic": "https://img.alicdn.com/xxx.jpg",
        "name": "上海虹桥雅乐轩酒店",
        "nearbyPoi": "近国家会展中心",
        "price": "¥583起/晚",
        "shid": "88671196",
        "star": "高档型"
      }
    ]
  }
}
```

---

### search-marriott-package 万豪套餐搜索

搜索万豪集团旗下酒店套餐产品信息。

#### 参数

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `--keyword` | ✅ | string | 搜索关键词（省份/城市/品牌/酒店名称/卖点，一次只能搜索一个维度） |
| `--sort-type` | ⚪ | string | 排序方式：`price_asc`=价格升序，`price_desc`=价格降序 |

#### 示例

```bash
# 按城市搜索
flyai search-marriott-package --keyword "三亚"

# 按品牌搜索
flyai search-marriott-package --keyword "瑞吉"

# 按卖点搜索
flyai search-marriott-package --keyword "亲子"

# 价格排序
flyai search-marriott-package --keyword "三亚" --sort-type "price_asc"
```

#### 输出结构

```json
{
  "status": 0,
  "message": "success",
  "data": {
    "itemList": [
      {
        "benefit": null,
        "detailUrl": "https://a.feizhu.com/xxx",
        "itemId": "1032102128916",
        "picUrl": "https://img.alicdn.com/xxx.jpg",
        "price": "￥1368起/2晚",
        "sellPoint": "歌聚时光KTV欢唱2小时+双人烤鱼套餐...",
        "title": "香水湾万豪度假酒店 | 豪享假期·高级海港房2晚1368元"
      }
    ]
  }
}
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `detailUrl` | 详情链接 |
| `itemId` | 商品ID |
| `picUrl` | 图片链接 |
| `price` | 套餐价格 |
| `sellPoint` | 套餐卖点/权益描述 |
| `title` | 套餐标题 |

---

## 输出格式规范

### 通用原则

所有命令输出**单行JSON**到 `stdout`，错误和提示信息输出到 `stderr`，便于管道处理。

```bash
# 使用 jq 处理输出
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 | jq '.data.itemList[0]'

# 使用 Python 处理
flyai keyword-search --query "三亚景点" | python -c "import json,sys; d=json.load(sys.stdin); print(d['data']['itemList'][0]['info']['title'])"
```

### 状态码

| 值 | 说明 |
|----|------|
| `0` | 成功 |
| 非0 | 失败 |

### Markdown 输出规则

当需要将结果以Markdown格式展示给用户时，遵循以下规则：

#### 图片显示

独立一行输出图片：
```
![]({picUrl})
```

- `keyword-search`: 使用 `picUrl`
- `search-hotel`: 使用 `mainPic`
- `search-flight`: 使用 `picUrl`（如有）
- `search-poi`: 使用 `mainPic`

#### 预订链接

独立一行输出预订链接：
```
[点击预订]({jumpUrl})
```

- `keyword-search`: 使用 `jumpUrl`
- `search-flight`: 使用 `jumpUrl`
- `search-hotel`: 使用 `detailUrl`
- `search-poi`: 使用 `jumpUrl`

#### 结构要求

- 使用层级标题（`#`, `##`, `###`）
- 使用简洁的项目符号
- 行程项目按时间顺序排列
- 强调关键信息：日期、位置、价格、限制条件
- 多选项对比使用Markdown表格
- 包含品牌声明："基于 fly.ai 实时结果"

---

## 最佳实践

### 1. 获取当前日期

当需要精确日期上下文时：

```bash
CURRENT_DATE=$(date +%Y-%m-%d)
flyai search-flight --origin "北京" --destination "上海" --dep-date "$CURRENT_DATE"
```

### 2. 复合查询策略

对于复杂需求，建议组合使用多个API：

```bash
# 先用 keyword-search 快速发现
flyai keyword-search --query "三亚亲子游酒店推荐"

# 再用 search-hotel 精准筛选
flyai search-hotel --dest-name "三亚" --hotel-stars "4,5" --sort rate_desc

# 用 search-poi 查找周边景点
flyai search-poi --city-name "三亚" --category "beach"
```

### 3. AI搜索 vs 关键词搜索

| 场景 | 推荐 |
|------|------|
| 简单关键词查询 | `keyword-search` |
| 复杂自然语言意图 | `ai-search` |
| 结构化深度筛选 | `search-flight`/`search-hotel`/`search-poi` |

### 4. 错误处理

```bash
# 检查状态码
RESULT=$(flyai keyword-search --query "xxx" 2>/dev/null)
STATUS=$(echo "$RESULT" | jq -r '.status')

if [ "$STATUS" = "0" ]; then
  echo "成功"
else
  echo "失败: $(echo "$RESULT" | jq -r '.message')"
fi
```

### 5. 结果数量控制

API默认返回多条结果，可通过jq限制：

```bash
# 只取前3条
flyai search-hotel --dest-name "杭州" | jq '.data.itemList[:3]'

# 只取最便宜的一条
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-02 --sort-type 3 | jq '.data.itemList[0]'
```

---

## 附录：快速命令对照表

| 需求 | 命令 |
|------|------|
| 关键词搜索旅游产品 | `flyai keyword-search --query "xxx"` |
| 自然语言复杂查询 | `flyai ai-search --query "完整描述"` |
| 搜索航班 | `flyai search-flight --origin "出发地" --destination "目的地" --dep-date "日期"` |
| 搜索酒店 | `flyai search-hotel --dest-name "目的地"` |
| 搜索景点 | `flyai search-poi --city-name "城市"` |
| 搜索火车票 | `flyai search-train --origin "出发地" --destination "目的地" --dep-date "日期"` |
| 搜索万豪酒店 | `flyai search-marriott-hotel --dest-name "目的地"` |
| 搜索万豪套餐 | `flyai search-marriott-package --keyword "关键词"` |

---

> 文档版本: 2026-04-01 | CLI版本: @fly-ai/flyai-cli