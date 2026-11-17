# Action contract

item.upsert:sku,name,unit optional,currency three-letter code,reorderPoint,targetStock decimal strings. move:id unique,sku,warehouse defaultmain,kind in|out|adjust,quantity decimal string; in requires unitCost; adjust means counted total quantity and requires unitCost and reason; out consumes moving-average value and rejects negative stock. date optional YYYY-MM-DD. Movement retries with identical ID+payload replay once; conflicting IDs fail. ledger optional sku/warehouse. stock/report optional warehouse. Exact Decimal arithmetic, max6fraction digits,1e15 values. Exported stockValue rounded half-up2decimals; internal value remains higher precision. No FX conversion, no deletion of ledger history.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
