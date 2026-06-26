---
name: "Travel Search Flight Train Scenery - 旅行搜索 航班 火车 景点"
description: 聚合航班列表、景点信息，火车段可走 train 能力。当用户说：查一下上海到东京的航班、杭州有什么景点推荐、顺带帮我看看火车票，或类似出行规划问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🧳", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 旅行聚合（机票、火车、景点）（jisu-travel）

数据使用同程旅行：<https://www.ly.com/>  
本技能由**极速数据**提供：[`https://www.jisuapi.com`](https://www.jisuapi.com)  
信息反馈：请发邮件至 `liupandeng@jisuapi.com`

能力说明：

- 航班（`flight`）：返回航班搜索链接与航班列表
- 景点（`scenery`）：返回景点搜索链接与景点列表
- 火车（`train_*`）：**使用极速数据火车接口**

## 依赖

```bash
pip install requests beautifulsoup4
```


火车需要先在极速数据平台申请火车相关接口，申请链接：<https://www.jisuapi.com/api/train/>

申请后再配置：

```bash
# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

- `skills/jisu-travel/search.py`

## 使用方式

### 1) 航班入口与相关链接

```bash
python3 skills/jisu-travel/search.py flight
```

可选参数（JSON）：

```bash
python3 skills/jisu-travel/search.py flight '{
  "from_city":"上海",
  "to_city":"北京",
  "from_code":"SHA",
  "to_code":"PEK",
  "depart_date":"2026-03-30",
  "return_date":"2026-04-02",
  "trip_type":"round",
  "limit_flights":20,
  "sort_by":"price",
  "sort_order":"asc"
}'
```

### 2) 景点搜索与列表

```bash
python3 skills/jisu-travel/search.py scenery
```

可选参数（JSON）：

```bash
python3 skills/jisu-travel/search.py scenery '{
  "city":"上海",
  "keyword":"迪士尼",
  "scenery_sort":"推荐",
  "limit_sceneries":20
}'
```

### 3) 火车站站查询（极速数据）

```bash
python3 skills/jisu-travel/search.py train_station2s '{"start":"杭州","end":"北京","ishigh":1}'
```

### 4) 火车车次查询（极速数据）

```bash
python3 skills/jisu-travel/search.py train_line '{"trainno":"G34"}'
```

### 5) 火车余票查询（极速数据）

```bash
python3 skills/jisu-travel/search.py train_ticket '{"start":"杭州","end":"北京","date":"2026-03-26"}'
```

## 输出字段说明

### 航班/景点

- `provider`: 固定 `ly.com`
- `channel`: `flight/scenery`
- `entry_url`: 对应频道入口
- `search_url`: 根据请求参数拼出的频道搜索链接
- `request`: 原始请求参数回显
- `source`: 首页来源链接
- `flight_count`: 航班数量（仅 `flight` 且命中列表页时）
- `flights`: 航班明细列表（仅 `flight` 且命中列表页时）
- `flight_sort`: 航班排序信息（默认 `price + asc`）
- `scenery_count`: 景点数量（仅 `scenery`）
- `sceneries`: 景点列表（仅 `scenery`）
- `scenery_sort`: 景点排序信息（`推荐/人气/级别`）

常用参数：

- `limit_flights`: 航班明细条数上限（默认 20，最大 100）
- `limit_sceneries`: 景点条数上限（默认 20，最大 100）
- `scenery_sort`: 景点排序，支持 `推荐`（默认）/`人气`/`级别`；也支持英文 `recommend/popular/level`
- `sort_by`: 航班排序字段，支持 `price` 或 `time`（默认 `price`）
- `sort_order`: 排序方向，支持 `asc`（默认）或 `desc`
- 航班：`from_city`、`to_city`、`from_code`、`to_code`、`depart_date`、`return_date`、`trip_type`
- 景点：`city`、`keyword`

补充：

- 航班若同时提供 `from_code` + `to_code` + `depart_date`，`search_url` 会优先生成同程机票列表页格式：  
  `https://www.ly.com/flights/itinerary/oneway/SHA-PEK?...`
- 若未传 `from_code/to_code`，会根据 `airport.md` 按 `from_city/to_city` 自动补全常用机场代号（可手动传参覆盖）。
- 景点会使用同程搜索页：`https://so.ly.com/scenery?q=...`，并解析页面卡片提取名称/等级/地址/价格/详情链接。

### 火车

- `channel`: `train_station2s/train_line/train_ticket`
- `data`: 极速数据火车接口返回结果

## 说明

- 站点前端结构可能变化，页面字段或列表内容可能出现波动。
- 火车能力走极速数据接口，更稳定，建议作为车次与余票主查询通道。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

