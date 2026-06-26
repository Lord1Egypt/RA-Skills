---
name: "Stock Inquiry - 股票查询"
description: 按股票代码查当日行情与详情（分钟级趋势），或按分类拉取沪深、港股、北证等股票列表。当用户说：今天的宁德时代股票走势怎样？宁德时代股票行情怎样？贵州茅台现在多少钱？或类似个股行情、股票列表问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据股票查询（Jisu Stock）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **股票查询**（`/stock/query`）：根据股票代码查询当日行情，数据粒度为分钟，含趋势数据
- **股票列表查询**（`/stock/list`）：按分类（沪深股市/港股/北证A股）分页获取股票列表
- **股票详情查询**（`/stock/detail`）：根据股票代码获取单只股票详情（最新价、涨跌幅、成交量、市盈率等）

如需做更深入的走势分析、K 线研究或回测，推荐配合 **股票历史行情查询 Skill（stockhistory）** 一起使用：  
- ClawHub 链接：[`https://clawhub.ai/jisuapi/stockhistory`](https://clawhub.ai/jisuapi/stockhistory)

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [股票查询 API](https://www.jisuapi.com/api/stock/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/stock/stock.py`

## 使用方式

### 1. 股票查询（/stock/query）

根据股票代码查询当日行情，返回名称、代码、最新价、昨收盘价、数据量、更新时间及按分钟维度的趋势数组（时间、价格、成交量、成交总额、平均价）。

```bash
python3 skills/stock/stock.py query '{"code":"300917"}'
```

请求 JSON：

```json
{
  "code": "300917"
}
```

| 字段名 | 类型   | 必填 | 说明     |
|--------|--------|------|----------|
| code   | string | 是   | 股票代码 |

### 2. 股票列表查询（/stock/list）

按分类分页获取股票列表。分类：1 沪深股市，3 港股，4 北证A股。

```bash
python3 skills/stock/stock.py list '{"classid":1,"pagenum":1,"pagesize":10}'
```

请求 JSON：

```json
{
  "classid": 1,
  "pagenum": 1,
  "pagesize": 10
}
```

| 字段名   | 类型   | 必填 | 说明                          |
|----------|--------|------|-------------------------------|
| classid  | int    | 是   | 1 沪深股市 3 港股 4 北证A股   |
| pagenum  | int    | 否   | 当前页，默认 1                |
| pagesize | int    | 否   | 每页数量，默认 30            |

### 3. 股票详情查询（/stock/detail）

根据股票代码获取单只股票详情：最新价、最高/最低价、成交量、成交额、换手率、开盘价、昨收盘价、涨跌幅、涨跌额、振幅、量比、市盈率、市净率、更新时间等。

```bash
python3 skills/stock/stock.py detail '{"code":"300917"}'
```

请求 JSON：

```json
{
  "code": "300917"
}
```

| 字段名 | 类型   | 必填 | 说明     |
|--------|--------|------|----------|
| code   | string | 是   | 股票代码 |

## 返回结果示例（节选）

### 股票查询（query）

```json
[
  {
    "name": "特发服务",
    "code": "300917",
    "price": "51.08",
    "lastclosingprice": 51,
    "trendnum": "271",
    "updatetime": "2020-12-29 15:28:13",
    "trend": [
      "2020-12-29 09:30,51.08,1582,8082745.00,51.080",
      "2020-12-29 09:31,48.50,4282,21596207.00,50.612"
    ]
  }
]
```

### 股票列表（list）

```json
{
  "pagesize": 10,
  "pagenum": 1,
  "total": "4486",
  "classid": 1,
  "list": [
    { "name": "信达增利", "code": "166105" },
    { "name": "R003", "code": "201000" }
  ]
}
```

### 股票详情（detail）

```json
{
  "name": "C特发",
  "code": "300917",
  "classid": 1,
  "price": "40.70",
  "maxprice": "43.80",
  "minprice": "40.20",
  "tradenum": 76873,
  "tradeamount": "319857632.00",
  "turnoverrate": "36.030",
  "openningprice": "43.00",
  "lastclosingprice": "47.60",
  "changepercent": "-14.5",
  "changeamount": "-6.90",
  "amplitude": "7.56",
  "quantityratio": "1.03",
  "per": "41.91",
  "pbr": "5.36",
  "updatetime": "2020-12-22 11:56:20"
}
```

当接口返回业务错误时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "股票代码为空"
}
```

## 常见错误码

来源于 [极速数据股票文档](https://www.jisuapi.com/api/stock/)：

| 代号 | 说明         |
|------|--------------|
| 201  | 股票代码为空 |
| 202  | 股票代码不存在 |
| 210  | 没有信息     |

系统错误码：

| 代号 | 说明                     |
|------|--------------------------|
| 101  | APPKEY 为空或不存在       |
| 102  | APPKEY 已过期            |
| 103  | APPKEY 无请求此数据权限  |
| 104  | 请求超过次数限制         |
| 105  | IP 被禁止                |
| 106  | IP 请求超过限制          |
| 107  | 接口维护中               |
| 108  | 接口已停用               |

## 推荐用法

1. 用户提问：「300917 这只股票今天行情怎么样？」  
2. 代理可先调用：`python3 skills/stock/stock.py detail '{"code":"300917"}'` 获取最新价、涨跌幅、成交量等摘要；若需要当日分钟级走势，再调用 `python3 skills/stock/stock.py query '{"code":"300917"}'`。  
3. 用户问「沪深股市有哪些股票」或「给我看一页港股列表」时，可调用：`python3 skills/stock/stock.py list '{"classid":1,"pagenum":1,"pagesize":20}'` 或 `classid: 3` 获取列表，再结合用户问题选取并展示名称、代码等信息。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

