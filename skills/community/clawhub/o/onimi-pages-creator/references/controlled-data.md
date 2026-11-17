# Controlled collaboration

Read this when sharing should collect information or save contributions. Reuse an explicit choice;
otherwise clarify local-only interaction versus cloud saving. Do not infer cloud storage from a button,
filter, animation or checkbox. Controlled-cloud projects are always private and require an invitation,
access code or authorized link. A manifest declares fields, not permission or moderation approval.

## Choose the participant experience

- **One shared record** (`recordScope: "shared"`): everyone maintains the same checklist, plan or values.
- **Each person's record** (`recordScope: "participant"`): the server isolates each participant's rows.
  This does not create a public leaderboard or authorize aggregate reporting. Anonymous identity is
  browser-session based; choose account saving for personal progress that should follow a login.
- **Save with a nickname** (`identityMode: "nickname"`): the trusted host asks before first save.
- **Sign in to save** (`identityMode: "account"`): the host preserves staged changes through login and
  binds the verified account. This is not real-name verification. Viewing still requires sharing access.

Describe this in user terms, for example: “The group shares one progress list. Each participant enters
a nickname before saving.” Ask only choices not established by the conversation.

Use primitive fields with stable names. For a new form or poll, declare
`reviewMode: "immediate"`. A valid submission is recorded when saving succeeds; the author does not
review individual answers. Older manifests may contain `manual`, `validated`, or
`owner_confirmation` for compatibility with already published revisions. Do not offer those modes
as choices for new forms or describe them as a pending approval step.

For single choice, declare a string field and question `options` with `choiceMode: "single"`.
For multiple choice, use a string field of sufficient bounded length, set `choiceMode: "multiple"`,
and encode chosen option labels as a JSON array string in declared option order, without duplicates.
The server validates this representation; do not send a raw array over the primitive data protocol.
Keep original question labels and custom field keys. Render participant text with `textContent`,
never `innerHTML`.

Render the choices as real participant controls inside the generated HTML: one `<select>` or radio
group for a single choice and labelled checkboxes for multiple choices. Match their visible labels
and values to the frozen question `options`. Do not show the JSON wire value to a participant. Read
the stored multiple-choice string with `JSON.parse` to restore checked boxes; only use an array of
declared options. When a control changes, call `state.set` with the single label or canonical JSON
string. The host save button then commits the staged answer; show “Changes ready to save” after
staging, and let the host show saved or failure. Do not say “Submitted” when
`state.set` has only staged a change.

```html
<label for="mood">How do you feel?</label>
<select id="mood" disabled>
  <option value="">Choose one</option>
  <option value="Happy">Happy</option>
  <option value="Calm">Calm</option>
</select>
<fieldset id="foods" disabled>
  <legend>Which foods do you like?</legend>
  <label><input type="checkbox" value="Rice">Rice</label>
  <label><input type="checkbox" value="Noodles">Noodles</label>
  <label><input type="checkbox" value="Dumplings">Dumplings</label>
</fieldset>
<p id="answer-status" role="status">Connecting…</p>
<script>
window.addEventListener("onimi:data-ready", async () => {
  const mood = document.getElementById("mood")
  const foods = document.getElementById("foods")
  const boxes = [...foods.querySelectorAll('input[type="checkbox"]')]
  const status = document.getElementById("answer-status")
  const foodOptions = ["Rice", "Noodles", "Dumplings"]
  const state = window.Onimi.data.createState({
    collectionKey: "responses", recordKey: "myAnswer", schemaVersion: 1,
    initial: {},
  })
  state.subscribe((values) => {
    mood.value = typeof values.mood === "string" ? values.mood : ""
    let selected = []
    try {
      const parsed = JSON.parse(values.foods)
      if (Array.isArray(parsed)) selected = parsed.filter((value) => foodOptions.includes(value))
    } catch { /* The server rejects invalid new answers; keep controls empty. */ }
    for (const box of boxes) box.checked = selected.includes(box.value)
  })
  try {
    await state.ready
    mood.disabled = false
    foods.disabled = false
    status.textContent = "Choose your answers, then save."
    const stageAnswers = async () => {
      const selected = foodOptions.filter((option) => boxes.some((box) =>
        box.value === option && box.checked))
      if (!mood.value || selected.length === 0) {
        status.textContent = "Choose a mood and at least one food."
        return
      }
      try {
        await state.set({ mood: mood.value, foods: JSON.stringify(selected) })
        status.textContent = "Changes ready to save."
      } catch { status.textContent = "Could not prepare this answer. Reconnect and try again." }
    }
    mood.addEventListener("change", stageAnswers)
    foods.addEventListener("change", stageAnswers)
  } catch { status.textContent = "Answers are unavailable. Open your authorized sharing link." }
}, { once: true })
</script>
```

Use the same fields in the artifact schema and participation question metadata; choose a string
`maxLength` that contains the longest JSON array of all option labels. Required choices need at
least one checked option before staging. The example starts with no answer and stages both required
fields together.

