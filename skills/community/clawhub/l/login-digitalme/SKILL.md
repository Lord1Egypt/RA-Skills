---
name: sms-login
description: 通过手机短信验证码完成用户登录/注册，包含发送验证码和验证码登录两个接口。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      env:
        - 180.184.28.174:30080
    primaryEnv: 180.184.28.174:30080
---

# 短信验证码登录

通过手机号和短信验证码实现用户快速登录或自动注册。

## 何时使用

当用户要求：发送手机验证码、用手机号登录、用验证码登录、手机号注册 时，使用此 skill。

## 前置条件

- 环境变量 `SMS_LOGIN_BASE_URL` 已设置为 API 服务器地址
- 系统已安装 `curl` 和 `jq`

---

## 步骤一：发送验证码

向用户确认手机号后，发送验证码：

```bash
curl -s -X POST "${SMS_LOGIN_BASE_URL}/api/v1/auth/phone/send" \
  -H "Content-Type: application/json" \
  -d '{"phone": "'"${PHONE}"'"}' | jq .
```

### 响应判断

| 条件 | 含义 | 下一步 |
|------|------|--------|
| `code == 200` | 发送成功 | 提示用户查看短信，进入步骤二 |
| HTTP 400 | 手机号格式错误 | 提示用户检查手机号，重新输入 |
| `code == 500` | 限流或系统错误 | 展示 `message` 内容，稍后重试 |

---

## 步骤二：验证码登录

向用户索要短信中的验证码后，发起登录：

```bash
curl -s -c - -X POST "${SMS_LOGIN_BASE_URL}/api/v1/auth/phone/login" \
  -H "Content-Type: application/json" \
  -d '{"phone": "'"${PHONE}"'", "code": "'"${CODE}"'"}' | jq .
```

### 响应判断

| 条件 | 含义 | 下一步 |
|------|------|--------|
| `code == 200` | 登录成功 | 从 `data.token` 提取 token，后续请求用 `Authorization: Bearer <token>` |
| HTTP 400 | 参数缺失/格式错误 | 提示用户重新输入 |
| `code == 401` | 验证码错误或已过期 | 建议用户重新获取验证码，回到步骤一 |

登录成功时，响应头会设置 `Set-Cookie: token=<value>`，浏览器场景会自动维持会话。

---

## Rules

- 手机号必须由用户明确提供，禁止猜测或自动填充
- 验证码必须由用户手动输入，禁止尝试自动获取或暴力枚举
- 同一手机号 60 秒内不得重复发送验证码
- 输出中不要暴露完整 token，最多显示前 20 个字符加省略号
- 中国大陆手机号为 11 位数字且以 1 开头，发送前先做格式校验
- 登录失败时必须向用户展示具体错误信息