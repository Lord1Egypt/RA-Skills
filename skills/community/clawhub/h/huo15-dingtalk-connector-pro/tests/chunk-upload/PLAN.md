# chunk-upload（分块上传）测试方案

## 1. 目的与覆盖范围

`tests/chunk-upload` 覆盖大文件分块上传的完整流程，包括事务启用、分块上传、事务提交和编排流程。

主要覆盖（以测试文件实际引用为准）：

- **enableUploadTransaction**：启用上传事务并获取 upload_id
- **uploadFileBlock**：上传单个文件分块
- **submitUploadTransaction**：提交上传事务获取最终结果
- **uploadLargeFileByChunks**：编排完整上传流程
- **CHUNK_CONFIG**：分块配置常量

## 2. 用例表（覆盖现有测试）

### 2.1 enableUploadTransaction

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | API 成功 | 返回 upload_id |
| 2 | API 返回错误 | 返回 null |
| 3 | 网络异常 | 返回 null |

### 2.2 uploadFileBlock

| 序号 | 场景 | 期望 |
|------|------|------|
| 4 | 上传成功 | 返回 true |
| 5 | API 返回错误 | 返回 false |
| 6 | 网络异常 | 返回 false |

### 2.3 submitUploadTransaction

| 序号 | 场景 | 期望 |
|------|------|------|
| 7 | 提交成功 | 返回 `{ fileId, downloadCode }` |
| 8 | API 返回错误 | 返回 null |
| 9 | 网络异常 | 返回 null |

### 2.4 uploadLargeFileByChunks

| 序号 | 场景 | 期望 |
|------|------|------|
| 10 | 完整上传流程 | 返回 download_code |
| 11 | 文件不存在 | 返回 null |

### 2.5 CHUNK_CONFIG

| 序号 | 场景 | 期望 |
|------|------|------|
| 12 | 读取配置 | SIZE_THRESHOLD 为 20MB |

## 3. 预期正确输出与潜在错误

- **正确**：事务启用、分块上传、事务提交三个阶段正确协调；错误被正确收敛为 null/false；文件存在性检查有效；配置常量符合预期。
- **潜在错误原因**：分块大小与服务器要求不匹配；事务 ID 传递错误；文件读取失败未正确处理；网络重试逻辑缺失。
