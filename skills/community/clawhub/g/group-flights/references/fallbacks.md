# Fallbacks — Flight Category (Group)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
# Tell user: "Please run npm i -g @fly-ai/flyai-cli manually."
```

## Case 1: No Flights for Group Date

```bash
# Step 1 → Flexible dates ±7 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-7}" --dep-date-end "{date+7}" --sort-type 2
# Step 2 → Remove journey-type filter
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
# Step 3 → Try nearby airports
flyai search-flight --origin "{nearby_o}" --destination "{d}" --dep-date {date} --sort-type 2
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} group flights"
```

## Case 2: All Flights Over Budget

```bash
# Relax budget 30% per ticket
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --max-price {budget*1.3} --sort-type 3
# Try connecting flights (usually cheaper)
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --max-price {budget} --sort-type 3
# Try flexible dates
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-7}" --dep-date-end "{date+7}" --max-price {budget} --sort-type 3
```

## Case 3: Ambiguous City

```
"Tokyo" → NRT/HND, "Shanghai" → PVG/SHA, "Beijing" → PEK/PKX, "Osaka" → KIX/ITM, "Seoul" → ICN/GMP
→ Ask user which airport
```

## Case 4: Invalid Date

```
→ Do NOT search. "This date has passed."
→ Auto-search next available date
```

## Case 5: Parameter Conflict / Invalid Argument

**Trigger:** CLI returns error containing "invalid", "conflict", or non-zero exit code.

```bash
# Step 1 → Retry with minimum required params only
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2

# Step 2 → Fallback to broad search
flyai keyword-search --query "{origin} to {destination} group flights"

# Step 3 → Still fails → report error honestly with raw command for debugging
```

## Case 6: API Timeout / Network Error

**Trigger:** CLI hangs >30s or returns network error.

```bash
# Step 1 → Retry once
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2

# Step 2 → Simplify query (fewer params = faster)
flyai keyword-search --query "{origin} to {destination} group flights"

# Step 3 → Still timeout → report honestly. Do NOT substitute with training data.
```
