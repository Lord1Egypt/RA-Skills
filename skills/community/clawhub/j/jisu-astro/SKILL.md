---
name: "Star Sign / Horoscope Inquiry - 星座运势查询"
description: 查十二星座列表与每日/周/月/年运势。当用户说：天蝎座今天运势？双子座本周财运？或类似星座运势问题时，使用本技能。
metadata: { "openclaw": { "emoji": "✨", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据星座运势（Jisu Astro）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [星座运势 API](https://www.jisuapi.com/api/astro/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

- **星座列表**（`/astro/all`）：获取 12 星座的 ID、名称、日期范围和图标。
- **星座运势查询**（`/astro/fortune`）：按星座 ID 和日期查询今日、明日、本周、本月、本年星座运势。

可用于对话中回答「我是什么座」「今天白羊座运势怎样」「帮我看看这个月的感情/工作运」等问题。


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/astro/astro.py`

## 使用方式与请求参数

### 1. 获取星座列表（/astro/all）

```bash
python3 skills/astro/astro.py all
```

返回结果示例（节选自 [极速数据文档](https://www.jisuapi.com/api/astro/)）：

```json
[
  {
    "astroid": "1",
    "astroname": "白羊座",
    "date": "3-21~4-19",
    "pic": "http://api.jisuapi.com/astro/static/images/baiyang.png"
  },
  {
    "astroid": "2",
    "astroname": "金牛座",
    "date": "4-20~5-20",
    "pic": "http://api.jisuapi.com/astro/static/images/jinniu.png"
  }
]
```

字段说明：

- `astroid`：星座 ID（1–12）
- `astroname`：星座名称（如 白羊座、金牛座）
- `date`：星座日期范围
- `pic`：星座图标地址

### 2. 星座运势查询（/astro/fortune）

```bash
python3 skills/astro/astro.py fortune '{"astroid":1,"date":"2016-01-19"}'
```

请求 JSON 示例：

```json
{
  "astroid": 1,
  "date": "2016-01-19"
}
```

| 字段名  | 类型 | 必填 | 说明                          |
|---------|------|------|-------------------------------|
| astroid | int  | 是   | 星座 ID（1–12）               |
| date    | string | 否 | 日期（`YYYY-MM-DD`），默认今天 |

返回结果示例（节选自 [极速数据文档](https://www.jisuapi.com/api/astro/)）：

```json
{
  "astroid": "1",
  "astroname": "白羊座",
  "year": {
    "date": "2016",
    "summary": "未来一年将是白羊座历经艰辛终于寻得新的突破的一年。",
    "money": "上半年收入还算稳定，但也不太会有意料之外的收入，需要花钱的地方倒是不少。",
    "career": "十月之前，都相对还是白羊座的蛰伏期。",
    "love": "与事业运类似，今年的桃花运也主要集中在下半年爆发。"
  },
  "week": {
    "date": "2016-01-17~01-23",
    "money": "偏财机会继续受重视。本职工作收入受压。",
    "career": "太阳本周转入朋友宫，对事业的执着感下调，会寻觅新的圈子。",
    "love": "一夜情几率高……",
    "health": "性能量高强，小心纵欲伤身。",
    "job": "方向有变，高新行业值得你更多关注。"
  },
  "today": {
    "date": "2016-01-19",
    "presummary": "你需要思考自身价值观是否符合当下环境。",
    "star": "处女座",
    "color": "黄色",
    "number": "5",
    "summary": "4",
    "money": "4",
    "career": "4",
    "love": "3",
    "health": "80%"
  },
  "tomorrow": {
    "date": "2016-01-20",
    "presummary": "今天你有些悲观哦。",
    "star": "巨蟹座",
    "color": "青绿色",
    "number": "4",
    "summary": "3",
    "money": "3",
    "career": "3",
    "love": "3",
    "health": "77%"
  },
  "month": {
    "date": "2016-1",
    "summary": "本月，事业对你而言是非常重要的。",
    "money": "火星入资源宫，热烈关注偏财。",
    "career": "木星上旬开启在工作宫的逆行……",
    "love": "心灵刹那的触动和性的爆发，高度吻合。"
  }
}
```

常见字段：

- 顶层：`astroid`, `astroname`
- `today` / `tomorrow`：`date`, `presummary`, `star`（贵人星座）, `color`, `number`, `summary`, `money`, `career`, `love`, `health`
- `week` / `month` / `year`：`date`, `summary`, `money`, `career`, `love`, 以及本周的 `job`、`health` 等。

脚本不会对内容做拆分或转换，而是原样返回 `result`，方便代理按需挑选段落进行摘要或重写。

## 常见错误码

来自 [极速数据星座运势文档](https://www.jisuapi.com/api/astro/) 的业务错误码：

| 代号 | 说明        |
|------|-------------|
| 201  | 日期不正确  |
| 202  | 星座 ID 不正确 |
| 203  | 没有信息    |

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

1. 用户提供生日或星座问题：「1995-04-10 是什么座？今天和本周运势如何？」  
2. 代理先调用：`astro all` 获取 12 星座的日期范围，基于生日确定用户星座对应的 `astroid`。  
3. 然后调用：`astro fortune '{"astroid":1,"date":"2025-03-02"}'` 获取白羊座的今日/本周/本月/本年运势。  
4. 从返回结构中选择合适粒度（例如今日 + 本周 + 本月），对 `summary`、`money`、`career`、`love`、`health` 等字段进行整理和摘要，用自然语言给出贴合用户问题的解读。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

