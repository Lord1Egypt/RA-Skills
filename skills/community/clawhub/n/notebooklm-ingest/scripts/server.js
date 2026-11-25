'use strict';
/**
 * The javis-server transport — two write calls, and nothing else.
 *
 * Spec: javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-design.md
 *       R2, R3, R4, R5, R9, R16, R19, R20.
 * Contract: references/tool-contract.md (wire shapes and every validation rule).
 *
 * `postJson` is gmail-wiki-ingest's, carried across rather than rewritten
 * (gmail-wiki-ingest/scripts/gmail-wiki-ingest.js:100), with its three
 * invariants intact and for its three reasons:
 *
 *   1. A non-2xx comes back as an ENVELOPE rather than thrown, because the
 *      agent has to be able to tell "nothing to ingest" from "the call failed",
 *      and an exception mid-turn reads to it as neither.
 *   2. A missing `OPENCLAW_GATEWAY_TOKEN` throws loudly. That is a broken
 *      container, not a runtime state, and it should stop the run rather than
 *      be reported as a refusal the user could act on.
 *   3. A 2xx whose body is not JSON is `unparseable_response` and never a bare
 *      `null` — handing `null` to a caller about to read `.status` off it turns
 *      a transport fault into a TypeError two frames later.
 *
 * **R19 — THIS MODULE IS WRITE-ONLY, AND THAT IS ENFORCED BY ITS SURFACE.**
 * There is no GET, no read helper and no "fetch the sources back" function; the
 * push endpoint answers with the outcome of the write it just did and nothing
 * else. A compromised skill therefore cannot use it to read the wiki, another
 * source, or another user's data. test/server.test.js asserts the absence as a
 * property of the exports, not as a comment — a read helper added later fails
 * the suite.
 *
 * **THE SHAPE BELOW IS JAVIS-SERVER'S, READ OFF THE ENDPOINT IT SHIPPED.**
 * It was this bundle's *expectation* while the server half was unbuilt, and the
 * expectation was wrong in four ways at once — a different path, a `path` and a
 * `notebook` field the request model does not declare, a response read for
 * `pages`/`spend` where the server answers `page`/`feeds`/`budget`, and a
 * refusal vocabulary that shared exactly one code with the server's. Each half
 * tested itself and both were green, so this block now cites the server file
 * that defines every value, and test/contract.test.js reads those files when a
 * javis-server checkout sits beside this one.
 *
 *   path      javis-server app/routers/skill_wiki_sources.py (`@router.post`)
 *             mounted with prefix `/api` in app/main.py
 *   request   `WikiSourcePushRequest` in that same file
 *   response  `_envelope` in app/services/skill_wiki_sources.py
 *   refusals  `REFUSAL_NEXT_STEPS` in app/services/skill_wiki_sources.py
 *
 * Env:
 *   OPENCLAW_GATEWAY_TOKEN  required — Bearer auth to javis-server
 *   JAVIS_SERVER_URL        optional — defaults to http://javis-server:8000
 */

const SERVER = process.env.JAVIS_SERVER_URL || 'http://javis-server:8000';

/** The ClawHub slug, the SKILL.md frontmatter name and the directory name. */
const SKILL = 'notebooklm-ingest';

/**
 * R17's client half. The server records WHICH KIND of source a row is and names
 * its wiki page after that kind; the kind travels in the body, because the
 * gateway token identifies the user and not the source type. javis-server keys
 * `SLUG_PREFIXES` on exactly this string (app/services/obsidian_ingest.py), so
 * a pushed note's source page is `notebooklm-note-<id>` and never
 * `obsidian-note-<id>`.
 */
const SOURCE_TYPE = 'notebooklm';

