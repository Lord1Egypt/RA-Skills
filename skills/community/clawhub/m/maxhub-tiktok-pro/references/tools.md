# TikTok Tools / TikTok 工具

> 本文件已移除所有反爬签名生成、设备注册、游客Cookie获取、登录加密等高风险端点文档。
> 仅保留与 MaxHub API 的基本交互说明。

## 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 3 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## 错误处理契约

> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 路径错误（404 / 410）
- **第 1 步：必须先做防臆造自检**
- **第 2 步：自检通过后**才能 STOP 并报告"资源不存在"
- **禁止**：改路径段 / 切换平台前缀 / 拼接新路径

### 限流（429）
- 读 `Retry-After` 头退避；最多重试 2 次
- **禁止**：立即重试 / 换端点

### 服务器错误（5xx）
- 等 3s 重试；最多 1 次
- 降级到备用端点（如有）
