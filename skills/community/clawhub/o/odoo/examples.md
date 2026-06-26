# Odoo Request Translation Examples

Use this file when the user asks for something vague and you need to convert it into the right Odoo lane quickly.

| User request | Likely lane | Safe first move |
|--------------|-------------|-----------------|
| "Why are orders not going out?" | sales + inventory triage | trace `sale.order` to delivery state, reservation, and picking blockers |
| "Fix duplicate customers" | master data cleanup | preview merge rules, downstream documents, and duplicate keys before touching `res.partner` |
| "Upload this pricing file" | import | review identifiers, variants, company scope, and update-vs-create rule before import |
| "Numbers do not match finance" | reporting or accounting triage | lock company, period, posted status, and journal logic before recalculating |
| "Automate invoice reminders" | native automation or integration | define trigger, audience, exclusions, and failure handling first |
| "Stock is wrong" | inventory triage | separate on-hand, forecast, reservations, lots, and valuation before proposing a fix |
| "Upgrade broke the module" | Odoo.sh or self-hosted triage | identify surface, changed module, failing view or ACL, and staging path first |
| "Make this flow faster" | process design | decide whether the answer is UI discipline, import, server action, or external API |

## Translation Pattern

1. Name the business object.
2. Name the lane.
3. Name the safest first move.
4. Name the write risk, if any.

If you cannot do all four in one pass, the request is still underspecified.