/**
 * EXACTLY TWO ENDPOINTS, both writes.
 *
 * `push` is the route javis-server serves at
 * `app/routers/skill_wiki_sources.py` under the `/api` prefix (R2: the only way
 * NotebookLM content enters). It is NOT named after NotebookLM, deliberately —
 * the spec's Ownership table: "every future 'a skill fetched something, ingest
 * it' feature reuses it".
 * `digest` is the existing generic chat push gmail-wiki-ingest already uses —
 * the scheduled run's only output path, because an `openclaw cron` turn is
 * started by openclaw's own timer and gets no `body.tools` from javis-server,
 * so `chat_emit_*` is simply absent on it (see references/trigger-contract.md).
 */
const ENDPOINTS = Object.freeze({
  push: '/api/skill/wiki/sources',
  digest: '/api/agent/push',
});

/**
 * The first path segment of every pushed note's DISPLAY path.
 *
 * **This is not a wire field.** The server derives the stored locator itself
 * (`wiki_source_gates.locator_for`: `notebooklm/<notebook_id>/<uuid>.md`) and
 * the request model has no `path` — "nothing a skill sends can shape a stored
 * path" is the rule, and a `path` field was being dropped in silence. What
 * `buildPath` produces is what the run report and the ledger SHOW the user, so
 * the two surfaces are honest about being two surfaces.
 */
const PATH_ROOT = 'NotebookLM';

/** Mirrors javis-server `_UUID` (javis_mcp/obsidian_sources.py:122): lowercase only. */
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

/** Mirrors `_check_vault_path`'s 1024-character ceiling. */
const MAX_PATH_CHARS = 1024;

/**
 * Mirrors `LOCATOR_SEGMENT_RE` (javis-server app/wiki_source_gates.py:64): what
 * `notebook_id` must look like for the server to put it in a locator. A
 * notebook TITLE is not one — a space or a CJK character would be a hard
 * `invalid_request` — so `notebookId()` below slugifies, and omits the field
 * entirely when nothing usable survives.
 */
const NOTEBOOK_ID_RE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;

/** How much of a server-written sentence this bundle will relay (R4, R5). */
const MAX_SERVER_TEXT_CHARS = 400;

/**
 * R16's bounds, mirroring `MAX_CANARY_HEADERS` / `MAX_CANARY_NAME_CHARS` in
 * javis-server app/wiki_source_gates.py. The names reported in a push body are
 * persisted in a `wiki_logs` row, so they are bounded on the way out as well
 * as on the way in.
 */
const MAX_CANARY_HEADERS = 20;
const MAX_CANARY_NAME_CHARS = 100;

/**
 * One machine-readable code per refusal, one reason and one next action each
 * (R4, R5).
 *
 * THE FIRST EIGHT ARE THE SERVER'S OWN, name for name with
 * `REFUSAL_NEXT_STEPS` in javis-server app/services/skill_wiki_sources.py. They
 * are listed here so the Errors table the agent reads has a row for every code
 * that can arrive, and so a refusal still reads sensibly if javis-server ever
 * answers one without a `next_step` — but the server's own `error_description`
 * and `next_step` WIN whenever it sends them (see `describeRefusal`), because
 * the server computed them against the actual request.
 *
 * The rest are the transport's own: codes nothing on the server emits because
 * the request never got there, or never got past this module.
 *
 * `text_too_large` is deliberately NOT redefined here — it is normalize.js's
 * code, and a bare 413 maps onto it, so one condition keeps one name whichever
 * side notices it first. A 413 that names `payload_too_large` keeps the
 * server's name.
 */
