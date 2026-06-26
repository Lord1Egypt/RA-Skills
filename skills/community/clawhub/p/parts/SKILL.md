---
name: "Auto Parts OE Inquiry - 汽车配件OE信息查询"
description: 查配件品牌、OE 号模糊搜、适用车型与替换件等。当用户说：这个原厂零件号对应什么件？有没有替换件？或类似汽车 OE 配件问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🔧", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据汽车配件OE信息查询（Jisu Parts）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **配件品牌**（`/parts/brand`）：获取配件品牌列表
- **原厂零件号模糊搜索**（`/parts/search`）：按零件号搜索 OE 信息及多品牌匹配
- **零件号查销售车型**（`/parts/salecar`）：查某零件号/品牌/零件 ID 对应的销售车型
- **查询替换件**（`/parts/replace`）：查某原厂件的替换件、品牌件

可用于对话中回答「这个零件号有哪些品牌在用」「L8WD807065K 适配哪些车」「04E115561C 的替换件有哪些」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [汽车配件OE信息查询 API](https://www.jisuapi.com/api/parts/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/parts/parts.py`

## 使用方式

### 1. 配件品牌（brand）

```bash
python3 skills/parts/parts.py brand
```

### 2. 原厂零件号模糊搜索（search）

```bash
python3 skills/parts/parts.py search '{"number":"L8WD807065KGRU"}'
```

### 3. 零件号查销售车型（salecar）

```bash
# 零件号 + 品牌ID
python3 skills/parts/parts.py salecar '{"number":"L8WD807065KGRU","brandid":219}'

# 仅品牌ID 或 仅零件ID 也可
python3 skills/parts/parts.py salecar '{"partsid":23064200}'
```

### 4. 查询替换件（replace）

```bash
# 零件号 + 品牌ID
python3 skills/parts/parts.py replace '{"number":"01402917258","brandid":10}'

# 或零件ID
python3 skills/parts/parts.py replace '{"partsid":12656367}'
```

## 请求参数摘要

| 子命令   | 必填/组合说明                    | 参数说明                          |
|----------|----------------------------------|-----------------------------------|
| brand    | 无参数                           | —                                 |
| search   | number（必填）                   | 零件号                            |
| salecar  | number / brandid / partsid 任选一或组合 | number、brandid、partsid 至少传一个 |
| replace  | partsid 或 number+brandid        | number、brandid、partsid 任选一组 |

## 返回结果说明

脚本直接输出接口的 `result` 字段（JSON）：

- **brand**：数组，每项含 `brandid`、`name`。
- **search**：对象，含 `list` 数组，每项含 `partsid`、`number`、`number2`、`brand`、`name`、`stdname`、`marketprice`、`remark` 等。
- **salecar**：对象，含 `brandid`、`number`、`number2`、`partsid`、`brand` 及 `list`（销售车型列表，含 `carid`、`fullname`、`price`、`yeartype`、`listdate`、`productionstate`、`salestate`、`sizetype`、`displacement`、`geartype` 等）。
- **replace**：对象，含 `partsid`、`name`、`brand`、`brandid`、`number` 及 `list`（替换件列表，含 `partsid`、`number`、`name`、`stdname`、`brandid`、`brand` 等）。

错误时输出形如：

```json
{
  "error": "api_error",
  "code": 202,
  "message": "配件ID错误"
}
```

## 常见错误码

来自 [极速数据汽车配件OE文档](https://www.jisuapi.com/api/parts/)：

| 代号 | 说明                 |
|------|----------------------|
| 201  | 零件ID和零件号不能都为空 |
| 202  | 配件ID错误           |
| 220  | 没有信息             |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无权限、104 超过次数限制、105 IP 被禁止、106 IP 超限、107 接口维护中、108 接口已停用。

## 推荐用法

1. 用户：「有哪些配件品牌？」→ `parts.py brand`。  
2. 用户：「零件号 L8WD807065KGRU 有哪些品牌？」→ `parts.py search '{"number":"L8WD807065KGRU"}'`。  
3. 用户：「这个零件能用在哪些车上？」→ 先 search 或确定 brandid/partsid，再 `parts.py salecar '{"number":"...","brandid":219}'`。  
4. 用户：「04E115561C 的替换件」→ `parts.py replace '{"number":"04E115561C","brandid":10}'` 或按零件 ID 查询，解析返回的 `list` 为用户总结。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

