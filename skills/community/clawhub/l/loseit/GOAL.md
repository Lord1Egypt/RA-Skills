# GOAL — rewrite loseit-cli in Go as a "dumb" data collector

> Implementation spec for `/goal`. Do the work on a branch; **do not push/tag/merge to `main` or
> publish to ClawHub without the owner's explicit OK** (see §13). `main` is PR-protected.

## 0. Mission — two changes at once, plus CI/ClawHub

1. **Complete Python → Go changeover.** A single self-contained Go binary; no Python runtime. Delete the
   Python package once ported.
2. **Make it "dumb."** Today loseit-cli *writes* `DAILY_LOG.json`. Stop. The Go tool **reads the Lose It
   export and emits per-day nutrition as JSON** — and nothing else. The consumer (**personal-workout-ai**)
   does the storing.
3. **Add the full CI / release / ClawHub setup** (this repo has none yet).

This is the exact transformation already completed for **`google-health-cli`** — it is your **gold-standard
template** (§2). Mirror it.

## 1. Toolchain (Go is NOT on PATH on this machine)

```powershell
$env:Path = "C:\Users\gates\go-sdk\go\bin;C:\Users\gates\go\bin;$env:Path"
```
Helpers (`gofumpt`, `goimports`, `golangci-lint`, `goreleaser`) are in `C:\Users\gates\go\bin`.
Run `make check` before committing. Install the finished binary to **`C:\Users\gates\bin\loseit-cli.exe`**
(on PATH, alongside `speediance-cli.exe` and `google-health-cli.exe`).

## 2. Reference implementation — STUDY `google-health-cli` FIRST

`C:\Users\gates\Personal\google-health-cli` is the finished version of this exact pivot. Before writing
code, read its: `CLAUDE.md`, `AGENTS.md`, `RELEASING.md`, `.github/workflows/{ci,release,publish-clawhub}.yml`,
`.goreleaser.yaml`, `.golangci.yml`, `SKILL.md`, `Makefile`, and `internal/` layout. **Mirror its conventions:**
thin `cmd/` entrypoint owning the ldflags vars; cobra "one file per command"; `App` struct + global flags +
stderr logger; **stdout = data, stderr = hints/logs**; a `writeJSON` helper with `SetEscapeHTML(false)` +
2-space indent + trailing newline; config discovery precedence; `internal/version` + `version.Set(...)`.
Copy its CI/release/ClawHub files near-verbatim, changing only the binary name, module path, and the
ClawHub slug/name.

## 3. Identity & the dumb-collector rule

loseit-cli (Go) is a **read-only nutrition extractor**: it obtains the Lose It export (downloaded ZIP or a
cookie fetch), parses it, and **emits per-day nutrition as JSON**. It has **no** knowledge of `DAILY_LOG.json`,
no `sync`, no upsert, no write path. Read-only use of the user's own Lose It data.

## 4. Command surface (Go)

- **`days`** (the core emit) — parse the export and print per-day nutrition. Flags: `--zip PATH`,
  `--date today|yesterday|YYYY-MM-DD` (default today), `--days N` (default 7), `--json`. Human table by
  default; `--json` emits the frozen JSON contract (§5). Mirror google-health's `sessions` command shape.
- **`config show|path`** — inspect the resolved config (mirror google-health).
- **`version`** (+ root `--version`), **`completion bash|zsh|fish|powershell`**.
- *(optional)* **`doctor`** — report config path, `export_url`, and whether a token is present / `--zip`
  is needed. No network required (there is no OAuth to validate).
- **REMOVE `sync` entirely** (and everything that wrote `DAILY_LOG.json`).
- **No `login` command** — the `liauth` cookie is grabbed from the browser manually; the tool just reads it.

## 5. Data contract — `days --json` (FROZEN)

A JSON object keyed by ISO date → nutrition object. Key order frozen:

```json
{
  "2026-06-16": {
    "source": "Lose It export",
    "calories_food": 505,
    "protein_g": 75,
    "carbs_g": 36,
    "fat_g": 6,
    "fiber_g": 3,
    "meals": [
      { "meal": "Breakfast", "calories": 225, "protein_g": 23, "carbs_g": 36, "fat_g": 0,
        "items": [ { "name": "Greek Yogurt", "qty": "1 cup", "calories": 120 } ] }
    ],
    "loseit_budget": 1663,
    "loseit_under": 1158,
    "exercise_adjustment": 120
  }
}
```