const REFUSALS = Object.freeze({
  // --- javis-server's vocabulary ---------------------------------------
  invalid_request: {
    reason: 'javis-server refused the body: a field is missing, malformed, or the hash does not match the text as sent',
    next: 'read the error_description the refusal carries, fix that one field and push again — normalise first, then hash, never the other way round',
  },
  unsupported_source_type: {
    reason: `javis-server does not accept ${SOURCE_TYPE} on this endpoint`,
    next: 'the push endpoint or its migration is not deployed yet — report the version and stop; do not fall back to another source type',
  },
  payload_too_large: {
    reason: 'the note is over the size the ingest accepts',
    next: 'tell the user to split that note in NotebookLM, and push the parts under their own ids; the rest of the batch is unaffected',
  },
  quota_exceeded: {
    reason: 'the account already stores as many ingest sources as it is allowed',
    next: 'say the wiki is full for ingest sources and that nothing was stored; removing sources this account no longer needs is what frees it',
  },
  conflict: {
    reason: 'this source id is already held by another kind of source, or was deleted and is never reused',
    next: 'report the id and stop; do not re-push under the same id, and never retry a delete into an add',
  },
  budget_exhausted: {
    reason: 'the account has spent its wiki-ingest units for the rolling hour',
    next: 'wait for the reset the refusal names, then run push again — the notes are still staged and nothing was lost',
  },
  upstream_unavailable: {
    reason: 'javis-server recorded that this container could not reach NotebookLM at all',
    next: 'offer to re-authorise NotebookLM; no wiki content was lost and nothing was changed',
  },
  internal_error: {
    reason: 'javis-server could not store the source',
    next: 'say nothing was stored and the next run will retry; report the source id if it keeps happening',
  },
  // --- this module's own ------------------------------------------------
  unauthorized: {
    reason: 'javis-server rejected the container gateway token',
    next: 'ask Samuel to check the container is provisioned; this is a broken container, not a user error',
  },
  source_id_invalid: {
    reason: 'the note id is not a lowercase uuid, which is what a source id must be',
    next: 'report the id and stop: a NotebookLM note id is already a lowercase uuid, so this is a CLI output change',
  },
  network_error: {
    reason: 'javis-server could not be reached from this container',
    next: 'retry on the next scheduled run; nothing was written and nothing was lost',
  },
  unparseable_response: {
    reason: 'javis-server answered a success code with a body that is not JSON',
    next: 'treat the push as not landed and retry; do not record an ingest for it',
  },
});

/**
 * How long ONE javis-server call may take before it is a `network_error`.
 *
 * `fetch` with no signal is unbounded in the only way that matters here:
 * undici waits ~300s for response headers, so a javis-server that is up but
 * wedged turns any call into a five-minute block. On the scheduled run that is
 * merely slow; on `notebooks` and `notes` — which report an R16 sighting and
 * were network-free before that — it is an interactive turn that reads as a
 * hang.
 *
 * The bound lives HERE, in the one place every call already goes through, so
 * the push, the digest, the upstream report and the listing report are all
 * bounded by construction rather than one caller remembering to pass a signal.
 * It is deliberately far above any healthy call (the endpoint writes one row
 * and answers) and far below undici's default, and `deps.timeoutMs` overrides
 * it so a test can prove the bound without waiting for it.
 */
const REQUEST_TIMEOUT_MS = 30 * 1000;

/**
 * An abort signal that fires after `ms`, and the cleanup that un-arms it.
 *
 * The timer is unref'd and cleared on every exit path, so a bound that exists
 * to stop a hang never becomes one itself: a finished call leaves nothing
 * holding the event loop open, which on a cron turn is the difference between
 * a process that exits and a process that lingers for the whole timeout.
 */
function startTimeout(ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => {
    controller.abort(new Error(`javis-server did not answer within ${ms} ms`));
  }, ms);
  if (typeof timer.unref === 'function') timer.unref();
  return { signal: controller.signal, done: () => clearTimeout(timer) };
}

function requireToken() {
  const t = process.env.OPENCLAW_GATEWAY_TOKEN;
  if (!t) {
    throw new Error(
      'OPENCLAW_GATEWAY_TOKEN is required (injected inside the openclaw container).'
    );
  }
  return t;
}

/** One bounded line of server-written prose, or null. */
function serverText(value) {
  if (typeof value !== 'string') return null;
  const s = value.trim();
  return s ? s.slice(0, MAX_SERVER_TEXT_CHARS) : null;
}

