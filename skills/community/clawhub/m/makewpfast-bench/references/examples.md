# Worked examples — prompt → command

These map common user requests to the right `mwf-bench` invocation. Run the CLI at
`scripts/mwf-bench`, then explain the numbers in plain English.

### "How fast is WooCommerce?" / "Is WooCommerce heavy?"
```
mwf-bench lookup "WooCommerce"
```
Report the grade, then the activation + homepage deltas. Note WooCommerce adds real homepage
cost on every page, not just admin.

### "Compare Yoast vs Rank Math for speed"
```
mwf-bench compare wordpress-seo seo-by-rank-math
```
One call resolves both, prints a side-by-side table, and names the faster one. Prefer this over
two separate `lookup` calls.

### "What's the TTFB cost of enabling this plugin on the homepage?"
```
mwf-bench lookup <name> --format json
```
Read `contexts.homepage.ttfb_delta_ms`. If `homepage` is null, say it wasn't measured on the
homepage (often the case for admin-only plugins).

### "Audit the plugins on this site"
```
mwf-bench me                      # show remaining quota first
mwf-bench audit --path . --top 10 # benchmark only active, heaviest plugins
```
Requires wp-cli and a WordPress install at `--path`. Only the active plugins are looked up, and
cached rows cost nothing.

### "I don't know the exact plugin slug"
```
mwf-bench resolve "<the name>"
```
Returns the slug, or a candidate list (exit 3) when ambiguous — in that case ask the user which
one before spending paid quota. Never guess a slug from memory.

### "Suggest a faster alternative to <plugin>"
1. `mwf-bench lookup <plugin>` to get its grade.
2. Propose 1–3 well-known alternatives from your own knowledge.
3. `mwf-bench compare <plugin> <alt1> <alt2>` to verify they're actually faster — don't claim an
   alternative is faster without checking it against the dataset.

## Quota discipline reminders
- Cached rows print "(cached, N days old)" and don't touch the API.
- `compare`/`audit` refuse more than 8 uncached paid calls unless you pass `--yes` or
  `--max-calls N` — surface this to the user rather than forcing it silently.
- `cat ~/.cache/makewpfast-bench/calls.log` shows exactly what consumed quota.
