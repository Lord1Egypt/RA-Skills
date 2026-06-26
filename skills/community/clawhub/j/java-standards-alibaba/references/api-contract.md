# 前后端规约

> 来源: Java开发手册（嵩山版）— 一(十) 前后端规约

## 【强制】规则

### 1. API 定义明确

前后端交互的 API，需要明确协议、域名、路径、请求方法、请求内容、状态码、响应体。

- **协议**: 生产环境必须使用 HTTPS
- **路径**: 资源名词，推荐复数，不用于动词；不大写；不带 `.json` 等后缀
- **请求方法**: GET(取)、POST(新建)、PUT(更新)、DELETE(删除)
- **请求内容**: URL 无敏感信息；body 参数设 Content-Type
- **响应体**: 由 Content-Type 头确定

### 2. 空列表返回 [] 或 {}

前后端数据列表接口，如果为空，返回空数组 `[]` 或空集合 `{}`，不要返回 null。

### 3. 错误响应四部分

服务端错误时，响应必须包含: HTTP 状态码、`errorCode`、`errorMessage`、用户提示信息。

### 4. JSON key 用 lowerCamelCase

所有 key 必须为小写字母开始的 `lowerCamelCase` 风格。

> **正例**: `errorCode` / `assetStatus` / `menuList`  
> **反例**: `ERRORCODE` / `ERROR_CODE` / `error_message`

### 5. errorMessage 用于追踪

可在前端输出到 `type="hidden"` 控件或用户端日志中。

### 6. 超大整数用 String 返回

服务端一律使用 String 字符串类型返回，禁止使用 Long。JS 的 Number 超过 2^53 有精度损失。

> **反例**: 订单号 362909601374617692，前端收到的却是 362909601374617660

### 7. URL 参数 ≤ 2048 字节

不同浏览器对 URL 长度限制不同，2048 是最小值。

### 8. body 长度控制

nginx 默认限制 1MB，tomcat 默认 2MB。

### 9. 翻页参数处理

- 前端: 用户输入 < 1，返回第一页参数给后端
- 后端: 参数 > 总页数，直接返回最后一页

### 10. 重定向

服务器内部重定向必须使用 `forward`；外部重定向地址必须使用 URL 统一代理模块生成。

## 【推荐】规则

### 11. 标记缓存

服务器返回信息必须标记是否可以缓存。

> **正例**: `response.setHeader("Cache-Control", "s-maxage=" + cacheSeconds);`

### 12. JSON 格式优先

服务端返回数据使用 JSON，而非 XML。

### 13. 时间格式统一

前后端时间格式统一为 `"yyyy-MM-dd HH:mm:ss"`，统一为 GMT。

### 14. 版本号在 HTTP 头

接口路径中不要加入版本号，版本控制在 HTTP 头信息中体现。
