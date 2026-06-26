# Example: monthly CPI for the last 24 months

This walkthrough shows the typical agent flow: `search` → `meta` → `data`.

## 1. Find the table

```bash
$ scripts/search.sh "소비자물가지수" --per-page 5
```

Returns hits like:

```jsonl
{"LIST_NM":"품목별 소비자물가지수","ORG_ID":"101","TBL_ID":"DT_1J17001",...}
```

Pick `orgId=101 (통계청)`, `tblId=DT_1J17001`.

## 2. Inspect the table's items + dimensions

```bash
$ scripts/meta.sh 101 DT_1J17001 --type ITM
```

Returns the available `ITM_ID` codes — for CPI: `T01` (총지수), `T02` (식료품), …

```bash
$ scripts/meta.sh 101 DT_1J17001 --type OBJ
```

Returns the available `OBJ` (object) dimensions and their codes.

## 3. Pull data

Latest 24 monthly observations of headline CPI (`T01`):

```bash
$ scripts/data.sh 101 DT_1J17001 \
    --prd-se M \
    --recent 24 \
    --itm T01 \
    --obj-l1 ALL
```

Output (JSONL, one row per period):

```jsonl
{"PRD_DE":"202301","PRD_SE":"M","ITM_NM":"총지수","C1_NM":"전국","DT":"110.10","UNIT_NM":"2020=100","ORG_ID":"101","TBL_ID":"DT_1J17001"}
{"PRD_DE":"202302","PRD_SE":"M","ITM_NM":"총지수","C1_NM":"전국","DT":"110.42","UNIT_NM":"2020=100","ORG_ID":"101","TBL_ID":"DT_1J17001"}
...
```

## 4. Pipe into jq for the bits you actually want

```bash
$ scripts/data.sh 101 DT_1J17001 --prd-se M --recent 24 --itm T01 --obj-l1 ALL \
  | jq -c '{period: .PRD_DE, value: (.DT | tonumber)}'
```

```jsonl
{"period":"202301","value":110.1}
{"period":"202302","value":110.42}
...
```

That's it. The same flow works for any KOSIS table — only the `tblId`, `itmId`, and dimension codes change.
