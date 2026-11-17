# InsurAI REST API 端點契約

> 適用於 `SkillInsurPlanResource`、`SkillOccupationResource`、`SkillInsurContractResource` 的 API 契約。

本文件**只定義 REST 端點契約**：HTTP method / path / 請求欄位（型別）/ 回傳 JSON 結構 / 錯誤碼。

以下內容以 [insurai-rules.md](insurai-rules.md) 為**單一真實來源**，本文件不重複，請逕參該文件：

- 適用地區、直接拒絕規則
- 保險公司代碼表（37 家）
- 值域定義：`contractType`、`gender`、`recommendType`、`campaignOverviewType`
- CLI 使用方式、各功能使用時機與回應守則、限制

> 所有呼叫一律透過 [scripts/insurai_api.py](../scripts/insurai_api.py)，**嚴禁 curl**。本文件相對路徑均以 skill 根目錄為基準。

---

## 系統配置

- Base URL：`$INSURAI_AGENT_URL`（預設 `https://insurai.com.tw/insurai/agent`；必須為 HTTPS）
- 路徑前綴：`/api/skill/v1`
- 認證：所有請求帶 Header `X-API-KEY: $INSURAI_API_KEY`
- TLS 驗證：一律啟用，使用 Python `requests` 預設安全設定；`INSURAI_AGENT_URL` 必須使用 HTTPS，且不提供停用 TLS 驗證的環境變數

若尚未取得 `INSURAI_API_KEY`，請先至 https://insurai.com.tw 註冊會員，登入後申請 `INSURAI-API-KEY`，再設定 `INSURAI_API_KEY`。`INSURAI_AGENT_URL` 可省略，預設使用正式端點。

> Privacy notice: insurance planning and lookup inputs may contain sensitive personal or financial information. Required request fields are transmitted to the configured `INSURAI_AGENT_URL`. Before the first API call in a conversation, inform users and obtain consent to continue. Submit only the minimum necessary data, and avoid unnecessary identifiers such as national ID numbers, contact details, full policy documents, payment data, or medical records.
> TLS policy: `INSURAI_AGENT_URL` must be an HTTPS URL. Certificate verification is always required and cannot be disabled through this helper. The helper uses Python `requests` default TLS verification for all API traffic.

```bash
export INSURAI_API_KEY=your_api_key_here
# Optional: override the production endpoint.
export INSURAI_AGENT_URL=https://insurai.com.tw/insurai/agent
```

範例中 `$BASE` = `${INSURAI_AGENT_URL:-https://insurai.com.tw/insurai/agent}`；helper 會從 `INSURAI_API_KEY` 讀取 API key 並放入 `X-API-KEY` header。

---

## 端點總覽

| #   | 功能                 | Method | Path                                                   | CLI action           |
| --- | -------------------- | ------ | ------------------------------------------------------ | -------------------- |
| 1   | 保險規劃判讀         | `POST` | `/api/skill/v1/insur-plan/interpret`                   | `plan_interpret`     |
| 2   | 職業分類查詢         | `GET`  | `/api/skill/v1/occupations/search`                     | `occupations_search` |
| 3   | 商品推薦             | `POST` | `/api/skill/v1/insur-contracts/recommend`              | `recommend`          |
| 4   | 商品檢索             | `POST` | `/api/skill/v1/insur-contracts/search`                 | `search`             |
| 5   | 商品 Metadata        | `GET`  | `/api/skill/v1/insur-contracts/{productCode}/metadata` | `metadata`           |
| 6   | 商品文件（Markdown） | `GET`  | `/api/skill/v1/insur-contracts/{productCode}/document` | `document`           |
| 7   | PDF 下載連結         | `GET`  | `/api/skill/v1/insur-contracts/{productCode}/pdf-link` | `pdf_link`           |

---

## 1. 保險規劃判讀

`POST /api/skill/v1/insur-plan/interpret`

**請求 body**

| 欄位       | 型別   | 必要 | 說明             |
| ---------- | ------ | ---- | ---------------- |
| `scenario` | string | ✔   | 完整保險需求描述 |

**回傳**

```json
{
  "success": true,
  "code": "OK",
  "message": "判讀完成",
  "data": {
    "household": { "summary": "", "mainHouseholdConcerns": [], "recommendationReason": "" },
    "insuredPersons": [],
    "overallPendingData": []
  },
  "error": null
}
```

`success = false` 常見 `code`：

- `STAGE1_INSUFFICIENT_CONTEXT`：輸入不足以辨識人生階段
- `INSUFFICIENT_CREDITS`：點數不足
- `INTERNAL_ERROR`：系統錯誤

