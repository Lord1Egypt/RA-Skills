# 保單檢視與缺口分析工作流

使用 insurai-tw skill 對既有保單進行全面檢視、比對需求、找出缺口並推薦補強方案。

## 適用時機

使用者在以下情境時觸發此工作流：
- 「幫我看這張保單」
- 「保單繳了X年都沒用到，該解嗎」
- 「我的保障夠嗎」
- 上傳保單圖片/PDF 詢問建議

## 完整工作流（6步驟）

### Step 1: 取得保單內容

三種方式：
- **OCR 圖片** → 先交由外部 OCR／文件處理能力轉成文字，再把 OCR 結果交給 insurai-tw 分析
- **PDF文件** → 先交由外部 OCR／文件處理能力抽出文字，再把文字結果交給 insurai-tw 分析
- **使用者口述** → 直接整理成表格

**目標**：列出所有商品代號（短碼）、商品名、保額、年繳保費、繳費年期。

> ⚠️ OCR 常將商品名辨識錯誤（如「無慮」→「無憂」、保險公司簡稱漏字），**不要只看 OCR 原文就斷定商品名**，要交叉比對 search 結果。
> ⚠️ 臺灣保險規劃書常用表格排版，OCR 容易欄位錯位（金額跑到保額欄）。必要時應要求外部 OCR／文件處理能力重新辨識，並用費率表交叉驗證金額正確性。

### Step 2: 短碼轉譯 → 找 InsurAI productCode

保單上的短碼（T09V0、HNRC、T02J1、SPAR、BJ0 等）**不是** InsurAI product code。

**正確流程**：
```bash
python3 scripts/insurai_api.py search --q "<保險公司> <商品名關鍵字>" --page-size 5
```

- 用 `--q` 參數帶入「公司名 + 商品名全名/關鍵字」
- 從回傳結果的 `productCode` 取得正式代碼
- 多商品平行查詢（同回合送多個 terminal call）

**找不到時的應對**：
- 換關鍵字組合（少掉一些字、換同義詞）
- 部分舊商品或停售商品可能不在資料庫 → 標註「InsurAI 無此商品資料，以保單面額為準」

### Step 3: 取得商品 metadata

用 search 找到的 productCode 查 metadata 確認商品內容：

```bash
# 批量查（優先，節省回合）
python3 scripts/insurai_api.py batch-metadata --codes "code1" "code2" "code3" --quiet
```

注意：`batch-metadata` 回傳的是 metadata 表，不含詳細條款。需要條款時再走 `document --campaign-type contract`。

### Step 4: 需求分析（plan_interpret）

取得使用者完整背景後跑規劃判讀：

```bash
python3 scripts/insurai_api.py plan_interpret --scenario "<完整情境描述>"
```

**情境描述必須包含**：
- 年齡、性別
- 職業（影響職業等級和風險評估）
- 家庭狀況（子女數、是否有配偶收入）
- 負債（房貸金額）
- 現有保障摘要（可省略，plan_interpret 不知道你已有的保單）

### Step 5: 缺口比對（人工分析）

用表格比對「plan_interpret 建議」vs「現有保單」：

| 保障類型 | 你需要 | 現有 | 缺口 | 優先級 |
|---------|--------|------|------|--------|
| 壽險 | ~600-800萬（房貸+子女教育） | XX萬 | 🔴 ~YYY萬 | 1 |
| 失能險 | 一次金200-300萬+月扶助 | 僅意外失能 | 🔴 疾病失能0 | 2 |
| 重大傷病 | 100-200萬 | XX萬 | 🟡 差YY萬 | 3 |
| 實支實付 | 夠用 | HNRC計劃二 | 🟢 OK | - |

### Step 6: 推薦補強商品

用 recommend API 找候選：

```bash
# 定期壽險
python3 scripts/insurai_api.py recommend --protection "定期壽險" "實支實付醫療保障" --age XX --gender male/female --occupation-level X --recommend-type main-rider

# 失能險（用多組關鍵字）
python3 scripts/insurai_api.py recommend --protection "失能保障" "實支實付醫療補強" --age XX --gender male/female --occupation-level X

# 重大傷病
python3 scripts/insurai_api.py recommend --protection "重大傷病保障" "實支實付醫療保障" --age XX --gender male/female --occupation-level X
```

> ⚠️ **recommend 已知限制**：單一廣義關鍵字（「壽險」、「失能」）常回傳空結果。一定要搭配另一個關鍵字組合，如 `"定期壽險" "實支實付醫療保障"`。

**費率查證**：對候選商品跑 `document --campaign-type premium`，取得真實費率表，算出該年齡性別的精確年繳。

**⭐ 費率交叉驗證（重要）**：規劃書上標示的保費未必與 API 費率表完全一致（可能因計劃別命名差異、優惠折扣、匯率等因素）。**拿到規劃書上的保費後，務必用 API 費率表核對**——例如「20計劃別」在 API 費率表中可能是 M20，費率可能與規劃書有差距。發現不一致時：
1. 先確認計劃別的命名對應（規劃書的 20計劃別 = M20？M10？）
2. 再確認性別費率差異（規劃書可能誤用異性費率）
3. 如有重大差異，提醒使用者向業務員確認

## 呈現方式

1. **保單現狀表格**：代號、商品名、保額、年繳、重要性標註
2. **方案比較**（如減額繳清 vs 解約 vs 保留）：省多少、風險是什麼
3. **缺口分析**：依優先級排列，每個缺口有具體數字
4. **補強建議**：推薦商品名稱 + 年繳金額 + 為什麼選這張
5. **預算總表**：省下的 vs 新增的，每月/年實際差異

## 常見陷阱

- ❌ **短碼直接送 metadata** → 一定會 404 或查到無關商品
- ❌ **只用一組關鍵字跑 recommend** → 常回空，需多組組合
- ❌ **先講結論再查資料** → 流程必須：查 API → 得資料 → 再給建議
- ❌ **只用一次 recommend 就交差** → 壽險/失能/重傷需各跑一次
- ⚠️ **plan_interpret 回傳的是「建議方向」而非「精確數字」** → 用它抓大方向，具體保額要用人腦估算（房貸+扶養比公式）
- ⚠️ **40歲族群的「三缺」高頻模式**：此年齡層國泰業務員規劃書常見三項集體缺失→① 實支實付額度過低（20計劃別以下）、② 完全無重大傷病險、③ 完全無癌症一次金。業務員傾向塞入高保費的終身日額商品而不補這三項。**看到其中一缺，強烈懷疑另外兩缺也存在**，主動查證後一併建議補強方向。
