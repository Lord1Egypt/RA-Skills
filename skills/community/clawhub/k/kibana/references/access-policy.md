# Kibana access policy

An access policy limits which endpoints Kibana connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/kibana#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Kibana: its 264 read-only endpoints, plus deny rules for the 2 write endpoints a read rule would otherwise match. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create kibana --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/actions/connector/{id}"},
    {"method": "GET", "path": "api/actions/connector_types"},
    {"method": "GET", "path": "api/actions/connectors"},
    {"method": "GET", "path": "api/agent_builder/a2a/{id}"},
    {"method": "GET", "path": "api/agent_builder/agents"},
    {"method": "GET", "path": "api/agent_builder/agents/{id}"},
    {"method": "GET", "path": "api/agent_builder/agents/{id}/access_control"},
    {"method": "POST", "path": "api/agent_builder/agents/{id}/consumption"},
    {"method": "GET", "path": "api/agent_builder/conversations"},
    {"method": "GET", "path": "api/agent_builder/conversations/{id}"},
    {"method": "GET", "path": "api/agent_builder/conversations/{id}/attachments"},
    {"method": "GET", "path": "api/agent_builder/conversations/{id}/attachments/stale"},
    {"method": "GET", "path": "api/agent_builder/conversations/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/agent_builder/plugins"},
    {"method": "GET", "path": "api/agent_builder/plugins/{id}"},
    {"method": "GET", "path": "api/agent_builder/skills"},
    {"method": "GET", "path": "api/agent_builder/skills/{id}"},
    {"method": "GET", "path": "api/agent_builder/tools"},
    {"method": "GET", "path": "api/agent_builder/tools/{id}"},
    {"method": "GET", "path": "api/alerting/_health"},
    {"method": "GET", "path": "api/alerting/rule/{id}"},
    {"method": "GET", "path": "api/alerting/rule/{id}/query_inspector"},
    {"method": "GET", "path": "api/alerting/rule_types"},
    {"method": "GET", "path": "api/alerting/rules/_find"},
    {"method": "POST", "path": "api/alerting/rules/backfill/_find"},
    {"method": "GET", "path": "api/alerting/rules/backfill/{id}"},
    {"method": "GET", "path": "api/alerting/v2/action_policies"},
    {"method": "GET", "path": "api/alerting/v2/action_policies/{id}"},
    {"method": "GET", "path": "api/alerting/v2/execution_history/action_policies"},
    {"method": "GET", "path": "api/alerting/v2/execution_history/rules"},
    {"method": "GET", "path": "api/alerting/v2/rules"},
    {"method": "POST", "path": "api/alerting/v2/rules/_bulk_get"},
    {"method": "GET", "path": "api/alerting/v2/rules/{id}"},
    {"method": "GET", "path": "api/apm/services/{id}/annotation/search"},
    {"method": "GET", "path": "api/apm/settings/agent-configuration"},
    {"method": "GET", "path": "api/apm/settings/agent-configuration/agent_name"},
    {"method": "GET", "path": "api/apm/settings/agent-configuration/environments"},
    {"method": "POST", "path": "api/apm/settings/agent-configuration/search"},
    {"method": "GET", "path": "api/apm/settings/agent-configuration/view"},
    {"method": "GET", "path": "api/apm/sourcemaps"},
    {"method": "GET", "path": "api/asset_criticality"},
    {"method": "GET", "path": "api/asset_criticality/list"},
    {"method": "GET", "path": "api/attack_discovery/_find"},
    {"method": "GET", "path": "api/attack_discovery/generations"},
    {"method": "GET", "path": "api/attack_discovery/generations/{id}"},
    {"method": "GET", "path": "api/attack_discovery/schedules/_find"},
    {"method": "GET", "path": "api/attack_discovery/schedules/{id}"},
    {"method": "GET", "path": "api/cases/_find"},
    {"method": "GET", "path": "api/cases/alerts/{id}"},
    {"method": "GET", "path": "api/cases/configure"},
    {"method": "GET", "path": "api/cases/configure/connectors/_find"},
    {"method": "GET", "path": "api/cases/field_definitions"},
    {"method": "GET", "path": "api/cases/field_definitions/{id}"},
    {"method": "GET", "path": "api/cases/fields"},
    {"method": "GET", "path": "api/cases/reporters"},
    {"method": "GET", "path": "api/cases/tags"},
    {"method": "GET", "path": "api/cases/templates"},
    {"method": "GET", "path": "api/cases/templates/{id}"},
    {"method": "GET", "path": "api/cases/{id}"},
    {"method": "GET", "path": "api/cases/{id}/alerts"},
    {"method": "GET", "path": "api/cases/{id}/attachments"},
    {"method": "GET", "path": "api/cases/{id}/attachments/{id}"},
    {"method": "GET", "path": "api/cases/{id}/comments/_find"},
    {"method": "GET", "path": "api/cases/{id}/comments/{id}"},
    {"method": "GET", "path": "api/cases/{id}/fields"},
    {"method": "GET", "path": "api/cases/{id}/user_actions/_find"},
    {"method": "GET", "path": "api/context_engine/ai_index"},
    {"method": "POST", "path": "api/context_engine/ai_index/_query"},
    {"method": "GET", "path": "api/context_engine/ai_index/{id}"},
    {"method": "GET", "path": "api/context_engine/ai_index/{id}/_describe"},
    {"method": "GET", "path": "api/dashboards"},
    {"method": "GET", "path": "api/dashboards/{id}"},
    {"method": "GET", "path": "api/data_views"},
    {"method": "GET", "path": "api/data_views/data_view/{id}"},
    {"method": "GET", "path": "api/data_views/data_view/{id}/runtime_field/{id}"},
    {"method": "GET", "path": "api/data_views/default"},
    {"method": "POST", "path": "api/data_views/swap_references/_preview"},
    {"method": "GET", "path": "api/data_views/v2"},
    {"method": "GET", "path": "api/data_views/v2/{id}"},
    {"method": "POST", "path": "api/detection_engine/attacks/search"},
    {"method": "GET", "path": "api/detection_engine/index"},
    {"method": "GET", "path": "api/detection_engine/privileges"},
    {"method": "GET", "path": "api/detection_engine/rules"},
    {"method": "POST", "path": "api/detection_engine/rules/_export"},
    {"method": "GET", "path": "api/detection_engine/rules/_find"},
    {"method": "GET", "path": "api/detection_engine/rules/prepackaged/_status"},
    {"method": "GET", "path": "api/detection_engine/signals/migration_status"},
    {"method": "POST", "path": "api/detection_engine/signals/search"},
    {"method": "GET", "path": "api/detection_engine/tags"},
    {"method": "GET", "path": "api/discover_sessions"},
    {"method": "GET", "path": "api/discover_sessions/{id}"},
    {"method": "GET", "path": "api/endpoint/action"},
    {"method": "GET", "path": "api/endpoint/action/state"},
    {"method": "GET", "path": "api/endpoint/action/{id}"},
    {"method": "GET", "path": "api/endpoint/action/{id}/file/{id}"},
    {"method": "GET", "path": "api/endpoint/action/{id}/file/{id}/download"},
    {"method": "GET", "path": "api/endpoint/action_status"},
    {"method": "GET", "path": "api/endpoint/metadata"},
    {"method": "GET", "path": "api/endpoint/metadata/{id}"},
    {"method": "GET", "path": "api/endpoint/policy_response"},
    {"method": "GET", "path": "api/endpoint/protection_updates_note/{id}"},
    {"method": "GET", "path": "api/endpoint/scripts_library"},
    {"method": "GET", "path": "api/endpoint/scripts_library/{id}"},
    {"method": "GET", "path": "api/endpoint/scripts_library/{id}/download"},
    {"method": "GET", "path": "api/endpoint_list/items"},
    {"method": "GET", "path": "api/endpoint_list/items/_find"},
    {"method": "GET", "path": "api/entity_analytics/monitoring/privileges/health"},
    {"method": "GET", "path": "api/entity_analytics/monitoring/privileges/privileges"},
    {"method": "GET", "path": "api/entity_analytics/monitoring/users/list"},
    {"method": "GET", "path": "api/entity_analytics/privileged_user_monitoring/pad/status"},
    {"method": "GET", "path": "api/entity_analytics/watchlists/list"},
    {"method": "GET", "path": "api/entity_analytics/watchlists/{id}"},
    {"method": "GET", "path": "api/exception_lists"},
    {"method": "POST", "path": "api/exception_lists/_export"},
    {"method": "GET", "path": "api/exception_lists/_find"},
    {"method": "GET", "path": "api/exception_lists/items"},
    {"method": "GET", "path": "api/exception_lists/items/_find"},
    {"method": "GET", "path": "api/exception_lists/summary"},
    {"method": "GET", "path": "api/features"},
    {"method": "POST", "path": "api/fleet/agent_policies/outputs"},
    {"method": "GET", "path": "api/fleet/agent_policies/{id}/auto_upgrade_agents_status"},
    {"method": "GET", "path": "api/fleet/agent_policies/{id}/outputs"},
    {"method": "GET", "path": "api/fleet/agent_status"},
    {"method": "GET", "path": "api/fleet/agent_status/data"},
    {"method": "GET", "path": "api/fleet/agents/action_status"},
    {"method": "GET", "path": "api/fleet/agents/available_versions"},
    {"method": "GET", "path": "api/fleet/agents/files/{id}/{id}"},
    {"method": "GET", "path": "api/fleet/agents/setup"},
    {"method": "GET", "path": "api/fleet/agents/tags"},
    {"method": "GET", "path": "api/fleet/agents/{id}/effective_config"},
    {"method": "GET", "path": "api/fleet/agents/{id}/uploads"},
    {"method": "GET", "path": "api/fleet/check-permissions"},
    {"method": "GET", "path": "api/fleet/cloud_connectors/{id}/usage"},
    {"method": "GET", "path": "api/fleet/cloud_onboarding_deployments"},
    {"method": "GET", "path": "api/fleet/cloud_onboarding_deployments/connector/{id}"},
    {"method": "GET", "path": "api/fleet/cloud_onboarding_deployments/{id}"},
    {"method": "GET", "path": "api/fleet/data_streams"},
    {"method": "GET", "path": "api/fleet/data_streams/data"},
    {"method": "POST", "path": "api/fleet/epm/bulk_assets"},
    {"method": "GET", "path": "api/fleet/epm/categories"},
    {"method": "GET", "path": "api/fleet/epm/data_streams"},
    {"method": "GET", "path": "api/fleet/epm/packages"},
    {"method": "GET", "path": "api/fleet/epm/packages/_bulk_rollback/{id}"},
    {"method": "GET", "path": "api/fleet/epm/packages/_bulk_uninstall/{id}"},
    {"method": "GET", "path": "api/fleet/epm/packages/_bulk_upgrade/{id}"},
    {"method": "GET", "path": "api/fleet/epm/packages/installed"},
    {"method": "GET", "path": "api/fleet/epm/packages/limited"},
    {"method": "GET", "path": "api/fleet/epm/packages/{id}"},
    {"method": "GET", "path": "api/fleet/epm/packages/{id}/stats"},
    {"method": "GET", "path": "api/fleet/epm/packages/{id}/{id}"},
    {"method": "GET", "path": "api/fleet/epm/packages/{id}/{id}/dependencies"},
    {"method": "GET", "path": "api/fleet/epm/packages/{id}/{id}/{id}"},
    {"method": "GET", "path": "api/fleet/epm/templates/{id}/{id}/inputs"},
    {"method": "GET", "path": "api/fleet/epm/verification_key_id"},
    {"method": "POST", "path": "api/fleet/health_check"},
    {"method": "GET", "path": "api/fleet/outputs/{id}/health"},
    {"method": "GET", "path": "api/fleet/remote_synced_integrations/status"},
    {"method": "GET", "path": "api/fleet/remote_synced_integrations/{id}/remote_status"},
    {"method": "GET", "path": "api/fleet/settings"},
    {"method": "GET", "path": "api/fleet/space_settings"},
    {"method": "GET", "path": "api/fleet/uninstall_tokens"},
    {"method": "GET", "path": "api/links"},
    {"method": "GET", "path": "api/links/{id}"},
    {"method": "GET", "path": "api/lists"},
    {"method": "GET", "path": "api/lists/_find"},
    {"method": "GET", "path": "api/lists/index"},
    {"method": "GET", "path": "api/lists/items"},
    {"method": "POST", "path": "api/lists/items/_export"},
    {"method": "GET", "path": "api/lists/items/_find"},
    {"method": "GET", "path": "api/lists/privileges"},
    {"method": "GET", "path": "api/logstash/pipeline/{id}"},
    {"method": "GET", "path": "api/logstash/pipelines"},
    {"method": "GET", "path": "api/maintenance_window/_find"},
    {"method": "GET", "path": "api/maintenance_window/{id}"},
    {"method": "GET", "path": "api/markdowns"},
    {"method": "GET", "path": "api/markdowns/{id}"},
    {"method": "GET", "path": "api/note"},
    {"method": "GET", "path": "api/observability/slos"},
    {"method": "GET", "path": "api/observability/slos/_bulk_delete/{id}"},
    {"method": "POST", "path": "api/observability/slos/_bulk_snapshot"},
    {"method": "GET", "path": "api/observability/slos/_definitions"},
    {"method": "GET", "path": "api/observability/slos/{id}"},
    {"method": "GET", "path": "api/observability/slos/{id}/_snapshot"},
    {"method": "GET", "path": "api/osquery/history"},
    {"method": "GET", "path": "api/osquery/live_queries"},
    {"method": "GET", "path": "api/osquery/live_queries/{id}"},
    {"method": "GET", "path": "api/osquery/live_queries/{id}/results/{id}"},
    {"method": "POST", "path": "api/osquery/live_queries/{id}/results/{id}/_export"},
    {"method": "GET", "path": "api/osquery/packs"},
    {"method": "GET", "path": "api/osquery/packs/{id}"},
    {"method": "GET", "path": "api/osquery/saved_queries"},
    {"method": "GET", "path": "api/osquery/saved_queries/{id}"},
    {"method": "GET", "path": "api/osquery/scheduled_results/{id}/{id}"},
    {"method": "POST", "path": "api/osquery/scheduled_results/{id}/{id}/_export"},
    {"method": "GET", "path": "api/osquery/scheduled_results/{id}/{id}/results"},
    {"method": "GET", "path": "api/profiling/setup/es_resources"},
    {"method": "GET", "path": "api/risk_score/history"},
    {"method": "POST", "path": "api/saved_objects/_bulk_get"},
    {"method": "POST", "path": "api/saved_objects/_bulk_resolve"},
    {"method": "POST", "path": "api/saved_objects/_export"},
    {"method": "GET", "path": "api/saved_objects/_find"},
    {"method": "GET", "path": "api/saved_objects/resolve/{id}/{id}"},
    {"method": "GET", "path": "api/saved_objects/{id}/{id}"},
    {"method": "GET", "path": "api/security/entity_store/entities"},
    {"method": "GET", "path": "api/security/entity_store/resolution/group"},
    {"method": "GET", "path": "api/security/entity_store/resolution/rules"},
    {"method": "GET", "path": "api/security/entity_store/status"},
    {"method": "GET", "path": "api/security/role"},
    {"method": "POST", "path": "api/security/role/_query"},
    {"method": "GET", "path": "api/security/role/{id}"},
    {"method": "GET", "path": "api/security_ai_assistant/anonymization_fields/_find"},
    {"method": "GET", "path": "api/security_ai_assistant/current_user/conversations/_find"},
    {"method": "GET", "path": "api/security_ai_assistant/current_user/conversations/{id}"},
    {"method": "GET", "path": "api/security_ai_assistant/knowledge_base"},
    {"method": "GET", "path": "api/security_ai_assistant/knowledge_base/entries/_find"},
    {"method": "GET", "path": "api/security_ai_assistant/knowledge_base/entries/{id}"},
    {"method": "GET", "path": "api/security_ai_assistant/knowledge_base/{id}"},
    {"method": "GET", "path": "api/security_ai_assistant/prompts/_find"},
    {"method": "GET", "path": "api/short_url/_slug/{id}"},
    {"method": "GET", "path": "api/short_url/{id}"},
    {"method": "POST", "path": "api/spaces/_get_shareable_references"},
    {"method": "GET", "path": "api/spaces/space"},
    {"method": "GET", "path": "api/spaces/space/{id}"},
    {"method": "GET", "path": "api/status"},
    {"method": "GET", "path": "api/streams"},
    {"method": "GET", "path": "api/streams/{id}"},
    {"method": "GET", "path": "api/streams/{id}/_ingest"},
    {"method": "GET", "path": "api/streams/{id}/_query"},
    {"method": "GET", "path": "api/streams/{id}/attachments"},
    {"method": "POST", "path": "api/streams/{id}/content/export"},
    {"method": "GET", "path": "api/synthetics/monitors"},
    {"method": "GET", "path": "api/synthetics/monitors/{id}"},
    {"method": "GET", "path": "api/synthetics/private_locations"},
    {"method": "GET", "path": "api/synthetics/private_locations/{id}"},
    {"method": "GET", "path": "api/tags"},
    {"method": "GET", "path": "api/tags/{id}"},
    {"method": "GET", "path": "api/task_manager/_health"},
    {"method": "GET", "path": "api/timeline"},
    {"method": "GET", "path": "api/timeline/_draft"},
    {"method": "POST", "path": "api/timeline/_export"},
    {"method": "GET", "path": "api/timeline/resolve"},
    {"method": "GET", "path": "api/timelines"},
    {"method": "GET", "path": "api/upgrade_assistant/status"},
    {"method": "GET", "path": "api/uptime/settings"},
    {"method": "GET", "path": "api/vega"},
    {"method": "GET", "path": "api/vega/{id}"},
    {"method": "GET", "path": "api/visualizations"},
    {"method": "GET", "path": "api/visualizations/{id}"},
    {"method": "GET", "path": "api/workflows"},
    {"method": "GET", "path": "api/workflows/aggs"},
    {"method": "GET", "path": "api/workflows/connectors"},
    {"method": "GET", "path": "api/workflows/executions/{id}"},
    {"method": "GET", "path": "api/workflows/executions/{id}/children"},
    {"method": "GET", "path": "api/workflows/executions/{id}/logs"},
    {"method": "GET", "path": "api/workflows/executions/{id}/step/{id}"},
    {"method": "GET", "path": "api/workflows/executions/{id}/steps"},
    {"method": "POST", "path": "api/workflows/export"},
    {"method": "POST", "path": "api/workflows/mget"},
    {"method": "GET", "path": "api/workflows/schema"},
    {"method": "GET", "path": "api/workflows/stats"},
    {"method": "GET", "path": "api/workflows/workflow/executions"},
    {"method": "GET", "path": "api/workflows/workflow/{id}"},
    {"method": "GET", "path": "api/workflows/workflow/{id}/executions"},
    {"method": "GET", "path": "api/workflows/workflow/{id}/executions/steps"}
  ],
  "deny": [
    {"method": "GET", "path": "api/actions/connector/_oauth_callback"},
    {"method": "GET", "path": "api/actions/connector/_oauth_callback_script"}
  ]
}
```

## Endpoints

The Kibana endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/actions/connector/_oauth_callback | write | actions | Handle OAuth callback. Kept out of read: completes an OAuth flow and stores tokens. |
| GET | api/actions/connector/_oauth_callback_script | write | actions | Get OAuth callback script. Kept out of read: completes an OAuth flow and stores tokens. |
| GET | api/actions/connector/{id} | read | actions | Get connector information. |
| POST | api/actions/connector/{id} | write | actions | Create a connector. |
| PUT | api/actions/connector/{id} | write | actions | Update a connector. |
| DELETE | api/actions/connector/{id} | write | actions | Delete a connector. |
| POST | api/actions/connector/{id}/_execute | write | actions | Run a connector. |
| GET | api/actions/connector/{id}/oauth/start | write | actions | Start OAuth authorization (redirects to the identity provider). Kept out of read: it starts an OAuth flow. |
| GET | api/actions/connector_types | read | actions | Get connector types. |
| GET | api/actions/connectors | read | actions | Get all connectors. |
| POST | api/actions/events/{id}/{id} | write | actions | Ingest an external event for a Kibana connector. |
| GET | api/agent_builder/a2a/{id} | read | agent_builder | Get A2A agent card. |
| POST | api/agent_builder/a2a/{id} | write | agent_builder | Send A2A task. |
| GET | api/agent_builder/agents | read | agent_builder | List agents. |
| POST | api/agent_builder/agents | write | agent_builder | Create an agent. |
| GET | api/agent_builder/agents/{id} | read | agent_builder | Get an agent by ID. |
| PUT | api/agent_builder/agents/{id} | write | agent_builder | Update an agent. |
| DELETE | api/agent_builder/agents/{id} | write | agent_builder | Delete an agent. |
| GET | api/agent_builder/agents/{id}/access_control | read | agent_builder | Get an agent's access control list. |
| PUT | api/agent_builder/agents/{id}/access_control | write | agent_builder | Update an agent's access control list. |
| POST | api/agent_builder/agents/{id}/consumption | read | agent_builder | Get agent consumption data. |
| GET | api/agent_builder/conversations | read | agent_builder | List conversations. |
| POST | api/agent_builder/conversations | write | agent_builder | Create conversation. |
| GET | api/agent_builder/conversations/{id} | read | agent_builder | Get conversation by ID. |
| DELETE | api/agent_builder/conversations/{id} | write | agent_builder | Delete conversation by ID. |
| POST | api/agent_builder/conversations/{id}/_add_events | write | agent_builder | Add events to a conversation. |
| PUT | api/agent_builder/conversations/{id}/access_control | write | agent_builder | Update a conversation's access control. |
| GET | api/agent_builder/conversations/{id}/attachments | read | agent_builder | List conversation attachments. |
| POST | api/agent_builder/conversations/{id}/attachments | write | agent_builder | Create conversation attachment. |
| GET | api/agent_builder/conversations/{id}/attachments/stale | read | agent_builder | Check attachment staleness. |
| GET | api/agent_builder/conversations/{id}/attachments/{id} | read | agent_builder | Get conversation attachment. |
| PUT | api/agent_builder/conversations/{id}/attachments/{id} | write | agent_builder | Update conversation attachment. |
| PATCH | api/agent_builder/conversations/{id}/attachments/{id} | write | agent_builder | Rename attachment. |
| DELETE | api/agent_builder/conversations/{id}/attachments/{id} | write | agent_builder | Delete conversation attachment. |
| POST | api/agent_builder/conversations/{id}/attachments/{id}/_restore | write | agent_builder | Restore deleted attachment. |
| PUT | api/agent_builder/conversations/{id}/attachments/{id}/origin | write | agent_builder | Update attachment origin. |
| POST | api/agent_builder/converse | write | agent_builder | Send chat message. |
| POST | api/agent_builder/converse/async | write | agent_builder | Send chat message (streaming). |
| POST | api/agent_builder/mcp | write | agent_builder | MCP server. |
| GET | api/agent_builder/plugins | read | agent_builder | List plugins. |
| POST | api/agent_builder/plugins/install | write | agent_builder | Install a plugin. |
| GET | api/agent_builder/plugins/{id} | read | agent_builder | Get a plugin by id. |
| DELETE | api/agent_builder/plugins/{id} | write | agent_builder | Delete a plugin. |
| GET | api/agent_builder/skills | read | agent_builder | List skills. |
| POST | api/agent_builder/skills | write | agent_builder | Create a skill. |
| GET | api/agent_builder/skills/{id} | read | agent_builder | Get a skill by id. |
| PUT | api/agent_builder/skills/{id} | write | agent_builder | Update a skill. |
| DELETE | api/agent_builder/skills/{id} | write | agent_builder | Delete a skill. |
| GET | api/agent_builder/tools | read | agent_builder | List tools. |
| POST | api/agent_builder/tools | write | agent_builder | Create a tool. |
| POST | api/agent_builder/tools/_execute | write | agent_builder | Run a tool. |
| GET | api/agent_builder/tools/{id} | read | agent_builder | Get a tool by id. |
| PUT | api/agent_builder/tools/{id} | write | agent_builder | Update a tool. |
| DELETE | api/agent_builder/tools/{id} | write | agent_builder | Delete a tool. |
| GET | api/alerting/_health | read | alerting | Get the alerting framework health. |
| GET | api/alerting/rule/{id} | read | alerting | Get rule details. |
| POST | api/alerting/rule/{id} | write | alerting | Create a rule. |
| PUT | api/alerting/rule/{id} | write | alerting | Update a rule. |
| DELETE | api/alerting/rule/{id} | write | alerting | Delete a rule. |
| POST | api/alerting/rule/{id}/_disable | write | alerting | Disable a rule. |
| POST | api/alerting/rule/{id}/_enable | write | alerting | Enable a rule. |
| POST | api/alerting/rule/{id}/_mute_all | write | alerting | Mute all alerts. |
| POST | api/alerting/rule/{id}/_unmute_all | write | alerting | Unmute all alerts. |
| POST | api/alerting/rule/{id}/_update_api_key | write | alerting | Update the API key for a rule. |
| POST | api/alerting/rule/{id}/alert/{id}/_mute | write | alerting | Mute an alert. |
| POST | api/alerting/rule/{id}/alert/{id}/_snooze | write | alerting | Snooze an alert. |
| POST | api/alerting/rule/{id}/alert/{id}/_unmute | write | alerting | Unmute an alert. |
| POST | api/alerting/rule/{id}/alert/{id}/_unsnooze | write | alerting | Unsnooze an alert. |
| GET | api/alerting/rule/{id}/query_inspector | read | alerting | Get the Elasticsearch query for a rule. |
| POST | api/alerting/rule/{id}/snooze_schedule | write | alerting | Schedule a snooze for the rule. |
| DELETE | api/alerting/rule/{id}/snooze_schedule/{id} | write | alerting | Delete a snooze schedule for a rule. |
| GET | api/alerting/rule_types | read | alerting | Get the rule types. |
| GET | api/alerting/rules/_find | read | alerting | Get information about rules. |
| POST | api/alerting/rules/backfill/_find | read | alerting | Find backfills for rules. |
| POST | api/alerting/rules/backfill/_schedule | write | alerting | Schedule a backfill for rules. |
| GET | api/alerting/rules/backfill/{id} | read | alerting | Get a backfill by ID. |
| DELETE | api/alerting/rules/backfill/{id} | write | alerting | Delete a backfill by ID. |
| GET | api/alerting/v2/action_policies | read | alerting | List action policies. |
| POST | api/alerting/v2/action_policies | write | alerting | Create an action policy. |
| POST | api/alerting/v2/action_policies/_bulk_delete | write | alerting | Delete action policies in bulk by ID. |
| POST | api/alerting/v2/action_policies/_bulk_disable | write | alerting | Disable action policies in bulk by ID. |
| POST | api/alerting/v2/action_policies/_bulk_enable | write | alerting | Enable action policies in bulk by ID. |
| POST | api/alerting/v2/action_policies/_bulk_snooze | write | alerting | Snooze action policies in bulk by ID. |
| POST | api/alerting/v2/action_policies/_bulk_unsnooze | write | alerting | Cancel snooze for action policies in bulk by ID. |
| POST | api/alerting/v2/action_policies/_bulk_update_api_key | write | alerting | Rotate API keys for action policies in bulk by ID. |
| GET | api/alerting/v2/action_policies/{id} | read | alerting | Get an action policy. |
| PUT | api/alerting/v2/action_policies/{id} | write | alerting | Create or replace an action policy. |
| PATCH | api/alerting/v2/action_policies/{id} | write | alerting | Partially update an action policy. |
| DELETE | api/alerting/v2/action_policies/{id} | write | alerting | Delete an action policy. |
| POST | api/alerting/v2/action_policies/{id}/_disable | write | alerting | Disable an action policy. |
| POST | api/alerting/v2/action_policies/{id}/_enable | write | alerting | Enable an action policy. |
| POST | api/alerting/v2/action_policies/{id}/_snooze | write | alerting | Snooze an action policy. |
| POST | api/alerting/v2/action_policies/{id}/_unsnooze | write | alerting | Unsnooze an action policy. |
| POST | api/alerting/v2/action_policies/{id}/_update_api_key | write | alerting | Update an action policy API key. |
| POST | api/alerting/v2/alerts/_bulk_ack | write | alerting | Bulk acknowledge alerts. |
| POST | api/alerting/v2/alerts/_bulk_activate | write | alerting | Bulk activate alerts. |
| POST | api/alerting/v2/alerts/_bulk_assign | write | alerting | Bulk assign alerts. |
| POST | api/alerting/v2/alerts/_bulk_deactivate | write | alerting | Bulk deactivate alerts. |
| POST | api/alerting/v2/alerts/_bulk_tag | write | alerting | Bulk tag alerts. |
| POST | api/alerting/v2/alerts/_bulk_unack | write | alerting | Bulk unacknowledge alerts. |
| POST | api/alerting/v2/alerts/{id}/_ack | write | alerting | Acknowledge an alert. |
| POST | api/alerting/v2/alerts/{id}/_activate | write | alerting | Activate an alert. |
| POST | api/alerting/v2/alerts/{id}/_assign | write | alerting | Assign an alert to a user. |
| POST | api/alerting/v2/alerts/{id}/_deactivate | write | alerting | Deactivate an alert. |
| POST | api/alerting/v2/alerts/{id}/_tag | write | alerting | Tag an alert. |
| POST | api/alerting/v2/alerts/{id}/_unack | write | alerting | Unacknowledge an alert. |
| GET | api/alerting/v2/execution_history/action_policies | read | alerting | List action policy executions. |
| GET | api/alerting/v2/execution_history/rules | read | alerting | List rule executions. |
| GET | api/alerting/v2/rules | read | alerting | List rules. |
| POST | api/alerting/v2/rules | write | alerting | Create a rule. |
| POST | api/alerting/v2/rules/_bulk_create | write | alerting | Create rules in bulk. |
| POST | api/alerting/v2/rules/_bulk_delete | write | alerting | Delete rules in bulk by ID. |
| POST | api/alerting/v2/rules/_bulk_disable | write | alerting | Disable rules in bulk by ID. |
| POST | api/alerting/v2/rules/_bulk_enable | write | alerting | Enable rules in bulk by ID. |
| POST | api/alerting/v2/rules/_bulk_get | read | alerting | Get rules in bulk. |
| POST | api/alerting/v2/rules/_bulk_update_api_key | write | alerting | Update the API key of rules in bulk by ID. |
| POST | api/alerting/v2/rules/_delete_by_query | write | alerting | Delete rules matching a query (dry-run by default). |
| POST | api/alerting/v2/rules/_disable_by_query | write | alerting | Disable rules matching a query (dry-run by default). |
| POST | api/alerting/v2/rules/_enable_by_query | write | alerting | Enable rules matching a query (dry-run by default). |
| POST | api/alerting/v2/rules/_update_api_key_by_query | write | alerting | Update the API key of rules matching a query (dry-run by default). |
| GET | api/alerting/v2/rules/{id} | read | alerting | Get a rule. |
| PUT | api/alerting/v2/rules/{id} | write | alerting | Create or replace a rule. |
| PATCH | api/alerting/v2/rules/{id} | write | alerting | Update a rule. |
| DELETE | api/alerting/v2/rules/{id} | write | alerting | Delete a rule. |
| POST | api/alerting/v2/rules/{id}/_disable | write | alerting | Disable a rule. |
| POST | api/alerting/v2/rules/{id}/_enable | write | alerting | Enable a rule. |
| POST | api/alerting/v2/rules/{id}/_run | write | alerting | Run a rule now. |
| POST | api/apm/agent_keys | write | apm | Create an APM agent key. |
| POST | api/apm/fleet/apm_server_schema | write | apm | Save APM server schema. |
| POST | api/apm/services/{id}/annotation | write | apm | Create a service annotation. |
| GET | api/apm/services/{id}/annotation/search | read | apm | Search for annotations. |
| GET | api/apm/settings/agent-configuration | read | apm | Get a list of agent configurations. |
| PUT | api/apm/settings/agent-configuration | write | apm | Create or update agent configuration. |
| DELETE | api/apm/settings/agent-configuration | write | apm | Delete agent configuration. |
| GET | api/apm/settings/agent-configuration/agent_name | read | apm | Get agent name for service. |
| GET | api/apm/settings/agent-configuration/environments | read | apm | Get environments for service. |
| POST | api/apm/settings/agent-configuration/search | read | apm | Lookup single agent configuration. |
| GET | api/apm/settings/agent-configuration/view | read | apm | Get single agent configuration. |
| GET | api/apm/sourcemaps | read | apm | Get source maps. |
| POST | api/apm/sourcemaps | write | apm | Upload a source map. |
| DELETE | api/apm/sourcemaps/{id} | write | apm | Delete source map. |
| GET | api/asset_criticality | read | asset_criticality | Get an asset criticality record. |
| POST | api/asset_criticality | write | asset_criticality | Upsert an asset criticality record. |
| DELETE | api/asset_criticality | write | asset_criticality | Delete an asset criticality record. |
| POST | api/asset_criticality/bulk | write | asset_criticality | Bulk upsert asset criticality records. |
| GET | api/asset_criticality/list | read | asset_criticality | List asset criticality records. |
| POST | api/attack_discovery/_bulk | write | attack_discovery | Bulk update Attack discoveries. |
| GET | api/attack_discovery/_find | read | attack_discovery | Find Attack discoveries that match the search criteria. |
| POST | api/attack_discovery/_generate | write | attack_discovery | Generate attack discoveries from alerts. |
| GET | api/attack_discovery/generations | read | attack_discovery | Get the latest Attack Discovery generations metadata for the current user. |
| GET | api/attack_discovery/generations/{id} | read | attack_discovery | Get a single Attack Discovery generation, including its discoveries and (optional) generation metadata. |
| POST | api/attack_discovery/generations/{id}/_dismiss | write | attack_discovery | Dismiss an Attack Discovery generation. |
| POST | api/attack_discovery/schedules | write | attack_discovery | Create Attack Discovery schedule. |
| POST | api/attack_discovery/schedules/_bulk_delete | write | attack_discovery | Bulk delete Attack Discovery schedules. |
| POST | api/attack_discovery/schedules/_bulk_disable | write | attack_discovery | Bulk disable Attack Discovery schedules. |
| POST | api/attack_discovery/schedules/_bulk_enable | write | attack_discovery | Bulk enable Attack Discovery schedules. |
| GET | api/attack_discovery/schedules/_find | read | attack_discovery | Find Attack Discovery schedules that match the search criteria. |
| GET | api/attack_discovery/schedules/{id} | read | attack_discovery | Get Attack Discovery schedule by ID. |
| PUT | api/attack_discovery/schedules/{id} | write | attack_discovery | Update Attack Discovery schedule. |
| DELETE | api/attack_discovery/schedules/{id} | write | attack_discovery | Delete Attack Discovery schedule. |
| POST | api/attack_discovery/schedules/{id}/_disable | write | attack_discovery | Disable Attack Discovery schedule. |
| POST | api/attack_discovery/schedules/{id}/_enable | write | attack_discovery | Enable Attack Discovery schedule. |
| POST | api/cases | write | cases | Create a case. |
| PATCH | api/cases | write | cases | Update cases. |
| DELETE | api/cases | write | cases | Delete cases. |
| GET | api/cases/_find | read | cases | Search cases. |
| GET | api/cases/alerts/{id} | read | cases | Get cases for an alert. |
| GET | api/cases/configure | read | cases | Get case settings. |
| POST | api/cases/configure | write | cases | Add case settings. |
| GET | api/cases/configure/connectors/_find | read | cases | Get case connectors. |
| PATCH | api/cases/configure/{id} | write | cases | Update case settings. |
| GET | api/cases/field_definitions | read | cases | Get all field definitions. |
| POST | api/cases/field_definitions | write | cases | Create a field definition. |
| GET | api/cases/field_definitions/{id} | read | cases | Get a field definition by ID. |
| PUT | api/cases/field_definitions/{id} | write | cases | Update a field definition. |
| DELETE | api/cases/field_definitions/{id} | write | cases | Delete a field definition. |
| GET | api/cases/fields | read | cases | Get the fields applicable to a case. |
| GET | api/cases/reporters | read | cases | Get case creators. |
| GET | api/cases/tags | read | cases | Get case tags. |
| GET | api/cases/templates | read | cases | Get all case templates. |
| POST | api/cases/templates | write | cases | Create a case template. |
| GET | api/cases/templates/{id} | read | cases | Get a case template by ID. |
| PUT | api/cases/templates/{id} | write | cases | Update a case template. |
| DELETE | api/cases/templates/{id} | write | cases | Delete a case template. |
| GET | api/cases/{id} | read | cases | Get case information. |
| GET | api/cases/{id}/alerts | read | cases | Get all alerts for a case. |
| GET | api/cases/{id}/attachments | read | cases | Find case attachments. |
| POST | api/cases/{id}/attachments | write | cases | Create a case attachment. |
| DELETE | api/cases/{id}/attachments | write | cases | Delete all case attachments. |
| GET | api/cases/{id}/attachments/{id} | read | cases | Get a case attachment. |
| PUT | api/cases/{id}/attachments/{id} | write | cases | Replace a case attachment. |
| DELETE | api/cases/{id}/attachments/{id} | write | cases | Delete a case attachment. |
| POST | api/cases/{id}/comments | write | cases | Add a case comment or alert. |
| PATCH | api/cases/{id}/comments | write | cases | Update a case comment or alert. |
| DELETE | api/cases/{id}/comments | write | cases | Delete all case comments and alerts. |
| GET | api/cases/{id}/comments/_find | read | cases | Find case comments. |
| GET | api/cases/{id}/comments/{id} | read | cases | Get a case comment or alert. |
| DELETE | api/cases/{id}/comments/{id} | write | cases | Delete a case comment or alert. |
| POST | api/cases/{id}/connector/{id}/_push | write | cases | Push a case to an external service. |
| GET | api/cases/{id}/fields | read | cases | Get the fields applicable to an existing case. |
| POST | api/cases/{id}/files | write | cases | Attach a file to a case. |
| GET | api/cases/{id}/user_actions/_find | read | cases | Find case activity. |
| POST | api/chat/message | write | chat | Send a message and get the answer. |
| GET | api/context_engine/ai_index | read | context_engine | List AI Indices. |
| POST | api/context_engine/ai_index | write | context_engine | Create an AI Index. |
| POST | api/context_engine/ai_index/_query | read | context_engine | Query AI Indices. |
| GET | api/context_engine/ai_index/{id} | read | context_engine | Get an AI Index. |
| PUT | api/context_engine/ai_index/{id} | write | context_engine | Create or update an AI Index. |
| DELETE | api/context_engine/ai_index/{id} | write | context_engine | Delete an AI Index. |
| GET | api/context_engine/ai_index/{id}/_describe | read | context_engine | Describe an AI Index. |
| POST | api/context_engine/memory/_forget | write | context_engine | Forget session memories. |
| POST | api/context_engine/memory/_remember | write | context_engine | Remember a session memory. |
| POST | api/context_engine/memory/_save_event | write | context_engine | Save session events. |
| GET | api/dashboards | read | dashboards | Search dashboards. |
| POST | api/dashboards | write | dashboards | Create a dashboard. |
| GET | api/dashboards/{id} | read | dashboards | Get a dashboard. |
| PUT | api/dashboards/{id} | write | dashboards | Upsert a dashboard. |
| DELETE | api/dashboards/{id} | write | dashboards | Delete a dashboard. |
| GET | api/data_views | read | data_views | Get all data views. |
| POST | api/data_views/data_view | write | data_views | Create a data view. |
| GET | api/data_views/data_view/{id} | read | data_views | Get a data view. |
| POST | api/data_views/data_view/{id} | write | data_views | Update a data view. |
| DELETE | api/data_views/data_view/{id} | write | data_views | Delete a data view. |
| POST | api/data_views/data_view/{id}/fields | write | data_views | Update field metadata. |
| POST | api/data_views/data_view/{id}/runtime_field | write | data_views | Create a runtime field. |
| PUT | api/data_views/data_view/{id}/runtime_field | write | data_views | Create or update a runtime field. |
| GET | api/data_views/data_view/{id}/runtime_field/{id} | read | data_views | Get a runtime field. |
| POST | api/data_views/data_view/{id}/runtime_field/{id} | write | data_views | Update a runtime field. |
| DELETE | api/data_views/data_view/{id}/runtime_field/{id} | write | data_views | Delete a runtime field. |
| GET | api/data_views/default | read | data_views | Get the default data view. |
| POST | api/data_views/default | write | data_views | Set the default data view. |
| POST | api/data_views/swap_references | write | data_views | Swap saved object references. |
| POST | api/data_views/swap_references/_preview | read | data_views | Preview swap references. |
| GET | api/data_views/v2 | read | data_views | Search data views. |
| POST | api/data_views/v2 | write | data_views | Create a data view. |
| GET | api/data_views/v2/{id} | read | data_views | Get a data view. |
| PUT | api/data_views/v2/{id} | write | data_views | Upsert a data view. |
| DELETE | api/data_views/v2/{id} | write | data_views | Delete a data view. |
| POST | api/detection_engine/attacks/assignees | write | detection_engine | Assign and unassign users from attack discovery alerts. |
| POST | api/detection_engine/attacks/search | read | detection_engine | Find and/or aggregate attack discovery alerts. |
| POST | api/detection_engine/attacks/status | write | detection_engine | Set attack discovery alerts workflow status. |
| POST | api/detection_engine/attacks/tags | write | detection_engine | Add and remove attack discovery alert tags. |
| GET | api/detection_engine/index | read | detection_engine | Reads the alert index name if it exists. |
| POST | api/detection_engine/index | write | detection_engine | Create an alerts index. |
| DELETE | api/detection_engine/index | write | detection_engine | Delete an alerts index. |
| GET | api/detection_engine/privileges | read | detection_engine | Returns user privileges for the Kibana space. |
| GET | api/detection_engine/rules | read | detection_engine | Retrieve a detection rule. |
| POST | api/detection_engine/rules | write | detection_engine | Create a detection rule. |
| PUT | api/detection_engine/rules | write | detection_engine | Update a detection rule. |
| PATCH | api/detection_engine/rules | write | detection_engine | Patch a detection rule. |
| DELETE | api/detection_engine/rules | write | detection_engine | Delete a detection rule. |
| POST | api/detection_engine/rules/_bulk_action | write | detection_engine | Apply a bulk action to detection rules. |
| POST | api/detection_engine/rules/_export | read | detection_engine | Export detection rules. |
| GET | api/detection_engine/rules/_find | read | detection_engine | List all detection rules. |
| POST | api/detection_engine/rules/_import | write | detection_engine | Import detection rules. |
| PUT | api/detection_engine/rules/prepackaged | write | detection_engine | Install prebuilt detection rules and Timelines. |
| GET | api/detection_engine/rules/prepackaged/_status | read | detection_engine | Retrieve the status of prebuilt detection rules and Timelines. |
| POST | api/detection_engine/rules/preview | write | detection_engine | Preview rule alerts generated on specified time range. |
| POST | api/detection_engine/rules/{id}/exceptions | write | detection_engine | Create rule exception items. |
| POST | api/detection_engine/signals/assignees | write | detection_engine | Assign and unassign users from detection alerts. |
| POST | api/detection_engine/signals/finalize_migration | write | detection_engine | Finalize detection alert migrations. |
| POST | api/detection_engine/signals/migration | write | detection_engine | Initiate a detection alert migration. |
| DELETE | api/detection_engine/signals/migration | write | detection_engine | Clean up detection alert migrations. |
| GET | api/detection_engine/signals/migration_status | read | detection_engine | Retrieve the status of detection alert migrations. |
| POST | api/detection_engine/signals/search | read | detection_engine | Find and/or aggregate detection alerts. |
| POST | api/detection_engine/signals/status | write | detection_engine | Set a detection alert status. |
| POST | api/detection_engine/signals/tags | write | detection_engine | Add and remove detection alert tags. |
| GET | api/detection_engine/tags | read | detection_engine | List all detection rule tags. |
| GET | api/discover_sessions | read | discover_sessions | Search Discover sessions. |
| POST | api/discover_sessions | write | discover_sessions | Create a Discover session. |
| GET | api/discover_sessions/{id} | read | discover_sessions | Get a Discover session. |
| PUT | api/discover_sessions/{id} | write | discover_sessions | Upsert a Discover session. |
| DELETE | api/discover_sessions/{id} | write | discover_sessions | Delete a Discover session. |
| POST | api/encrypted_saved_objects/_rotate_key | write | encrypted_saved_objects | Rotate a key for encrypted saved objects. |
| GET | api/endpoint/action | read | endpoint | Get response actions. |
| POST | api/endpoint/action/cancel | write | endpoint | Cancel a response action. |
| POST | api/endpoint/action/execute | write | endpoint | Run a command. |
| POST | api/endpoint/action/get_file | write | endpoint | Get a file. |
| POST | api/endpoint/action/isolate | write | endpoint | Isolate an endpoint. |
| POST | api/endpoint/action/kill_process | write | endpoint | Terminate a process. |
| POST | api/endpoint/action/memory_dump | write | endpoint | Generate a memory dump from the host machine. |
| POST | api/endpoint/action/run_script | write | endpoint | Run a script. |
| POST | api/endpoint/action/running_procs | write | endpoint | Get running processes. |
| POST | api/endpoint/action/scan | write | endpoint | Scan a file or directory. |
| GET | api/endpoint/action/state | read | endpoint | Get actions state. |
| POST | api/endpoint/action/suspend_process | write | endpoint | Suspend a process. |
| POST | api/endpoint/action/unisolate | write | endpoint | Release an isolated endpoint. |
| POST | api/endpoint/action/upload | write | endpoint | Upload a file. |
| GET | api/endpoint/action/{id} | read | endpoint | Get action details. |
| GET | api/endpoint/action/{id}/file/{id} | read | endpoint | Get file information. |
| GET | api/endpoint/action/{id}/file/{id}/download | read | endpoint | Download a file. |
| GET | api/endpoint/action_status | read | endpoint | Get response actions status. |
| GET | api/endpoint/metadata | read | endpoint | Get a metadata list. |
| GET | api/endpoint/metadata/{id} | read | endpoint | Get metadata. |
| GET | api/endpoint/policy_response | read | endpoint | Get a policy response. |
| GET | api/endpoint/protection_updates_note/{id} | read | endpoint | Get a protection updates note. |
| POST | api/endpoint/protection_updates_note/{id} | write | endpoint | Create or update a protection updates note. |
| GET | api/endpoint/scripts_library | read | endpoint | Get a list of scripts. |
| POST | api/endpoint/scripts_library | write | endpoint | Create script. |
| GET | api/endpoint/scripts_library/{id} | read | endpoint | Get script. |
| PATCH | api/endpoint/scripts_library/{id} | write | endpoint | Update script. |
| DELETE | api/endpoint/scripts_library/{id} | write | endpoint | Delete a script. |
| GET | api/endpoint/scripts_library/{id}/download | read | endpoint | Download a script file. |
| POST | api/endpoint_list | write | endpoint_list | Create an Elastic Endpoint rule exception list. |
| GET | api/endpoint_list/items | read | endpoint_list | Get an Elastic Endpoint rule exception list item. |
| POST | api/endpoint_list/items | write | endpoint_list | Create an Elastic Endpoint rule exception list item. |
| PUT | api/endpoint_list/items | write | endpoint_list | Update an Elastic Endpoint rule exception list item. |
| DELETE | api/endpoint_list/items | write | endpoint_list | Delete an Elastic Endpoint exception list item. |
| GET | api/endpoint_list/items/_find | read | endpoint_list | Get Elastic Endpoint exception list items. |
| DELETE | api/entity_analytics/monitoring/engine/delete | write | entity_analytics | Delete the Privilege Monitoring Engine. |
| POST | api/entity_analytics/monitoring/engine/disable | write | entity_analytics | Disable the Privilege Monitoring Engine. |
| POST | api/entity_analytics/monitoring/engine/init | write | entity_analytics | Initialize the Privilege Monitoring Engine. |
| POST | api/entity_analytics/monitoring/engine/schedule_now | write | entity_analytics | Schedule the Privilege Monitoring Engine. |
| GET | api/entity_analytics/monitoring/privileges/health | read | entity_analytics | Health check on Privilege Monitoring. |
| GET | api/entity_analytics/monitoring/privileges/privileges | read | entity_analytics | Run a privileges check on Privilege Monitoring. |
| POST | api/entity_analytics/monitoring/users | write | entity_analytics | Create a new monitored user. |
| POST | api/entity_analytics/monitoring/users/_csv | write | entity_analytics | Upsert multiple monitored users via CSV upload. |
| GET | api/entity_analytics/monitoring/users/list | read | entity_analytics | List all monitored users. |
| PUT | api/entity_analytics/monitoring/users/{id} | write | entity_analytics | Update a monitored user. |
| DELETE | api/entity_analytics/monitoring/users/{id} | write | entity_analytics | Delete a monitored user. |
| POST | api/entity_analytics/privileged_user_monitoring/pad/install | write | entity_analytics | Installs the privileged access detection package for the Entity Analytics privileged user monitoring experience. |
| GET | api/entity_analytics/privileged_user_monitoring/pad/status | read | entity_analytics | Gets the status of the privileged access detection package for the Entity Analytics privileged user monitoring experience. |
| POST | api/entity_analytics/watchlists | write | entity_analytics | Create a new watchlist. |
| GET | api/entity_analytics/watchlists/list | read | entity_analytics | List all watchlists. |
| GET | api/entity_analytics/watchlists/{id} | read | entity_analytics | Get a watchlist by ID. |
| PUT | api/entity_analytics/watchlists/{id} | write | entity_analytics | Update an existing watchlist. |
| POST | api/entity_analytics/watchlists/{id}/csv_upload | write | entity_analytics | Upload a CSV file to add entities to a watchlist. |
| POST | api/entity_analytics/watchlists/{id}/entities/assign | write | entity_analytics | Manually assign entities to a watchlist. |
| POST | api/entity_analytics/watchlists/{id}/entities/unassign | write | entity_analytics | Manually unassign entities from a watchlist. |
| GET | api/exception_lists | read | exception_lists | Get exception list details. |
| POST | api/exception_lists | write | exception_lists | Create an exception list. |
| PUT | api/exception_lists | write | exception_lists | Update an exception list. |
| DELETE | api/exception_lists | write | exception_lists | Delete an exception list. |
| POST | api/exception_lists/_duplicate | write | exception_lists | Duplicate an exception list. |
| POST | api/exception_lists/_export | read | exception_lists | Export an exception list. |
| GET | api/exception_lists/_find | read | exception_lists | Get exception lists. |
| POST | api/exception_lists/_import | write | exception_lists | Import an exception list. |
| GET | api/exception_lists/items | read | exception_lists | Get an exception list item. |
| POST | api/exception_lists/items | write | exception_lists | Create an exception list item. |
| PUT | api/exception_lists/items | write | exception_lists | Update an exception list item. |
| DELETE | api/exception_lists/items | write | exception_lists | Delete an exception list item. |
| GET | api/exception_lists/items/_find | read | exception_lists | Get exception list items. |
| GET | api/exception_lists/summary | read | exception_lists | Get an exception list summary. |
| POST | api/exceptions/shared | write | exceptions | Create a shared exception list. |
| GET | api/features | read | features | Get features. |
| GET | api/fleet/agent_download_sources | write | fleet | Get agent binary download sources. Kept out of read: sources can include passwords and API keys. |
| POST | api/fleet/agent_download_sources | write | fleet | Create an agent binary download source. |
| GET | api/fleet/agent_download_sources/{id} | write | fleet | Get an agent binary download source. Kept out of read: sources can include passwords and API keys. |
| PUT | api/fleet/agent_download_sources/{id} | write | fleet | Update an agent binary download source. |
| DELETE | api/fleet/agent_download_sources/{id} | write | fleet | Delete an agent binary download source. |
| GET | api/fleet/agent_policies | write | fleet | Get agent policies. Kept out of read: embeds package policies, whose vars can include credentials. |
| POST | api/fleet/agent_policies | write | fleet | Create an agent policy. |
| POST | api/fleet/agent_policies/_bulk_get | write | fleet | Bulk get agent policies. Kept out of read: embeds package policies, whose vars can include credentials. |
| POST | api/fleet/agent_policies/delete | write | fleet | Delete an agent policy. |
| POST | api/fleet/agent_policies/outputs | read | fleet | Get outputs for agent policies. |
| GET | api/fleet/agent_policies/{id} | write | fleet | Get an agent policy. Kept out of read: embeds package policies, whose vars can include credentials. |
| PUT | api/fleet/agent_policies/{id} | write | fleet | Update an agent policy. |
| GET | api/fleet/agent_policies/{id}/auto_upgrade_agents_status | read | fleet | Get auto upgrade agent status. |
| POST | api/fleet/agent_policies/{id}/copy | write | fleet | Copy an agent policy. |
| GET | api/fleet/agent_policies/{id}/download | write | fleet | Download an agent policy. Kept out of read: the policy file includes output credentials and API keys. |
| GET | api/fleet/agent_policies/{id}/full | write | fleet | Get a full agent policy. Kept out of read: the full policy includes output credentials and API keys. |
| GET | api/fleet/agent_policies/{id}/outputs | read | fleet | Get outputs for an agent policy. |
| GET | api/fleet/agent_status | read | fleet | Get an agent status summary. |
| GET | api/fleet/agent_status/data | read | fleet | Get incoming agent data. |
| GET | api/fleet/agentless_policies | write | fleet | Deprecated: Get managed integrations. Kept out of read: integration vars can include credentials. |
| POST | api/fleet/agentless_policies | write | fleet | Deprecated: Create a managed integration. |
| POST | api/fleet/agentless_policies/_upgrade | write | fleet | Deprecated: Bulk upgrade managed integrations. |
| POST | api/fleet/agentless_policies/_upgrade/dryrun | write | fleet | Deprecated: Preview a managed integrations upgrade. Kept out of read: returns the upgraded policies, whose vars can include credentials. |
| GET | api/fleet/agentless_policies/{id} | write | fleet | Deprecated: Get a managed integration. Kept out of read: integration vars can include credentials. |
| PUT | api/fleet/agentless_policies/{id} | write | fleet | Deprecated: Update a managed integration. |
| DELETE | api/fleet/agentless_policies/{id} | write | fleet | Deprecated: Delete a managed integration. |
| GET | api/fleet/agents | write | fleet | Get agents. Kept out of read: agent records include agent API keys. |
| POST | api/fleet/agents | write | fleet | Get agents by action ids. |
| GET | api/fleet/agents/action_status | read | fleet | Get an agent action status. |
| POST | api/fleet/agents/actions/{id}/cancel | write | fleet | Cancel an agent action. |
| GET | api/fleet/agents/available_versions | read | fleet | Get available agent versions. |
| POST | api/fleet/agents/bulk_migrate | write | fleet | Migrate multiple agents. |
| POST | api/fleet/agents/bulk_privilege_level_change | write | fleet | Bulk change agent privilege level. |
| POST | api/fleet/agents/bulk_reassign | write | fleet | Bulk reassign agents. |
| POST | api/fleet/agents/bulk_remove_collectors | write | fleet | Bulk remove OpAMP collectors. |
| POST | api/fleet/agents/bulk_request_diagnostics | write | fleet | Bulk request diagnostics from agents. |
| POST | api/fleet/agents/bulk_restart | write | fleet | Bulk restart agents. |
| POST | api/fleet/agents/bulk_rollback | write | fleet | Bulk rollback agents. |
| POST | api/fleet/agents/bulk_unenroll | write | fleet | Bulk unenroll agents. |
| POST | api/fleet/agents/bulk_update_agent_tags | write | fleet | Bulk update agent tags. |
| POST | api/fleet/agents/bulk_upgrade | write | fleet | Bulk upgrade agents. |
| DELETE | api/fleet/agents/files/{id} | write | fleet | Delete an uploaded file. |
| GET | api/fleet/agents/files/{id}/{id} | read | fleet | Get an uploaded file. |
| GET | api/fleet/agents/setup | read | fleet | Get agent setup info. |
| POST | api/fleet/agents/setup | write | fleet | Initiate Fleet setup. |
| GET | api/fleet/agents/tags | read | fleet | Get agent tags. |
| GET | api/fleet/agents/{id} | write | fleet | Get an agent. Kept out of read: agent records include agent API keys. |
| PUT | api/fleet/agents/{id} | write | fleet | Update an agent by ID. |
| DELETE | api/fleet/agents/{id} | write | fleet | Delete an agent. |
| POST | api/fleet/agents/{id}/actions | write | fleet | Create an agent action. |
| GET | api/fleet/agents/{id}/effective_config | read | fleet | Get an agent's effective config. |
| POST | api/fleet/agents/{id}/migrate | write | fleet | Migrate a single agent. |
| POST | api/fleet/agents/{id}/privilege_level_change | write | fleet | Change agent privilege level. |
| POST | api/fleet/agents/{id}/reassign | write | fleet | Reassign an agent. |
| POST | api/fleet/agents/{id}/remove_collector | write | fleet | Remove an OpAMP collector. |
| POST | api/fleet/agents/{id}/request_diagnostics | write | fleet | Request agent diagnostics. |
| POST | api/fleet/agents/{id}/restart | write | fleet | Restart an agent. |
| POST | api/fleet/agents/{id}/rollback | write | fleet | Rollback an agent. |
| POST | api/fleet/agents/{id}/unenroll | write | fleet | Unenroll an agent. |
| POST | api/fleet/agents/{id}/upgrade | write | fleet | Upgrade an agent. |
| GET | api/fleet/agents/{id}/uploads | read | fleet | Get agent uploads. |
| GET | api/fleet/check-permissions | read | fleet | Check permissions. |
| GET | api/fleet/cloud_connectors | write | fleet | Get cloud connectors. Kept out of read: connector vars hold cloud credentials. |
| POST | api/fleet/cloud_connectors | write | fleet | Create cloud connector. |
| GET | api/fleet/cloud_connectors/{id} | write | fleet | Get cloud connector. Kept out of read: connector vars hold cloud credentials. |
| PUT | api/fleet/cloud_connectors/{id} | write | fleet | Update cloud connector. |
| DELETE | api/fleet/cloud_connectors/{id} | write | fleet | Delete cloud connector (supports force deletion). |
| GET | api/fleet/cloud_connectors/{id}/usage | read | fleet | Get cloud connector usage (package policies using the connector). |
| GET | api/fleet/cloud_onboarding_deployments | read | fleet | Get cloud onboarding instances. |
| POST | api/fleet/cloud_onboarding_deployments | write | fleet | Create cloud onboarding instance. |
| GET | api/fleet/cloud_onboarding_deployments/connector/{id} | read | fleet | Get cloud onboarding instances by connector ID. |
| GET | api/fleet/cloud_onboarding_deployments/{id} | read | fleet | Get cloud onboarding instance. |
| PUT | api/fleet/cloud_onboarding_deployments/{id} | write | fleet | Update cloud onboarding instance. |
| DELETE | api/fleet/cloud_onboarding_deployments/{id} | write | fleet | Delete cloud onboarding instance. |
| GET | api/fleet/data_streams | read | fleet | Get data streams. |
| GET | api/fleet/data_streams/data | read | fleet | Check if data streams have data. |
| GET | api/fleet/enrollment_api_keys | write | fleet | Get enrollment API keys. Kept out of read: it returns enrollment API keys. |
| POST | api/fleet/enrollment_api_keys | write | fleet | Create an enrollment API key. |
| POST | api/fleet/enrollment_api_keys/_bulk_delete | write | fleet | Bulk revoke or delete enrollment API keys. |
| GET | api/fleet/enrollment_api_keys/{id} | write | fleet | Get an enrollment API key. Kept out of read: it returns the enrollment API key. |
| DELETE | api/fleet/enrollment_api_keys/{id} | write | fleet | Revoke or delete an enrollment API key. |
| POST | api/fleet/epm/bulk_assets | read | fleet | Bulk get assets. |
| GET | api/fleet/epm/categories | read | fleet | Get package categories. |
| POST | api/fleet/epm/custom_integrations | write | fleet | Create a custom integration. |
| PUT | api/fleet/epm/custom_integrations/{id} | write | fleet | Update a custom integration. |
| GET | api/fleet/epm/data_streams | read | fleet | Get data streams. |
| GET | api/fleet/epm/packages | read | fleet | Get packages. |
| POST | api/fleet/epm/packages | write | fleet | Install a package by upload. |
| POST | api/fleet/epm/packages/_bulk | write | fleet | Bulk install packages. |
| POST | api/fleet/epm/packages/_bulk_namespace_customization | write | fleet | Bulk enable/disable namespace-level customization for packages. |
| POST | api/fleet/epm/packages/_bulk_rollback | write | fleet | Bulk rollback packages. |
| GET | api/fleet/epm/packages/_bulk_rollback/{id} | read | fleet | Get Bulk rollback packages details. |
| POST | api/fleet/epm/packages/_bulk_uninstall | write | fleet | Bulk uninstall packages. |
| GET | api/fleet/epm/packages/_bulk_uninstall/{id} | read | fleet | Get Bulk uninstall packages details. |
| POST | api/fleet/epm/packages/_bulk_upgrade | write | fleet | Bulk upgrade packages. |
| GET | api/fleet/epm/packages/_bulk_upgrade/{id} | read | fleet | Get Bulk upgrade packages details. |
| GET | api/fleet/epm/packages/installed | read | fleet | Get installed packages. |
| GET | api/fleet/epm/packages/limited | read | fleet | Get a limited package list. |
| GET | api/fleet/epm/packages/{id} | read | fleet | Get a package. |
| POST | api/fleet/epm/packages/{id} | write | fleet | Install a package from the registry. |
| PUT | api/fleet/epm/packages/{id} | write | fleet | Update package settings. |
| DELETE | api/fleet/epm/packages/{id} | write | fleet | Delete a package. |
| POST | api/fleet/epm/packages/{id}/review_upgrade | write | fleet | Review a pending policy upgrade for a package with deprecations. |
| POST | api/fleet/epm/packages/{id}/rollback | write | fleet | Rollback a package to previous version. |
| GET | api/fleet/epm/packages/{id}/stats | read | fleet | Get package stats. |
| GET | api/fleet/epm/packages/{id}/{id} | read | fleet | Get a package. |
| POST | api/fleet/epm/packages/{id}/{id} | write | fleet | Install a package from the registry. |
| PUT | api/fleet/epm/packages/{id}/{id} | write | fleet | Update package settings. |
| DELETE | api/fleet/epm/packages/{id}/{id} | write | fleet | Delete a package. |
| DELETE | api/fleet/epm/packages/{id}/{id}/datastream_assets | write | fleet | Delete assets for a package. |
| GET | api/fleet/epm/packages/{id}/{id}/dependencies | read | fleet | Get package dependencies. |
| POST | api/fleet/epm/packages/{id}/{id}/kibana_assets | write | fleet | Install Kibana assets for a package. |
| DELETE | api/fleet/epm/packages/{id}/{id}/kibana_assets | write | fleet | Delete Kibana assets for a package. |
| POST | api/fleet/epm/packages/{id}/{id}/rule_assets | write | fleet | Install Kibana alert rule for a package. |
| POST | api/fleet/epm/packages/{id}/{id}/transforms/authorize | write | fleet | Authorize transforms. |
| GET | api/fleet/epm/packages/{id}/{id}/{id} | read | fleet | Get a package file. |
| GET | api/fleet/epm/templates/{id}/{id}/inputs | read | fleet | Get an inputs template. |
| GET | api/fleet/epm/verification_key_id | read | fleet | Get a package signature verification key ID. |
| GET | api/fleet/fleet_server_hosts | write | fleet | Get Fleet Server hosts. Kept out of read: hosts can include TLS private keys and secrets. |
| POST | api/fleet/fleet_server_hosts | write | fleet | Create a Fleet Server host. |
| GET | api/fleet/fleet_server_hosts/{id} | write | fleet | Get a Fleet Server host. Kept out of read: hosts can include TLS private keys and secrets. |
| PUT | api/fleet/fleet_server_hosts/{id} | write | fleet | Update a Fleet Server host. |
| DELETE | api/fleet/fleet_server_hosts/{id} | write | fleet | Delete a Fleet Server host. |
| POST | api/fleet/health_check | read | fleet | Check Fleet Server health. |
| POST | api/fleet/iac_provisioner/callbacks/{id} | write | fleet | Receive a provisioning callback. |
| GET | api/fleet/kubernetes | write | fleet | Get a full K8s agent manifest. Kept out of read: the manifest embeds an enrollment token. |
| GET | api/fleet/kubernetes/download | write | fleet | Download an agent manifest. Kept out of read: the manifest embeds an enrollment token. |
| POST | api/fleet/logstash_api_keys | write | fleet | Generate a Logstash API key. |
| GET | api/fleet/managed_integrations | write | fleet | Get managed integrations. Kept out of read: integration vars can include credentials. |
| POST | api/fleet/managed_integrations | write | fleet | Create a managed integration. |
| POST | api/fleet/managed_integrations/_upgrade | write | fleet | Bulk upgrade managed integrations. |
| POST | api/fleet/managed_integrations/_upgrade/dryrun | write | fleet | Preview a managed integrations upgrade. Kept out of read: returns the upgraded policies, whose vars can include credentials. |
| GET | api/fleet/managed_integrations/{id} | write | fleet | Get a managed integration. Kept out of read: integration vars can include credentials. |
| PUT | api/fleet/managed_integrations/{id} | write | fleet | Update a managed integration. |
| DELETE | api/fleet/managed_integrations/{id} | write | fleet | Delete a managed integration. |
| POST | api/fleet/message_signing_service/rotate_key_pair | write | fleet | Rotate a Fleet message signing key pair. |
| GET | api/fleet/outputs | write | fleet | Get outputs. Kept out of read: outputs can include passwords, service tokens and API keys. |
| POST | api/fleet/outputs | write | fleet | Create output. |
| GET | api/fleet/outputs/{id} | write | fleet | Get output. Kept out of read: outputs can include passwords, service tokens and API keys. |
| PUT | api/fleet/outputs/{id} | write | fleet | Update output. |
| DELETE | api/fleet/outputs/{id} | write | fleet | Delete output. |
| GET | api/fleet/outputs/{id}/health | read | fleet | Get the latest output health. |
| GET | api/fleet/package_policies | write | fleet | Get package policies. Kept out of read: integration vars can include credentials. |
| POST | api/fleet/package_policies | write | fleet | Create a package policy. |
| POST | api/fleet/package_policies/_bulk_get | write | fleet | Bulk get package policies. Kept out of read: integration vars can include credentials. |
| POST | api/fleet/package_policies/delete | write | fleet | Bulk delete package policies. |
| POST | api/fleet/package_policies/upgrade | write | fleet | Upgrade a package policy. |
| POST | api/fleet/package_policies/upgrade/dryrun | write | fleet | Dry run a package policy upgrade. |
| GET | api/fleet/package_policies/{id} | write | fleet | Get a package policy. Kept out of read: integration vars can include credentials. |
| PUT | api/fleet/package_policies/{id} | write | fleet | Update a package policy. |
| DELETE | api/fleet/package_policies/{id} | write | fleet | Delete a package policy. |
| GET | api/fleet/proxies | write | fleet | Get proxies. Kept out of read: proxy objects can include the TLS client certificate_key. |
| POST | api/fleet/proxies | write | fleet | Create a proxy. |
| GET | api/fleet/proxies/{id} | write | fleet | Get a proxy. Kept out of read: proxy objects can include the TLS client certificate_key. |
| PUT | api/fleet/proxies/{id} | write | fleet | Update a proxy. |
| DELETE | api/fleet/proxies/{id} | write | fleet | Delete a proxy. |
| GET | api/fleet/remote_synced_integrations/status | read | fleet | Get remote synced integrations status. |
| GET | api/fleet/remote_synced_integrations/{id}/remote_status | read | fleet | Get remote synced integrations status by outputId. |
| POST | api/fleet/service_tokens | write | fleet | Create a service token. |
| GET | api/fleet/settings | read | fleet | Get settings. |
| PUT | api/fleet/settings | write | fleet | Update settings. |
| POST | api/fleet/setup | write | fleet | Initiate Fleet setup. |
| GET | api/fleet/space_settings | read | fleet | Get space settings. |
| PUT | api/fleet/space_settings | write | fleet | Create space settings. |
| GET | api/fleet/uninstall_tokens | read | fleet | Get metadata for latest uninstall tokens. |
| GET | api/fleet/uninstall_tokens/{id} | write | fleet | Get a decrypted uninstall token. Kept out of read: it returns the decrypted uninstall token. |
| POST | api/fleet/uninstall_tokens/{id}/rotate | write | fleet | Rotate an uninstall token. |
| GET | api/links | read | links | List links library items. |
| POST | api/links | write | links | Create a links library item. |
| GET | api/links/{id} | read | links | Get a links library item by ID. |
| PUT | api/links/{id} | write | links | Upsert links library item. |
| DELETE | api/links/{id} | write | links | Delete a links library item. |
| GET | api/lists | read | lists | Get value list details. |
| POST | api/lists | write | lists | Create a value list. |
| PUT | api/lists | write | lists | Update a value list. |
| PATCH | api/lists | write | lists | Patch a value list. |
| DELETE | api/lists | write | lists | Delete a value list. |
| GET | api/lists/_find | read | lists | Get value lists. |
| GET | api/lists/index | read | lists | Get status of value list data streams. |
| POST | api/lists/index | write | lists | Create list data streams. |
| DELETE | api/lists/index | write | lists | Delete value list data streams. |
| GET | api/lists/items | read | lists | Get a value list item. |
| POST | api/lists/items | write | lists | Create a value list item. |
| PUT | api/lists/items | write | lists | Update a value list item. |
| PATCH | api/lists/items | write | lists | Patch a value list item. |
| DELETE | api/lists/items | write | lists | Delete a value list item. |
| POST | api/lists/items/_export | read | lists | Export value list items. |
| GET | api/lists/items/_find | read | lists | Get value list items. |
| POST | api/lists/items/_import | write | lists | Import value list items. |
| GET | api/lists/privileges | read | lists | Get value list privileges. |
| GET | api/logstash/pipeline/{id} | read | logstash | Get a Logstash pipeline. |
| PUT | api/logstash/pipeline/{id} | write | logstash | Create or update a Logstash pipeline. |
| DELETE | api/logstash/pipeline/{id} | write | logstash | Delete a Logstash pipeline. |
| GET | api/logstash/pipelines | read | logstash | Get all Logstash pipelines. |
| POST | api/maintenance_window | write | maintenance_window | Create a maintenance window. |
| GET | api/maintenance_window/_find | read | maintenance_window | Search for a maintenance window. |
| GET | api/maintenance_window/{id} | read | maintenance_window | Get maintenance window details. |
| PATCH | api/maintenance_window/{id} | write | maintenance_window | Update a maintenance window. |
| DELETE | api/maintenance_window/{id} | write | maintenance_window | Delete a maintenance window. |
| POST | api/maintenance_window/{id}/_archive | write | maintenance_window | Archive a maintenance window. |
| POST | api/maintenance_window/{id}/_unarchive | write | maintenance_window | Unarchive a maintenance window. |
| GET | api/markdowns | read | markdowns | List markdown library items. |
| POST | api/markdowns | write | markdowns | Create a markdown library item. |
| GET | api/markdowns/{id} | read | markdowns | Get a markdown library item by ID. |
| PUT | api/markdowns/{id} | write | markdowns | Upsert a markdown library item. |
| DELETE | api/markdowns/{id} | write | markdowns | Delete a markdown library item. |
| GET | api/ml/saved_objects/sync | write | ml | Sync saved objects in the default space. Kept out of read: it syncs saved objects, changing state. |
| POST | api/ml/saved_objects/update_jobs_spaces | write | ml | Update jobs spaces. |
| POST | api/ml/saved_objects/update_trained_models_spaces | write | ml | Update trained models spaces. |
| GET | api/note | read | note | Get notes. |
| PATCH | api/note | write | note | Add or update a note. |
| DELETE | api/note | write | note | Delete one or more notes. |
| GET | api/observability/slos | read | observability | Get a paginated list of SLOs. |
| POST | api/observability/slos | write | observability | Create an SLO. |
| POST | api/observability/slos/_bulk_delete | write | observability | Bulk delete SLO definitions and their associated summary and rollup data. |
| GET | api/observability/slos/_bulk_delete/{id} | read | observability | Retrieve the status of the bulk deletion. |
| POST | api/observability/slos/_bulk_purge_rollup | write | observability | Batch delete rollup and summary data. |
| POST | api/observability/slos/_bulk_snapshot | read | observability | Compute SLO instance summaries in bulk at a point in time. |
| GET | api/observability/slos/_definitions | read | observability | Get the SLO definitions. |
| POST | api/observability/slos/_delete_instances | write | observability | Batch delete SLO instances. |
| GET | api/observability/slos/{id} | read | observability | Get an SLO. |
| PUT | api/observability/slos/{id} | write | observability | Update an SLO. |
| DELETE | api/observability/slos/{id} | write | observability | Delete an SLO. |
| POST | api/observability/slos/{id}/_reset | write | observability | Reset an SLO. |
| GET | api/observability/slos/{id}/_snapshot | read | observability | Compute an SLO instance summary at a point in time. |
| POST | api/observability/slos/{id}/disable | write | observability | Disable an SLO. |
| POST | api/observability/slos/{id}/enable | write | observability | Enable an SLO. |
| POST | api/observability_ai_assistant/chat/complete | write | observability_ai_assistant | Generate a chat completion. |
| GET | api/osquery/history | read | osquery | Get unified query history. |
| GET | api/osquery/live_queries | read | osquery | Get live queries. |
| POST | api/osquery/live_queries | write | osquery | Create a live query. |
| GET | api/osquery/live_queries/{id} | read | osquery | Get live query details. |
| GET | api/osquery/live_queries/{id}/results/{id} | read | osquery | Get live query results. |
| POST | api/osquery/live_queries/{id}/results/{id}/_export | read | osquery | Export live query results. |
| GET | api/osquery/packs | read | osquery | Get packs. |
| POST | api/osquery/packs | write | osquery | Create a pack. |
| GET | api/osquery/packs/{id} | read | osquery | Get pack details. |
| PUT | api/osquery/packs/{id} | write | osquery | Update a pack. |
| DELETE | api/osquery/packs/{id} | write | osquery | Delete a pack. |
| POST | api/osquery/packs/{id}/copy | write | osquery | Copy a pack. |
| GET | api/osquery/saved_queries | read | osquery | Get saved queries. |
| POST | api/osquery/saved_queries | write | osquery | Create a saved query. |
| GET | api/osquery/saved_queries/{id} | read | osquery | Get saved query details. |
| PUT | api/osquery/saved_queries/{id} | write | osquery | Update a saved query. |
| DELETE | api/osquery/saved_queries/{id} | write | osquery | Delete a saved query. |
| POST | api/osquery/saved_queries/{id}/copy | write | osquery | Copy a saved query. |
| GET | api/osquery/scheduled_results/{id}/{id} | read | osquery | Get scheduled action results. |
| POST | api/osquery/scheduled_results/{id}/{id}/_export | read | osquery | Export scheduled query results. |
| GET | api/osquery/scheduled_results/{id}/{id}/results | read | osquery | Get scheduled query results. |
| PATCH | api/pinned_event | write | pinned_event | Pin/unpin an event. |
| GET | api/profiling/setup/es_resources | read | profiling | Get Universal Profiling setup status. |
| POST | api/profiling/setup/es_resources | write | profiling | Initialize Universal Profiling setup. |
| DELETE | api/risk_score/engine/dangerously_delete_data | write | risk_score | Cleanup the Risk Engine. |
| PATCH | api/risk_score/engine/saved_object/configure | write | risk_score | Configure the Risk Engine Saved Object. |
| GET | api/risk_score/history | read | risk_score | Get risk score history for an entity. |
| POST | api/saved_objects/_bulk_create | write | saved_objects | Create saved objects. |
| POST | api/saved_objects/_bulk_delete | write | saved_objects | Delete saved objects. |
| POST | api/saved_objects/_bulk_get | read | saved_objects | Get saved objects. |
| POST | api/saved_objects/_bulk_resolve | read | saved_objects | Resolve saved objects. |
| PUT | api/saved_objects/_bulk_update | write | saved_objects | Update saved objects. |
| POST | api/saved_objects/_export | read | saved_objects | Export saved objects. |
| GET | api/saved_objects/_find | read | saved_objects | Search for saved objects. |
| POST | api/saved_objects/_import | write | saved_objects | Import saved objects. |
| POST | api/saved_objects/_resolve_import_errors | write | saved_objects | Resolve import errors. |
| GET | api/saved_objects/resolve/{id}/{id} | read | saved_objects | Resolve a saved object. |
| POST | api/saved_objects/{id} | write | saved_objects | Create a saved object. |
| GET | api/saved_objects/{id}/{id} | read | saved_objects | Get a saved object. |
| POST | api/saved_objects/{id}/{id} | write | saved_objects | Create a saved object. |
| PUT | api/saved_objects/{id}/{id} | write | saved_objects | Update a saved object. |
| DELETE | api/saved_objects/{id}/{id} | write | saved_objects | Delete a saved object. |
| PUT | api/security/entity_store | write | security | Update the Entity Store. |
| GET | api/security/entity_store/entities | read | security | List entities. |
| DELETE | api/security/entity_store/entities | write | security | Delete an entity. |
| PUT | api/security/entity_store/entities/bulk | write | security | Bulk update entities. |
| POST | api/security/entity_store/entities/{id} | write | security | Create an entity. |
| PUT | api/security/entity_store/entities/{id} | write | security | Update an entity. |
| PUT | api/security/entity_store/history_snapshot/disable | write | security | Disable the history snapshot task. |
| PUT | api/security/entity_store/history_snapshot/enable | write | security | Enable the history snapshot task. |
| POST | api/security/entity_store/install | write | security | Install the Entity Store. |
| GET | api/security/entity_store/resolution/group | read | security | Get resolution group. |
| POST | api/security/entity_store/resolution/link | write | security | Link entities. |
| GET | api/security/entity_store/resolution/rules | read | security | List entity resolution rules. |
| PUT | api/security/entity_store/resolution/rules/{id}/disable | write | security | Disable an entity resolution rule. |
| PUT | api/security/entity_store/resolution/rules/{id}/enable | write | security | Enable an entity resolution rule. |
| POST | api/security/entity_store/resolution/unlink | write | security | Unlink entities. |
| PUT | api/security/entity_store/start | write | security | Start Entity Store engines. |
| GET | api/security/entity_store/status | read | security | Get Entity Store status. |
| PUT | api/security/entity_store/stop | write | security | Stop Entity Store engines. |
| POST | api/security/entity_store/uninstall | write | security | Uninstall the Entity Store. |
| POST | api/security/entity_store/update_api_key | write | security | Update the API key of the Entity Store tasks. |
| GET | api/security/role | read | security | Get all roles. |
| POST | api/security/role/_query | read | security | Query roles. |
| GET | api/security/role/{id} | read | security | Get a role. |
| PUT | api/security/role/{id} | write | security | Create or update a role. |
| DELETE | api/security/role/{id} | write | security | Delete a role. |
| POST | api/security/roles | write | security | Create or update roles. |
| POST | api/security/session/_invalidate | write | security | Invalidate user sessions. |
| POST | api/security_ai_assistant/anonymization_fields/_bulk_action | write | security_ai_assistant | Apply a bulk action to anonymization fields. |
| GET | api/security_ai_assistant/anonymization_fields/_find | read | security_ai_assistant | Get anonymization fields. |
| POST | api/security_ai_assistant/chat/complete | write | security_ai_assistant | Create a model response. |
| POST | api/security_ai_assistant/current_user/conversations | write | security_ai_assistant | Create a conversation. |
| DELETE | api/security_ai_assistant/current_user/conversations | write | security_ai_assistant | Delete conversations. |
| GET | api/security_ai_assistant/current_user/conversations/_find | read | security_ai_assistant | Get conversations. |
| GET | api/security_ai_assistant/current_user/conversations/{id} | read | security_ai_assistant | Get a conversation. |
| PUT | api/security_ai_assistant/current_user/conversations/{id} | write | security_ai_assistant | Update a conversation. |
| DELETE | api/security_ai_assistant/current_user/conversations/{id} | write | security_ai_assistant | Delete a conversation. |
| GET | api/security_ai_assistant/knowledge_base | read | security_ai_assistant | Read a KnowledgeBase. |
| POST | api/security_ai_assistant/knowledge_base | write | security_ai_assistant | Create a KnowledgeBase. |
| POST | api/security_ai_assistant/knowledge_base/entries | write | security_ai_assistant | Create a Knowledge Base Entry. |
| POST | api/security_ai_assistant/knowledge_base/entries/_bulk_action | write | security_ai_assistant | Applies a bulk action to multiple Knowledge Base Entries. |
| GET | api/security_ai_assistant/knowledge_base/entries/_find | read | security_ai_assistant | Finds Knowledge Base Entries that match the given query. |
| GET | api/security_ai_assistant/knowledge_base/entries/{id} | read | security_ai_assistant | Read a Knowledge Base Entry. |
| PUT | api/security_ai_assistant/knowledge_base/entries/{id} | write | security_ai_assistant | Update a Knowledge Base Entry. |
| DELETE | api/security_ai_assistant/knowledge_base/entries/{id} | write | security_ai_assistant | Deletes a single Knowledge Base Entry using the `id` field. |
| GET | api/security_ai_assistant/knowledge_base/{id} | read | security_ai_assistant | Read a KnowledgeBase for a resource. |
| POST | api/security_ai_assistant/knowledge_base/{id} | write | security_ai_assistant | Create a KnowledgeBase for a resource. |
| POST | api/security_ai_assistant/prompts/_bulk_action | write | security_ai_assistant | Apply a bulk action to prompts. |
| GET | api/security_ai_assistant/prompts/_find | read | security_ai_assistant | Get prompts. |
| POST | api/security_solution/initialize | write | security_solution | Initialize security solution flows. |
| POST | api/short_url | write | short_url | Create a short URL. |
| GET | api/short_url/_slug/{id} | read | short_url | Resolve a short URL. |
| GET | api/short_url/{id} | read | short_url | Get a short URL. |
| DELETE | api/short_url/{id} | write | short_url | Delete a short URL. |
| POST | api/spaces/_copy_saved_objects | write | spaces | Copy saved objects between spaces. |
| POST | api/spaces/_disable_legacy_url_aliases | write | spaces | Disable legacy URL aliases. |
| POST | api/spaces/_get_shareable_references | read | spaces | Get shareable references. |
| POST | api/spaces/_resolve_copy_saved_objects_errors | write | spaces | Resolve conflicts copying saved objects. |
| POST | api/spaces/_update_objects_spaces | write | spaces | Update saved objects in spaces. |
| GET | api/spaces/space | read | spaces | Get all spaces. |
| POST | api/spaces/space | write | spaces | Create a space. |
| GET | api/spaces/space/{id} | read | spaces | Get a space. |
| PUT | api/spaces/space/{id} | write | spaces | Update a space. |
| DELETE | api/spaces/space/{id} | write | spaces | Delete a space. |
| GET | api/status | read | status | Get Kibana's current status. |
| GET | api/streams | read | streams | Get stream list. |
| POST | api/streams/_disable | write | streams | Disable streams. |
| POST | api/streams/_enable | write | streams | Enable streams. |
| POST | api/streams/_resync | write | streams | Resync streams. |
| GET | api/streams/{id} | read | streams | Get a stream. |
| PUT | api/streams/{id} | write | streams | Create or update a stream. |
| DELETE | api/streams/{id} | write | streams | Delete a stream. |
| POST | api/streams/{id}/_fork | write | streams | Fork a stream. |
| GET | api/streams/{id}/_ingest | read | streams | Get ingest stream settings. |
| PUT | api/streams/{id}/_ingest | write | streams | Update ingest stream settings. |
| GET | api/streams/{id}/_query | read | streams | Get query stream settings. |
| PUT | api/streams/{id}/_query | write | streams | Upsert query stream settings. |
| GET | api/streams/{id}/attachments | read | streams | Get stream attachments. |
| POST | api/streams/{id}/attachments/_bulk | write | streams | Bulk update attachments. |
| PUT | api/streams/{id}/attachments/{id}/{id} | write | streams | Link an attachment to a stream. |
| DELETE | api/streams/{id}/attachments/{id}/{id} | write | streams | Unlink an attachment from a stream. |
| POST | api/streams/{id}/content/export | read | streams | Export stream content. |
| POST | api/streams/{id}/content/import | write | streams | Import content into a stream. |
| POST | api/synthetics/monitor/test/{id} | write | synthetics | Trigger an on-demand test run for a monitor. |
| GET | api/synthetics/monitors | read | synthetics | Search monitors. |
| POST | api/synthetics/monitors | write | synthetics | Create a monitor. |
| POST | api/synthetics/monitors/_bulk_create | write | synthetics | Bulk create monitors. |
| POST | api/synthetics/monitors/_bulk_delete | write | synthetics | Delete monitors. |
| PUT | api/synthetics/monitors/_bulk_update | write | synthetics | Bulk update monitors. |
| GET | api/synthetics/monitors/{id} | read | synthetics | Get a monitor. |
| PUT | api/synthetics/monitors/{id} | write | synthetics | Update a monitor. |
| DELETE | api/synthetics/monitors/{id} | write | synthetics | Delete a monitor. |
| GET | api/synthetics/params | write | synthetics | Search parameters. Kept out of read: parameter values are commonly secrets. |
| POST | api/synthetics/params | write | synthetics | Add parameters. |
| POST | api/synthetics/params/_bulk_delete | write | synthetics | Delete parameters. |
| GET | api/synthetics/params/{id} | write | synthetics | Get a parameter. Kept out of read: parameter values are commonly secrets. |
| PUT | api/synthetics/params/{id} | write | synthetics | Update a parameter. |
| DELETE | api/synthetics/params/{id} | write | synthetics | Delete a parameter. |
| GET | api/synthetics/private_locations | read | synthetics | Get private locations. |
| POST | api/synthetics/private_locations | write | synthetics | Create a private location. |
| GET | api/synthetics/private_locations/{id} | read | synthetics | Get a private location. |
| PUT | api/synthetics/private_locations/{id} | write | synthetics | Update a private location. |
| DELETE | api/synthetics/private_locations/{id} | write | synthetics | Delete a private location. |
| GET | api/tags | read | tags | Search tags. |
| POST | api/tags | write | tags | Create a tag. |
| GET | api/tags/{id} | read | tags | Get a tag. |
| PUT | api/tags/{id} | write | tags | Upsert a tag. |
| DELETE | api/tags/{id} | write | tags | Delete a tag. |
| GET | api/task_manager/_health | read | task_manager | Get the task manager health. |
| GET | api/timeline | read | timeline | Get Timeline or Timeline template details. |
| POST | api/timeline | write | timeline | Create a Timeline or Timeline template. |
| PATCH | api/timeline | write | timeline | Update a Timeline. |
| DELETE | api/timeline | write | timeline | Delete Timelines or Timeline templates. |
| POST | api/timeline/_copy | write | timeline | Copies timeline or timeline template. |
| GET | api/timeline/_draft | read | timeline | Get draft Timeline or Timeline template details. |
| POST | api/timeline/_draft | write | timeline | Create a clean draft Timeline or Timeline template. |
| POST | api/timeline/_export | read | timeline | Export Timelines. |
| PATCH | api/timeline/_favorite | write | timeline | Favorite a Timeline or Timeline template. |
| POST | api/timeline/_import | write | timeline | Import Timelines. |
| POST | api/timeline/_prepackaged | write | timeline | Install prepackaged Timelines. |
| GET | api/timeline/resolve | read | timeline | Resolve a Timeline or Timeline template. |
| GET | api/timelines | read | timelines | Get Timelines or Timeline templates. |
| GET | api/upgrade_assistant/status | read | upgrade_assistant | Get the upgrade readiness status. |
| GET | api/uptime/settings | read | uptime | Get uptime settings. |
| PUT | api/uptime/settings | write | uptime | Update uptime settings. |
| GET | api/vega | read | vega | List Vega library items. |
| POST | api/vega | write | vega | Create a Vega library item. |
| GET | api/vega/{id} | read | vega | Get a Vega library item. |
| PUT | api/vega/{id} | write | vega | Upsert a Vega library item. |
| DELETE | api/vega/{id} | write | vega | Delete a Vega library item. |
| GET | api/visualizations | read | visualizations | Search visualizations. |
| POST | api/visualizations | write | visualizations | Create visualization. |
| GET | api/visualizations/{id} | read | visualizations | Get visualization. |
| PUT | api/visualizations/{id} | write | visualizations | Upsert visualization. |
| DELETE | api/visualizations/{id} | write | visualizations | Delete visualization. |
| GET | api/workflows | read | workflows | Get workflows. |
| POST | api/workflows | write | workflows | Bulk create workflows. |
| DELETE | api/workflows | write | workflows | Bulk delete workflows. |
| GET | api/workflows/aggs | read | workflows | Get workflow aggregations. |
| GET | api/workflows/connectors | read | workflows | Get available connectors. |
| GET | api/workflows/executions/{id} | read | workflows | Get a workflow execution. |
| POST | api/workflows/executions/{id}/cancel | write | workflows | Cancel a workflow execution. |
| GET | api/workflows/executions/{id}/children | read | workflows | Get child executions. |
| GET | api/workflows/executions/{id}/logs | read | workflows | Get execution logs. |
| POST | api/workflows/executions/{id}/resume | write | workflows | Resume a workflow execution. |
| GET | api/workflows/executions/{id}/step/{id} | read | workflows | Get a step execution. |
| GET | api/workflows/executions/{id}/steps | read | workflows | Get execution step executions. |
| GET | api/workflows/executions/{id}/steps/{id}/resume/external | write | workflows | Resume a workflow execution from an external link. Kept out of read: resumes a paused workflow step. |
| POST | api/workflows/executions/{id}/steps/{id}/resume/external | write | workflows | Submit external input for a paused workflow execution. |
| GET | api/workflows/executions/{id}/steps/{id}/resume/external/form | write | workflows | Get the external input form for a paused workflow execution. Kept out of read: resumes a paused workflow step. |
| POST | api/workflows/export | read | workflows | Export workflows. |
| PUT | api/workflows/managed/workflow/{id} | write | workflows | Update a managed workflow. |
| POST | api/workflows/mget | read | workflows | Get workflows by IDs. |
| GET | api/workflows/schema | read | workflows | Get workflow JSON schema. |
| GET | api/workflows/stats | read | workflows | Get workflow statistics. |
| POST | api/workflows/step/test | write | workflows | Test a workflow step. |
| POST | api/workflows/test | write | workflows | Test a workflow. |
| POST | api/workflows/workflow | write | workflows | Create a workflow. |
| GET | api/workflows/workflow/executions | read | workflows | Search workflow executions. |
| GET | api/workflows/workflow/{id} | read | workflows | Get a workflow. |
| PUT | api/workflows/workflow/{id} | write | workflows | Update a workflow. |
| DELETE | api/workflows/workflow/{id} | write | workflows | Delete a workflow. |
| POST | api/workflows/workflow/{id}/clone | write | workflows | Clone a workflow. |
| GET | api/workflows/workflow/{id}/executions | read | workflows | Get workflow executions. |
| POST | api/workflows/workflow/{id}/executions/cancel | write | workflows | Cancel all active workflow executions. |
| GET | api/workflows/workflow/{id}/executions/steps | read | workflows | Get workflow step executions. |
| POST | api/workflows/workflow/{id}/run | write | workflows | Run a workflow. |
