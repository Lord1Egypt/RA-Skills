# Fallbacks — Flight Category (One-Way)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No One-Way Flights Found

```bash
# Step 1 → Flexible dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3
# Step 2 → Remove sort filter
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date}
# Step 3 → Nearby airports
flyai search-flight --origin "{nearby_o}" --destination "{d}" --dep-date {date} --sort-type 3
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} one-way flights"
```

## Case 2: All Flights Over Budget

```bash
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --max-price {budget*1.3} --sort-type 3
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX
→ Ask user which airport
```

## Case 4: Invalid Date

```
→ Do NOT search. "This date has passed."
```

## Case 5: Parameter Conflict

```bash
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3
flyai keyword-search --query "{origin} to {destination} one-way flights"
```

## Case 6: API Timeout

```bash
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 3
flyai keyword-search --query "{origin} to {destination} one-way flights"
# Still timeout → report honestly.
```
