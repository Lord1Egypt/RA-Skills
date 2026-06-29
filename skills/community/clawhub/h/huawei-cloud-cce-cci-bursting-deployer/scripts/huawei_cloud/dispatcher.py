"""CLI dispatch helpers for modular Huawei Cloud actions."""

from __future__ import annotations

from typing import Any, Callable, Dict

import json

from . import aom, apm, cce, cce_metrics, ecs, elb, hss, identity, network, storage
from . import cce_inspection
from . import cce_diagnosis
from . import pod_diagnosis
from . import workload_rollout_diagnosis
from . import cce_auto_inspection
from . import chart_generator
from . import common
from . import cce_cluster, cce_nodepool, cce_node, cce_addon, cce_k8s, cce_hpa, cce_cost_optimization, cce_availability_risk, cce_capacity_trend, cce_cci_bursting, cce_pressure_test, cce_apm, ops_report_generator
from . import node_failure_diagnosis, network_failure_diagnosis, storage_failure_diagnosis, autoscaling_diagnosis, change_impact_analysis
from . import dependency_impact_analysis, root_cause_analysis, auto_remediation
from . import cce_events_lts
from . import cce_cluster_monitoring

# cce_app_logs and lts require huaweicloudsdklts which may not be installed
try:
    from . import cce_app_logs as _cce_app_logs_mod
    from . import lts as _lts_mod
    cce_app_logs = _cce_app_logs_mod
    lts = _lts_mod
    _lts_available = True
except ImportError:
    _lts_available = False
    _cce_app_logs_mod = None
    _lts_mod = None


Handler = Callable[[Dict[str, str]], Dict[str, Any]]


def _require(params: Dict[str, str], *keys: str) -> str | None:
    missing = [key for key in keys if not params.get(key)]
    if missing:
        return f"{', '.join(missing)} are required" if len(missing) > 1 else f"{missing[0]} is required"
    return None


def _to_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _to_optional_int(value: str | None) -> int | None:
    if value is None or value.strip().lower() in {"", "none", "null"}:
        return None
    return _to_int(value, 0)


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "y", "on"}


