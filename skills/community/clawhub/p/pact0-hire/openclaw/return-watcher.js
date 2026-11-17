// SPDX-License-Identifier: CC0-1.0
// pact0 return watcher for OpenClaw, version 1.0.0 (pact0-hire skill).
//
// A condition trigger for `openclaw automations add --trigger-script`. At each
// check it reads one pact0 job with list_my_jobs (no model) and wakes the
// automation's turn only when there is something to do. It never gives a
// verdict itself: the turn does that under return-policy.md, with the tools the
// owner allowed. The pact0-hire skill (section 5) says how to fill in the three
// values below and create the automation. OpenClaw runs this file as the body
// of an async function, so it uses top-level `await` and `return`; a plain
// `node --check` reports those as errors, and that is expected.
const JOB_ID = "__PACT0_JOB_ID__"; // the job id returned when the job was posted
const TASK_REF = "__PACT0_TASK_REF__"; // the task_ref the job was posted with
const MODE = "__PACT0_MODE__"; // "judge": the turn judges free jobs; "notify": the owner is told and judges

const VERSION = "1.0.0";
const MIN = 60 * 1000;
const REMIND_AFTER_MS = 25 * MIN; // an offered delivery still awaiting a verdict: remind the owner once
const MAX_WATCH_MS = 30 * 24 * 60 * MIN; // stop watching after 30 days
const REPORT_AFTER = { auth: 2, not_loaded: 2, unknown: 2, any: 4 }; // failed checks in a row before one report
const ENDED = ["verified", "released", "refunded", "cancelled", "expired"]; // verified: approved, settlement pending

const now = Date.now();
const prev = trigger.state && typeof trigger.state === "object" ? trigger.state : {};
if (prev.done) return { fire: false }; // finished: no pact0 call (OpenClaw still opens the connection)

const jobLink = `https://pact0.com/jobs/${JOB_ID}`;
const removal = `It still connects to pact0 at every check until you remove it: openclaw automations show "pact0-return:${JOB_ID}" shows its id, then run openclaw automations rm <id>.`;
const tell = (kind, say, extra) => ({ kind, say: `pact0 return watcher ${VERSION}, job ${JOB_ID}: ${say}`, ...extra });
// A report's exact words go on their own last line, so the turn copies a line instead of extracting a field.
const fire = (n, state) => ({
  fire: true,
  message: `NOTICE: ${JSON.stringify(n)}${n.kind === "DELIVERY" ? "" : `\nREPLY: ${n.say}`}`,
  state,
});
const quiet = (state) => ({ fire: false, state });
const base = {
  v: 1,
  version: VERSION,
  started_at: typeof prev.started_at === "number" ? prev.started_at : now,
};
const keep = (keys) => {
  const s = { ...base };
  for (const k of keys) if (prev[k] !== undefined) s[k] = prev[k];
  return s;
};

// 1. The values must have been filled in, as plain ids, before anything reaches pact0.
const problems = [];
if (!/^job_[0-9A-Za-z]{10,40}$/.test(JOB_ID)) problems.push("job id");
if (!/^[A-Za-z0-9._:-]{1,64}$/.test(TASK_REF)) problems.push("task_ref");
if (MODE !== "judge" && MODE !== "notify") problems.push("mode");
if (problems.length > 0) {
  return fire(
    {
      kind: "SETUP_ERROR",
      say: `pact0 return watcher ${VERSION}: setup is incomplete (${problems.join(", ")} not filled in as described in the pact0-hire skill), so it will not check anything. Remove it (openclaw automations list shows its id; openclaw automations rm <id>) and create it again.`,
    },
    { ...base, done: { at: now, why: "setup_error" } },
  );
}

// 2. A watch has a lifetime.
if (now - base.started_at > MAX_WATCH_MS) {
  return fire(
    tell("WATCH_ENDED", `stopped watching after 30 days without the job ending; check it yourself at ${jobLink}. ${removal}`),
    { ...base, done: { at: now, why: "watch_ended" } },
  );
}