`loseit_budget` / `loseit_under` / `exercise_adjustment` appear **only** when `daily-calorie-summary.csv`
provides them, and **after** `meals`. Empty result → `{}`.

**Parity gotchas — match the Python (`loseit/nutrition.py`) exactly:**
- **Rounding is round-half-to-even.** Python `round()` is banker's rounding → use `math.RoundToEven`. Sum
  the raw floats across rows first, **then** round each total (day totals and per-meal totals each round the
  summed float; do NOT sum pre-rounded values). `item.calories = RoundToEven(row Calories)`. The validated
  numbers depend on this.
- **Deleted filter:** skip a row when `Deleted` ∈ {`true`,`1`,`yes`} (case-insensitive).
- **Date normalization:** try `2006-01-02`, `01/02/2006`, `01/02/06`, `2006/01/02` → ISO; unparseable → skip.
- **Meal order:** `Breakfast, Lunch, Dinner, Snacks` first (that order), then any other meals in
  first-encounter order. Meal name defaults to `Other` when blank.
- **`qty`** = `Quantity` + " " + `Units`, skipping empty parts.
- **CSV:** UTF-8 **BOM-stripped** (`utf-8-sig`); header-keyed rows (like `csv.DictReader`).
- **JSON:** HTML-escaping OFF, indent 2, trailing newline.

## 6. Auth / export model (preserve both paths)

1. **`--zip PATH`** — read a downloaded export ZIP, no token. Validate it starts with `PK`.
2. **Cookie fetch** — `GET export_url` with headers `Cookie: liauth=<t>; fn_auth=<t>` and a `User-Agent`;
   token from `LOSEIT_TOKEN` env or the `token_path` file (default `~/.config/loseit/token`). Validate the
   response is a ZIP (`len>1000` && starts `PK`); otherwise error: token probably expired.

Export ZIP contents: `food-logs.csv` (cols: `Date,Name,Icon,Meal,Quantity,Units,Calories,Deleted,Fat (g),
Protein (g),Carbohydrates (g),Saturated Fat (g),Sugars (g),Fiber (g),Cholesterol (mg),Sodium (mg)`) and
`daily-calorie-summary.csv` (`Date,Food cals,Exercise cals,Budget cals,EER`).

**The wrinkle (document prominently):** the `liauth` cookie **expires with no auto-refresh**. So for
hands-off/agent use the reliable path is `--zip` with a freshly downloaded export. Surface this honestly in
README / SKILL / the personal-workout-ai docs.

## 7. Config

- **Discovery** (mirror google-health): `--config` flag > `LOSEIT_CONFIG` env > `./config.json` >
  next-to-exe. `config.json` is **optional** (the defaults below work).
- **Keys (drop `daily_log`):** `token_path` (default `~/.config/loseit/token`), `export_url`
  (default `https://www.loseit.com/export/data`).
- **Env:** `LOSEIT_TOKEN` (cookie value), `LOSEIT_CONFIG`. (Optionally `LOSEIT_EXPORT_URL`,
  `LOSEIT_TOKEN_PATH`.)
- Update `config.example.json` to drop `daily_log`. `.gitignore`: `config.json`, `token`, `*.zip`, `/bin`,
  `/dist`, `*.exe`.

## 8. Project layout (Go) — mirror google-health-cli

```
cmd/loseit-cli/main.go          thin entrypoint; ldflags vars (versionString/commit/date) -> version.Set; exit codes
internal/cli/                   cobra commands: days, config, version, completion (+ optional doctor); root.go; exit.go; output.go
internal/export/                token read, cookie fetch (net/http), --zip read, ZIP open (archive/zip), CSV read (encoding/csv, BOM strip); typed Error -> exit 2
internal/nutrition/             per-day aggregation (the §5 contract); RoundToEven
internal/config/                discovery + precedence
internal/version/               version package
testdata/                       fixtures (synthetic export) + golden (days --json)
```
- **Module:** `github.com/stozo04/loseit-cli`. **`go` directive: `go 1.24`** (no external deps — pure
  stdlib — so keep it at 1.24; this lets the simple lint recipe in §10 work).

## 9. Tests — port `tests/test_offline.py` to Go

Build a synthetic export ZIP in-test (as the Python does) and assert the **exact** ported values:
- `2026-06-16`: `calories_food` 505, `protein_g` 75, `fiber_g` 3, `carbs_g` 36, `source` "Lose It export";
  the deleted 999-cal row excluded.
