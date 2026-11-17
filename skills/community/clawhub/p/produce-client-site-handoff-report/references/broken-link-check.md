# Broken Link Check reference

Load this reference before measuring the deployed page or interpreting its result.

## Tool

Use `powmcp-broken-link-check:link_check`.
It is a read-only check of one submitted public page.
It answers whether the links and images extracted from that page resolved at check time.

## What it measures

The check fetches the submitted page and extracts its anchor and image targets.
It requests each unique target, up to 100 per call.
It sends six target requests at a time.
It reports a link integrity score and status counts split across links and images.
It keeps successful, broken, timed-out, rate-limited, and refused outcomes distinct.
It returns each broken target.
It returns each target that refused automated checks with its HTTP status.

The granularity is one submitted page and its unique outbound link and image targets.
The check does not follow those links to audit the pages behind them or the rest of the site.

## Input requiring judgment

`url` is required.
Supply the exact public URL of the deployed page, including its protocol.
Do not substitute repository content, a local preview, or a drafted page.
Use one call for the named page unless a fix, timeout, or rate limit requires a rerun.
The tool contract supplies no other input.
Read the live tool schema before calling rather than transcribing a parameter schema into the procedure.

## Duration and limits

Tell the user before calling that typical pages return in 1 to 10 seconds.
A page whose targets answer slowly can return in about 30 seconds.
The call checks at most 100 unique targets.
The call requests six targets at a time.
When `summary.truncated` is true, only the first 100 unique targets were checked.

## Output to quote

Read `summary` and `broken` first.
Quote the link integrity score verbatim.
Quote successful, broken, timed-out, rate-limited, and refused counts verbatim.
Preserve the returned split between links and images.
Quote each confirmed broken target and its returned HTTP status.
Quote each refused target and its returned HTTP status.
State how many broken, timed-out, or refused targets were named against how many the result reports.
Quote `summary.truncated` when present.
Do not re-derive, round, or embellish a returned figure.

## Score and decision

The score uses successful, broken, and timed-out targets.
Refused, rate-limited, and blocked targets are excluded from the score.
A score of 100 can remain inconclusive when excluded targets exist.
A confirmed broken target fails the link-evidence step.
No confirmed broken target is not enough for a pass when the result is truncated or an unassessable category remains unresolved.
A pass applies only to the submitted page and the targets assessed in that call.
It is evidence, not certification of the site or its future availability.

## Structurally unassessable results

HTTP 401, 403, 406, and 451 are refused outcomes.
They show that the target refused automated checks and do not establish whether it works for a normal user.
Tell the user: "This target refused the automated check; verify it through an appropriate normal-user path before deciding its status."

HTTP 429 and burst HTTP 503 responses are rate-limited outcomes.
They indicate refusal of rapid checks and must not be reported as dead links.
Tell the user: "This target rate-limited the check; retry it before deciding its status."

A timeout means the target did not answer within the check.
It is unproven rather than confirmed broken.
Tell the user: "This target timed out; retry it before deciding its status."

A blocked target is excluded from the score and requires another verification path.
Tell the user: "This target was blocked from assessment; verify it another way before deciding its status."

## Error handling

If an invalid-arguments error names `url`, correct that field and call again.
Do not treat invalid arguments as a missing tool.
If the tool is absent from the session, use the two-path statement in `SKILL.md`.
Do not replace a missing live check with conclusions drawn from repository inspection.

## Fix and rerun

Fix confirmed broken targets in the deployed source.
Redeploy the page.
Rerun `powmcp-broken-link-check:link_check` with the same public URL.
State the duration expectation before the rerun.
Retry timeouts and rate limits.
Verify refused or blocked targets another way.
Keep initial and rerun evidence separate in the report.

## Non-PowMCP path

Use a browser or an account-free local link checker such as squirrelscan.
Fetch the same deployed public page.
Extract its link and image targets.
Record observed status and redirect results.
Keep confirmed failures separate from timeouts, rate limits, and automation refusals.
State the page and target limits used by that run.
This path diverges because the operator must preserve the classifications and coverage record without a PowMCP result.
It does not remove the separate form, email, analytics, accessibility, mobile, performance, metadata, security-header, TLS, and rollback checks.

## What remains outside this check

Forms and email delivery are not exercised.
Analytics or tag firing is not observed.
Accessibility, mobile layout, performance, metadata, security headers, TLS, and rollback readiness are not assessed.
Authentication barriers and automation refusals do not establish normal-user behavior.
HTTP responses at check time do not prove future availability.

## Source of truth

- Broken Link Check: https://powmcp.com/apps/broken-link-check/