def _to_float(value: str | None, default: float) -> float:
    try:
        return float(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _to_optional_bool(value: str | None) -> bool | None:
    if value is None or value.strip().lower() in {"", "none", "null"}:
        return None
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    return None


def _parse_json_param(value: str | None) -> Any:
    if not value:
        return None
    return json.loads(value)


def _hpa_cpu_target(params: Dict[str, str]) -> int | None:
    if "target_cpu_utilization" not in params:
        return 60
    return _to_optional_int(params.get("target_cpu_utilization"))


def _list_ecs(params: Dict[str, str]) -> Dict[str, Any]:
    return ecs.list_ecs_instances(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _get_ecs_metrics(params: Dict[str, str]) -> Dict[str, Any]:
    return ecs.get_ecs_metrics(params["region"], params["instance_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_flavors(params: Dict[str, str]) -> Dict[str, Any]:
    return ecs.list_ecs_flavors(params["region"], params.get("az"), params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _list_vpc(params: Dict[str, str]) -> Dict[str, Any]:
    return network.list_vpc_networks(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _list_vpc_subnets(params: Dict[str, str]) -> Dict[str, Any]:
    return network.list_vpc_subnets(params["region"], params.get("vpc_id"), params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _list_security_groups(params: Dict[str, str]) -> Dict[str, Any]:
    return network.list_security_groups(params["region"], params.get("vpc_id"), params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _list_vpc_acls(params: Dict[str, str]) -> Dict[str, Any]:
    return network.list_vpc_acls(params["region"], params.get("vpc_id"), params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_eip(params: Dict[str, str]) -> Dict[str, Any]:
    return network.list_eip_addresses(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100))


def _get_eip_metrics(params: Dict[str, str]) -> Dict[str, Any]:
    return network.get_eip_metrics(params["region"], params["eip_id"], _to_int(params.get("hours"), 1), _to_int(params.get("period"), 300), params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_nat(params: Dict[str, str]) -> Dict[str, Any]:
    return network.list_nat_gateways(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0), params.get("id"), params.get("name"), params.get("description"), params.get("spec"), params.get("router_id"), params.get("internal_network_id"), params.get("status"), None if params.get("admin_state_up") is None else params.get("admin_state_up", "").lower() == "true", params.get("created_at"))


def _get_nat_metrics(params: Dict[str, str]) -> Dict[str, Any]:
    return network.get_nat_gateway_metrics(params["region"], params["nat_gateway_id"], _to_int(params.get("hours"), 1), _to_int(params.get("period"), 300), params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_evs(params: Dict[str, str]) -> Dict[str, Any]:
    return storage.list_evs_volumes(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0), params.get("volume_type"), params.get("availability_zone"))


def _get_evs_metrics(params: Dict[str, str]) -> Dict[str, Any]:
    return storage.get_evs_metrics(params["region"], params["volume_id"], params["instance_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_sfs(params: Dict[str, str]) -> Dict[str, Any]:
    return storage.list_sfs(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _list_sfs_turbo(params: Dict[str, str]) -> Dict[str, Any]:
    return storage.list_sfs_turbo(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _list_elb(params: Dict[str, str]) -> Dict[str, Any]:
    return elb.list_elb_loadbalancers(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), params.get("marker"))


def _create_elb(params: Dict[str, str]) -> Dict[str, Any]:
    return elb.create_elb_loadbalancer(
        region=params["region"],
        name=params["name"],
        vip_subnet_cidr_id=params["vip_subnet_cidr_id"],
        vpc_id=params.get("vpc_id"),
        availability_zone_list=params.get("availability_zone_list"),
        l4_flavor_id=params.get("l4_flavor_id"),
        l7_flavor_id=params.get("l7_flavor_id"),
        elb_virsubnet_ids=params.get("elb_virsubnet_ids"),
        description=params.get("description"),
        provider=params.get("provider"),
        guaranteed=_to_optional_bool(params.get("guaranteed")),
        deletion_protection_enable=params.get("deletion_protection_enable", "true").lower() == "true",
        ip_target_enable=_to_optional_bool(params.get("ip_target_enable")),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _list_elb_listeners(params: Dict[str, str]) -> Dict[str, Any]:
    return elb.list_elb_listeners(params["region"], params.get("loadbalancer_id"), params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100))


def _get_elb_metrics(params: Dict[str, str]) -> Dict[str, Any]:
    return elb.get_elb_metrics(params["region"], params["elb_id"], _to_int(params.get("hours"), 1), _to_int(params.get("period"), 300), params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_elb_backend_status(params: Dict[str, str]) -> Dict[str, Any]:
    return elb.get_elb_backend_status(params["region"], params["elb_id"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 200))


def _list_projects(params: Dict[str, str]) -> Dict[str, Any]:
    return identity.list_projects(params.get("ak"), params.get("sk"), params.get("domain_id"), params.get("region"))


def _get_project_by_region(params: Dict[str, str]) -> Dict[str, Any]:
    return identity.get_project_by_region(params["region"], params.get("ak"), params.get("sk"))


def _list_cce_clusters(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_clusters(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _delete_cce_cluster(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.delete_cce_cluster(params["region"], params["cluster_id"], params.get("confirm", "").lower() == "true", params.get("delete_evs", "").lower() == "true", params.get("delete_net", "").lower() == "true", params.get("delete_obs", "").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_cce_nodes(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_cluster_nodes(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _get_cce_nodes(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_cce_nodes(params["region"], params["cluster_id"], params.get("node_name"), params.get("ak"), params.get("sk"), params.get("project_id"))


def _delete_cce_node(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.delete_cce_node(params["region"], params["cluster_id"], params["node_id"], params.get("confirm", "").lower() == "true", params.get("scale_down", "true").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_cce_nodepools(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_node_pools(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0))


def _get_cce_kubeconfig(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_cce_kubeconfig(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("duration"), 30))


def _list_cce_addons(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_addons(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_cce_addon_detail(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_cce_addon_detail(params["region"], params["cluster_id"], params["addon_name"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _resize_cce_nodepool(params: Dict[str, str]) -> Dict[str, Any]:
    scale_group_names = None
    if params.get("scale_group_names"):
        scale_group_names = [name.strip() for name in params["scale_group_names"].split(",") if name.strip()]
    return cce.resize_node_pool(params["region"], params["cluster_id"], params["nodepool_id"], int(params["node_count"]), params.get("confirm", "").lower() == "true", scale_group_names, params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_cce_pods(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_pods(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"), params.get("labels"))


def _get_pod_logs(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_pod_logs(
        params["region"],
        params["cluster_id"],
        params["pod_name"],
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
        params.get("namespace", "default"),
        params.get("container"),
        params.get("previous", "false").lower() == "true",
        _to_int(params.get("tail_lines"), 100)
    )


def _get_cce_namespaces(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_namespaces(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_cce_deployments(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_deployments(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"))


def _scale_cce_workload(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.scale_cce_workload(params["region"], params["cluster_id"], params["workload_type"], params["name"], params["namespace"], int(params["replicas"]), params.get("confirm", "").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _resize_cce_workload(params: Dict[str, str]) -> Dict[str, Any]:
    replicas = int(params["replicas"]) if params.get("replicas") else None
    return cce.resize_cce_workload(
        params["region"], params["cluster_id"], params["workload_type"], params["name"], params["namespace"],
        replicas=replicas,
        cpu_limit=params.get("cpu_limit"),
        memory_limit=params.get("memory_limit"),
        cpu_request=params.get("cpu_request"),
        memory_request=params.get("memory_request"),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id")
    )


def _delete_cce_workload(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.delete_cce_workload(params["region"], params["cluster_id"], params["workload_type"], params["name"], params["namespace"], params.get("confirm", "").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_kubernetes_nodes(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_nodes(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_cce_events(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_events(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"), _to_int(params.get("limit"), 500))


def _query_k8s_events_from_lts(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_events_lts.query_k8s_events_from_lts_action(params)


def _cce_cluster_monitoring_aggregation(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cluster_monitoring.cce_cluster_monitoring_aggregation_action(params)


def _get_cce_pvcs(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_pvcs(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"))


def _get_cce_pvs(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_pvs(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_cce_services(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_services(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"))


def _get_cce_ingresses(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.get_kubernetes_ingresses(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"))


def _list_cce_configmaps(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_configmaps(params["region"], params["cluster_id"], params.get("namespace"), _to_int(params.get("limit"), 100), _to_int(params.get("offset"), 0), params.get("include_data", "false").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_cce_secrets(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_secrets(params["region"], params["cluster_id"], params.get("namespace"), _to_int(params.get("limit"), 100), params.get("include_data", "false").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_cce_daemonsets(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_daemonsets(params["region"], params["cluster_id"], params.get("namespace"), _to_int(params.get("limit"), 100), params.get("include_data", "false").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_cce_statefulsets(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_statefulsets(params["region"], params["cluster_id"], params.get("namespace"), _to_int(params.get("limit"), 100), params.get("include_data", "false").lower() == "true", params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_aom_instances(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.list_aom_instances(
        params["region"],
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
        params.get("prom_type"),
        params.get("enterprise_project_id"),
    )


def _resolve_cce_aom_instance(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_diagnosis.get_aom_instance(
        params["region"],
        params["cluster_id"],
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _get_apm_master_address(params: Dict[str, str]) -> Dict[str, Any]:
    return apm.get_apm_master_address(
        params["region"],
        params.get("auth_token"),
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _get_aom_metrics(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.get_aom_prom_metrics_http(params["region"], params["aom_instance_id"], params["query"], None if params.get("start") is None else int(params["start"]), None if params.get("end") is None else int(params["end"]), _to_int(params.get("step"), 60), _to_int(params.get("hours"), 1), params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_aom_alarm_rules(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.list_aom_alarm_rules(
        params["region"],
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
        _to_int(params.get("limit"), 100),
        _to_int(params.get("offset"), 0),
        params.get("enterprise_project_id"),
    )


def _alarm_rule_fields(params: Dict[str, str], json_key: str) -> Dict[str, Any]:
    fields = _parse_json_param(params.get(json_key)) or {}
    for key in (
        "action_enabled",
        "alarm_actions",
        "alarm_advice",
        "alarm_description",
        "alarm_level",
        "comparison_operator",
        "dimensions",
        "evaluation_periods",
        "is_turn_on",
        "insufficient_data_actions",
        "metric_name",
        "namespace",
        "ok_actions",
        "period",
        "statistic",
        "threshold",
        "unit",
    ):
        if key in params:
            value: Any = params[key]
            if key in {"alarm_actions", "dimensions", "insufficient_data_actions", "ok_actions"}:
                value = _parse_json_param(value)
            elif key in {"action_enabled", "is_turn_on"}:
                value = value.lower() == "true"
            elif key in {"alarm_level", "evaluation_periods", "period"}:
                value = _to_int(value, 0)
            fields[key] = value
    return fields


def _create_aom_alarm_rule(params: Dict[str, str]) -> Dict[str, Any]:
    fields = _alarm_rule_fields(params, "fields")
    return aom.create_aom_alarm_rule(
        region=params["region"],
        rule_name=params["rule_name"],
        metric_name=params["metric_name"],
        namespace=params["namespace"],
        comparison_operator=params["comparison_operator"],
        threshold=params["threshold"],
        period=_to_int(params["period"], 0),
        evaluation_periods=_to_int(params["evaluation_periods"], 0),
        statistic=params["statistic"],
        alarm_level=_to_int(params["alarm_level"], 0),
        create_fields=fields,
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _create_aom_event_alarm_rule(params: Dict[str, str]) -> Dict[str, Any]:
    bind_notification_rule_id = (
        params.get("bind_notification_rule_id")
        or params.get("notification_rule_name")
    )
    return aom.create_aom_event_alarm_rule(
        region=params["region"],
        cluster_id=params["cluster_id"],
        rule_name=params["rule_name"],
        event_name=params["event_name"],
        bind_notification_rule_id=bind_notification_rule_id,
        event_label=params.get("event_label"),
        alarm_level=params.get("alarm_level", "Major"),
        description=params.get("description"),
        alias=params.get("alias"),
        trigger_type=params.get("trigger_type", "immediately"),
        frequency=params.get("frequency", "-1"),
        prom_instance_id=params.get("prom_instance_id"),
        enterprise_project_id=params.get("enterprise_project_id"),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _update_aom_alarm_rule(params: Dict[str, str]) -> Dict[str, Any]:
    updates = _alarm_rule_fields(params, "updates")
    return aom.update_aom_alarm_rule(
        params["region"],
        params["rule_name"],
        updates,
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _delete_aom_alarm_rule(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.delete_aom_alarm_rule(
        params["region"],
        params["rule_name"],
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _disable_aom_alarm_rule(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.disable_aom_alarm_rule(
        params["region"],
        params["rule_id"],
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _enable_aom_alarm_rule(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.enable_aom_alarm_rule(
        params["region"],
        params["rule_id"],
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _list_aom_action_rules(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.list_aom_action_rules(
        params["region"],
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
        params.get("enterprise_project_id"),
    )


def _delete_aom_action_rule(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.delete_aom_action_rule(
        params["region"],
        params["rule_name"],
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _list_aom_mute_rules(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.list_aom_mute_rules(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_aom_current_alarms(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.list_aom_current_alarms(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("event_type", "active_alert"), params.get("event_severity"), params.get("time_range"), _to_int(params.get("limit"), 100), params.get("cluster_id"))


def _list_aom_alarms(params: Dict[str, str]) -> Dict[str, Any]:
    return aom.list_aom_alarms(
        region=params["region"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        hours=_to_int(params.get("hours"), 1),
        event_severity=params.get("event_severity"),
        cluster_id=params.get("cluster_id"),
        cluster_name=params.get("cluster_name"),
        limit=_to_int(params.get("limit"), 500),
    )


def _list_log_groups(params: Dict[str, str]) -> Dict[str, Any]:
    return _lts_mod.list_log_groups(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))


def _list_log_streams(params: Dict[str, str]) -> Dict[str, Any]:
    return _lts_mod.list_log_streams(params["region"], params.get("log_group_id"), params.get("ak"), params.get("sk"), params.get("project_id"))


def _query_logs(params: Dict[str, str]) -> Dict[str, Any]:
    labels = _parse_json_param(params.get("labels"))
    return _lts_mod.query_logs(params["region"], params["log_group_id"], params["log_stream_id"], params.get("start_time"), params.get("end_time"), params.get("keywords"), _to_int(params.get("limit"), 1000), params.get("scroll_id"), params.get("is_desc", "true").lower() == "true", params.get("is_iterative", "false").lower() == "true", labels, params.get("ak"), params.get("sk"), params.get("project_id"))


def _get_recent_logs(params: Dict[str, str]) -> Dict[str, Any]:
    labels = _parse_json_param(params.get("labels"))
    return _lts_mod.get_recent_logs(params["region"], params["log_group_id"], params["log_stream_id"], _to_int(params.get("hours"), 1), _to_int(params.get("limit"), 1000), params.get("keywords"), labels, params.get("ak"), params.get("sk"), params.get("project_id"))


def _query_aom_logs(params: Dict[str, str]) -> Dict[str, Any]:
    return _lts_mod.query_aom_logs(params["region"], params["cluster_id"], params.get("namespace"), params.get("pod_name"), params.get("container_name"), params.get("start_time"), params.get("end_time"), params.get("keywords"), _to_int(params.get("limit"), 100), params.get("ak"), params.get("sk"), params.get("project_id"))


def _inspection_action(handler: Callable[[Dict[str, str]], Dict[str, Any]], params: Dict[str, str]) -> Dict[str, Any]:
    return handler(params)


def _metric_action(handler: Callable[..., Dict[str, Any]], *args: Any, **kwargs: Any) -> Dict[str, Any]:
    return handler(*args, **kwargs)



def _inspection_check_action(fn, params):
    """通用巡检action封装：直接调用fn并返回 {success, check, issues}"""
    check, issues = fn(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    return {"success": True, "check": check, "issues": issues}


def _addon_pod_inspection_action(params):
    aom_id = cce_inspection._get_aom_instance(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))
    cluster_name = cce_inspection._get_cluster_name(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    all_pods_map = cce_inspection._get_all_pods_map(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    check, issues = cce_inspection.addon_pod_monitoring_inspection(
        params["region"], params["cluster_id"], aom_id, cluster_name,
        params.get("ak"), params.get("sk"), params.get("project_id"), all_pods_map
    )
    return {"success": True, "check": check, "issues": issues}


def _biz_pod_inspection_action(params):
    aom_id = cce_inspection._get_aom_instance(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))
    cluster_name = cce_inspection._get_cluster_name(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    all_pods_map = cce_inspection._get_all_pods_map(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    all_namespaces = cce_inspection._get_all_namespaces(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    check, issues = cce_inspection.biz_pod_monitoring_inspection(
        params["region"], params["cluster_id"], aom_id, cluster_name,
        params.get("ak"), params.get("sk"), params.get("project_id"), all_pods_map, all_namespaces
    )
    return {"success": True, "check": check, "issues": issues}


def _node_resource_inspection_action(params):
    aom_id = cce_inspection._get_aom_instance(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))
    cluster_name = cce_inspection._get_cluster_name(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    check, issues = cce_inspection.node_resource_monitoring_inspection(
        params["region"], params["cluster_id"], aom_id, cluster_name,
        params.get("ak"), params.get("sk"), params.get("project_id")
    )
    return {"success": True, "check": check, "issues": issues}


def _aom_alarm_inspection_action(params):
    cluster_name = cce_inspection._get_cluster_name(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    check, issues = cce_inspection.aom_alarm_inspection(
        params["region"], params["cluster_id"], cluster_name,
        params.get("ak"), params.get("sk"), params.get("project_id")
    )
    return {"success": True, "check": check, "issues": issues}


def _elb_monitoring_inspection_action(params):
    aom_id = cce_inspection._get_aom_instance(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))
    cluster_name = cce_inspection._get_cluster_name(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))
    check, issues = cce_inspection.elb_monitoring_inspection(
        params["region"], params["cluster_id"], aom_id, cluster_name,
        params.get("ak"), params.get("sk"), params.get("project_id")
    )
    return {"success": True, "check": check, "issues": issues}


def _aggregate_results_action(params):
    try:
        return cce_inspection.aggregate_subagent_results(json.loads(params["results"]), json.loads(params["cluster_info"]))
    except Exception as exc:
        return {"success": False, "error": str(exc)}



# ---- Diagnosis action helpers (inlined from diagnosis_actions.py) ----

def _network_diagnose_action(params):
    try:
        return cce_diagnosis.network_diagnose(
            params["region"], params["cluster_id"],
            params.get("workload_name"), params.get("namespace", "default"),
            params.get("ak"), params.get("sk"), params.get("project_id")
        )
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "stage": "huawei_network_diagnose"}


def _network_diagnose_by_alarm_action(params):
    return cce_diagnosis.network_diagnose_by_alarm(
        params["region"], params["cluster_id"], params["alarm_info"],
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _network_verify_pod_scheduling_action(params):
    return cce_diagnosis.verify_pod_scheduling_after_scale(
        params["region"], params["cluster_id"], params["workload_name"],
        params.get("namespace", "default"),
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _network_failure_diagnose_action(params):
    return network_failure_diagnosis.diagnose_network_failure_action(params)


def _storage_failure_diagnose_action(params):
    return storage_failure_diagnosis.diagnose_storage_failure_action(params)


def _node_batch_diagnose_action(params):
    node_ips = [ip.strip() for ip in params.get("node_ips", "").split(",") if ip.strip()] or None
    return cce_diagnosis.batch_node_diagnose(
        params["region"], params["cluster_id"], node_ips,
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _node_diagnose_action(params):
    import re
    from .common import get_credentials_with_region
    from .cce import get_kubernetes_nodes
    from .cce_metrics import get_cce_node_metrics

    region = params["region"]
    cluster_id = params["cluster_id"]
    ak = params.get("ak")
    sk = params.get("sk")
    project_id = params.get("project_id")
    node_ip = params.get("node_ip")
    node_name = params.get("node_name")

    if not node_ip and node_name:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        if "." in node_name and all(part.isdigit() for part in node_name.split(".") if part):
            node_ip = node_name

        if not node_ip:
            k8s_result = get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id)
            if k8s_result.get("success"):
                for node in k8s_result.get("nodes", []):
                    if node_name == node.get("name", "") or node_name == node.get("internal_ip", ""):
                        node_ip = node.get("internal_ip", "")
                        break

        if not node_ip:
            k8s_result = get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id) if not k8s_result.get("success") else k8s_result
            if not k8s_result.get("success"):
                return {"success": False, "error": "Cannot find node and failed to get kubernetes nodes"}

            return {
                "success": False,
                "error": f"Cannot automatically convert CCE node name '{node_name}' to IP.",
                "note": "CCE node names cannot be automatically resolved to IPs via API.",
                "hint": "Use node_ip parameter instead.",
                "available_k8s_ips": [n.get("internal_ip") for n in k8s_result.get("nodes", [])],
            }

    if not node_ip:
        return {"success": False, "error": "node_ip or node_name is required"}

    cluster_name = cce_diagnosis.get_cluster_name(region, cluster_id, ak, sk, project_id)
    diagnose_result = cce_diagnosis.diagnose_single_node(node_ip, region, cluster_id, ak, sk, project_id)
    if isinstance(diagnose_result, dict) and "success" in diagnose_result:
        return diagnose_result
    return {"success": True, "region": region, "action": "node_diagnose", "cluster_id": cluster_id, "node_ip": node_ip, "result": diagnose_result}


def _flatten_diagnosis_result(raw):
    """workload_diagnose 返回 {success, diagnosis, report}，展平 diagnosis 到顶层"""
    if not raw.get("success"):
        return raw
    diag = raw.get("diagnosis", {})
    report = raw.get("report", {})
    flat = dict(diag)
    flat["success"] = True
    flat["report"] = report
    return flat


def _workload_diagnose_action(params):
    try:
        raw = cce_diagnosis.workload_diagnose(
            params["region"], params["cluster_id"],
            params.get("workload_name"), params.get("namespace", "default"),
            params.get("ak"), params.get("sk"), params.get("project_id"),
            params.get("fault_time"),
            int(params.get("hours", 6))
        )
        return _flatten_diagnosis_result(raw)
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "stage": "workload_diagnose"}


def _workload_diagnose_by_alarm_action(params):
    try:
        raw = cce_diagnosis.workload_diagnose_by_alarm(
            params["region"], params["cluster_id"], params["alarm_info"],
            params.get("ak"), params.get("sk"), params.get("project_id"),
            int(params.get("hours", 6))
        )
        return _flatten_diagnosis_result(raw)
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "stage": "workload_diagnose_by_alarm"}


def _pod_failure_diagnose_action(params):
    try:
        return pod_diagnosis.pod_failure_diagnose(
            region=params["region"],
            cluster_id=params["cluster_id"],
            namespace=params.get("namespace"),
            pod_name=params.get("pod_name"),
            workload_name=params.get("workload_name"),
            labels=params.get("labels"),
            include_logs=params.get("include_logs", "true").lower() != "false",
            include_metrics=params.get("include_metrics", "false").lower() == "true",
            tail_lines=_to_int(params.get("tail_lines"), 80),
            hours=_to_int(params.get("hours"), 1),
            max_pods=_to_int(params.get("max_pods"), 20),
            event_limit=_to_int(params.get("event_limit"), 500),
            ak=params.get("ak"),
            sk=params.get("sk"),
            project_id=params.get("project_id"),
        )
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "stage": "pod_failure_diagnose"}


def _get_workload_rollout_context_action(params):
    try:
        return workload_rollout_diagnosis.get_workload_rollout_context(
            region=params["region"],
            cluster_id=params["cluster_id"],
            namespace=params["namespace"],
            kind=params["kind"],
            name=params["name"],
            event_limit=_to_int(params.get("event_limit"), 500),
            label_selector=params.get("label_selector"),
            ak=params.get("ak"),
            sk=params.get("sk"),
            project_id=params.get("project_id"),
        )
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "stage": "get_workload_rollout_context"}


def _workload_rollout_diagnose_action(params):
    try:
        return workload_rollout_diagnosis.workload_rollout_diagnose(
            region=params["region"],
            cluster_id=params["cluster_id"],
            namespace=params["namespace"],
            kind=params["kind"],
            name=params["name"],
            include_pod_diagnosis=params.get("include_pod_diagnosis", "true").lower() != "false",
            include_logs=params.get("include_logs", "true").lower() != "false",
            include_metrics=params.get("include_metrics", "false").lower() == "true",
            tail_lines=_to_int(params.get("tail_lines"), 80),
            hours=_to_int(params.get("hours"), 1),
            max_pods=_to_int(params.get("max_pods"), 20),
            event_limit=_to_int(params.get("event_limit"), 500),
            label_selector=params.get("label_selector"),
            ak=params.get("ak"),
            sk=params.get("sk"),
            project_id=params.get("project_id"),
        )
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "stage": "workload_rollout_diagnose"}


def _hibernate_cce_cluster_action(params):
    if params.get("confirm", "").lower() == "true":
        return cce.hibernate_cce_cluster(
            region=params["region"], cluster_id=params["cluster_id"],
            ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"),
            confirm=True
        )
    return cce.hibernate_cce_cluster(
        params["region"], params["cluster_id"],
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _awake_cce_cluster_action(params):
    if params.get("confirm", "").lower() == "true":
        return cce.awake_cce_cluster(
            region=params["region"], cluster_id=params["cluster_id"],
            ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"),
            confirm=True
        )
    return cce.awake_cce_cluster(
        params["region"], params["cluster_id"],
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _stop_ecs_instance_action(params):
    return ecs.stop_ecs_instance(
        params["region"], params["instance_id"],
        params.get("stop_type", "SOFT"),
        params.get("ak"), params.get("sk"), params.get("project_id"),
        params.get("confirm", "false").lower() == "true"
    )


def _start_ecs_instance_action(params):
    return ecs.start_ecs_instance(
        params["region"], params["instance_id"],
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _list_cce_cronjobs(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.list_cce_cronjobs(
        params["region"], params["cluster_id"],
        params.get("namespace"),
        params.get("ak"), params.get("sk"), params.get("project_id")
    )


def _list_cce_hpas(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_hpa.list_cce_hpas(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        namespace=params.get("namespace"),
        include_system=params.get("include_system", "false").lower() == "true",
    )


def _generate_cce_hpa_manifest(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_hpa.generate_cce_hpa_manifest(
        workload_name=params["workload_name"],
        namespace=params["namespace"],
        min_replicas=_to_int(params["min_replicas"], 1),
        max_replicas=_to_int(params["max_replicas"], 1),
        workload_type=params.get("workload_type", "deployment"),
        hpa_name=params.get("hpa_name"),
        target_cpu_utilization=_hpa_cpu_target(params),
        target_memory_utilization=_to_optional_int(params.get("target_memory_utilization")),
        behavior=_parse_json_param(params.get("behavior")),
        output_file=params.get("output_file"),
    )


def _configure_cce_hpa(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_hpa.configure_cce_hpa(
        region=params["region"],
        cluster_id=params["cluster_id"],
        workload_name=params["workload_name"],
        namespace=params["namespace"],
        min_replicas=_to_int(params["min_replicas"], 1),
        max_replicas=_to_int(params["max_replicas"], 1),
        workload_type=params.get("workload_type", "deployment"),
        hpa_name=params.get("hpa_name"),
        target_cpu_utilization=_hpa_cpu_target(params),
        target_memory_utilization=_to_optional_int(params.get("target_memory_utilization")),
        behavior=_parse_json_param(params.get("behavior")),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _analyze_cce_cost_optimization(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cost_optimization.analyze_cce_cost_optimization(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        short_hours=_to_int(params.get("short_hours"), 24),
        long_hours=_to_int(params.get("long_hours"), 168),
        top_n=_to_int(params.get("top_n"), 50),
        exclude_namespaces=params.get("exclude_namespaces"),
        business_namespaces=params.get("business_namespaces"),
        output_dir=params.get("output_dir"),
        include_raw=params.get("include_raw", "false").lower() == "true",
        hpa_workload_name=params.get("hpa_workload_name"),
        hpa_namespace=params.get("hpa_namespace"),
        hpa_workload_type=params.get("hpa_workload_type", "deployment"),
        hpa_min_replicas=_to_int(params.get("hpa_min_replicas"), 1),
        hpa_max_replicas=_to_int(params.get("hpa_max_replicas"), 3),
        hpa_target_cpu_utilization=_to_optional_int(params.get("hpa_target_cpu_utilization"))
        if "hpa_target_cpu_utilization" in params
        else 60,
        hpa_target_memory_utilization=_to_optional_int(params.get("hpa_target_memory_utilization")),
    )


def _scan_cce_availability_risk(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_availability_risk.scan_cce_availability_risk(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        exclude_namespaces=params.get("exclude_namespaces"),
        gateway_keywords=params.get("gateway_keywords"),
        metrics_hours=_to_int(params.get("metrics_hours"), 24),
        limit=_to_int(params.get("limit"), 500),
        cpu_limit_request_ratio=float(params.get("cpu_limit_request_ratio", 4.0)),
        memory_limit_request_ratio=float(params.get("memory_limit_request_ratio", 2.0)),
        output_dir=params.get("output_dir"),
        include_raw=params.get("include_raw", "false").lower() == "true",
    )


def _analyze_cce_capacity_trend(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_capacity_trend.analyze_cce_capacity_trend(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        hours=_to_int(params.get("hours"), 168),
        step_seconds=_to_int(params.get("step_seconds"), 3600),
        top_n=_to_int(params.get("top_n"), 200),
        exclude_namespaces=params.get("exclude_namespaces"),
        business_namespaces=params.get("business_namespaces"),
        output_dir=params.get("output_dir"),
        history_dir=params.get("history_dir"),
        record_history=params.get("record_history", "true").lower() == "true",
        compare_history_count=_to_int(params.get("compare_history_count"), 8),
        include_raw=params.get("include_raw", "false").lower() == "true",
        target_cpu_percent=float(params.get("target_cpu_percent", 60.0)),
        target_memory_percent=float(params.get("target_memory_percent", 70.0)),
        bottleneck_percent=float(params.get("bottleneck_percent", 80.0)),
        headroom_percent=float(params.get("headroom_percent", 15.0)),
        action_note=params.get("action_note"),
    )


def _generate_ops_report(params: Dict[str, str]) -> Dict[str, Any]:
    return ops_report_generator.generate_ops_report(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        report_type=params.get("report_type", "weekly"),
        hours=_to_optional_int(params.get("hours")),
        short_hours=_to_optional_int(params.get("short_hours")),
        long_hours=_to_optional_int(params.get("long_hours")),
        step_seconds=_to_int(params.get("step_seconds"), 3600),
        top_n=_to_int(params.get("top_n"), 200),
        exclude_namespaces=params.get("exclude_namespaces"),
        business_namespaces=params.get("business_namespaces"),
        gateway_keywords=params.get("gateway_keywords"),
        output_dir=params.get("output_dir"),
        include_raw=params.get("include_raw", "false").lower() == "true",
        oncall_report_path=params.get("oncall_report_path"),
        oncall_summary=params.get("oncall_summary"),
    )


def _autoscaling_diagnose(params: Dict[str, str]) -> Dict[str, Any]:
    return autoscaling_diagnosis.diagnose_cce_autoscaling(
        region=params["region"],
        cluster_id=params["cluster_id"],
        question=params.get("question", ""),
        target=params.get("target"),
        scale_direction=params.get("scale_direction"),
        namespace=params.get("namespace"),
        workload_name=params.get("workload_name"),
        workload_type=params.get("workload_type"),
        include_metrics=_to_bool(params.get("include_metrics"), True),
        include_raw=_to_bool(params.get("include_raw"), False),
        hours=_to_int(params.get("hours"), 1),
        event_limit=_to_int(params.get("event_limit"), 500),
        top_n=_to_int(params.get("top_n"), 20),
        tolerance=_to_float(params.get("tolerance"), 0.1),
        output_file=params.get("output_file"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _change_impact_analyze(params: Dict[str, str]) -> Dict[str, Any]:
    return change_impact_analysis.analyze_change_impact_action(params)


# ---- HSS handlers ----
def _hss_list_vul_host_hosts(params: Dict[str, str]) -> Dict[str, Any]:
    return hss.list_vul_host_hosts(region=params["region"], ak=params.get("ak"), sk=params.get("sk"))

def _hss_list_host_vuls_all(params: Dict[str, str]) -> Dict[str, Any]:
    return hss.list_host_vuls_all(
        region=params["region"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        host_id=params.get("host_id"),
        host_name=params.get("host_name"),
        status=params.get("status"),
        repair_priority=params.get("repair_priority"),
        severity_level=params.get("severity_level"),
        limit=int(params.get("limit", 100)),
        enterprise_project_id=params.get("enterprise_project_id", "all_granted_eps"),
    )

def _hss_change_vul_status(params: Dict[str, str]) -> Dict[str, Any]:
    return hss.change_vul_status(
        region=params["region"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        operate_type=params["operate_type"],
        vul_ids=params.get("vul_ids"),
        host_ids=params.get("host_ids"),
        vul_type=params.get("vul_type", "linux_vul"),
        remark=params.get("remark"),
        select_type=params.get("select_type"),
        confirm=params.get("confirm", "").lower() == "true",
        enterprise_project_id=params.get("enterprise_project_id", "all_granted_eps"),
    )


def _cce_node_cordon(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.cce_node_cordon(
        region=params["region"], cluster_id=params["cluster_id"], node_name=params["node_name"],
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))

def _cce_node_uncordon(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.cce_node_uncordon(
        region=params["region"], cluster_id=params["cluster_id"], node_name=params["node_name"],
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))

def _cce_node_drain(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.cce_node_drain(
        region=params["region"], cluster_id=params["cluster_id"], node_name=params["node_name"],
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))

def _cce_node_status(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.cce_node_status(
        region=params["region"], cluster_id=params["cluster_id"], node_name=params["node_name"],
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))

def _bind_cce_cluster_eip(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.bind_cce_cluster_eip(
        region=params["region"], cluster_id=params["cluster_id"], eip_id=params["eip_id"],
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))


def _unbind_cce_cluster_eip(params: Dict[str, str]) -> Dict[str, Any]:
    return cce.unbind_cce_cluster_eip(
        region=params["region"], cluster_id=params["cluster_id"],
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))


def _generate_monitor_dashboard(params: Dict[str, str]) -> Dict[str, Any]:
    extra_promql = None
    if params.get("extra_promql"):
        try:
            extra_promql = json.loads(params["extra_promql"])
        except (json.JSONDecodeError, TypeError):
            extra_promql = None
    return chart_generator.generate_monitor_dashboard(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        namespace=params.get("namespace"),
        label_selector=params.get("label_selector"),
        hours=_to_int(params.get("hours"), 1),
        include_network=params.get("include_network", "true").lower() != "false",
        top_n=_to_int(params.get("top_n"), 10),
        output_file=params.get("output_file"),
        title=params.get("title"),
        tz_offset_hours=_to_int(params.get("tz_offset_hours"), 8),
        inline_js=params.get("inline_js", "true").lower() != "false",
        extra_promql=extra_promql,
    )


def _generate_diagnosis_report(params: Dict[str, str]) -> Dict[str, Any]:
    """Dispatch wrapper for generate_diagnosis_report."""
    return chart_generator.generate_diagnosis_report(
        region=params["region"],
        cluster_id=params["cluster_id"],
        workload_name=params["workload_name"],
        namespace=params.get("namespace", "default"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        fault_time=params.get("fault_time"),
        hours=_to_int(params.get("hours"), 1),
        output_file=params.get("output_file"),
    )


def _analyze_aom_alarms(params: Dict[str, str]) -> Dict[str, Any]:
    """Dispatch wrapper for analyze_aom_alarms."""
    return aom.analyze_aom_alarms(
        region=params["region"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        cluster_id=params.get("cluster_id"),
        cluster_name=params.get("cluster_name"),
        hours=_to_int(params.get("hours"), 1),
        chronic_threshold=_to_int(params.get("chronic_threshold"), 5),
        sudden_window_minutes=_to_int(params.get("sudden_window_minutes"), 10),
    )


def _cce_quick_check_action(params: Dict[str, str]) -> Dict[str, Any]:
    """快检：3 个 API，< 30s，判断是否有异常"""
    # Parse optional thresholds
    thresholds = None
    if params.get("thresholds"):
        try:
            thresholds = json.loads(params["thresholds"])
        except (json.JSONDecodeError, TypeError):
            pass

    # Parse optional elb_ids
    elb_ids = None
    if params.get("elb_ids"):
        elb_ids = [e.strip() for e in params["elb_ids"].split(",") if e.strip()]

    return cce_auto_inspection.cce_quick_check(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        thresholds=thresholds,
        elb_ids=elb_ids,
    )


def _cce_deep_diagnosis_action(params: Dict[str, str]) -> Dict[str, Any]:
    """深度诊断：快检发现异常后调用，6+ 个 API 全链路诊断"""
    quick_check_result = None
    if params.get("quick_check_result"):
        try:
            quick_check_result = json.loads(params["quick_check_result"])
        except (json.JSONDecodeError, TypeError):
            pass

    return cce_auto_inspection.cce_deep_diagnosis(
        region=params["region"],
        cluster_id=params["cluster_id"],
        quick_check_result=quick_check_result,
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        notify_email=params.get("notify_email"),
        report_file=params.get("report_file"),
    )


def _cce_auto_inspection_action(params: Dict[str, str]) -> Dict[str, Any]:
    """自动巡检：快检 + 判断 + (诊断 | HEARTBEAT_OK) 一步到位"""
    thresholds = None
    if params.get("thresholds"):
        try:
            thresholds = json.loads(params["thresholds"])
        except (json.JSONDecodeError, TypeError):
            pass

    elb_ids = None
    if params.get("elb_ids"):
        elb_ids = [e.strip() for e in params["elb_ids"].split(",") if e.strip()]

    return cce_auto_inspection.cce_auto_inspection(
        region=params["region"],
        cluster_id=params["cluster_id"],
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        thresholds=thresholds,
        elb_ids=elb_ids,
        notify_email=params.get("notify_email"),
    )


def _reboot_ecs(params: Dict[str, str]) -> Dict[str, Any]:
    return ecs.reboot_ecs_instance(
        region=params["region"], instance_id=params["instance_id"],
        reboot_type=params.get("reboot_type", "SOFT"),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"), sk=params.get("sk"), project_id=params.get("project_id"))


def _create_cce_cluster(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cluster.create_cce_cluster(
        region=params["region"],
        cluster_name=params["cluster_name"],
        vpc_id=params["vpc_id"],
        subnet_id=params["subnet_id"],
        cluster_version=params.get("cluster_version"),
        cluster_type=params.get("cluster_type", "VirtualMachine"),
        container_network_type=params.get("container_network_type", "overlay_l2"),
        container_network_cidr=params.get("container_network_cidr"),
        service_network_cidr=params.get("service_network_cidr"),
        flavor_id=params.get("flavor_id"),
        description=params.get("description"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _create_cce_nodepool(params: Dict[str, str]) -> Dict[str, Any]:
    data_volumes = _parse_json_param(params.get("data_volumes"))
    autoscaling_enabled = params.get("autoscaling_enabled", "false").lower() == "true"
    return cce_nodepool.create_node_pool(
        region=params["region"],
        cluster_id=params["cluster_id"],
        nodepool_name=params["nodepool_name"],
        flavor=params["flavor"],
        availability_zone=params["availability_zone"],
        root_volume_size=int(params["root_volume_size"]),
        root_volume_type=params["root_volume_type"],
        initial_node_count=_to_int(params.get("initial_node_count"), 1),
        os_type=params.get("os_type", "EulerOS"),
        ssh_key=params.get("ssh_key"),
        data_volumes=data_volumes,
        subnet_id=params.get("subnet_id"),
        autoscaling_enabled=autoscaling_enabled,
        min_node_count=_to_int(params.get("min_node_count"), 0) if autoscaling_enabled else None,
        max_node_count=_to_int(params.get("max_node_count"), 0) if autoscaling_enabled else None,
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _delete_cce_nodepool(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_nodepool.delete_node_pool(
        region=params["region"],
        cluster_id=params["cluster_id"],
        nodepool_id=params["nodepool_id"],
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _create_cce_node(params: Dict[str, str]) -> Dict[str, Any]:
    data_volumes = _parse_json_param(params.get("data_volumes"))
    return cce_node.create_cce_node(
        region=params["region"],
        cluster_id=params["cluster_id"],
        flavor=params["flavor"],
        availability_zone=params["availability_zone"],
        root_volume_size=int(params["root_volume_size"]),
        root_volume_type=params["root_volume_type"],
        node_count=_to_int(params.get("node_count"), 1),
        os_type=params.get("os_type"),
        ssh_key=params.get("ssh_key"),
        data_volumes=data_volumes,
        subnet_id=params.get("subnet_id"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _install_cce_addon(params: Dict[str, str]) -> Dict[str, Any]:
    values = _parse_json_param(params.get("values"))
    return cce_addon.install_cce_addon(
        region=params["region"],
        cluster_id=params["cluster_id"],
        addon_template_name=params["addon_template_name"],
        addon_version=params.get("addon_version"),
        values=values,
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _uninstall_cce_addon(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_addon.uninstall_cce_addon(
        region=params["region"],
        cluster_id=params["cluster_id"],
        addon_id=params["addon_id"],
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _update_cce_addon(params: Dict[str, str]) -> Dict[str, Any]:
    values = _parse_json_param(params.get("values"))
    return cce_addon.update_cce_addon(
        region=params["region"],
        cluster_id=params["cluster_id"],
        addon_id=params["addon_id"],
        addon_version=params.get("addon_version"),
        values=values,
        addon_template_name=params.get("addon_template_name"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _configure_cce_bursting_addon(params: Dict[str, str]) -> Dict[str, Any]:
    subnets = None
    if params.get("subnets"):
        subnets = [item.strip() for item in params["subnets"].split(",") if item.strip()]

    return cce_addon.configure_cce_bursting_addon(
        region=params["region"],
        cluster_id=params["cluster_id"],
        subnet_id=params["subnet_id"],
        subnets=subnets,
        addon_id=params.get("addon_id", "virtual-kubelet"),
        addon_version=params.get("addon_version"),
        enable_schedule_profile_local_surge=_to_optional_bool(params.get("enable_schedule_profile_local_surge")),
        is_install_proxy=_to_optional_bool(params.get("is_install_proxy")),
        enable_log_collection=_to_optional_bool(params.get("enable_log_collection")),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _csv_param(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _precheck_cce_cci_bursting(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cci_bursting.precheck_cce_cci_bursting(
        region=params["region"],
        cluster_id=params["cluster_id"],
        vpcep_subnet_id=params.get("vpcep_subnet_id"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _ensure_cce_cci_vpcep(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cci_bursting.ensure_cce_cci_vpcep(
        region=params["region"],
        cluster_id=params["cluster_id"],
        vpcep_subnet_id=params.get("vpcep_subnet_id"),
        obs_endpoint_service_name=params.get("obs_endpoint_service_name"),
        route_table_ids=_csv_param(params.get("route_table_ids")),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _setup_cce_cci_bursting(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cci_bursting.setup_cce_cci_bursting(
        region=params["region"],
        cluster_id=params["cluster_id"],
        vpcep_subnet_id=params.get("vpcep_subnet_id"),
        cci_subnet_id=params.get("cci_subnet_id"),
        obs_endpoint_service_name=params.get("obs_endpoint_service_name"),
        route_table_ids=_csv_param(params.get("route_table_ids")),
        addon_version=params.get("addon_version"),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _deploy_cce_cci_smoke_workload(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cci_bursting.deploy_cce_cci_smoke_workload(
        region=params["region"],
        cluster_id=params["cluster_id"],
        namespace=params.get("namespace", cce_cci_bursting.DEFAULT_SMOKE_NAMESPACE),
        workload_name=params.get("workload_name", cce_cci_bursting.DEFAULT_SMOKE_WORKLOAD),
        image=params.get("image"),
        replicas=_to_int(params.get("replicas"), 2),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _verify_cce_cci_bursting(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_cci_bursting.verify_cce_cci_bursting(
        region=params["region"],
        cluster_id=params["cluster_id"],
        namespace=params.get("namespace"),
        workload_name=params.get("workload_name"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _prepare_cce_pressure_test_route(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_pressure_test.prepare_cce_pressure_test_route(
        params["region"],
        params["cluster_id"],
        params["namespace"],
        params["workload_name"],
        _to_int(params.get("service_port"), 80),
        _to_int(params.get("target_port"), 8080),
        params.get("service_name"),
        params.get("ingress_name"),
        params.get("ingress_class_name", "nginx"),
        params.get("host"),
        params.get("path", "/"),
        params.get("selector_json"),
        params.get("annotations_json"),
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _deploy_cce_pressure_test_java_sample(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_pressure_test.deploy_cce_pressure_test_java_sample(
        params["region"],
        params["cluster_id"],
        params.get("namespace", cce_pressure_test.DEFAULT_JAVA_NAMESPACE),
        params.get("workload_name", cce_pressure_test.DEFAULT_JAVA_WORKLOAD),
        params.get("image", cce_pressure_test.DEFAULT_JAVA_IMAGE),
        _to_int(params.get("replicas"), 2),
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _generate_cce_pressure_test_client(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_pressure_test.generate_cce_pressure_test_client(
        params["target_url"],
        params.get("namespace", cce_pressure_test.DEFAULT_NAMESPACE),
        params.get("test_name"),
        params.get("model", "keepalive"),
        _to_int(params.get("vus"), 10),
        _to_int(params.get("duration_seconds"), 60),
        params.get("image", cce_pressure_test.DEFAULT_K6_IMAGE),
        params.get("host_header"),
        float(params.get("sleep_seconds", 0.1)),
    )


def _run_cce_pressure_test(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_pressure_test.run_cce_pressure_test(
        params["region"],
        params["cluster_id"],
        params["target_url"],
        params.get("namespace", cce_pressure_test.DEFAULT_NAMESPACE),
        params.get("workload_name"),
        params.get("workload_namespace"),
        params.get("test_name"),
        params.get("model", "keepalive"),
        _to_int(params.get("vus"), 10),
        _to_int(params.get("duration_seconds"), 60),
        params.get("image", cce_pressure_test.DEFAULT_K6_IMAGE),
        params.get("host_header"),
        float(params.get("sleep_seconds", 0.1)),
        _to_int(params.get("sample_interval_seconds"), 5),
        _to_optional_int(params.get("timeout_seconds")),
        params.get("wait", "true").lower() == "true",
        params.get("output_dir"),
        params.get("confirm", "").lower() == "true",
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _collect_cce_pressure_test_observability(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_pressure_test.collect_cce_pressure_test_observability(
        params["region"],
        params["cluster_id"],
        params["namespace"],
        params["workload_name"],
        params.get("label_selector"),
        params.get("elb_id"),
        params.get("aom_instance_id"),
        params.get("queries_json"),
        _to_int(params.get("hours"), 1),
        _to_int(params.get("period"), 300),
        params.get("output_dir"),
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )


def _generate_cce_pressure_test_report(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_pressure_test.generate_cce_pressure_test_report(
        params["result_path"],
        params.get("observations_path"),
        params.get("output_dir"),
    )


def _inject_cce_apm_javaagent(params: Dict[str, str]) -> Dict[str, Any]:
    return cce_apm.inject_cce_apm_javaagent(
        region=params["region"],
        cluster_id=params["cluster_id"],
        namespace=params["namespace"],
        workload_name=params["workload_name"],
        app_name=params["app_name"],
        business=params["business"],
        env_name=params["env_name"],
        workload_type=params.get("workload_type", "deployment"),
        container_name=params.get("container_name"),
        master_address=params.get("master_address"),
        monitor_group=params.get("monitor_group", cce_apm.DEFAULT_MONITOR_GROUP),
        agent_version=params.get("agent_version", cce_apm.DEFAULT_AGENT_VERSION),
        swr_address=params.get("swr_address"),
        secret_name=params.get("secret_name"),
        apm_access_key=params.get("apm_access_key"),
        apm_secret_key=params.get("apm_secret_key"),
        auth_token=params.get("auth_token"),
        confirm=params.get("confirm", "").lower() == "true",
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


ACTION_SPECS: Dict[str, tuple[tuple[str, ...], Handler]] = {
    "huawei_list_ecs": (("region",), _list_ecs),
    "huawei_get_ecs_metrics": (("region", "instance_id"), _get_ecs_metrics),
    "huawei_list_flavors": (("region",), _list_flavors),
    "huawei_stop_ecs_instance": (("region", "instance_id"), _stop_ecs_instance_action),
    "huawei_start_ecs_instance": (("region", "instance_id"), _start_ecs_instance_action),
    "huawei_list_vpc": (("region",), _list_vpc),
    "huawei_list_vpc_subnets": (("region",), _list_vpc_subnets),
    "huawei_list_security_groups": (("region",), _list_security_groups),
    "huawei_list_vpc_acls": (("region",), _list_vpc_acls),
    "huawei_list_eip": (("region",), _list_eip),
    "huawei_get_eip_metrics": (("region", "eip_id"), _get_eip_metrics),
    "huawei_list_nat": (("region",), _list_nat),
    "huawei_get_nat_gateway_metrics": (("region", "nat_gateway_id"), _get_nat_metrics),
    "huawei_list_evs": (("region",), _list_evs),
    "huawei_get_evs_metrics": (("region", "volume_id", "instance_id"), _get_evs_metrics),
    "huawei_list_sfs": (("region",), _list_sfs),
    "huawei_list_sfs_turbo": (("region",), _list_sfs_turbo),
    "huawei_list_elb": (("region",), _list_elb),
    "huawei_create_elb": (("region", "name", "vip_subnet_cidr_id"), _create_elb),
    "huawei_list_elb_listeners": (("region",), _list_elb_listeners),
    "huawei_get_elb_metrics": (("region", "elb_id"), _get_elb_metrics),
    "huawei_get_elb_backend_status": (("region", "elb_id"), _get_elb_backend_status),
    "huawei_list_supported_regions": ((), lambda params: identity.list_supported_regions()),
    "huawei_list_projects": ((), _list_projects),
    "huawei_get_project_by_region": (("region",), _get_project_by_region),
    "huawei_list_cce_clusters": (("region",), _list_cce_clusters),
    "huawei_create_cce_cluster": (("region", "cluster_name", "vpc_id", "subnet_id"), _create_cce_cluster),
    "huawei_delete_cce_cluster": (("region", "cluster_id"), _delete_cce_cluster),
    "huawei_list_cce_nodes": (("region", "cluster_id"), _list_cce_nodes),
    "huawei_get_cce_nodes": (("region", "cluster_id"), _get_cce_nodes),
    "huawei_delete_cce_node": (("region", "cluster_id", "node_id"), _delete_cce_node),
    "huawei_list_cce_nodepools": (("region", "cluster_id"), _list_cce_nodepools),
    "huawei_get_cce_kubeconfig": (("region", "cluster_id"), _get_cce_kubeconfig),
    "huawei_list_cce_addons": (("region", "cluster_id"), _list_cce_addons),
    "huawei_get_cce_addon_detail": (("region", "cluster_id", "addon_name"), _get_cce_addon_detail),
    "huawei_resize_cce_nodepool": (("region", "cluster_id", "nodepool_id", "node_count"), _resize_cce_nodepool),
    "huawei_create_cce_nodepool": (("region", "cluster_id", "nodepool_name", "flavor", "availability_zone", "root_volume_size", "root_volume_type"), _create_cce_nodepool),
    "huawei_delete_cce_nodepool": (("region", "cluster_id", "nodepool_id"), _delete_cce_nodepool),
    "huawei_create_cce_node": (("region", "cluster_id", "flavor", "availability_zone", "root_volume_size", "root_volume_type"), _create_cce_node),
    "huawei_install_cce_addon": (("region", "cluster_id", "addon_template_name"), _install_cce_addon),
    "huawei_uninstall_cce_addon": (("region", "cluster_id", "addon_id"), _uninstall_cce_addon),
    "huawei_update_cce_addon": (("region", "cluster_id", "addon_id"), _update_cce_addon),
    "huawei_configure_cce_bursting_addon": (("region", "cluster_id", "subnet_id"), _configure_cce_bursting_addon),
    "huawei_precheck_cce_cci_bursting": (("region", "cluster_id"), _precheck_cce_cci_bursting),
    "huawei_ensure_cce_cci_vpcep": (("region", "cluster_id"), _ensure_cce_cci_vpcep),
    "huawei_setup_cce_cci_bursting": (("region", "cluster_id"), _setup_cce_cci_bursting),
    "huawei_deploy_cce_cci_smoke_workload": (("region", "cluster_id"), _deploy_cce_cci_smoke_workload),
    "huawei_verify_cce_cci_bursting": (("region", "cluster_id"), _verify_cce_cci_bursting),
    "huawei_deploy_cce_pressure_test_java_sample": (("region", "cluster_id"), _deploy_cce_pressure_test_java_sample),
    "huawei_prepare_cce_pressure_test_route": (("region", "cluster_id", "namespace", "workload_name"), _prepare_cce_pressure_test_route),
    "huawei_generate_cce_pressure_test_client": (("target_url",), _generate_cce_pressure_test_client),
    "huawei_run_cce_pressure_test": (("region", "cluster_id", "target_url"), _run_cce_pressure_test),
    "huawei_collect_cce_pressure_test_observability": (("region", "cluster_id", "namespace", "workload_name"), _collect_cce_pressure_test_observability),
    "huawei_generate_cce_pressure_test_report": (("result_path",), _generate_cce_pressure_test_report),
    "huawei_inject_cce_apm_javaagent": (("region", "cluster_id", "namespace", "workload_name", "app_name", "business", "env_name"), _inject_cce_apm_javaagent),
    "huawei_get_cce_pods": (("region", "cluster_id"), _get_cce_pods),
    "huawei_pod_failure_diagnose": (("region", "cluster_id"), _pod_failure_diagnose_action),
    "huawei_get_workload_rollout_context": (("region", "cluster_id", "namespace", "kind", "name"), _get_workload_rollout_context_action),
    "huawei_workload_rollout_diagnose": (("region", "cluster_id", "namespace", "kind", "name"), _workload_rollout_diagnose_action),
    "huawei_get_pod_logs": (("region", "cluster_id", "pod_name"), _get_pod_logs),
    "huawei_get_cce_namespaces": (("region", "cluster_id"), _get_cce_namespaces),
    "huawei_get_cce_deployments": (("region", "cluster_id"), _get_cce_deployments),
    "huawei_scale_cce_workload": (("region", "cluster_id", "workload_type", "name", "namespace", "replicas"), _scale_cce_workload),
    "huawei_resize_cce_workload": (("region", "cluster_id", "workload_type", "name", "namespace"), _resize_cce_workload),
    "huawei_delete_cce_workload": (("region", "cluster_id", "workload_type", "name", "namespace"), _delete_cce_workload),
    "huawei_get_kubernetes_nodes": (("region", "cluster_id"), _get_kubernetes_nodes),
    "huawei_get_cce_events": (("region", "cluster_id"), _get_cce_events),
    "huawei_query_k8s_events_from_lts": (("region", "cluster_id", "start_time", "end_time"), _query_k8s_events_from_lts),  # limit is optional
    "huawei_cce_cluster_monitoring_aggregation": (("region", "cluster_id", "start_time", "end_time"), _cce_cluster_monitoring_aggregation),  # namespace, top_n are optional
    "huawei_get_cce_pvcs": (("region", "cluster_id"), _get_cce_pvcs),
    "huawei_get_cce_pvs": (("region", "cluster_id"), _get_cce_pvs),
    "huawei_get_cce_storageclasses": (("region", "cluster_id"), lambda params: storage_failure_diagnosis.list_storage_classes_action(params)),
    "huawei_get_cce_volumeattachments": (("region", "cluster_id"), lambda params: storage_failure_diagnosis.list_volume_attachments_action(params)),
    "huawei_get_cce_node_stats_summary": (("region", "cluster_id"), lambda params: storage_failure_diagnosis.get_node_stats_summary_action(params)),
    "huawei_get_cce_everest_csi_logs": (("region", "cluster_id"), lambda params: storage_failure_diagnosis.get_everest_csi_logs_action(params)),
    "huawei_get_cce_services": (("region", "cluster_id"), _get_cce_services),
    "huawei_get_cce_ingresses": (("region", "cluster_id"), _get_cce_ingresses),
    "huawei_list_cce_configmaps": (("region", "cluster_id"), _list_cce_configmaps),
    "huawei_list_cce_secrets": (("region", "cluster_id"), _list_cce_secrets),
    "huawei_list_cce_daemonsets": (("region", "cluster_id"), _list_cce_daemonsets),
    "huawei_list_cce_statefulsets": (("region", "cluster_id"), _list_cce_statefulsets),
    "huawei_list_cce_cronjobs": (("region", "cluster_id"), _list_cce_cronjobs),
    "huawei_list_cce_hpas": (("region", "cluster_id"), _list_cce_hpas),
    "huawei_generate_cce_hpa_manifest": (("workload_name", "namespace", "min_replicas", "max_replicas"), _generate_cce_hpa_manifest),
    "huawei_configure_cce_hpa": (("region", "cluster_id", "workload_name", "namespace", "min_replicas", "max_replicas"), _configure_cce_hpa),
    "huawei_analyze_cce_cost_optimization": (("region", "cluster_id"), _analyze_cce_cost_optimization),
    "huawei_scan_cce_availability_risk": (("region", "cluster_id"), _scan_cce_availability_risk),
    "huawei_analyze_cce_capacity_trend": (("region", "cluster_id"), _analyze_cce_capacity_trend),
    "huawei_generate_ops_report": (("region", "cluster_id"), _generate_ops_report),
    "huawei_autoscaling_diagnose": (("region", "cluster_id"), _autoscaling_diagnose),
    "huawei_change_impact_analyze": (("region", "cluster_id"), _change_impact_analyze),
    "huawei_dependency_impact_analyze": (("region", "cluster_id"), lambda params: dependency_impact_analysis.analyze_dependency_impact_action(params)),
    "huawei_root_cause_analyze": (("region", "cluster_id"), lambda params: root_cause_analysis.analyze_root_cause_action(params)),
    "huawei_list_aom_instances": (("region",), _list_aom_instances),
    "huawei_resolve_cce_aom_instance": (("region", "cluster_id"), _resolve_cce_aom_instance),
    "huawei_get_apm_master_address": (("region",), _get_apm_master_address),
    "huawei_get_aom_metrics": (("region", "aom_instance_id", "query"), _get_aom_metrics),
    "huawei_list_aom_alarm_rules": (("region",), _list_aom_alarm_rules),
    "huawei_create_aom_alarm_rule": (("region", "rule_name", "metric_name", "namespace", "comparison_operator", "threshold", "period", "evaluation_periods", "statistic", "alarm_level"), _create_aom_alarm_rule),
    "huawei_create_aom_event_alarm_rule": (("region", "cluster_id", "rule_name", "event_name"), _create_aom_event_alarm_rule),
    "huawei_update_aom_alarm_rule": (("region", "rule_name"), _update_aom_alarm_rule),
    "huawei_delete_aom_alarm_rule": (("region", "rule_name"), _delete_aom_alarm_rule),
    "huawei_disable_aom_alarm_rule": (("region", "rule_id"), _disable_aom_alarm_rule),
    "huawei_enable_aom_alarm_rule": (("region", "rule_id"), _enable_aom_alarm_rule),
    "huawei_list_aom_action_rules": (("region",), _list_aom_action_rules),
    "huawei_delete_aom_action_rule": (("region", "rule_name"), _delete_aom_action_rule),
    "huawei_list_aom_mute_rules": (("region",), _list_aom_mute_rules),
    "huawei_list_aom_current_alarms": (("region",), _list_aom_current_alarms),
    "huawei_list_aom_alarms": (("region",), _list_aom_alarms),
    "huawei_list_log_groups": (("region",), _list_log_groups),
    "huawei_list_log_streams": (("region",), _list_log_streams),
    "huawei_query_logs": (("region", "log_group_id", "log_stream_id"), _query_logs),
    "huawei_get_recent_logs": (("region", "log_group_id", "log_stream_id"), _get_recent_logs),
    "huawei_query_aom_logs": (("region", "cluster_id"), _query_aom_logs),
    "huawei_cce_cluster_inspection": (("region", "cluster_id"), lambda params: cce_inspection.cce_cluster_inspection(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))),
    "huawei_cce_cluster_inspection_parallel": (("region", "cluster_id"), lambda params: cce_inspection.cce_cluster_inspection_parallel(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), int(params.get("max_workers", 4)))),
    "huawei_cce_cluster_inspection_subagent": (("region", "cluster_id"), lambda params: cce_inspection.generate_auto_subagent_info(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))),
    "huawei_aggregate_inspection_results": (("results", "cluster_info"), _aggregate_results_action),
    "huawei_export_inspection_report": (("region", "cluster_id"), lambda params: cce_inspection.export_inspection_report(params["region"], params["cluster_id"], params.get("output_file", f"/tmp/cce_inspection_report_{params['cluster_id'][:8]}.html"), params.get("ak"), params.get("sk"))),
    "huawei_pod_status_inspection": (("region", "cluster_id"), lambda params: _inspection_check_action(cce_inspection.pod_status_inspection, params)),
    "huawei_addon_pod_monitoring_inspection": (("region", "cluster_id"), _addon_pod_inspection_action),
    "huawei_biz_pod_monitoring_inspection": (("region", "cluster_id"), _biz_pod_inspection_action),
    "huawei_node_status_inspection": (("region", "cluster_id"), lambda params: _inspection_check_action(cce_inspection.node_status_inspection, params)),
    "huawei_node_resource_inspection": (("region", "cluster_id"), _node_resource_inspection_action),
    "huawei_node_vul_inspection": (("region", "cluster_id"), lambda params: _inspection_check_action(cce_inspection.node_vul_inspection, params)),
    "huawei_event_inspection": (("region", "cluster_id"), lambda params: _inspection_check_action(cce_inspection.event_inspection, params)),
    "huawei_aom_alarm_inspection": (("region", "cluster_id"), _aom_alarm_inspection_action),
    "huawei_elb_monitoring_inspection": (("region", "cluster_id"), _elb_monitoring_inspection_action),
    "huawei_get_cce_logconfigs": (("region", "cluster_id"), lambda params: _cce_app_logs_mod.get_cce_logconfigs_action(params)),
    "huawei_create_cce_logconfig": (("region", "cluster_id", "logconfig_name", "source_type", "log_group_id", "log_stream_id"), lambda params: _cce_app_logs_mod.create_cce_logconfig_action(params)),
    "huawei_delete_cce_logconfig": (("region", "cluster_id", "logconfig_name"), lambda params: _cce_app_logs_mod.delete_cce_logconfig_action(params)),
    "huawei_query_cce_audit_logs": (("region", "cluster_id"), lambda params: _cce_app_logs_mod.query_cce_audit_logs_action(params)),
    "huawei_get_application_logconfigs": (("region", "cluster_id", "app_name"), lambda params: _cce_app_logs_mod.get_application_logconfigs_action(params)),
    "huawei_query_application_logs": (("region", "cluster_id", "app_name"), lambda params: _cce_app_logs_mod.query_application_logs_action(params)),
    "huawei_query_application_recent_logs": (("region", "cluster_id", "app_name"), lambda params: _cce_app_logs_mod.query_application_recent_logs_action(params)),
    "huawei_analyze_application_logs": (("region", "cluster_id", "app_name"), lambda params: _cce_app_logs_mod.analyze_application_logs_action(params)),
    "huawei_get_cce_pod_metrics_topN": (("region", "cluster_id"), lambda params: _metric_action(cce_metrics.get_cce_pod_metrics_topN, params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"), params.get("label_selector"), _to_int(params.get("top_n"), 10), _to_int(params.get("hours"), 1), params.get("cpu_query"), params.get("memory_query"), params.get("node_ip"))),
    "huawei_get_cce_pod_metrics": (("region", "cluster_id", "pod_name"), lambda params: _metric_action(cce_metrics.get_cce_pod_metrics, params["region"], params["cluster_id"], params["pod_name"], params.get("ak"), params.get("sk"), params.get("project_id"), params.get("namespace"), _to_int(params.get("hours"), 1), params.get("cpu_query"), params.get("memory_query"))),
    "huawei_get_cce_node_metrics_topN": (("region", "cluster_id"), lambda params: _metric_action(cce_metrics.get_cce_node_metrics_topN, params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("top_n"), 10), _to_int(params.get("hours"), 1), params.get("cpu_query"), params.get("memory_query"), params.get("disk_query"))),
    "huawei_get_cce_node_metrics": (("region", "cluster_id", "node_ip"), lambda params: _metric_action(cce_metrics.get_cce_node_metrics, params["region"], params["cluster_id"], params["node_ip"], params.get("ak"), params.get("sk"), params.get("project_id"), _to_int(params.get("hours"), 1), params.get("cpu_query"), params.get("memory_query"), params.get("disk_query"))),
    "huawei_network_diagnose": (("region", "cluster_id"), _network_diagnose_action),
    "huawei_network_diagnose_by_alarm": (("region", "cluster_id", "alarm_info"), _network_diagnose_by_alarm_action),
    "huawei_network_failure_diagnose": (("region", "cluster_id"), _network_failure_diagnose_action),
    "huawei_storage_failure_diagnose": (("region", "cluster_id"), _storage_failure_diagnose_action),
    "huawei_workload_diagnose": (("region", "cluster_id"), _workload_diagnose_action),
    "huawei_workload_diagnose_by_alarm": (("region", "cluster_id", "alarm_info"), _workload_diagnose_by_alarm_action),
    "huawei_hibernate_cce_cluster": (("region", "cluster_id"), _hibernate_cce_cluster_action),
    "huawei_awake_cce_cluster": (("region", "cluster_id"), _awake_cce_cluster_action),

    "huawei_network_verify_pod_scheduling": (("region", "cluster_id", "workload_name"), _network_verify_pod_scheduling_action),
    "huawei_node_batch_diagnose": (("region", "cluster_id"), _node_batch_diagnose_action),
    "huawei_node_diagnose": (("region", "cluster_id"), _node_diagnose_action),
    "huawei_node_failure_diagnose": (("region", "cluster_id"), lambda params: node_failure_diagnosis.diagnose_node_failure_action(params)),

    # HSS vulnerability management
    "huawei_hss_list_hosts": (("region",), _hss_list_vul_host_hosts),
    "huawei_hss_list_host_vuls_all": (("region", "host_id"), _hss_list_host_vuls_all),
    "huawei_hss_change_vul_status": (("region",), _hss_change_vul_status),

    # CCE node operations
    "huawei_cce_node_cordon": (("region", "cluster_id", "node_name"), _cce_node_cordon),
    "huawei_cce_node_uncordon": (("region", "cluster_id", "node_name"), _cce_node_uncordon),
    "huawei_cce_node_drain": (("region", "cluster_id", "node_name"), _cce_node_drain),
    "huawei_cce_node_status": (("region", "cluster_id", "node_name"), _cce_node_status),

    # ECS operations
    "huawei_reboot_ecs": (("region", "instance_id"), _reboot_ecs),
    "huawei_rollback_cce_workload": (("region", "cluster_id", "namespace", "workload_type", "name"), lambda params: auto_remediation.rollback_cce_workload_action(params)),
    "huawei_auto_remediation_run": (("region", "cluster_id", "namespace"), lambda params: auto_remediation.auto_remediation_run_action(params)),

    # CCE EIP operations
    "huawei_bind_cce_cluster_eip": (("region", "cluster_id", "eip_id"), _bind_cce_cluster_eip),
    "huawei_unbind_cce_cluster_eip": (("region", "cluster_id"), _unbind_cce_cluster_eip),

    # Monitor dashboard generation
    "huawei_generate_monitor_dashboard": (("region", "cluster_id"), _generate_monitor_dashboard),

    # Diagnosis report generation
    "huawei_generate_diagnosis_report": (("region", "cluster_id", "workload_name"), _generate_diagnosis_report),

    # Alarm filtering & analysis
    "huawei_analyze_aom_alarms": (("region",), _analyze_aom_alarms),

    # ===== Auto Inspection (Quick Check + Deep Diagnosis) =====
    "huawei_cce_quick_check": (("region", "cluster_id"), _cce_quick_check_action),
    "huawei_cce_deep_diagnosis": (("region", "cluster_id"), _cce_deep_diagnosis_action),
    "huawei_cce_auto_inspection": (("region", "cluster_id"), _cce_auto_inspection_action),
}


def is_registered_action(action: str) -> bool:
    return action in ACTION_SPECS


def dispatch_action(action: str, params: Dict[str, str]) -> Dict[str, Any]:
    required, handler = ACTION_SPECS[action]
    error = _require(params, *required)
    if error:
        return {"success": False, "error": error}
    return handler(params)
