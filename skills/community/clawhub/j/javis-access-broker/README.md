# javis-access-broker

The instructions for Javis's **access broker**: the dedicated openclaw agent that
answers an outside agent's `ask_javis` request with only the minimum the stated
task needs (agent-access spec R2, R4, R6, R11).

This is not a store skill. It has no `metadata.routes`, it is not listed in
`hijavis-skills.json`, and it is never installed into the user's workspace.

## How it is delivered

1. `/jv-deploy` tags a release as `javis-access-broker-v<version>` on
   `DeepShareAI/ClawSkills` (version from `package.json`).
2. javis-server fetches that tag through `github_skill_source` (the per-skill tag
   ref `<slug>-v<version>`; no catalog entry is needed), reads `SKILL.md` and
   strips the front matter.
3. For each `ask_javis` request, javis-server calls the per-user openclaw
   container's `/v1/responses` with:
   - `model: "openclaw/access-broker"`, `user: "access_<request_id>"` (one session
     per request);
   - `instructions`: the `SKILL.md` body;
   - `tools`: only `access_slice_list`, `access_slice_read`,
     `access_submit_answer`, served by javis-server and bound to this request's
     slice;
   - `input`: the `ACCESS REQUEST <id>` block, with all agent text wrapped in
     `<agent_claim>…</agent_claim>`.

Because the agent has no file-reading tool, everything the broker does must live
in the `SKILL.md` body. `references/` is for people and tests only.

## Security model

The model is never the only boundary. The server decides what the broker may see
and checks what it produces:

- **Agent entry** (`agents.entries.access-broker`, written by javis-server's
  `gateway_config_factory`): its own empty workspace and `tools.allow` set to the
  three slice tools. No exec, sessions, memory, browser or elevated tools. A skill
  cannot widen its own tools.
- **Slice**: javis-server builds a small per-request slice (up to 12 wiki pages,
  3 conversation excerpts, a few to-do/calendar/spend items). `access_slice_read`
  on any other id returns `not_in_slice`.
- **Answer check** (deterministic, server side): points must be non-empty, every
  source must be a slice id, exact words only from excerpt segments inside the
  window, a valid `task_kind`. A failure refuses the answer and the agent gets
  `declined{answer_check_failed}`. Exact words are fetched by segment id, never
  taken from model text.
- **Gate**: cited categories decide whether the user must approve on their phone
  (presets, 7-day grants). The broker's draft is held only until delivery, deny,
  expiry or stop.
- **Prompt injection**: agent text and slice content are data. The body tells the
  broker never to follow instructions in either, and the checks above hold even
  when it does.

## Handed-over tasks (0.2.0)

When the agent holds a to-do or spending item the user handed over in HiJavis,
javis-server adds a `HANDED-OVER TASK` block (the task, the user's item and a
consent line) to the request and puts the item first in the slice. The broker
then shares only the facts the item needs, one per point, each with `sources`
and a short `label` (80 characters or fewer, for example "Launch date: Fri Nov
21"). javis-server stores the labels as the task's shared-facts record and adds
the closing "Nothing else was shared." line itself, so the broker never writes
it. Conversations, voice memos and Gmail still go to the user's approval card.
Requests without the block are handled exactly as in 0.1.x, and the server
ignores `label` on them.

## 0.2.1

- The hand-over lets Javis share the item itself and the matching to-dos and
  calendar items without asking, and the broker answers from those first. A
  question that is only what the item is, or when it is due or was noted, is
  answered from the item alone.
- The broker cites a wiki page, conversation or voice memo only for a fact the
  task needs that the item, to-dos and calendar do not hold, never for an
  unrelated fact such as other discussion in the same recording. javis-server
  sends anything the hand-over does not cover (wiki pages built from
  conversations, conversations, voice memos and Gmail) to the user's approval
  card per the user's own rules. A category the user set to Ask me waits for
  their approval; a category set to Always, or a live grant for that agent,
  shares the answer without a card. The broker does not decide which applies.
- Every `answer` has at least one point: `points` is an array of
  `{text, sources}` objects, also for `kind: exact`; `exact_segments` is an
  optional addition. With nothing to write, the broker declines
  (`nothing_to_share`, or a reason for a full-transcript or bulk ask).
  `access_submit_answer` refuses an answer that fails the point checks (no
  points, a malformed or empty point, a point without sources) with
  `answer_refused`, a reason and a fix hint, and the broker submits again. The
  schema keeps `points` an array: `invalid-answer-without-points.json` fails it
  and the server refuses it; `invalid-points-as-string.json` fails the schema,
  though javis-server parses a JSON-string `points` value and accepts it.

`references/submit-answer.schema.json` mirrors the static part of the answer
check. `references/examples/` holds valid and invalid submissions.
`references/schema-lite.js` is the dependency-free validator the tests use.

## 0.2.2

- A label only names what its point's text says. Javis drops the label of any
  point that cites an excerpt (conversation or voice-memo words).
- Labels on an answer that goes to the user's approval card are shown on the
  card next to each point's text. javis-server keeps a label on the task's
  shared-facts record only if the user's app showed it and the user approved.
- An exact (verbatim) answer carries no labels.

## Iterating from history

Every exchange is recorded by javis-server (`agent_access_requests`, `_turns`,
`_slice_items`, `_reads`): the task, the question, what the broker opened, what
it submitted, the decision and any refusal reason. To improve the broker:

1. Look at refused requests (`state = refused`, `refusal_reason`), declines and
   `ask_agent` loops, and at what was opened versus cited.
2. Change the `SKILL.md` body. Keep it under 20,000 characters (openclaw's
   bootstrap limit) and name no tools beyond the three slice tools.
3. Run the tests, bump `package.json`, and let `/jv-deploy` tag the new version.
4. On a test account with `AGENT_ACCESS_TEST_HOOKS=1`, `POST
   /api/agent-access/test/inject` can replay a fixed `broker_reply` (the same
   shape as `access_submit_answer`) through the answer check without a model.

## Tests

```bash
cd javis-access-broker && node --test   # this skill only
node --test test/                        # from the ClawSkills root, every suite
```
