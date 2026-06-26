# probe（连接探测）测试方案

## 1. 目的与覆盖范围

`tests/probe` 覆盖钉钉连接器的连接探测功能，包括凭证验证、超时处理、API 错误处理和缓存机制。

主要覆盖（以测试文件实际引用为准）：

- 连接探测：**probeDingtalk**
- 缓存清理：**clearProbeCache**

## 2. 用例表（覆盖现有测试）

### 2.1 probeDingtalk

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | 凭证缺失 | 返回 ok=false，错误包含 "missing credentials" |
| 2 | 中止信号预先中止 | 返回 ok=false，错误为 "probe aborted" |
| 3 | Token 请求超时 | 返回 ok=false，错误包含 "timed out" |
| 4 | Token 响应无 accessToken | 返回 ok=false，错误为 "failed to get access token" |
| 5 | Bot 信息 API 错误 | 返回 ok=false，错误为 "API error: bad" |
| 6 | 探测成功并复用缓存 | 返回 ok=true 和 botName，第二次调用复用缓存 |
| 7 | 捕获意外的 fetch 错误 | 返回 ok=false，错误为 "network down" |

## 3. 预期正确输出与潜在错误

- **正确**：探测函数在各种错误场景下返回正确的错误信息；成功时返回 botName；缓存机制正确工作；网络异常被正确捕获。
- **潜在错误原因**：凭证检查逻辑错误；超时处理不当；API 错误响应解析错误；缓存机制失效；网络异常未正确捕获。
