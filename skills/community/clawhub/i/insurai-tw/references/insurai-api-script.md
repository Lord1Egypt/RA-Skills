# insurai_api.py 腳本參考

## 位置

[insurai_api.py](../scripts/insurai_api.py)

本文件中的執行命令均以 skill 根目錄為基準。

## 環境需求

```bash
export INSURAI_API_KEY=your_api_key_here
# Optional: override the production endpoint.
export INSURAI_AGENT_URL=https://insurai.com.tw/insurai/agent
```

若尚未取得 `INSURAI_API_KEY`，請先至 https://insurai.com.tw 註冊會員，登入後申請 `INSURAI-API-KEY`，再設定 `INSURAI_API_KEY`。`INSURAI_AGENT_URL` 可省略，預設使用正式端點。

> Privacy notice: insurance planning and lookup inputs may contain sensitive personal or financial information. Required request fields are transmitted to the configured `INSURAI_AGENT_URL`. Before the first API call in a conversation, inform users and obtain consent to continue. Submit only the minimum necessary data, and avoid unnecessary identifiers such as national ID numbers, contact details, full policy documents, payment data, or medical records.

> TLS policy: `INSURAI_AGENT_URL` must be an HTTPS URL. Certificate verification is always required and cannot be disabled through this helper. The helper uses Python `requests` default TLS verification for all API traffic.

> ⚠️ **正式機部署前確認**：執行 `python3 -c "import requests"` 確認 trusted runtime 已預先提供 `requests` 庫。

---

## 完整 CLI 用法

```bash
# 職業查詢
python3 scripts/insurai_api.py occupations_search --keyword "護理師"

# 保險規劃判讀
python3 scripts/insurai_api.py plan_interpret --scenario "62歲女性，桃園人，目前有南山AI意外險+實支實付+意外醫療，年繳6000元"

# 商品推薦
python3 scripts/insurai_api.py recommend \
  --protection "意外險" "實支實付" "意外醫療" \
  --age 62 --gender female --recommend-type main-rider

# 商品檢索（預設只查可售商品；使用 --no-available-product 包含停售商品）
python3 scripts/insurai_api.py search --q "糖尿病" --page-size 5
python3 scripts/insurai_api.py search --q "意外" --no-available-product --page-size 10

# 商品 Metadata（單筆）
python3 scripts/insurai_api.py metadata --product-code "216321MZ2B24023A11Z10000008"

# 批量 Metadata（平行，結果順序與輸入順序完全一致）
python3 scripts/insurai_api.py batch-metadata \
  --codes "105151424501010003" "205211MZ1A00821A11Z10000006" \
  "202131MZ1A98A22A11Z10000000" "108151424500120005" \
  --quiet

# 商品條款文件
python3 scripts/insurai_api.py document \
  --product-code "216321MZ2B24023A11Z10000008" --campaign-type contract

# PDF 下載連結
python3 scripts/insurai_api.py pdf_link \
  --product-code "216321MZ2B24023A11Z10000008" --campaign-type contract
```

---

## 全域參數

| 參數          | 說明                        |
| ------------- | --------------------------- |
| `--minify`    | 輸出壓縮 JSON（無縮排）     |
| `--quiet`     | 抑制 stderr 進度訊息        |
| `--timeout N` | 覆寫本次呼叫的 timeout 秒數 |

---

## 已發現並修復的 Bug（供未來除錯參考）

### 1. Retry 多計一次

- 檔案：`scripts/insurai_api.py`
- 問題：`while attempt <= max_retries` 會執行 4 次而非 3 次
- 正確：`while attempt < max_retries`
- 觸發情境：5xx 或連線錯誤時，預期重試 3 次但實際重試 4 次，浪費一次 API call

### 2. Retry-After 非數字 crash

- 問題：`int(response.headers.get("Retry-After", 5))` 若 header 值非數字（如 `"please wait"`）會拋 `ValueError`
- 修復：包 `try/except ValueError`，失敗時預設 5 秒

### 3. batch_metadata 回傳順序隨機

- 問題：用 `as_completed` 但直接 append，結果順序每次不同
- 修復：預分配 `results: List[Dict] = [{} for _ in range(total)]`，以 index 寫入確保順序與輸入一致，避免多個元素共用同一個 dict 參照

### 4. 空 product-code 未驗證

- 問題：`metadata --product-code ""` 仍送出 API request
- 修復：CLI 在 `metadata`/`document`/`pdf_link` action 前檢查，空白提前回傳錯誤 JSON

### 5. response.json() 無 HTTP status 把關

- 問題：4xx 錯誤時直接回傳 JSON，caller 無法區分成功與錯誤
- 修復：`_check_response()` 統一把關，4xx/5xx 拋出 `RuntimeError`

### 6. requests 庫未安裝時錯誤訊息不清

- 問題：正式機若 `python3` 指向沒有 requests 的 Python，錯誤為 `No module named 'requests'`
- 修復：腳本延遲載入 `requests`，失敗時清楚說明 trusted runtime 需預先提供 `requests`

