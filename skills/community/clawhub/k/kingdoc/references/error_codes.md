# KingDoc 完整错误码

| 错误码 | 类型 | 含义 | 解决方案 |
|--------|------|------|---------|
| KD001 | AuthError | Token 鉴权失败 | 重新执行 setup 授权 |
| KD002 | PermissionError | 权限不足 | 升级应用权限或联系管理员 |
| KD003 | QuotaError | API 配额不足 | 申请提额或购买配额 |
| KD004 | DocTypeError | 文档类型不匹配 | 执行 file.info 确认品类 |
| KD005 | DocNotFoundError | 文档不存在 | 检查 file_id 是否正确 |
| KD006 | RateLimitError | 请求限流（429） | 自动指数退避重试 |
| KD007 | VersionConflictError | 文档版本冲突 | 获取最新版本后重新写入 |
| KD008 | FileTooLargeError | 文件过大 | 走异步上传或压缩 |
| KD009 | FileTypeBlockedError | 文件类型被拦截 | 检查 MIME 类型 |
| KD010 | ServiceUnavailableError | 服务暂时不可用 | 稍后重试 |
| KD011 | ParamError | 请求参数错误 | 检查必填参数 |
| KD012 | FolderNotFoundError | 文件夹不存在 | 检查 folder_id |
| KD013 | FormClosedError | 收集表已截止 | 收集表已过截止日期 |
| KD014 | WebhookError | Webhook 回调失败 | 检查回调 URL |
| KD015 | ConvertError | 格式转换失败 | 格式不支持或文件损坏 |
