# jp-supplier-due-diligence — endpoints

Generated from the live JPVerify catalog. Prices are USD per successful call (the same with an API key or x402).

## English

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/companies/resolve` | `jp_company_resolve` | $0.25 | You hold an English, brand or romanized Japanese company name, an English address or postal code, a website or e-mail domain, a T-number, corporate number, LEI or securities code and need the Japanese legal entity, in English. | Decision (matched / likely_match / candidates), legally binding Japanese name, kana, English name with source, contract party name, status and qualified-invoice registration. Brand names (au, MOS Burger) find the owner as candidates; listing, Wikidata prominence and gBizINFO employee counts only order candidates. |
| `POST /v1/jp/suppliers/resolve` | `jp_supplier_resolve` | $0.10 | You need one coverage-aware supplier check combining company, qualified-invoice, and address evidence; optionally includes projected gBizINFO activity evidence when the internal feature flag is enabled. | Independent evidence checks, source versions, and a resolved/ambiguous/not-found/insufficient-coverage status; optional gBizINFO is projected enrichment inside this response, not a standalone source or raw-response resale. Not a legal or KYB determination. |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | You have a T-number and the issuer name from an invoice (address and invoice date optional) and need to know whether they belong together and the issuer was registered on the invoice date. | Registry fields, issuer name and address comparison, registration on the invoice date, supplier master comparison, and one status per check in check_results. |
| `POST /v1/jp/regulated-entities/verify` | — | $0.03 | You need to verify an entity against the covered Japanese FSA financial instruments, funds transfer, or crypto-asset exchange datasets. | Coverage-aware licensing decision, freshness, identity match, license evidence, and review warnings; not a legal unlicensed determination. |
| `GET /v1/jp/filings` | — | $0.01 | You need EDINET filing metadata for a Japanese company by corporate number, EDINET code, or security code. | Filing metadata, correction/withdrawal relationships, freshness, and official evidence references; raw files remain internal. |

## 日本語

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/companies/resolve` | `jp_company_resolve` | $0.25 | 英語名・ブランド名・ローマ字・英語住所・郵便番号・Webサイト／メールのドメイン・T番号・法人番号・LEI・証券コードから日本の法人を特定したい場合。 | 判定、正式な日本語商号、読み、出典付き英語名、契約当事者名、状態、適格請求書登録を返します。ブランド名（au、MOS Burger）からは所有企業を候補として返し、上場・Wikidataの知名度・Gビズインフォの従業員数は候補の並び順だけに使います。 |
| `POST /v1/jp/suppliers/resolve` | `jp_supplier_resolve` | $0.10 | 会社、適格請求書、住所の根拠を組み合わせ、必要に応じて内部機能フラグでgBizINFO活動根拠も付加した、対象範囲を明示した仕入先確認を行う場合。 | 個別の根拠チェック、ソース版、resolved/ambiguous/not-found/insufficient-coverage状態を返します。任意のgBizINFOはこのレスポンス内の加工済み補助根拠であり、単独ソースや原レスポンスの再販ではありません。法的判断やKYB判定ではありません。 |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | 請求書のT番号と発行者名（住所・日付は任意）が一致するか、請求書の日付時点で登録済みかを確認したい場合。 | 国税庁の登録情報、発行者名・住所の比較結果、請求書日付時点の登録状況、確認項目ごとの結果を返します。 |
| `POST /v1/jp/regulated-entities/verify` | — | $0.03 | 金融商品、資金移動、暗号資産交換の対象事業者データセットで日本法人を照合する場合。 | 対象範囲、鮮度、法人照合、免許根拠、確認警告を返します。無登録の法的判断ではありません。 |
| `GET /v1/jp/filings` | — | $0.01 | 法人番号、EDINETコード、証券コードから日本企業のEDINET提出書類を検索する場合。 | 提出書類メタデータ、訂正・撤回関係、鮮度、公式根拠を返します。原本ファイルは返しません。 |