---

## 2. 職業分類查詢

`GET /api/skill/v1/occupations/search`

**查詢參數**

| 參數 | 型別   | 必要 | 說明                      |
| ---- | ------ | ---- | ------------------------- |
| `q`  | string | ✔   | 職業關鍵字（如 `護理師`） |

**回傳**（陣列）

```json
[
  {
    "primaryCode": "10",
    "primaryName": "衛生保健",
    "secondaryCode": "1001",
    "secondaryName": "醫院",
    "occupationCode": "1001007",
    "occupationLevel": "1",
    "occupationName": "一般護理人員(護士、護理師)",
    "widelyUsed": true
  }
]
```

| 欄位                              | 說明                                                        |
| --------------------------------- | ----------------------------------------------------------- |
| `primaryCode` / `primaryName`     | 大分類代碼 / 名稱                                           |
| `secondaryCode` / `secondaryName` | 中分類代碼 / 名稱                                           |
| `occupationCode`                  | 職業代碼                                                    |
| `occupationName`                  | 小分類／職業名稱（工作性質）                                |
| `occupationLevel`                 | 職業等級（`1` 最低風險 ～ `6` 最高風險；`0`/`null` 為未知） |
| `widelyUsed`                      | 是否常用職業項目                                            |

---

## 3. 商品推薦

`POST /api/skill/v1/insur-contracts/recommend`

**請求 body**

| 欄位              | 型別     | 必要 | 說明                             |
| ----------------- | -------- | ---- | -------------------------------- |
| `protectionNames` | string[] | ✔   | 保障名稱清單（自然語言，可多值） |
| `age`             | int      |      | 被保險人年齡                     |
| `gender`          | string   |      | `male` / `female`                |
| `insurers`        | string[] |      | 保險公司名稱或代碼清單（可多值） |
| `occupationLevel` | int      |      | 職類等級 `1-6`                   |
| `recommendType`   | string   |      | `main`（預設）/ `main-rider`     |

> `availableProduct` 由 server 端固定為 `true`，不受請求控制。

**回傳**

```json
{
  "productCodes": [
    {
      "main": {
        "code": "202121MZ2A82023A11Z10000003",
        "name": "台灣人壽新意享人生終身保險",
        "insurer": "台灣人壽",
        "mainBenefits": [
          { "item": "滿期保險金", "description": "…", "note": "" },
          { "item": "意外失能保險金", "description": "…", "note": "" }
        ]
      },
      "supplementaryRiders": []
    }
  ]
}
```

| 欄位                  | 說明                                                                                                                  |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `productCodes`        | 推薦結果清單，每筆為一組主約與可搭配附約（**回傳 key 為 `productCodes`，非 `combinations`**）                         |
| `main`                | 主約商品（`code` / `name` / `insurer` / `mainBenefits`）                                                              |
| `supplementaryRiders` | 推薦組合中與 `main` 搭配以補足保障需求的附約清單，結構同 `main`；**無附約時為 `[]`**                                  |
| `mainBenefits`        | 給付項目明細（`item` + `description` + `note`），**判斷商品保障屬性的唯一依據**，不可依 `contractType` 或商品名稱判斷 |

---

## 4. 商品檢索

`POST /api/skill/v1/insur-contracts/search`

**請求 body**

| 欄位               | 型別     | 必要 | 說明                             |
| ------------------ | -------- | ---- | -------------------------------- |
| `q`                | string   |      | 全文查詢字串                     |
| `productName`      | string   |      | 商品名稱關鍵字                   |
| `protectionNames`  | string[] |      | 保障名稱清單（可多值）           |
| `insurers`         | string[] |      | 保險公司名稱或代碼清單（可多值） |
| `availableProduct` | bool     |      | 是否只查可售商品（預設 `true`）  |
| `occupationLevel`  | int      |      | 職類等級 `1-6`                   |
| `gender`           | string   |      | `male` / `female`                |
| `age`              | int      |      | 年齡                             |
| `pageSize`         | int      |      | 回傳筆數上限（預設 `10`）        |

> 建議至少提供 `q` / `productName` / `protectionNames` 其中一個。

**回傳**（陣列）

```json
[{ "productCode": "A123456789", "snippet": "…復健費用給付，被保險人因意外或疾病接受復健治療…" }]
```

| 欄位          | 說明                   |
| ------------- | ---------------------- |
| `productCode` | 商品代碼               |
| `snippet`     | 命中關鍵字的前後文摘要 |

---

## 5. 商品 Metadata

`GET /api/skill/v1/insur-contracts/{productCode}/metadata`

**路徑參數**