## Declare the save contract

Embed exactly one inert manifest and SDK placeholder. Do not put API URLs, SDK bytes, credentials or
account IDs inside the artifact. The trusted publication pipeline provides the reviewed runtime.

```html
<script id="onimi-artifact" type="application/json">{"protocolVersion":1,"kind":"page","data":{"mode":"controlled-cloud","collections":[{"id":"progress","schemaVersion":1,"recordScope":"shared","reviewMode":"immediate","capabilities":["records.read","records.append","records.patch","records.subscribe"],"fields":[{"key":"interviewReady","type":"boolean","required":true},{"key":"summaryReady","type":"boolean","required":true}]}]}}</script>
<script type="application/onimi-data-sdk"></script>
```

A collection has at most 32 fields. Use lower-case-starting identifiers matching
`[a-z][a-zA-Z0-9_-]{0,63}` for collections and record keys. Keep task labels and page copy in the reviewed
HTML; store only declared changing values. Do not synchronize an entire localStorage object.

## Stage changes for the host FAB

Wait for the trusted connection. `createState` opens a stable record key; its initial values are a
fallback until a server record exists. Calling `set` stages declared fields and marks the host FAB as
unsaved. It does not claim a successful save. The host controls identity, atomic save, history and
network/conflict feedback.

```js
window.addEventListener("onimi:data-ready", async () => {
  const progress = window.Onimi.data.createState({
    collectionKey: "progress",
    recordKey: "groupProgress",
    schemaVersion: 1,
    initial: { interviewReady: false, summaryReady: false },
  })
  const inputs = [...document.querySelectorAll("input[data-progress-key]")]
  progress.subscribe((values) => {
    for (const input of inputs) input.checked = Boolean(values[input.dataset.progressKey])
  })
  try {
    await progress.ready
    for (const input of inputs) {
      input.disabled = false
      input.addEventListener("change", async () => {
        try {
          await progress.set({ [input.dataset.progressKey]: input.checked })
        } catch {
          document.querySelector("[data-connection-status]").textContent =
            "This change could not be staged. Reconnect before saving."
        }
      })
    }
  } catch {
    document.querySelector("[data-connection-status]").textContent =
      "Shared progress is unavailable. Open your authorized sharing link."
  }
}, { once: true })
```

Initially disable connected controls and show a clear connecting state. Standalone/offline HTML can
preview content but cannot claim shared saving outside the trusted host. Keep FAB-style save/history
and login UI out of the untrusted artifact. Never put a bearer secret into its URL or iframe.

For append-oriented forms, the compatible `window.OnimiData.collection(key)` API exposes
`list({limit,cursor})`, `append({mutationId,schemaVersion,values})`,
`patch(recordId,{mutationId,schemaVersion,baseVersion,values})`, and
`subscribe({cursor,onChange,intervalMs})`. These direct mutations still enforce identity, version
and field validation, and a successful append is recorded directly. Prefer `createState` for a shared
checklist with explicit FAB saving.
Keep a UUID with the exact logical mutation for uncertain retries. Never generate a new ID to evade a
conflict. Subscription is bounded polling of visible saved records, not broader read permission.

The published controlled page runs inside an `allow-scripts` iframe with `form-action 'none'`.
Native HTML form submission is intentionally blocked. For an append form, use a
`<button type="button">` with a `click` handler that validates the fields and calls
`collection.append(...)`; do not rely on a `<form>` `submit` event or request `allow-forms`.
If the page retains a `<form>` for labels and grouping, handle Enter on single-line inputs in that
same click path and leave Enter in a textarea for a new line. Verify the button by saving from the
**published authorized participant page**, not only from a standalone preview.

## Configure and publish the selected project

Read `onimi_get_collaboration`, then configure with its exact current policy epoch, manifest and UUID.
The target must be the user-selected project. Upgrading a local page requires a new draft with this
manifest and SDK integration, configuration, review and publication; a dataMode toggle alone is not
sufficient. Keep older source and releases. A repeated request uses the same UUID and body; a conflict
requires a fresh read and reconciliation.

Create only the authorized invitation, code or link with the selected `identityMode`, least collection
capabilities and bounded expiry. The owner receives its private `redeemPath`; never put its secret in
HTML, logs, a public URL listing or source control. Follow the Publish Skill for immutable review and
activation. Existing approval does not authorize changed artifact bytes.

## Verify the actual outcome

Verify with two independently authorized sessions: A changes and saves; B sees the committed value;
refresh and a fresh authorized session also load it. Check nickname saving and account-required saving
separately, including retained changes after login. Verify read-only access, stale-version conflict,
expired/revoked access and offline failure without a false success message. Check that a successful
form submission appears in authorized results without an author approval step.
Participants' history shows only the displayed name and time. Owners use project management to inspect
before/after changes and append a rollback under the current version; this is separate from restoring
an HTML or Slides source version. Never describe URL fragments, localStorage, draft saves or a single
HTTP success as proof of cross-person synchronization.
