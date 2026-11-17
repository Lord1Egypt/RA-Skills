# Changelog

## v1.2.0

Security-focused release: model output is now treated as untrusted data at every stage.

- **Unique per-run temp files** — the workflow generates a `run_id` and writes every payload to `mdls-{run_id}-*.json` in a private temp location. Concurrent runs can no longer collide, and predictable shared `/tmp` names (a symlink hazard) are gone.
- **Injection-resistant judge prompt** — each blind response is wrapped in explicit BEGIN/END delimiters and the judge is instructed to treat response content as untrusted data. Embedded "score me 10/10" / "ignore previous instructions" attempts are scored down, not obeyed.
- **Constrained context fetching** — the orchestrator only fetches URLs/files the *user* explicitly referenced, never links that appear inside model responses or judge output.
- **Clean JSON errors everywhere** — `judge_pipeline.py` validates payloads and reports every failure as `{"error": "..."}` with exit code 1 instead of a Python traceback; both scripts cap payloads at 64 MB.
- **Built-in self-test** — `python3 judge_pipeline.py --selftest` verifies the full anonymize → judge → finalize round trip.
- **No silent overwrites** — `save_results.py` uniquifies filenames when two runs save in the same minute.
- **Safer index pruning** — `update_modelshow_index.py` only ever deletes files matching the ModelShow result-name pattern, so pointing `--web` at a shared directory can't remove unrelated files; index timestamps are now true UTC.
- **Test suite** — `test_modelshow.py` (30 tests, stdlib-only) covers the pipeline, sanitization, hostile prompts, and CLI error paths. Run with `python3 -m unittest test_modelshow`.
- **Fixes** — model names containing regex replacement syntax no longer corrupt de-anonymization; the alias map is cached per process; the legacy `blind_judge_manager.py` shim now uses the same cryptographically secure shuffle (and is formally deprecated in favor of `judge_pipeline.py`).

## v1.1.0

- **Shell-injection hardening** — `judge_pipeline.py` and `save_results.py` accept `--file PATH` (and still read stdin), so payloads containing quotes, backticks, `$`, or newlines never touch a shell command line.
- **Deterministic ranking** — the judge emits a structured `scores` map and `finalize` ranks from it directly, falling back to prose regex only when absent.
- **>26 model guard** — anonymization auto-switches from alphabetic to numeric labels past 26 models.
- **Path-traversal safety** — `save_results.py` sanitizes the slug, resolves `output_dir`, and refuses to write outside it.
- **Per-criterion scores** — optional `judge_criteria` + per-result `criteria_scores` persisted to JSON/Markdown.
- **Per-run model override** — `mdls [grok,kimi,sonnet] <prompt>` compares just those models for one run.

## v1.0.1

- **Cryptographic shuffle** — `judge_pipeline.py` uses `secrets.SystemRandom()` for anonymization order, eliminating positional bias.
- **Holistic judge analysis** — the judge writes an "Overall Assessment" identifying cross-model patterns; `save_results.py` extracts this section separately.
- **Improved polling** — poll every 20s; exit immediately when all agents are done; minimum 3 polls before timeout.
- **Progress reporting rules** — explicit rules for what to send (status only) vs. never send (content) during polling.
- **judge_analysis_full** — JSON results store both the extracted assessment (`judge_analysis`) and the complete judge output (`judge_analysis_full`).

## v1.0.0

Initial release: parallel multi-model querying, blind anonymization, judge-based ranking, and Markdown/JSON result saving.
