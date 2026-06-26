---
name: moltenview
description: "Push persistent visual views (charts, metrics, lists, progress bars) to MoltenView Mac app. Use when agent output benefits from visual display that persists outside chat. NOT for: simple text responses, one-off data."
homepage: https://moltenrock.com
user-invocable: false
metadata: { "openclaw": { "emoji": "🔥", "requires": { "apps": ["MoltenView"] } } }
---

# MoltenView Skill

Push structured data to MoltenView — a persistent visual canvas for AI agents.

## When to Use

✅ **USE this skill when:**
- Displaying charts, metrics, or dashboards
- Data that should persist (not scroll away)
- Live-updating information
- Visual summaries the user will reference

❌ **DON'T use when:**
- Simple text responses suffice
- One-time data that doesn't need persistence

## Socket Path

```bash
export MOLTENVIEW_SOCKET="/Users/$USER/Library/Containers/com.goldcote.MoltenView/Data/.moltenview/view.sock"
```

## Push a View

```bash
echo '{"action":"push","data":{"title":"Dashboard","source":"openclaw","sections":[{"id":"s1","header":"Metrics","items":[{"id":"i1","title":"Sales","subtitle":"$12,450"}]}]}}' | nc -U "$MOLTENVIEW_SOCKET"
```

## Required Fields

- `data.source` — Agent name (string)
- `sections[].id` — Unique section ID
- `sections[].items[].id` — Unique item ID
- `sections[].items[].title` — Item title

## Supported Item Types

Set `type` on each item (omit or `"text"` for default):

| Type | Key Fields |
|------|-----------|
| **text** | title, subtitle, detail, badge |
| **chart** | chart.chartType (bar/line/pie/area), chart.dataPoints [{label, value, color}] |
| **gauge** | gauge.value, gauge.min, gauge.max, gauge.label, gauge.color |
| **progress** | progress (0.0-1.0), subtitle |
| **metric** | title (label), subtitle (big value), detail (change), metricColor |
| **link** | url (https/mailto), title, subtitle, icon |
| **image** | imageBase64, icon (SF Symbol), title |

## Example: Push a Chart

```bash
echo '{"action":"push","data":{"title":"Sales","source":"openclaw","sections":[{"id":"s1","header":"Revenue","items":[{"id":"c1","type":"chart","title":"Monthly","chart":{"chartType":"bar","dataPoints":[{"label":"Jan","value":100},{"label":"Feb","value":150},{"label":"Mar","value":200}]}}]}]}}' | nc -U "$MOLTENVIEW_SOCKET"
```

## Example: Push Metrics

```bash
echo '{"action":"push","data":{"title":"KPIs","source":"openclaw","sections":[{"id":"s1","header":"Today","items":[{"id":"m1","type":"metric","title":"Revenue","subtitle":"$12,450","detail":"+12%","metricColor":"#00FF00"},{"id":"m2","type":"progress","title":"Goal","progress":0.73}]}]}}' | nc -U "$MOLTENVIEW_SOCKET"
```

## Actions

| Action | Purpose | Data Required |
|--------|---------|---------------|
| `push` | Display new view | Yes |
| `update` | Update existing view | Yes |
| `clear` | Clear current view | No |
| `status` | Check connection | No |

## Status Check

```bash
echo '{"action":"status"}' | nc -U "$MOLTENVIEW_SOCKET"
# Returns: {"status":"ok"}
```

## Notes

- MoltenView must be running (free on Mac App Store)
- Views persist until cleared or replaced
- Get socket path from MoltenView → Settings → Connection
- Download: https://apps.apple.com/app/molten-view/id6742515562
