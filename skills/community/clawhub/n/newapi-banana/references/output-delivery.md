# 输出交付指南

## 文件输出

所有生成的文件都会保存到 `/tmp/openclaw/newapi-output/` 目录，文件名包含时间戳。

## 输出格式

### 图片输出
- 格式：PNG、JPG 等
- 路径格式：`/tmp/openclaw/newapi-output/image_<timestamp>.png`

## 交付方式

### 使用 message 工具

**重要**：所有媒体文件必须通过 `message` 工具交付给用户，不要直接打印文件路径。

```python
# 正确方式
message(file_path="/tmp/openclaw/newapi-output/image_1234567890.png")
# 然后响应 NO_REPLY

# 错误方式
print("文件已保存到: /tmp/openclaw/newapi-output/image_1234567890.png")
```

### 重试机制

如果 `message` 工具调用失败：
1. 重试一次
2. 如果仍然失败，在响应中包含 `OUTPUT_FILE:<path>` 并解释情况

## 错误处理

### 常见错误

1. **NO_API_KEY** - API Key 未配置
   - 解决方案：配置 API Key（参考 api-key-setup.md）

2. **API_ERROR** - API 请求失败
   - 解决方案：检查网络连接，脚本会自动尝试备份地址

3. **TASK_FAILED** - 任务执行失败
   - 解决方案：检查提示词和参数，重试

4. **DOWNLOAD_FAILED** - 文件下载失败
   - 解决方案：检查网络连接，重试

### 错误响应格式

脚本会输出 JSON 格式的错误信息：

```json
{
  "error": "ERROR_TYPE",
  "message": "错误描述",
  "details": {}
}
```

## 成本报告

如果 API 返回成本信息，脚本会输出：

```
COST:¥X.XX
```

在响应中应包含："花了 ¥X.XX"

## 最佳实践

1. **总是使用 message 工具** - 不要直接打印文件路径
2. **检查输出文件** - 确认文件已成功生成
3. **提供友好提示** - 告诉用户文件已生成
4. **建议下一步** - 例如"需要调整一下吗？"
