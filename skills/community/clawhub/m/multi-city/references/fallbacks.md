# Fallbacks — Flight Category (Multi-City)

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli
flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: One Leg Has No Flights

```bash
# Retry failed leg with flexible dates
flyai search-flight --origin "{o}" --destination "{d}" --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 2
# Try connecting flights
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
# Try nearby airports
flyai search-flight --origin "{nearby_o}" --destination "{d}" --dep-date {date} --sort-type 2
```

## Case 2: Connection Time Too Short

```
→ Warn user: "两段之间中转时间不足3小时，可能存在误机风险"
→ Suggest later departure for second leg
```

## Case 3: Ambiguous City

```
→ Ask user which airport for each ambiguous city
```

## Case 4: Invalid Date Sequence

```
→ Do NOT search. "后续航段日期不能早于前一航段"
→ Ask user to correct date sequence
```

## Case 5: Parameter Conflict

```bash
# Retry each leg with minimum params
flyai search-flight --origin "{o}" --destination "{d}" --sort-type 2
```

## Case 6: API Timeout

```bash
# Retry failed leg only
flyai search-flight --origin "{o}" --destination "{d}" --dep-date {date} --sort-type 2
# If still timeout → keyword fallback for that leg
flyai keyword-search --query "{origin} to {destination} flights"
```
