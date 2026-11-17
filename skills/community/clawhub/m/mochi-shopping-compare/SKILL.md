---
name: "mochi-shopping-compare"
description: "Calculate purchase costs, compare saved price snapshots, preserve referral URLs and export reports. Use for Shopping Comparison."
metadata: {"openclaw": {"requires": {"bins": ["node"]}, "homepage": "https://mochilab.bz", "version": "1.1.1"}}
---

# Shopping Comparison

## Compare sourced offers, not unsupported prices

Collect the intended use and the user's product links or quotes. The model gathers current evidence through available browsing when requested; the local script does not scrape websites or purchase items. compare takes asOf, criteria and 2..20 items with name,url,observedOn,currency,evidence plus known price,shipping,discount,quantity and specs. Preserve each exact source URL including referral parameters.

## Calculate the complete purchase cost

The script computes price times quantity plus shipping minus discount using integer currency units. Missing shipping stays unknown instead of becoming free. Incomplete offers stay out of complete-total rankings, and currencies remain separate. Use both bundle quantity and unit cost when comparing offers. A ranking by purchase total is not automatically a recommendation for suitability or lifetime cost.

## Track changes between saved snapshots

changes takes fromId and toId for two comparisons already saved in the same workspace. It matches exact URL, currency and quantity. Comparable offers show beforeMinor, afterMinor, deltaMinor and percentage change. A changed pack size is marked separately; missing prices or shipping are not treated as savings. Removed products remain visible in the change result. This is an on-demand comparison of supplied snapshots, not a background price monitor.

## Export a comparison that can be checked

export takes a comparison id and writes comparison.md and comparison.csv with observed dates, quantities, exact amounts, missing fields and original evidence. Show source dates alongside any conclusion. Keep the source link intact in exports. A scheduled watch or notification requires the host's scheduler and a defined data source; it is not created by saving a comparison.

## Run the local helper

Prepare an input JSON file inside the active agent workspace. Use the actual workspace, not another agent's directory.

```text
node "{baseDir}/scripts/run.mjs" --workspace "CURRENT_WORKSPACE" --input "request.json"
```

Read [references/input.md](references/input.md) before preparing fields. Every mutation and export uses a stable unique requestId; an identical retry returns its saved result. Put user text in JSON, not shell code. Successful exports return actual file paths, sizes and SHA256 values under this workspace's `.mochilab/mochi-shopping-compare/exports/` directory. Inspect the files before reporting completion. Previous exports are retained. No MochiLab key is needed by this standalone helper.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
