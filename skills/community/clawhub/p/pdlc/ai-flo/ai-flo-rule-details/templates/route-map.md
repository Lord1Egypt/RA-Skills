<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Route Map — AI-FLO

**Generated:** {date}
**Projects:** {N} active

---

## Visual Flow (All Projects)

```
{Project ID} (#{priority}):
  {pkg} ✅ → {pkg} ✅ → [{pkg} ⚡] → {pkg} → {pkg}
                          ↑ current position

{Project ID} (#{priority}):
  {pkg} ✅ → [{pkg} ⚡ ⚠️{N}d] → {pkg} → {pkg}
                    ↑ stalled

{Project ID} (#{priority}):
  [{pkg} ⚡] → {pkg} → {pkg} 🚫 → {pkg} → {pkg}
                              ↑ skipped
```

**Legend:**
- ✅ Complete
- ⚡ In Progress
- 🚫 Skipped (toggled OFF or not in profile)
- ⏸ Blocked
- ⚠️ Stalled ({N} days without movement)
- 🔴 Conflict (HOLDING)

---

## Summary Bar

| Metric | Count |
|--------|:-----:|
| Active projects | {N} |
| ✅ Complete (all stages) | {N} |
| ⚡ In Progress | {N} |
| ⏸ Blocked | {N} |
| ⚠️ Stalled | {N} |
| 🔴 Conflict | {N} |
| 🚫 Cancelled | {N} |

---

## Fan-In Status (AI-DWG)

| Project ID | AP (Required) | PBP (Optional) | UXP (Optional) | Ready? |
|------------|:-------------:|:--------------:|:--------------:|:------:|
| {PRJ-ID} | ✅ | ✅ | ⏳ | Minimum |
| {PRJ-ID} | ✅ | ✅ | ✅ | Full |
| {PRJ-ID} | ⏳ | — | — | Not yet |

---

## Active Holds

| Project ID | Reason | Since | Timeout | Fallback |
|------------|--------|-------|:-------:|----------|
| {PRJ-ID} | {conflict/block/wait} | {date} | {N}d | {rule} |

{If no holds: "No projects currently held."}

---

*Refresh with: `route map` or `status`*
