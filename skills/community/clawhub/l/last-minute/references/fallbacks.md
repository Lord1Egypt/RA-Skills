# Fallbacks — Flight Category (Last Minute)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
# Tell user: "Please run npm i -g @fly-ai/flyai-cli manually."
```

## Case 1: No Same-Day Flights Found

```bash
# Step 1 → Remove hour filter
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 6
# Step 2 → Try tomorrow
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --sort-type 6
# Step 3 → Expand to 3-day window
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {today} --dep-date-end {today+3} --sort-type 6
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} last minute flights"
```

## Case 2: Same-Day Flights Over Budget

```bash
# Relax budget 30%
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --max-price {budget*1.3} --sort-type 6
# Try connecting flights (may be cheaper)
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --max-price {budget} --sort-type 3
# Try tomorrow
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {tomorrow} --max-price {budget} --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX, "Osaka" → KIX/ITM, "Seoul" → ICN/GMP
→ Ask user which airport
```

## Case 4: Invalid Date (Past Date)

```
→ Do NOT search. "This date has passed."
→ Auto-search today or next available date
```

## Case 5: Parameter Conflict / Invalid Argument

**Trigger:** CLI returns error containing "invalid", "conflict", or non-zero exit code.

```bash
# Step 1 → Retry with minimum required params only
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 6

# Step 2 → Fallback to broad search
flyai keyword-search --query "{origin} to {destination} urgent flights today"

# Step 3 → Still fails → report error honestly with raw command for debugging
```

## Case 6: API Timeout / Network Error

**Trigger:** CLI hangs >30s or returns network error.

```bash
# Step 1 → Retry once
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {today} --sort-type 6

# Step 2 → Simplify query (fewer params = faster)
flyai keyword-search --query "{origin} to {destination} last minute flights"

# Step 3 → Still timeout → report honestly. Do NOT substitute with training data.
```
