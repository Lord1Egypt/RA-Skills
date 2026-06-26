---
name: juhe-verify-bankcard-three
description: 银行卡三要素核验。验证银行卡号、姓名、身份证号三要素是否一致。使用场景：用户说"验证银行卡"、"核验银行卡三要素"、"银行卡实名认证"、"检查银行卡号和身份证是否匹配"、"银行卡三元素检测"等。通过聚合数据（juhe.cn）API实时核验，支持单次查询和批量核验。
homepage: https://www.juhe.cn/docs/api/id/207
metadata: {"openclaw":{"emoji":"💳","requires":{"bins":["python3"],"env":["JUHE_BANKCARD3_KEY"]},"primaryEnv":"JUHE_BANKCARD3_KEY"}}
---

# 银行卡三要素核验

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP查询等 200+ 免费/低价 API。

验证 **银行卡号、姓名、身份证号** 三要素是否一致，用于实名认证、风控校验等场景。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [银行卡三要素核验 API](https://www.juhe.cn/docs/api/id/207) 页面，点击「申请使用」
3. 审核通过后在「我的API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_BANKCARD3_KEY=你的AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_BANKCARD3_KEY=你的AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/verify_bankcard_three.py --key 你的AppKey --bankcard 卡号 --realname 姓名 --idcard 身份证号
```

---

## 使用方法

### 单次核验

```bash
python scripts/verify_bankcard_three.py --bankcard 6228480402564890018 --realname 张三 --idcard 320311198901010101
```

输出示例：

```
💳 核验结果: 一致 ✓

{
  "success": true,
  "bankcard": "6228480402564890018",
  "realname": "张三",
  "idcard": "320311198901010101",
  "res": "1",
  "message": "验证信息一致"
}
```

### 直接调用 API（无需脚本）

```
GET http://v.juhe.cn/verifybankcard3/query?key=YOUR_KEY&bankcard=卡号&realname=姓名&idcard=身份证号
```

---

## AI 使用指南

当用户请求银行卡三要素核验时，按以下步骤操作：

1. **收集信息** — 从用户消息中提取银行卡号、姓名、身份证号
2. **基本校验** — 检查银行卡号是否全为数字且长度合理（15-19位）、身份证号是否为18位
3. **调用脚本或 API** — 执行核验，获取 JSON 结果
4. **展示结果** — 明确告知核验是否一致

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `bankcard` | 银行卡号 | 6228480402564890018 |
| `realname` | 姓名 | 张三 |
| `idcard` | 身份证号 | 320311198901010101 |
| `res` | 核验结果 | 1=一致, 2=不一致 |
| `message` | 结果描述 | 验证信息一致 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/207) 重新申请 |
| `error_code` 10012 | 请求次数超限，建议升级套餐 |
| `error_code` 220703 | 认证失败 |
| 参数错误 | 如银行卡号、姓名、身份证号为空或格式不正确，提示用户提供 |
| 网络超时 | 重试一次，仍失败则告知网络问题 |

### 隐私提醒

银行卡三要素涉及敏感个人信息，AI 在展示结果时应：
- 对银行卡号中间部分脱敏显示（如 6228****0018）
- 对身份证号中间部分脱敏显示（如 3203****0101）
- 提醒用户注意信息安全

---

## 脚本位置

`scripts/verify_bankcard_three.py` — 封装了 API 调用、参数校验、批量核验表格输出和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP查询、DNS解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **物流快递**：100+ 快递公司实时追踪
- **身份核验**：手机号归属地、身份证实名验证、银行卡核验
- **金融数据**：汇率、股票、黄金价格

注册即可免费使用，适合个人开发者和企业接入。
