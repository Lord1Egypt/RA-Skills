---
name: hormuz-monitor
description: >
  Monitor Strait of Hormuz shipping traffic from JMIC, Iranian sources,
  and news aggregation. Write findings to MONITOR_LOG.md.
  Auto-update website data after each cycle.
version: 1.3.0
---

# Hormuz Strait Shipping Monitor

## Sources to check

### Tier 1 - Primary data sources
- Web fetch: https://www.ukmto.org/partner-products/jmic-products (JMIC updates)
- Web fetch: https://windward.ai/blog/ (Daily maritime intelligence)

### Tier 2 - Iranian sources
- Web fetch: https://www.tasnimnews.ir/en/ (search for "Hormuz" or "strait")
- Web fetch: https://www.farsnews.ir/en (search for "Hormuz")

### Tier 3 - News & market data
- Web search: "Strait of Hormuz shipping traffic today"
- Web search: "تنگه هرمز کشتی" (Farsi search for Hormuz shipping)
- Web search: "Brent crude oil gold price today"
- Web search: "VLCC tanker rate Hormuz insurance today"

## Workflow

### Step 1-3: Data Collection
1. Fetch Tier 1 URLs and extract latest updates
2. Fetch Tier 2 Iranian sources for new articles
3. Run Tier 3 web searches for breaking developments and prices

### Step 4: Log Results

Read current MONITOR_LOG.md. Append a new timestamped entry at the bottom.

**CRITICAL FORMAT RULES — the website parser depends on exact formatting:**
- Price values: plain numbers, NO markdown bold `**`, NO tilde `~`. Example: `$115.27/bbl` not `**~$115.27/bbl**`
- VLCC rate: use `K` suffix. Example: `$423K/day` not `$423,000/day`
- All summary fields (新事件, 伊朗立场, 西方动态, 外交动态, 保险, Flash触发) MUST be written in Chinese
- Keep each summary field to ONE concise sentence (≤80 characters). Put detailed analysis in a sub-bullet if needed.
- Do NOT use markdown bold `**` anywhere in field values

Entry format:

```
## [YYYY-MM-DDThh:mmZ] — [NORMAL/ALERT]
- Vessel crossings: [number]/day
- Status: [open/restricted/closed]
- Brent: $[X]/bbl | WTI: $[X]/bbl
- Gold: $[X]/oz
- TTF Gas: €[X]/MWh
- VLCC rate: $[X]K/day
- 新事件: [一句话中文摘要]
  - [详细内容可放子项，英文可接受]
- 伊朗立场: [一句话中文摘要]
  - [详细内容]
- 西方动态: [一句话中文摘要]
  - [详细内容]
- 外交动态: [一句话中文摘要]
  - [详细内容]
- 保险: [一句话中文摘要]
  - [详细内容]
- Sources checked: [list]
- Flash触发: [无 / 一句话中文描述]
  - [详细数据对比]
```

Example entry:

```
## 2026-03-30T17:18Z — ALERT
- Vessel crossings: 11/day
- Status: restricted
- Brent: $115.27/bbl | WTI: $109.58/bbl
- Gold: $4,493/oz
- TTF Gas: €55/MWh
- VLCC rate: $423K/day
- 新事件: 航运量回升至11艘/日，两艘中国超大型集装箱船成功通过海峡
  - JMIC reports 11 transits/day March 28-29, up from 1-2 previously
  - CSCL Indian Ocean and CSCL Arctic Ocean transited successfully March 30
  - GPS/GNSS/AIS interference significantly reduced
- 伊朗立场: 选择性封锁持续，"德黑兰收费站"运营中，否认与美谈判
  - IRGC: vetting system operational for approved vessels
  - FM Araghchi: "Strait open, but closed to our enemies"
  - Parliament advancing legislation to formalize fees
- 西方动态: 联军分裂，美军事行动持续，Trump延期至4月6日
  - 22 nations condemn Iran's attacks; CENTCOM mine-laying prevention ongoing
  - UAE announced willingness to join multinational naval force
  - UK considering deploying mine-clearing vessel
- 外交动态: 巴基斯坦四方会谈进行中，间接谈判僵局未破
  - Pakistan hosts Turkey, Egypt, Saudi Arabia meeting March 29-30
  - US 15-point ceasefire proposal via Pakistan mediator
  - Iran submitted 5-point counter-proposal (war reparations, sovereignty)
- 保险: 战争险保费涨20-50倍，P&I保险暂停，劳合社扩大冲突区范围
  - War risk premiums 4-10% of vessel value per voyage (vs 0.2-0.5% pre-crisis)
  - International Group of P&I Clubs suspended standard cover Mar 5
- Sources checked: JMIC, Tasnim, Fars, Windward, CNBC, Trading Economics
- Flash触发: 通行量增幅>50%（11艘 vs 此前4-7艘）
  - Oil: $115.27 vs prior $116.18 = -0.8% (not >5%)
  - Vessels: 11/day vs prior 4-7/day = 57-175% increase
  - No ceasefire/breakthrough
```

### Step 5: Trim Old Entries
If MONITOR_LOG.md has entries older than 7 days, remove them.

### Step 6: Flash Alert Check
- Oil moved >5% since last entry? → FLASH
- Vessel count changed >50%? → FLASH
- Ceasefire/breakthrough/major attack detected? → FLASH
- Brent crossed $100 or $75? → FLASH

If FLASH: send immediate alert. If no FLASH: send brief summary.

### Step 7: Update Website Data
After writing MONITOR_LOG.md, run this command to update the website:

exec command: bash ~/hormuz-website/scripts/update_and_deploy.sh

This parses MONITOR_LOG.md into data.json and pushes to GitHub.
Vercel auto-deploys on push. If the script fails, log the error but
do not retry — the website will show the previous data until next cycle.

## Alert format
🚢 **Hormuz Monitor Update** [timestamp]
- **通行量:** [number]艘/日
- **状态:** [通航/受限/关闭]
- **Brent:** $[X] | **Gold:** $[X] | **VLCC日租:** $[X]K
- **新事件:** [摘要]
- **伊朗立场:** [摘要]
- **西方动态:** [摘要]
- **保险:** [状态]
- **数据源:** [list]
