# LinkedCamp tool map

The hosted server exposes about 130 tools in 14 toolsets. In OpenClaw each is
called as `linkedcamp__<name>`. Your plan can hide some of them: a toolset the
web app hides for this user is withheld here too.

Legend: no mark = read-only · `+` = write · `*` = write, flagged destructive
(confirm first — see `safety.md`).

| Toolset | Tools |
| --- | --- |
| Core | `whoami` `reference` `unread_counts` |
| Campaigns | `campaign_list` `campaign_get` `campaign_create+` `campaign_update+` `campaign_set_source*` `campaign_add_prospects*` `campaign_upload_leads+` `campaign_launch*` `campaign_set_status+` `campaign_delete*` `campaign_duplicate+` `campaign_create_ab_variant+` `campaign_generate_ai_sequence+` `campaign_preview_message` `campaign_send_test_email*` `campaign_activity_summary` `campaign_logs` `campaign_export_stats+` `search_url_build` |
| Flows and sequences | `flow_get` `flow_set*` `flow_from_template+` `flow_audit` `flow_history` `sequence_list` `sequence_update*` `sequence_step_stats` `sequence_leads_at_step` |
| Leads and activities | `lead_list` `lead_get` `lead_add+` `lead_update+` `lead_move+` `lead_export+` `lead_flow_state` `lead_delete*` `lead_blacklist*` `lead_notes_list` `lead_note_add+` `lead_note_update*` `activity_list` `activity_skip*` |
| Sending accounts | `linkedin_account_list` `linkedin_account_get` `linkedin_account_update+` `linkedin_account_refresh+` `linkedin_account_stats` `linkedin_account_daily_stats` `linkedin_account_ssi` `email_account_list` `email_account_get` `email_account_update+` `email_account_add_imap+` `email_account_oauth_url` `email_account_stats` |
| Unified inbox | `conversation_list` `conversation_get+` `conversation_update+` `conversation_mark_all_read+` `message_draft_ai_reply+` `message_send*` `message_delete*` `saved_reply_list` `saved_reply_upsert*` |
| Analytics | `analytics_account` `analytics_campaign` `analytics_campaign_funnel` `analytics_reporting` `analytics_trend` |
| Library | `tag_list` `tag_create+` `tag_update+` `tag_delete*` `blacklist_list` `blacklist_add+` `blacklist_add_bulk+` `blacklist_copy+` `blacklist_export+` `blacklist_delete*` `template_list` `template_get` `template_upsert*` `placeholder_list` `placeholder_add+` `placeholder_delete*` `holiday_list` `holiday_add+` `holiday_delete*` `hyperise_images` |
| Personas (Pro) | `persona_list` `persona_get` `persona_create+` `persona_update*` `persona_delete*` |
| AI agents (`Agents` permission) | `agent_list` `agent_get` `agent_upsert*` `agent_duplicate+` `agent_train+` `agent_query` `agent_stats` `agent_logs` `agent_delete*` `kb_list` `kb_upsert*` `kb_attach+` `kb_delete*` |
| Content (`Publish` permission) | `post_list` `post_generate` `post_upsert*` `post_schedule_get` `post_schedule_set*` `post_schedule_settings+` |
| CRM and follow-up | `appointment_list` `appointment_get` `task_list` `task_upsert+` `reminder_list` `reminder_create+` `reminder_delete*` |
| Automations | `automation_list` `automation_get` `automation_upsert+` `automation_duplicate+` |
| Account settings | `account_settings_update+` `notification_list` `notification_mark_read+` `team_members_list` `subaccount_list` `help_videos` |

`conversation_get` is marked write because opening a conversation marks it read.

Each tool's own description is the authority on its parameters and behaviour —
read it rather than guessing an argument shape. If a tool named here is missing
from your tool list, the plan or permissions hide it; do not look for a
substitute.
