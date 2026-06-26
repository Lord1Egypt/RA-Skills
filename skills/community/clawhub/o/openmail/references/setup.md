# OpenMail Setup

Run this once when OpenMail credentials are missing.

---

## Phase 1: Credentials

Ask the user:

> I need your OpenMail API key to set up your email inbox.
> You can get one at **https://console.openmail.sh** — sign up for free,
> then copy your API key from the dashboard.

Wait for the user to provide the key. Once received, write it to the env
file and source it into the current shell:

```bash
mkdir -p ~/.openclaw
printf 'OPENMAIL_API_KEY=%s\n' "<their-key>" > ~/.openclaw/openmail.env
source ~/.openclaw/openmail.env
```

Verify the key works:

```bash
openmail inbox list --json
```

If this fails with an auth error, tell the user the key is invalid and ask
them to generate a fresh one from **https://console.openmail.sh** under
Settings → API Keys.

---

## Phase 2: Inbox selection

List the user's existing inboxes:

```bash
openmail inbox list --json
```

The response has a `data` array. Each inbox has `id`, `address`, and
optionally `displayName`.

**Always present a choice** — even if only one inbox exists. Build the
options as:
- One entry per existing inbox, labelled with `address` (and `displayName`
  if present)
- A final option: **Create a new inbox**

Never auto-select. Ask the user which inbox this agent should use.

**If the user selects an existing inbox**, store its `id` and `address`.

**If the user selects "Create a new inbox"**, ask for a mailbox name
(the local part before the `@`, e.g. `assistant` → `assistant@yourdomain.sh`)
and an optional display name, then:

```bash
openmail inbox create \
  --mailbox-name "<name>" \
  --display-name "<display name>" \
  --json
```

Store the returned `id` and `address`.

---

## Phase 3: Save and confirm

Append the inbox values to the same env file (`OPENMAIL_API_KEY` is already
there from Phase 1), then source it to pick up all three vars:

```bash
printf 'OPENMAIL_INBOX_ID=%s\nOPENMAIL_ADDRESS=%s\n' \
  "<inbox-id>" "<inbox-address>" >> ~/.openclaw/openmail.env
source ~/.openclaw/openmail.env
```

Tell the user:

> OpenMail is ready. Your agent's email address is **<inbox-address>**.
> Try it: "send an email to yourself with subject Test"
