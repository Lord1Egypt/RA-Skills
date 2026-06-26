# Smoke Test

## Preconditions

- `python3` available
- run from skill root

## Test Cases

### 1. Basic single engine
```bash
python3 scripts/build_search_urls.py --query "openclaw"
```
Expected:
- exit code 0
- outputs one URL
- default engine is valid

### 2. Compare mode
```bash
python3 scripts/build_search_urls.py --query "react hooks" --compare google,ddg,brave --format json
```
Expected:
- exit code 0
- JSON array/object returned
- 3 engine entries

### 3. Operator composition
```bash
python3 scripts/build_search_urls.py --query "retrieval augmented generation" --site arxiv.org --filetype pdf --time year
```
Expected:
- URL contains encoded `site:arxiv.org`
- URL contains encoded `filetype:pdf`

### 4. Preset
```bash
python3 scripts/build_search_urls.py --query "privacy tools" --preset privacy
```
Expected:
- multiple privacy engines selected

### 5. Unknown engine failure
```bash
python3 scripts/build_search_urls.py --query "x" --engine not-real
```
Expected:
- non-zero exit
- clear error message

### 6. WolframAlpha route
```bash
python3 scripts/build_search_urls.py --query "100 USD to CNY" --engine wolframalpha
```
Expected:
- URL uses WolframAlpha template
