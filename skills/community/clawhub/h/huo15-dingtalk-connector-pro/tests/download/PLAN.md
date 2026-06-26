# Download 模块测试方案

## 1. 模块划分与职责

本套件覆盖“下载图片/媒体/文件”的辅助函数（HTTP 获取 + 本地落盘 + 文件名处理）：

- **downloadImageToFile(url, log)**：根据响应 `content-type` 推断扩展名并写入到 `~/.openclaw/workspace/media/inbound/`，返回本地路径；失败返回 null。
- **downloadMediaByCode(downloadCode, config, log)**：通过下载码换取下载链接并下载媒体，返回本地路径；失败返回 null。
- **downloadFileByCode(downloadCode, originalFileName, config, log)**：下载文件并尽可能保留原始文件名，同时对非法字符进行清理；失败返回 null。

## 2. 用例表（覆盖现有测试）

### 2.1 downloadImageToFile

| 序号 | 场景 | mock headers.content-type | 期望 | 说明 |
|------|------|---------------------------|------|------|
| 1 | jpg | `image/jpeg` | 路径以 `.jpg` 结尾 | 默认 |
| 2 | png | `image/png` | `.png` |  |
| 3 | gif | `image/gif` | `.gif` |  |
| 4 | webp | `image/webp` | `.webp` |  |
| 5 | 未知类型 | `application/octet-stream` | `.jpg` | 回退 |
| 6 | 下载失败 | axios.get 抛错 | null | error |

并验证：路径落在 `~/.openclaw/workspace/media/inbound/` 且记录 info 日志。

### 2.2 downloadMediaByCode

| 序号 | 场景 | downloadCode→url 响应 | 期望 | 说明 |
|------|------|------------------------|------|------|
| 7 | 成功 | `data.downloadUrl` 存在 | 返回本地路径 | 组合调用 |
| 8 | 无 downloadUrl | 返回 errcode/errmsg 或缺字段 | null + warn | API 异常但不抛 |
| 9 | API 错误 | axios.post 抛错 | null + error |  |

### 2.3 downloadFileByCode

| 序号 | 场景 | originalFileName | 期望 | 说明 |
|------|------|------------------|------|------|
| 10 | 成功保留文件名 | `report.pdf` | 结果以 `report.pdf` 结尾 | 尽可能保留 |
| 11 | 清理非法字符 | `file/with:invalid*chars.pdf` | 返回文件名（basename）不含 `\\:*?"<>|` | 完整路径必然包含 `/`，因此只校验文件名 |
| 12 | 无 downloadUrl | 响应缺字段 | null + warn |  |
| 13 | API 错误 | axios.post 抛错 | null + error |  |

## 3. 预期正确输出与潜在错误

- **正确**：content-type→扩展名映射正确；下载失败不抛异常；文件名清理规则能避免路径穿越/非法字符；目录创建与写入行为可被 mock。
- **潜在错误原因**：忽略 content-type 导致扩展名错误；未清理文件名导致写入失败或安全问题；API 返回结构变更未判空；错误路径未记录日志导致排障困难。

