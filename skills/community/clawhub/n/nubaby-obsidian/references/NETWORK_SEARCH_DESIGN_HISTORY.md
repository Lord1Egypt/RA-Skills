# NETWORK_SEARCH_DESIGN_HISTORY (HISTORY)

> **歷史研究 / 設計脈絡**（降噪）：不是當前日常操作入口。
> 
> 現行規則請優先看：
> - `SEARCH_RULES.md`
> - `OPERATIONS_RULES.md`
> - `READONLY_GATEWAY_BOUNDARIES.md`

## 目的
保存 Obsidian 搜尋方案、LAN 安全搜尋、以及其他龍蝦如何安全查 Arthur-OS 的歷史研究結論，供回顧設計脈絡使用。

## 比較對象
### 1. Obsidian Local REST API
- 類型：經典的 Obsidian REST API 外掛
- 主要定位：把 vault 能力直接暴露成 REST 介面
- 公開描述能力：
  - read / create / update / delete notes
  - PATCH 指定段落
  - list notes
  - periodic notes
  - execute commands
  - list available commands
- 公開安全訊號：
  - secure HTTPS interface
  - API key authentication
- 初步判斷：
  - 比較像成熟通用的 REST 基底
  - 生態辨識度高，很多後續橋接工具會拿它當底層
  - 但若直接拿來開 LAN，能力面偏大，不只搜尋

### 2. Obsidian CLI REST
- 類型：把 Obsidian CLI 命令包成 HTTP API + MCP server 的外掛
- 主要定位：agent / automation / MCP 導向的 Obsidian 控制面
- 公開描述能力：
  - files
  - create / read / append / prepend / move / rename / delete
  - search
  - properties / frontmatter
  - daily notes
  - tags / tasks / links / templates / bookmarks
  - plugins / themes / sync / publish / workspaces
  - MCP endpoint（search / execute）
- 公開安全訊號：
  - localhost only by default
  - API key authentication
  - dangerous commands disabled by default
  - per-command blocklist
  - no shell injection
  - 若改成 network mode，仍強制 API key
- 初步判斷：
  - 比較接近 agent 時代的設計語言
  - 安全邊界說明更清楚
  - 但對目前需求來說，仍然太大，不只搜尋

## 差異總結
### API 服務差異
- Local REST API：偏直接 CRUD / command API
- CLI REST：偏 CLI 映射 + MCP + automation control plane

### 權限 / 安全差異
- Local REST API：有 API key、HTTPS；但目前查到的公開摘要中，安全控制細節沒有 CLI REST 講得那麼細
- CLI REST：localhost only、API key、dangerous commands off、blocklist、network mode 仍強制 auth，安全邊界較清楚

### 使用者操作成本
- Local REST API：中等，裝 plugin + 取 API key
- CLI REST：中高，要啟用 CLI、裝 plugin、設定 key、理解 REST/MCP/bind address

### 社群 / 生態感受
- Local REST API：較像經典基礎層，許多橋接工具會基於它來做 MCP 或其他自動化整合
- CLI REST：比較新、agent 導向、設計較現代，但目前沒有足夠硬資料證明其採用量一定更大

## 對 Arthur 場景的結論
Arthur 真正要的不是完整遠端控制 Obsidian，而是：
- 其他龍蝦可搜尋 Arthur-OS
- 區域網路可用
- 但要安全
- 最好先只讀
- 寫入仍盡量由 Mac Studio 主控

所以這兩個方案目前比較適合當：
- **參考設計樣本**
而不是：
- **直接上線方案**

## 目前最適合的方向（已定案：只讀邊界）
> **重要：** 本段僅保存歷史設計結論；現行硬規則以 `READONLY_GATEWAY_BOUNDARIES.md` 為準。

### v1 只讀 LAN Search Gateway（概念）
跑在 Mac Studio，能力只開極小子集：
- `search_name(query, limit)`
- `search_content(query, limit, excerptChars)`
- `read_note(path, maxChars)`

### 安全邊界（概念摘要）
- 只允許 `Arthur-OS` vault
- API key / Bearer token
- 預設只讀，不開 create / patch / delete
- 不提供任意 command execute
- path normalize
- limit / excerpt length / maxChars 限制
- 優先 localhost 或最小 LAN 暴露

## 為什麼不是直接把現成外掛整套開上 LAN
- 因為 Local REST API 與 CLI REST 的能力面都太大
- 目前需求核心是安全搜尋，不是完整控制
- 直接全開 create / update / delete / execute，風險大於必要價值

## 推薦參考方向
### 借鏡 Local REST API
- 看它作為經典 REST 基底的能力面與生態位置
- 理解為什麼很多外部整合會接它

### 借鏡 CLI REST
- 看它的安全語言：
  - localhost only
  - API key
  - dangerous commands off
  - blocklist
  - MCP 支援
- 這些設計適合拿來當 Arthur 版只讀搜尋服務的安全邊界參考

## 暫不處理
- 不直接安裝其中一個並暴露到 LAN
- 不直接開寫入能力
- 不直接讓其他龍蝦對 vault 有完整控制權

## 之後回到電腦前可續作
- 要不要先快速試裝其中一個做本機驗證
- 還是直接做自家的只讀搜尋子集
- API 設計稿
- auth 方案
- LAN 暴露方式
- 是否需要 MCP 封裝