- `meals` == `[Breakfast, Lunch]`; Breakfast `calories` 225; Breakfast items {Greek Yogurt, Banana}.
- `loseit_budget` 1663, `loseit_under` 1663−505, `exercise_adjustment` 120.

Add a `days --json` **golden** over the fixture, with an `UPDATE_GOLDEN=1` regeneration path (mirror
google-health's `assertGolden`). **Do NOT port the `test_upsert_*` tests** — that write path is removed; its
logic moves to personal-workout-ai (§11C).

## 10. CI / release / ClawHub (the repo has NONE — add all of it)

Copy google-health-cli's files near-verbatim; change binary name / module / slug. **Hard-won lessons baked
in so you don't refight them:**

- **`.github/workflows/ci.yml`** — build + `test -race` + golangci-lint. Use `actions/checkout@v6` +
  `actions/setup-go@v6` (no Node-20 warnings). **golangci-lint gotcha:** golangci-lint **v2** needs
  `golangci-lint-action` **≥ v7** (v6 errors "invalid version string"), AND the golangci-lint release binary
  must be built with a Go **≥ the module's `go` directive** or it refuses to lint. Two proven recipes:
  - **speediance-cli** (`go 1.24`): `golangci-lint-action@v9` + `actions/setup-go@v6` with
    `go-version-file: go.mod` (pins the runner Go to 1.24, matching the prebuilt golangci-lint binary).
    **Use this one** — loseit targets `go 1.24`, so it's the simplest and needs no source build.
  - google-health-cli (`go 1.25`): `golangci-lint-action@v7` + `install-mode: goinstall`. Only needed if a
    dep ever forces `go ≥ 1.25`.
  Reuse google-health's **`.golangci.yml`** verbatim (default: standard + revive/gosec/misspell/bodyclose/
  errorlint/nilnil; gofumpt+goimports formatters) — just set `local-prefixes` to the loseit module.
- **`.github/workflows/release.yml`** — copy google-health's: GoReleaser on `v*` tags **plus
  `workflow_dispatch`** with a `version` input that validates + creates/pushes the tag at HEAD (a tag pushed
  with `GITHUB_TOKEN` does not double-trigger). One-button releases from the Actions UI.
- **`.goreleaser.yaml`** — copy google-health's: 6 targets (linux/darwin/windows × amd64/arm64), ldflags
  `-X main.versionString/commit/date`, archives (tar.gz + Windows zip) bundling `README.md AGENTS.md SKILL.md
  LICENSE` + `checksums.txt`, `prerelease: auto`, github changelog. Change `binary: loseit-cli`,
  `main: ./cmd/loseit-cli`.
- **`.github/workflows/publish-clawhub.yml`** — copy google-health's; trigger on `SKILL.md`→`main` +
  `workflow_dispatch`; `clawhub skill publish . --owner stozo04 --slug <slug> --name "<name>"`.
- **`SKILL.md`** — frontmatter mirrors google-health/speediance: `name: <slug>`, an emoji (🥗 / 🍎),
  `homepage`, `primaryEnv: LOSEIT_TOKEN`, permissions (**network:** loseit.com export endpoint; **files.read:**
  config.json / token / `--zip` file; **files.write: the session-token cache only (`token_path`, 0600) —
  it is a credential, so declare it; do not claim "writes nothing"**), `requires`/`envVars`
  (`LOSEIT_TOKEN` optional; `--zip` is the no-token path). Body: setup, the **cookie-expiry wrinkle**, command
  reference, conventions, `days --json` sample. Be honest that headless use means supplying `--zip` with a
  fresh export.
- **`RELEASING.md`** — copy google-health's (semver; dispatch + manual-tag paths; verification; the separate
  ClawHub publish).
- **`AGENTS.md`** — machine contract: exit codes (`0` ok, `2` export/parse failure, `64` usage, `78` config),
  the `days --json` shape (§5), `config show --json` shape.
