# Fallbacks — Trip Planning Category

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli && flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: Flight Search Failed

```bash
flyai search-flight ... --dep-date-start "{date-7}" --dep-date-end "{date+7}" --sort-type 3
flyai search-flight ... --destination "{alt_city}" --sort-type 3
```

## Case 2: Hotel Search Failed

```bash
flyai search-hotel --dest-name "{city}" --sort rate_desc  # Remove filters
flyai search-hotel --dest-name "{nearby}" --sort rate_desc
```

## Case 3: Partial Failure in Multi-Command

```
→ Show successful parts normally
→ Mark failed: "⚠️ {section} data unavailable"
→ Provide manual CLI command for retry
```

## Case 4: Parameter Conflict

```bash
flyai keyword-search --query "{user request}"
```

## Case 5: API Timeout

```
Retry once → Simplify → Report honestly.
```
