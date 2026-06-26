# Data Integrity Checklist for Prospecting

## Purpose
Ensure all prospecting outputs contain **real data only** — no fabrication, inference, or hallucination.

## Pre-Output Verification

Before saving any `P###.json` or `index.json`, verify:

| Field | Source | If Missing |
|-------|--------|------------|
| `name` | Google Maps listing text | Mark as `"unknown"` |
| `phone` | Google Maps listing or website | Mark as `"not found"` |
| `address` | Google Maps listing | Mark as `"not found"` |
| `rating` | Google Maps listing | Mark as `"not visible"` |
| `reviews_count` | Google Maps listing (may be hidden in restricted view) | Mark as `"restricted view"` |
| `has_website` | Google Maps listing ("网站" link visible?) | Set to `false` |
| `website_url` | Click through or web_fetch | Mark as `"not extracted"` |
| `business_type` | Google Maps category label | Mark as `"unknown"` |

## Red Flags — STOP and Report

- [ ] **Placeholder phone numbers** — Any `(XXX) 555-XXXX` pattern
- [ ] **Template data** — Data that looks "too perfect" or matches examples exactly
- [ ] **Missing `candidates-raw.txt`** — No raw extraction log from agent-browser
- [ ] **Empty `raw_notes`** — No record of data source or extraction issues
- [ ] **Assumed fields** — Any field filled with "likely", "probably", "expected"

## Network Failure Protocol

If agent-browser or web_fetch fails:

1. **Document the failure** in `raw_notes`: `"agent-browser timeout on Google Maps load"`
2. **Do NOT generate fake data** to fill the gap
3. **Report to user**: "Google Maps search timed out. Attempted [URL]. Got [partial data / no data]."
4. **Offer alternatives**:
   - Retry with different network/proxy
   - User manually provides data
   - Use alternative data source (Yelp, Yellow Pages API)

## Output Annotation Standards

When data is incomplete or unverified, use these markers:

```json
{
  "phone": "(713) 555-0101",
  "phone_status": "unverified_placeholder",
  "rating": "4.5",
  "rating_source": "visible_in_feed",
  "reviews_count": null,
  "reviews_count_note": "restricted_view_google_maps",
  "raw_notes": "Google Maps restricted view. Phone visible. Reviews count hidden. Website link present but not clicked."
}
```

## Post-Output Audit

After generating a batch, run this quick check:

```bash
# Check for placeholder phones
grep -r "555-01" prospect-data/

# Check for empty raw_notes
grep -r '"raw_notes": ""' prospect-data/

# Check for "unknown" sources
grep -r "likely\|probably\|expected\|assumed" prospect-data/
```

If any hits found, flag the batch for re-verification.

## User Communication Template

When data is incomplete:

> **Houston TX 搜索完成 — 部分数据受限**
> 
> 成功获取：7 家店铺名称 + 电话 + 地址 + 评分
> 
> 受限：Google Maps 未登录，评论数无法获取
> 
> 建议：登录 Google Maps 或手动验证以下字段：评论数、网站URL、营业时间
> 
> 已保存：`candidates-raw.txt` 记录原始提取数据

## Enforcement

This checklist is part of the prospecting skill. Violations (fabricated data without marking) should be:
1. Flagged in `raw_notes`
2. Reported to user immediately
3. Corrected before any call list is used
