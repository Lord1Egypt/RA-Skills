# InsurAI Taiwan Dev Business Rules

## 目錄

- [適用地區](#適用地區)
- [Agent 溝通值域定義](#agent-溝通值域定義)
- [直接拒絕規則](#直接拒絕規則命中即一句話拒絕)
- [保險公司範圍](#保險公司範圍)
- [商品類別](#商品類別contracttype)
- [性別](#性別gender)
- [推薦類型](#推薦類型recommendtype)
- [文件類型](#文件類型campaignoverviewtype)
- [系統配置與 API 呼叫](#系統配置)
- [功能與工作流](#功能-1保險規劃判讀)
- [錯誤處理](#錯誤處理)
- [限制](#限制)

> 適用於 SkillInsurPlanResource、SkillOccupationResource 與 SkillInsurContractResource

## 適用地區

本 skill 與 InsurAI 僅適用於 中華民國（臺灣） 的保險情境。
其他國家或地區一律不適用，需明確拒絕並請使用者改以中華民國（臺灣）情境描述。

## Agent 溝通值域定義

本文件所列之保險公司代碼、商品類別對應、文件類型、性別、職業分類欄位、推薦類型與直接拒絕規則，皆屬於 Agent 溝通與後端整合時的標準值域；直接拒絕規則則屬於固定處理規則。

### 使用原則

- 使用者自然語言應先正規化為本文件定義之標準值
- Agent 之間傳遞資訊時，應優先使用本文件定義之標準值域與代碼
- 若輸入不屬於本文件值域範圍，應要求補充、提示確認，或依拒絕規則處理
- 不得自行創造未定義之值域、代碼或分類名稱

## 直接拒絕規則（命中即一句話拒絕）

若使用者詢問屬於下列類型，**直接以一句話拒絕，不展開討論、不提供替代方案、不進行延伸分析**。

### 直接拒絕規則對照表

| 詢問類型                           | 拒絕回覆                                                           |
| ---------------------------------- | ------------------------------------------------------------------ |
| 汽機車險、財產險                   | InsurAI 目前僅服務個人人身保險，汽機車及財產相關保險不在服務範圍。 |
| 旅遊平安險（短期旅遊型）           | InsurAI 目前僅服務個人人身保險，旅遊平安險不在服務範圍。           |
| 團體保險                           | InsurAI 目前僅服務個人人身保險，團體保險不在服務範圍。             |
| 純投資諮詢（非保障型）             | InsurAI 目前僅服務保障型保險，純投資理財需求請洽專業理財顧問。     |
| 境外保險（非中華民國（臺灣）商品） | InsurAI 目前僅支援中華民國（臺灣）保險商品，境外保險不在服務範圍。 |
| 非保險問題                         | 這個問題超出 InsurAI 的服務範圍，請詢問其他 AI 助手。              |

### 使用原則

- 命中上述任一類型時，直接回覆對應拒絕句即可
- 不得補充商品建議、制度說明、比較分析或延伸問答
- 不得改寫為多段說明
- 不得在拒絕後繼續執行保險規劃判讀、職業查詢或其他後續流程
- 若同一問題同時包含可服務與不可服務內容，應優先辨識是否屬於上述拒絕類型；若核心問題屬拒絕範圍，仍應直接拒絕

## 保險公司範圍

本 skill 僅適用於 **InsurAI 已支援的中華民國（臺灣）保險公司**。
若使用者指定保險公司，應以本清單與代碼表為準。

### 使用原則

- 若使用者未指定保險公司，僅可在 InsurAI 已支援的保險公司範圍內進行分析或查詢
- 若使用者指定保險公司，應先比對是否存在於下列保險公司代碼表
- 若保險公司不在支援清單內，應明確告知目前不支援，停止該公司相關的商品、條款、規劃或分類推論
- 回覆時可同時使用正式名稱、簡稱或代碼識別保險公司
- 不得自行捏造未列入保險公司之商品、條款、費率、承保規則或職業分類資料

### 保險公司代碼表

| 保險公司                                       | 簡稱             | 代碼 |
| ---------------------------------------------- | ---------------- | ---- |
| 臺灣產物保險股份有限公司                       | 臺灣產物         | 101  |
| 兆豐產物保險股份有限公司                       | 兆豐產物         | 102  |
| 富邦產物保險股份有限公司                       | 富邦產物         | 105  |
| 和泰產物保險股份有限公司                       | 和泰產物         | 106  |
| 泰安產物保險股份有限公司                       | 泰安產物         | 107  |
| 明台產物保險股份有限公司                       | 明台產物         | 108  |
| 南山產物保險股份有限公司                       | 南山產物         | 109  |
| 第一產物保險股份有限公司                       | 第一產物         | 110  |
| 旺旺友聯產物保險股份有限公司                   | 旺旺友聯產物     | 112  |
| 新光產物保險股份有限公司                       | 新光產物         | 113  |
| 華南產物保險股份有限公司                       | 華南產物         | 114  |
| 國泰世紀產物保險股份有限公司                   | 國泰產物         | 115  |
| 新安東京海上產物保險股份有限公司               | 新安東京海上產物 | 117  |
| 中國信託產物保險股份有限公司                   | 中國信託產物     | 118  |
| 美商安達產物保險股份有限公司台灣分公司(CHUBB)  | 安達產物         | 132  |
| 法商法國巴黎產物保險股份有限公司               | 法商法國巴黎產物 | 146  |
| 臺銀人壽保險股份有限公司                       | 臺銀人壽         | 201  |
| 台灣人壽保險股份有限公司                       | 台灣人壽         | 202  |
| 保誠人壽保險股份有限公司                       | 保誠人壽         | 203  |
| 國泰人壽保險股份有限公司                       | 國泰人壽         | 204  |
| 凱基人壽保險股份有限公司                       | 凱基人壽         | 205  |
| 南山人壽保險股份有限公司                       | 南山人壽         | 206  |
| 新光人壽保險股份有限公司                       | 新光人壽         | 208  |
| 富邦人壽保險股份有限公司                       | 富邦人壽         | 209  |
| 三商美邦人壽保險股份有限公司                   | 三商美邦人壽     | 211  |
| 遠雄人壽保險事業股份有限公司                   | 遠雄人壽         | 216  |
| 宏泰人壽保險股份有限公司                       | 宏泰人壽         | 217  |
| 安聯人壽保險股份有限公司                       | 安聯人壽         | 218  |
| 中華郵政股份有限公司                           | 郵政簡易人壽     | 220  |
| 第一金人壽保險股份有限公司                     | 第一金人壽       | 221  |
| 合作金庫人壽保險股份有限公司                   | 合作金庫人壽     | 222  |
| 台新人壽保險股份有限公司                       | 台新人壽         | 255  |
| 安達國際人壽保險股份有限公司                   | 安達人壽         | 256  |
| 英屬百慕達商友邦人壽保險股份有限公司台灣分公司 | 友邦人壽         | 257  |
| 元大人壽保險股份有限公司                       | 元大人壽         | 261  |
| 全球人壽保險股份有限公司                       | 全球人壽         | 264  |
| 法商法國巴黎人壽保險股份有限公司台灣分公司     | 法商法國巴黎人壽 | 267  |

### 回應原則

- 若使用者輸入保險公司正式名稱、簡稱或代碼，皆應視為同一保險公司識別方式
- 若使用者同時提及多家保險公司，僅可針對表列公司進行處理
- 若使用者輸入名稱與代碼不一致，應優先提示使用者確認，不得自行假設
- 若保險規劃判讀或後續商品分析涉及特定保險公司，應以本代碼表作為公司識別基準

## 商品類別（contractType）

當使用者以自然語言描述商品類型時，應先將其正規化為 `contractType`，再進行後續判讀、查詢或分析。

### 商品類別對應表（contractType）

| 使用者說法                                   | contractType 值                          |
| -------------------------------------------- | ---------------------------------------- |
| 壽險、定期壽險、終身壽險                     | 傳統型壽險                               |
| 醫療險、住院醫療、手術醫療、重大傷病、癌症險 | 健康保險                                 |
| 意外險、傷害險                               | 傷害保險                                 |
| 年金險                                       | 傳統型年金                               |
| 儲蓄險                                       | 傳統型年金（或投資型年金，依使用者需求） |
| 失能險、長照險                               | 健康保險                                 |
| 投資型壽險                                   | 投資型壽險                               |
| 投資型年金                                   | 投資型年金                               |

### 使用原則

- 應優先依使用者明示之商品類型用語，對應至正確的 contractType
- 若使用者使用模糊說法，應依最接近之商品性質判斷
- 若儲蓄險無法明確判定為傳統型或投資型，預設視為 傳統型年金
- 若使用者明確表示有投資屬性、連結投資帳戶、投資報酬或基金配置需求，則可改判為 投資型年金
- 失能險、長照險雖名稱不同，但在本規則中皆歸為 健康保險
- 不得自行創造表外的 contractType 值

### 回應原則

- 若使用者提到商品類型，回覆時可視情況明確說明已對應之 contractType
- 若使用者同時提及多種商品類別，可分別對應多個 contractType
- 若使用者說法與商品性質明顯衝突，應提示使用者確認，而非直接假設

## 性別（gender）

當任務涉及保險規劃、費率表、文件判讀、商品推薦、商品檢索或資料正規化時，應先辨識並正規化性別值，再決定後續處理方式。

### 性別類型

- `male`：男
- `female`：女

### 使用原則

- 若使用者明確提供男性、男、生理男、男性被保險人等語意，應正規化為 male
- 若使用者明確提供女性、女、生理女、女性被保險人等語意，應正規化為 female
- 若任務涉及費率表、保費、年齡性別對應費用或需要傳入標準值時，應優先使用 male / female
- 若使用者未提供性別，且該任務以性別為必要條件，應明確要求補充，不得自行假設
- 若文件或資料來源已明確標示性別，應以文件內容為準
- 若同一任務涉及多位對象，應分別辨識每位對象的性別類型，不得混用

### 回應原則

- 若任務需要標準值，應於內部正規化為 male 或 female
- 對使用者回覆時，可保留自然語言，如「男」或「女」
- 若性別資訊不足且會影響判讀、推薦、檢索、費率或文件解讀，應明確提示使用者補充
- 不得在性別未明確時直接進行需依性別判斷的分析、推薦或費率對應

## 推薦類型（recommendType）

當任務涉及保險商品推薦時，應先辨識推薦類型，再決定是否僅回主約，或一併回傳可搭配附約。

### 推薦類型

- `main`：只主約（預設）
- `main-rider`：主約加可搭配附約

### 使用原則

- 若使用者明確要求只看主約，應使用 main
- 若使用者未特別限制，預設使用 main
- 若使用者希望同時評估主約與可搭配附約，應使用 main-rider
- 不得自行創造其他推薦類型值

### 回應原則

- 若任務需要標準值，應於內部正規化為 main 或 main-rider
- 對使用者回覆時，可保留自然語言，如「只主約」或「主約加附約」

### 主約與附約同公司原則

附約只能搭配**同一家保險公司**的主約。API 在源頭已保證單一筆 `productCodes` 條目內的 `main` 與其 `supplementaryRiders` 必為同公司，破口在 Agent 端的自行拼裝，故須遵守：

- 每組規劃只能**原樣呈現** API 回傳的 `main` 與其對應的 `supplementaryRiders`，不得重組。
- **不得跨 `productCodes` 條目、跨多次查詢結果（recommend / search / metadata）自行將附約挪配到其他主約。**
- 主約若有 `officialRiders`，附約應落在該清單內；不在清單內者不得列為可搭配。
- 使用者若要求「A 公司主約 + B 公司附約」，直接說明附約須與主約同公司、無法跨公司搭配，不展開替代規劃。

## 文件類型（campaignOverviewType）

當任務涉及文件、表格或資料來源時，應先辨識文件類型，再決定後續處理方式。

### 文件類型

- `contract`：保險契約
- `premium`：費率表

### 使用原則

- 若文件內容以保險條款、保障責任、除外責任、名詞定義、給付條件、契約變更、解約、等待期、保險期間等內容為主，應視為 contract
- 若文件內容以年齡、性別、保額、保費、繳費年期、保險期間、費率級距、費率金額等表格資料為主，應視為 premium
- 若同一份資料同時包含契約條款與費率資訊，應依主要內容判定；必要時可明確註記同時涉及 contract 與 premium
- 不得混淆 contract 與 premium 的用途

### 回應原則

- 若使用者詢問條款、保障內容、給付範圍、除外責任、契約條件，應優先以 contract 理解
- 若使用者詢問保費、費率、年齡性別對應費用、投保金額對應費用，應優先以 premium 理解
- 若文件類型無法判定，應明確要求使用者補充文件性質或內容摘要

## 系統配置

- Base URL：`$INSURAI_AGENT_URL`（預設：`https://insurai.com.tw/insurai/agent`；必須為 HTTPS）
- 認證方式：所有請求都必須帶入 Header X-API-KEY: $INSURAI_API_KEY
- TLS 驗證：一律啟用，使用 Python `requests` 預設安全設定；`INSURAI_AGENT_URL` 必須使用 HTTPS，且不提供停用 TLS 驗證的環境變數
- **外部依賴**：Python `requests` 庫（腳本會在執行時自動檢查，若缺少會清楚提示）

若尚未取得 `INSURAI_API_KEY`，請先至 https://insurai.com.tw 註冊會員，登入後申請 `INSURAI-API-KEY`，再設定 `INSURAI_API_KEY`。`INSURAI_AGENT_URL` 可省略，預設使用正式端點。

### 安全與能力邊界

本 skill 僅透過內建 Python helper 呼叫 InsurAI Agent API。

會使用的環境變數：

- `INSURAI_AGENT_URL`：HTTPS API base URL，預設為 `https://insurai.com.tw/insurai/agent`
- `INSURAI_API_KEY`：僅作為 `X-API-KEY` header 傳送至 `INSURAI_AGENT_URL`

網路存取：

- helper 僅向 `INSURAI_AGENT_URL` 發送請求
- 預設正式端點為 `https://insurai.com.tw/insurai/agent`
- `INSURAI_AGENT_URL` 必須使用 HTTPS；非 HTTPS URL 會在送出任何 API 請求前被拒絕

會送至 API 的資料：

- 使用者提供的保險情境、職業關鍵字、商品搜尋字詞、保險公司篩選條件、年齡、性別、職業等級、商品代碼與文件類型等必要查詢參數

隱私與資料處理：

- 保險規劃與商品查詢輸入可能包含敏感個人或財務資料，例如年齡、性別、地區、職業、家庭狀況、既有保單、健康相關情境與保障需求
- 每次對話首次呼叫 API 前，應告知使用者必要資料會送至設定的 `INSURAI_AGENT_URL`，並取得使用者同意後才繼續
- 送出內容應採最小化原則
- 除非使用者明確要求且該 action 必要，否則不得包含身分證字號、聯絡方式、完整保單文件、付款資料、醫療紀錄或其他不必要識別資訊
- 若代他人查詢，應先取得該當事人同意

不允許的行為：

- 不列舉本機檔案
- 不列舉環境變數；helper 只讀取明確列入允許清單的 `INSURAI_AGENT_URL` 與 `INSURAI_API_KEY`
- 不讀取或上傳使用者檔案
- 不輸出或暴露 `INSURAI_API_KEY`
- 不執行 sudo、安裝套件、下載外部腳本或任意 shell 指令

在執行任何 API 呼叫前，先確認環境變數已設定；不要輸出 API key 明文：

```bash
echo "Agent URL: ${INSURAI_AGENT_URL:-https://insurai.com.tw/insurai/agent}"
test -n "$INSURAI_API_KEY" && echo "API Key: set" || echo "API Key: missing"
```

若 `INSURAI_API_KEY` 未設定，請提示使用者先至 https://insurai.com.tw 註冊會員並申請 `INSURAI-API-KEY`，再設定 `INSURAI_API_KEY`；只有需要覆寫正式端點時才設定 `INSURAI_AGENT_URL`：

```bash
export INSURAI_API_KEY=your_api_key_here
# Optional: override the production endpoint.
export INSURAI_AGENT_URL=https://insurai.com.tw/insurai/agent
```

---

## API 呼叫方式（重要）

**一律使用 Python 幫手腳本**，嚴禁使用 curl。

原因：Python 幫手腳本會統一處理 API key、TLS 驗證、retry、timeout 與錯誤訊息。所有 API 呼叫都必須透過以下 Python 腳本：

> 📎 **腳本進階用法**（含已知 Bug 修復、批量查詢技巧、timeout 分級）：參見 [insurai-api-script.md](insurai-api-script.md)
> 📎 **REST 端點契約**（各功能 HTTP method/path、請求欄位型別、回傳 JSON schema、錯誤碼）：參見 [insurai-api-spec.md](insurai-api-spec.md)。本文件為值域與行為規則的單一真實來源。

以下相對路徑均以 skill 根目錄為基準。執行前先切換至 skill 的實際安裝目錄：

```bash
python3 scripts/insurai_api.py <action> [args...]
```

Python 腳本使用 `requests` 庫，`INSURAI_AGENT_URL` 必須使用 HTTPS，TLS 憑證驗證一律啟用且不得關閉；不提供停用 TLS 驗證的環境變數，避免帶有 `X-API-KEY` 與保險資料的請求暴露於中間人攔截或竄改風險。

---

## Python 腳本使用方法

### 職業查詢

```bash
python3 scripts/insurai_api.py occupations_search --keyword "護理師"
```

### 保險規劃判讀

```bash
python3 scripts/insurai_api.py plan_interpret --scenario "30歲男性，機車外送員..."
```

### 商品推薦

```bash
python3 scripts/insurai_api.py recommend \
  --protection "失能生活支持保障" "實支實付醫療保障" \
  --age 30 --gender male --occupation-level 3 \
  --insurers "204" "209" \
  --recommend-type main-rider
```

> ⚠️ **CLI 參數名稱**：`--insurers`（非 `--insurer` 或 `--insurer-codes`）；`--protection` 可多值（空白分隔）；`--occupation-level` 為整數。

### 商品檢索

```bash
python3 scripts/insurai_api.py search --q "糖尿病" --page-size 5
```

**預設只回傳可售商品**。search 會送出 `availableProduct=true`；如需包含停售商品，使用 `--no-available-product`。recommend 的可售條件由 server-side 固定為 true，CLI 傳入可售參數時只會印 WARNING 後忽略。
同一商品有多次變更（第一次部分變更、第二次部分變更…）時，系統只回傳目前在售的最新版本。

### 批量 Metadata（平行，結果順序與輸入順序完全一致）

```bash
python3 scripts/insurai_api.py batch-metadata \
  --codes "105151424501010003" "205211MZ1A00821A11Z10000006" \
  "202131MZ1A98A22A11Z10000000" "108151424500120005" \
  --quiet
```

### 商品 Metadata

```bash
python3 scripts/insurai_api.py metadata --product-code "216321MZ2B24023A11Z10000008"
```

### 商品條款文件

```bash
python3 scripts/insurai_api.py document --product-code "216321MZ2B24023A11Z10000008" --campaign-type contract
```

### PDF 下載連結

```bash
python3 scripts/insurai_api.py pdf_link --product-code "216321MZ2B24023A11Z10000008" --campaign-type contract
```

---

## 功能 1：保險規劃判讀

### 使用時機

當使用者提供個人或家庭情境，想取得保障分析、家庭風險重點、建議方向、待補資料時使用。

### 輸入要求

scenario 必須是單一完整文字描述，建議至少包含：

- 年齡
- 性別
- 家庭狀況（單身 / 已婚 / 有無子女 / 有無負債等）
- 職業（若已知）

若最低必要資訊不足，直接要求補充，不得呼叫 API。
若任務需要標準值，性別應依本文件 gender 規則正規化為 male 或 `female`。

### API

```bash
python3 scripts/insurai_api.py plan_interpret \
  --scenario "情境文字"
```

### ⚠️ Agent 執行紀律（嚴格遵守）

**當使用者提出的問題屬於保險規劃、癌症險、醫療險、壽險、失能險、長照險、意外險、年金險等場景時，Agent 必須依以下順序執行，嚴禁跳過或先用一般知識搪塞：**

1. 先套用本文件的適用範圍、拒絕與正規化規則
2. 依工作流呼叫 InsurAI API 取得真實資料
3. 以 API 回傳結果為基礎，再結合通用知識給予建議

**常見失敗模式：Agent 先用自己的通用保險知識快速回覆，事後才補叫 InsurAI——這是執行順序錯誤，應杜絕。**

---

### 癌症險查詢工作流（重要）

當使用者詢問癌症險時，建議遵循以下順序，以避免過早深入錯誤的商品：

1. **`recommend`** — 先用保障關鍵字取得候選商品代碼清單
2. **`batch-metadata`** — 一次查多筆商品的結構化資訊（名稱、公司、銷售/停售狀態）
3. **`document`** — 確認感興趣的商品後，再查閱條款全文

**常見陷阱**：使用者可能描述「84歲滿期領回」的癌症險，但 InsurAI 系統中沒有 84 歲滿期的防癌險。實務上最接近的選項是：

- **85歲滿期**：全球人壽臻心85防癌定期健康保險附約（`264321RZ1AXCE22A11Z10000002`，為附約需搭配主約）
- **90歲滿期**：國泰人壽豪康愛防癌定期保險（`204321MZ9BMFA22A11E10000000`）
- **100歲祝壽**：台新人壽愛寶倍終身壽險（`255191MA2B23723A11Z10000001`）

若使用者提及 84 歲，應先提醒這個數字可能與系統商品不完全吻合，建議以「多少歲以前確診癌症一次領」或「滿期年齡」重新確認需求。

### 請求欄位

- `scenario`：使用者完整保險需求描述（必要；例如 `35 歲男性，已婚有一子，職業護理師，想補強醫療與意外保障`）

### 成功回傳結構（示意）

{
"success": true,
"code": "OK",
"message": "判讀完成",
"data": {
"household": {
"summary": "",
"mainHouseholdConcerns": [],
"recommendationReason": ""
},
"insuredPersons": [],
"overallPendingData": []
},
"error": null
}

### 回應原則

不要直接傾倒完整 JSON，請整理以下重點：

- data.household.summary
- data.household.mainHouseholdConcerns
- data.household.recommendationReason
- 每位 insuredPerson 的重點保障建議
- data.overallPendingData

### 回覆模板

家庭風險摘要：

- ...

主要關注：

- ...

建議方向：

- ...

被保險人建議：

- [姓名或角色] immediate：...
- [姓名或角色] future：...

尚待補充資料：

- ...

### success = false 處理

success = false 時，僅回報 error.reason 或 code 對應訊息，立即停止，不做額外推論。

常見 `code`：

- `STAGE1_INSUFFICIENT_CONTEXT`：輸入不足以辨識人生階段，需補充資料
- `INSUFFICIENT_CREDITS`：點數不足，請聯絡客服
- `INTERNAL_ERROR`：系統錯誤，請稍後再試

---

## 功能 2：保險個人職業分類表查詢

### 使用時機

當使用者想查詢保險用途的個人職業分類資料時使用。

適用情境包括：

- 查詢某職業在保險個人職業分類表中的對應資料
- 查詢職業所屬的大分類、中分類、小分類／職業名稱（工作性質）
- 查詢職業等級
- 查詢職業代碼或最接近的職業名稱

### API

```bash
python3 scripts/insurai_api.py occupations_search --keyword "護理師"
```

### 查詢參數

- q`：職業關鍵字（必要），例如 `護理師`；在呼叫範例中以 `{keyword} 代入

### 成功回傳結構（示意）

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

### 欄位說明

- `primaryCode`：大分類代碼
- `primaryName`：大分類名稱
- `secondaryCode`：中分類代碼
- `secondaryName`：中分類名稱
- `occupationCode`：職業代碼
- `occupationLevel`：職業等級
- `occupationName`：小分類／職業名稱（工作性質）
- `widelyUsed`：是否為常用職業項目

### 回應原則

- 優先回傳最符合關鍵字的職業項目
- 回覆時應整理以下資訊：大分類代碼、大分類名稱、中分類代碼、中分類名稱、職業代碼、小分類／職業名稱（工作性質）、職業等級、是否為常用職業
- 若查得多筆相近結果，優先列出最相關結果；必要時可補充其他相近職業供使用者確認
- 若查無明確結果，應明確告知查無符合的保險個人職業分類資料
- 若 occupationLevel 無有效值，應明確標示職業等級未知

### 風險等級說明

- 1 = 最低風險
- 6 = 最高風險
- 0 或 null = 未知或無有效資料

---

## 功能 3：依保障名稱推薦保險商品

### 使用時機

當使用者已有明確保障需求，或保險規劃判讀已產出保障名稱，想進一步取得對應商品推薦時使用。

適用情境包括：

- insur-plan/interpret 回傳後，針對各被保險人之 immediate 保障名稱推薦商品
- 使用者直接指定保障名稱，如意外保障（意外醫療＋意外失能）、身故保障等
- 需依年齡、性別、保險公司、職業等級縮小推薦範圍
- 需決定只看主約，或同時看主約與可搭配附約

### API

```bash
python3 scripts/insurai_api.py recommend \
  --protection "實支實付醫療保障" --age 30 --gender male \
  --occupation-level 2 --recommend-type main-rider

# --insurers: 保險公司名稱或代碼（可多值），對應 API 欄位 insurers
python3 scripts/insurai_api.py recommend \
  --protection "實支實付醫療保障" "手術費用保障" \
  --age 30 --gender male --occupation-level 3 \
  --insurers "204" "209" \
  --recommend-type main-rider
```

### 請求參數（JSON Body）

- `protectionNames`：保障名稱清單，可多值（自然語言，必要；例如 `["醫療保障（住院日額＋實支實付＋手術）"]`）
- `age`：被保險人年齡（選填）
- `gender`：被保險人性別（選填，`male / female`）
- `insurers`：保險公司代碼清單，可多值（選填；例如 `["204","209"]`）
- `occupationLevel`：職類等級（選填，`1-6`）
- `recommendType`：推薦類型（選填，`main / main-rider`，預設 `main`）

> **CLI 提示**：`--insurers` 接受保險公司名稱或代碼（多值），對應 JSON 欄位 `insurers`。

### 使用原則

- 若來自保險規劃判讀，應優先使用各被保險人的 immediate 保障名稱作為 `protectionNames`
- 若使用者已提供年齡、性別、保險公司或職業等級，應一併帶入以提升推薦精準度
- recommendType 若未指定，預設使用 main
- recommendType 僅可為 main 或 main-rider

### 成功回傳結構（示意）

{
"productCodes": [
{
"main": {
"code": "204321MZ9BMFA22A11E10000000",
"name": "國泰人壽豪康愛防癌定期保險（外溢型）",
"insurer": "國泰人壽",
"mainBenefits": [
{
"item": "滿期保險金",
"description": "被保險人生存至90歲保單週年日，保險公司按「當年度保險金額」給付「滿期保險金」。",
"note": "給付後契約終止。"
},
{
"item": "初次罹患癌症（初期）或癌症（輕度）保險金",
"description": "被保險人初次診斷確定罹患癌症（初期）或癌症（輕度），保險公司按診斷確定的保單年度給付保險金。",
"note": "以給付一次為限，需滿足等待期且為首次罹患。"
}
]
},
"supplementaryRiders": [
{
"code": "...",
"name": "...",
"insurer": "...",
"mainBenefits": [...]
}
]
}
]
}

### 欄位說明

- `productCodes`：推薦結果清單，每筆代表一組主約與可搭配附約
- `main`：主約商品完整資訊，含 code、name、insurer、mainBenefits
- `supplementaryRiders`：推薦組合中，與 `main` 搭配以補足保障需求的附約商品列表；各元素結構與 `main` 相同。若無附約搭配，回傳 `[]`。
- `mainBenefits`：給付項目明細（item + description + note），**這是判斷商品屬性的依據**，不是 contractType 或商品名稱

### ⚠️ 重要觀念：如何正確判斷保險商品屬性

保險商品的本質屬性（是否癌症險、是否含意外理賠等）**必須依靠 mainBenefits 給付項目來判斷**，原因如下：

- `contractType` 欄位時常為「無資料」或過於籠統（例如：終身壽險同時理賠癌症、意外、骨質疏鬆）。
- 商品名稱無法完整反映商品實際涵蓋的給付項目。
- 同一家保險公司可能推出多張癌症相關商品，保障範圍差異需靠給付項目比對才能確認。

因此，**絕對不可依賴 contractType 或商品名稱來判斷商品保障範圍**，必須檢視 `mainBenefits` 的 `item`（給付名稱）與 `description`（說明）內容。

### ⚠️ Pitfall：`recommend` 回傳 key 是 `productCodes`，不是 `combinations`

初次使用時容易用錯 key 導致取不到數據。實際回傳格式：

```json
{ "productCodes": [{ "main": {...}, "supplementaryRiders": [...] }] }
```

**不是** `combinations`、`results`、`items`。取陣列長度應用 `len(d.get('productCodes',[]))`。
`supplementaryRiders` 在無附約時為 `[]`；可直接迭代 `for r in item.get('supplementaryRiders', []):`。

### ⚠️ 年齡計算：西元年出生 vs 民國年

- **西元出生**（如 `1979.03`）：2026 − 1979 = **47歲**（已過生日則維持47，未過生日則46）
- **民國出生**（如 `68.03`）：68 + 1911 = 1979 → 演算法相同
- 呼叫 API 時傳入 `age=47`（整數）

### 回應原則

- 若功能恢復後，回傳最多 8 組商品（主約與可搭配附約）
- 回傳時應自動內嵌 code、name、insurer、mainBenefits，不需另外呼叫 batch-metadata
- Agent 取得推薦結果後，可針對每筆商品再呼叫 Markdown 文件取得功能閱讀條款全文，或呼叫 PDF 連結功能提供下載

---

## 功能 4：保險商品檢索

### 使用時機

當使用者想搜尋特定商品、條款內容、保障名稱或全文關鍵字時使用。

適用情境包括：

- 指定商品名稱或商品代碼進行查詢
- 查詢條款中的特定條件，如復健費用、除外責任、理賠條件
- 查詢特定保障名稱所對應的商品清單
- 需依保險類別、公司、職業等級、性別、年齡進一步過濾商品

### API

```bash
python3 scripts/insurai_api.py search \
  --q "關鍵字" --page-size 10
```

### 請求參數（JSON Body）

- `q`：全文查詢字串（選填；例如 `糖尿病`）
- `productName`：商品名稱關鍵字（選填；例如 `安心終身`）
- `protectionNames`：保障名稱清單，可多值（選填；例如 `["死亡給付","完全失能給付"]`）
- `insurers`：保險公司代碼清單，可多值（選填；例如 `["203","209"]`）
- `availableProduct`：是否只查可售商品（預設為 `true`；需要包含停售商品時使用 `--no-available-product`）
- `occupationLevel`：職類等級（選填，`1-6`）
- gender`：性別（選填，`male / `female`）
- `age`：年齡（選填）
- `pageSize`：回傳筆數上限（選填，預設 10；例如 `10`）

### 使用原則

- 建議至少提供 `q`、`productName`、`protectionNames` 其中一個
- 若使用者已提供保險公司、性別、年齡、職類等級，應一併帶入以提升檢索精準度
- pageSize 預設為 10

### 成功回傳結構（示意）

[
{
"productCode": "A123456789",
"snippet": "...復健費用給付，被保險人因意外或疾病接受復健治療..."
}
]

### 欄位說明

- `productCode`：商品代碼
- `snippet`：命中關鍵字的前後文摘要

### 回應原則

- 若功能恢復後，回傳結果應包含 productCode 與 `snippet`（命中前後文）
- 對有興趣的商品，可進一步呼叫 Markdown 文件取得功能閱讀全文，或呼叫 PDF 連結功能提供下載

---

## 功能 5：查詢保險商品 Metadata

### 使用時機

當已知 `productCode`，但只需要商品的結構化資訊，不需要閱讀全文時使用。

適用情境包括：

- 確認商品名稱、保險公司、銷售日期、停售日期等 metadata
- 比較多筆商品的結構化屬性
- 已知商品代碼，需補齊商品基本資訊

### API

```bash
python3 scripts/insurai_api.py metadata --product-code "商品代碼"
```

### 查詢參數

- `productCode`：保險商品代碼（必要；例如 `202121MZ1A81A23A11Z10XXXXX0`）

### 使用原則

- 僅適用於已知 productCode 的情況
- {productCode} 為路徑參數，實際呼叫時應替換為真實商品代碼
- 若需要條款全文，不應只查 metadata，應改用 Markdown 文件取得功能
- 若使用者只需要 PDF 下載，不應查 metadata，應改用 PDF 連結功能

### 成功回傳結構（示意）

{
"productCode": "202121MZ1A81A23A11Z10000000",
"metadata": {
"version": "1.x.x",
"insuranceCompany": "XX人壽保險股份有限公司",
"productName": "XX人壽XX分紅終身還本保險",
"contractType": "無資料",
"coverage": {
"mainBenefits": [
{
"item": "生存保險金",
"description": "被保險人每屆保單週年日仍生存時給付。"
},
{
"item": "身故保險金或喪葬費用保險金",
"description": "被保險人身故時依約給付。"
},
{
"item": "完全失能保險金",
"description": "被保險人致成完全失能時依約給付，僅給付一次。"
}
],
"exclusions": [
"要保人故意導致被保險人死亡。",
"被保險人故意自殺（兩年後故意自殺仍負給付責任）。"
]
},
"premiumOptions": [
{
"paymentMethod": "年繳、半年繳、季繳或月繳。"
}
],
"policyTerms": [
{
"duration": "終身"
}
],
"officialRiders": []
}
}

### 欄位說明

- `productCode`：商品代碼
- `metadata`：商品 metadata（JSON 物件格式；主約存在 `riderProductCodes` 時可能包含 `officialRiders`）

### 回應原則

- 若功能恢復後，應回傳單一商品完整 metadata，不含 Markdown 全文

---

## 功能 6：取得保險商品文件（Markdown）

### 使用時機

當需要深入閱讀商品條款或費率表全文時使用。

適用情境包括：

- 確認除外責任、理賠條件、保障範圍等契約條款
- 取得費率表全文
- 商品推薦或商品檢索後，進一步閱讀條款全文

### API

```bash
python3 scripts/insurai_api.py document \
  --product-code "商品代碼" --campaign-type contract
```

### 查詢參數

- `productCode`：保險商品代碼（必要；例如 `202121MZ1A81A23A11Z10XXXXX0`）
- campaignOverviewType`：文件類型（必要，`contract / `premium`）

### 使用原則

- {productCode} 為路徑參數，實際呼叫時應替換為真實商品代碼
- 若需閱讀條款全文，應使用 campaignOverviewType=contract
- 若需閱讀費率表全文，應使用 campaignOverviewType=premium
- campaignOverviewType 僅可為 contract 或 premium

### 成功回傳結構（示意）

{
"productCode": "202121MZ1A81A23A11Z10XXXXX0",
"document": "# XX終身醫療保險條款\n\n## 第一條 保險範圍\n被保險人於本契約有效期間內..."
}

### 欄位說明

- `productCode`：商品代碼
- `document`：文件內容（Markdown 格式全文）

### 回應原則

- 若功能恢復後，回傳內容可包含 Markdown 全文

---

## 功能 7：取得保險商品 PDF 下載連結

### 使用時機

當使用者要求下載 PDF，或需要取得保險契約 / 費率表 PDF 連結時使用。

適用情境包括：

- 使用者明確要求下載商品 PDF
- 需要取得保險契約 PDF
- 需要取得費率表 PDF

### API

```bash
python3 scripts/insurai_api.py pdf_link \
  --product-code "商品代碼" --campaign-type contract
```

### 查詢參數

- `productCode`：保險商品代碼（必要；例如 `202121MZ1A81A23A11Z10XXXXX0`）
- campaignOverviewType`：文件類型（必要，`contract / `premium`）

### 使用原則

- {productCode} 為路徑參數，實際呼叫時應替換為真實商品代碼
- 若需保險契約 PDF，應使用 campaignOverviewType=contract
- 若需費率表 PDF，應使用 campaignOverviewType=premium
- campaignOverviewType 僅可為 contract 或 premium

### 成功回傳結構（示意）

{
"productCode": "202121MZ1A81A23A11Z10000000",
"type": "contract",
"pdfUrl": "https://example.com/documents/%E5%95%86%E5%93%81%E5%90%8D%E7%A8%B1.pdf?tiiProductCode=xxxxxx"
}

### 欄位說明

- `productCode`：商品代碼
- type`：文件類型（`contract 或 `premium`）
- `pdfUrl`：PDF 下載連結

### 回應原則

- 若功能恢復後，應回傳 PDF 下載連結
- 若使用者要求下載 PDF，應優先使用本功能，而非 Markdown 文件取得功能

---

### 錯誤處理

### HTTP / 連線層

- `400 Bad Request`：請求參數有誤，指出缺少、格式錯誤或不合法欄位
- `401 Unauthorized`：API Key 無效或未設定，提示確認 `INSURAI_API_KEY`
- `402 Payment Required`：**點數不足**（後端回報 `INSUFFICIENT_CREDITS`）。適用於 occupations 與 insur-contracts 各端點；應明確告知使用者點數不足，請聯絡客服或儲值，**不得自行捏造結果**。
- `404 Not Found`：找不到指定商品、metadata、Markdown 文件或 PDF 連結
  - 僅在後端對「查無資料」明確回 404 時出現；不同部署可能以 502 或其他錯誤碼呈現下游服務異常。
- `501 Not Implemented`：功能暫停提供，應明確告知使用者目前無法使用該功能
- `502 Bad Gateway`：後端服務暫時無回應、回應格式錯誤或連線異常，建議稍後再試
- 其他 `5xx`：系統錯誤，建議稍後再試或聯絡管理員
- 網路連線失敗 / 逾時：告知無法連線至 `$BASE`，請確認網路或服務狀態
- ℹ️ **點數不足在 `plan_interpret` 是例外**：保險規劃判讀的點數不足不走 402，而是 HTTP 200 + `success=false` + `code=INSUFFICIENT_CREDITS`（in-body，見「功能 1」與下方業務層）。

### 常見連線失敗診斷

當 python3 指令逾時（exit code 非 0）且 API Key 已設定時，先執行以下檢查：

```bash
# 1. 確認 API Key 存在，不輸出明文
test -n "$INSURAI_API_KEY" && echo "API Key: set" || echo "API Key: missing"

# 2. 檢查主機解析結果
host insurai.com.tw

# 3. 測量對外網路是否正常
python3 -c "import requests; r=requests.get('https://www.google.com', timeout=10); print(r.status_code)"

# 4. 測試 Python 腳本是否正常
python3 scripts/insurai_api.py occupations_search --keyword "test"
```

**若主機解析到私有 IP（如 192.168.x.x）**：代表 API 伺服器需透過內網/VPN 才能訪問，請確認目前網路環境是否可達。若 TCP 443 連線正常（openssl s_client 可連線）但 Python 腳本逾時，可能是網路 policy 阻擋了對該 IP 的 HTTPS 流量，請告知使用者聯絡 IT 確認防火牆規則。

### 業務層

- `/insur-plan/interpret` 回傳 `success = false`：僅告知 `error.reason` 或 `code` 對應訊息，停止處理
- `/insur-contracts/recommend` 若 `recommendType` 非 `main` 或 `main-rider`：視為參數錯誤
- `/insur-contracts/document` 若 `campaignOverviewType` 非 `contract` 或 `premium`：視為參數錯誤
- `/insur-contracts/pdf-link` 若 `campaignOverviewType` 非 `contract` 或 `premium`：視為參數錯誤

---

## 限制

以下情況不得使用本 skill：

- 未授權的服務維運、部署、資料庫或伺服器操作
- 非中華民國（臺灣）的保險規劃或保險個人職業分類表查詢
- 投保、出單、付款
- 保單異動
- 理賠申請
- 不得回答未列入保險公司代碼表之保險公司商品、條款、費率、承保規則或分類資料
- 命中直接拒絕規則之問題，不得展開討論、不得提供替代方案、不得進行後續分析
- 不得自行跨保險公司或跨查詢結果拼裝主約／附約組合（須原樣呈現 API 回傳之主約與其對應附約）
- 與 InsurAI 保險規劃、保險個人職業分類表查詢、商品推薦、商品檢索、metadata 查詢、Markdown 文件取得或 PDF 連結取得無關的任務
- 對於目前回應 501 Not Implemented 的商品相關功能，不得自行捏造推薦結果、檢索結果、metadata、Markdown 全文、摘要或 PDF 連結