- **`Makefile`** — copy google-health's (build/test/test-race/lint/fmt/vet/check; `golden` via `UPDATE_GOLDEN`).
- **Branch protection (owner step, after the first PR's CI runs once):** require a PR + required status
  checks (the CI job names — likely `build & test` and `lint`) + block force-push/deletion. The exact
  `gh api` PUT recipe is in google-health-cli's history; **use the check-run names that actually appear on
  the first PR** (a wrong name locks the branch).

**Owner steps to flag (you can't do these):** (a) confirm the ClawHub **slug + display name** — proposed
`slug: loseit`, `name: "Lose It Nutrition"`; (b) add a **`CLAWHUB_TOKEN`** repo secret to *this* repo
(per-repo — the google-health one does not carry over).

## 11. Install + personal-workout-ai contract (load-bearing — the agent now stores nutrition)

> **Scope note (security):** Everything in §11 below describes the **consumer**
> (`personal-workout-ai`), **not** loseit-cli. loseit-cli never touches
> `DAILY_LOG.json`. The `DAILY_LOG.json` write happens in the consuming agent, **in
> response to the user's own action** (Steven logging food or dropping a fresh
> export) — it is user-initiated, not autonomous, and it only sets the day's
> `nutrition` key, never clobbering `training` / `body` / `watch` / `final_note`.

**A. Install the binary** to a directory on `PATH` (e.g. `$HOME/bin/loseit-cli`). Verify
`loseit-cli days --zip <export.zip> --json` emits the §5 contract.

**B. Update personal-workout-ai docs** (`C:\Users\gates\Personal\personal-workout-ai`). Grep for
`python -m loseit` and `loseit sync` and fix **every** hit — `CLAUDE.md` (the daily-loop step, the
Tracking-tools loseit bullet, the `DAILY_LOG.json` file-map line), `PROJECT_INSTRUCTIONS.md` (loseit
tracking bullet + the weekly-pull block), `PROGRAM.md` if referenced. New model, mirroring how the
google-health cardio bullet was rewritten ("the CLI only emits data — you do the storing"): when Steven logs
food, the agent runs **`loseit-cli days --zip <export> --json`** (or the cookie path), takes the per-day
nutrition, and **writes it into `DAILY_LOG.json` itself**.

**C. The nutrition-storage procedure (moved from `loseit/daily_log.py` into the agent's instructions):**
- Set `days[<date>].nutrition = <nutrition object from loseit-cli>`.
- If the day is missing, create it **in date order** with the skeleton:
  `{ "date": <iso>, "weekday": <Mon..Sun from the date>, "partial": true, "nutrition": <obj>,
     "body": {"weight_lb": null, "waist_in": null}, "watch": {"sleep_hrs": null, "resting_hr": null, "steps": null} }`.
- **Never clobber other keys** on the day (`training`, `final_note`, `body`, `watch`) — only set `nutrition`.
  Lose It is the source of truth for nutrition, so overwriting the day's `nutrition` on re-import is the
  correct, idempotent behavior.
- Preserve `DAILY_LOG.json` key order + line endings on write (same care the agent already uses for cardio).

**D. The wrinkle:** the `liauth` cookie expires with no refresh, so the agent usually can't pull headlessly —
the reliable path is Steven dropping a fresh export ZIP and the agent running `loseit-cli days --zip <path>
--json`. Document this so the agent doesn't chase a dead cookie.

## 12. Definition of done

- [ ] Python sources removed (`loseit/`, `pyproject.toml`; `tests/test_offline.py` ported) and the Go tree in
      place — on a `rewrite-in-go` branch, one PR (so `main` is never half Python / half Go).
- [ ] `loseit-cli days --zip <fixture> --json` matches §5; golden + ported assertions pass (505 / 75 / 3 / 36;
      meals; budget/under/exercise).
- [ ] `make check` green: build, vet, golangci-lint (0 issues), `gofumpt -l` empty, `go test -race`.
- [ ] No `DAILY_LOG` / `sync` / write path anywhere in the Go tree.
- [ ] CI + release + ClawHub workflows added; `goreleaser check` passes; version stamping verified via an
      ldflags test build.
- [ ] Binary installed to `C:\Users\gates\bin`; works from any directory (cookie at `~/.config/loseit/token`
      or `--zip`).
- [ ] personal-workout-ai docs updated — zero stale `python -m loseit` / `loseit sync` refs; the agent now
      pulls + stores nutrition.
- [ ] `SKILL.md` written; ClawHub slug/name + `CLAWHUB_TOKEN` secret confirmed/added by the owner.
- [ ] Live check: run against a real, fresh Lose It export and confirm the parsed numbers are right.

## 13. Guardrails

- **Never** `git push`, tag, merge to `main`, or `clawhub publish` without the owner's explicit OK. `main` is
  PR-protected. Prepare everything, then stop and ask.
- Don't commit `config.json`, the token file, or `*.zip` exports. Never print the `liauth` cookie.
- The ClawHub **slug/name** and the **`CLAWHUB_TOKEN`** secret are owner decisions/steps — flag them.
- Verify the **round-half-to-even** parity against the Python's validated numbers before declaring done.
