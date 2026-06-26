# Fallbacks — Flight Category (Island Flight)

## Case 0: flyai-cli Not Installed

**Trigger:** `flyai --version` returns `command not found`.

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Fails → sudo npm i -g @fly-ai/flyai-cli
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Direct Island Flights

```bash
# Step 1 → Try connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --sort-type 2
# Step 2 → Try nearby mainland airport
flyai search-flight --origin "{o}" --destination "{nearby_mainland}" --dep-date {date} --sort-type 2
# Step 3 → Try date range
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {start} --dep-date-end {end} --sort-type 2
# Step 4 → Keyword search
flyai keyword-search --query "{origin} to {destination} island flights"
```

## Case 2: Island Route Over Budget

```bash
# Try off-peak dates
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start {off_start} --dep-date-end {off_end} --max-price {budget} --sort-type 3
# Try connecting
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --journey-type 2 --max-price {budget} --sort-type 3
```

## Case 3: Ambiguous City

```
"Shanghai" → PVG/SHA, "Sanya" → SYX, "Xiamen" → XMN
→ Ask user which airport
```

## Case 4: Invalid Date (Past Date)

```
→ Do NOT search. "This date has passed."
→ Auto-search next available date
```

## Case 5: Parameter Conflict / Invalid Argument

```bash
# Retry with minimum required params
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2
# Fallback
flyai keyword-search --query "{origin} to {destination} island flights"
# Still fails → report error honestly
```

## Case 6: API Timeout / Network Error

```bash
# Retry once
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
# Simplify
flyai keyword-search --query "{origin} to {destination} flights"
# Still timeout → report honestly
```
