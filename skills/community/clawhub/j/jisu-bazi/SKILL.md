---
name: "Bazi Chart - 八字排盘"
description: 按出生时间与城市排八字，返回四柱、纳音、大运流年等。当用户说：1990 年 6 月生于北京八字排盘、看看大运流年，或类似八字排盘时，使用本技能。
metadata: { "openclaw": { "emoji": "🔮", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据八字排盘（Jisu Bazi）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

适合在对话中回答「帮我排个八字」「看一下 2009 年 10 月 18 日 凌晨 2:05 的八字」「哪一年大运、流年更有利于事业或感情」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [八字排盘 API](https://www.jisuapi.com/api/bazi/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

> **重要说明**：此接口仅用于娱乐和学习参考，不构成任何现实决策依据。


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/bazi/bazi.py`

## 使用方式

### 八字排盘

```bash
python3 skills/bazi/bazi.py '{\
"name":"张三",\
"city":"杭州",\
"year":2009,\
"month":10,\
"day":18,\
"hour":2,\
"minute":5,\
"sex":1,\
"islunar":0,\
"istaiyang":0,\
"islunarmonth":2\
}'
```

常用参数说明：

- `name`：姓名（用于展示，可留空，但建议填写便于区分）  
- `city`：城市，用于更精确地定位节气与太阳时（可为空字符串）  
- `year` / `month` / `day` / `hour` / `minute`：公历时间，`year` 支持 1901–2099 年  
- `sex`：性别，`1` 男，`0` 女  
- `islunar`：是否为农历时间，`0` 为阳历（默认），`1` 为阴历  
- `istaiyang`：是否使用太阳时，`0` 默认不使用，`1` 使用太阳时  
- `islunarmonth`：是否为农历闰月，仅在 `islunar=1` 时有效，`1` 闰月，`2` 否  

## 请求参数（JSON）

| 字段名       | 类型     | 必填 | 说明                                      |
|--------------|----------|------|-------------------------------------------|
| name         | string   | 是   | 姓名                                      |
| city         | string   | 是   | 城市（可传空字符串）                      |
| year         | int      | 是   | 年（1901–2099）                           |
| month        | int      | 是   | 月                                       |
| day          | int      | 是   | 日                                       |
| hour         | int      | 是   | 时（0–23）                                |
| minute       | int      | 是   | 分（0–59）                                |
| sex          | int      | 是   | 性别：1 男，0 女                          |
| islunar      | int      | 是   | 是否为农历：0 阳历（默认），1 阴历         |
| istaiyang    | int      | 是   | 是否使用太阳时：0 不使用（默认），1 使用   |
| islunarmonth | int      | 是   | 是否闰月：1 是，2 否（仅在农历时有效）      |

脚本会将上述字段原样传给 `https://api.jisuapi.com/bazi/paipan`，并直接输出 `result` 字段内容。

## 返回结果概览

返回结果字段较多，这里只列出主要结构（具体字段以 [极速数据文档](https://www.jisuapi.com/api/bazi/) 为准）：

顶层主要字段：

| 字段名       | 说明                              |
|--------------|-----------------------------------|
| year/month/day/hour/minute | 出生公历时间              |
| name/city    | 姓名和城市                        |
| istaiyang    | 是否太阳时                        |
| lunaryear/lunarmonth/lunarday/lunarhour | 农历时间 |
| animal       | 生肖                              |
| yearganzhi   | 年干支                            |
| jieqiprev    | 出生的上一个节气（名称 + 日期）   |
| jieqinext    | 出生的下一个节气（名称 + 日期）   |
| bazi         | 生辰八字（年、月、日、时四柱）    |
| taiyuan      | 胎元                              |
| minggong     | 命宫                              |
| xunkong      | 旬空                              |
| qiyun        | 起运时间（年、月、日、时）        |
| jiaoyun      | 交运时间（年、月、日、时）        |
| qiankunzao   | 乾造/坤造（天干、地支、藏干等）   |
| nayin        | 四柱纳音                          |
| shensha      | 神煞（数组，竖排）                |
| dayun        | 大运（纳音、食神、干支、岁数、年份） |
| liunian      | 流年列表                          |

典型返回（节选）：

```json
{
  "year": "2009",
  "month": "10",
  "day": "18",
  "hour": "02",
  "minute": "05",
  "name": "",
  "city": "",
  "istaiyang": "0",
  "lunaryear": "2009",
  "lunarmonth": "九月",
  "lunarday": "初一",
  "lunarhour": "丑时",
  "animal": "牛",
  "yearganzhi": "己丑",
  "bazi": ["己丑", "甲戌", "丙申", "己丑"],
  "taiyuan": "乙丑",
  "minggong": "庚午",
  "xunkong": ["午未", "申酉", "辰巳", "午未"],
  "qiyun": { "year": "3", "month": "2", "day": "12", "hour": "2" },
  "jiaoyun": { "year": "2012", "month": "12", "day": "30", "hour": "04" },
  "dayun": {
    "nayin": ["山头火", "剑锋金"],
    "shishen": ["偏印", "正官"],
    "ganzhi": ["甲戌", "癸酉", "壬申"],
    "sui": ["1-2岁", "3岁", "13岁"],
    "year": ["2009", "2012", "2022"]
  },
  "liunian": [
    ["己丑", "壬辰", "壬寅"]
  ]
}
```

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "日期不正确"
}
```

## 常见错误码

来源于 [极速数据八字排盘文档](https://www.jisuapi.com/api/bazi/)：

| 代号 | 说明       |
|------|------------|
| 201  | 日期不正确 |
| 202  | 时间不正确 |
| 210  | 没有信息   |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无请求此数据权限、104 请求超过次数限制、105 IP 被禁止、106 IP 请求超过限制、107 接口维护中、108 接口已停用。

## 推荐用法

1. 用户：「帮我排一下 2009-10-18 凌晨 2:05（男）的八字」→ 将自然语言解析为年月日时分和性别，调用 `bazi.py`，再根据返回的 `bazi`、`qiankunzao`、`dayun`、`liunian` 做摘要说明。  \n
2. 用户：「看未来几年运势大概如何」→ 结合 `dayun` 与近期的 `liunian` 信息，以「偏印/正官/比肩」等十神和干支变化为线索，输出自然语言总结。  \n
3. 用户：「只知道农历时间」→ 将 `islunar` 设为 1，并按阴历年月日时传入（必要时结合万年历接口先转换），再使用本技能排盘。  \n
4. 用户：「是否要考虑太阳时」→ 当用户提供城市且对精准性有额外要求时，可将 `istaiyang` 设为 1，告诉用户这是基于太阳时修正后的排盘结果。  \n

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

