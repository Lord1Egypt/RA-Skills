# 快递100用户版 - 完整字段说明

## 地址簿信息（来自 kd100 sender / kd100 receiver）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 地址ID |
| name | string | 姓名 |
| mobile | string | 手机号（下单时映射为 `--sender-phone` / `--receiver-phone`） |
| province | string | 省份 |
| city | string | 城市 |
| district | string | 区县 |
| addr | string | 详细地址（下单时映射为 `--sender-address` / `--receiver-address`） |
| tel | string | 座机电话 |
| latitude | string | 纬度 |
| longitude | string | 经度 |
| xzqName | string | 行政区名称 |

---

## 快递公司信息（来自 kd100 companies）

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 快递公司名称（下单时映射为 `--kuaidi-name`） |
| com | string | 快递公司编码（下单时映射为 `--kuaidi-com`） |
| sign | string | 签名标识（下单时映射为 `--company-sign`，下单必传） |
| totalprice | number | 总运费（下单时映射为 `--estimated-amount`） |
| arriveTipsDate | string | 预计送达时间 |
| priceInfo | string | 价格信息字符串（如"18元，1-2天"） |
| logo | string | 快递公司 logo URL |
| firstPrice | number | 首重价格 |
| overPricePerKg | number | 续重价格 |

---

## 地址解析结果（来自 kd100 address）

| 字段 | 类型 | 说明 |
|------|------|------|
| resultCode | boolean | 是否解析成功 |
| message | string | 解析结果消息 |
| province | string | 省份 |
| city | string | 城市 |
| district | string | 区县 |
| subArea | string | 详细地址（不含省市区） |

---

## 物品重量（来自 kd100 weight）

| 字段 | 类型 | 说明 |
|------|------|------|
| original_name | string | 原始物品名称 |
| item_name | string | 物品展示名称 |
| spec_weight | string | 标准重量（**字符串**，需 parseFloat() 转换） |
| category | string | 物品分类 |
| restriction_level | string | 限制级别 |
| package_volume | string | 包装体积 |
| label_express_delivery | string | 快递标签（如"含锂电池"） |
| auditor | string | 审核人 |
| audit_status | number | 审核状态 |
| selected_count | number | 选择次数 |

---

## 下单返回（来自 kd100 order create）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| data.orderInfo.orderNo | string | 订单编号 |
| data.orderInfo.status | string | 订单状态 |
| data.orderInfo.createTime | string | 下单时间 |
| data.orderInfo.itemName | string | 物品名称 |
| data.orderInfo.kuaidiName | string | 快递公司名称 |
| data.url | string | 微信小程序链接 |
| data.qrCode | string | 二维码链接 |
| data.markdownInfo | string | Markdown 格式订单信息 |

---

## 物流轨迹（来自 kd100 order track）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| data.com | string | 快递公司编码 |
| data.nu | string | 运单号 |
| data.state | string | 物流状态 |
| data.data | array | 轨迹列表 |
| data.data[].time | string | 时间 |
| data.data[].context | string | 物流描述 |

---

## SSO 分步登录响应（降级：`kd100 auth login --no-wait --json`）

仅在 `--open` 无法自动打开浏览器时使用。正常登录请用 `kd100 auth login --open`，**Agent 不得代为打开链接**。

| 字段 | 类型 | 说明 |
|------|------|------|
| data.verificationUriComplete | string | 完整授权 URL（由后端返回，CLI 打开 / 降级时展示此字段） |
| data.deviceCode | string | 设备码，供 `--device-code` 轮询使用 |
| data.userCode | string | 用户授权码（供 CLI 内部使用，Agent 无需拼接 URL） |
| data.expiresIn | number | 授权链接有效期（秒） |

> 降级时 Agent **仅文本展示**链接，提示用户自行复制到外部浏览器打开；**禁止** Agent 代为打开。

---

## 错误响应

CLI 错误统一输出到 stderr：

```json
{"status": 401, "message": "未登录，请先执行 kuaidi100-cli auth login", "keyRequired": true}
```

| status | 说明 |
|--------|------|
| 400 | 参数错误 |
| 401 | 未登录或登录已失效，提示 `kd100 auth login --open` 重新登录 |
| 404 | 资源不存在 |
| 429 | 请求频率超限 |
| 500 | 系统异常 |
