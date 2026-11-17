# Changelog

## [3.7.0] - 2026-09-16

### Added
- **Local skillgrade eval runner** — integrate `skillgrade` CLI for local offline evaluation of a skill's `eval.yaml` suite before submitting variants; gates candidate patches prior to formal `ocas-fellow` benchmarking. Note a missing `eval.yaml` in the critique rather than skipping evaluation.