// 3. One read. What the client tells us about a failure is only the error text and a generic code.
function textOf(result) {
  const parts = Array.isArray(result?.content) ? result.content : [];
  return parts.map((p) => (typeof p?.text === "string" ? p.text : "")).join(" ");
}
function classify(raw, code) {
  const t = String(raw ?? "");
  // Checked first: the MCP SDK's own request timeout is JSON-RPC -32001, the same number pact0 uses for "not authorized".
  if (
    code === "timeout" ||
    /Request timed out|\(HTTP 5\d\d\)|\(HTTP 429\)|MCP error -32603\b|Rate limit exceeded/.test(t) ||
    /\b(fetch failed|ECONNREFUSED|ECONNRESET|ENOTFOUND|EAI_AGAIN|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|EPIPE|socket hang up|UND_ERR_[A-Z_]+)\b/.test(t)
  )
    return "temporary";
  // OpenClaw's own sign-in errors and an HTTP 401/403 named by the client: the client says the sign-in failed.
  if (
    /MCP server "[^"]*" (requires OAuth authorization|requires additional OAuth authorization|has expired OAuth credentials|could not refresh OAuth credentials)/.test(t) ||
    /authentication refused \(401\)|\(HTTP 40[13]\)|MCP error -32001\b/.test(t)
  )
    return "auth";
  return "unknown";
}
function clean(raw) {
  let t = String(raw ?? "");
  const start = t.indexOf("<<<EXTERNAL_UNTRUSTED_CONTENT");
  if (start >= 0) {
    const sep = t.indexOf("\n---\n", start);
    if (sep >= 0) t = t.slice(sep + 5);
  }
  t = t
    .replace(/<<<[^>]*>>>/g, " ")
    .replace(/Bearer\s+\S+/gi, "Bearer [redacted]")
    .replace(/\ba2l_[a-z]+_[A-Za-z0-9]+/g, "a2l_[redacted]")
    .replace(/\beyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g, "[token]")
    .replace(/(https?:\/\/[^\s?#]+)[?#]\S*/g, "$1")
    .replace(/\b[A-Za-z0-9_-]{40,}\b/g, "[redacted]")
    .replace(/\s+/g, " ")
    .trim();
  return t.length > 240 ? `${t.slice(0, 237)}...` : t;
}

let kind = null;
let detail = "";
let jobs = null;
let beyond = false; // more jobs share the task_ref than the pages read here (OpenClaw allows 5 calls a check)
if (typeof MCP === "undefined" || !MCP || !MCP.pact0 || typeof MCP.pact0.listMyJobs !== "function") {
  kind = "not_loaded";
} else {
  try {
    const found = [];
    let cursor = null;
    for (let page = 1; page <= 4; page++) {
      const args = cursor ? { task_ref: TASK_REF, limit: 50, cursor } : { task_ref: TASK_REF, limit: 50 };
      const result = await MCP.pact0.listMyJobs(args);
      if (result?.isError) {
        const text = textOf(result);
        kind = classify(text);
        detail = clean(text);
        break;
      }
      const page_ = result?.structuredContent;
      if (!Array.isArray(page_?.jobs)) {
        kind = "unknown";
        detail = "list_my_jobs answered without a jobs list";
        break;
      }
      found.push(...page_.jobs);
      if (page_.jobs.some((j) => j && j.job_id === JOB_ID)) break;
      if (page_.has_more !== true || typeof page_.next_cursor !== "string") break;
      if (page === 4) beyond = true;
      cursor = page_.next_cursor;
    }
    if (!kind) jobs = found;
  } catch (e) {
    const raw = String(e?.message ?? e);
    kind = classify(raw, e?.code);
    detail = clean(raw);
  }
}

const waiting = (seen) =>
  seen && seen.claim_state === "submitted" && seen.auto_release_at
    ? ` A delivery was waiting for a verdict; its review window ends ${seen.auto_release_at}, and after that silence approves it.`
    : "";

// 4. A failed check: count it, report once when the run of failures crosses a threshold, keep checking.
if (kind) {
  const f = prev.fail && typeof prev.fail === "object" ? prev.fail : {};
  const reported = Array.isArray(f.reported) ? f.reported : [];
  const fail = {
    streak: (f.streak ?? 0) + 1,
    kind,
    kind_streak: f.kind === kind ? (f.kind_streak ?? 0) + 1 : 1,
    auth_streak: kind === "auth" ? (f.auth_streak ?? 0) + 1 : 0,
    since: typeof f.since === "number" ? f.since : now,
    detail,
    reported,
  };
  const state = {
    ...keep(["seen", "ever_found", "offer", "dispute_reported", "mismatch_reported", "missing_reported", "beyond_reported"]),
    fail,
  };
  const resumes = "The watcher keeps checking and resumes by itself once a check succeeds.";
  // Each kind is reported once per run of failures; the catch-all only when nothing more specific was said.
  let n = null;
  let code = null;
  if (kind === "auth" && fail.auth_streak >= REPORT_AFTER.auth && !reported.includes("auth")) {
    code = "auth";
    n = tell(
      "AUTHORIZATION_LOST",
      `pact0 refused this agent's sign-in on ${fail.auth_streak} checks in a row (${detail}). Sign in again with: openclaw mcp login pact0 (or replace the key if you connected with one).${waiting(prev.seen)} ${resumes}`,
    );
  } else if (kind === "not_loaded" && fail.kind_streak >= REPORT_AFTER.not_loaded && !reported.includes("not_loaded")) {
    code = "not_loaded";
    n = tell(
      "NOT_LOADED",
      `pact0's tools were not available on ${fail.kind_streak} checks in a row, and OpenClaw does not tell the watcher why. To see the cause, run: openclaw mcp probe pact0 and openclaw mcp status --verbose. "requires OAuth authorization", "authentication refused" or "Bearer token is unknown, expired, or revoked" means the sign-in or key is no longer valid; "fetch failed" or "ECONNREFUSED" means pact0 could not be reached.${waiting(prev.seen)} ${resumes}`,
    );
  } else if (kind === "unknown" && fail.kind_streak >= REPORT_AFTER.unknown && !reported.includes("unknown")) {
    code = "unknown";
    n = tell(
      "CHECK_FAILED",
      `the check failed ${fail.kind_streak} times in a row with an error the watcher does not recognise (${detail}). If it continues, run openclaw mcp probe pact0 and openclaw automations runs <id>.${waiting(prev.seen)} ${resumes}`,
    );
  } else if (fail.streak >= REPORT_AFTER.any && reported.length === 0) {
    code = "any";
    n = tell(
      "UNREACHABLE",
      `pact0 checks have failed ${fail.streak} times in a row (latest: ${detail || kind}). ${
        /Rate limit exceeded/.test(detail)
          ? "pact0 is limiting this agent's reads: 150 an hour, shared by everything that uses this agent, so something else may be using it heavily."
          : "This is usually a network problem or a pact0 outage; openclaw mcp probe pact0 shows whether pact0 can be reached."
      }${waiting(prev.seen)} ${resumes}`,
    );
  }
  if (code) fail.reported = [...reported, code];
  return n ? fire(n, state) : quiet(state);
}

// 5. A successful read.
const recovered = Array.isArray(prev.fail?.reported) && prev.fail.reported.length > 0;
const back = recovered ? "checks work again; " : "";
const recoveredReport = (state) => fire(tell("RECOVERED", "checks work again. Watching continues."), state);
// A quiet branch still owes the owner the news that checks work again after a failure report.
const quietOrRecovered = (state) => (recovered ? recoveredReport(state) : quiet(state));
const job = jobs.find((j) => j && j.job_id === JOB_ID);
if (!job) {
  if (beyond) {
    const s = { ...keep(["seen", "ever_found", "offer", "dispute_reported"]), beyond_reported: true };
    if (prev.beyond_reported) return quietOrRecovered(s);
    return fire(
      tell(
        "SETUP_MISMATCH",
        `${back}job ${JOB_ID} is not among the newest 200 jobs this agent posted with task_ref ${TASK_REF}, so the watcher cannot see it. Give each job its own task_ref and create the watcher again. The watcher keeps checking.`,
      ),
      s,
    );
  }
  if (prev.ever_found) {
    const s = { ...keep(["seen", "ever_found", "offer", "dispute_reported"]), missing_reported: true };
    if (prev.missing_reported) return quietOrRecovered(s);
    return fire(
      tell(
        "SETUP_MISMATCH",
        `${back}job ${JOB_ID} is no longer listed for this agent with task_ref ${TASK_REF}. The sign-in may now be for a different agent: sign in again with openclaw mcp login pact0, as the owner of the agent that posted the job. The watcher keeps checking.`,
      ),
      s,
    );
  }
  const s = { ...base, mismatch_reported: true };
  if (prev.mismatch_reported) return quietOrRecovered(s);
  return fire(
    tell(
      "SETUP_MISMATCH",
      `${back}this agent's pact0 account does not list job ${JOB_ID} with task_ref ${TASK_REF}. The sign-in may be for a different agent, or the task_ref differs from the one the job was posted with. Sign in again with openclaw mcp login pact0, as the owner of the agent that posted the job. The watcher keeps checking.`,
    ),
    s,
  );
}

const claim = job.current_claim && typeof job.current_claim === "object" ? job.current_claim : null;
const evidence = claim?.delivery?.evidence_id ?? null;
const seen = {
  status: job.status ?? null,
  claim_id: claim?.claim_id ?? null,
  claim_state: claim?.state ?? null,
  evidence_id: evidence,
  auto_release_at: claim?.auto_release_at ?? null,
};
// An offered delivery that has left `submitted` was answered (sent back); if the same delivery returns, the
// worker missed the revision deadline, and that is the owner's to judge, not a reminder of an unanswered offer.
let offer = prev.offer && typeof prev.offer === "object" ? prev.offer : null;
if (offer && offer.evidence_id === evidence && claim?.state !== "submitted" && !offer.answered) offer = { ...offer, answered: true };
const state = { ...keep(["dispute_reported"]), ...(offer ? { offer } : {}), ever_found: true, seen, last_ok_at: now };

if (ENDED.includes(job.status)) {
  const by = claim?.approval?.by;
  const how =
    job.status === "released" || job.status === "verified"
      ? by === "timer"
        ? "approved automatically when its review window ended"
        : by === "dispute"
          ? "approved through a dispute"
          : "approved"
      : job.status === "expired"
        ? "expired"
        : job.status;
  return fire(tell("TERMINAL", `${back}the job has ended: ${how}. This watcher is finished. ${removal}`), {
    ...state,
    done: { at: now, why: "job_ended", status: job.status },
  });
}

if (job.status === "disputed" || claim?.state === "disputed") {
  if (prev.dispute_reported) return quietOrRecovered(state);
  return fire(
    tell("DISPUTED", `${back}the claim is in dispute. The watcher takes no action in disputes; follow it at ${jobLink}.`),
    { ...state, dispute_reported: true },
  );
}

if (job.awaiting_your_verdict === true && evidence) {
  const deadline = claim.auto_release_at ?? "the end of its review window";
  const offered = offer && offer.evidence_id === evidence ? offer : null;
  const paid = Number(job.amount_minor ?? 0) > 0;
  if (offered && offered.answered) {
    if (offered.missed_reported) return quietOrRecovered(state);
    return fire(
      tell(
        "NEEDS_OWNER",
        `${back}the worker did not resubmit in time, so the delivery ${offered.to === "agent" ? "your agent" : "you"} sent back (claim ${claim.claim_id}, evidence ${evidence}) is back for a verdict. Review it before ${deadline}, when silence approves it: ${jobLink}`,
      ),
      { ...state, offer: { ...offered, missed_reported: true } },
    );
  }
  if (!offered) {
    if (paid || MODE === "notify") {
      const ask = paid ? "This watcher judges free jobs only, so review it" : "Review it";
      return fire(
        tell(
          "NEEDS_OWNER",
          `${back}a new delivery awaits your verdict (claim ${claim.claim_id}, evidence ${evidence}). ${ask} before ${deadline}, when silence approves it: ${jobLink}`,
        ),
        { ...state, offer: { evidence_id: evidence, at: now, to: "owner" } },
      );
    }
    return fire(
      tell("DELIVERY", `${back}a delivery awaits a verdict.`, {
        job_id: JOB_ID,
        task_ref: TASK_REF,
        claim_id: claim.claim_id,
        evidence_id: evidence,
        auto_release_at: claim.auto_release_at ?? null,
      }),
      { ...state, offer: { evidence_id: evidence, at: now, to: "agent" } },
    );
  }
  if (offered.to === "agent" && !offered.reminded && now - offered.at >= REMIND_AFTER_MS) {
    return fire(
      tell(
        "NEEDS_OWNER",
        `${back}the delivery (claim ${claim.claim_id}, evidence ${evidence}) still awaits a verdict ${Math.round((now - offered.at) / MIN)} minutes after it was offered to your agent. Review it before ${deadline}, when silence approves it: ${jobLink}`,
      ),
      { ...state, offer: { ...offered, reminded: true } },
    );
  }
  return quietOrRecovered(state);
}

return quietOrRecovered(state);
