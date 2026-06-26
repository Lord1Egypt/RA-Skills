# CLI Contracts

`privacy-protector` has three primary CLI surfaces:

- `scripts/anonymize.py`
- `scripts/deanonymize.py`
- `scripts/detect_local.py`

## `anonymize.py`

Primary flags:

- `--input`: literal text or supported file path
- `--level`: `lite`, `dynamic`, `strict`, `crossborder`
- `--sender-code` and `--recipient-code`: required for `crossborder`
- `--json`: emit machine-readable contract
- `--output`: explicit output path
- `--in-place`: overwrite file input

JSON envelope:

- top level: `success`, `tool`, `mode`, `level`, `data`
- `data` may include:
  - `anonymizedContent`
  - `hasPII`
  - `inputType`
  - `inputPath`
  - `mapRef`
  - `outputPath`
  - `warnings`
  - `applyReport`
  - `verificationReport`
  - `assurancePolicy`

## `deanonymize.py`

Primary flags:

- `--input`: anonymized text or supported file path
- `--map`: explicit map file or map ID
- `--output`: explicit output path
- `--in-place`: overwrite file input
- `--json`: emit machine-readable contract

Map resolution order when `--map` is omitted:

1. Embedded marker in `.txt` / `.md` / `.markdown` (`privacy-protector-map-id`, with legacy `modeio-redact-map-id` still accepted)
2. Sidecar `.map.json`
3. Latest local map fallback for literal text input only

## `detect_local.py`

Primary flags:

- `--profile`: `strict`, `balanced`, `precision`
- `--allowlist-file`
- `--blocklist-file`
- `--thresholds-file`
- `--json`
- `--explain`

JSON payload fields:

- `originalText`
- `sanitizedText`
- `items`
- `riskScore`
- `riskLevel`
- `profile`
- `thresholds`
- `scoringMethod`
- `detectorVersion`
- `stats`
