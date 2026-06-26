# Eval — lane deadlock guidance

## Expectation
The skill must treat `agent:main:main` cron routing as critical, but should prefer safe recovery first.

## Pass criteria
- Flags `agent:main:main` as a critical lane error
- Does **not** casually recommend editing `jobs.json` directly
- Allows direct `jobs.json` edits only as explicit break-glass recovery with backup + validation
