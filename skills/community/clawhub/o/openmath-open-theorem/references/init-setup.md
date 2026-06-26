# Init Setup

## Overview

Triggered when:

1. No `openmath-env.json` found in `./.openmath-skills/` or `~/.openmath-skills/` -> full discovery setup
2. `openmath-env.json` found but `preferred_language` is missing -> language selection only

This is a hard gate. Until setup is complete, do not call the OpenMath theorem list, theorem detail, or download APIs.

## Setup Flow

```text
No project/global config found        Config found, preferred_language missing
            |                                       |
            v                                       v
  +------------------------+              +------------------------+
  | AskUserQuestion        |              | AskUserQuestion        |
  | (full setup)           |              | (language only)        |
  +------------------------+              +------------------------+
            |                                       |
            v                                       v
  +--------------------------+            +--------------------------+
  | Create openmath-env.json |            | Update openmath-env.json |
  +--------------------------+            +--------------------------+
            |                                       |
            v                                       v
  +------------------------+              +------------------------+
  | Run check_openmath_env |              | Run check_openmath_env |
  +------------------------+              +------------------------+
            |                                       |
            v                                       v
         Continue                                Continue
```

## Flow 1: No `openmath-env.json` (Full Discovery Setup)

**Language**: Use the user's input language or saved conversation language preference.

Use AskUserQuestion with all questions in one call:

### Question 1: Preferred Language

```yaml
header: "Language"
question: "Preferred OpenMath theorem language?"
options:
  - label: "Lean (Recommended)"
    description: "Best default if the user is solving OpenMath Lean problems"
  - label: "Rocq"
    description: "Use Rocq theorems and Rocq scaffolds by default"
```

### Question 2: Save Location

```yaml
header: "Save"
question: "Where should OpenMath preferences be saved?"
options:
  - label: "Project (Recommended)"
    description: "./.openmath-skills/openmath-env.json, only for the current repository"
  - label: "User"
    description: "~/.openmath-skills/openmath-env.json, reused across repositories"
```

Do not ask about submission identity fields here unless the user explicitly wants end-to-end submission in the same request.

### Save Locations

| Choice | Path | Scope |
|--------|------|-------|
| Project | `./.openmath-skills/openmath-env.json` | Current repository / workspace only |
| User | `~/.openmath-skills/openmath-env.json` | Reused across repositories |

### `openmath-env.json` Template

```json
{
  "preferred_language": "lean"
}
```

After the user answers:

1. Create the target directory if needed
2. Create `./.openmath-skills/` if needed, then write `openmath-env.json`
3. Confirm where it was saved
4. Run `python3 scripts/check_openmath_env.py`
5. Only after `Status: ready`, continue with theorem discovery

## Flow 2: Config Exists, `preferred_language` Missing

Ask only the missing language question.

### Question: Preferred Language

```yaml
header: "Language"
question: "Preferred OpenMath theorem language?"
options:
  - label: "Lean (Recommended)"
    description: "Use Lean theorems and Lean scaffolds by default"
  - label: "Rocq"
    description: "Use Rocq theorems and Rocq scaffolds by default"
```

After the user answers:

1. Update the existing `openmath-env.json` in place
2. Run `python3 scripts/check_openmath_env.py`
3. Only after `Status: ready`, continue

## Runtime Defaults

Runtime endpoint settings are not stored in `openmath-env.json`.

Defaults:

- `OPENMATH_SITE_URL`: `https://openmath.shentu.org`
- `OPENMATH_API_HOST`: `https://openmath-be.shentu.org`

Only mention these environment variables when the user explicitly wants endpoint overrides.

## After Setup

Expected behavior after setup:

1. `python3 scripts/check_openmath_env.py` returns `Status: ready`
2. `python3 scripts/fetch_theorems.py` uses `preferred_language` by default when no explicit language is passed
3. If `preferred_language` is `lean`, it queries only Lean; if it is `rocq`, it queries only Rocq
4. If the configured language has no open theorems, report that result and stop instead of querying the other language automatically
5. `python3 scripts/fetch_theorem_detail.py` and `python3 scripts/download_theorem.py` are allowed to continue
6. If the config is missing again in another workspace, repeat this flow instead of guessing

## Notes

- User-facing and API language naming is `rocq`
- Do not treat “no theorem found for the configured language” as permission to query the other language
- Do not ask about endpoint overrides during normal setup
- Do not force authz setup during theorem discovery unless the user explicitly asks to submit proofs too
