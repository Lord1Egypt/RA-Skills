# Release verification — 1.0.1, 2026-11-17 UTC

Authoring environment: OpenClaw 2026.11.4 (d843d6a), Python 3.

Passed:

- Official skill-creator quick validator: Skill is valid.
- 20 unittest cases: catalog shapes, malformed data, duplicate IDs, dated inventory, alias filtering, endpoint matching, tools, exact IDs, USD conversion, token budgets, missing limits, three transports, metadata retention, Markdown escaping, in-process stdout-only CLI, missing/existing configuration paths, directory-symlink destinations, output-flag rejection and absence of filesystem-output APIs.
- The helper rejects the removed --output flag before any input read or HTTP request. Tests use no subprocesses; live catalog output remains stdout-only.
- Public live catalog fetch through the bundled helper, exporting 62 tool-capable model registrations. No API key required.
- Generated model field names and optional cost entries reviewed against the installed OpenClaw config schema and local custom-provider documentation.

Limits:

- Full JSON Schema validation was not run: the optional Python jsonschema library is not installed. No dependency was installed for this check.
- No account login, secret mutation, provider configuration mutation, primary/fallback change, paid inference, tool loop, UI picker verification, mining or funding action was performed.
- Model support is advertised public metadata, not a claim that all 62 models were inference-tested.
- Snapshot is dated; prices, inventory, privacy, feature flags and promotions require refresh.
- Registry security review is separate: these local tests do not assert that ClawHub has accepted the release or issued a clean verdict. See SECURITY.md for the 1.0.0 findings and changes.

Run from this skill directory:

~~~bash
python3 -B -m unittest discover -s tests -v
python3 scripts/catalog.py --agents-only --format openclaw
~~~
