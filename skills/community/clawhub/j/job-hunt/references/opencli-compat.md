# Known OpenCLI compatibility patches

OpenCLI remains the default reader. The optional patches here address defects
reproduced with `@jackwener/opencli` 1.8.7; they are maintained by this skill,
not an OpenCLI upstream release. Before the first BOSS, Indeed, 51job, LinkedIn or
Nowcoder read, the agent
runs the read-only check below. If all affected bytes match the known original or
patched version, apply automatically; users need not copy commands or approve
this reversible local compatibility repair. Unknown versions or custom edits
are left unchanged. A rejected patch is not proof the installed adapter is broken:
use the normal reader, or the browser fallback when incompatibility is diagnosed.

## Diagnosed defects

| Observed defect | Narrow repair | Verified scope |
|---|---|---|
| BOSS headhunter detail may omit address/recruiter containers and use a plain h1; swallowed DOM errors become a false login refusal | Tolerate absent optional containers, recognize the detail title, ignore hidden login templates, navigate once with bounded render polling, and keep recommendation cards out of employer metadata | Shanghai original detail live on 2026-10-31 plus extraction/error regressions |
| 51job's `/pc/search?keyword=…&searchType=2` navigation times out while `/pc/search` renders results | Open the plain entry page; retain the existing keyword, area and limit in the search API request | Python / Shanghai / 3 rows on 2026-09-09 |
| 51job detail mislabels a current slider as a parsing error, shifts company attributes and loses address/paragraph breaks | Recognize the observed slider instructions as `ANTI_BOT`; use labelled company icons and the full address; preserve HTML line breaks | Beijing live detail on 2026-09-12 plus current/old DOM regressions |
| Indeed detail returns a sign-in heading as a job | Detect account pages with no job description and report a login error | Account-page DOM regressions and classifier stop-lock tests |
| Indeed puts `Full-time` into salary, losing job type | Separate labelled pay and job-type fields; only use pay-like header text as salary | Real no-pay posting plus pay/type DOM variants |
| Indeed search cards have ids but empty titles | Read the identified title link, including its existing title-attribute variant | Real search and DOM variants |
| Indeed header's `Remote` has no old location test id | Read the observed company-header sibling when the explicit location markers are absent | Real detail and old/new header DOM variants |
| Indeed's current detail page uses `vj-job-title` and a description heading instead of `h1` and `#jobDescriptionText` | Read the observed title, adjacent description and header metadata; wait for description text rather than a title alone | Current/old DOM variants, missing and delayed descriptions; live result recorded separately |
| LinkedIn rejects a country-qualified location such as `Shanghai, China` with HTTP 400 | Encode each Rest.li value without turning location commas into query separators; use the observed job-card decoration version | Live Shanghai, China search on 2026-10-07 |
| LinkedIn's inline job data contains a complete description, but the adapter emits an empty string | Join the matching job ID across inline payloads, preserve its description, wait for delayed content and reject empty descriptions | Live complete detail on 2026-10-07 and bounded-wait regressions |
| Nowcoder long articles are returned with a UUID that its detail endpoint cannot resolve; descriptions are cut at 500 characters | Carry the numeric long-article ID, retain moment UUIDs, read the complete available content and `createTime`, and preserve access errors | Live recommendation; free-article and ID/error regressions |
| Nowcoder returns a paid preview with HTTP 200 | Carry `content_complete` and `content_access` from its access flags; the result classifier refuses to count a preview as full detail | Recorded paid-preview and free-article responses; no restricted content retrieved |

## Check, apply, revert

`python scripts/opencli_compat.py --site indeed` is read-only; substitute `51job`,
`linkedin`, `nowcoder` or `boss` for those adapters. It checks the installed package version and exact source hashes.
Unknown versions, official-source drift, or local edits are refused, not guessed
at. Exact hashes of earlier patches shipped by this skill are recognized as
`previous_patch` and can be upgraded or reverted; user edits remain untouched.
`--package-dir` supports installations where the executable wrapper does not
resolve to the npm package. Stock OpenCLI 1.8.7 loads adapter overrides from
`~/.opencli/clis` even when `OPENCLI_CONFIG_DIR` changes the trace/profile root.
The helper therefore defaults to `~/.opencli`; `--config-dir` is only for test
fixtures or a custom loader that actually reads that directory.

