# Destructive LinkedCamp calls

Each of these reaches real people or removes something that cannot be put
back. Before calling one: say in specifics what will happen, get an explicit
yes in the conversation, and never cover several calls with one yes. A
"go ahead with everything" for a batch is not a confirmation for each item —
list them and confirm them one at a time, or ask the user to name exactly
which ones.

If a gentler tool does what the user actually wants, offer it first.

| Tool | What actually happens | Offer instead |
| --- | --- | --- |
| `campaign_launch` | Starts real outreach from the connected LinkedIn account and mailboxes on the campaign's schedule. Show the audience URL and full sequence. A paused LinkedIn account sends nothing — check `linkedin_account_get` first. | Leave it as a draft. |
| `campaign_set_status` → `ACTIVE` | Resumes outreach on a paused campaign. Not flagged destructive, so no client prompt will appear. Accepts only `PAUSED` and `ACTIVE`; a never-launched campaign is started with `campaign_launch`. | Ask why it was paused. |
| `campaign_set_source`, `campaign_add_prospects` | Changes who gets messaged. Show the URL first. | — |
| `message_send` | Delivers on LinkedIn or by email immediately; cannot be recalled. Also stands a CHAT agent down on that thread when the agent has `pauseBotOnManualMessage` set. Show the exact text and recipient. | `message_draft_ai_reply` and let the user send. |
| `message_delete` | Edits LinkedCamp's own record only. It does **not** unsend — the recipient keeps the message. Say this. | — |
| `campaign_send_test_email` | Sends a real email. Show recipient, subject and body. | `campaign_preview_message`. |
| `post_upsert` with a due `scheduledAt`, `post_schedule_set` | May publish publicly on LinkedIn. Show the exact post. | Save without `scheduledAt`. |
| `flow_set` on an ACTIVE campaign | Re-evaluates every lead against the new graph; can cancel or reschedule pending actions. `flow_audit` afterwards reports what moved. | Duplicate into a new draft. |
| `sequence_update` | On ACTIVE/PAUSED only. On a DRAFTED campaign the edit is silently reverted at launch. | `flow_set` for drafts. |
| `campaign_delete` | Moves the campaign to DELETED. Nothing is erased, but it disappears and no tool restores it. Also removes still-active "add prospects" child campaigns. | `campaign_set_status` → `PAUSED`. |
| `lead_delete` | Removes leads and their pending actions. | `lead_update` with `isExcluded: true` to stop sending. |
| `lead_blacklist` | Excludes the person from every future campaign on the account; nothing removes that. Right for an opt-out, wrong for "stop messaging them here". | `lead_update` with `isExcluded: true`. |
| `activity_skip` | Skips a scheduled action for a lead; it will not run. | — |
| `lead_note_update` | Overwrites the note text. | `lead_note_add`. |
| `agent_upsert` on an active agent | Changes how it answers real prospects from the next reply. | Set `isActive: false` while iterating; test with `agent_query`. |
| `agent_delete` | Campaigns using it silently lose automated replies; prospects mid-conversation stop getting answers. | `agent_upsert` with `isActive: false`. |
| `kb_upsert` / `kb_delete` | Changes or removes an agent's source material; a crawled page must be crawled again. | `kb_attach` to exclude an entry. |
| `persona_update` / `persona_delete` | Every QUALIFIER step pointing at it changes or breaks, and that campaign's flow then fails to save. Check `usageCount` first. | — |
| `tag_delete` | Leads lose the classification; past reply-sentiment reporting changes. Deleting a campaign's identity tag makes its leads indistinguishable. | `tag_update` to rename. |
| `blacklist_delete` | People the rule was blocking become targetable again. Read the rule out first. | — |
| `placeholder_delete` | Copy using `{{key}}` then renders empty with no error — a live campaign sends messages with a hole in them. | — |
| `template_upsert`, `saved_reply_upsert` | Overwrites saved copy other campaigns or teammates may use. | Create a new one. |
| `reminder_delete`, `holiday_delete` | Removes the record by id. | — |

## Sub-accounts

With a `userId` or a record id from an agency sub-account, every write above
lands in the **client's** account. Name the client in the confirmation.

## Credentials

Never request, accept or repeat a LinkedCamp API key, LinkedIn password,
session cookie, verification PIN or mailbox password in chat. Connecting
LinkedCamp happens through `openclaw mcp login linkedcamp`; connecting a
LinkedIn account happens in the LinkedCamp web app.
