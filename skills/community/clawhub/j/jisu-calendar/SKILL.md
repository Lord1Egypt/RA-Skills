---
name: "Calendar - 万年历查询"
description: 查询指定日期的公历、农历、星座、生肖、黄历要点与节假日。当用户说：明天农历几号？今年春节是哪天？或类似万年历问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🗓️", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据万年历（Jisu Calendar）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [万年历 API](https://www.jisuapi.com/api/calendar/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

- **万年历查询**（`/calendar/query`）：指定日期查询公历、农历、星座、生肖、干支、黄历（宜忌、吉神凶神等）信息，可进行阴阳历转换。
- **节假日查询**（`/calendar/holiday`）：查询法定节假日的放假/调休说明。

适合在对话中回答「某天是周几、什么星座」「农历是多少」「这天宜做什么」「今年有什么法定节假日安排」等问题。


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/calendar/calendar.py`

## 使用方式与请求参数

### 1. 万年历查询（/calendar/query）

```bash
python3 skills/calendar/calendar.py '{"date":"2015-10-22"}'
```

也可以显式指定阴历标记，例如按农历查询：

```bash
python3 skills/calendar/calendar.py '{"date":"2015-09-10","islunar":1,"islunarmonth":0}'
```

请求 JSON 示例：

```json
{
  "date": "2015-10-22",
  "islunar": 0,
  "islunarmonth": 0
}
```

| 字段名        | 类型   | 必填 | 说明                         |
|---------------|--------|------|------------------------------|
| date          | string | 是   | 日期，格式 `YYYY-MM-DD`，默认今天 |
| islunar       | int    | 否   | 是否是阴历，0 表示阳历（默认），1 表示阴历 |
| islunarmonth  | int    | 否   | 是否是闰月，0 不是（默认），1 为闰月 |

返回结果示例（节选自 [极速数据文档](https://www.jisuapi.com/api/calendar/)）：

```json
{
  "year": "2015",
  "month": "10",
  "day": "22",
  "week": "四",
  "lunaryear": "2015",
  "lunarmonth": "九月",
  "lunarday": "初十 ",
  "ganzhi": "乙未",
  "shengxiao": "羊",
  "star": "天枰座",
  "huangli": {
    "nongli": "农历二〇一五年九月初十",
    "taishen": "厨灶厕外西南",
    "wuxing": "路旁土",
    "chong": "冲（乙丑）牛",
    "sha": "煞西",
    "jiri": "朱雀（黑道）收日",
    "zhiri": "朱雀（黑道凶日）",
    "xiongshen": "地曩 月刑 河魁 五虚 朱雀",
    "jishenyiqu": "天德合 母仓 不将 玉宇 月德合",
    "caishen": "正东",
    "xishen": "西南",
    "fushen": "西南",
    "suici": [
      "乙未年",
      "丙戌月",
      "辛未日"
    ],
    "yi": [
      "祭祀",
      "冠笄",
      "移徙",
      "会亲友",
      "纳财",
      "理发",
      "捕捉"
    ],
    "ji": [
      "嫁娶",
      "开市",
      "开池",
      "作厕",
      "破土"
    ]
  }
}
```

主要字段说明：

- **公历与星期**：`year`, `month`, `day`, `week`
- **农历与干支**：`lunaryear`, `lunarmonth`, `lunarday`, `ganzhi`, `shengxiao`, `nongli`
- **星座**：`star`
- **黄历信息**（在 `huangli` 对象中）：`yi`（宜）、`ji`（忌）、`suici`（岁次）、`taishen`、`wuxing`、`chong`、`sha`、`jiri`、`zhiri`、`xiongshen`、`jishenyiqu`、`caishen`、`xishen`、`fushen` 等。

### 2. 节假日查询（/calendar/holiday）

```bash
python3 skills/calendar/calendar.py holiday
```

无额外 JSON 参数。

返回结果示例（节选自 [极速数据文档](https://www.jisuapi.com/api/calendar/)）：

```json
{
  "2015-01-01": "1月1日至3日放假调休，共3天。1月4日（星期日）上班。",
  "2015-02-18": "2月18日至24日放假调休，共7天。2月15日（星期日）、2月28日（星期六）上班。",
  "2015-04-05": "4月5日放假，4月6日（星期一）补休。"
}
```

部分实现中也可能返回更结构化的对象（包含 `name`、`content`），脚本不会做额外处理，原样返回 `result`。

## 常见错误码

来自 [极速数据万年历文档](https://www.jisuapi.com/api/calendar/) 的业务错误码：

| 代号 | 说明     |
|------|----------|
| 201  | 日期有误 |
| 202  | 没有信息 |

系统错误码：

| 代号 | 说明                     |
|------|--------------------------|
| 101  | APPKEY 为空或不存在     |
| 102  | APPKEY 已过期           |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制         |
| 105  | IP 被禁止               |
| 106  | IP 请求超过限制         |
| 107  | 接口维护中               |
| 108  | 接口已停用               |

## 推荐用法

1. 用户提问：「帮我查一下 2025-05-20 是周几、农历多少、属什么、适合干什么？」  
2. 代理构造 JSON：`{"date":"2025-05-20"}` 并调用：  
   `python3 skills/calendar/calendar.py '{"date":"2025-05-20"}'`。  
3. 从结果中读取：`week`、`nongli`、`shengxiao`、`star`，以及 `huangli.yi` / `huangli.ji`、`huangli.jiri`、`huangli.xiongshen` 等字段，整理成自然语言回答。  
4. 如用户只关心法定节假日安排，则调用：`python3 skills/calendar/calendar.py holiday`，根据返回的日期键值对，提取今年或指定年份的放假/调休说明，并用人话归纳给用户。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

