# Fallbacks — Flight Category (Infant)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
# Tell user: "Please run npm i -g @fly-ai/flyai-cli manually."
```

## Case 1: No Flights in Infant-Friendly Hours

```bash
# Step 1 → Expand hour window to 5-22
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 5 --dep-hour-end 22 --sort-type 4
# Step 2 → Remove hour filter entirely
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 4
# Step 3 → Try flexible dates ±3 days
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --dep-hour-start 6 --dep-hour-end 20 --sort-type 4
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} flights with baby"
```

## Case 2: All Flights Over Budget

```bash
# Relax budget 30%
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --dep-hour-start 6 --dep-hour-end 20 --max-price {budget*1.3} --sort-type 3
# Try connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --max-price {budget} --sort-type 3
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
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 4

# Step 2 → Fallback to broad search
flyai keyword-search --query "{origin} to {destination} flights"

# Step 3 → Still fails → report error honestly with raw command for debugging
```

## Case 6: API Timeout / Network Error

**Trigger:** CLI hangs >30s or returns network error.

```bash
# Step 1 → Retry once
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 4

# Step 2 → Simplify query
flyai keyword-search --query "{origin} to {destination} flights"

# Step 3 → Still timeout → report honestly. Do NOT substitute with training data.
```
