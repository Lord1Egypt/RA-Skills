# 物流延迟检测 — API 配置参考

## 一、物流查询 API

### UAPI（推荐，免费额度）

- **官网**: https://uapis.cn
- **接口**: `GET https://uapis.cn/api/v1/misc/tracking/query`
- **认证**: API Key (Bearer Token)
- **费用**: 40积分/次，注册送免费积分
- **支持**: 60+快递公司（自动识别）
- **限制**: 访客积分有限，建议注册

#### 获取 API Key

1. 访问 https://uapis.cn 注册账号
2. 进入控制台 → API密钥
3. 复制 API Key

#### 配置方式

**方式一：环境变量（推荐）**
```bash
export UAPI_API_KEY="your_api_key_here"
```

**方式二：在此文件下方直接填写（仅本地使用）**
```python
# 取消注释并填写
# UAPI_API_KEY = "your_api_key_here"
```

#### 支持的快递公司编码（部分）

| 编码 | 快递公司 | 编码 | 快递公司 |
|------|----------|------|----------|
| SF | 顺丰速运 | YTO | 圆通速递 |
| ZTO | 中通快递 | STO | 申通快递 |
| YUNDA | 韵达快递 | JD | 京东物流 |
| EMS | 邮政EMS | DBL | 德邦快递 |
| HTKY | 百世快递 | BEST | 百世快运 |
| UC | 优速快递 | TTKDEX | 天天快递 |


## 二、短信发送 API

### 阿里云短信（推荐）

- **产品页**: https://www.aliyun.com/product/sms
- **SDK**: `pip install alibabacloud_dysmsapi20170525`
- **费用**: 0.045元/条（国内），新用户免费200条
- **到达率**: 99%+

#### 开通步骤

1. 登录阿里云控制台 → 短信服务
2. 申请短信签名（需企业认证，2个工作日内审核）
3. 申请短信模板（模板内容需包含变量，如 `${content}`）
4. 获取 AccessKey ID 和 AccessKey Secret

#### 配置方式

**方式一：JSON配置文件**
```json
{
  "access_key_id": "your_key",
  "access_key_secret": "your_secret",
  "sign_name": "您的签名",
  "template_code": "SMS_XXXXXX"
}
```

**方式二：环境变量**
```bash
export ALIYUN_ACCESS_KEY_ID="your_key"
export ALIYUN_ACCESS_KEY_SECRET="your_secret"
export SMS_SIGN_NAME="您的签名"
export SMS_TEMPLATE_CODE="SMS_XXXXXX"
```

#### 短信模板示例

模板内容：`${content}`

> 注意：阿里云短信模板中，我们使用单个变量 `${content}` 来传递完整的短信正文。
> 这样可以灵活生成不同风格的话术。

### 腾讯云短信（备用）

- **产品页**: https://cloud.tencent.com/product/sms
- **SDK**: `pip install tencentcloud-sdk-python`
- **费用**: 0.045元/条（国内）

#### 配置方式

**JSON配置文件**
```json
{
  "secret_id": "your_secret_id",
  "secret_key": "your_secret_key",
  "sdk_app_id": "1400XXXXXX",
  "template_id": "1234567",
  "sign_name": "您的签名"
}
```

**环境变量**
```bash
export TENCENT_SECRET_ID="your_id"
export TENCENT_SECRET_KEY="your_key"
export TENCENT_SMS_APP_ID="1400XXXXXX"
export TENCENT_SMS_TEMPLATE_ID="1234567"
export SMS_SIGN_NAME="您的签名"
```


## 三、延迟检测规则配置

规则定义在 `scripts/logistics_checker.py` 的 `DELAY_RULES` 字典中。

| 规则 | 阈值 | 说明 |
|------|------|------|
| shipping_timeout | 48小时 | 下单超48h未发货 |
| transit_stuck | 24小时 | 运输中超过24h无更新 |
| delivery_problem | - | 物流状态异常 |
| estimated_late | - | 超过预计送达时间 |
| no_tracking | 24小时 | 运单号查不到信息 |

如需调整阈值，修改对应规则的 `threshold_hours` 字段即可。


## 四、安抚话术模板

模板定义在 `scripts/sms_sender.py` 的 `MESSAGE_TEMPLATES` 字典中。

支持的变量:
- `{shop_name}` — 店铺名称
- `{customer_name}` — 客户名称
- `{order_id}` — 订单号
- `{tracking_number}` — 运单号
- `{product_name}` — 商品名称
- `{contact_phone}` — 客服电话
- `{compensation}` — 补偿方案
- `{new_eta}` — 新的预计时间
- `{deadline}` — 解决方案期限
- `{cause}` — 延迟原因
- `{delay_days}` — 延迟天数