| 參數          | 型別   | 必要 | 說明         |
| ------------- | ------ | ---- | ------------ |
| `productCode` | string | ✔   | 保險商品代碼 |

**回傳**

```json
{
  "productCode": "202121MZ1A81A23A11Z10000000",
  "metadata": {
    "version": "1.x.x",
    "insuranceCompany": "…",
    "productName": "…",
    "contractType": "無資料",
    "coverage": {
      "mainBenefits": [],
      "exclusions": []
    },
    "premiumOptions": [],
    "policyTerms": [],
    "officialRiders": []
  }
}
```

| 欄位          | 說明                                                                                     |
| ------------- | ---------------------------------------------------------------------------------------- |
| `productCode` | 商品代碼                                                                                 |
| `metadata`    | 商品 metadata（**JSON 物件**；主約存在 `riderProductCodes` 時可能包含 `officialRiders`） |

---

## 6. 商品文件（Markdown）

`GET /api/skill/v1/insur-contracts/{productCode}/document`

**參數**

| 參數                   | 位置  | 型別   | 必要 | 說明                                    |
| ---------------------- | ----- | ------ | ---- | --------------------------------------- |
| `productCode`          | path  | string | ✔   | 保險商品代碼                            |
| `campaignOverviewType` | query | string | ✔   | `contract`（條款）/ `premium`（費率表） |

**回傳**

```json
{
  "productCode": "202121MZ1A81A23A11Z10XXXXX0",
  "document": "# XX終身醫療保險條款\n\n## 第一條 保險範圍\n…"
}
```

| 欄位          | 說明                      |
| ------------- | ------------------------- |
| `productCode` | 商品代碼                  |
| `document`    | 文件內容（Markdown 全文） |

---

## 7. PDF 下載連結

`GET /api/skill/v1/insur-contracts/{productCode}/pdf-link`

**參數**

| 參數                   | 位置  | 型別   | 必要 | 說明                   |
| ---------------------- | ----- | ------ | ---- | ---------------------- |
| `productCode`          | path  | string | ✔   | 保險商品代碼           |
| `campaignOverviewType` | query | string | ✔   | `contract` / `premium` |

**回傳**

```json
{
  "productCode": "202121MZ1A81A23A11Z10000000",
  "type": "contract",
  "pdfUrl": "https://example.com/documents/%E5%95%86%E5%93%81%E5%90%8D%E7%A8%B1.pdf?tiiProductCode=xxxxxx"
}
```

| 欄位          | 說明                    |
| ------------- | ----------------------- |
| `productCode` | 商品代碼                |
| `type`        | `contract` 或 `premium` |
| `pdfUrl`      | PDF 下載連結            |

---

## 錯誤處理

### HTTP / 連線層

| 狀態                   | 處理                                                                              |
| ---------------------- | --------------------------------------------------------------------------------- |
| `400 Bad Request`      | 請求參數有誤，指出缺少 / 格式錯誤 / 不合法欄位                                    |
| `401 Unauthorized`     | API Key 無效或未設定，提示確認 `INSURAI_API_KEY`                                  |
| `402 Payment Required` | 點數不足（core 回報 `INSUFFICIENT_CREDITS`）。適用 occupations 與 insur-contracts |
| `404 Not Found`        | 找不到指定商品、metadata、文件或 PDF 連結（需 core 明確回 404 才出現）            |
| `501 Not Implemented`  | 功能暫停提供，明確告知使用者目前無法使用                                          |
| `502 Bad Gateway`      | core 5xx / 回應格式錯誤 / 連線異常 / 空回應，建議稍後再試                         |
| 其他 `5xx`             | 系統錯誤，建議稍後再試或聯絡管理員                                                |
| 連線失敗 / 逾時        | 告知無法連線至 `$BASE`，請確認網路或服務狀態                                      |

> 非公開測試環境可能有不同的 API key 驗證或錯誤碼轉換設定；公開使用時以實際 API 回應狀態碼為準。

### 點數不足對應（依端點而異）

- **occupations / insur-contracts**（裸資料端點）：點數不足 → HTTP `402 Payment Required`。
- **insur-plan/interpret**（統一 envelope）：點數不足 → HTTP `200` + `success=false` + `code=INSUFFICIENT_CREDITS` + `error.type=system`（in-body）。

### 業務層

- `/insur-plan/interpret` 回傳 `success = false`：僅告知 `error.reason` 或 `code` 對應訊息，停止處理
- `recommendType` 非 `main` / `main-rider`：視為參數錯誤
- `campaignOverviewType` 非 `contract` / `premium`：視為參數錯誤
