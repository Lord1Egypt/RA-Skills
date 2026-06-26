---
name: "Summary of JisuAPI - 极速数据API汇总"
description: 统一入口：一个 Key 调用多类极速数据接口（天气、黄金、股票、快递等），通过 call 路由。当用户说：用同一个接口查天气又查黄金、不想配很多个 skill，或类似一站式数据网关时，使用本技能。
metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据统一入口（Jisu Unified）

**极速数据**（官网：[https://www.jisuapi.com/](https://www.jisuapi.com/)）是基础数据 API 接口提供商，提供天气、股票、黄金、菜谱、汇率、快递、车辆等百余类接口。本 Skill 为**统一入口**：只需配置一个 `JISU_API_KEY`，即可通过 `call` 命令按「接口路径 + 参数」调用任意已开通的极速数据 API，无需为每个品类单独安装技能。

适合在 OpenClaw/ClawHub 中作为「结构化数据网关」使用：用户问天气、金价、股票、菜谱等，Agent 先 `list` 查接口，再 `call` 调对应 API，一次配置覆盖多类数据。

使用前请在极速数据官网申请 API Key 并开通需要的数据接口；各接口计费与额度以官网为准。


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/jisu/jisu.py`

## 使用方式

### 1. 列出支持的接口（list）

```bash
python3 skills/jisu/jisu.py list
```

返回当前支持的 `api` 列表及简短说明，便于按需选择接口。

### 2. 统一调用（call）

请求 JSON：`{"api": "接口路径", "params": { ... }}`。`params` 可选，无参接口可省略。

**无参示例：**

```bash
python3 skills/jisu/jisu.py call '{"api":"gold/shgold"}'
python3 skills/jisu/jisu.py call '{"api":"stockindex/sh"}'
```

**带参示例：**

```bash
python3 skills/jisu/jisu.py call '{"api":"stock/query","params":{"code":"300917"}}'
python3 skills/jisu/jisu.py call '{"api":"weather/query","params":{"city":"北京"}}'
python3 skills/jisu/jisu.py call '{"api":"recipe/search","params":{"keyword":"白菜","num":10,"start":0}}'
python3 skills/jisu/jisu.py call '{"api":"exchange/convert","params":{"from":"CNY","to":"USD","amount":100}}'
```

返回格式与极速数据官网一致：成功时为 `result` 内容；失败时脚本返回 `error`、`code`、`message` 等。

## 支持的接口一览（节选）

| 分类     | api                    | 说明 |
|----------|------------------------|------|
| 黄金     | gold/shgold, gold/shfutures, gold/hkgold, gold/bank, gold/london, gold/storegold | 上海黄金/上海期货/香港/银行/伦敦/金店金价 |
| 股票     | stock/query            | 当日行情，params: code |
| 股票     | stock/list             | 列表，params: classid, pagenum, pagesize |
| 股票     | stock/detail           | 详情，params: code |
| 股票历史 | stockhistory/query    | 历史行情，params: code, startdate, enddate |
| 指数     | stockindex/sh          | 上证/深证/创业板等指数 |
| 天气     | weather/query          | 天气预报，params: city 或 cityid 等 |
| 天气     | weather/city           | 支持城市列表 |
| 菜谱     | recipe/search, recipe/class, recipe/byclass, recipe/detail | 搜索/分类/按分类检索/详情 |
| MBTI     | character/questions   | 题目，params 可选 version |
| MBTI     | character/answer       | 提交答案，params: answer, version |
| 汇率     | exchange/convert, exchange/single, exchange/currency, exchange/bank | 换算/单货币/货币列表/银行汇率 |
| 历史上的今天 | todayhistory/query | 指定月日的历史事件，params: month, day |
| 历史天气 | weather2/query      | 按城市与日期查历史天气，params: date 必填，city 或 cityid 可选 |
| 历史天气 | weather2/city       | 历史天气支持城市列表 |
| 企业联系方式 | enterprisecontact/query | 企业电话/邮箱等，params: company/creditno/regno/orgno 任填其一 |
| 二维码   | qrcode/generate, qrcode/read, qrcode/template | 二维码生成/识别/模板样例 |
| 条码     | barcode/generate, barcode/read | 条形码生成/识别，params: type, barcode, fontsize, dpi, scale, height / barcode |
| 商品条码查询 | barcode2/query           | 商品条码信息查询，params: barcode |
| ip       | ip/location             | IP 归属地，params: ip |
| 手机归属地   | shouji/query             | 手机归属地，params: shouji |
| 身份证查询   | idcard/query             | 身份证查询，params: idcard |
| 银行卡归属地 | bankcard/query           | 银行卡归属地，params: bankcard |
| 快递     | express/query, express/type | 快递查询、快递公司类型 |
| 车型大全     | car/brand, car/type, car/car, car/detail, car/search, car/hot, car/rank | 品牌/车型/车款/详情/搜索/热门/销量排行 |
| 限行     | vehiclelimit/city, vehiclelimit/query | 限行城市、限行查询 |
| 车辆     | vin/query                | VIN 车辆信息，params: vin |
| VIN识别 OCR | vinrecognition/recognize | VIN 车架号图像识别，params: pic(base64 或本地读后编码) |
| 通用文字识别 OCR | generalrecognition/recognize | 通用文字识别，将图片中的文字识别为文本，params: pic(base64)、type(cnen/en/fr/pt/de/it/es/ru/jp) |
| 身份证等证件 OCR | idcardrecognition/type, idcardrecognition/recognize | 证件类型列表，以及身份证/驾照/护照等证件 OCR 识别，params: typeid, pic(base64) |
| 银行卡 OCR | bankcardcognition/recognize | 银行卡号、卡类型、银行名称识别，params: pic(base64) |
| 油价     | oil/query, oil/province  | 省市油价、支持省市列表 |
| 白银     | silver/shgold, silver/shfutures, silver/london | 上海黄金/上海期货/伦敦银价 |
| 万年历     | calendar/query, calendar/holiday, huangli/date | 万年历、节假日、黄历 |
| 新闻     | news/get, news/channel   | 新闻、新闻频道 |
| 经纬度地址转换     | geoconvert/coord2addr, geoconvert/addr2coord | 坐标转地址、地址转坐标 |
| 周公解梦 | dream/search            | 搜索，params: keyword, pagenum, pagesize |
| 热搜榜单     | hotsearch/weibo, hotsearch/baidu, hotsearch/douyin | 微博/百度/抖音热搜榜 |
| 期货     | futures/shfutures, futures/dlfutures, futures/zzfutures, futures/zgjrfutures, futures/gzfutures | 上海/大连/郑州/中金所/广州期货价格 |

完整列表以 `jisu.py list` 输出为准；参数含义见 [极速数据 API 文档](https://www.jisuapi.com/)。

## 错误返回

- 未配置 Key：脚本直接报错退出。
- `api` 缺失：`{"error": "missing_param", "message": "api is required"}`。
- 接口返回业务错误：`{"error": "api_error", "code": xxx, "message": "..."}`。
- 网络/解析错误：`request_failed` / `http_error` / `invalid_json`。

## 推荐用法

1. 用户提问：「北京天气怎么样」「300917 股票今天多少钱」「人民币兑美元汇率」等。
2. 代理先调用 `python3 skills/jisu/jisu.py list` 确认接口名，再按需调用 `call`，例如：  
   `python3 skills/jisu/jisu.py call '{"api":"weather/query","params":{"city":"北京"}}'`  
   `python3 skills/jisu/jisu.py call '{"api":"stock/detail","params":{"code":"300917"}}'`  
   `python3 skills/jisu/jisu.py call '{"api":"exchange/convert","params":{"from":"CNY","to":"USD","amount":1}}'`  
3. 从返回的 `result` 中抽取关键字段，用自然语言回复用户；若需更多接口参数说明，可引导用户查看极速数据官网文档。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

