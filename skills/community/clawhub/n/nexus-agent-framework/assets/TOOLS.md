# TOOLS.md - 工具配置 | Tool Configuration
# 版本 Version: 1.0.0 | 更新 Updated: 2026-03-24

---

## 概述 | Overview

本文件記錄所有可用工具的配置、使用注意事項和安全設置。

This file documents all available tools, their configurations, usage notes, and security settings.

---

## 工具分類 | Tool Categories

### 🔧 系統工具 | System Tools

| 工具 | 功能 | 風險等級 | 默認狀態 |
|------|------|----------|----------|
| bash | 執行系統命令 | 🔴 高 | 需確認 |
| file_read | 讀取文件 | 🟡 中 | 開啟 |
| file_write | 寫入文件 | 🔴 高 | 需確認 |
| glob | 搜索文件 | 🟢 低 | 開啟 |

| Tool | Function | Risk Level | Default Status |
|------|----------|------------|---------------|
| bash | Execute system commands | 🔴 High | Requires confirm |
| file_read | Read files | 🟡 Medium | Enabled |
| file_write | Write files | 🔴 High | Requires confirm |
| glob | Search files | 🟢 Low | Enabled |

### 🌐 網絡工具 | Network Tools

| 工具 | 功能 | 風險等級 | 默認狀態 |
|------|------|----------|----------|
| web_search | 網絡搜索 | 🟡 中 | 需確認 |
| web_fetch | 獲取網頁 | 🟡 中 | 需確認 |
| api_call | API 調用 | 🔴 高 | 需確認 |

| Tool | Function | Risk Level | Default Status |
|------|----------|------------|---------------|
| web_search | Web search | 🟡 Medium | Requires confirm |
| web_fetch | Fetch web pages | 🟡 Medium | Requires confirm |
| api_call | API calls | 🔴 High | Requires confirm |

### 📊 數據工具 | Data Tools

| 工具 | 功能 | 風險等級 | 默認狀態 |
|------|------|----------|----------|
| data_process | 數據處理 | 🟢 低 | 開啟 |
| data_visualize | 數據可視化 | 🟢 低 | 開啟 |

---

## 工具配置模板 | Tool Configuration Template

```markdown
## [工具名] | [Tool Name]
### 狀態 | Status: [開啟/關閉/需確認]

### 基本配置 | Basic Config
- 超時時間: [N] 秒
- 最大重試: [N] 次
- 默認參數: [列出]

### 安全設置 | Security Settings
- [ ] 需要用戶確認
- [ ] 記錄所有操作
- [ ] 限制訪問路徑
- [ ] 限制網絡目標

### 使用示例 | Usage Examples
```示例代碼
[使用示例]
```

### 注意事項 | Gotchas
1. [注意事項1]
2. [注意事項2]
```

---

## 敏感操作設置 | Sensitive Operation Settings

### 🔴 高風險操作 | High-Risk Operations

```markdown
## 高風險操作 | High-Risk Operations

### 需要明確授權 | Requires Explicit Authorization
1. 刪除文件或目錄
2. 執行系統命令
3. 修改配置文件
4. 訪問外部 API
5. 處理敏感數據

### 授權格式 | Authorization Format
```markdown
用戶確認:
[是/否] 允許執行 [操作描述]
額外限制: [如有]
```
```

### 🟡 中風險操作 | Medium-Risk Operations

```markdown
## 中風險操作 | Medium-Risk Operations

### 需要簡單確認 | Requires Simple Confirmation
1. 讀取文件
2. 搜索內容
3. 獲取網頁信息
4. 創建新文件

### 確認格式 | Confirmation Format
```markdown
即將執行: [操作描述]
[自動確認/需要回复]
```
```

---

## 憑證管理 | Credential Management

### 存儲原則 | Storage Principles

1. **永遠不**將憑證寫入代碼
2. **永遠不**將憑證寫入日誌
3. **永遠**使用環境變量或專用配置
4. **永遠**記錄憑證訪問（不含實際值）

### 環境變量格式 | Environment Variable Format

```markdown
## 環境變量 | Environment Variables
| 變量名 | 用途 | 狀態 |
|--------|------|------|
| API_KEY_* | API 密鑰 | 已配置/待配置 |
| DATABASE_URL | 數據庫連接 | 待配置 |
| SECRET_* | 其他密鑰 | 待配置 |

## 配置檢查 | Configuration Check
- [ ] 所有必需變量已設置
- [ ] 變量格式正確
- [ ] 測試連接成功
```

---

## 工具使用日誌 | Tool Usage Log

```markdown
## 使用日誌 | Usage Log

### 今日使用 | Today's Usage
| 時間 | 工具 | 操作 | 結果 |
|------|------|------|------|
| HH:MM | bash | ls -la | ✅ |

### 異常記錄 | Anomaly Records
[記錄任何工具使用異常]
```

---

## 自定義工具 | Custom Tools

```markdown
## 自定義工具 | Custom Tools

### [工具名稱]
- 描述: [功能描述]
- 創建日期: [日期]
- 最後更新: [日期]
- 配置: [配置詳情]
- 使用記錄: [使用統計]
```

---

## 故障排除 | Troubleshooting

### 工具不可用 | Tool Unavailable

```markdown
## 工具不可用 | Tool Unavailable

### 檢查清單 | Checklist
1. [ ] 工具是否已正確配置
2. [ ] 是否有所需的依賴
3. [ ] 權限是否足夠
4. [ ] 環境變量是否正確

### 解決方案 | Solutions
1. [ ] 重新配置工具
2. [ ] 安裝依賴
3. [ ] 請求更高權限
4. [ ] 檢查環境變量
```

---

## 安全審核清單 | Security Audit Checklist

- [ ] 所有工具都有明確的風險等級
- [ ] 高風險工具默認需要確認
- [ ] 憑證使用環境變量
- [ ] 操作日誌完整記錄
- [ ] 無硬編碼的敏感信息
- [ ] 自定義工具經過安全審核

---

*🔧 TOOLS.md - 安全使用工具，放心工作*
*🔧 TOOLS.md - Use tools safely, work with confidence*
