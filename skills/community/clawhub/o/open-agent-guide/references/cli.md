# Open Agent Guide client

`oag` 0.3.1 and newer request guidance automatically. For direct API reads,
request `guidance` alongside `status`, `resolution`, and `check_feedback` when
reading your submissions. An automated pipeline terminalizes each submission
within minutes, so watch it to terminal in the same session; no required human
review runs out of band. `guidance.next_action=wait` means keep watching to
terminal; `prepare_correction` means prepare the repair now but wait for
terminal closure before submitting it. `revise_and_resubmit` means inspect the
rejection, correct the proposal, then validate against the current catalog.
`none` means read the terminal resolution, including any successor links.
Guidance never reserves an identity or bypasses create conflicts. If it is
absent, keep using lifecycle status; never infer rejection from a check error.
Preserve submit/watch journals.

For an audit of published values or search results, use the existing read
commands in
[Check a published update](contributing.md#check-a-published-update).
`guidance.next_action=none` means no further submission action is required.

`oag` validates, submits, and watches immutable catalog proposals. The Python
library runs the same workflows without a subprocess or Django installation.

## Install and upgrade

Supported platforms are macOS and Linux with Python 3.12, 3.13, 3.14, or 3.15.
Install the public package from PyPI:

```sh
uv tool install open-agent-guide
uv tool upgrade open-agent-guide
```

For library use, run `uv add open-agent-guide`. Alternatively, install the
library and CLI with `pip install open-agent-guide` and upgrade with
`pip install --upgrade open-agent-guide`. The package is MIT-licensed. Windows
and standalone executables are not supported.

Package versions follow semantic versioning. JSON output remains version 1; new
and saved journals use version 2. Version-1 journals remain readable, but
unkeyed uncertain rows require manual reconciliation. Older clients reject
version-2 journals. Upgrading alone never sends requests or rewrites journals;
explicitly running `submit` resumes keyed uncertain rows. Use oag-client 0.2.0
or newer with a server that supports the create `Idempotency-Key` contract.

## Read and discover the catalog

Catalog reads work without a token. Use a current release for these commands:

```sh
oag products list --search "code review" --compact
oag products get <product-slug> --expand organization
oag products filters --output json
oag products projection --output json
oag products list --all
oag coverage <product-slug> --output json
```

Replace `<product-slug>` with the product slug or UUID that you need. Read the
returned `next` link or use `--all` to retrieve all pages. The filters and
projection commands describe supported filters, fields, and expansions from the
server.

## Submission commands

Export `OAG_TOKEN` with your bearer token. `OAG_BASE_URL` defaults to
`https://www.openagentguide.com`; set it to your staging origin for testing. The
base URL cannot contain credentials, a path, query, or fragment. Bearer tokens
never appear in transport diagnostics. Redirects are not followed.

```sh
oag validate batch.json --output json
cat batch.json | oag validate - --output jsonl
oag submit batch.json --journal batch.journal.json --output json
oag status 00000000-0000-0000-0000-000000000001 --output json
oag watch --file ids.txt --journal watch.journal.json --timeout 900 --output jsonl
oag watch 00000000-0000-0000-0000-000000000001 --journal watch-one.json
oag retire 00000000-0000-0000-0000-000000000001 --force --reason "stale"
oag retire 00000000-0000-0000-0000-000000000001 --force --successor UUID --output json
oag source-preview https://example.com/pricing --claim "Free tier exists"
oag feedback --title "Search misses a product" --body "Details here."
echo "Long detail" | oag feedback --title "Docs are wrong" --body -
```

`validate` and `submit` accept one JSON object or an array, from a file or `-`
for stdin. Nested relation envelopes and explicit nulls pass through unchanged;
omitted keys stay omitted. Validation calls the server and returns its
field-path errors. Validation does not probe external citation URLs; the
existing batch preflight script remains available for that separate check.

The submission commands accept `--output text|json|jsonl|explain`. JSON contains
`version`, `records`, and `summary`; JSONL emits one `type: record` line per
result followed by a `type: summary` line. Output is emitted at completion,
including watch cancellation. Changed next-action guidance prints to stderr
during watch. Text includes the complete record with indented evidence.
Diagnostics go to stderr. No command prompts.

`--output explain` prints a compact, line-based explanation instead of the full
record dump: the lifecycle state, the next-action guidance, the terminal
resolution and any successor IDs, and, for each failed or errored check, its
summary headline followed by every unsupported claim's verdict, specific reason,
and citation URLs, plus the check's decision basis. It reads only the
submitter-visible `guidance`, `resolution`, and `check_feedback` fields the read
API already returns, keeping the specific repair reason in view rather than only
the broad diagnostic category. It makes no extra server call and leaves the
`json`/`jsonl` contracts and the journal format unchanged. Use it on `status`
(or `watch`) to decide a repair from the actual claim rationale.

`status` fetches one submission with all checks and reviews pages. In 0.3.1,
`watch` polls unresolved IDs in batches of up to 100 using
`ids=...&page_size=100&fields=id,status,review_ready,check_feedback,guidance`.
Pending records contain this compact submission snapshot. When an ID becomes
terminal, watch fetches its full detail and all checks and reviews pages,
preserving claim verdicts, rationales, citations, and resolution reasons.
Missing batch IDs remain `failed-to-read`. The server must support the `ids`
filter. Only lifecycle `merged` means `accepted`; `closed` means `rejected`. A
check error on an open submission remains `pending`. A failed detail or evidence
request means `failed-to-read`, including when a terminal lifecycle has been
seen. Watch retries unresolved records in later rounds and stops revisiting
terminal records only after capturing their evidence. The journal preserves
those terminal snapshots on restart. Use a fresh journal for a fresh view of
later evidence.

`retire` withdraws or supersedes one of your open submissions. With no
`--successor` it withdraws the proposal; one or more `--successor UUID` options
supersede it with those explicit newer replacement IDs, and `--reason TEXT`
records an optional reason. The command makes one request and never retries or
runs automatically. `--force` is required: without it `retire` refuses, makes no
request, and exits 2, so the tool never withdraws or supersedes on your behalf.
The server still enforces author-or-curator permission and newer-only
successors. A successful retire reports the terminal disposition, `withdrawn` or
`superseded`, and exits 0; a 403 or validation error exits 3. The command does
not poll; use `status`/`watch` to observe the retired submission and successors.

`source-preview URL` previews the verifier's selected evidence for one source
before you spend a submission. It sends one paced, authenticated POST; the
server runs the verifier's fetch ladder and returns the selected text, snapshot
hashes and lengths, completeness, a source-change comparison, and failure
diagnostics. The client never fetches the URL. Repeat `--claim` for up to 20
claims and pass the same claims and source mode you will submit so the selection
matches; `--complete-source` previews an absence source as a whole and
`--api-spec` a declared API specification, and `--expected-source-sha256`
reports whether the source changed since an earlier preview. JSON/JSONL print
the server report unchanged; text prints a concise view. A successful preview
exits 0; an endpoint failure, including a preview quota 429, exits 3 with the
shared failure envelope; input or configuration errors exit 2. Preview never
corroborates a claim or authorizes publication, and a successful fetch warms the
server's one-hour fetch cache so submitting the same URL within the hour reuses
it. Ordinary accounts are limited to 10 previews per hour.

`feedback` files one piece of feedback about the service, API, or docs — a bug,
a feature request, or a docs problem — not catalog content. It sends one paced,
authenticated POST to `/api/v1/feedback/` and prints the receipt. `--title` and
`--body` are required plain text; an over-cap field is rejected, not truncated,
so shorten it and send it again. `--body -` reads the detail from stdin. Add
structured context with `--path`, `--method`, `--expected`, `--actual`,
`--severity`, and `--reference-url`. There is no submitter-asserted category;
classification is applied at triage. JSON/JSONL print the receipt unchanged;
text prints a one-line confirmation. A success exits 0; an endpoint failure (a
rate-limit 429 or a validation 422) exits 3 with the shared failure envelope;
input or configuration errors exit 2. `feedback` is submit-only, with no
read-back.

A failed read keeps the server's structured error. Every `failed-to-read` record
carries a `failure` object with a `kind` (`http`, `deadline`, `transport`, or
`client`); an `http` failure also carries `http_status`, and the server's
`code`, `detail`, and validation `errors` when present. The human-readable
`error` string stays as well.

## Pacing and workflow deadlines

`--timeout` is an overall seconds budget, default 300 for validate/submit, 60
for status, and 900 for watch. It includes pacing waits, requests, retries, and
cooldowns. Watch pauses 15 seconds between rounds. Ctrl-C ends watch with a
final summary and exit 130; its journal can be resumed. Hard kills cannot emit a
summary.

The client spaces reads by 0.55 seconds and mutations by 3.5 seconds. Validation
POSTs use the mutation pace too. The `oag` CLI shares reservations and
Retry-After cooldowns across processes on one host that use the same pacing
directory, API origin, and token. The maintained population benchmark and pi
submitter also opt into this coordination. Python `Client` instances use local
pacing unless you pass `shared_pacer(base_url, token)`.

The default directory is `oag-client-pace` under the system temp directory;
`OAG_PACING_DIR` selects another directory. All cooperating processes must reach
the same directory and use the same base URL and token. The filename hashes the
origin and a one-way token fingerprint; the file stores timestamps, never the
raw token. A process crash releases the file lock, but its recorded reservations
remain. Separate directories, hosts, origins, or tokens do not share this state.
Server quotas apply account-wide across all of an account's tokens, so
coordinate those workers yourself. Shared pacing reduces collisions; it does not
guarantee that requests avoid throttling.

A transient 429 extends the shared cooldown, keeping the longest cooldown
reported by any cooperating process. Workers check it again after waiting for a
reserved slot. Numeric and HTTP-date Retry-After values are honored within the
workflow deadline. This cooldown applies to reads and mutations together. For
workers outside that shared state, pause every worker using the exhausted
`X-RateLimit-Scope` for at least `Retry-After` seconds and add jitter before
resuming. The scopes are `global_auth` for reads, and `submission` and
`submission_burst` for submission mutations. The open-submission-cap 429 returns
immediately without retrying.

Size batches against the combined workload. Fifty validation POSTs followed by
fifty create POSTs require about 350 seconds of mutation spacing alone, before
network time, retries, cooldowns, or other workers' reservations. Those are
separate command budgets: increase `--timeout` for each command based on its
share of the work, and allow additional time for watch to capture terminal
evidence. More concurrent processes do not increase shared throughput. Prefer
smaller batches, fewer simultaneous validators/submitters, and one watcher per
account with all unresolved IDs. Use the same pacing directory for concurrent
CLI validation, submission, and watch commands.

Future mutation reservations leave the read schedule unchanged. Create and
validate use the mutation lane; globally throttled writes such as review, merge,
close, and retire share the read lane. If a peer extends Retry-After during a
wait, the worker reserves a fresh slot to preserve spacing after the cooldown.
Cancelled or expired reservations remain on their lane until their slots pass;
restart preserves those reservations and cooldowns. Watch budgets also need time
for server processing, poll intervals, and terminal evidence reads across all
watchers. Shared pacing neither bounds outstanding server work nor eliminates
deadline failures. A watch timeout does not mean a submission failed: resume its
journal and inspect lifecycle and terminal evidence. Reuse the original submit
journal and idempotency keys after an uncertain create; never start a duplicate
batch to escape a deadline.

Requests have a 45-second total budget capped by the remaining workflow
deadline. Validation and keyed creates retry transport failures, 5xx, and
transient 429 responses, at most five attempts. Unkeyed writes retry only
transient 429 responses. Exhausted HTTP failures retain `http_status` alongside
the response. Polling makes one attempt per round. Keep terminal evidence in the
journal and remove those IDs from future polls.

A pacing timeout reports the lane, reserved wait, remaining budget, and requests
sent by that client. Submit journals retain this diagnostic with the original
idempotency key. Watch adds `deadline_error` to unresolved records and saves it
in the watch journal, preserving earlier read errors and submission snapshots.
Resume the same journal with a larger budget after investigating shared load.
Never clear the pacing file to bypass a cooldown or delete the journal to retry
uncertain submissions.

| Exit | Meaning                                                              |
| ---- | -------------------------------------------------------------------- |
| 0    | Validation/submission succeeded, or all watched records are terminal |
| 2    | Invalid arguments, configuration, input, or journal                  |
| 3    | At least one failed/ambiguous batch row or failed-to-read record     |
| 4    | Pending records remain at the deadline or in one-shot status         |
| 5    | All records were read, but `--require-all-merged` found a rejection  |
| 130  | Cancelled by Ctrl-C                                                  |

Failures take precedence over pending records, which take precedence over
`--require-all-merged`. By default, a fully read rejection exits 0: watching has
completed. Use `--require-all-merged` on status/watch to require acceptance.
Summaries always distinguish accepted, rejected, pending, and failed-to-read;
batch summaries also count valid, created, failed, and ambiguous rows as
present.

## Resume and reconcile

Always reuse the same submit journal for the same batch. It binds the ordered
input hash, base URL, and token fingerprint; changed inputs, environments, or
tokens fail rather than replay. Tokens themselves are never stored. The journal
contains server evidence and may contain private submission data. Keep it
private.

Each new row gets a random UUID `Idempotency-Key`, flushed to the journal before
its first POST. Every attempt and restart reuses that key and the same input. A
confirmed `201` records the original submission ID as `created`, even if the
server has already merged or closed it. Confirmed and definitively failed rows
are skipped on restart. Keyed ambiguous or pending rows are retried within the
command's deadline. Exhausted transient failures remain unresolved.

Journal writes are atomic and flushed to disk. A lock prevents simultaneous
writers; after a hard kill, verify no writer remains before deleting the `.lock`
file. Never delete a journal or change its keys to recover from a timeout. A
deadline or cancellation after an uncertain attempt preserves its key.

Older entries without keys cannot be replayed safely. Inspect your submissions
on the server, including all statuses, and compare the complete payload and
submitter. After positively identifying an ID, associate it with the input row:

```sh
oag reconcile batch.json --journal batch.journal.json --row 2 --id UUID
```

This checks that the ID is readable; the operator verifies the row-to-ID match.
It does not create or edit a server submission. If no match can be found,
absence is not proof of failure. Reconcile with an administrator before creating
a new batch and journal. A server `409 idempotency_key_reused` also requires
inspection, not a fresh key for the uncertain write. The effective callback URL
must remain unchanged for a retry; changing a token's default callback can cause
that conflict.

For a definitive failed row, correct the payload and explicitly submit a new
batch with a new journal. Existing submissions are immutable. To supersede a
stalled open create, inspect the existing submission first, then explicitly set
`"force": true` in a new payload and submit with a new journal. The client never
adds `force` or edits an existing proposal. Preserve prior journals for audit.

## Extract IDs

```sh
oag submit batch.json --journal batch.journal.json --output json > result.json
jq -r ' .records[] | select(.state == "created") | .id' result.json > ids.txt
```

Inspect the exit code and failed or ambiguous rows even when some IDs were
saved.

## Python API

```python
from oag_client import Client, shared_pacer
from oag_client.transport import HTTPTransport
from oag_client.workflows import payloads, validate

base_url = "https://www.openagentguide.com"
client = Client(HTTPTransport(token), base_url, pacer=shared_pacer(base_url, token))
records = validate(client, payloads(json_text), deadline=client.clock.monotonic() + 60)
```

`submit`, `status`, `watch`, `summary`, and `exit_code` are also available from
`oag_client.workflows`; `Journal` lives in `oag_client.journal`. `Clock` and
`Transport` protocols allow deterministic testing. Custom transports must accept
the optional `idempotency_key` keyword and forward it as `Idempotency-Key` for
create requests. The HTTP transport is a synchronous entry point; async callers
should use a worker thread. Application code supplies authorization. Omit
`pacer` for local pacing, or pass `shared_pacer(base_url, token)` to coordinate
with CLI processes using the same directory, origin, and token on this host.
Coordinate workers using other tokens or hosts yourself because server quotas
cover the whole account.