### 7. batch_metadata 全錯時仍回傳 200（2025-06-15）

- 問題：8個商品代碼全部 API失敗 → 回傳 `[{error}, {error}, ...]` → caller 以為成功
- 修復：新增 all-failure 檢查，全部失敗時拋出 `RuntimeError`

### 8. ThreadPoolExecutor max_workers 寫死（2025-06-15）

- 問題：`max_workers=8`，少量代碼也開 8 執行緒
- 修復：改為 `min(8, total)` 動態決定

### 9. --available-product 滲透到 recommend（2026-06-15）

- 問題：`recommend` 的 `availableProduct` 固定為 `true`，不接受 CLI 控制，但全域 CLI 引數會被接收
- 修復：search 預設送出 `availableProduct=true`，可用 `--no-available-product` 關閉；recommend 明確指定時發出 WARNING；其他不適用 action 發出錯誤

### 10. --quiet 無法抑制 retry 警告（2025-06-15）

- 問題：`--quiet` 只抑制 progress，429/5xx retry 訊息仍輸出
- 修復：模組層級 `_QUIET` 旗標，retry/logic helpers 皆檢查

### 11. 參數缺少驗證（2025-06-15）

- `--recommend-type`：未驗證是否為 `main`/`main-rider`
- `--gender`：未驗證是否為 `male`/`female`
- `--campaign-type`：未驗證是否為 `contract`/`premium`
- `--age`：未阻止負數或 0
- `--occupation-level`：未阻止範圍外值（1-6）
- `--page-size`：未阻止負數或 0，過大（>100）僅 WARNING
- `--codes`：未設上限（500 上限）
- 修復：統一在 `_main()` 前置驗證區塊攔截

### 12. CLI 引數名稱易混淆：--insurers 而非 --insurer / --insurer-codes（2025-06-15）

- 問題：使用者常誤用 `--insurer` 或 `--insurer-codes`，但 argparse 定義的長參數名稱是 `--insurers`
- 觸發：`recommend --insurer-codes "204" "209"` → `error: unrecognized arguments: --insurer-codes`
- 正確：`recommend --insurers "204" "209"`（nargs="+" 支援多值）
- 實作：`ArgumentParser(allow_abbrev=False)`，避免 `--insurer` 被 argparse 自動視為 `--insurers` 的縮寫
- 補充：`--available-product` / `--no-available-product` 對 `recommend` 會被忽略並發 WARNING，僅對 `search` 有效

### 13. 重試耗盡時遺失 HTTP 狀態碼（2026-06-15）

- 問題：`_request_with_retry` 的 `last_exc` 只在連線錯誤的 `except` 區被賦值；持續 5xx / 429 走 `if`+`continue`，耗盡後 `last_exc` 仍為 `None`，丟出通用「Request failed after N retries」，502/503/429 真實狀態全失。連帶讓 `_check_response` 的 5xx 分支變死碼
- 修復：迴圈追蹤 `last_retryable_response`（最後一個 429/5xx response），耗盡後優先回傳它，交由 `_check_response` 丟出帶狀態碼的 `RuntimeError`（如 `Server error 503: …`）

### 14. 最後一次重試後仍空等一輪 backoff（2026-06-15）

- 問題：5xx / 429 / 連線錯誤分支皆「先 `sleep` 再 `continue`」，最後一次嘗試 sleep 完才發現不會再重試，純浪費（5xx 白等 `2**3=8` 秒）
- 修復：改用 `for attempt in range(1, max_retries+1)`，`is_last_attempt` 為真時直接 `break`，不再 sleep。持續 5xx 的等待由 `[2,4,8]=14s` 降為 `[2,4]=6s`，請求次數仍為 3

### 15. batch_metadata 健壯性（2026-06-15）

- 問題：`[{}] * total` 讓 N 個元素共用同一個 dict 參照（目前因整格重新指派而剛好安全，但屬 footgun）；`batch_metadata([])` 會 `ThreadPoolExecutor(max_workers=0)` 拋 `ValueError`，且空 `all()` 為 `True` 導致 `error_msgs[0]` `IndexError`
- 修復：改 `[{} for _ in range(total)]` 配置獨立 dict；函式開頭加 `if total == 0: return []`

### 16. 2xx HTML fallback 診斷（2026-06-25）

- 問題：若 `INSURAI_AGENT_URL` 指到前端站台或 reverse proxy fallback，API path 可能回 `HTTP 200` + `text/html`，原本會在 `response.json()` 產生難判讀的 JSON parse error
- 修復：2xx 回應先檢查 `Content-Type` 是否為 JSON；若不是，明確提示檢查 `INSURAI_AGENT_URL` 與 reverse proxy routing

---

## 批量查詢最佳實踐

當需要查多個商品代碼的 metadata 時，永遠用 `batch-metadata` 而非串行迴圈：

