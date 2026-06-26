---
name: "Almanac / Huangli Inquiry - 黄历查询"
description: 按公历日期查询农历、宜忌、吉神凶煞等黄历信息。当用户说：明天宜不宜搬家？这周五适合领证吗？或类似黄历择日时，使用本技能。
metadata: { "openclaw": { "emoji": "📅", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据黄历查询（Jisu Huangli）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

按指定的年、月、日查询农历、星座、生肖、胎神、五行、冲煞、宜忌、吉神凶神、财神方位、星期等黄历信息。
数据范围覆盖 1900–2100 年，可用于回答「今天适合干什么」「这天宜嫁娶吗」「农历和生肖是什么」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [黄历查询 API](https://www.jisuapi.com/api/huangli) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/huangli/huangli.py`

## 使用方式

黄历接口只有一个：`/huangli/date`，脚本直接接收 JSON 请求体。

### 查询指定日期的黄历（/huangli/date）

```bash
python3 skills/huangli/huangli.py '{"year":2015,"month":10,"day":27}'
```

请求 JSON 示例：

```json
{
  "year": 2015,
  "month": 10,
  "day": 27
}
```

### 请求参数

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| year   | string | 是   | 年   |
| month  | string | 是   | 月   |
| day    | string | 是   | 日   |

脚本会对 `year`、`month`、`day` 做必填校验，缺失时直接报错退出。

## 返回结果示例

脚本直接输出接口的 `result` 字段，结构与官网示例一致，例如（节选自
[极速数据文档](https://www.jisuapi.com/api/huangli)）：

```json
{
  "year": "2015",
  "month": "10",
  "day": "27",
  "yangli": "公元2015年10月27日",
  "nongli": "农历二〇一五年九月十五",
  "star": "天蝎座",
  "taishen": "厨灶碓外西南",
  "wuxing": "涧下水",
  "chong": "冲（庚午）马",
  "sha": "煞南",
  "shengxiao": "羊",
  "jiri": "天牢（黑道）满日",
  "zhiri": "天牢（黑道凶日）",
  "xiongshen": "灾煞 天火 大煞 归忌 天牢 触水龙",
  "jishenyiqu": "天德 月德 时德 福德 民日 天巫 普护 鸣犬对",
  "caishen": "西南",
  "xishen": "西南",
  "fushen": "正东",
  "suici": [
    "乙未年",
    "丙戌月",
    "丙子日"
  ],
  "yi": [
    "纳采",
    "成服"
  ],
  "ji": [
    "入宅",
    "上梁",
    "谢土"
  ],
  "eweek": "TUESDAY",
  "emonth": "October",
  "week": "二"
}
```

其中：

- `yangli` / `nongli`：阳历 / 农历完整描述  
- `star` / `shengxiao`：星座和生肖  
- `yi` / `ji`：宜做的事和忌讳的事，通常是字符串数组  
- `suici`：岁次（干支），数组形式  
- 其余字段对应文档中的黄历、方位、吉凶信息。

## 常见错误码

来自 [极速数据黄历文档](https://www.jisuapi.com/api/huangli) 的业务错误码：

| 代号 | 说明       |
|------|------------|
| 201  | 日期不正确 |
| 203  | 没有信息   |

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

1. 用户提问：「帮我看看 2025 年 5 月 20 日黄历如何，适合结婚吗？」  
2. 代理构造 JSON：`{"year":2025,"month":5,"day":20}` 并调用：  
   `python3 skills/huangli/huangli.py '{"year":2025,"month":5,"day":20}'`。  
3. 从返回结果中读取 `yi` / `ji`、`jiri`、`zhiri`、`xiongshen`、`jishenyiqu` 等字段，判断是否宜嫁娶、是否有明显凶神，结合用户问题做自然语言总结。  
4. 如用户只关心农历、生肖或星座，可直接读取 `nongli`、`shengxiao`、`star` 等字段给出简要回答。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

