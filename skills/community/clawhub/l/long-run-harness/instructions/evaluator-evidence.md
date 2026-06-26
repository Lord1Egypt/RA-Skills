# Evaluator Evidence Collector

Prefer deterministic evidence collection before LLM grading. The LLM should grade facts,
screenshots, DOM summaries, source excerpts, and command output; it should not be responsible
for discovering every relevant signal from scratch.

## Evidence Schema

For each sprint, write one canonical evidence JSON:

```text
harness-state/evidence/sprint-N/evidence.json
```

Suggested shape:

```json
{
  "sprint": 12,
  "goal": "...",
  "app_url": "http://localhost:3000",
  "commands": {},
  "navigation": {},
  "pages": {},
  "api": {},
  "screenshots": [],
  "viewport_checks": [],
  "axe": {},
  "lighthouse": {},
  "source_files": {},
  "git": {},
  "notes": []
}
```

## Default Browser Evidence

Collect:

- page URL, status, title
- full-page screenshot at 1440px
- viewport screenshots at 375, 768, 1440
- horizontal overflow status per viewport
- body text excerpt
- headings
- links/buttons/forms/inputs summary
- console errors/warnings
- network failures
- axe critical/serious violations
- Lighthouse summary when enabled

Store screenshots under:

```text
harness-state/evidence/sprint-N/screenshots/
```

Store axe/Lighthouse raw output under:

```text
harness-state/evidence/sprint-N/axe/
harness-state/evidence/sprint-N/lighthouse/
```

## Contract-Declared Evidence

Extend `SprintContract` with optional evidence hints:

```json
{
  "evidence": {
    "routes": ["/", "/api/auth/session"],
    "api": [
      {"method": "GET", "path": "/api/health/ready", "expectStatus": 200}
    ],
    "commands": [
      {"name": "build", "cmd": ["npm", "run", "build"]}
    ],
    "source_files": ["src/app/api/health/ready/route.ts"],
    "negative_tests": [
      "Missing required env should make readiness fail"
    ],
    "public_routes": []
  }
}
```

If no hints exist, derive routes from success criteria text, but keep derivation conservative.

## Source Evidence

Only include source excerpts needed to grade a criterion. Prefer:

- files explicitly listed in `evidence.source_files`
- files named in success criteria
- small excerpts around matched symbols

Do not dump the whole repo into evidence JSON.

Store copied/excerpted source evidence under:

```text
harness-state/evidence/sprint-N/source/
```

## API and Production Readiness Evidence

For production hardening sprints, include:

- `/api/auth/session` anonymous response
- `/api/health` and `/api/health/ready`
- expected failure cases: invalid auth, missing body, rate limit, bad token
- build output
- env contract check output
- logs redaction checks

Record raw responses under:

```text
harness-state/evidence/sprint-N/api/
harness-state/evidence/sprint-N/commands/
```

## LLM Grading Prompt

The grader prompt should say:

```text
Grade only from collected evidence. Do not assume untested behavior passes.
If evidence is missing for a success criterion, mark that criterion fail or conditional.
For each criterion, cite a specific evidence key/path.
```

Then recompute the final verdict in code from criterion statuses and rubric scores.
