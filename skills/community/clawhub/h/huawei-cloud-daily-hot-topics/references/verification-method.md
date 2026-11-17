# Verification Method — huawei-cloud-daily-hot-topics

## Offline unit tests (primary, no network)

```bash
python3 -m unittest discover -s tests -v
```

`tests/test_fetch_hot_topics.py` mocks the HTTP layer (`fetch_hot_topics._http_get`)
so the suite is fully offline and deterministic. It covers:

- record extraction and normalisation into `{rank, title, hot, source, url}`;
- retry-then-success and bad-envelope rejection in `fetch_source`;
- ordered degradation across providers (first fails → second succeeds);
- all-providers-fail → bundled sample fallback (`is_sample=true`);
- `--offline` shortcut;
- Markdown / text / JSON rendering and the `--top` constraint;
- argument validation (`--top 0`, unknown `--source`) and `--list-sources`.

## Structural validation

```bash
bash <skill-creator>/scripts/validate-skill.sh -s skills/devtools/common/huawei-cloud-daily-hot-topics
```

Checks the Huawei Cloud Skill Specification: YAML frontmatter, name/directory
match, required sections, reference documents, size limits, allowed extensions,
and the absence of hardcoded AK/SK.

## Live read-only spot check (optional, needs network)

```bash
python3 scripts/fetch_hot_topics.py --top 5
python3 scripts/fetch_hot_topics.py --format json --top 5 | python3 -m json.tool >/dev/null
python3 scripts/fetch_hot_topics.py --offline --format json
```

- The first command prints a live ranking table.
- The second confirms JSON is parseable.
- The third exercises the fallback path without network.

## Degradation verification

The fallback path is asserted by unit tests and can also be observed live by
forcing an unreachable provider, e.g. running with no network (or by setting a
very small `--timeout` against a blocked host); the output then carries the
`示例数据` label and a warning trail, and the exit code stays `0`.

## Scope of verification

Functional behaviour (parsing, normalisation, degradation, rendering) is covered
by the offline unit tests. Real network reachability and content of the
third-party endpoints are outside our control and are therefore verified as
best-effort (`live_skipped` in the coding self-test; the QA stage performs the
real read-only calls).