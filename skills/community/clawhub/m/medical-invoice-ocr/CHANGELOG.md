# 变更日志

## [1.0.0] - 2025-04-10

### 新增
- 初始版本发布
- 支持 1 种 OCR 识别类型：医疗发票
- 从 `.env` 文件读取 API Key
- 友好的配置检测和 Token 过期提示
- 输出识别结果为 JSON 格式

## [1.0.1] - 2025-04-13

### 优化
- update channelTag

## [1.0.2] - 2025-04-15

### 优化
- update ClawHub 的安全扫描

## [1.0.3] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V1

## [1.0.4] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V2

## [1.0.5] - 2025-04-16

### 修复
- 修正 skill.yaml 元数据，明确声明 required_env_vars 和 homepage
- 增加环境变量读取支持，兼容 os.environ
- 保留 API 返回的 confidence 字段，与文档一致
- 清理 README 中的内部链接，提升可信度

## [1.0.6] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V3

## [1.0.7] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V4

## [1.0.8] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V5

## [1.0.9] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V6

## [1.1.0] - 2025-04-16

### 安全修复
- **删除脚本中诱导用户将 API Key 粘贴到聊天中的危险提示**
- 修正 homepage 为可验证的官方地址
- 清理 README 内部链接，提升可信度
- 增加 config/.env.example 示例文件
- 保留 API 返回的 confidence 字段

## [1.1.1] - 2025-04-16

### 安全修复
- **删除脚本中所有诱导用户粘贴 API Key 到聊天的提示**
- 修正 homepage 为可验证的官方地址
- 清理 README 内部链接，提升可信度
- 增加 config/.env.example 示例文件
- 保留 API 返回的 confidence 字段
- 增加环境变量读取支持，与文档一致

## [1.1.2] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V7

## [1.1.3] - 2025-04-16

### 优化
- update ClawHub 的安全扫描V8