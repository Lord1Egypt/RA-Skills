# Pay Skill 打包标准 — SkillHub 官方规范

> 来源: https://skillhub.cn/skillpay
> 存档时间: 2026-07-30
> 适用范围: 所有昆仑瑶池出品的付费 Skill 包

## 是什么
Pay Skill 是 SkillHub 上支持微信 Agent Pay 支付的付费技能。AI Agent 调用时触发支付 → 用户授权 → Agent 继续获取付费内容。

## 改造前确认清单
- [x] 企业认证通过（沈阳百事通网络科技有限公司）
- [ ] 绑定微信商户号（SkillHub 后台 → 商户入驻）
- [x] 已有微信支付下单能力（WXPAY_MCHID 等已配置）
- [ ] 已发布 Skill 并设置定价（SkillHub 后台）

## X402 架构四段
1. 企业服务生成微信支付订单 → code_url
2. SkillHub 开发者密钥签名 → 调 X402 预下单 → payment_code
3. WeixinPay-Required 返回给 Agent
4. Agent 向用户申请支付授权 → 获取付费内容

## 接入步骤
### Step 1: 生成开发者密钥
- pub_key_id: PUB_KEY_ + 32位大写 HEX
- private_key_pem: RSA 2048 PEM，仅展示一次，SkillHub 不存储

### Step 2: 微信支付 Native 下单
POST /v3/pay/transactions/native → code_url

### Step 3: X402 AI 预下单（纯 Body RSA 鉴权）
L2 业务 JSON → Base64 → L1 签名 → POST /preorder → payment_code

签名串 5 行（每行 \n 结尾）:
```
POST\n
/palmpayminiapp/clawagentpay/preorder\n
{timestamp}\n
{nonce_str}\n
{payment_required}\n
```

- signature_type: SKILLHUB-SHA256-RSA2048
- developer_platform: SKILLHUB
- SHA256withRSA (PKCS#1 v1.5) + Base64 编码

### Step 4: 返回 402
- Header: WeixinPay-Required + X-Out-Trade-No
- Body: JSON 含 WeixinPay 提示块

## pay_data 格式
```json
{"type": "code_url", "value": "weixin://wxpay/bizpayurl?pr=xxx"}
```

## 关键约束
- 纯 Body 鉴权，不用 Authorization 头
- product_id 格式 SPxxx
- expires_at 最长 15 分钟（900 秒）
- 同商户最多 3 组有效密钥
