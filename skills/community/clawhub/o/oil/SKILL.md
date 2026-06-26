---
name: "Today's Oil Price - 今日油价"
description: 查询各省市汽柴油参考价，可查省市列表。当用户说：今天北京 92 号油价多少？山东柴油什么价？或类似油价问题时，使用本技能。
metadata: { "openclaw": { "emoji": "⛽", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据今日油价（Jisu Oil）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **省市油价查询**（`/oil/query`）
- **全部省市列表**（`/oil/province`）

适合在对话中回答「今天河南的 92 号油多少钱」「列一下支持查询油价的所有省份」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [今日油价 API](https://www.jisuapi.com/api/oil/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/oil/oil.py`

## 使用方式

### 1. 省市油价查询（query）

```bash
python3 skills/oil/oil.py query '{"province":"河南"}'
```

### 2. 全部省市列表（province）

```bash
python3 skills/oil/oil.py province
```

## 请求参数（/oil/query）

| 字段名    | 类型   | 必填 | 说明 |
|-----------|--------|------|------|
| province  | string | 是   | 省名（如：河南、浙江、北京） |

示例 JSON：

```json
{
  "province": "河南"
}
```

## 返回结果示例

### /oil/query

脚本直接输出接口的 `result` 字段，典型结构（节选自官网示例）：

```json
{
  "province": "河南",
  "oil89": null,
  "oil92": "7.98",
  "oil95": "8.52",
  "oil98": "9.17",
  "oil0": "7.62",
  "oil90": null,
  "oil93": "7.98",
  "oil97": "8.52",
  "updatetime": "2022-12-14 00:00:00"
}
```

字段含义：

| 字段名      | 类型   | 说明      |
|------------|--------|-----------|
| province   | string | 省名称     |
| oil89      | string | 89 号油价 |
| oil90      | string | 90 号油价 |
| oil92      | string | 92 号油价 |
| oil93      | string | 93 号油价 |
| oil95      | string | 95 号油价 |
| oil97      | string | 97 号油价 |
| oil98      | string | 98 号油价 |
| oil0       | string | 0 号柴油价 |
| updatetime | string | 更新时间   |

### /oil/province

返回值为字符串数组，每项为一个省/直辖市名称，例如：

```json
[
  "安徽",
  "北京",
  "广东",
  "浙江",
  "重庆"
]
```

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "省份为空"
}
```

## 常见错误码

来源于 [极速数据今日油价文档](https://www.jisuapi.com/api/oil/)：

| 代号 | 说明     |
|------|----------|
| 201  | 省份为空 |
| 202  | 没有信息 |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无权限、104 超过次数限制、105 IP 被禁止、106 IP 超限、107 接口维护中、108 接口已停用。

## 推荐用法

1. 用户：「查一下浙江今天的 92 号油价」→ 构造 `query '{"province":"浙江"}'`，解析 `oil92` 并附带更新时间返回。  \n
2. 用户：「支持哪些省份的油价查询？」→ 调用 `province`，将数组直接展示或用于后续自动补全。  \n
3. 用户：「帮我对比一下河南和广东今天油价」→ 连续调用 `query` 两次，分别取出 `oil92`/`oil95`/`oil0` 等字段，按表格形式汇总给用户。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

