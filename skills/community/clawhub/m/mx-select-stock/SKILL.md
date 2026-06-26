---
name: mx_select_stock
description: 基于妙想 (Meixiang) 智能选股 API，按用户提供的指标、行业或板块条件筛选 A 股、港股、美股等股票，返回完整 CSV 数据并提供列说明，避免使用过时的金融信息。
---

# 妙想智能选股 Skill (mx_select_stock)

## Overview
This skill enables safe, up‑to‑date stock screening using the Meixiang (妙想) stock‑screening service. It supports custom filters on market, financial indicators, and sector/category constraints, returning a full data table (CSV) with Chinese column headers and a supplemental description file.

## Prerequisites
1. Obtain an API key from the Meixiang Skills page.
2. Export the key to the environment variable `MX_APIKEY`:
   ```bash
   export MX_APIKEY="your_api_key_here"
   ```
3. Ensure `curl` is installed (standard on macOS).

## Usage Steps
1. **Formulate the query** – translate the user’s natural‑language request into a JSON payload containing at least:
   - `keyword` – the screening condition (e.g., "今日涨幅2%的股票")
   - `pageNo` – page number (default 1)
   - `pageSize` – number of rows per page (max 100, adjust as needed)
2. **Execute the POST request**:
   ```bash
   curl -X POST \
     --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen' \
     --header 'Content-Type: application/json' \
     --header "apikey:${MX_APIKEY}" \
     --data '{"keyword":"<YOUR_KEYWORD>","pageNo":1,"pageSize":20}'
   ```
3. **Parse the JSON response** – important fields:
   - `status` / `message` – overall request success.
   - `data.code` / `data.msg` – business‑level status.
   - `data.data.result.columns` – column definitions.
   - `data.data.result.dataList` – rows of stock data.
   - `responseConditionList` – condition statistics.
4. **Transform column titles** – map each `key` to its Chinese `title` from the `columns` array, then build a CSV where the header line uses the Chinese titles.
5. **Save output** (optional):
   ```bash
   # Save raw JSON
   curl ... > mx_select_stock_raw.json
   # Save CSV
   <script to convert> > mx_select_stock.csv
   # Save column description
   <script to extract> > mx_select_stock_columns.md
   ```
6. **Present to the user** – show a brief summary (total matches, key conditions) and attach the CSV/description files if the user requested them.

## Example
**User request:** “筛选今日涨幅在 2% 以上的 A 股”。

**Command:**
```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen' \
  --header 'Content-Type: application/json' \
  --header 'apikey:${MX_APIKEY}' \
  --data '{"keyword":"今日涨幅2%的股票","pageNo":1,"pageSize":20}'
```

**Sample JSON excerpt (truncated):**
```json
{"status":0,"message":"ok","data":{"code":"100","msg":"解析成功","data":{"result":{"total":57,"columns":[{"title":"序号","key":"SERIAL"},{"title":"代码","key":"SECURITY_CODE"},{"title":"简称","key":"SECURITY_SHORT_NAME"},{"title":"市场","key":"MARKET_SHORT_NAME"},{"title":"最新价 (元)","key":"NEWEST_PRICE"},{"title":"涨跌幅 (%)","key":"CHG"}],"dataList":[{"SERIAL":"1","SECURITY_CODE":"603866","SECURITY_SHORT_NAME":"桃李面包","MARKET_SHORT_NAME":"SH","NEWEST_PRICE":12.34,"CHG":2.13}, ...]}}}}
```

**Formatted reply to user:**
- **匹配股票数量**：57 只（符合条件）
- **筛选条件**：今日涨幅 ≥ 2%
- **示例数据**：
  |序号|代码|简称|市场|最新价 (元)|涨跌幅 (%)|
  |---|---|---|---|---|---|
  |1|603866|桃李面包|SH|12.34|2.13|
  |2|300991|创益通|SZ|8.76|2.05| …

## Saving Results (optional)
If the user wants the full CSV, run a conversion script (e.g., Python) that reads `dataList`, maps each `key` to its Chinese `title`, writes rows, and stores the file `mx_select_stock.csv`. Also generate `mx_select_stock_columns.md` describing each column.

## When Not to Use
Do not invoke this skill for non‑financial queries, for generic web searches, or when the user explicitly asks for opinion‑based advice without needing raw screening data.

## References
- Meixiang API documentation (internal).
- Column‑mapping table (see `columns` description above).
