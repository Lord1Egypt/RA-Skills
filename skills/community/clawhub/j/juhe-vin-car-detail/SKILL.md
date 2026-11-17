---
name: juhe-vin-car-detail
description: VIN查车辆信息-精准版。通过17位车架号查询品牌、车系、车型、年款、排量、排放标准、外形尺寸、轮胎规格、变速器、公告号、轴距等出厂参数。使用场景：用户说"VIN查车"、"车架号查车"、"查车型配置"、"这个VIN是什么车"、"排量排放"、"厂商指导价"、"二手车核对配置"等。通过聚合数据（juhe.cn）API 实时查询。
homepage: https://www.juhe.cn/docs/api/id/862
metadata: {"openclaw":{"emoji":"🚗","requires":{"bins":["python3"],"env":["JUHE_VIN_CAR_DETAIL_KEY"]},"primaryEnv":"JUHE_VIN_CAR_DETAIL_KEY"}}
---

# VIN 查车辆信息（精准版）

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

通过 17 位 VIN（车架号）查询车辆出厂档案：品牌、车系、销售车型、排量、排放标准、外形尺寸、轮胎规格、变速器类型、公告号、轴距等。

> 查得计费。需提交应用场景审核。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 注册账号
2. 进入 [VIN查车辆信息-精准版 API](https://www.juhe.cn/docs/api/id/862) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_VIN_CAR_DETAIL_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_VIN_CAR_DETAIL_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/vin_info.py --key 你的 AppKey --vin LBV21AF05MSZ88595
```

---

## 使用方法

```bash
python scripts/vin_info.py --vin LBV21AF05MSZ88595
```

输出示例：

```
🚗 VIN 查车辆信息（精准版）

VIN：LBV21AF05MSZ88595
车型：2021款 525Li 2.0T 自动 M运动套装

基本信息
   一级品牌：宝马
   二级品牌：华晨宝马
   车系：5系
   年款：2021
   厂商指导价(元)：426,900
   ...
```

### 直接调用 API（无需脚本）

```
GET https://apis.juhe.cn/carinfo/vinInfo?key=YOUR_KEY&vin=LBV21AF05MSZ88595
```

---

## AI 使用指南

当用户需要按车架号查车时，按以下步骤操作：

1. **收集信息** — 从用户消息中获取 VIN / 车架号
2. **验证格式** — 去除空格和连字符后须为 17 位，且不含字母 I、O、Q
3. **调用脚本或 API** — 执行查询
4. **展示结果** — 按基本信息、动力排放、车身尺寸分组展示；空字段可省略

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `vin` | 是 | 17 位车架号 |
| `key` | 是 | 聚合数据 AppKey |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `vin` | 车架号 | LBV21AF05MSZ88595 |
| `amMainBrandName` | 一级品牌 | 宝马 |
| `amBrandName` | 二级品牌 | 华晨宝马 |
| `amSeriesName` | 车系 | 5系 |
| `amVehicleName` | 销售车型 | 2021款 525Li 2.0T 自动 M运动套装 |
| `amYear` | 年款 | 2021 |
| `amVinYear` | VIN 出厂年份 | 2021 |
| `price` | 厂商指导价(元) | 426900 |
| `purchasePrice` | 新车市场价 | 405000 |
| `displacement` | 排量(L) | 2.0 |
| `powerType` | 动力类型 | 汽油 |
| `effluentStandard` | 排放标准 | 国Ⅵ |
| `vehicleSize` | 外形尺寸 | 5106*1868*1500 |
| `wheelBase` | 轴距(mm) | 3105 |
| `gearboxType` | 变速器类型 | 手自一体 |
| `frontTyreSize` / `rearTyreSize` | 轮胎规格 | 245/45 R18 |
| `publicationNos` | 公告号 | BMW7201LN |
| `engineModel` | 发动机型号 | B48B20C |
| `importFlag` | 国产/进口 | 合资 |

完整字段还包括车型分类、座位数、车门数、驱动形式、燃油标号、整备质量、ABS、底盘号、停产日期等，见脚本 JSON 输出。

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/862) 重新申请 |
| `error_code` 10012 | 当日调用次数已用尽，建议升级套餐 |
| `error_code` 286201 | 车架号格式错误，须为 17 位且不含 I/O/Q |
| `error_code` 286204 | 查无记录 |
| `error_code` 286202/286203 | 网络或查询失败，告知稍后重试 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

---

## 脚本位置

`scripts/vin_info.py` — 封装了 VIN 清洗校验、API 调用、分组展示和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **车辆数据**：VIN 查车辆信息、VIN 码查车五项、营运车辆判定
- **企业数据**：企业工商信息、被执行人、限制高消费
- **身份核验**：手机号实名认证、身份证实名验证、银行卡认证
- **生活服务**：天气预报、万年历、快递查询

注册并完成接口审核后即可使用。
