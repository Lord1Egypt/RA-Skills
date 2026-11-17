# Workflow contract

This reference defines how to use the host's Apify tool for `instagram-media-links-and-post-insights`. It does not call services or process credentials. No helper is used for request transformation: preserve the user's exact URL strings and order in the required `videoUrls` array.

## Preflight before user commitment or Actor call

This is an internal check. Complete it before telling the user “I’ll process these”, “I’m starting”, or otherwise implying work has begun. A successful Apify OAuth connection does not establish that this Actor's tools or result readers are present in the current ChatGPT connector.

1. Inspect the Apify tools actually exposed in this session, their live descriptions/schemas, and any explicit host-visible authorization status. Identify the current host. Do not infer authorization or tool availability from an installed Skill or a prior conversation.
2. Establish one of the two call paths below, including a way to obtain real output rows. If neither path is completely available, or authorization/schema/run-data access is unclear, stop before starting an Actor. Tell the user which capability is missing and state that no Actor was started and no results were received. Do not call a different Actor, use a direct HTTP/API request, shell, token, or `sessionid`, or guess at an unexposed tool.
3. Keep the exact user URL strings and their original positions. Do not normalize or merge distinct URLs under unverified equivalence rules. If exact duplicate strings share a submitted entry, preserve every original position in the final report.
4. Only after preflight passes may you tell the user you will process the URLs and invoke the Actor. Use only `apple_yang/instagram-video-scraper-api`, with the Actor-schema-confirmed required `videoUrls` array and the exact supplied URLs. For combined modes, reuse one result where possible. Do not automatically retry or call a second Actor.

## Supported tool paths

### A. Dedicated target-Actor tool

Treat a tool as the dedicated target-Actor tool only when its live description/schema identifies the exact owner and Actor name `apple_yang/instagram-video-scraper-api`. A similar name, generic Instagram description, or missing/unclear owner or Actor identity is not sufficient. If identity is not exact, do not use it as the dedicated path; use the generic path only if that path is fully available, otherwise fail closed.

For an exact dedicated tool, inspect its live input and output schemas before calling and construct arguments from those schemas. If it directly returns result rows, use that actual output schema and do not invent a Dataset step. If it instead returns a run status and Dataset/storage identifier, follow the run-state and dataset-reading procedure below; do not treat the run envelope as result rows.

### B. Generic Actor-call tool

Use this path only if no dedicated target-Actor tool is exposed and the session exposes all required generic tools:

1. Use the currently exposed `fetch-actor-details` tool or its host-provided equivalent to retrieve the target Actor's current input and output schemas. Confirm `videoUrls` is the required array field and establish which returned fields are relevant. If the Actor details/schema tool is absent or the contract is incomplete, stop before any Actor run.
2. Read the generic Actor-call tool's own live schema. Supply the target Actor identifier in exactly the format required by the currently exposed generic tool schema or authoritative documentation. Do not infer API/MCP identifier format from the Store page URL or hardcode an unverified representation. Pass the URL array under the verified Actor input field `videoUrls`.
3. Read the actual call response and record the returned run status and actual Dataset identifier using the fields defined by the live tool schema. Do not fabricate either. A generic `call-actor` may return only run status and storage IDs, not output rows.
4. Determine whether the run has reached a confirmed terminal state using its actual returned status and the current tool/host contract. Do not assume a fixed set of terminal status values. If the run is non-terminal and the session exposes a run query/wait tool, use that tool's live schema to continue checking the same run. Do not start the Actor again merely because the run is still in progress. If the run remains non-terminal or no run-query capability is available, tell the user that processing is still running/pending and results may be incomplete; do not say the task is complete.
5. Use the exposed `get-dataset-items` tool or its host-provided equivalent to read rows from that Dataset when available. Inspect its live schema and pagination metadata. If paginated, continue using the returned offset/limit/total or other documented continuation signal until the available evidence establishes all pages were read. Do not conclude there was no data from an empty/short first page. Dataset rows read while the run is non-terminal are provisional/partial unless there is explicit evidence that the Dataset is already complete. If no Dataset reader is exposed, or pagination/completeness cannot be established, report that results are unavailable, partial, or not confirmed; never describe that condition as an empty Actor result. Describe results as complete only when both the run is in a terminal state defined by its tool contract and the Dataset has evidence of a complete read.

Apify currently documents the names `fetch-actor-details`, `call-actor`, `get-actor-run`, and `get-dataset-items`; it describes Actor details as including input/output schemas, generic calls as returning run status/storage IDs rather than result rows, run lookup as available, and Dataset reads as supporting pagination. These are reference examples, not a guarantee that the current host exposes those exact tools or schemas. Use live host schemas. Actor identifier argument format, tool argument names, run-status semantics, result envelope structure, and pagination completion signals remain determined by the current tool contract and must be confirmed at runtime.

## Match returned rows

- Match only with returned `url` evidence that can be safely compared to the original input. Exact string equality is the default. If a host/tool documents a safe canonical comparison, apply only that documented rule and preserve both original strings.
- `code`, `pk`, and `id` are not matching fallbacks unless a current, independently verified contract establishes their semantics.
- Never assign rows by return order. If `url` is missing, conflicting, or yields multiple candidates, explain that the input-to-result mapping cannot be confirmed and cite the available evidence in the user's language. If no row can be reliably matched to an input, explain that no matching row was received and cite the evidence in the user's language.

## Classify each matched row

- A non-empty string `errMsg` is the Actor's returned error text. Report it as returned; do not infer why it occurred.
- If `errMsg` is empty or absent, report that state only. It does not prove success.
- If an output field is missing, empty, or absent, explain that it was not returned or is unavailable in the user's language. This does not mean zero, absent media, or an unsuccessful post.
- A returned `videoUrl` or `audioUrl` is a direct link supplied by the Actor, not a downloaded local file or a guarantee of future availability.
- If the content type cannot be established from the user's stated intent and Actor output, say support cannot be confirmed. `/p/` alone is not video evidence. Do not make a photo/carousel support claim.
- Treat `likeCount` and `commentCount` as returned raw counts. Do not calculate rates or infer trend, performance, audience response, or causation. Treat the output as a snapshot.

## Batch report

Return one status per original URL, in original order. Report confirmed rows, non-empty Actor error messages, inputs with no reliably matching row, fields that were not returned, and unresolved mappings separately. Do not assume batch-order guarantees, an always-present `errMsg`, or undocumented top-level errors. Do not call partial results complete. Use only the visible tool output and accurately state when the host did not provide enough evidence to classify a result.
