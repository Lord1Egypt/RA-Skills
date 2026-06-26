---
name: payment_skill
description: AI 原生支付解决方案 - 提供安全、可靠的支付功能
version: 1.0.3
author: Payment Institution
license: MIT
tags:
  - payment
  - finance
  - commerce
skill_type: code
has_server: false
has_install_scripts: true
security_level: high
requires:
  - python>=3.6
environment_variables:
  required:
    - PAYMENT_API_KEY: "API 密钥，用于身份认证"
    - PAYMENT_API_SECRET: "API 密钥，用于请求签名"
  optional:
    - PAYMENT_API_URL: "支付 API 地址，默认 https://api.zlclaw.com"
    - PAYMENT_ENCRYPTION_KEY: "32 字节加密密钥（可选）"
    - PAYMENT_LOG_LEVEL: "日志级别，默认 INFO"
tools:
  - name: create_payment
    description: 创建支付请求，触发用户授权流程
    parameters:
      - name: amount
        type: number
        description: 支付金额，最多2位小数
        required: true
        example: 299.00
      - name: currency
        type: string
        description: ISO 4217 货币代码
        required: false
        default: CNY
        example: CNY
      - name: merchant_id
        type: string
        description: 商户唯一标识
        required: true
        example: taobao_merchant_001
      - name: description
        type: string
        description: 支付描述，用户可见
        required: false
        example: 购买无线鼠标
    returns:
      type: object
      properties:
        success:
          type: boolean
          description: 是否成功
        transaction_id:
          type: string
          description: 交易ID
        status:
          type: string
          description: 支付状态
        amount:
          type: number
          description: 支付金额
        currency:
          type: string
          description: 货币代码
        verification_url:
          type: string
          description: 验证URL
        qr_code:
          type: string
          description: 二维码数据
  
  - name: query_payment
    description: 查询支付状态
    parameters:
      - name: transaction_id
        type: string
        description: 交易 ID
        required: true
        example: txn_20260315_001
    returns:
      type: object
      properties:
        success:
          type: boolean
          description: 是否成功
        transaction_id:
          type: string
          description: 交易ID
        status:
          type: string
          description: 支付状态
        amount:
          type: number
          description: 支付金额
  
  - name: refund_payment
    description: 发起退款
    parameters:
      - name: transaction_id
        type: string
        description: 原交易 ID
        required: true
        example: txn_20260315_001
      - name: amount
        type: number
        description: 退款金额（可选，不填则全额退款）
        required: false
        example: 100.00
      - name: reason
        type: string
        description: 退款原因
        required: false
        example: 商品质量问题
    returns:
      type: object
      properties:
        success:
          type: boolean
          description: 是否成功
        refund_id:
          type: string
          description: 退款ID
        status:
          type: string
          description: 退款状态
        amount:
          type: number
          description: 退款金额
---

# 支付 Skill

AI 原生支付解决方案，提供安全、可靠的支付功能。

## 工具调用方式

AI 通过执行 `skill_cli.py` 脚本来调用工具：

```bash
python skill_cli.py <tool_name> --param1=value1 --param2=value2
```

**示例**：
```bash
# 创建支付
python skill_cli.py create_payment --amount=299.00 --currency=CNY --merchant_id=taobao_001 --description="购买商品"

# 查询支付
python skill_cli.py query_payment --transaction_id=txn_001

# 发起退款
python skill_cli.py refund_payment --transaction_id=txn_001 --amount=100.00 --reason="质量问题"
```

**返回格式**：所有工具都返回 JSON 格式的结果
```json
{
  "success": true,
  "data": { ... }
}
```

## 快速开始

### 1. 安装依赖

```bash
# Linux/macOS
./scripts/setup.sh

# Windows
scripts\setup.bat
```

### 2. 配置环境变量

**必需**：
```bash
export PAYMENT_API_KEY=your_api_key
export PAYMENT_API_SECRET=your_api_secret
```

**可选**：
```bash
export PAYMENT_API_URL=https://api.zlclaw.com
```

### 3. 使用示例

```bash
# 创建支付
python skill_cli.py create_payment --amount=299.00 --currency=CNY --merchant_id=taobao_001

# 查询支付
python skill_cli.py query_payment --transaction_id=txn_001

# 发起退款
python skill_cli.py refund_payment --transaction_id=txn_001 --amount=100.00
```

## 核心功能

- **create_payment**: 创建支付请求
- **query_payment**: 查询支付状态
- **refund_payment**: 发起退款

## 安全特性

- TLS 加密通信
- HMAC-SHA256 签名
- 参数验证
- 审计日志

## 技术要求

- Python 3.6+
- 网络访问权限
- 环境变量配置

## 支持

- 📧 技术支持: dev@zlclaw.com
- 🐛 问题报告: https://github.com/zlclaw/payment-skill/issues

---

**版本**: 1.0.3 | **许可证**: MIT
