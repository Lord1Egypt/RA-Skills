# Background execution

Most commands are short-lived one-shot tools and should run in the foreground.
Only `search` over many sources, and `analyze` over many PDFs, are worth
backgrounding.

## Search with a progress file

```bash
python run.py search -q "regression data selection" -s arxiv openalex -l 50 \
    -o ./proj/01-literature-survey --background
```

`--background` writes `search-progress-search.json` next to the results with
stage, percentage, elapsed seconds and status. Poll it while the run proceeds;
when it reaches `status: completed` the `summary` field holds the final counts.

## Long-running tasks and this environment

A long-running command started as a detached background job is killed when the
session that started it ends. If a search or analysis may exceed a couple of
minutes, either keep it in the foreground with a generous timeout, or split it:

```bash
# split by source instead of one long run
python run.py search -q "..." -s arxiv    -l 30 -o ./proj/01-literature-survey
python run.py search -q "..." -s openalex -l 30 -o ./proj/01-literature-survey
```

## Interrupted runs

Results are written only after all sources have been queried, so an interrupted
run leaves no partial BibTeX behind. Re-run it; nothing needs cleaning up.
