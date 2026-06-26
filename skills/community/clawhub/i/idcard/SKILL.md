---
name: "ID Card Number Origin Query - 身份证号码归属地查询"
description: 根据身份证号解析地区、出生日期、性别与校验位；可按城市查前六位规则。当用户说：这个身份证号是哪里发的？110101 开头是哪？或类似身份证归属问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🪪", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据身份证号码归属地查询（Jisu Idcard）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

支持：

- **身份证查询**（`/idcard/query`）
- **城市查身份证前 6 位**（`/idcard/city2code`）

可用于对话中回答「这个身份证是哪里的」「校验位对不对」「鹿邑县对应的身份证前 6 位是多少」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [身份证号码归属地查询 API](https://www.jisuapi.com/api/idcard/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/idcard/idcard.py`

## 使用方式

### 1. 身份证查询（query）

```bash
python3 skills/idcard/idcard.py query '{"idcard":"41272519800102067x"}'
```

### 2. 城市查身份证前 6 位（city2code）

```bash
python3 skills/idcard/idcard.py city2code '{"city":"鹿邑"}'
```

## 请求参数

### /idcard/query

| 字段名  | 类型   | 必填 | 说明             |
|---------|--------|------|------------------|
| idcard  | string | 是   | 身份证号或前 6 位 |

### /idcard/city2code

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| city   | string | 是   | 城市 |

## 返回结果示例

### /idcard/query

```json
{
  "province": "河南省",
  "city": "周口市",
  "town": "鹿邑县",
  "lastflag": "0",
  "sex": "男",
  "birth": "1980年01月02日",
  "area": "河南省周口市鹿邑县"
}
```

字段说明：

| 字段名   | 类型   | 说明                                             |
|----------|--------|--------------------------------------------------|
| province | string | 省                                               |
| city     | string | 市                                               |
| town     | string | 县                                               |
| lastflag | string | 最后一位校验码：`0` 正确，`1` 错误                |
| sex      | string | 性别                                             |
| birth    | string | 出生年月                                         |
| area     | string | 区域信息（由于行政区划调整，具体以该字段为准）   |

### /idcard/city2code

```json
{
  "province": "河南省",
  "city": "周口市",
  "town": "鹿邑县",
  "code": "412725"
}
```

字段说明：

| 字段名   | 类型   | 说明       |
|----------|--------|------------|
| code     | string | 身份证前 6 位 |
| province | string | 省         |
| city     | string | 市         |
| town     | string | 县         |

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "身份证为空"
}
```

## 常见错误码

来源于 [极速数据身份证号码归属地文档](https://www.jisuapi.com/api/idcard/)：

| 代号 | 说明       |
|------|------------|
| 201  | 身份证为空 |
| 202  | 身份证不正确 |
| 203  | 没有信息   |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无请求此数据权限、104 请求超过次数限制、105 IP 被禁止、106 IP 请求超过限制、107 接口维护中、108 接口已停用。

## 推荐用法

1. 用户：「帮我查一下 41272519800102067x 是哪里的」→ 调用 `query`，读取 `province`、`city`、`town` 和 `lastflag`，说明地区和校验是否通过。  \n
2. 用户：「鹿邑县的身份证前 6 位是多少？」→ 使用 `city2code '{"city":"鹿邑"}'`，返回 `code`。  \n
3. 用户：「校验一下这个身份证号是否正确」→ 使用 `query`，根据 `lastflag` 和是否返回 `result` 告知是否为合法号码。  \n
4. 用户：「只知道前 6 位，想确认大概地区」→ 仍使用 `query`，传入前 6 位，结合返回的 `province/city/town/area` 做说明。  \n

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

