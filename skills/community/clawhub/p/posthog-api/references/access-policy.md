# PostHog access policy

An access policy limits which endpoints PostHog connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/posthog#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for PostHog: its 451 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create posthog --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/projects/{id}/actions"},
    {"method": "GET", "path": "api/projects/{id}/actions/{id}"},
    {"method": "GET", "path": "api/projects/{id}/actions/{id}/references"},
    {"method": "GET", "path": "api/projects/{id}/activity_log"},
    {"method": "GET", "path": "api/projects/{id}/advanced_activity_logs"},
    {"method": "GET", "path": "api/projects/{id}/advanced_activity_logs/available_filters"},
    {"method": "GET", "path": "api/projects/{id}/alerts"},
    {"method": "GET", "path": "api/projects/{id}/alerts/pagerduty_availability"},
    {"method": "GET", "path": "api/projects/{id}/alerts/{id}"},
    {"method": "GET", "path": "api/projects/{id}/alerts/{id}/destinations"},
    {"method": "GET", "path": "api/projects/{id}/annotations"},
    {"method": "GET", "path": "api/projects/{id}/annotations/{id}"},
    {"method": "GET", "path": "api/projects/{id}/approval_policies"},
    {"method": "GET", "path": "api/projects/{id}/approval_policies/{id}"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/test"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}/backfills"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}/backfills/{id}"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}/logs"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}/runs"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}/runs/{id}"},
    {"method": "GET", "path": "api/projects/{id}/batch_exports/{id}/runs/{id}/logs"},
    {"method": "GET", "path": "api/billing"},
    {"method": "GET", "path": "api/billing/coupons/overview"},
    {"method": "GET", "path": "api/billing/credits/overview"},
    {"method": "GET", "path": "api/billing/get_invoices"},
    {"method": "GET", "path": "api/billing/period"},
    {"method": "GET", "path": "api/billing/portal"},
    {"method": "GET", "path": "api/billing/spend"},
    {"method": "GET", "path": "api/billing/spend/export"},
    {"method": "GET", "path": "api/billing/usage"},
    {"method": "GET", "path": "api/billing/usage/export"},
    {"method": "GET", "path": "api/billing/usage/team_options"},
    {"method": "GET", "path": "api/projects/{id}/change_requests"},
    {"method": "GET", "path": "api/projects/{id}/change_requests/{id}"},
    {"method": "GET", "path": "api/projects/{id}/cohorts"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/activity"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/{id}"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/{id}/blocking_workflows"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/{id}/calculation_history"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/{id}/persons"},
    {"method": "GET", "path": "api/projects/{id}/cohorts/{id}/used_in"},
    {"method": "GET", "path": "api/projects/{id}/comments"},
    {"method": "GET", "path": "api/projects/{id}/comments/count"},
    {"method": "GET", "path": "api/projects/{id}/comments/{id}"},
    {"method": "GET", "path": "api/projects/{id}/comments/{id}/thread"},
    {"method": "GET", "path": "api/projects/{id}/customer_journeys"},
    {"method": "GET", "path": "api/projects/{id}/customer_journeys/{id}"},
    {"method": "GET", "path": "api/projects/{id}/dashboard_templates"},
    {"method": "GET", "path": "api/projects/{id}/dashboard_templates/json_schema"},
    {"method": "GET", "path": "api/projects/{id}/dashboard_templates/{id}"},
    {"method": "GET", "path": "api/projects/{id}/dashboards"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/widget_catalog"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}/activity_summary"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}/cached_tiles"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}/run_insights"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}/run_widgets"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}/stream_query_results"},
    {"method": "GET", "path": "api/projects/{id}/dashboards/{id}/stream_tiles"},
    {"method": "GET", "path": "api/projects/{id}/data_color_themes"},
    {"method": "GET", "path": "api/projects/{id}/data_color_themes/{id}"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/check-database-name"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/check-schema-name"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/completed_activity"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/data_health_issues"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/data_ops_dashboard"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/data_quality_gate"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/job_stats"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/managed-warehouse-data-status"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/managed-warehouse-monitoring"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/managed-warehouse-monitoring-timeseries"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/managed-warehouse-source-schemas"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/managed-warehouse-trino-monitoring"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/managed-warehouse-trino-monitoring-timeseries"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/property_values"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/running_activity"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/total_rows_stats"},
    {"method": "GET", "path": "api/projects/{id}/data_warehouse/warehouse_status"},
    {"method": "GET", "path": "api/projects/{id}/dataset_items"},
    {"method": "GET", "path": "api/projects/{id}/dataset_items/{id}"},
    {"method": "GET", "path": "api/projects/{id}/dataset_items/{id}/versions"},
    {"method": "GET", "path": "api/projects/{id}/datasets"},
    {"method": "GET", "path": "api/projects/{id}/datasets/retention"},
    {"method": "GET", "path": "api/projects/{id}/datasets/{id}"},
    {"method": "GET", "path": "api/projects/{id}/datasets/{id}/exports/{id}"},
    {"method": "GET", "path": "api/projects/{id}/datasets/{id}/exports/{id}/content"},
    {"method": "GET", "path": "api/projects/{id}/datasets/{id}/revisions"},
    {"method": "GET", "path": "api/projects/{id}/early_access_feature"},
    {"method": "GET", "path": "api/projects/{id}/early_access_feature/{id}"},
    {"method": "GET", "path": "api/projects/{id}/elements"},
    {"method": "GET", "path": "api/projects/{id}/elements/stats"},
    {"method": "GET", "path": "api/projects/{id}/elements/values"},
    {"method": "GET", "path": "api/projects/{id}/elements/{id}"},
    {"method": "GET", "path": "api/projects/{id}/endpoints"},
    {"method": "GET", "path": "api/projects/{id}/endpoints/{id}"},
    {"method": "GET", "path": "api/projects/{id}/endpoints/{id}/logs"},
    {"method": "GET", "path": "api/projects/{id}/endpoints/{id}/materialization_status"},
    {"method": "GET", "path": "api/projects/{id}/endpoints/{id}/openapi.json"},
    {"method": "GET", "path": "api/projects/{id}/endpoints/{id}/versions"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/alerts"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/alerts/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/assignment_rules"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/assignment_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/built_in_filters"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/bypass_rules"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/bypass_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/external_references"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/external_references/search_issues"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/external_references/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/fingerprints"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/fingerprints/resolve"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/fingerprints/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/git-provider-file-links/resolve_github"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/git-provider-file-links/resolve_gitlab"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/grouping_rules"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/grouping_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/activity"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/exists"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/tag_definitions"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/values"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/issues/{id}/summary"},
    {"method": "POST", "path": "api/projects/{id}/error_tracking/query/issue"},
    {"method": "POST", "path": "api/projects/{id}/error_tracking/query/issue_events"},
    {"method": "POST", "path": "api/projects/{id}/error_tracking/query/issues"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/recommendations"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/recommendations/source_maps_examples"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/releases"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/releases/hash/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/releases/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/settings/retrieve_settings"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/severity_rules"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/severity_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/spike_detection_config"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/spike_events"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/stack_frames"},
    {"method": "POST", "path": "api/projects/{id}/error_tracking/stack_frames/batch_get"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/stack_frames/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/suppression_rules"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/suppression_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/symbol_sets"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/symbol_sets/{id}"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/tag_rules"},
    {"method": "GET", "path": "api/projects/{id}/error_tracking/tag_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/evaluations"},
    {"method": "GET", "path": "api/projects/{id}/evaluations/overview"},
    {"method": "GET", "path": "api/projects/{id}/evaluations/{id}"},
    {"method": "GET", "path": "api/projects/{id}/evaluations/{id}/backfills"},
    {"method": "GET", "path": "api/projects/{id}/evaluations/{id}/backfills/{id}"},
    {"method": "GET", "path": "api/projects/{id}/evaluations/{id}/runs"},
    {"method": "GET", "path": "api/projects/{id}/evaluations/{id}/score_distribution"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/by_name"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/golang"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/primary_properties"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/python"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/typescript"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/{id}"},
    {"method": "GET", "path": "api/projects/{id}/event_definitions/{id}/metrics"},
    {"method": "GET", "path": "api/projects/{id}/event_schemas"},
    {"method": "GET", "path": "api/projects/{id}/events"},
    {"method": "GET", "path": "api/projects/{id}/events/values"},
    {"method": "GET", "path": "api/projects/{id}/events/{id}"},
    {"method": "GET", "path": "api/projects/{id}/experiment_holdouts"},
    {"method": "GET", "path": "api/projects/{id}/experiment_holdouts/{id}"},
    {"method": "GET", "path": "api/projects/{id}/experiment_saved_metrics"},
    {"method": "GET", "path": "api/projects/{id}/experiment_saved_metrics/{id}"},
    {"method": "GET", "path": "api/projects/{id}/experiments"},
    {"method": "POST", "path": "api/projects/{id}/experiments/calculate_running_time"},
    {"method": "GET", "path": "api/projects/{id}/experiments/matching_ids"},
    {"method": "GET", "path": "api/projects/{id}/experiments/prompt_templates"},
    {"method": "GET", "path": "api/projects/{id}/experiments/session_context"},
    {"method": "GET", "path": "api/projects/{id}/experiments/stats"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/flag_cleanup_target"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/flag_cleanup_task"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/health"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/health_inputs"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/in_session_exposure"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/metrics_recalculation/latest"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/metrics_recalculation/{id}"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/running_time_target"},
    {"method": "GET", "path": "api/projects/{id}/experiments/{id}/timeseries_results"},
    {"method": "GET", "path": "api/projects/{id}/exports"},
    {"method": "GET", "path": "api/projects/{id}/exports/{id}"},
    {"method": "GET", "path": "api/projects/{id}/exports/{id}/content"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/activity"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/evaluation_reasons"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/matching_ids"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/my_flags"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/code_analysis"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/code_analysis_target"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/dependent_flags"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/remote_config"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/status"},
    {"method": "GET", "path": "api/projects/{id}/feature_flags/{id}/versions/{id}"},
    {"method": "GET", "path": "api/projects/{id}/file_system"},
    {"method": "GET", "path": "api/projects/{id}/file_system/frequent"},
    {"method": "GET", "path": "api/projects/{id}/file_system/log_view"},
    {"method": "GET", "path": "api/projects/{id}/file_system/search"},
    {"method": "GET", "path": "api/projects/{id}/file_system/unfiled"},
    {"method": "GET", "path": "api/projects/{id}/file_system/{id}"},
    {"method": "GET", "path": "api/projects/{id}/groups"},
    {"method": "GET", "path": "api/projects/{id}/groups/activity"},
    {"method": "GET", "path": "api/projects/{id}/groups/find"},
    {"method": "GET", "path": "api/projects/{id}/groups/property_values"},
    {"method": "GET", "path": "api/projects/{id}/groups/related"},
    {"method": "GET", "path": "api/projects/{id}/groups_types"},
    {"method": "GET", "path": "api/projects/{id}/groups_types/{id}/metrics"},
    {"method": "GET", "path": "api/projects/{id}/groups_types/{id}/metrics/{id}"},
    {"method": "GET", "path": "api/projects/{id}/health_issues"},
    {"method": "GET", "path": "api/projects/{id}/health_issues/summary"},
    {"method": "GET", "path": "api/projects/{id}/health_issues/{id}"},
    {"method": "GET", "path": "api/projects/{id}/heatmap_screenshots/{id}/content"},
    {"method": "GET", "path": "api/projects/{id}/heatmaps"},
    {"method": "GET", "path": "api/projects/{id}/heatmaps/events"},
    {"method": "GET", "path": "api/projects/{id}/hog_function_templates"},
    {"method": "GET", "path": "api/projects/{id}/hog_function_templates/{id}"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/icon"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/icons"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/masked_secrets"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/{id}/logs"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/{id}/metrics"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/{id}/metrics/totals"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/{id}/revisions"},
    {"method": "GET", "path": "api/projects/{id}/hog_functions/{id}/revisions/{id}"},
    {"method": "GET", "path": "api/projects/{id}/ingestion_warnings_v2"},
    {"method": "GET", "path": "api/projects/{id}/insight_variables"},
    {"method": "GET", "path": "api/projects/{id}/insight_variables/{id}"},
    {"method": "GET", "path": "api/projects/{id}/insights"},
    {"method": "GET", "path": "api/projects/{id}/insights/activity"},
    {"method": "POST", "path": "api/projects/{id}/insights/data_checks"},
    {"method": "GET", "path": "api/projects/{id}/insights/my_last_viewed"},
    {"method": "GET", "path": "api/projects/{id}/insights/trending"},
    {"method": "GET", "path": "api/projects/{id}/insights/{id}"},
    {"method": "GET", "path": "api/projects/{id}/insights/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/insights/{id}/data_checks"},
    {"method": "GET", "path": "api/projects/{id}/insights/{id}/explanations/{id}"},
    {"method": "GET", "path": "api/projects/{id}/insights/{id}/thresholds"},
    {"method": "GET", "path": "api/projects/{id}/insights/{id}/thresholds/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/clustering_config"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/clustering_jobs"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/clustering_jobs/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/evaluation_reports"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/evaluation_reports/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/evaluation_reports/{id}/runs"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/models"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/parser_recipes"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/parser_recipes/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/provider_keys/{id}/dependent_configs"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/provider_keys/{id}/models"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/review_queue_items"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/review_queue_items/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/review_queues"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/review_queues/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/score_definitions"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/score_definitions/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/score_definitions/{id}/versions"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/score_definitions/{id}/versions/{id}"},
    {"method": "POST", "path": "api/projects/{id}/llm_analytics/summarization/batch_check"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/trace_reviews"},
    {"method": "GET", "path": "api/projects/{id}/llm_analytics/trace_reviews/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_prompts"},
    {"method": "GET", "path": "api/projects/{id}/llm_prompts/name/{id}"},
    {"method": "GET", "path": "api/projects/{id}/llm_prompts/resolve/name/{id}"},
    {"method": "GET", "path": "api/projects/{id}/logs/alerts"},
    {"method": "GET", "path": "api/projects/{id}/logs/alerts/{id}"},
    {"method": "GET", "path": "api/projects/{id}/logs/alerts/{id}/destinations/sends"},
    {"method": "GET", "path": "api/projects/{id}/logs/alerts/{id}/events"},
    {"method": "GET", "path": "api/projects/{id}/logs/attributes"},
    {"method": "POST", "path": "api/projects/{id}/logs/facet_values"},
    {"method": "GET", "path": "api/projects/{id}/logs/has_logs"},
    {"method": "GET", "path": "api/projects/{id}/logs/metric_rules"},
    {"method": "GET", "path": "api/projects/{id}/logs/metric_rules/{id}"},
    {"method": "POST", "path": "api/projects/{id}/logs/natural_language_query"},
    {"method": "POST", "path": "api/projects/{id}/logs/query"},
    {"method": "GET", "path": "api/projects/{id}/logs/retention_rules"},
    {"method": "GET", "path": "api/projects/{id}/logs/retention_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/logs/sampling_rules"},
    {"method": "GET", "path": "api/projects/{id}/logs/sampling_rules/{id}"},
    {"method": "GET", "path": "api/projects/{id}/logs/values"},
    {"method": "GET", "path": "api/projects/{id}/logs/views"},
    {"method": "GET", "path": "api/projects/{id}/logs/views/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/activity"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/kernel/compute_options"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/recording_comments"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/collab/stream"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/kernel/status"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/runs/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/sql_v2/runs/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/sql_v2/state"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/widget_snapshots/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/widget_snapshots/{id}/frames/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/widgets/{id}/frames/{id}"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/widgets/{id}/source"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/widgets/{id}/status"},
    {"method": "GET", "path": "api/projects/{id}/notebooks/{id}/widgets/{id}/versions"},
    {"method": "GET", "path": "api/organizations"},
    {"method": "GET", "path": "api/organizations/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/advanced_activity_logs"},
    {"method": "GET", "path": "api/organizations/{id}/advanced_activity_logs/available_filters"},
    {"method": "GET", "path": "api/organizations/{id}/billing/features"},
    {"method": "GET", "path": "api/organizations/{id}/billing/forecast"},
    {"method": "GET", "path": "api/organizations/{id}/billing/invoices"},
    {"method": "GET", "path": "api/organizations/{id}/billing/invoices/{id}/content"},
    {"method": "GET", "path": "api/organizations/{id}/billing/limits"},
    {"method": "GET", "path": "api/organizations/{id}/billing/products"},
    {"method": "GET", "path": "api/organizations/{id}/billing/products/summary"},
    {"method": "GET", "path": "api/organizations/{id}/billing/products/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/billing/projects"},
    {"method": "GET", "path": "api/organizations/{id}/billing/spend"},
    {"method": "GET", "path": "api/organizations/{id}/billing/spend/export"},
    {"method": "GET", "path": "api/organizations/{id}/billing/spend/timeseries"},
    {"method": "GET", "path": "api/organizations/{id}/billing/subscription"},
    {"method": "GET", "path": "api/organizations/{id}/billing/usage"},
    {"method": "GET", "path": "api/organizations/{id}/billing/usage/export"},
    {"method": "GET", "path": "api/organizations/{id}/billing/usage/status"},
    {"method": "GET", "path": "api/organizations/{id}/billing/usage/timeseries"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/channel-pages/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/dreams"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/dreams/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/export"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/pages"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/proposals"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/status"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/tree"},
    {"method": "GET", "path": "api/organizations/{id}/context_layer/wiki/report"},
    {"method": "GET", "path": "api/organizations/{id}/domains"},
    {"method": "GET", "path": "api/organizations/{id}/domains/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/domains/{id}/scim/logs"},
    {"method": "GET", "path": "api/organizations/{id}/invites"},
    {"method": "GET", "path": "api/organizations/{id}/members"},
    {"method": "GET", "path": "api/organizations/{id}/members/project_access"},
    {"method": "GET", "path": "api/organizations/{id}/members/{id}/github_login"},
    {"method": "GET", "path": "api/organizations/{id}/members/{id}/offboarding_preview"},
    {"method": "GET", "path": "api/organizations/{id}/projects"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_default_objects"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_default_properties"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_defaults"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_management"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_member_objects"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_member_properties"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_members"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_role_objects"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_role_properties"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/access_control_roles"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/activity"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/default_evaluation_contexts"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/default_release_conditions"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/event_ingestion_restrictions"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/experiments_config"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/is_generating_demo_data"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/logs_config"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/settings_as_of"},
    {"method": "GET", "path": "api/organizations/{id}/projects/{id}/tracing_config"},
    {"method": "GET", "path": "api/organizations/{id}/roles"},
    {"method": "GET", "path": "api/organizations/{id}/roles/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/roles/{id}/role_memberships"},
    {"method": "GET", "path": "api/organizations/{id}/roles/{id}/role_memberships/{id}"},
    {"method": "GET", "path": "api/organizations/{id}/teams/data_freshness"},
    {"method": "GET", "path": "api/projects/{id}/persons"},
    {"method": "GET", "path": "api/projects/{id}/persons/activity"},
    {"method": "GET", "path": "api/projects/{id}/persons/cohorts"},
    {"method": "GET", "path": "api/projects/{id}/persons/deletion_status"},
    {"method": "GET", "path": "api/projects/{id}/persons/properties_at_time"},
    {"method": "GET", "path": "api/projects/{id}/persons/values"},
    {"method": "GET", "path": "api/projects/{id}/persons/{id}"},
    {"method": "GET", "path": "api/projects/{id}/persons/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/persons/{id}/emails"},
    {"method": "GET", "path": "api/projects/{id}/persons/{id}/push_notifications"},
    {"method": "GET", "path": "api/projects/{id}/plugin_configs/{id}/logs"},
    {"method": "GET", "path": "api/projects/{id}/product_tours"},
    {"method": "GET", "path": "api/projects/{id}/product_tours/{id}"},
    {"method": "GET", "path": "api/projects/{id}/product_tours/{id}/draft_status"},
    {"method": "GET", "path": "api/projects/{id}/property_definitions"},
    {"method": "GET", "path": "api/projects/{id}/property_definitions/seen_together"},
    {"method": "GET", "path": "api/projects/{id}/property_definitions/{id}"},
    {"method": "POST", "path": "api/projects/{id}/query"},
    {"method": "GET", "path": "api/projects/{id}/query/draft_sql"},
    {"method": "GET", "path": "api/projects/{id}/query/scan/{id}"},
    {"method": "POST", "path": "api/projects/{id}/query/upgrade"},
    {"method": "GET", "path": "api/projects/{id}/query/{id}"},
    {"method": "GET", "path": "api/projects/{id}/query/{id}/log"},
    {"method": "GET", "path": "api/projects/{id}/quota_limits"},
    {"method": "GET", "path": "api/projects/{id}/releases"},
    {"method": "GET", "path": "api/projects/{id}/releases/broadcast_search"},
    {"method": "GET", "path": "api/projects/{id}/releases/catalog_flags"},
    {"method": "GET", "path": "api/projects/{id}/releases/catalog_releases"},
    {"method": "GET", "path": "api/projects/{id}/releases/flag_suggestions"},
    {"method": "GET", "path": "api/projects/{id}/releases/{id}"},
    {"method": "GET", "path": "api/projects/{id}/saved"},
    {"method": "GET", "path": "api/projects/{id}/saved/{id}"},
    {"method": "GET", "path": "api/projects/{id}/saved/{id}/screenshot_history"},
    {"method": "GET", "path": "api/projects/{id}/saved/{id}/screenshot_history/requests/{id}"},
    {"method": "GET", "path": "api/projects/{id}/saved/{id}/screenshot_history/{id}/content"},
    {"method": "GET", "path": "api/projects/{id}/scheduled_changes"},
    {"method": "GET", "path": "api/projects/{id}/scheduled_changes/{id}"},
    {"method": "GET", "path": "api/projects/{id}/schema_property_groups"},
    {"method": "GET", "path": "api/projects/{id}/schema_property_groups/{id}"},
    {"method": "GET", "path": "api/projects/{id}/sdk_health/report"},
    {"method": "GET", "path": "api/projects/{id}/session_recording_playlists"},
    {"method": "GET", "path": "api/projects/{id}/session_recording_playlists/{id}"},
    {"method": "GET", "path": "api/projects/{id}/session_recording_playlists/{id}/recordings"},
    {"method": "GET", "path": "api/projects/{id}/session_recordings"},
    {"method": "GET", "path": "api/projects/{id}/session_recordings/{id}"},
    {"method": "GET", "path": "api/projects/{id}/session_recordings/{id}/console_logs"},
    {"method": "GET", "path": "api/projects/{id}/sessions/property_definitions"},
    {"method": "GET", "path": "api/projects/{id}/sessions/values"},
    {"method": "GET", "path": "api/projects/{id}/subscriptions"},
    {"method": "GET", "path": "api/projects/{id}/subscriptions/summaries"},
    {"method": "GET", "path": "api/projects/{id}/subscriptions/summary_quota"},
    {"method": "GET", "path": "api/projects/{id}/subscriptions/{id}"},
    {"method": "GET", "path": "api/projects/{id}/subscriptions/{id}/deliveries"},
    {"method": "GET", "path": "api/projects/{id}/subscriptions/{id}/deliveries/{id}"},
    {"method": "GET", "path": "api/projects/{id}/surveys"},
    {"method": "GET", "path": "api/projects/{id}/surveys/activity"},
    {"method": "GET", "path": "api/projects/{id}/surveys/question_labels"},
    {"method": "GET", "path": "api/projects/{id}/surveys/responses_count"},
    {"method": "GET", "path": "api/projects/{id}/surveys/stats"},
    {"method": "GET", "path": "api/projects/{id}/surveys/{id}"},
    {"method": "GET", "path": "api/projects/{id}/surveys/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/surveys/{id}/archived-response-uuids"},
    {"method": "GET", "path": "api/projects/{id}/surveys/{id}/responses"},
    {"method": "GET", "path": "api/projects/{id}/surveys/{id}/site_snapshot"},
    {"method": "GET", "path": "api/projects/{id}/surveys/{id}/stats"},
    {"method": "GET", "path": "api/users"},
    {"method": "GET", "path": "api/users/{id}"},
    {"method": "GET", "path": "api/projects/{id}/warehouse_saved_queries"},
    {"method": "GET", "path": "api/projects/{id}/warehouse_saved_queries/{id}"},
    {"method": "GET", "path": "api/projects/{id}/warehouse_saved_queries/{id}/activity"},
    {"method": "GET", "path": "api/projects/{id}/warehouse_saved_queries/{id}/dependencies"},
    {"method": "GET", "path": "api/projects/{id}/warehouse_saved_queries/{id}/run_history"},
    {"method": "GET", "path": "api/projects/{id}/warehouse_tables/{id}/history_table"},
    {"method": "GET", "path": "api/projects/{id}/web_analytics/recap"},
    {"method": "GET", "path": "api/projects/{id}/web_analytics/weekly_digest"},
    {"method": "GET", "path": "api/projects/{id}/web_experiments"},
    {"method": "GET", "path": "api/projects/{id}/web_experiments/{id}"},
    {"method": "GET", "path": "api/projects/{id}/web_vitals"}
  ],
  "deny": []
}
```

## Endpoints

The PostHog endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/projects/{id}/actions | read | actions | actions_list. |
| POST | api/projects/{id}/actions | write | actions | actions_create. |
| POST | api/projects/{id}/actions/bulk_update_tags | write | actions | Bulk update tags on multiple objects. |
| GET | api/projects/{id}/actions/{id} | read | actions | actions_retrieve. |
| PUT | api/projects/{id}/actions/{id} | write | actions | actions_update. |
| PATCH | api/projects/{id}/actions/{id} | write | actions | actions_partial_update. |
| DELETE | api/projects/{id}/actions/{id} | write | actions | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/actions/{id}/references | read | actions | actions_references_list. |
| GET | api/projects/{id}/activity_log | read | activity_log | activity_log_list. |
| GET | api/projects/{id}/advanced_activity_logs | read | advanced_activity_logs | advanced_activity_logs_list. |
| GET | api/projects/{id}/advanced_activity_logs/available_filters | read | advanced_activity_logs | advanced_activity_logs_available_filters_retrieve. |
| POST | api/projects/{id}/advanced_activity_logs/export | write | advanced_activity_logs | advanced_activity_logs_export_create. |
| GET | api/projects/{id}/alerts | read | alerts | alerts_list. |
| POST | api/projects/{id}/alerts | write | alerts | alerts_create. |
| GET | api/projects/{id}/alerts/pagerduty_availability | read | alerts | Whether a new alert with these settings could open PagerDuty incidents once it is created. |
| POST | api/projects/{id}/alerts/simulate | write | alerts | Simulate a detector on an insight's historical data. |
| GET | api/projects/{id}/alerts/{id} | read | alerts | alerts_retrieve. |
| PUT | api/projects/{id}/alerts/{id} | write | alerts | alerts_update. |
| PATCH | api/projects/{id}/alerts/{id} | write | alerts | alerts_partial_update. |
| DELETE | api/projects/{id}/alerts/{id} | write | alerts | alerts_destroy. |
| GET | api/projects/{id}/alerts/{id}/destinations | read | alerts | This alert's notification destinations, one entry per destination, with credential-bearing URL components removed. |
| POST | api/projects/{id}/alerts/{id}/destinations | write | alerts | Send this alert to a Slack channel as well as by email. |
| POST | api/projects/{id}/alerts/{id}/destinations/customize | write | alerts | Make a destination's message editable. |
| POST | api/projects/{id}/alerts/{id}/destinations/delete | write | alerts | Stop sending this alert to a destination. |
| POST | api/projects/{id}/alerts/{id}/destinations/pagerduty | write | alerts | Open a PagerDuty incident when this alert starts firing, and resolve it when the alert stops. |
| POST | api/projects/{id}/alerts/{id}/destinations/reset | write | alerts | Send a customized destination's standard message again. |
| POST | api/projects/{id}/alerts/{id}/destinations/webhook | write | alerts | Send this alert's firings to a Discord or Microsoft Teams channel, or to any webhook. |
| POST | api/projects/{id}/alerts/{id}/take_ownership | write | alerts | Take ownership of this alert and enable it. |
| POST | api/projects/{id}/alerts/{id}/test-delivery | write | alerts | Send a synthetic test notification to subscribed users and every active destination on this alert. |
| GET | api/projects/{id}/annotations | read | annotations | Create, Read, Update and Delete annotations. |
| POST | api/projects/{id}/annotations | write | annotations | Create, Read, Update and Delete annotations. |
| GET | api/projects/{id}/annotations/{id} | read | annotations | Create, Read, Update and Delete annotations. |
| PUT | api/projects/{id}/annotations/{id} | write | annotations | Create, Read, Update and Delete annotations. |
| PATCH | api/projects/{id}/annotations/{id} | write | annotations | Create, Read, Update and Delete annotations. |
| DELETE | api/projects/{id}/annotations/{id} | write | annotations | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/approval_policies | read | approval_policies | approval_policies_list. |
| POST | api/projects/{id}/approval_policies | write | approval_policies | approval_policies_create. |
| GET | api/projects/{id}/approval_policies/{id} | read | approval_policies | approval_policies_retrieve. |
| PUT | api/projects/{id}/approval_policies/{id} | write | approval_policies | approval_policies_update. |
| PATCH | api/projects/{id}/approval_policies/{id} | write | approval_policies | approval_policies_partial_update. |
| DELETE | api/projects/{id}/approval_policies/{id} | write | approval_policies | approval_policies_destroy. |
| GET | api/projects/{id}/batch_exports | read | batch_exports | batch_exports_list. |
| POST | api/projects/{id}/batch_exports | write | batch_exports | batch_exports_create. |
| POST | api/projects/{id}/batch_exports/run_test_step_new | write | batch_exports | batch_exports_run_test_step_new_create. |
| GET | api/projects/{id}/batch_exports/test | read | batch_exports | batch_exports_test_retrieve. |
| GET | api/projects/{id}/batch_exports/{id} | read | batch_exports | batch_exports_retrieve. |
| PUT | api/projects/{id}/batch_exports/{id} | write | batch_exports | batch_exports_update. |
| PATCH | api/projects/{id}/batch_exports/{id} | write | batch_exports | batch_exports_partial_update. |
| DELETE | api/projects/{id}/batch_exports/{id} | write | batch_exports | batch_exports_destroy. |
| GET | api/projects/{id}/batch_exports/{id}/backfills | read | batch_exports | ViewSet for BatchExportBackfill models. |
| POST | api/projects/{id}/batch_exports/{id}/backfills | write | batch_exports | Create a new backfill for a BatchExport. |
| GET | api/projects/{id}/batch_exports/{id}/backfills/{id} | read | batch_exports | ViewSet for BatchExportBackfill models. |
| POST | api/projects/{id}/batch_exports/{id}/backfills/{id}/cancel | write | batch_exports | Cancel a batch export backfill. |
| GET | api/projects/{id}/batch_exports/{id}/logs | read | batch_exports | batch_exports_logs_retrieve. |
| POST | api/projects/{id}/batch_exports/{id}/pause | write | batch_exports | Pause a BatchExport. |
| POST | api/projects/{id}/batch_exports/{id}/run_test_step | write | batch_exports | batch_exports_run_test_step_create. |
| GET | api/projects/{id}/batch_exports/{id}/runs | read | batch_exports | batch_exports_runs_list. |
| GET | api/projects/{id}/batch_exports/{id}/runs/{id} | read | batch_exports | batch_exports_runs_retrieve. |
| POST | api/projects/{id}/batch_exports/{id}/runs/{id}/cancel | write | batch_exports | Cancel a batch export run. |
| GET | api/projects/{id}/batch_exports/{id}/runs/{id}/logs | read | batch_exports | batch_exports_runs_logs_retrieve. |
| POST | api/projects/{id}/batch_exports/{id}/runs/{id}/retry | write | batch_exports | Retry a batch export run. |
| POST | api/projects/{id}/batch_exports/{id}/unpause | write | batch_exports | Unpause a BatchExport. |
| GET | api/billing | read | billing | billing_list. |
| POST | api/billing/activate | write | billing | billing_activate_create. |
| POST | api/billing/activate/authorize | write | billing | billing_activate_authorize_create. |
| POST | api/billing/activate/authorize/status | write | billing | billing_activate_authorize_status_create. |
| POST | api/billing/coupons/claim | write | billing | billing_coupons_claim_create. |
| GET | api/billing/coupons/overview | read | billing | billing_coupons_overview_retrieve. |
| GET | api/billing/credits/overview | read | billing | billing_credits_overview_retrieve. |
| POST | api/billing/credits/purchase | write | billing | billing_credits_purchase_create. |
| POST | api/billing/deactivate | write | billing | billing_deactivate_create. |
| GET | api/billing/get_invoices | read | billing | billing_get_invoices_retrieve. |
| PATCH | api/billing/license | write | billing | billing_license_partial_update. |
| GET | api/billing/period | read | billing | Get the current organization billing period. |
| GET | api/billing/portal | read | billing | billing_portal_retrieve. |
| GET | api/billing/spend | read | billing | Endpoint to fetch spend data (proxy to billing service). |
| GET | api/billing/spend/export | read | billing | Download the spend breakdown as CSV, honouring the requested project cap. |
| POST | api/billing/startups/apply | write | billing | billing_startups_apply_create. |
| POST | api/billing/subscription/switch-plan | write | billing | billing_subscription_switch_plan_create. |
| POST | api/billing/trials/activate | write | billing | billing_trials_activate_create. |
| POST | api/billing/trials/cancel | write | billing | billing_trials_cancel_create. |
| GET | api/billing/usage | read | billing | billing_usage_retrieve. |
| GET | api/billing/usage/export | read | billing | Download the usage breakdown as CSV, honouring the requested project cap. |
| GET | api/billing/usage/team_options | read | billing | The project ids the project filter offers, loaded apart from the charts. |
| GET | api/projects/{id}/change_requests | read | change_requests | change_requests_list. |
| GET | api/projects/{id}/change_requests/{id} | read | change_requests | change_requests_retrieve. |
| POST | api/projects/{id}/change_requests/{id}/approve | write | change_requests | Approve a change request. |
| POST | api/projects/{id}/change_requests/{id}/cancel | write | change_requests | Cancel a change request. |
| POST | api/projects/{id}/change_requests/{id}/reject | write | change_requests | Reject a change request. |
| GET | api/projects/{id}/cohorts | read | cohorts | cohorts_list. |
| POST | api/projects/{id}/cohorts | write | cohorts | cohorts_create. |
| GET | api/projects/{id}/cohorts/activity | read | cohorts | cohorts_all_activity_retrieve. |
| GET | api/projects/{id}/cohorts/{id} | read | cohorts | cohorts_retrieve. |
| PUT | api/projects/{id}/cohorts/{id} | write | cohorts | cohorts_update. |
| PATCH | api/projects/{id}/cohorts/{id} | write | cohorts | cohorts_partial_update. |
| DELETE | api/projects/{id}/cohorts/{id} | write | cohorts | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/cohorts/{id}/activity | read | cohorts | cohorts_activity_retrieve. |
| PATCH | api/projects/{id}/cohorts/{id}/add_persons_to_static_cohort | write | cohorts | cohorts_add_persons_to_static_cohort_partial_update. |
| GET | api/projects/{id}/cohorts/{id}/blocking_workflows | read | cohorts | Active workflows that block deleting this cohort or editing it so it stops updating in real time. |
| GET | api/projects/{id}/cohorts/{id}/calculation_history | read | cohorts | cohorts_calculation_history_retrieve. |
| GET | api/projects/{id}/cohorts/{id}/persons | read | cohorts | cohorts_persons_retrieve. |
| POST | api/projects/{id}/cohorts/{id}/realtime | write | cohorts | Turn realtime on or off for a cohort. |
| PATCH | api/projects/{id}/cohorts/{id}/remove_person_from_static_cohort | write | cohorts | cohorts_remove_person_from_static_cohort_partial_update. |
| GET | api/projects/{id}/cohorts/{id}/used_in | read | cohorts | cohorts_used_in_retrieve. |
| GET | api/projects/{id}/comments | read | comments | comments_list. |
| POST | api/projects/{id}/comments | write | comments | Create a comment. |
| GET | api/projects/{id}/comments/count | read | comments | comments_count_retrieve. |
| GET | api/projects/{id}/comments/{id} | read | comments | comments_retrieve. |
| PUT | api/projects/{id}/comments/{id} | write | comments | comments_update. |
| PATCH | api/projects/{id}/comments/{id} | write | comments | comments_partial_update. |
| DELETE | api/projects/{id}/comments/{id} | write | comments | Hard delete of this model is not allowed. |
| POST | api/projects/{id}/comments/{id}/complete | write | comments | Mark a task-comment as complete. |
| POST | api/projects/{id}/comments/{id}/reopen | write | comments | Reopen a completed task-comment. |
| POST | api/projects/{id}/comments/{id}/send_to_slack | write | comments | Mirror this discussion thread to a Slack channel. |
| GET | api/projects/{id}/comments/{id}/thread | read | comments | comments_thread_retrieve. |
| GET | api/projects/{id}/customer_journeys | read | customer_journeys | customer_journeys_list. |
| POST | api/projects/{id}/customer_journeys | write | customer_journeys | customer_journeys_create. |
| GET | api/projects/{id}/customer_journeys/{id} | read | customer_journeys | customer_journeys_retrieve. |
| PUT | api/projects/{id}/customer_journeys/{id} | write | customer_journeys | customer_journeys_update. |
| PATCH | api/projects/{id}/customer_journeys/{id} | write | customer_journeys | customer_journeys_partial_update. |
| DELETE | api/projects/{id}/customer_journeys/{id} | write | customer_journeys | customer_journeys_destroy. |
| GET | api/projects/{id}/dashboard_templates | read | dashboard_templates | dashboard_templates_list. |
| POST | api/projects/{id}/dashboard_templates | write | dashboard_templates | dashboard_templates_create. |
| POST | api/projects/{id}/dashboard_templates/copy_between_projects | write | dashboard_templates | Copy a team template to this project. |
| GET | api/projects/{id}/dashboard_templates/json_schema | read | dashboard_templates | dashboard_templates_json_schema_retrieve. |
| GET | api/projects/{id}/dashboard_templates/{id} | read | dashboard_templates | dashboard_templates_retrieve. |
| PUT | api/projects/{id}/dashboard_templates/{id} | write | dashboard_templates | dashboard_templates_update. |
| PATCH | api/projects/{id}/dashboard_templates/{id} | write | dashboard_templates | dashboard_templates_partial_update. |
| DELETE | api/projects/{id}/dashboard_templates/{id} | write | dashboard_templates | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/dashboards | read | dashboards | dashboards_list. |
| POST | api/projects/{id}/dashboards | write | dashboards | dashboards_create. |
| POST | api/projects/{id}/dashboards/bulk_delete | write | dashboards | Soft-delete up to 100 dashboards. |
| POST | api/projects/{id}/dashboards/bulk_update_tags | write | dashboards | Bulk update tags on multiple objects. |
| POST | api/projects/{id}/dashboards/create_from_template_json | write | dashboards | dashboards_create_from_template_json_create. |
| POST | api/projects/{id}/dashboards/create_unlisted_dashboard | write | dashboards | Creates an unlisted dashboard from template by tag. |
| GET | api/projects/{id}/dashboards/widget_catalog | read | dashboards | List registered dashboard widget types and per-type config_schema documentation for agents. |
| GET | api/projects/{id}/dashboards/{id} | read | dashboards | dashboards_retrieve. |
| PUT | api/projects/{id}/dashboards/{id} | write | dashboards | dashboards_update. |
| PATCH | api/projects/{id}/dashboards/{id} | write | dashboards | dashboards_partial_update. |
| DELETE | api/projects/{id}/dashboards/{id} | write | dashboards | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/dashboards/{id}/activity_summary | read | dashboards | Signals for judging whether a dashboard is still in use: its last logged change and recent human views in the app. |
| POST | api/projects/{id}/dashboards/{id}/add_insight | write | dashboards | Place an existing insight on this dashboard as a new tile. |
| GET | api/projects/{id}/dashboards/{id}/cached_tiles | read | dashboards | Read the cached results of several insight tiles in one request. |
| POST | api/projects/{id}/dashboards/{id}/copy_group | write | dashboards | Copy a group of tiles and its settings to another dashboard. |
| POST | api/projects/{id}/dashboards/{id}/copy_tile | write | dashboards | Copy an existing dashboard tile to another dashboard (insight, text card, or widget tile). |
| POST | api/projects/{id}/dashboards/{id}/create_text_tile | write | dashboards | Add a markdown text tile to a dashboard. |
| POST | api/projects/{id}/dashboards/{id}/delete_tile | write | dashboards | Soft-delete a single tile from a dashboard. |
| POST | api/projects/{id}/dashboards/{id}/move_tile | write | dashboards | dashboards_move_tile_create. |
| PATCH | api/projects/{id}/dashboards/{id}/move_tile | write | dashboards | dashboards_move_tile_partial_update. |
| POST | api/projects/{id}/dashboards/{id}/reorder_tiles | write | dashboards | dashboards_reorder_tiles_create. |
| GET | api/projects/{id}/dashboards/{id}/run_insights | read | dashboards | Run all insights on a dashboard and return their results. |
| GET | api/projects/{id}/dashboards/{id}/run_widgets | read | dashboards | dashboards_run_widgets_retrieve. |
| GET | api/projects/{id}/dashboards/{id}/sharing | write | dashboards | dashboards_sharing_list. Kept out of read: returns share access tokens. |
| POST | api/projects/{id}/dashboards/{id}/sharing/passwords | write | dashboards | Create a new password for the sharing configuration. |
| DELETE | api/projects/{id}/dashboards/{id}/sharing/passwords/{id} | write | dashboards | Delete a password from the sharing configuration. |
| POST | api/projects/{id}/dashboards/{id}/sharing/refresh | write | dashboards | dashboards_sharing_refresh_create. |
| GET | api/projects/{id}/dashboards/{id}/stream_query_results | read | dashboards | Experimentally refresh insight tiles. |
| GET | api/projects/{id}/dashboards/{id}/stream_tiles | read | dashboards | Stream dashboard metadata and tiles via Server-Sent Events. |
| POST | api/projects/{id}/dashboards/{id}/subscribe_nudge | write | dashboards | Send the requesting user an in-app notification suggesting they subscribe to this dashboard. |
| POST | api/projects/{id}/dashboards/{id}/update_text_tile | write | dashboards | Update the markdown body, layout, or color of an existing text tile on a dashboard. |
| POST | api/projects/{id}/dashboards/{id}/widgets/batch | write | dashboards | Add multiple widget tiles to a dashboard in one atomic request. |
| PATCH | api/projects/{id}/dashboards/{id}/widgets/batch_update | write | dashboards | Update the settings of existing widgets in place, atomically — config, name, and description. |
| GET | api/projects/{id}/data_color_themes | read | data_color_themes | data_color_themes_list. |
| POST | api/projects/{id}/data_color_themes | write | data_color_themes | data_color_themes_create. |
| GET | api/projects/{id}/data_color_themes/{id} | read | data_color_themes | data_color_themes_retrieve. |
| PUT | api/projects/{id}/data_color_themes/{id} | write | data_color_themes | data_color_themes_update. |
| PATCH | api/projects/{id}/data_color_themes/{id} | write | data_color_themes | data_color_themes_partial_update. |
| DELETE | api/projects/{id}/data_color_themes/{id} | write | data_color_themes | data_color_themes_destroy. |
| GET | api/projects/{id}/data_warehouse/check-database-name | read | data_warehouse | Check if a database name is available. |
| GET | api/projects/{id}/data_warehouse/check-schema-name | read | data_warehouse | Check if a schema name is free within the organization's managed warehouse. |
| GET | api/projects/{id}/data_warehouse/completed_activity | read | data_warehouse | Returns completed/non-running activities (jobs with status 'Completed'). |
| GET | api/projects/{id}/data_warehouse/data_health_issues | read | data_warehouse | Returns failed/disabled data pipeline items for the Pipeline status side panel. |
| GET | api/projects/{id}/data_warehouse/data_ops_dashboard | read | data_warehouse | Returns the data ops overview dashboard ID for this team, creating it if it doesn't exist yet. |
| GET | api/projects/{id}/data_warehouse/data_quality_gate | read | data_warehouse | Read or update the team's data quality gate: whether a materialization whose error-severity checks fail is published. |
| PATCH | api/projects/{id}/data_warehouse/data_quality_gate | write | data_warehouse | Read or update the team's data quality gate: whether a materialization whose error-severity checks fail is published. |
| DELETE | api/projects/{id}/data_warehouse/delete-org | write | data_warehouse | Remove the organization's provisioning record after teardown, freeing its warehouse name. |
| POST | api/projects/{id}/data_warehouse/deprovision | write | data_warehouse | Start deprovisioning the organization's managed warehouse. |
| GET | api/projects/{id}/data_warehouse/hoglake_credentials | write | data_warehouse | List hoglake credentials. Kept out of read: returns warehouse credentials. |
| POST | api/projects/{id}/data_warehouse/hoglake_credentials | write | data_warehouse | Create a hoglake credential. |
| DELETE | api/projects/{id}/data_warehouse/hoglake_credentials/{id} | write | data_warehouse | Revoke a hoglake credential. |
| POST | api/projects/{id}/data_warehouse/hoglake_credentials/{id}/rotate | write | data_warehouse | Rotate a hoglake credential's secret. |
| GET | api/projects/{id}/data_warehouse/job_stats | read | data_warehouse | Returns success and failed job statistics for the last 1, 7, or 30 days. |
| GET | api/projects/{id}/data_warehouse/managed-warehouse-data-status | read | data_warehouse | Get events, persons, and imported source readiness for the managed warehouse. |
| GET | api/projects/{id}/data_warehouse/managed-warehouse-monitoring | read | data_warehouse | Get managed warehouse monitoring snapshot. |
| GET | api/projects/{id}/data_warehouse/managed-warehouse-monitoring-timeseries | read | data_warehouse | Get managed warehouse monitoring time series. |
| GET | api/projects/{id}/data_warehouse/managed-warehouse-source-schemas | read | data_warehouse | Get per-schema detail for one imported source. |
| GET | api/projects/{id}/data_warehouse/managed-warehouse-trino-monitoring | read | data_warehouse | Get managed warehouse Trino monitoring snapshot. |
| GET | api/projects/{id}/data_warehouse/managed-warehouse-trino-monitoring-timeseries | read | data_warehouse | Get managed warehouse Trino monitoring time series. |
| GET | api/projects/{id}/data_warehouse/my_hoglake_credentials | write | data_warehouse | List your hoglake credentials. Kept out of read: returns warehouse credentials. |
| POST | api/projects/{id}/data_warehouse/my_hoglake_credentials | write | data_warehouse | Create a hoglake credential of your own. |
| DELETE | api/projects/{id}/data_warehouse/my_hoglake_credentials/{id} | write | data_warehouse | Revoke one of your hoglake credentials. |
| POST | api/projects/{id}/data_warehouse/my_hoglake_credentials/{id}/rotate | write | data_warehouse | Rotate one of your hoglake credentials. |
| POST | api/projects/{id}/data_warehouse/onboard-team | write | data_warehouse | Onboard this project onto the organization's existing managed warehouse. |
| GET | api/projects/{id}/data_warehouse/property_values | read | data_warehouse | API endpoints for data warehouse aggregate statistics and operations. |
| POST | api/projects/{id}/data_warehouse/provision | write | data_warehouse | Start provisioning a managed warehouse for this organization (shared by all its teams). |
| POST | api/projects/{id}/data_warehouse/reset-password | write | data_warehouse | Reset the root password for the managed warehouse. |
| GET | api/projects/{id}/data_warehouse/running_activity | read | data_warehouse | Returns currently running activities (jobs with status 'Running'). |
| GET | api/projects/{id}/data_warehouse/total_rows_stats | read | data_warehouse | Returns aggregated statistics for the data warehouse total rows processed within the current billing period. |
| GET | api/projects/{id}/data_warehouse/warehouse_status | read | data_warehouse | Get the current provisioning status of the managed warehouse, with this project's onboarding state. |
| GET | api/projects/{id}/dataset_items | read | dataset_items | List a dataset's current items or its exact contents at a prior revision. |
| POST | api/projects/{id}/dataset_items | write | dataset_items | Create an item and its first immutable version. |
| GET | api/projects/{id}/dataset_items/{id} | read | dataset_items | Retrieve the current item version or the version visible at an exact dataset revision. |
| PATCH | api/projects/{id}/dataset_items/{id} | write | dataset_items | Create a new immutable item version from editable fields. |
| POST | api/projects/{id}/dataset_items/{id}/archive | write | dataset_items | Archive an active item by creating a new immutable version. |
| POST | api/projects/{id}/dataset_items/{id}/restore | write | dataset_items | Restore an archived item by copying content into a new immutable version. |
| GET | api/projects/{id}/dataset_items/{id}/versions | read | dataset_items | List every immutable version of an item, newest first. |
| GET | api/projects/{id}/datasets | read | datasets | List active datasets by default, or archived datasets when requested. |
| POST | api/projects/{id}/datasets | write | datasets | Create an empty dataset. |
| GET | api/projects/{id}/datasets/retention | read | datasets | Find accessible datasets and older revisions within seven days of expiry without refreshing their retention. |
| GET | api/projects/{id}/datasets/{id} | read | datasets | Retrieve an active or archived dataset. |
| PATCH | api/projects/{id}/datasets/{id} | write | datasets | Update descriptive dataset fields without changing its revision. |
| POST | api/projects/{id}/datasets/{id}/archive | write | datasets | Archive a dataset. |
| POST | api/projects/{id}/datasets/{id}/exports | write | datasets | Create an asynchronous JSONL export pinned to an immutable dataset revision. |
| GET | api/projects/{id}/datasets/{id}/exports/{id} | read | datasets | Check the status of a dataset export created by the current user. |
| GET | api/projects/{id}/datasets/{id}/exports/{id}/content | read | datasets | Download a completed dataset JSONL export. |
| POST | api/projects/{id}/datasets/{id}/extend_retention | write | datasets | Refresh retention for a dataset and optionally one revision, with the same access required to read them. |
| POST | api/projects/{id}/datasets/{id}/restore | write | datasets | Restore an archived dataset without changing its item states. |
| GET | api/projects/{id}/datasets/{id}/revisions | read | datasets | List immutable dataset revisions, newest first. |
| GET | api/projects/{id}/early_access_feature | read | early_access_feature | early_access_feature_list. |
| POST | api/projects/{id}/early_access_feature | write | early_access_feature | early_access_feature_create. |
| GET | api/projects/{id}/early_access_feature/{id} | read | early_access_feature | early_access_feature_retrieve. |
| PUT | api/projects/{id}/early_access_feature/{id} | write | early_access_feature | early_access_feature_update. |
| PATCH | api/projects/{id}/early_access_feature/{id} | write | early_access_feature | early_access_feature_partial_update. |
| DELETE | api/projects/{id}/early_access_feature/{id} | write | early_access_feature | early_access_feature_destroy. |
| GET | api/projects/{id}/elements | read | elements | elements_list. |
| POST | api/projects/{id}/elements | write | elements | elements_create. |
| GET | api/projects/{id}/elements/stats | read | elements | Counts of $autocapture, $rageclick, and $dead_click events grouped by the element chain they occurred on, ordered by count. |
| GET | api/projects/{id}/elements/values | read | elements | elements_values_list. |
| GET | api/projects/{id}/elements/{id} | read | elements | elements_retrieve. |
| PUT | api/projects/{id}/elements/{id} | write | elements | elements_update. |
| PATCH | api/projects/{id}/elements/{id} | write | elements | elements_partial_update. |
| DELETE | api/projects/{id}/elements/{id} | write | elements | elements_destroy. |
| GET | api/projects/{id}/endpoints | read | endpoints | List all endpoints for the team. |
| POST | api/projects/{id}/endpoints | write | endpoints | Create a new endpoint. |
| POST | api/projects/{id}/endpoints/last_execution_times | write | endpoints | Get the most recent execution time per endpoint (endpoint-level). |
| GET | api/projects/{id}/endpoints/{id} | read | endpoints | Retrieve an endpoint, or a specific version via ?version=N. |
| PUT | api/projects/{id}/endpoints/{id} | write | endpoints | Update an existing endpoint. |
| PATCH | api/projects/{id}/endpoints/{id} | write | endpoints | Update an existing endpoint. |
| DELETE | api/projects/{id}/endpoints/{id} | write | endpoints | Delete an endpoint and clean up materialized query. |
| GET | api/projects/{id}/endpoints/{id}/logs | read | endpoints | endpoints_logs_retrieve. |
| POST | api/projects/{id}/endpoints/{id}/materialization_preview | write | endpoints | Preview the materialization transform for an endpoint. |
| GET | api/projects/{id}/endpoints/{id}/materialization_status | read | endpoints | Get materialization status for an endpoint. |
| GET | api/projects/{id}/endpoints/{id}/openapi.json | read | endpoints | Get OpenAPI 3.0 specification for this endpoint. |
| GET | api/projects/{id}/endpoints/{id}/run | write | endpoints | Execute endpoint with optional materialization. Kept out of read: executes the endpoint (optionally materializes). |
| POST | api/projects/{id}/endpoints/{id}/run | write | endpoints | Execute endpoint with optional materialization. |
| GET | api/projects/{id}/endpoints/{id}/versions | read | endpoints | List all versions for an endpoint. |
| GET | api/projects/{id}/error_tracking/alerts | read | error_tracking | error_tracking_alerts_list. |
| POST | api/projects/{id}/error_tracking/alerts | write | error_tracking | error_tracking_alerts_create. |
| GET | api/projects/{id}/error_tracking/alerts/{id} | read | error_tracking | error_tracking_alerts_retrieve. |
| PUT | api/projects/{id}/error_tracking/alerts/{id} | write | error_tracking | error_tracking_alerts_update. |
| PATCH | api/projects/{id}/error_tracking/alerts/{id} | write | error_tracking | error_tracking_alerts_partial_update. |
| DELETE | api/projects/{id}/error_tracking/alerts/{id} | write | error_tracking | error_tracking_alerts_destroy. |
| GET | api/projects/{id}/error_tracking/assignment_rules | read | error_tracking | error_tracking_assignment_rules_list. |
| POST | api/projects/{id}/error_tracking/assignment_rules | write | error_tracking | error_tracking_assignment_rules_create. |
| PATCH | api/projects/{id}/error_tracking/assignment_rules/reorder | write | error_tracking | error_tracking_assignment_rules_reorder_partial_update. |
| GET | api/projects/{id}/error_tracking/assignment_rules/{id} | read | error_tracking | error_tracking_assignment_rules_retrieve. |
| PUT | api/projects/{id}/error_tracking/assignment_rules/{id} | write | error_tracking | error_tracking_assignment_rules_update. |
| PATCH | api/projects/{id}/error_tracking/assignment_rules/{id} | write | error_tracking | error_tracking_assignment_rules_partial_update. |
| DELETE | api/projects/{id}/error_tracking/assignment_rules/{id} | write | error_tracking | error_tracking_assignment_rules_destroy. |
| GET | api/projects/{id}/error_tracking/built_in_filters | read | error_tracking | error_tracking_built_in_filters_list. |
| PATCH | api/projects/{id}/error_tracking/built_in_filters/{id} | write | error_tracking | error_tracking_built_in_filters_partial_update. |
| GET | api/projects/{id}/error_tracking/bypass_rules | read | error_tracking | error_tracking_bypass_rules_list. |
| POST | api/projects/{id}/error_tracking/bypass_rules | write | error_tracking | error_tracking_bypass_rules_create. |
| PATCH | api/projects/{id}/error_tracking/bypass_rules/reorder | write | error_tracking | error_tracking_bypass_rules_reorder_partial_update. |
| GET | api/projects/{id}/error_tracking/bypass_rules/{id} | read | error_tracking | error_tracking_bypass_rules_retrieve. |
| PUT | api/projects/{id}/error_tracking/bypass_rules/{id} | write | error_tracking | error_tracking_bypass_rules_update. |
| PATCH | api/projects/{id}/error_tracking/bypass_rules/{id} | write | error_tracking | error_tracking_bypass_rules_partial_update. |
| DELETE | api/projects/{id}/error_tracking/bypass_rules/{id} | write | error_tracking | error_tracking_bypass_rules_destroy. |
| GET | api/projects/{id}/error_tracking/external_references | read | error_tracking | error_tracking_external_references_list. |
| POST | api/projects/{id}/error_tracking/external_references | write | error_tracking | error_tracking_external_references_create. |
| POST | api/projects/{id}/error_tracking/external_references/link_issue | write | error_tracking | Link an error to an issue that already exists in the connected provider. |
| GET | api/projects/{id}/error_tracking/external_references/search_issues | read | error_tracking | Search a connected provider for existing issues to link an error to. |
| GET | api/projects/{id}/error_tracking/external_references/{id} | read | error_tracking | error_tracking_external_references_retrieve. |
| DELETE | api/projects/{id}/error_tracking/external_references/{id} | write | error_tracking | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/error_tracking/fingerprints | read | error_tracking | error_tracking_fingerprints_list. |
| GET | api/projects/{id}/error_tracking/fingerprints/resolve | read | error_tracking | error_tracking_fingerprints_resolve_retrieve. |
| GET | api/projects/{id}/error_tracking/fingerprints/{id} | read | error_tracking | error_tracking_fingerprints_retrieve. |
| DELETE | api/projects/{id}/error_tracking/fingerprints/{id} | write | error_tracking | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/error_tracking/git-provider-file-links/resolve_github | read | error_tracking | error_tracking_git_provider_file_links_resolve_github_retrieve. |
| GET | api/projects/{id}/error_tracking/git-provider-file-links/resolve_gitlab | read | error_tracking | error_tracking_git_provider_file_links_resolve_gitlab_retrieve. |
| GET | api/projects/{id}/error_tracking/grouping_rules | read | error_tracking | error_tracking_grouping_rules_list. |
| POST | api/projects/{id}/error_tracking/grouping_rules | write | error_tracking | error_tracking_grouping_rules_create. |
| PATCH | api/projects/{id}/error_tracking/grouping_rules/reorder | write | error_tracking | error_tracking_grouping_rules_reorder_partial_update. |
| GET | api/projects/{id}/error_tracking/grouping_rules/{id} | read | error_tracking | error_tracking_grouping_rules_retrieve. |
| PUT | api/projects/{id}/error_tracking/grouping_rules/{id} | write | error_tracking | error_tracking_grouping_rules_update. |
| PATCH | api/projects/{id}/error_tracking/grouping_rules/{id} | write | error_tracking | error_tracking_grouping_rules_partial_update. |
| DELETE | api/projects/{id}/error_tracking/grouping_rules/{id} | write | error_tracking | error_tracking_grouping_rules_destroy. |
| GET | api/projects/{id}/error_tracking/issues | read | error_tracking | error_tracking_issues_list. |
| GET | api/projects/{id}/error_tracking/issues/activity | read | error_tracking | error_tracking_issues_all_activity_retrieve. |
| POST | api/projects/{id}/error_tracking/issues/bulk | write | error_tracking | error_tracking_issues_bulk_create. |
| GET | api/projects/{id}/error_tracking/issues/exists | read | error_tracking | error_tracking_issues_exists_retrieve. |
| GET | api/projects/{id}/error_tracking/issues/tag_definitions | read | error_tracking | error_tracking_issues_tag_definitions_retrieve. |
| GET | api/projects/{id}/error_tracking/issues/values | read | error_tracking | error_tracking_issues_values_retrieve. |
| GET | api/projects/{id}/error_tracking/issues/{id} | read | error_tracking | error_tracking_issues_retrieve. |
| PUT | api/projects/{id}/error_tracking/issues/{id} | write | error_tracking | error_tracking_issues_update. |
| PATCH | api/projects/{id}/error_tracking/issues/{id} | write | error_tracking | error_tracking_issues_partial_update. |
| DELETE | api/projects/{id}/error_tracking/issues/{id} | write | error_tracking | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/error_tracking/issues/{id}/activity | read | error_tracking | error_tracking_issues_activity_retrieve. |
| PATCH | api/projects/{id}/error_tracking/issues/{id}/assign | write | error_tracking | error_tracking_issues_assign_partial_update. |
| PUT | api/projects/{id}/error_tracking/issues/{id}/cohort | write | error_tracking | error_tracking_issues_cohort_update. |
| POST | api/projects/{id}/error_tracking/issues/{id}/merge | write | error_tracking | error_tracking_issues_merge_create. |
| POST | api/projects/{id}/error_tracking/issues/{id}/split | write | error_tracking | error_tracking_issues_split_create. |
| GET | api/projects/{id}/error_tracking/issues/{id}/summary | read | error_tracking | error_tracking_issues_summary_retrieve. |
| PATCH | api/projects/{id}/error_tracking/issues/{id}/tag | write | error_tracking | error_tracking_issues_tag_partial_update. |
| POST | api/projects/{id}/error_tracking/query/issue | read | error_tracking | Get compact error tracking issue details. |
| POST | api/projects/{id}/error_tracking/query/issue_events | read | error_tracking | List sampled exception events for an error tracking issue. |
| POST | api/projects/{id}/error_tracking/query/issues | read | error_tracking | List compact error tracking issues. |
| GET | api/projects/{id}/error_tracking/recommendations | read | error_tracking | error_tracking_recommendations_list. |
| GET | api/projects/{id}/error_tracking/recommendations/source_maps_examples | read | error_tracking | List frames missing symbols. |
| POST | api/projects/{id}/error_tracking/recommendations/{id}/dismiss | write | error_tracking | error_tracking_recommendations_dismiss_create. |
| POST | api/projects/{id}/error_tracking/recommendations/{id}/refresh | write | error_tracking | error_tracking_recommendations_refresh_create. |
| POST | api/projects/{id}/error_tracking/recommendations/{id}/restore | write | error_tracking | error_tracking_recommendations_restore_create. |
| GET | api/projects/{id}/error_tracking/releases | read | error_tracking | error_tracking_releases_list. |
| POST | api/projects/{id}/error_tracking/releases | write | error_tracking | error_tracking_releases_create. |
| GET | api/projects/{id}/error_tracking/releases/hash/{id} | read | error_tracking | error_tracking_releases_hash_retrieve. |
| GET | api/projects/{id}/error_tracking/releases/{id} | read | error_tracking | error_tracking_releases_retrieve. |
| PUT | api/projects/{id}/error_tracking/releases/{id} | write | error_tracking | error_tracking_releases_update. |
| PATCH | api/projects/{id}/error_tracking/releases/{id} | write | error_tracking | error_tracking_releases_partial_update. |
| DELETE | api/projects/{id}/error_tracking/releases/{id} | write | error_tracking | error_tracking_releases_destroy. |
| GET | api/projects/{id}/error_tracking/settings/retrieve_settings | read | error_tracking | error_tracking_settings_retrieve_settings_retrieve. |
| PATCH | api/projects/{id}/error_tracking/settings/update_settings | write | error_tracking | error_tracking_settings_update_settings_partial_update. |
| GET | api/projects/{id}/error_tracking/severity_rules | read | error_tracking | error_tracking_severity_rules_list. |
| POST | api/projects/{id}/error_tracking/severity_rules | write | error_tracking | error_tracking_severity_rules_create. |
| PATCH | api/projects/{id}/error_tracking/severity_rules/reorder | write | error_tracking | error_tracking_severity_rules_reorder_partial_update. |
| GET | api/projects/{id}/error_tracking/severity_rules/{id} | read | error_tracking | error_tracking_severity_rules_retrieve. |
| PUT | api/projects/{id}/error_tracking/severity_rules/{id} | write | error_tracking | error_tracking_severity_rules_update. |
| PATCH | api/projects/{id}/error_tracking/severity_rules/{id} | write | error_tracking | error_tracking_severity_rules_partial_update. |
| DELETE | api/projects/{id}/error_tracking/severity_rules/{id} | write | error_tracking | error_tracking_severity_rules_destroy. |
| GET | api/projects/{id}/error_tracking/spike_detection_config | read | error_tracking | error_tracking_spike_detection_config_list. |
| PATCH | api/projects/{id}/error_tracking/spike_detection_config/update_config | write | error_tracking | error_tracking_spike_detection_config_update_config_partial_update. |
| GET | api/projects/{id}/error_tracking/spike_events | read | error_tracking | error_tracking_spike_events_list. |
| GET | api/projects/{id}/error_tracking/stack_frames | read | error_tracking | error_tracking_stack_frames_list. |
| POST | api/projects/{id}/error_tracking/stack_frames/batch_get | read | error_tracking | error_tracking_stack_frames_batch_get_create. |
| GET | api/projects/{id}/error_tracking/stack_frames/{id} | read | error_tracking | error_tracking_stack_frames_retrieve. |
| DELETE | api/projects/{id}/error_tracking/stack_frames/{id} | write | error_tracking | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/error_tracking/suppression_rules | read | error_tracking | error_tracking_suppression_rules_list. |
| POST | api/projects/{id}/error_tracking/suppression_rules | write | error_tracking | error_tracking_suppression_rules_create. |
| PATCH | api/projects/{id}/error_tracking/suppression_rules/reorder | write | error_tracking | error_tracking_suppression_rules_reorder_partial_update. |
| GET | api/projects/{id}/error_tracking/suppression_rules/{id} | read | error_tracking | error_tracking_suppression_rules_retrieve. |
| PUT | api/projects/{id}/error_tracking/suppression_rules/{id} | write | error_tracking | error_tracking_suppression_rules_update. |
| PATCH | api/projects/{id}/error_tracking/suppression_rules/{id} | write | error_tracking | error_tracking_suppression_rules_partial_update. |
| DELETE | api/projects/{id}/error_tracking/suppression_rules/{id} | write | error_tracking | error_tracking_suppression_rules_destroy. |
| GET | api/projects/{id}/error_tracking/symbol_sets | read | error_tracking | error_tracking_symbol_sets_list. |
| POST | api/projects/{id}/error_tracking/symbol_sets/bulk_check_upload | write | error_tracking | Report which of the given symbol sets still need `bulk_start_upload`. |
| POST | api/projects/{id}/error_tracking/symbol_sets/bulk_delete | write | error_tracking | error_tracking_symbol_sets_bulk_delete_create. |
| POST | api/projects/{id}/error_tracking/symbol_sets/bulk_finish_upload | write | error_tracking | error_tracking_symbol_sets_bulk_finish_upload_create. |
| POST | api/projects/{id}/error_tracking/symbol_sets/bulk_start_upload | write | error_tracking | error_tracking_symbol_sets_bulk_start_upload_create. |
| GET | api/projects/{id}/error_tracking/symbol_sets/{id} | read | error_tracking | error_tracking_symbol_sets_retrieve. |
| DELETE | api/projects/{id}/error_tracking/symbol_sets/{id} | write | error_tracking | error_tracking_symbol_sets_destroy. |
| GET | api/projects/{id}/error_tracking/symbol_sets/{id}/download | write | error_tracking | Return a presigned URL for downloading the symbol set's source map. Kept out of read: returns a pre-signed download URL. |
| PUT | api/projects/{id}/error_tracking/symbol_sets/{id}/finish_upload | write | error_tracking | error_tracking_symbol_sets_finish_upload_update. |
| GET | api/projects/{id}/error_tracking/tag_rules | read | error_tracking | error_tracking_tag_rules_list. |
| POST | api/projects/{id}/error_tracking/tag_rules | write | error_tracking | error_tracking_tag_rules_create. |
| PATCH | api/projects/{id}/error_tracking/tag_rules/reorder | write | error_tracking | error_tracking_tag_rules_reorder_partial_update. |
| GET | api/projects/{id}/error_tracking/tag_rules/{id} | read | error_tracking | error_tracking_tag_rules_retrieve. |
| PUT | api/projects/{id}/error_tracking/tag_rules/{id} | write | error_tracking | error_tracking_tag_rules_update. |
| PATCH | api/projects/{id}/error_tracking/tag_rules/{id} | write | error_tracking | error_tracking_tag_rules_partial_update. |
| DELETE | api/projects/{id}/error_tracking/tag_rules/{id} | write | error_tracking | error_tracking_tag_rules_destroy. |
| GET | api/projects/{id}/evaluations | read | evaluations | evaluations_list. |
| POST | api/projects/{id}/evaluations | write | evaluations | evaluations_create. |
| GET | api/projects/{id}/evaluations/overview | read | evaluations | Each evaluation's results over a period, compared with the period of equal length before it. |
| POST | api/projects/{id}/evaluations/sample_traffic | write | evaluations | The latest units an unsaved evaluation would run on, newest first. |
| POST | api/projects/{id}/evaluations/test_hog | write | evaluations | Test Hog evaluation code against sample events without saving. |
| POST | api/projects/{id}/evaluations/test_on_sample | write | evaluations | Run an unsaved LLM judge on a few samples. |
| GET | api/projects/{id}/evaluations/{id} | read | evaluations | evaluations_retrieve. |
| PUT | api/projects/{id}/evaluations/{id} | write | evaluations | evaluations_update. |
| PATCH | api/projects/{id}/evaluations/{id} | write | evaluations | evaluations_partial_update. |
| DELETE | api/projects/{id}/evaluations/{id} | write | evaluations | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/evaluations/{id}/backfills | read | evaluations | Historical runs of one evaluation over a closed time window (nested under an evaluation). |
| POST | api/projects/{id}/evaluations/{id}/backfills | write | evaluations | Create a backfill: freeze the conditions, count the units, start the walk. |
| POST | api/projects/{id}/evaluations/{id}/backfills/estimate | write | evaluations | Count what a backfill over the given window would evaluate, without creating one. |
| GET | api/projects/{id}/evaluations/{id}/backfills/{id} | read | evaluations | Historical runs of one evaluation over a closed time window (nested under an evaluation). |
| POST | api/projects/{id}/evaluations/{id}/backfills/{id}/cancel | write | evaluations | Stop a running backfill. |
| GET | api/projects/{id}/evaluations/{id}/runs | read | evaluations | One evaluation's latest graded runs in a period, newest first, optionally only the passed or failed ones. |
| GET | api/projects/{id}/evaluations/{id}/score_distribution | read | evaluations | How one numeric evaluation's scores in a period spread across its configured scale. |
| GET | api/projects/{id}/event_definitions | read | event_definitions | List the event definitions of a project. |
| POST | api/projects/{id}/event_definitions | write | event_definitions | event_definitions_create. |
| POST | api/projects/{id}/event_definitions/bulk_update_tags | write | event_definitions | Add, remove, or replace tags across multiple event definitions in one request. |
| POST | api/projects/{id}/event_definitions/bulk_update_verified | write | event_definitions | Mark multiple event definitions as verified or unverified in one request. |
| GET | api/projects/{id}/event_definitions/by_name | read | event_definitions | Get event definition by exact name. |
| GET | api/projects/{id}/event_definitions/golang | read | event_definitions | event_definitions_golang_retrieve. |
| GET | api/projects/{id}/event_definitions/primary_properties | read | event_definitions | Resolve team-configured primary properties for event definitions. |
| GET | api/projects/{id}/event_definitions/python | read | event_definitions | event_definitions_python_retrieve. |
| GET | api/projects/{id}/event_definitions/typescript | read | event_definitions | event_definitions_typescript_retrieve. |
| GET | api/projects/{id}/event_definitions/{id} | read | event_definitions | event_definitions_retrieve. |
| PUT | api/projects/{id}/event_definitions/{id} | write | event_definitions | event_definitions_update. |
| PATCH | api/projects/{id}/event_definitions/{id} | write | event_definitions | event_definitions_partial_update. |
| DELETE | api/projects/{id}/event_definitions/{id} | write | event_definitions | event_definitions_destroy. |
| GET | api/projects/{id}/event_definitions/{id}/metrics | read | event_definitions | event_definitions_metrics_retrieve. |
| POST | api/projects/{id}/event_definitions/{id}/stop_ingesting | write | event_definitions | Drop new events with this name at ingestion, then hide the definition and schedule its delete. |
| GET | api/projects/{id}/event_schemas | read | event_schemas | event_schemas_list. |
| POST | api/projects/{id}/event_schemas | write | event_schemas | event_schemas_create. |
| PUT | api/projects/{id}/event_schemas/{id} | write | event_schemas | event_schemas_update. |
| PATCH | api/projects/{id}/event_schemas/{id} | write | event_schemas | event_schemas_partial_update. |
| DELETE | api/projects/{id}/event_schemas/{id} | write | event_schemas | event_schemas_destroy. |
| GET | api/projects/{id}/events | read | events | This endpoint allows you to list and filter events. |
| GET | api/projects/{id}/events/values | read | events | List values of an event property from recent events. |
| GET | api/projects/{id}/events/{id} | read | events | events_retrieve. |
| GET | api/projects/{id}/experiment_holdouts | read | experiment_holdouts | Create, read, update and delete experiment holdouts. |
| POST | api/projects/{id}/experiment_holdouts | write | experiment_holdouts | Create, read, update and delete experiment holdouts. |
| GET | api/projects/{id}/experiment_holdouts/{id} | read | experiment_holdouts | Create, read, update and delete experiment holdouts. |
| PUT | api/projects/{id}/experiment_holdouts/{id} | write | experiment_holdouts | Create, read, update and delete experiment holdouts. |
| PATCH | api/projects/{id}/experiment_holdouts/{id} | write | experiment_holdouts | Create, read, update and delete experiment holdouts. |
| DELETE | api/projects/{id}/experiment_holdouts/{id} | write | experiment_holdouts | Create, read, update and delete experiment holdouts. |
| GET | api/projects/{id}/experiment_saved_metrics | read | experiment_saved_metrics | experiment_saved_metrics_list. |
| POST | api/projects/{id}/experiment_saved_metrics | write | experiment_saved_metrics | experiment_saved_metrics_create. |
| GET | api/projects/{id}/experiment_saved_metrics/{id} | read | experiment_saved_metrics | experiment_saved_metrics_retrieve. |
| PUT | api/projects/{id}/experiment_saved_metrics/{id} | write | experiment_saved_metrics | experiment_saved_metrics_update. |
| PATCH | api/projects/{id}/experiment_saved_metrics/{id} | write | experiment_saved_metrics | experiment_saved_metrics_partial_update. |
| DELETE | api/projects/{id}/experiment_saved_metrics/{id} | write | experiment_saved_metrics | experiment_saved_metrics_destroy. |
| GET | api/projects/{id}/experiments | read | experiments | List experiments for the current project. |
| POST | api/projects/{id}/experiments | write | experiments | Create a new experiment in draft status with optional metrics. |
| POST | api/projects/{id}/experiments/bulk_update_tags | write | experiments | Bulk update tags on multiple objects. |
| POST | api/projects/{id}/experiments/calculate_running_time | read | experiments | Estimate the recommended sample size and running time for an experiment. |
| POST | api/projects/{id}/experiments/create_from_prompt | write | experiments | Create an experiment that compares N versions of an LLM prompt using a metric template. |
| GET | api/projects/{id}/experiments/matching_ids | read | experiments | Get IDs of all experiments matching the current list filters. |
| GET | api/projects/{id}/experiments/prompt_templates | read | experiments | List the LLM metric templates that can be passed to `create_from_prompt`. |
| GET | api/projects/{id}/experiments/session_context | read | experiments | Resolve which experiments (and variants) a session recording saw. |
| POST | api/projects/{id}/experiments/session_contexts | write | experiments | Resolve experiment context for a batch of session recordings. |
| POST | api/projects/{id}/experiments/setup_context | write | experiments | Facts about this project that decide how to configure a new experiment. |
| GET | api/projects/{id}/experiments/stats | read | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/projects/{id}/experiments/{id} | read | experiments | Retrieve a single experiment by ID, including its current status, metrics, feature flag, and results metadata. |
| PUT | api/projects/{id}/experiments/{id} | write | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| PATCH | api/projects/{id}/experiments/{id} | write | experiments | Update an experiment. |
| DELETE | api/projects/{id}/experiments/{id} | write | experiments | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/experiments/{id}/activity | read | experiments | Change history for this experiment. |
| POST | api/projects/{id}/experiments/{id}/archive | write | experiments | Archive an ended experiment. |
| POST | api/projects/{id}/experiments/{id}/copy_to_project | write | experiments | Copy an experiment into another project in the same organization as a new draft. |
| POST | api/projects/{id}/experiments/{id}/create_exposure_cohort_for_experiment | write | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/experiments/{id}/duplicate | write | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/experiments/{id}/end | write | experiments | End a running experiment without shipping a variant. |
| GET | api/projects/{id}/experiments/{id}/flag_cleanup_target | read | experiments | Repository a flag-cleanup pull request for this experiment would be opened in. |
| GET | api/projects/{id}/experiments/{id}/flag_cleanup_task | read | experiments | Status of the flag-cleanup Desktop task opened for this experiment. |
| POST | api/projects/{id}/experiments/{id}/freeze_exposure | write | experiments | Freeze exposure on a running experiment while metrics keep flowing. |
| GET | api/projects/{id}/experiments/{id}/health | read | experiments | Health check findings for this experiment: problems in its configuration and its feature flag that keep it from producing trustworthy results, each with a fix. |
| GET | api/projects/{id}/experiments/{id}/health_inputs | read | experiments | Staff only. |
| GET | api/projects/{id}/experiments/{id}/in_session_exposure | read | experiments | How the recordings tab's in-session exposure scope reads on this experiment. |
| POST | api/projects/{id}/experiments/{id}/launch | write | experiments | Launch a draft experiment. |
| POST | api/projects/{id}/experiments/{id}/metrics_recalculation | write | experiments | Trigger a batch recalculation of all metrics for this experiment. |
| GET | api/projects/{id}/experiments/{id}/metrics_recalculation/latest | read | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/projects/{id}/experiments/{id}/metrics_recalculation/{id} | read | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/experiments/{id}/migrate | write | experiments | Move a legacy experiment onto the new experiments engine. |
| POST | api/projects/{id}/experiments/{id}/pause | write | experiments | Pause a running experiment. |
| POST | api/projects/{id}/experiments/{id}/recalculate_timeseries | write | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/experiments/{id}/reset | write | experiments | Reset an experiment back to draft state. |
| POST | api/projects/{id}/experiments/{id}/resume | write | experiments | Resume a paused experiment. |
| GET | api/projects/{id}/experiments/{id}/running_time_target | read | experiments | The target sample of the experiment's running time estimate, which the experiment page's header compares with the exposures so far, and what the experiment can detect over time. |
| POST | api/projects/{id}/experiments/{id}/session_buckets | write | experiments | Session recordings of this experiment matching a bucket. |
| POST | api/projects/{id}/experiments/{id}/session_event_deltas | write | experiments | The recordings worth watching for this experiment, grouped into cards. |
| POST | api/projects/{id}/experiments/{id}/ship_variant | write | experiments | Ship a variant and (optionally) end the experiment. |
| GET | api/projects/{id}/experiments/{id}/timeseries_results | read | experiments | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/experiments/{id}/unarchive | write | experiments | Unarchive an archived experiment. |
| POST | api/projects/{id}/experiments/{id}/unfreeze_exposure | write | experiments | Reopen enrollment on an exposure-frozen experiment. |
| GET | api/projects/{id}/exports | read | exports | exports_list. |
| POST | api/projects/{id}/exports | write | exports | exports_create. |
| GET | api/projects/{id}/exports/{id} | read | exports | exports_retrieve. |
| GET | api/projects/{id}/exports/{id}/content | read | exports | exports_content_retrieve. |
| GET | api/projects/{id}/feature_flags | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags | write | feature_flags | Create, read, update and delete feature flags. |
| GET | api/projects/{id}/feature_flags/activity | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags/bulk_delete | write | feature_flags | Bulk delete feature flags by filter criteria or explicit IDs. |
| POST | api/projects/{id}/feature_flags/bulk_keys | write | feature_flags | Get feature flag keys by IDs. |
| POST | api/projects/{id}/feature_flags/bulk_update_tags | write | feature_flags | Bulk update tags on multiple objects. |
| GET | api/projects/{id}/feature_flags/evaluation_reasons | read | feature_flags | Create, read, update and delete feature flags. |
| GET | api/projects/{id}/feature_flags/matching_ids | read | feature_flags | Get IDs of all feature flags matching the current filters. |
| GET | api/projects/{id}/feature_flags/my_flags | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags/user_blast_radius | write | feature_flags | Create, read, update and delete feature flags. |
| GET | api/projects/{id}/feature_flags/{id} | read | feature_flags | Create, read, update and delete feature flags. |
| PUT | api/projects/{id}/feature_flags/{id} | write | feature_flags | Create, read, update and delete feature flags. |
| PATCH | api/projects/{id}/feature_flags/{id} | write | feature_flags | Create, read, update and delete feature flags. |
| DELETE | api/projects/{id}/feature_flags/{id} | write | feature_flags | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/feature_flags/{id}/activity | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags/{id}/analyze_code | write | feature_flags | Start a read-only analysis of where the project's GitHub repository checks this flag. |
| POST | api/projects/{id}/feature_flags/{id}/archive | write | feature_flags | Archive a feature flag, hiding it from the default flag list. |
| GET | api/projects/{id}/feature_flags/{id}/code_analysis | read | feature_flags | The latest code analysis of this flag: where the project's GitHub repository checks the flag, and the code each outcome runs. |
| GET | api/projects/{id}/feature_flags/{id}/code_analysis_target | read | feature_flags | Repository a code analysis of this flag would read. |
| POST | api/projects/{id}/feature_flags/{id}/create_static_cohort_for_flag | write | feature_flags | Create, read, update and delete feature flags. |
| GET | api/projects/{id}/feature_flags/{id}/dependent_flags | read | feature_flags | Get other active flags that depend on this flag. |
| POST | api/projects/{id}/feature_flags/{id}/disable | write | feature_flags | Disable a feature flag. |
| POST | api/projects/{id}/feature_flags/{id}/enable | write | feature_flags | Enable a feature flag. |
| POST | api/projects/{id}/feature_flags/{id}/open_cleanup_pr | write | feature_flags | Open a draft pull request that removes this stale flag's checks from the code. |
| GET | api/projects/{id}/feature_flags/{id}/remote_config | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags/{id}/roll_out_to_everyone | write | feature_flags | Serve a feature flag to every user. |
| POST | api/projects/{id}/feature_flags/{id}/set_release_condition_rollout | write | feature_flags | Set what percentage of one release condition's audience a feature flag is served to. |
| GET | api/projects/{id}/feature_flags/{id}/status | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags/{id}/test_evaluation | write | feature_flags | Test feature flag evaluation against a specific user at an optional point in time. |
| POST | api/projects/{id}/feature_flags/{id}/unarchive | write | feature_flags | Restore an archived feature flag to the default flag list. |
| GET | api/projects/{id}/feature_flags/{id}/versions/{id} | read | feature_flags | Create, read, update and delete feature flags. |
| POST | api/projects/{id}/feature_flags/{id}/versions/{id}/restore | write | feature_flags | Restore a past version of a feature flag. |
| GET | api/projects/{id}/file_system | read | file_system | file_system_list. |
| POST | api/projects/{id}/file_system | write | file_system | file_system_create. |
| POST | api/projects/{id}/file_system/count_by_path | write | file_system | Get count of all files in a folder. |
| GET | api/projects/{id}/file_system/frequent | read | file_system | List frequently viewed files. |
| POST | api/projects/{id}/file_system/home_folder | write | file_system | file_system_home_folder_create. |
| GET | api/projects/{id}/file_system/log_view | read | file_system | file_system_log_view_retrieve. |
| POST | api/projects/{id}/file_system/log_view | write | file_system | file_system_log_view_create. |
| GET | api/projects/{id}/file_system/search | read | file_system | Search files by relevance. |
| POST | api/projects/{id}/file_system/undo_delete | write | file_system | file_system_undo_delete_create. |
| GET | api/projects/{id}/file_system/unfiled | read | file_system | file_system_unfiled_retrieve. |
| GET | api/projects/{id}/file_system/{id} | read | file_system | file_system_retrieve. |
| PUT | api/projects/{id}/file_system/{id} | write | file_system | file_system_update. |
| PATCH | api/projects/{id}/file_system/{id} | write | file_system | file_system_partial_update. |
| DELETE | api/projects/{id}/file_system/{id} | write | file_system | file_system_destroy. |
| POST | api/projects/{id}/file_system/{id}/count | write | file_system | Get count of all files in a folder. |
| POST | api/projects/{id}/file_system/{id}/link | write | file_system | file_system_link_create. |
| POST | api/projects/{id}/file_system/{id}/move | write | file_system | file_system_move_create. |
| GET | api/projects/{id}/groups | read | groups | List all groups of a specific group type. |
| POST | api/projects/{id}/groups | write | groups | groups_create. |
| GET | api/projects/{id}/groups/activity | read | groups | groups_activity_retrieve. |
| POST | api/projects/{id}/groups/delete_property | write | groups | groups_delete_property_create. |
| GET | api/projects/{id}/groups/find | read | groups | groups_find_retrieve. |
| GET | api/projects/{id}/groups/property_values | read | groups | groups_property_values_retrieve. |
| GET | api/projects/{id}/groups/related | read | groups | groups_related_list. |
| POST | api/projects/{id}/groups/update_property | write | groups | groups_update_property_create. |
| GET | api/projects/{id}/groups_types | read | groups_types | groups_types_list. |
| PUT | api/projects/{id}/groups_types/create_detail_dashboard | write | groups_types | groups_types_create_detail_dashboard_update. |
| PUT | api/projects/{id}/groups_types/set_default_columns | write | groups_types | groups_types_set_default_columns_update. |
| PATCH | api/projects/{id}/groups_types/update_metadata | write | groups_types | groups_types_update_metadata_partial_update. |
| DELETE | api/projects/{id}/groups_types/{id} | write | groups_types | groups_types_destroy. |
| GET | api/projects/{id}/groups_types/{id}/metrics | read | groups_types | groups_types_metrics_list. |
| POST | api/projects/{id}/groups_types/{id}/metrics | write | groups_types | groups_types_metrics_create. |
| GET | api/projects/{id}/groups_types/{id}/metrics/{id} | read | groups_types | groups_types_metrics_retrieve. |
| PUT | api/projects/{id}/groups_types/{id}/metrics/{id} | write | groups_types | groups_types_metrics_update. |
| PATCH | api/projects/{id}/groups_types/{id}/metrics/{id} | write | groups_types | groups_types_metrics_partial_update. |
| DELETE | api/projects/{id}/groups_types/{id}/metrics/{id} | write | groups_types | groups_types_metrics_destroy. |
| GET | api/projects/{id}/health_issues | read | health_issues | List health issues. |
| POST | api/projects/{id}/health_issues/refresh | write | health_issues | health_issues_refresh_create. |
| GET | api/projects/{id}/health_issues/summary | read | health_issues | Summarize active health issues. |
| GET | api/projects/{id}/health_issues/{id} | read | health_issues | Get a health issue. |
| PATCH | api/projects/{id}/health_issues/{id} | write | health_issues | health_issues_partial_update. |
| POST | api/projects/{id}/health_issues/{id}/resolve | write | health_issues | health_issues_resolve_create. |
| GET | api/projects/{id}/heatmap_screenshots/{id}/content | read | heatmap_screenshots | Fetch the rendered screenshot image (JPEG bytes) for a saved heatmap at a given viewport width. |
| GET | api/projects/{id}/heatmaps | read | heatmaps | Aggregated heatmap interactions for a page. |
| GET | api/projects/{id}/heatmaps/events | read | heatmaps | Drill into the individual session interactions behind one or more heatmap coordinates. |
| GET | api/projects/{id}/hog_function_templates | read | hog_function_templates | hog_function_templates_list. |
| GET | api/projects/{id}/hog_function_templates/{id} | read | hog_function_templates | hog_function_templates_retrieve. |
| GET | api/projects/{id}/hog_functions | read | hog_functions | hog_functions_list. |
| POST | api/projects/{id}/hog_functions | write | hog_functions | hog_functions_create. |
| GET | api/projects/{id}/hog_functions/icon | read | hog_functions | hog_functions_icon_retrieve. |
| GET | api/projects/{id}/hog_functions/icons | read | hog_functions | hog_functions_icons_retrieve. |
| GET | api/projects/{id}/hog_functions/masked_secrets | read | hog_functions | Hog functions storing the secret mask in place of a real credential. |
| PATCH | api/projects/{id}/hog_functions/rearrange | write | hog_functions | Update the execution order of multiple HogFunctions. |
| GET | api/projects/{id}/hog_functions/{id} | write | hog_functions | hog_functions_retrieve. Kept out of read: returns function secrets and tokens. |
| PUT | api/projects/{id}/hog_functions/{id} | write | hog_functions | hog_functions_update. |
| PATCH | api/projects/{id}/hog_functions/{id} | write | hog_functions | hog_functions_partial_update. |
| DELETE | api/projects/{id}/hog_functions/{id} | write | hog_functions | Hard delete of this model is not allowed. |
| POST | api/projects/{id}/hog_functions/{id}/discard_draft | write | hog_functions | hog_functions_discard_draft_create. |
| POST | api/projects/{id}/hog_functions/{id}/enable_backfills | write | hog_functions | hog_functions_enable_backfills_create. |
| POST | api/projects/{id}/hog_functions/{id}/invocations | write | hog_functions | hog_functions_invocations_create. |
| GET | api/projects/{id}/hog_functions/{id}/logs | read | hog_functions | hog_functions_logs_retrieve. |
| GET | api/projects/{id}/hog_functions/{id}/metrics | read | hog_functions | hog_functions_metrics_retrieve. |
| GET | api/projects/{id}/hog_functions/{id}/metrics/totals | read | hog_functions | hog_functions_metrics_totals_retrieve. |
| POST | api/projects/{id}/hog_functions/{id}/publish | write | hog_functions | hog_functions_publish_create. |
| POST | api/projects/{id}/hog_functions/{id}/rerun | write | hog_functions | Rerun past invocations of this hog function from their stored payloads. |
| GET | api/projects/{id}/hog_functions/{id}/revisions | read | hog_functions | hog_functions_revisions_list. |
| GET | api/projects/{id}/hog_functions/{id}/revisions/{id} | read | hog_functions | hog_functions_revisions_retrieve. |
| POST | api/projects/{id}/hog_functions/{id}/revisions/{id}/restore | write | hog_functions | hog_functions_revisions_restore_create. |
| GET | api/projects/{id}/ingestion_warnings_v2 | read | ingestion_warnings_v2 | List ingestion warnings. |
| GET | api/projects/{id}/insight_variables | read | insight_variables | insight_variables_list. |
| POST | api/projects/{id}/insight_variables | write | insight_variables | insight_variables_create. |
| GET | api/projects/{id}/insight_variables/{id} | read | insight_variables | insight_variables_retrieve. |
| PUT | api/projects/{id}/insight_variables/{id} | write | insight_variables | insight_variables_update. |
| PATCH | api/projects/{id}/insight_variables/{id} | write | insight_variables | insight_variables_partial_update. |
| DELETE | api/projects/{id}/insight_variables/{id} | write | insight_variables | insight_variables_destroy. |
| GET | api/projects/{id}/insights | read | insights | insights_list. |
| POST | api/projects/{id}/insights | write | insights | insights_create. |
| GET | api/projects/{id}/insights/activity | read | insights | Project-wide audit trail across all insights — who created, edited, deleted, or restored insights, what changed (with before/after diffs), and when. |
| POST | api/projects/{id}/insights/bulk_delete | write | insights | Soft-delete insights in bulk by ID. |
| POST | api/projects/{id}/insights/bulk_restore | write | insights | Restore soft-deleted insights in bulk by ID — the inverse of bulk_delete. |
| POST | api/projects/{id}/insights/bulk_set_test_account_filter | write | insights | Turn 'filter out internal and test users' on or off for every existing insight in the project. |
| POST | api/projects/{id}/insights/bulk_update_tags | write | insights | Bulk update tags on multiple objects. |
| POST | api/projects/{id}/insights/cancel | write | insights | insights_cancel_create. |
| POST | api/projects/{id}/insights/data_checks | read | insights | Check the events behind an insight for the common ways they mislead: internal and test users, local development traffic, bots and crawlers, and events sent twice. |
| POST | api/projects/{id}/insights/generate_metadata | write | insights | Generate an AI-suggested name and description for an insight based on its query configuration. |
| GET | api/projects/{id}/insights/my_last_viewed | read | insights | Returns basic details about the last 5 insights viewed by this user. |
| GET | api/projects/{id}/insights/trending | read | insights | Returns insights ranked by view count over the last N days (default 7), highest first. |
| POST | api/projects/{id}/insights/viewed | write | insights | Record that the current user has just viewed one or more insights. |
| GET | api/projects/{id}/insights/{id} | read | insights | insights_retrieve. |
| PUT | api/projects/{id}/insights/{id} | write | insights | insights_update. |
| PATCH | api/projects/{id}/insights/{id} | write | insights | insights_partial_update. |
| DELETE | api/projects/{id}/insights/{id} | write | insights | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/insights/{id}/activity | read | insights | Audit trail for a single insight — every change made to it, by whom, and when. |
| GET | api/projects/{id}/insights/{id}/data_checks | read | insights | Run the data checks on a saved insight, found by its numeric id or its `short_id`. |
| POST | api/projects/{id}/insights/{id}/explanations | write | insights | insights_explanations_create. |
| GET | api/projects/{id}/insights/{id}/explanations/{id} | read | insights | insights_explanations_retrieve. |
| PUT | api/projects/{id}/insights/{id}/explanations/{id} | write | insights | insights_explanations_update. |
| GET | api/projects/{id}/insights/{id}/sharing | write | insights | insights_sharing_list. Kept out of read: returns share access tokens. |
| POST | api/projects/{id}/insights/{id}/sharing/passwords | write | insights | Create a new password for the sharing configuration. |
| DELETE | api/projects/{id}/insights/{id}/sharing/passwords/{id} | write | insights | Delete a password from the sharing configuration. |
| POST | api/projects/{id}/insights/{id}/sharing/refresh | write | insights | insights_sharing_refresh_create. |
| GET | api/projects/{id}/insights/{id}/thresholds | read | insights | insights_thresholds_list. |
| GET | api/projects/{id}/insights/{id}/thresholds/{id} | read | insights | insights_thresholds_retrieve. |
| GET | api/projects/{id}/llm_analytics/clustering_config | read | llm_analytics | Team-level clustering configuration (event filters for automated pipelines). |
| POST | api/projects/{id}/llm_analytics/clustering_config/set_enabled | write | llm_analytics | Team-level clustering configuration (event filters for automated pipelines). |
| POST | api/projects/{id}/llm_analytics/clustering_config/set_event_filters | write | llm_analytics | Team-level clustering configuration (event filters for automated pipelines). |
| GET | api/projects/{id}/llm_analytics/clustering_jobs | read | llm_analytics | CRUD for clustering job configurations (max 10 per team). |
| POST | api/projects/{id}/llm_analytics/clustering_jobs | write | llm_analytics | CRUD for clustering job configurations (max 10 per team). |
| GET | api/projects/{id}/llm_analytics/clustering_jobs/{id} | read | llm_analytics | CRUD for clustering job configurations (max 10 per team). |
| PUT | api/projects/{id}/llm_analytics/clustering_jobs/{id} | write | llm_analytics | CRUD for clustering job configurations (max 10 per team). |
| PATCH | api/projects/{id}/llm_analytics/clustering_jobs/{id} | write | llm_analytics | CRUD for clustering job configurations (max 10 per team). |
| DELETE | api/projects/{id}/llm_analytics/clustering_jobs/{id} | write | llm_analytics | CRUD for clustering job configurations (max 10 per team). |
| POST | api/projects/{id}/llm_analytics/clustering_runs | write | llm_analytics | Trigger a new clustering workflow run. |
| GET | api/projects/{id}/llm_analytics/evaluation_config | write | llm_analytics | Get the evaluation config for this team. Kept out of read: returns LLM provider API keys. |
| POST | api/projects/{id}/llm_analytics/evaluation_config/set_active_key | write | llm_analytics | Set the active provider key for evaluations. |
| GET | api/projects/{id}/llm_analytics/evaluation_reports | read | llm_analytics | CRUD for evaluation report configurations + report run history. |
| POST | api/projects/{id}/llm_analytics/evaluation_reports | write | llm_analytics | CRUD for evaluation report configurations + report run history. |
| GET | api/projects/{id}/llm_analytics/evaluation_reports/{id} | read | llm_analytics | CRUD for evaluation report configurations + report run history. |
| PUT | api/projects/{id}/llm_analytics/evaluation_reports/{id} | write | llm_analytics | CRUD for evaluation report configurations + report run history. |
| PATCH | api/projects/{id}/llm_analytics/evaluation_reports/{id} | write | llm_analytics | CRUD for evaluation report configurations + report run history. |
| DELETE | api/projects/{id}/llm_analytics/evaluation_reports/{id} | write | llm_analytics | Evaluation report configs are deleted only when their evaluation is deleted. |
| POST | api/projects/{id}/llm_analytics/evaluation_reports/{id}/generate | write | llm_analytics | Trigger immediate report generation. |
| GET | api/projects/{id}/llm_analytics/evaluation_reports/{id}/runs | read | llm_analytics | List report runs (history) for this report. |
| GET | api/projects/{id}/llm_analytics/models | read | llm_analytics | List available models, for one provider or for every supported provider. |
| GET | api/projects/{id}/llm_analytics/parser_recipes | read | llm_analytics | llm_analytics_parser_recipes_list. |
| POST | api/projects/{id}/llm_analytics/parser_recipes | write | llm_analytics | llm_analytics_parser_recipes_create. |
| GET | api/projects/{id}/llm_analytics/parser_recipes/{id} | read | llm_analytics | llm_analytics_parser_recipes_retrieve. |
| PATCH | api/projects/{id}/llm_analytics/parser_recipes/{id} | write | llm_analytics | llm_analytics_parser_recipes_partial_update. |
| DELETE | api/projects/{id}/llm_analytics/parser_recipes/{id} | write | llm_analytics | llm_analytics_parser_recipes_destroy. |
| POST | api/projects/{id}/llm_analytics/provider_key_validations | write | llm_analytics | Validate LLM provider API keys without persisting them. |
| GET | api/projects/{id}/llm_analytics/provider_keys | write | llm_analytics | llm_analytics_provider_keys_list. Kept out of read: returns LLM provider API keys. |
| POST | api/projects/{id}/llm_analytics/provider_keys | write | llm_analytics | llm_analytics_provider_keys_create. |
| GET | api/projects/{id}/llm_analytics/provider_keys/{id} | write | llm_analytics | llm_analytics_provider_keys_retrieve. Kept out of read: returns LLM provider API keys. |
| PUT | api/projects/{id}/llm_analytics/provider_keys/{id} | write | llm_analytics | llm_analytics_provider_keys_update. |
| PATCH | api/projects/{id}/llm_analytics/provider_keys/{id} | write | llm_analytics | llm_analytics_provider_keys_partial_update. |
| DELETE | api/projects/{id}/llm_analytics/provider_keys/{id} | write | llm_analytics | llm_analytics_provider_keys_destroy. |
| GET | api/projects/{id}/llm_analytics/provider_keys/{id}/dependent_configs | read | llm_analytics | Get evaluations using this key and alternative keys for replacement. |
| GET | api/projects/{id}/llm_analytics/provider_keys/{id}/models | read | llm_analytics | Models this provider key can run, as the model pickers list them. |
| POST | api/projects/{id}/llm_analytics/provider_keys/{id}/validate | write | llm_analytics | llm_analytics_provider_keys_validate_create. |
| GET | api/projects/{id}/llm_analytics/review_queue_items | read | llm_analytics | llm_analytics_review_queue_items_list. |
| POST | api/projects/{id}/llm_analytics/review_queue_items | write | llm_analytics | llm_analytics_review_queue_items_create. |
| GET | api/projects/{id}/llm_analytics/review_queue_items/{id} | read | llm_analytics | llm_analytics_review_queue_items_retrieve. |
| PATCH | api/projects/{id}/llm_analytics/review_queue_items/{id} | write | llm_analytics | llm_analytics_review_queue_items_partial_update. |
| DELETE | api/projects/{id}/llm_analytics/review_queue_items/{id} | write | llm_analytics | llm_analytics_review_queue_items_destroy. |
| GET | api/projects/{id}/llm_analytics/review_queues | read | llm_analytics | llm_analytics_review_queues_list. |
| POST | api/projects/{id}/llm_analytics/review_queues | write | llm_analytics | llm_analytics_review_queues_create. |
| GET | api/projects/{id}/llm_analytics/review_queues/{id} | read | llm_analytics | llm_analytics_review_queues_retrieve. |
| PATCH | api/projects/{id}/llm_analytics/review_queues/{id} | write | llm_analytics | llm_analytics_review_queues_partial_update. |
| DELETE | api/projects/{id}/llm_analytics/review_queues/{id} | write | llm_analytics | llm_analytics_review_queues_destroy. |
| GET | api/projects/{id}/llm_analytics/score_definitions | read | llm_analytics | llm_analytics_score_definitions_list. |
| POST | api/projects/{id}/llm_analytics/score_definitions | write | llm_analytics | llm_analytics_score_definitions_create. |
| POST | api/projects/{id}/llm_analytics/score_definitions/validate_composition | write | llm_analytics | llm_analytics_score_definitions_validate_composition_create. |
| GET | api/projects/{id}/llm_analytics/score_definitions/{id} | read | llm_analytics | llm_analytics_score_definitions_retrieve. |
| PATCH | api/projects/{id}/llm_analytics/score_definitions/{id} | write | llm_analytics | llm_analytics_score_definitions_partial_update. |
| POST | api/projects/{id}/llm_analytics/score_definitions/{id}/new_version | write | llm_analytics | llm_analytics_score_definitions_new_version_create. |
| GET | api/projects/{id}/llm_analytics/score_definitions/{id}/versions | read | llm_analytics | llm_analytics_score_definitions_versions_list. |
| GET | api/projects/{id}/llm_analytics/score_definitions/{id}/versions/{id} | read | llm_analytics | llm_analytics_score_definitions_versions_retrieve. |
| POST | api/projects/{id}/llm_analytics/summarization | write | llm_analytics | Generate an AI-powered summary of an LLM trace or event. |
| POST | api/projects/{id}/llm_analytics/summarization/batch_check | read | llm_analytics | Check which traces have cached summaries available. |
| POST | api/projects/{id}/llm_analytics/text_repr | write | llm_analytics | Generate a human-readable text representation of an LLM trace event. |
| GET | api/projects/{id}/llm_analytics/trace_reviews | read | llm_analytics | llm_analytics_trace_reviews_list. |
| POST | api/projects/{id}/llm_analytics/trace_reviews | write | llm_analytics | llm_analytics_trace_reviews_create. |
| GET | api/projects/{id}/llm_analytics/trace_reviews/{id} | read | llm_analytics | llm_analytics_trace_reviews_retrieve. |
| PATCH | api/projects/{id}/llm_analytics/trace_reviews/{id} | write | llm_analytics | llm_analytics_trace_reviews_partial_update. |
| DELETE | api/projects/{id}/llm_analytics/trace_reviews/{id} | write | llm_analytics | llm_analytics_trace_reviews_destroy. |
| POST | api/projects/{id}/llm_analytics/translate | write | llm_analytics | Translate text to target language. |
| GET | api/projects/{id}/llm_prompts | read | llm_prompts | llm_prompts_list. |
| POST | api/projects/{id}/llm_prompts | write | llm_prompts | llm_prompts_create. |
| GET | api/projects/{id}/llm_prompts/name/{id} | read | llm_prompts | llm_prompts_name_retrieve. |
| PATCH | api/projects/{id}/llm_prompts/name/{id} | write | llm_prompts | llm_prompts_name_partial_update. |
| POST | api/projects/{id}/llm_prompts/name/{id}/archive | write | llm_prompts | llm_prompts_name_archive_create. |
| POST | api/projects/{id}/llm_prompts/name/{id}/duplicate | write | llm_prompts | llm_prompts_name_duplicate_create. |
| PUT | api/projects/{id}/llm_prompts/name/{id}/labels/{id} | write | llm_prompts | llm_prompts_name_labels_update. |
| DELETE | api/projects/{id}/llm_prompts/name/{id}/labels/{id} | write | llm_prompts | llm_prompts_name_labels_destroy. |
| POST | api/projects/{id}/llm_prompts/name/{id}/unarchive | write | llm_prompts | llm_prompts_name_unarchive_create. |
| GET | api/projects/{id}/llm_prompts/resolve/name/{id} | read | llm_prompts | llm_prompts_resolve_name_retrieve. |
| GET | api/projects/{id}/logs/alerts | read | logs | logs_alerts_list. |
| POST | api/projects/{id}/logs/alerts | write | logs | logs_alerts_create. |
| POST | api/projects/{id}/logs/alerts/simulate | write | logs | Simulate a logs alert on historical data using the full state machine. |
| GET | api/projects/{id}/logs/alerts/{id} | read | logs | logs_alerts_retrieve. |
| PUT | api/projects/{id}/logs/alerts/{id} | write | logs | logs_alerts_update. |
| PATCH | api/projects/{id}/logs/alerts/{id} | write | logs | logs_alerts_partial_update. |
| DELETE | api/projects/{id}/logs/alerts/{id} | write | logs | logs_alerts_destroy. |
| POST | api/projects/{id}/logs/alerts/{id}/destinations | write | logs | Create a notification destination for this alert. |
| POST | api/projects/{id}/logs/alerts/{id}/destinations/customize | write | logs | Make a destination's message editable. |
| POST | api/projects/{id}/logs/alerts/{id}/destinations/delete | write | logs | Delete a notification destination by deleting its HogFunction group atomically. |
| POST | api/projects/{id}/logs/alerts/{id}/destinations/reset | write | logs | Send a customized destination's standard message again. |
| GET | api/projects/{id}/logs/alerts/{id}/destinations/sends | read | logs | The last messages sent to one destination of this alert in the past 7 days, newest first, on both delivery paths, with whether each one succeeded. |
| GET | api/projects/{id}/logs/alerts/{id}/events | read | logs | Paginated event history for this alert, newest first. |
| POST | api/projects/{id}/logs/alerts/{id}/reset | write | logs | Reset a broken alert. |
| POST | api/projects/{id}/logs/anomalies/scan | write | logs | Scan a service's logs for volume anomalies. |
| POST | api/projects/{id}/logs/anomalies/series_bands | write | logs | Per-series log volume with expected bands. |
| GET | api/projects/{id}/logs/attributes | read | logs | logs_attributes_retrieve. |
| POST | api/projects/{id}/logs/context | write | logs | logs_context_create. |
| POST | api/projects/{id}/logs/count | write | logs | logs_count_create. |
| POST | api/projects/{id}/logs/count-ranges | write | logs | logs_count_ranges_create. |
| POST | api/projects/{id}/logs/explainLogWithAI | write | logs | Explain a log entry using AI. |
| POST | api/projects/{id}/logs/export | write | logs | logs_export_create. |
| POST | api/projects/{id}/logs/facet_values | read | logs | logs_facet_values_create. |
| POST | api/projects/{id}/logs/group-by | write | logs | logs_group_by_create. |
| GET | api/projects/{id}/logs/has_logs | read | logs | logs_has_logs_retrieve. |
| POST | api/projects/{id}/logs/impact | write | logs | logs_impact_create. |
| GET | api/projects/{id}/logs/metric_rules | read | logs | logs_metric_rules_list. |
| POST | api/projects/{id}/logs/metric_rules | write | logs | logs_metric_rules_create. |
| GET | api/projects/{id}/logs/metric_rules/{id} | read | logs | logs_metric_rules_retrieve. |
| PUT | api/projects/{id}/logs/metric_rules/{id} | write | logs | logs_metric_rules_update. |
| PATCH | api/projects/{id}/logs/metric_rules/{id} | write | logs | logs_metric_rules_partial_update. |
| DELETE | api/projects/{id}/logs/metric_rules/{id} | write | logs | logs_metric_rules_destroy. |
| POST | api/projects/{id}/logs/natural_language_query | read | logs | Turn a plain-language request into ranked log viewer filter candidates. |
| POST | api/projects/{id}/logs/patterns | write | logs | logs_patterns_create. |
| POST | api/projects/{id}/logs/patterns_diff | write | logs | logs_patterns_diff_create. |
| POST | api/projects/{id}/logs/query | read | logs | logs_query_create. |
| GET | api/projects/{id}/logs/retention_rules | read | logs | Retention rules for one record kind. |
| POST | api/projects/{id}/logs/retention_rules | write | logs | Retention rules for one record kind. |
| POST | api/projects/{id}/logs/retention_rules/reorder | write | logs | Atomically reassign priorities so the given ID order maps to ascending priorities (0..n-1). |
| POST | api/projects/{id}/logs/retention_rules/suggest_name | write | logs | Suggest a human-readable name for a retention rule from its retention tier and filter group. |
| GET | api/projects/{id}/logs/retention_rules/{id} | read | logs | Retention rules for one record kind. |
| PUT | api/projects/{id}/logs/retention_rules/{id} | write | logs | Retention rules for one record kind. |
| PATCH | api/projects/{id}/logs/retention_rules/{id} | write | logs | Retention rules for one record kind. |
| DELETE | api/projects/{id}/logs/retention_rules/{id} | write | logs | Retention rules for one record kind. |
| GET | api/projects/{id}/logs/sampling_rules | read | logs | logs_sampling_rules_list. |
| POST | api/projects/{id}/logs/sampling_rules | write | logs | logs_sampling_rules_create. |
| POST | api/projects/{id}/logs/sampling_rules/reorder | write | logs | Atomically reassign priorities so the given ID order maps to ascending priorities (0..n-1). |
| GET | api/projects/{id}/logs/sampling_rules/{id} | read | logs | logs_sampling_rules_retrieve. |
| PUT | api/projects/{id}/logs/sampling_rules/{id} | write | logs | logs_sampling_rules_update. |
| PATCH | api/projects/{id}/logs/sampling_rules/{id} | write | logs | logs_sampling_rules_partial_update. |
| DELETE | api/projects/{id}/logs/sampling_rules/{id} | write | logs | logs_sampling_rules_destroy. |
| POST | api/projects/{id}/logs/sampling_rules/{id}/simulate | write | logs | Dry-run estimate for how much volume this rule would remove (placeholder response until CH-backed simulation is wired). |
| POST | api/projects/{id}/logs/services | write | logs | logs_services_create. |
| POST | api/projects/{id}/logs/sparkline | write | logs | logs_sparkline_create. |
| GET | api/projects/{id}/logs/values | read | logs | logs_values_retrieve. |
| GET | api/projects/{id}/logs/views | read | logs | logs_views_list. |
| POST | api/projects/{id}/logs/views | write | logs | logs_views_create. |
| GET | api/projects/{id}/logs/views/{id} | read | logs | logs_views_retrieve. |
| PUT | api/projects/{id}/logs/views/{id} | write | logs | logs_views_update. |
| PATCH | api/projects/{id}/logs/views/{id} | write | logs | logs_views_partial_update. |
| DELETE | api/projects/{id}/logs/views/{id} | write | logs | logs_views_destroy. |
| GET | api/projects/{id}/notebooks | read | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks | write | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/activity | read | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/kernel/compute_options | read | notebooks | Compute rates, presets, and the sizes the kernel config endpoint accepts. |
| GET | api/projects/{id}/notebooks/recording_comments | read | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id} | read | notebooks | The API for interacting with Notebooks. |
| PUT | api/projects/{id}/notebooks/{id} | write | notebooks | The API for interacting with Notebooks. |
| PATCH | api/projects/{id}/notebooks/{id} | write | notebooks | The API for interacting with Notebooks. |
| DELETE | api/projects/{id}/notebooks/{id} | write | notebooks | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/notebooks/{id}/activity | read | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/collab/markdown_save | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/collab/presence | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/collab/save | write | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/collab/stream | read | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/kernel/complete | write | notebooks | Completions for the cursor position in a Python cell, from the notebook's running kernel. |
| POST | api/projects/{id}/notebooks/{id}/kernel/config | write | notebooks | Set the notebook's kernel compute configuration. |
| POST | api/projects/{id}/notebooks/{id}/kernel/execute | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/kernel/inspect | write | notebooks | The signature and docstring of the name at the cursor in a Python cell, from the notebook's running kernel. |
| POST | api/projects/{id}/notebooks/{id}/kernel/restart | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/kernel/start | write | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/kernel/status | read | notebooks | Live-checked kernel runtime state for this notebook, its compute configuration, and the catalog of dataframes/tables a cell can currently reference (with column schemas). |
| POST | api/projects/{id}/notebooks/{id}/kernel/stop | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/runs | write | notebooks | Run every SQL and Python cell of a markdown notebook, in document order, stopping at the first cell that does not finish. |
| GET | api/projects/{id}/notebooks/{id}/runs/{id} | read | notebooks | Read a whole-notebook run: its state, which cell it is on, and one line per planned cell. |
| POST | api/projects/{id}/notebooks/{id}/runs/{id}/interrupt | write | notebooks | Stop a whole-notebook run and the cell it is on. |
| GET | api/projects/{id}/notebooks/{id}/sharing | write | notebooks | notebooks_sharing_list. Kept out of read: returns share access tokens. |
| POST | api/projects/{id}/notebooks/{id}/sharing/passwords | write | notebooks | Create a new password for the sharing configuration. |
| DELETE | api/projects/{id}/notebooks/{id}/sharing/passwords/{id} | write | notebooks | Delete a password from the sharing configuration. |
| POST | api/projects/{id}/notebooks/{id}/sharing/refresh | write | notebooks | notebooks_sharing_refresh_create. |
| POST | api/projects/{id}/notebooks/{id}/sql_v2/run | write | notebooks | Dispatch an asynchronous run of a notebook SQL or Python cell. |
| GET | api/projects/{id}/notebooks/{id}/sql_v2/runs/{id} | read | notebooks | Read a run's durable state: its status, and — once done or interrupted — the result envelope (columns, first rows, stdout/stderr, media, error). |
| POST | api/projects/{id}/notebooks/{id}/sql_v2/runs/{id}/interrupt | write | notebooks | Stop a running cell. |
| GET | api/projects/{id}/notebooks/{id}/sql_v2/state | read | notebooks | The full notebook view for agents: title, document source (markdown, or raw content for legacy rich-text notebooks), the notebook's declared variables, every cell with its dependency edges and... |
| POST | api/projects/{id}/notebooks/{id}/widget_snapshots | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widget_snapshots/publish | write | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/widget_snapshots/{id} | read | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/widget_snapshots/{id}/frames/{id} | read | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/attach | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/cancel | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/fork | write | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/widgets/{id}/frames/{id} | read | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/generate | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/pin | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/publish | write | notebooks | The API for interacting with Notebooks. |
| POST | api/projects/{id}/notebooks/{id}/widgets/{id}/revert | write | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/widgets/{id}/source | read | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/widgets/{id}/status | read | notebooks | The API for interacting with Notebooks. |
| GET | api/projects/{id}/notebooks/{id}/widgets/{id}/versions | read | notebooks | The API for interacting with Notebooks. |
| GET | api/organizations | read | organizations | list. |
| POST | api/organizations | write | organizations | create. |
| GET | api/organizations/{id} | read | organizations | retrieve. |
| PUT | api/organizations/{id} | write | organizations | update. |
| PATCH | api/organizations/{id} | write | organizations | partial_update. |
| DELETE | api/organizations/{id} | write | organizations | destroy. |
| GET | api/organizations/{id}/advanced_activity_logs | read | organizations | Organization-wide view of activity logs across every project in the organization. |
| GET | api/organizations/{id}/advanced_activity_logs/available_filters | read | organizations | Organization-wide view of activity logs across every project in the organization. |
| POST | api/organizations/{id}/advanced_activity_logs/export | write | organizations | Organization-wide view of activity logs across every project in the organization. |
| GET | api/organizations/{id}/billing/features | read | organizations | Get the features the organization's plans include. |
| GET | api/organizations/{id}/billing/forecast | read | organizations | Get the forecast for the rest of the billing period. |
| GET | api/organizations/{id}/billing/invoices | read | organizations | List the organization's invoices. |
| GET | api/organizations/{id}/billing/invoices/{id}/content | read | organizations | Download an invoice as PDF. |
| GET | api/organizations/{id}/billing/limits | read | organizations | Get the organization's spend limits. |
| GET | api/organizations/{id}/billing/products | read | organizations | List the organization's products. |
| GET | api/organizations/{id}/billing/products/summary | read | organizations | Get every product in summary. |
| GET | api/organizations/{id}/billing/products/{id} | read | organizations | Get one product. |
| GET | api/organizations/{id}/billing/projects | read | organizations | List the projects with usage. |
| GET | api/organizations/{id}/billing/spend | read | organizations | Get spend so far this billing period. |
| GET | api/organizations/{id}/billing/spend/export | read | organizations | Export spend as CSV. |
| GET | api/organizations/{id}/billing/spend/timeseries | read | organizations | Spend over time. |
| GET | api/organizations/{id}/billing/subscription | read | organizations | Get the organization's subscription. |
| GET | api/organizations/{id}/billing/usage | read | organizations | Get usage so far this billing period. |
| GET | api/organizations/{id}/billing/usage/export | read | organizations | Export usage as CSV. |
| GET | api/organizations/{id}/billing/usage/status | read | organizations | Get usage against limits, without the counts. |
| GET | api/organizations/{id}/billing/usage/timeseries | read | organizations | Usage over time. |
| GET | api/organizations/{id}/context_layer/channel-pages/{id} | read | organizations | Resolve a channel's wiki page. |
| POST | api/organizations/{id}/context_layer/commits | write | organizations | Land agent commits from a git bundle. |
| GET | api/organizations/{id}/context_layer/dreams | read | organizations | List dream runs. |
| GET | api/organizations/{id}/context_layer/dreams/{id} | read | organizations | Read one dream run. |
| POST | api/organizations/{id}/context_layer/enable | write | organizations | Enable the context layer. |
| GET | api/organizations/{id}/context_layer/export | read | organizations | Export the wiki. |
| GET | api/organizations/{id}/context_layer/pages | read | organizations | Read a wiki page. |
| PUT | api/organizations/{id}/context_layer/pages | write | organizations | Create or replace a wiki page. |
| GET | api/organizations/{id}/context_layer/proposals | read | organizations | List your pending wiki edits. |
| POST | api/organizations/{id}/context_layer/proposals/{id}/apply | write | organizations | Apply a reviewed wiki edit. |
| GET | api/organizations/{id}/context_layer/status | read | organizations | Get the wiki head. |
| GET | api/organizations/{id}/context_layer/tree | read | organizations | List wiki pages. |
| GET | api/organizations/{id}/context_layer/wiki/report | read | organizations | Report wiki health findings. |
| GET | api/organizations/{id}/domains | read | organizations | domains_list. |
| POST | api/organizations/{id}/domains | write | organizations | domains_create. |
| GET | api/organizations/{id}/domains/{id} | read | organizations | domains_retrieve. |
| PUT | api/organizations/{id}/domains/{id} | write | organizations | domains_update. |
| PATCH | api/organizations/{id}/domains/{id} | write | organizations | domains_partial_update. |
| DELETE | api/organizations/{id}/domains/{id} | write | organizations | domains_destroy. |
| GET | api/organizations/{id}/domains/{id}/scim/logs | read | organizations | domains_scim_logs_retrieve. |
| POST | api/organizations/{id}/domains/{id}/verify | write | organizations | domains_verify_create. |
| GET | api/organizations/{id}/invites | read | organizations | invites_list. |
| POST | api/organizations/{id}/invites | write | organizations | invites_create. |
| POST | api/organizations/{id}/invites/bulk | write | organizations | invites_bulk_create. |
| POST | api/organizations/{id}/invites/delegate | write | organizations | Create an onboarding delegation invite: an admin-level invite flagged as a setup delegation. |
| DELETE | api/organizations/{id}/invites/{id} | write | organizations | invites_destroy. |
| GET | api/organizations/{id}/members | read | organizations | members_list. |
| GET | api/organizations/{id}/members/project_access | read | organizations | Every visible member's access to every project the caller can reach, with the rule behind it. |
| PUT | api/organizations/{id}/members/{id} | write | organizations | members_update. |
| PATCH | api/organizations/{id}/members/{id} | write | organizations | members_partial_update. |
| DELETE | api/organizations/{id}/members/{id} | write | organizations | members_destroy. |
| GET | api/organizations/{id}/members/{id}/github_login | read | organizations | members_github_login_retrieve. |
| GET | api/organizations/{id}/members/{id}/offboarding_preview | read | organizations | members_offboarding_preview_retrieve. |
| GET | api/organizations/{id}/members/{id}/scoped_api_keys | write | organizations | members_scoped_api_keys_retrieve. Kept out of read: lists a member's API keys. |
| GET | api/organizations/{id}/projects | read | organizations | Projects for the current organization. |
| POST | api/organizations/{id}/projects | write | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id} | write | organizations | Retrieve a project and its settings. Kept out of read: returns project secrets and tokens. |
| PUT | api/organizations/{id}/projects/{id} | write | organizations | Replace a project and its settings. |
| PATCH | api/organizations/{id}/projects/{id} | write | organizations | Update one or more of a project's settings. |
| DELETE | api/organizations/{id}/projects/{id} | write | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id}/access_control_default_objects | read | organizations | Object rules that apply to everyone in the project without a rule of their own on that object. |
| GET | api/organizations/{id}/projects/{id}/access_control_default_properties | read | organizations | Property rules that apply to everyone in the project without a rule of their own on that property. |
| GET | api/organizations/{id}/projects/{id}/access_control_defaults | read | organizations | The project's default access. |
| GET | api/organizations/{id}/projects/{id}/access_control_management | read | organizations | Whether Terraform manages this project's access rules. |
| PUT | api/organizations/{id}/projects/{id}/access_control_management | write | organizations | Enable or disable the Terraform lock. |
| GET | api/organizations/{id}/projects/{id}/access_control_member_objects | read | organizations | Object rules configured for a member: the single objects, for example a dashboard or a notebook, the member is granted or denied, regardless of the resource-level rules. |
| GET | api/organizations/{id}/projects/{id}/access_control_member_properties | read | organizations | Property rules configured for a member: the person and event properties the member can read, read and write, or not see. |
| GET | api/organizations/{id}/projects/{id}/access_control_members | read | organizations | Every organization member's access in this project. |
| GET | api/organizations/{id}/projects/{id}/access_control_role_objects | read | organizations | Object rules configured for a role: the single objects the role's members are granted or denied, regardless of the resource-level rules. |
| GET | api/organizations/{id}/projects/{id}/access_control_role_properties | read | organizations | Property rules configured for a role: the person and event properties the role's members can read, read and write, or not see. |
| GET | api/organizations/{id}/projects/{id}/access_control_roles | read | organizations | Every role's resolved access to this project and to each resource type in it: the role's own rule, the level that is enforced, and the rule the enforced level comes from. |
| GET | api/organizations/{id}/projects/{id}/activity | read | organizations | Projects for the current organization. |
| PATCH | api/organizations/{id}/projects/{id}/add_product_intent | write | organizations | Projects for the current organization. |
| POST | api/organizations/{id}/projects/{id}/cancel-deletion | write | organizations | Cancel a scheduled project deletion and restore access to the project. |
| POST | api/organizations/{id}/projects/{id}/change_organization | write | organizations | Projects for the current organization. |
| PATCH | api/organizations/{id}/projects/{id}/complete_product_onboarding | write | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id}/default_evaluation_contexts | read | organizations | Manage default evaluation contexts for a project. |
| POST | api/organizations/{id}/projects/{id}/default_evaluation_contexts | write | organizations | Manage default evaluation contexts for a project. |
| DELETE | api/organizations/{id}/projects/{id}/default_evaluation_contexts | write | organizations | Manage default evaluation contexts for a project. |
| GET | api/organizations/{id}/projects/{id}/default_release_conditions | read | organizations | Manage default release conditions for new feature flags in this project. |
| PUT | api/organizations/{id}/projects/{id}/default_release_conditions | write | organizations | Manage default release conditions for new feature flags in this project. |
| POST | api/organizations/{id}/projects/{id}/evaluation_context_suggestions | write | organizations | Hide an evaluation context name from the flag editor's suggestion list, or restore it. |
| DELETE | api/organizations/{id}/projects/{id}/evaluation_context_suggestions | write | organizations | Hide an evaluation context name from the flag editor's suggestion list, or restore it. |
| GET | api/organizations/{id}/projects/{id}/event_ingestion_restrictions | read | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id}/experiments_config | read | organizations | Manage experiment configuration for this project. |
| PATCH | api/organizations/{id}/projects/{id}/experiments_config | write | organizations | Manage experiment configuration for this project. |
| POST | api/organizations/{id}/projects/{id}/generate_conversations_public_token | write | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id}/is_generating_demo_data | read | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id}/logs_config | read | organizations | Manage logs product configuration for this project's canonical environment. |
| PATCH | api/organizations/{id}/projects/{id}/logs_config | write | organizations | Manage logs product configuration for this project's canonical environment. |
| PATCH | api/organizations/{id}/projects/{id}/reset_token | write | organizations | Projects for the current organization. |
| PATCH | api/organizations/{id}/projects/{id}/rotate_heatmaps_screenshot_secret | write | organizations | Projects for the current organization. |
| GET | api/organizations/{id}/projects/{id}/settings_as_of | read | organizations | Return the project settings as of the provided timestamp. |
| GET | api/organizations/{id}/projects/{id}/tracing_config | read | organizations | Manage tracing product configuration for this project's canonical environment. |
| PATCH | api/organizations/{id}/projects/{id}/tracing_config | write | organizations | Manage tracing product configuration for this project's canonical environment. |
| GET | api/organizations/{id}/roles | read | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| POST | api/organizations/{id}/roles | write | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| GET | api/organizations/{id}/roles/{id} | read | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| PUT | api/organizations/{id}/roles/{id} | write | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| PATCH | api/organizations/{id}/roles/{id} | write | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| DELETE | api/organizations/{id}/roles/{id} | write | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| GET | api/organizations/{id}/roles/{id}/role_memberships | read | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| POST | api/organizations/{id}/roles/{id}/role_memberships | write | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| GET | api/organizations/{id}/roles/{id}/role_memberships/{id} | read | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| DELETE | api/organizations/{id}/roles/{id}/role_memberships/{id} | write | organizations | Role endpoints disclose member records, so they scope them the same way the members list does when the org restricts member list visibility. |
| GET | api/organizations/{id}/teams/data_freshness | read | organizations | When each project in the organization last received data, broken down by kind of data. |
| GET | api/projects/{id}/persons | read | persons | This endpoint is meant for reading and deleting persons. |
| GET | api/projects/{id}/persons/activity | read | persons | This endpoint is meant for reading and deleting persons. |
| POST | api/projects/{id}/persons/batch_by_distinct_ids | write | persons | This endpoint is meant for reading and deleting persons. |
| POST | api/projects/{id}/persons/batch_by_uuids | write | persons | This endpoint is meant for reading and deleting persons. |
| POST | api/projects/{id}/persons/bulk_delete | write | persons | This endpoint allows you to bulk delete persons, either by the PostHog person IDs or by distinct IDs. |
| GET | api/projects/{id}/persons/cohorts | read | persons | This endpoint is meant for reading and deleting persons. |
| GET | api/projects/{id}/persons/deletion_status | read | persons | List the status of queued event deletions for persons. |
| GET | api/projects/{id}/persons/properties_at_time | read | persons | Get person properties as they existed at a specific point in time. |
| GET | api/projects/{id}/persons/values | read | persons | This endpoint is meant for reading and deleting persons. |
| GET | api/projects/{id}/persons/{id} | read | persons | This endpoint is meant for reading and deleting persons. |
| PUT | api/projects/{id}/persons/{id} | write | persons | Only for setting properties on the person. |
| PATCH | api/projects/{id}/persons/{id} | write | persons | This endpoint is meant for reading and deleting persons. |
| GET | api/projects/{id}/persons/{id}/activity | read | persons | This endpoint is meant for reading and deleting persons. |
| POST | api/projects/{id}/persons/{id}/delete_property | write | persons | This endpoint is meant for reading and deleting persons. |
| GET | api/projects/{id}/persons/{id}/emails | read | persons | This endpoint is meant for reading and deleting persons. |
| POST | api/projects/{id}/persons/{id}/properties_timeline | write | persons | Get a person's properties timeline for an insight data point. |
| GET | api/projects/{id}/persons/{id}/push_notifications | read | persons | This endpoint is meant for reading and deleting persons. |
| POST | api/projects/{id}/persons/{id}/split | write | persons | Split distinct_ids off a merged person. |
| POST | api/projects/{id}/persons/{id}/update_property | write | persons | This endpoint is meant for reading and deleting persons. |
| GET | api/projects/{id}/plugin_configs/{id}/logs | read | plugin_configs | plugin_configs_logs_list. |
| GET | api/projects/{id}/product_tours | read | product_tours | Create, read, update, and manage product tours and their targeting. |
| POST | api/projects/{id}/product_tours | write | product_tours | Create, read, update, and manage product tours and their targeting. |
| GET | api/projects/{id}/product_tours/{id} | read | product_tours | Create, read, update, and manage product tours and their targeting. |
| PUT | api/projects/{id}/product_tours/{id} | write | product_tours | Create, read, update, and manage product tours and their targeting. |
| PATCH | api/projects/{id}/product_tours/{id} | write | product_tours | Create, read, update, and manage product tours and their targeting. |
| DELETE | api/projects/{id}/product_tours/{id} | write | product_tours | Create, read, update, and manage product tours and their targeting. |
| DELETE | api/projects/{id}/product_tours/{id}/discard_draft | write | product_tours | Discard draft content. |
| PATCH | api/projects/{id}/product_tours/{id}/draft | write | product_tours | Save draft content (server-side merge). |
| GET | api/projects/{id}/product_tours/{id}/draft_status | read | product_tours | Lightweight polling endpoint for draft change detection. |
| POST | api/projects/{id}/product_tours/{id}/publish_draft | write | product_tours | Commit draft to live tour. |
| GET | api/projects/{id}/property_definitions | read | property_definitions | property_definitions_list. |
| POST | api/projects/{id}/property_definitions/bulk_update_tags | write | property_definitions | Bulk update tags on multiple objects. |
| GET | api/projects/{id}/property_definitions/seen_together | read | property_definitions | Allows a caller to provide a list of event names and a single property name Returns a map of the event names to a boolean representing whether that property has ever been seen with that event_name. |
| POST | api/projects/{id}/property_definitions/usage_metrics | write | property_definitions | 30-day query usage for a set of properties. |
| GET | api/projects/{id}/property_definitions/{id} | read | property_definitions | property_definitions_retrieve. |
| PUT | api/projects/{id}/property_definitions/{id} | write | property_definitions | property_definitions_update. |
| PATCH | api/projects/{id}/property_definitions/{id} | write | property_definitions | property_definitions_partial_update. |
| DELETE | api/projects/{id}/property_definitions/{id} | write | property_definitions | property_definitions_destroy. |
| POST | api/projects/{id}/query | read | query | query_create. |
| POST | api/projects/{id}/query/check_auth_for_async | write | query | query_check_auth_for_async_create. |
| GET | api/projects/{id}/query/draft_sql | read | query | query_draft_sql_retrieve. |
| GET | api/projects/{id}/query/scan/{id} | read | query | Get the query scan for a cache key: the analysis of the last slow run of that query. |
| POST | api/projects/{id}/query/upgrade | read | query | Upgrades a query without executing it. |
| GET | api/projects/{id}/query/{id} | read | query | (Experimental). |
| POST | api/projects/{id}/query/{id} | write | query | query_create_with_kind. |
| DELETE | api/projects/{id}/query/{id} | write | query | (Experimental). |
| GET | api/projects/{id}/query/{id}/log | read | query | Get query log details from query_log_archive table for a specific query_id, the query must have been issued in last 24 hours. |
| GET | api/projects/{id}/quota_limits | read | quota_limits | Get a team's quota-limit state. |
| GET | api/projects/{id}/releases | read | releases | List the releases of the project, oldest first. |
| POST | api/projects/{id}/releases | write | releases | Create a release. |
| GET | api/projects/{id}/releases/broadcast_search | read | releases | Search the broadcasts a release can link, returning only their ID, name and status. |
| GET | api/projects/{id}/releases/catalog_flags | read | releases | List the project's feature flags the caller can see, newest or oldest first, with only the fields a list shows. |
| GET | api/projects/{id}/releases/catalog_releases | read | releases | List the project's releases, newest or oldest first, with only the fields a list shows. |
| GET | api/projects/{id}/releases/flag_suggestions | read | releases | Find the releases a feature flag is in, and the existing releases it probably belongs to. |
| POST | api/projects/{id}/releases/import_all | write | releases | Set up releases for the whole project once: one per active flag. |
| GET | api/projects/{id}/releases/{id} | read | releases | Get one release with its linked flags, broadcasts, surveys and insights. |
| PATCH | api/projects/{id}/releases/{id} | write | releases | Change the name, description, owner or linked flags, broadcasts, surveys and insights of a release. |
| DELETE | api/projects/{id}/releases/{id} | write | releases | Delete a release. |
| POST | api/projects/{id}/releases/{id}/merge | write | releases | Merge other releases into this one. |
| GET | api/projects/{id}/saved | read | saved | List saved heatmaps for the project. |
| POST | api/projects/{id}/saved | write | saved | Create a saved heatmap for a page URL. |
| POST | api/projects/{id}/saved/capture | write | saved | Persist screenshots captured client-side by the on-page toolbar as a completed screenshot heatmap. |
| POST | api/projects/{id}/saved/preflight | write | saved | Check whether a page can back a heatmap. |
| POST | api/projects/{id}/saved/prewarm | write | saved | Speculatively render a screenshot for a page URL ahead of heatmap creation, so it's ready (or closer to ready) by the time the user reaches the generation screen. |
| GET | api/projects/{id}/saved/{id} | read | saved | Get a single saved heatmap by its short_id, including per-width render status. |
| PATCH | api/projects/{id}/saved/{id} | write | saved | Update a saved heatmap (e.g. |
| DELETE | api/projects/{id}/saved/{id} | write | saved | Hard delete of this model is not allowed. |
| POST | api/projects/{id}/saved/{id}/regenerate | write | saved | Re-run screenshot generation for a saved heatmap of type 'screenshot'. |
| GET | api/projects/{id}/saved/{id}/screenshot_history | read | saved | List the daily screenshot captures kept for a saved heatmap, newest first. |
| POST | api/projects/{id}/saved/{id}/screenshot_history/capture | write | saved | Render and keep a capture of the page now, instead of waiting for the daily run, for example right after a deploy. |
| GET | api/projects/{id}/saved/{id}/screenshot_history/requests/{id} | read | saved | Read the outcome of a capture request. |
| GET | api/projects/{id}/saved/{id}/screenshot_history/{id}/content | read | saved | Fetch the JPEG for one daily capture, or its thumbnail. |
| GET | api/projects/{id}/scheduled_changes | read | scheduled_changes | Create, read, update and delete scheduled changes. |
| POST | api/projects/{id}/scheduled_changes | write | scheduled_changes | Create, read, update and delete scheduled changes. |
| GET | api/projects/{id}/scheduled_changes/{id} | read | scheduled_changes | Create, read, update and delete scheduled changes. |
| PUT | api/projects/{id}/scheduled_changes/{id} | write | scheduled_changes | Create, read, update and delete scheduled changes. |
| PATCH | api/projects/{id}/scheduled_changes/{id} | write | scheduled_changes | Create, read, update and delete scheduled changes. |
| DELETE | api/projects/{id}/scheduled_changes/{id} | write | scheduled_changes | Create, read, update and delete scheduled changes. |
| GET | api/projects/{id}/schema_property_groups | read | schema_property_groups | schema_property_groups_list. |
| POST | api/projects/{id}/schema_property_groups | write | schema_property_groups | schema_property_groups_create. |
| GET | api/projects/{id}/schema_property_groups/{id} | read | schema_property_groups | schema_property_groups_retrieve. |
| PUT | api/projects/{id}/schema_property_groups/{id} | write | schema_property_groups | schema_property_groups_update. |
| PATCH | api/projects/{id}/schema_property_groups/{id} | write | schema_property_groups | schema_property_groups_partial_update. |
| DELETE | api/projects/{id}/schema_property_groups/{id} | write | schema_property_groups | schema_property_groups_destroy. |
| GET | api/projects/{id}/sdk_health/report | read | sdk_health | Get SDK health report for a project. |
| GET | api/projects/{id}/session_recording_playlists | read | session_recording_playlists | Override list to include synthetic playlists. |
| POST | api/projects/{id}/session_recording_playlists | write | session_recording_playlists | session_recording_playlists_create. |
| GET | api/projects/{id}/session_recording_playlists/{id} | read | session_recording_playlists | session_recording_playlists_retrieve. |
| PUT | api/projects/{id}/session_recording_playlists/{id} | write | session_recording_playlists | session_recording_playlists_update. |
| PATCH | api/projects/{id}/session_recording_playlists/{id} | write | session_recording_playlists | session_recording_playlists_partial_update. |
| DELETE | api/projects/{id}/session_recording_playlists/{id} | write | session_recording_playlists | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/session_recording_playlists/{id}/recordings | read | session_recording_playlists | session_recording_playlists_recordings_retrieve. |
| POST | api/projects/{id}/session_recording_playlists/{id}/recordings/{id} | write | session_recording_playlists | session_recording_playlists_recordings_create. |
| DELETE | api/projects/{id}/session_recording_playlists/{id}/recordings/{id} | write | session_recording_playlists | session_recording_playlists_recordings_destroy. |
| GET | api/projects/{id}/session_recordings | read | session_recordings | session_recordings_list. |
| POST | api/projects/{id}/session_recordings/bulk_delete | write | session_recordings | Delete a batch of session recordings by session ID. |
| GET | api/projects/{id}/session_recordings/{id} | read | session_recordings | session_recordings_retrieve. |
| PUT | api/projects/{id}/session_recordings/{id} | write | session_recordings | session_recordings_update. |
| PATCH | api/projects/{id}/session_recordings/{id} | write | session_recordings | session_recordings_partial_update. |
| DELETE | api/projects/{id}/session_recordings/{id} | write | session_recordings | session_recordings_destroy. |
| GET | api/projects/{id}/session_recordings/{id}/console_logs | read | session_recordings | List console logs of a session recording. |
| GET | api/projects/{id}/session_recordings/{id}/sharing | write | session_recordings | session_recordings_sharing_list. Kept out of read: returns share access tokens. |
| POST | api/projects/{id}/session_recordings/{id}/sharing/passwords | write | session_recordings | Create a new password for the sharing configuration. |
| DELETE | api/projects/{id}/session_recordings/{id}/sharing/passwords/{id} | write | session_recordings | Delete a password from the sharing configuration. |
| POST | api/projects/{id}/session_recordings/{id}/sharing/refresh | write | session_recordings | session_recordings_sharing_refresh_create. |
| GET | api/projects/{id}/sessions/property_definitions | read | sessions | sessions_property_definitions_retrieve. |
| GET | api/projects/{id}/sessions/values | read | sessions | sessions_values_retrieve. |
| GET | api/projects/{id}/subscriptions | read | subscriptions | subscriptions_list. |
| POST | api/projects/{id}/subscriptions | write | subscriptions | subscriptions_create. |
| GET | api/projects/{id}/subscriptions/summaries | read | subscriptions | List AI summaries for an insight or dashboard. |
| GET | api/projects/{id}/subscriptions/summary_quota | read | subscriptions | subscriptions_summary_quota_retrieve. |
| GET | api/projects/{id}/subscriptions/{id} | read | subscriptions | subscriptions_retrieve. |
| PUT | api/projects/{id}/subscriptions/{id} | write | subscriptions | subscriptions_update. |
| PATCH | api/projects/{id}/subscriptions/{id} | write | subscriptions | subscriptions_partial_update. |
| DELETE | api/projects/{id}/subscriptions/{id} | write | subscriptions | Hard delete of this model is not allowed. |
| GET | api/projects/{id}/subscriptions/{id}/deliveries | read | subscriptions | List subscription deliveries. |
| GET | api/projects/{id}/subscriptions/{id}/deliveries/{id} | read | subscriptions | Retrieve subscription delivery. |
| POST | api/projects/{id}/subscriptions/{id}/take_ownership | write | subscriptions | Take ownership of this subscription and enable it. |
| POST | api/projects/{id}/subscriptions/{id}/test-delivery | write | subscriptions | subscriptions_test_delivery_create. |
| GET | api/projects/{id}/surveys | read | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/surveys | write | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/projects/{id}/surveys/activity | read | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/projects/{id}/surveys/question_labels | read | surveys | Return a slim list of question labels for the team's surveys. |
| GET | api/projects/{id}/surveys/responses_count | read | surveys | Get response counts for all surveys. |
| GET | api/projects/{id}/surveys/stats | read | surveys | Get aggregated response statistics across all surveys. |
| GET | api/projects/{id}/surveys/{id} | read | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| PUT | api/projects/{id}/surveys/{id} | write | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| PATCH | api/projects/{id}/surveys/{id} | write | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| DELETE | api/projects/{id}/surveys/{id} | write | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/projects/{id}/surveys/{id}/activity | read | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/projects/{id}/surveys/{id}/archived-response-uuids | read | surveys | Get list of archived response UUIDs for HogQL filtering. |
| POST | api/projects/{id}/surveys/{id}/duplicate_to_projects | write | surveys | Duplicate a survey to multiple projects in a single transaction. |
| POST | api/projects/{id}/surveys/{id}/generate_translations | write | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| POST | api/projects/{id}/surveys/{id}/launch | write | surveys | Launch a survey by setting `start_date` to the current time. |
| GET | api/projects/{id}/surveys/{id}/responses | read | surveys | List survey responses for a specific survey, with question text resolved server-side so callers do not have to map opaque `$survey_response_` keys. |
| POST | api/projects/{id}/surveys/{id}/responses/{id}/archive | write | surveys | Archive a single survey response. |
| POST | api/projects/{id}/surveys/{id}/responses/{id}/unarchive | write | surveys | Unarchive a single survey response. |
| GET | api/projects/{id}/surveys/{id}/site_snapshot | read | surveys | Get a site snapshot for the draft preview. |
| GET | api/projects/{id}/surveys/{id}/stats | read | surveys | Get survey response statistics for a specific survey. |
| POST | api/projects/{id}/surveys/{id}/stop | write | surveys | Stop a survey by setting `end_date` to the current time. |
| POST | api/projects/{id}/surveys/{id}/summarize_responses | write | surveys | Summarize survey responses. |
| POST | api/projects/{id}/surveys/{id}/summary_headline | write | surveys | Mixin for ViewSets to handle approval-gate exceptions raised from decorated serializers. |
| GET | api/users | read | users | users_list. |
| GET | api/users/{id} | read | users | Retrieve a user's profile and settings. |
| PUT | api/users/{id} | write | users | Replace the authenticated user's profile and settings. |
| PATCH | api/users/{id} | write | users | Update one or more of the authenticated user's profile fields or settings. |
| DELETE | api/users/{id} | write | users | users_destroy. |
| GET | api/projects/{id}/warehouse_saved_queries | read | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/warehouse_saved_queries | write | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/warehouse_saved_queries/check_incremental | write | warehouse_saved_queries | Report whether a query can be materialized incrementally, without running it. |
| POST | api/projects/{id}/warehouse_saved_queries/resume_schedules | write | warehouse_saved_queries | Resume materialization for several models that were suspended after repeated failures. |
| GET | api/projects/{id}/warehouse_saved_queries/{id} | read | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| PUT | api/projects/{id}/warehouse_saved_queries/{id} | write | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| PATCH | api/projects/{id}/warehouse_saved_queries/{id} | write | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| DELETE | api/projects/{id}/warehouse_saved_queries/{id} | write | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| GET | api/projects/{id}/warehouse_saved_queries/{id}/activity | read | warehouse_saved_queries | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/ancestors | write | warehouse_saved_queries | Return the ancestors of this saved query. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/cancel | write | warehouse_saved_queries | Cancel a running saved query workflow. |
| GET | api/projects/{id}/warehouse_saved_queries/{id}/dependencies | read | warehouse_saved_queries | Return the count of immediate upstream and downstream dependencies for this saved query. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/descendants | write | warehouse_saved_queries | Return the descendants of this saved query. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/materialize | write | warehouse_saved_queries | Enable materialization for this saved query, at the requested sync frequency or daily. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/resume | write | warehouse_saved_queries | Resume materialization suspended after repeated failures. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/revert_materialization | write | warehouse_saved_queries | Undo materialization, revert back to the original view. |
| POST | api/projects/{id}/warehouse_saved_queries/{id}/run | write | warehouse_saved_queries | Run this saved query. |
| GET | api/projects/{id}/warehouse_saved_queries/{id}/run_history | read | warehouse_saved_queries | Return the recent run history (up to 5 most recent) for this materialized view. |
| GET | api/projects/{id}/warehouse_tables | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. Kept out of read: returns warehouse access credentials. |
| POST | api/projects/{id}/warehouse_tables | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/warehouse_tables/create_from_upload | write | warehouse_tables | Create a warehouse table and FileUpload source from an uploaded file. |
| POST | api/projects/{id}/warehouse_tables/file | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/warehouse_tables/upload_file | write | warehouse_tables | Upload a file for a new warehouse table and FileUpload source. |
| GET | api/projects/{id}/warehouse_tables/{id} | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. Kept out of read: returns warehouse access credentials. |
| PUT | api/projects/{id}/warehouse_tables/{id} | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. |
| PATCH | api/projects/{id}/warehouse_tables/{id} | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. |
| DELETE | api/projects/{id}/warehouse_tables/{id} | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/warehouse_tables/{id}/copy_access_rules_to_history_table | write | warehouse_tables | Copy the table's access rules to its history table. |
| GET | api/projects/{id}/warehouse_tables/{id}/history_table | read | warehouse_tables | Get the table's history table. |
| POST | api/projects/{id}/warehouse_tables/{id}/refresh_schema | write | warehouse_tables | Refresh table schema from source. |
| POST | api/projects/{id}/warehouse_tables/{id}/replace_file | write | warehouse_tables | Replace the file of a table made from an uploaded file. |
| POST | api/projects/{id}/warehouse_tables/{id}/update_schema | write | warehouse_tables | Create, Read, Update and Delete Warehouse Tables. |
| POST | api/projects/{id}/web_analytics/llms_txt | write | web_analytics | Load an llms.txt file. |
| GET | api/projects/{id}/web_analytics/recap | read | web_analytics | Weekly web analytics recap. |
| GET | api/projects/{id}/web_analytics/weekly_digest | read | web_analytics | Summarize web analytics. |
| GET | api/projects/{id}/web_experiments | read | web_experiments | web_experiments_list. |
| POST | api/projects/{id}/web_experiments | write | web_experiments | web_experiments_create. |
| GET | api/projects/{id}/web_experiments/{id} | read | web_experiments | web_experiments_retrieve. |
| PUT | api/projects/{id}/web_experiments/{id} | write | web_experiments | web_experiments_update. |
| PATCH | api/projects/{id}/web_experiments/{id} | write | web_experiments | web_experiments_partial_update. |
| DELETE | api/projects/{id}/web_experiments/{id} | write | web_experiments | web_experiments_destroy. |
| GET | api/projects/{id}/web_vitals | read | web_vitals | Get web vitals for a specific pathname. |
