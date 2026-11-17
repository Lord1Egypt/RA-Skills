# Recommendation Analysis Process

Step-by-step procedure for generating a recommendation from Taste data. This is the analytical backbone that feeds into `recommendation_style.md` for output formatting.

## Procedure

### 1. Load Data

Always load all three files from `<hermes-home>/commons/data/ocas-taste/`:
- `signals.jsonl` — all consumption signals
- `items.jsonl` — all item records with enrichment data
- `config.json` — strength model params + user preferences

Use the venv Python: `<hermes-home>/commons/data/ocas-taste/venv/bin/python3`

### 2. Compute Effective Strengths Per Item

Use the strength model from `config.json`:

```python
from datetime import datetime, timezone
from collections import defaultdict

now = datetime.now(timezone.utc)
item_signals = defaultdict(list)
for s in signals:
    iid = s.get("item_id", "")
    if iid:
        item_signals[iid].append(s)

for iid, sigs in item_signals.items():
    strengths = []
    for s in sigs:
        stype = s.get("signal_type", s.get("source_type", "visit"))
        base = strength_cfg.get(f"base_{stype}", 0.6)
        ts_str = s.get("timestamp", s.get("created_at", ""))
        if ts_str:
            try:
                ts = datetime.fromisoformat(ts_str)
                days_since = (now - ts).days
            except:
                days_since = 365
        else:
            days_since = 365
        decayed = base * (0.5 ** (days_since / halflife))
        strengths.append((decayed, days_since))
    
    max_strength = max(s[0] for s in strengths)
    freq_bonus = min(freq_cap, freq_per_visit * (len(sigs) - 1))
    min_days = min(s[1] for s in strengths)
    recency_bonus = recency_value if min_days <= recency_days else 0
    effective = min(1.0, max_strength + freq_bonus + recency_bonus)
```

### 3. Build Visited Venue Set

Extract ALL venue names from items.jsonl. Normalize to lowercase for dedup:

```python
visited = set()
for it in items:
    vn = it.get("venue_name", "")
    if vn:
        visited.add(vn.lower().strip())
```

This is the blocklist — never recommend from this set.

### 4. Identify Taste Patterns

Focus on restaurant/food domain items with 2+ signals (repeat visits = pattern evidence):

- **Cuisine patterns**: Aggregate by cuisine tag, sort by total effective strength. Top 5 cuisines = taste profile.
- **Price comfort zone**: Distribution of `price_level` across top items. Most cluster at 1–2 ($$).
- **Frequency signals**: Items with 5+ signals are strong favorites. Reference them by name in the recommendation.
- **Cross-domain bridges**: If cuisine clusters overlap with price/spend patterns, note the intersection (e.g., "Indian at $$" + "Mediterranean at $$$ for special occasions" → candidate is elevated Indian).

### 5. Find Candidate Restaurants

Search Eater SF, Michelin Guide, or local food guides for the top cuisine pattern(s). Cross-reference every candidate against the visited set.

Reliable SF sources:
- `sf.eater.com/maps/best-X-restaurants-san-francisco` — updated ~annually
- `guide.michelin.com/us/en/california/san-francisco/restaurants/X` — for high-end
- Use `curl` to `r.jina.ai/<url>` for page extraction from VPS
- Use SearXNG `http://localhost:8888/search?q=...` for discovery searches

### 6. Select and Format

Pick the candidate that:
- Matches the strongest cuisine pattern
- Fits the price comfort zone (or is a justified step up)
- Has strong external validation (Michelin, Eater inclusion, 4.0+ rating)
- Is NOT in the visited set

Format per `recommendation_style.md`:
1. Restaurant name + location
2. Evidence paragraph: name specific prior venues, visit counts, spend data
3. Pattern statement ("You eat X regularly" / "You go to Y for elevated dinners")
4. What to order (from external reviews)
5. Confirmation it's new (not in signal history)
6. Caveats (price, format, etc.)

## Tips

- Use `terminal()` with heredoc (`python3 << 'PYEOF'`) for inline analysis, not `execute_code` (may be blocked on VPS)
- `visited` set should include ALL items, not just enriched ones — calendar signals count too
- If a candidate's name partially matches a visited venue, flag for manual review rather than silently dropping
- Always check `config.json > user_preferences > dietary_restrictions` before finalizing
- When cross-referencing visited names, do fuzzy matching — the same restaurant may appear under slightly different names in items.jsonl vs. external sources
- External search from VPS: avoid Yelp/Reddit (403), prefer news sites, Eater, Michelin, restaurant homepages