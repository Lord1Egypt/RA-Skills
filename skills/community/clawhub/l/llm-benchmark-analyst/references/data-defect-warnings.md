# Data Defect Warnings

Use these warnings inline whenever the affected benchmark appears. Then summarize them again in the report's limitations or confidence section.

## Severity labels
- **critical data warning**: do not treat the benchmark as decisive on its own
- **high caution**: useful as one signal, but avoid strong ranking claims from small gaps
- **medium caution**: usable with caveats; avoid over-reading tiny deltas

## Benchmark-specific warnings

### swe-bench verified
- Severity: critical data warning
- Prefer instead: SWE-bench Pro when available
- Ready wording: `critical data warning: swe-bench verified has published concerns about contamination and test-design defects; prefer swe-bench pro when available and do not treat small gaps here as decisive.`

### τ²-bench (original)
- Severity: high caution
- Prefer instead: τ²-Bench-Verified when available
- Ready wording: `high caution: the original τ²-bench has published issues around policy alignment, database accuracy, logic consistency, and evaluation ambiguity; prefer τ²-bench-verified when possible.`

### mmlu-pro
- Severity: high caution
- Ready wording: `high caution: mmlu-pro has published answer-format vulnerabilities, including whitespace and answer-length artifacts, so treat small score gaps with caution.`

### gpqa diamond
- Severity: critical data warning
- Ready wording: `critical data warning: gpqa diamond has published forensic concerns about OCR and data-entry quality; use it as weak evidence and avoid strong conclusions from fine-grained score gaps.`

### humanity's last exam (hle)
- Severity: critical data warning
- Ready wording: `critical data warning: humanity's last exam has published forensic concerns about OCR and data-entry quality; do not rely on it as a sole measure of scientific frontier ability.`

### aa-omniscience
- Severity: high caution
- Ready wording: `high caution: aa-omniscience has published community concerns about question quality, so use it as one signal rather than a decisive ranking source.`

### algotune
- Severity: medium caution
- Ready wording: `medium caution: algotune can understate expensive models because of the benchmark's api cost cap and its awkward tool-call format, so part of the score may reflect benchmark mechanics rather than pure capability.`

## Global warning patterns

### hf open-llm-leaderboard / lm-evaluation-harness whitespace issue
- Severity: high caution
- Apply when: a reported score comes from HF Open-LLM-Leaderboard-era evaluations or clearly depends on affected harness settings
- Ready wording: `high caution: some historical open-llm-leaderboard-style results were affected by a whitespace-selection bug in the evaluation harness, so legacy scores may not be strictly comparable.`

### agentic coding infrastructure noise
- Severity: medium caution
- Apply when: interpreting small deltas on terminal, tool-use, or agentic coding benchmarks
- Ready wording: `medium caution: agentic coding benchmarks can move by several points because of infrastructure and environment differences, so very small gaps are not decisive.`

### visual benchmark instability
- Severity: medium caution
- Apply when: the benchmark is small, annotation-sensitive, or visibly unstable to formatting/compression changes
- Ready wording: `medium caution: some multimodal rankings are sensitive to data size, annotation style, or even image-format details, so small ranking shifts should not be over-interpreted.`

### image-extracted leaderboard rows
- Severity: medium caution
- Apply when: the score was read from a screenshot or chart rather than machine-readable text
- Ready wording: `medium caution: this row was extracted from an image-rendered leaderboard, so transcription risk is higher than for machine-readable tables.`

## Confidence downgrade rule
Downgrade the overall report confidence when:
- a core conclusion depends on one or more `critical data warning` benchmarks
- most evidence is vendor-reported rather than official
- most decisive rows are image-extracted
- the exact model version or benchmark variant could not be matched cleanly
