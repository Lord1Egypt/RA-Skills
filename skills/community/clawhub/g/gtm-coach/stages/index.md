# GTM Coach — stage router

Load exactly one stage SOP matching `strategy.period` for the CMO board. The stage stays visible every turn. Channel SOPs are separate and load only after the founder chooses a channel.

| Period | Load |
| --- | --- |
| `validate` | [validate.md](validate.md) |
| `build` | [build.md](build.md) |
| `cold_start` | [cold-start.md](cold-start.md) |
| `launch` | [launch.md](launch.md) |
| `promote` | [promote.md](promote.md) |
| `monitor` | [monitor.md](monitor.md) |

Stages can overlap in reality, but the weekly plan must have one primary period. Partnerships are an optional channel/campaign, not a required stage.

## First-run period (propose, do not confirm)

If `/status.picture.suggested_period` exists, use it as a hypothesis. Otherwise:

| Bound facts | Propose |
| --- | --- |
| Project not `confirmed`, or no public offer/URL | `validate` |
| Offer is usable/live, no proven ICP conversation or activation loop | `cold_start` |
| Founder names a time-bounded PH/HN/event this week | `launch` |
| One channel already produces repeat **ICP** outcomes | `promote` |
| Repeat economics are healthy | `monitor` |

Keep `strategy.confirmed=false` until the founder agrees. Never pick `promote` or `monitor` from NicheReach instrument counts alone (`leads_pending`, `replies_posted_7d`).