```bash
# ✅ 正確：平行，結果順序與輸入順序一致
python3 scripts/insurai_api.py batch-metadata \
  --codes "CODE1" "CODE2" "CODE3" "CODE4" "CODE5" "CODE6" "CODE7" "CODE8" \
  --quiet

# ❌ 錯誤：串行，慢，且順序隨機
for code in "CODE1" "CODE2" "CODE3"; do
  python3 scripts/insurai_api.py metadata --product-code "$code"
done
```

---

## Timeout 分級參考

| 操作                 | 預設 timeout |
| -------------------- | ------------ |
| `occupations_search` | 30s          |
| `plan_interpret`     | 60s          |
| `recommend`          | 60s          |
| `search`             | 60s          |
| `metadata`           | 15s          |
| `document`           | 120s         |
| `pdf_link`           | 120s         |

可用 `--timeout N` 覆寫。

---

## 癌症險查詢實務經驗

### 常見使用者描述陷阱：84歲滿期

使用者常說「84歲若未使用可領回」，但 InsurAI 系統中**沒有任何防癌險的滿期年齡是 84 歲**。實務上最接近的選項：

| 商品                               | 滿期年齡  | 代碼                          | 備註               |
| ---------------------------------- | --------- | ----------------------------- | ------------------ |
| 全球人壽臻心85防癌定期健康保險附約 | 85歲      | `264321RZ1AXCE22A11Z10000002` | 附約，需搭配主約   |
| 國泰人壽豪康愛防癌定期保險         | 90歲      | `204321MZ9BMFA22A11E10000000` | 主約               |
| 台新人壽愛寶倍終身壽險             | 100歲祝壽 | `255191MA2B23723A11Z10000001` | 終身壽險含癌症保障 |

**處理方式**：當使用者提及 84 歲，應主動說明這個數字與系統商品不完全吻合，引導使用者確認「滿期年齡」或「罹癌一次領的年齡」。

### recommend 保障名稱選用原則（重要）

**發現（2025-06-15）**：API 對保障名稱的匹配邏輯並非簡單子字串比對，某些廣義名稱組合會回傳 0 筆，更具體的名稱反而有結果。

**實測對照：**

| protection 名稱組合                    | recommend 回傳筆數 |
| -------------------------------------- | ------------------ |
| `"實支實付醫療保障"`                   | 8 筆 ✅            |
| `"意外保障" + "失能保障"`              | 0 筆（空）         |
| `"壽險"`                               | 0 筆（空）         |
| `"意外險" "實支實付" "意外醫療"`       | 有結果（文件範例） |
| `"癌症險" "癌症一次領" "癌症身故給付"` | 有結果（文件範例） |

**原則：**

- 優先使用**具體、保障范围明确**的名稱（如「實支實付醫療保障」、「癌症一次領」）
- 避免僅用**抽象分類**（如「意外保障」、「失能保障」、「壽險」）單獨查詢
- 若某組名稱回傳 0 筆，嘗試換成更具體的同義詞
- 一次丟 2-4 個具體關鍵字比一次丟 1 個廣義關鍵字更穩定

**範例（外送員情境）：**

```bash
# ✅ 穩定：具體的實支實付 + 明確的手術類型
python3 scripts/insurai_api.py recommend \
  --protection "實支實付醫療保障" "手術費用保障" \
  --age 35 --gender male --occupation-level 3 --recommend-type main-rider

# ⚠️ 不穩定：廣義抽象類別
python3 scripts/insurai_api.py recommend \
  --protection "意外保障" "失能保障" \
  --age 35 --gender male --occupation-level 3 --recommend-type main-rider
```

### 癌症險查詢工作流

```
recommend (保障關鍵字)
  → batch-metadata (一次查多筆代碼)
    → document (確認有興趣的商品再看條款)
```

**範例**（查詢癌症險）：

```bash
# Step 1: 取得候選商品代碼
python3 scripts/insurai_api.py recommend \
  --protection "癌症險" "癌症一次領" "癌症身故給付" \
  --age 30 --gender male --insurers 204 --recommend-type main-rider

# Step 2: 一次查多筆 metadata（結果順序與輸入順序一致）
python3 scripts/insurai_api.py batch-metadata \
  --codes "204321MZ9BMFA22A11E10000000" "204321MZ9BFMB22A11E10000000" \
  --quiet

# Step 3: 確認有興趣的商品後，查閱條款全文
python3 scripts/insurai_api.py document \
  --product-code "204321MZ9BMFA22A11E10000000" --campaign-type contract
```

---

## Python 版本相容性

- 最低需求：**Python 3.9+**（CPython）
- 所有 `typing` 功能（`List`, `Dict`, `Tuple`, `Optional`）在 3.9 即齊備
- `from __future__ import annotations` 已移除，不依賴任何 3.10+ 語法
- 外部依賴：**`requests` 庫**（非標準庫，必須已安裝）
  `INSURAI_AGENT_URL` 必須使用 HTTPS；TLS 憑證驗證一律啟用，且不提供停用 TLS 驗證的環境變數。

helper 使用 Python `requests` 預設 TLS 驗證設定，避免帶有 `X-API-KEY` 與保險資料的請求暴露於中間人攔截或竄改風險。
