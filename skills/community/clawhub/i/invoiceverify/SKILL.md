---
name: "Invoice Verification - 发票查验"
description: 按发票代码、号码、日期、金额等查验发票真伪与详情。当用户说：帮我验一下这张增值税发票、这张票能不能报销查验？或类似发票查验时，使用本技能。
metadata: { "openclaw": { "emoji": "🧾", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据发票查验（Jisu InvoiceVerify）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。
可以通过发票代码、发票号码、开票日期、合计金额、校验码等信息获取发票详情，
也支持获取平台支持的发票类型列表。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [发票查验 API](https://www.jisuapi.com/api/invoiceverify/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/invoiceverify/invoiceverify.py`

## 使用方式

### 1. 查验发票信息

通过 `/invoiceverify/verify` 接口，根据发票号、开票日期及金额等信息查验发票。

```bash
python3 skills/invoiceverify/invoiceverify.py verify '{"number":"61124608","date":"2019-06-15","code":"033001800311","extaxtotalfee":"2388.46","checkcode":"62057237940487749830"}'
```

请求 JSON 示例：

```json
{
  "code": "033001800311",
  "number": "61124608",
  "date": "2019-06-15",
  "extaxtotalfee": "2388.46",
  "checkcode": "62057237940487749830",
  "sellercreditno": ""
}
```

### 请求参数（verify）

| 字段名         | 类型   | 必填 | 说明                                   |
|----------------|--------|------|----------------------------------------|
| code           | int    | 否   | 发票代码                               |
| number         | int    | 是   | 发票号码                               |
| date           | string | 是   | 开票日期（格式：YYYY-MM-DD）          |
| extaxtotalfee  | string | 否   | 合计金额（不含税，与 totalfee 二选一）|
| totalfee       | string | 否   | 价税合计（与 extaxtotalfee 二选一）   |
| checkcode      | string | 否   | 校验码（部分场景必填）                 |
| sellercreditno | int    | 否   | 销方税号（区块链发票必填）            |

### 返回结果示例（verify）

脚本会直接输出接口 `result` 字段内容，结构与官网示例一致，典型示例可参考
[官网文档](https://www.jisuapi.com/api/invoiceverify/) 中的 JSON：

```json
{
  "number": "61120000",
  "code": "033001800000",
  "seller": "杭州XXXXX有限公司",
  "sellercreditno": "913301833000000000",
  "sellerbank": "交通银行浙江分行富阳支行 300000060010100002000",
  "selleraddress": "杭州富阳区xxxxx路xx号x幢x层 0571-60000000",
  "buyer": "个人",
  "buyercreditno": "",
  "buyerbank": "",
  "buyeraddress": "",
  "totalfee": "2698.95",
  "extaxtotalfee": "2388.46",
  "date": "2019-06-15",
  "totaltax": "310.49",
  "type": "10",
  "remark": "订单号:97670000000 IMEI:868237000000000",
  "district": "浙江",
  "machinecode": "661620000000",
  "checkcode": "62050000040000000000",
  "state": 1,
  "itemlist": [
    {
      "name": "*移动通信设备*荣耀20 麒麟Kirin980全网通版",
      "type": "",
      "unit": "",
      "num": "0.0",
      "price": "0.0",
      "totalfee": "0.00",
      "taxrate": "0.13",
      "taxfee": "00000000.00"
    },
    {
      "name": "*移动通信设备*荣耀20 麒麟Kirin980全网通版",
      "type": "荣耀20",
      "unit": "台",
      "num": "1.0",
      "price": "2388.49557522",
      "totalfee": "2388.50",
      "taxrate": "0.13",
      "taxfee": "00000310.50"
    }
  ]
}
```

### 2. 获取发票类型列表

通过 `/invoiceverify/type` 接口获取平台支持的发票类型列表。

```bash
python3 skills/invoiceverify/invoiceverify.py type
```

返回结果示例：

```json
[
  {
    "type": "01",
    "name": "增值税专用发票"
  },
  {
    "type": "02",
    "name": "货运运输业增值税专用发票"
  },
  {
    "type": "03",
    "name": "机动车销售统一发票"
  },
  {
    "type": "04",
    "name": "增值税普通发票"
  },
  {
    "type": "10",
    "name": "增值税普通发票（电子）"
  }
]
```

### 常见错误码（业务错误）

来自 [极速数据发票查验文档](https://www.jisuapi.com/api/invoiceverify/) 的业务错误码：

| 代号 | 说明                                |
|------|-------------------------------------|
| 201  | 发票信息不一致（扣次数）           |
| 202  | 发票查验失败                        |
| 203  | 所查发票不存在（扣次数）           |
| 204  | 发票代码为空                        |
| 205  | 发票号码为空                        |
| 206  | 开票日期为空                        |
| 207  | 合计金额为空                        |
| 208  | 校验码为空                          |
| 209  | 校验码小于 6 位                     |
| 210  | 未知错误                            |
| 211  | 该票在平台核验失败已超 5 次（扣次数）|
| 212  | 校验码小于 5 位（区块链发票 5 位必填）|
| 213  | 销方税号为空（区块链发票必填）     |

### 系统错误码

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

1. 用户提供发票信息（发票代码、号码、开票日期、金额、校验码等）。  
2. 代理根据需要构造 JSON 请求体，例如：  
   `{"code":"033001800311","number":"61124608","date":"2019-06-15","extaxtotalfee":"2388.46","checkcode":"62057237940487749830"}`。  
3. 调用：`python3 skills/invoiceverify/invoiceverify.py verify '<JSON_BODY>'`。  
4. 从返回结果中读取销售方、购买方、税额、发票状态、明细行等信息，并向用户总结发票是否有效及其关键信息。  
5. 如需提示发票类型选择，可先调用 `python3 skills/invoiceverify/invoiceverify.py type` 获取支持的发票类型列表，为用户解释不同发票类型的含义。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