For recognized source, the agent runs:

```sh
python scripts/opencli_compat.py --site indeed --action apply
opencli validate indeed
```

The helper creates a local override from the installed adapter only when none
exists. It never ejects over an existing override, and only edits recognized
bytes in the listed files, preserving other adapter files. It never edits the installed npm package, contacts
a site, changes browser settings, installs dependencies, or retries a stopped
source. A second apply is a no-op. All files are checked before any is written.
Bundled `auth.js` stays in the installed package: copying it into a site-only
override would break its relative import of `../_shared/site-auth.js`.

Revert only this skill's recognized edits:

```sh
python scripts/opencli_compat.py --site indeed --action revert
```

The local override remains, with the original file contents. Use `opencli adapter
reset <site>` only if the user intends to discard that **entire** local override.
After upgrading OpenCLI, re-check; don't force an old patch onto new source.

The versioned replacement data is in [opencli-patches/1.8.7.json](opencli-patches/1.8.7.json).
Upstream-derived snippets retain the OpenCLI license, Apache-2.0
(https://www.apache.org/licenses/LICENSE-2.0); upstream: https://github.com/jackwener/opencli.
They were modified for the fixes listed above; no candidate data or cookies are
part of these patches.

## Browser fallback is independent of patching

When a supported browser can complete the requested search but a **diagnosed
adapter incompatibility** prevents extraction, use `unsupported_extraction` under
[browser-fallback.md](browser-fallback.md). Preserve the failed adapter output
and the evidence for the incompatibility. A patch is optional, not a required
step before browser use. Read and import the actual page results with their
URLs, timestamps and verbatim text; do not pass a browser capture off as an
adapter response. The bundled fallback reads known URLs and links. If the site needs an
interactive search that its adapter cannot execute, request the result URL or
original JD from the user; do not claim that a known-URL capture tested its search box. Google/search-engine discovery is a separate source
strategy, not the definition of built-in CDP and not a substitute for a site's
search acceptance test.

One timeout or blank field alone is not that diagnosis. A login wall, CAPTCHA,
permission denial or rate limit still stops the site across tools. Fixing local
code does not authorize a new read after such a refusal; follow the existing
user-confirmed recovery workflow. Never call all live tests passed merely because
unit tests or a patch checksum passed.

The optional DOM integration tests exercise the actual patched browser scripts:
with `jsdom` available to Node and `OPENCLI_TEST_ADAPTER_DIR` pointing to the local
`clis` directory, run `node --test scripts/tests/opencli-dom.test.cjs` on a checkout of the source repository. No live
site access is made by these tests.


### 51job search filters (verified 2026-10-11)

The search page's `dictStore.d_search_*` dictionaries differ from the resume
editor's company-type dictionary. The 1.8.7 compatibility patch uses the search
page's actual values: 国企 `04`, 合资 `03`, 民营 `05`, 3–5 年 `03`, and 5 万以上 `12`.
It updates salary, experience, ownership and exact label aliases together;
unknown, obsolete or ambiguous filter labels now fail instead of silently
removing the condition. A 国企 query also rejects returned rows whose original
company type is missing or not 国企. The response is not silently filtered into
an apparently successful empty list.

Primary evidence: [51job search page](https://we.51job.com/pc/search), its
[loaded search application](https://fccdn.51jobcdn.com/we/static/js/app-e2e93592-4d50a46c.js),
and the dated public-enum fixture in the source repository's test fixtures. A live control
query with `companyType=04` returned three original `companyTypeString: 国企`
rows. Recheck the search UI if these enums change; do not substitute a similar
company-type table found elsewhere in a bundle.
