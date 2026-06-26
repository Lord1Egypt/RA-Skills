# AIOB 认证（来自 `生成认证.md`）

## 目标
先调用获取 token 接口，拿到 `accessToken`，再用于后续外呼接口的 `Authorization` 头。

## 接口
- URL: `https://aiob-open.baidu.com/api/v2/getToken`
- Method: `POST`
- Header: `Content-Type: application/json`
- Body:
  - `accessKey` (string, required)
  - `secretKey` (string, required)

## 成功响应关键字段
- `code = 200`
- `data.accessToken`：后续请求使用
- `data.expiresTime`：有效期（分钟）

## 安全约束
- 不要在日志、聊天消息、代码仓库中明文暴露 AK/SK 或 token
- 凭证泄露时，立刻在控制台轮换/删除密钥
