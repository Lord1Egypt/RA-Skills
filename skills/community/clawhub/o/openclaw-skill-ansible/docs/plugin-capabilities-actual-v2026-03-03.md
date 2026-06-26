# Plugin Capability Inventory (Actual)

Snapshot date: 2026-03-03  
Source: `openclaw-plugin-ansible` code (`src/tools.ts`, `src/cli.ts`)

## Runtime Tool Surface

Messaging/task lifecycle:

1. `ansible_send_message`
2. `ansible_delegate_task`
3. `ansible_claim_task`
4. `ansible_update_task`
5. `ansible_complete_task`
6. `ansible_read_messages`
7. `ansible_mark_read`
8. `ansible_approve_task`

Capability lifecycle:

1. `ansible_capability_publish`
2. `ansible_capability_unpublish`
3. `ansible_capability_lifecycle_evidence`
4. `ansible_list_capabilities`
5. `ansible_capability_health_summary`

Governance/ops:

1. `ansible_set_gateway_admin`
2. `ansible_set_distribution_policy`
3. `ansible_set_backpressure_policy`
4. `ansible_set_retention`
5. `ansible_sla_sweep`
6. `ansible_set_delegation_policy`
7. `ansible_ack_delegation_policy`
8. `ansible_set_coordination`

Agent onboarding/auth:

1. `ansible_register_agent`
2. `ansible_invite_agent`
3. `ansible_accept_agent_invite`
4. `ansible_issue_agent_token`
5. `ansible_rebind_agent`
6. `ansible_disable_agent`
7. `ansible_enable_agent`
8. `ansible_list_agents`

Observability/debug:

1. `ansible_status`
2. `ansible_task_timeline`
3. `ansible_find_task`
4. `ansible_dump_state`
5. `ansible_dump_tasks`
6. `ansible_dump_messages`

## CLI Surface

Setup/bootstrap:

1. `openclaw ansible setup`
2. `openclaw ansible bootstrap`
3. `openclaw ansible invite`
4. `openclaw ansible join`
5. `openclaw ansible ws-ticket`
6. `openclaw ansible revoke`

Capability lifecycle:

1. `openclaw ansible capability publish`
2. `openclaw ansible capability unpublish`
3. `openclaw ansible capability list`
4. `openclaw ansible capability health`
5. `openclaw ansible capability evidence`

Tasks/messages:

1. `openclaw ansible tasks list|claim|update|approve|complete`
2. `openclaw ansible tasks timeline`
3. `openclaw ansible messages`
4. `openclaw ansible messages-delete`

Governance:

1. `openclaw ansible delegation show|set|ack`
2. `openclaw ansible admin set|seed|distribution|backpressure`
3. `openclaw ansible retention set`
4. `openclaw ansible sla sweep`

Agent management:

1. `openclaw ansible agent register|invite|accept|token-issue|rebind|normalize|disable|enable|distribution-opt|list`

## Notes for This Skill

1. Prefer plugin-manager operations (`openclaw plugins install`, `openclaw ansible setup`) over direct filesystem mutation.
2. Keep high-risk execution (`run-cmd`, `deploy-skill`) explicitly gated and auditable.