/**
 * POST json to `path` and return the parsed body.
 *
 * Carried from gmail-wiki-ingest unchanged in behaviour, with one addition:
 * every call is bounded by `REQUEST_TIMEOUT_MS` (or `deps.timeoutMs`). A
 * timeout is a `network_error` like any other unreachable server — nothing was
 * written and the next run retries — so no caller gains a new code to handle,
 * only a bound. The method is hardcoded: there is no parameter that could make
 * this a read (R19).
 */
async function postJson(path, body, deps = {}) {
  const fetchFn = deps.fetch || globalThis.fetch;
  const token = deps.token || requireToken();
  const ms = Number(deps.timeoutMs) > 0 ? Number(deps.timeoutMs) : REQUEST_TIMEOUT_MS;
  const clock = startTimeout(ms);
  try {
    let res;
    try {
      res = await fetchFn(`${SERVER}${path}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
        signal: clock.signal,
      });
    } catch (e) {
      return {
        status: 'error',
        error: 'network_error',
        detail: clock.signal.aborted
          ? `timed out after ${ms} ms`
          : String((e && e.message) || e),
      };
    }

    let parsed = null;
    try {
      parsed = await res.json();
    } catch (_) {
      parsed = null;
    }
    if (!res.ok) {
      const envelope = {
        status: 'error',
        error: errorCodeFor(res.status, parsed),
        http_status: res.status,
        detail: parsed,
      };
      // R5 lives here. javis-server computes one action per refusal against the
      // actual request (`REFUSAL_NEXT_STEPS`), and the only way it can reach the
      // user is if the transport carries it up instead of dropping it for a
      // generic "report the code and stop".
      if (parsed && typeof parsed === 'object') {
        const described = serverText(parsed.error_description);
        const next = serverText(parsed.next_step);
        if (described) envelope.error_description = described;
        if (next) envelope.next_step = next;
      }
      return envelope;
    }
    if (parsed == null || typeof parsed !== 'object') {
      return { status: 'error', error: 'unparseable_response', detail: `http_${res.status}` };
    }
    return parsed;
  } finally {
    clock.done();
  }
}

/**
 * The server's own code when it sends one, else the code its status means.
 *
 * The status fallback exists because R4 requires a named reason for every
 * refusal, including the ones that never reach application code — a 401 from an
 * ingress and a 413 from a body-size guard both have to arrive as something the
 * Errors table has a row for.
 */
function errorCodeFor(status, parsed) {
  const named = parsed
    && ((parsed.detail && parsed.detail.error) || parsed.error);
  if (typeof named === 'string' && named.trim()) return named.trim();
  if (status === 401 || status === 403) return 'unauthorized';
  if (status === 413) return 'text_too_large';
  return `http_${status}`;
}

/**
 * Did this envelope land?
 *
 * Three shapes say no: postJson's own failure envelope (`status: 'error'`), the
 * server's refusal envelope (`status: 'refused'`, which arrives with a 4xx/5xx
 * and so normally through postJson, but is read directly too), and any envelope
 * carrying an `error` code. A 2xx answer sets `error: null`, so a successful
 * push is never mistaken for a refusal.
 */
function failed(envelope) {
  if (!envelope) return true;
  if (envelope.status === 'error' || envelope.status === 'refused') return true;
  return Boolean(envelope.error);
}

/**
 * The reason-and-next-action pair for a refusal envelope (R4, R5).
 *
 * THE SERVER'S WORDS WIN. It answered this exact request and its
 * `error_description` names the field; its `next_step` is the action it
 * computed. The local table is the fallback for a code that arrived without
 * them, and an unknown code is NOT dressed up as a known one: it comes back
 * with its own name, so a server that grows a code this bundle has not met yet
 * is reported accurately rather than mislabelled.
 */
function describeRefusal(envelope) {
  const code = (envelope && envelope.error) || 'unknown_error';
  const known = REFUSALS[code];
  const said = serverText(envelope && envelope.error_description);
  const next = serverText(envelope && envelope.next_step);
  return {
    code,
    reason: said
      || (known && known.reason)
      || `javis-server refused the push with the code ${code}`,
    next: next
      || (known && known.next)
      || 'report the code verbatim and stop; do not retry a refusal this skill does not recognise',
  };
}

/**
 * One DISPLAY path per note: `NotebookLM/<notebook>/<title>.md`.
 *
 * Never sent on the wire (see `PATH_ROOT`). The rules are still javis-server's
 * `_check_vault_path`, because what the user is shown should be a path the wiki
 * could hold: relative, no empty / `.` / `..` segment, `.md` suffix, and never
 * under `Javis-wiki`. A separator inside a title becomes a hyphen rather than a
 * new segment, because a note called `A/B` is one note.
 */
function buildPath(notebook, title, sourceId) {
  const segment = (value, fallback) => {
    const s = String(value == null ? '' : value)
      .replace(/[\\/]+/g, '-')
      .replace(/[\u0000-\u001F\u007F]/g, '')
      .replace(/\s+/g, ' ')
      .trim()
      .replace(/^\.+/, '')
      .trim();
    return s || fallback;
  };
  const book = segment(notebook, 'notebook');
  const name = segment(title, String(sourceId || 'note'));
  let path = `${PATH_ROOT}/${book}/${name}.md`;
  if (path.length > MAX_PATH_CHARS) {
    // Truncate the NOTE name, never the root or the notebook: the first two
    // segments are what makes the provenance readable (R17).
    const room = MAX_PATH_CHARS - `${PATH_ROOT}/${book}/.md`.length;
    path = `${PATH_ROOT}/${book}/${name.slice(0, Math.max(1, room))}.md`;
  }
  return path;
}

/**
 * The notebook as a `notebook_id` the server will accept, or null.
 *
 * R17's readable provenance: with it the stored locator is
 * `notebooklm/<notebook>/<uuid>.md`, without it `notebooklm/<uuid>.md`. So the
 * field is worth deriving — but `check_namespace` refuses anything outside
 * `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`, which a notebook TITLE routinely is not.
 * Slugify, and when nothing usable survives (a title that is entirely CJK, say)
 * send NOTHING: a locator without a notebook segment is a worse locator, but a
 * hard `invalid_request` would be no ingest at all.
 */
function notebookId(value) {
  const raw = String(value == null ? '' : value).trim();
  if (!raw) return null;
  if (NOTEBOOK_ID_RE.test(raw)) return raw;
  const slug = raw
    .replace(/[^A-Za-z0-9._-]+/g, '-')
    .replace(/^[^A-Za-z0-9]+/, '')
    .replace(/[-_.]+$/, '')
    .slice(0, 128);
  return NOTEBOOK_ID_RE.test(slug) ? slug : null;
}

/**
 * The pages one push answer names, in the shape the digest renders (R20).
 *
 * The server's envelope carries `page` — the source page, with `action`
 * `create` or `update` — and `feeds`, the pages the ledger already says this
 * source contributes to. There is no `pages` key and there never was; reading
 * one produced an empty list on every push, so the success card listed nothing,
 * the ledger recorded `pages: 0` forever, and a dry run reported no pages at
 * all. No `url` either: the envelope names pages by slug (R19 — it hands back
 * no content), so a page renders unlinked unless javis-server starts sending
 * one.
 */
/**
 * The server's own body, whichever wrapper it arrived in.
 *
 * A 2xx IS the envelope. A refusal comes back through `postJson`, which keeps
 * the parsed body under `detail` so the transport's own fields (`http_status`,
 * `network_error`) cannot collide with the server's. The account-wide facts —
 * the budget and the canary — are on BOTH, and R9 and R16 are about the
 * account, so they have to be readable either way.
 */
function payloadOf(envelope) {
  if (!envelope || typeof envelope !== 'object') return null;
  if (envelope.detail && typeof envelope.detail === 'object' && !Array.isArray(envelope.detail)) {
    return envelope.detail;
  }
  return envelope;
}

function pagesFrom(envelope) {
  const rows = [];
  const push = (p) => {
    if (!p || typeof p !== 'object') return;
    const slug = String(p.slug || '').trim();
    if (!slug) return;
    if (rows.some((r) => r.slug === slug)) return;
    rows.push({
      title: slug,
      slug,
      page_type: String(p.page_type || ''),
      url: p.url ? String(p.url) : null,
      status: String(p.action || '').toLowerCase() === 'create' ? 'new' : 'updated',
    });
  };
  const body = payloadOf(envelope);
  push(body && body.page);
  for (const p of (body && Array.isArray(body.feeds) ? body.feeds : [])) push(p);
  return rows;
}

/**
 * R9's budget, as javis-server states it:
 * `{units_per_hour, units_remaining, window_seconds, shared_with}`. Returned
 * as-is and rendered verbatim — the number is the server's, never this
 * bundle's arithmetic.
 */
function budgetFrom(envelope) {
  const body = payloadOf(envelope);
  const b = body && body.budget;
  return b && typeof b === 'object' && !Array.isArray(b) ? b : null;
}

/** R16: whether this answer says a `Sec-Session-*` header reached the account. */
function canaryFrom(envelope) {
  const body = payloadOf(envelope);
  const c = body && body.canary;
  if (!c || typeof c !== 'object' || !c.flagged) return null;
  return {
    flagged: true,
    first: Boolean(c.first),
    headers: (Array.isArray(c.headers) ? c.headers : []).slice(0, 10).map(String),
  };
}

/**
 * A `response_headers` body the server will read, or null (R16).
 *
 * Takes the names the CLI boundary extracted (an array) or an already-built
 * header object, and answers the shape `sec_session_headers` reads: a plain
 * object keyed by NAME. **Every value is the empty string.** The server only
 * ever looks at keys, and a `Sec-Session-*` value is a device-binding
 * challenge sitting next to a cookie — there is no version of this skill that
 * sends one.
 *
 * Bounded here as well as on the server (`MAX_CANARY_HEADERS`) because these
 * names end up in a `wiki_logs` row, and a bound that only exists at the far
 * end is a bound this bundle is not keeping.
 */
function canaryHeadersBody(value) {
  if (!value) return null;
  const names = Array.isArray(value)
    ? value
    : (typeof value === 'object' ? Object.keys(value) : []);
  const out = {};
  for (const raw of names) {
    if (typeof raw !== 'string') continue;
    const name = raw.toLowerCase().replace(/[^a-z0-9._-]/g, '').slice(0, MAX_CANARY_NAME_CHARS);
    if (!name) continue;
    out[name] = '';
    if (Object.keys(out).length >= MAX_CANARY_HEADERS) break;
  }
  return Object.keys(out).length ? out : null;
}

/**
 * Push one note. The whole content-write surface of this skill (R2).
 *
 * `dryRun` is a field on the one endpoint rather than a second route, so there
 * is exactly one way NotebookLM content enters and the dry run cannot
 * accidentally become a second, less-checked door (R3). `source_id` is the
 * NotebookLM note uuid verbatim (F65) — no mapping table, and refused here if
 * it ever stops being a lowercase uuid.
 *
 * EVERY FIELD IN THIS BODY IS ONE THE SERVER DECLARES. `WikiSourcePushRequest`
 * takes no `skill`, no `path` and no `notebook`; pydantic drops unknown keys
 * without a word, so sending them looked like a contract and was a silence.
 *
 * `responseHeaders` is R16's other door. `reportUpstream` carries a sighting
 * that stopped a run, but a canary seen on a run that still has notes to push
 * reaches the server HERE or nowhere: `_canary` reads `response_headers` off
 * whatever push arrives, and with no caller ever setting the key it got `None`
 * every time and the `source_canary` row was never written.
 */
async function pushSource(note, deps = {}) {
  const sourceId = String((note && note.sourceId) || '');
  if (!UUID_RE.test(sourceId)) {
    return Object.assign(
      { status: 'error', error: 'source_id_invalid', detail: sourceId.slice(0, 80) },
      REFUSALS.source_id_invalid,
    );
  }

  const body = {
    source_type: SOURCE_TYPE,
    source_id: sourceId,
    op: 'upsert',
    title: String((note && note.title) || ''),
    text: String((note && note.text) || ''),
    body_hash: String((note && note.bodyHash) || ''),
    dry_run: note && note.dryRun === true,
  };
  const namespace = notebookId(note && note.notebook);
  if (namespace) body.notebook_id = namespace;

  const headers = canaryHeadersBody(note && note.responseHeaders);
  if (headers) body.response_headers = headers;

  return postJson(ENDPOINTS.push, body, deps);
}

/**
 * Tell javis-server the container could not reach NotebookLM at all (R16, R4).
 *
 * The one push a run makes when it never got as far as a note. Two things it
 * is for, and neither can be done from inside the container:
 *
 *   - **R16.** The server records the FIRST `Sec-Session-*` ever reported for
 *     this account (`wiki_logs`, op `source_canary`). A canary that only ever
 *     printed one line into one chat turn cannot tell the first appearance from
 *     the hundredth, which is the whole content of the requirement.
 *   - **R4/R5.** `upstream_error` is the field the endpoint declares for
 *     exactly this, and it answers `upstream_unavailable` with the
 *     re-authorise action. So a dead session leaves a server-side trace instead
 *     of silence.
 *
 * The expected answer is a REFUSAL (502): nothing is stored, which is right —
 * there is nothing to store. The caller treats it as an acknowledgement.
 */
async function reportUpstream({ sourceId, upstreamError, responseHeaders } = {}, deps = {}) {
  const id = String(sourceId || '');
  if (!UUID_RE.test(id)) {
    return Object.assign(
      { status: 'error', error: 'source_id_invalid', detail: id.slice(0, 80) },
      REFUSALS.source_id_invalid,
    );
  }
  const body = {
    source_type: SOURCE_TYPE,
    source_id: id,
    op: 'upsert',
    dry_run: false,
    upstream_error: String(upstreamError || 'unreachable').slice(0, 200),
  };
  const headers = canaryHeadersBody(responseHeaders);
  if (headers) body.response_headers = headers;
  return postJson(ENDPOINTS.push, body, deps);
}

/**
 * Push the run digest to the user's chat (R10, R20).
 *
 * NO `session_id` and NO `dedup_key`, following gmail-wiki-ingest for the same
 * reason: with neither set the server resolves `session_source="history"` and
 * the message appends to this skill's existing thread rather than branching the
 * chat tree on every run.
 */
async function pushDigest(content, deps = {}) {
  const text = String(content == null ? '' : content);
  if (!text.trim()) return { status: 'error', error: 'empty_digest' };
  return postJson(ENDPOINTS.digest, { skill: SKILL, content: text }, deps);
}

module.exports = {
  SERVER,
  SKILL,
  SOURCE_TYPE,
  ENDPOINTS,
  PATH_ROOT,
  UUID_RE,
  MAX_PATH_CHARS,
  MAX_CANARY_HEADERS,
  MAX_CANARY_NAME_CHARS,
  NOTEBOOK_ID_RE,
  REQUEST_TIMEOUT_MS,
  REFUSALS,
  postJson,
  errorCodeFor,
  failed,
  describeRefusal,
  buildPath,
  notebookId,
  payloadOf,
  pagesFrom,
  budgetFrom,
  canaryFrom,
  canaryHeadersBody,
  pushSource,
  reportUpstream,
  pushDigest,
};
