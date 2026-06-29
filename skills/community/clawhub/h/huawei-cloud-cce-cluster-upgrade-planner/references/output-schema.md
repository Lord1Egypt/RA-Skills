# Output Schema

## Assessment Report Schema

```json
{
  "report_type": "cce_cluster_upgrade_assessment",
  "generated_at": "2026-05-30T00:00:00+00:00",
  "cluster_info": {
    "cluster_id": "xxx",
    "cluster_name": "my-cluster",
    "current_version": "v1.23.5-r0",
    "target_version": "v1.25.3-r0",
    "cluster_status": "Available",
    "region": "cn-north-4",
    "total_nodes": 10,
    "active_nodes": 10,
    "node_pools": [
      {
        "nodepool_id": "pool-xxx",
        "name": "worker-pool",
        "node_count": 10,
        "flavor": "c7.large.2",
        "os": "EulerOS 2.9"
      }
    ],
    "installed_addons": [
      {
        "addon_name": "coredns",
        "current_version": "1.23.6",
        "status": "running"
      }
    ]
  },
  "upgrade_path": {
    "is_direct": true,
    "current_to_target": "v1.23 → v1.25",
    "intermediate_hops": [],
    "upgrade_path_rules": [
      "v1.23 → v1.25 is a direct upgrade",
      "Patch version must be latest before major upgrade"
    ]
  },
  "pre_check_result": {
    "status": "pass|fail|warning",
    "total_items": 76,
    "passed": 70,
    "failed": 2,
    "warnings": 4,
    "failed_items": [
      {
        "check_id": 11,
        "name": "节点CPU使用率检查",
        "description": "Node CPU usage exceeds 90%",
        "affected_nodes": ["node-xxx"],
        "remediation": "Reduce workload or add nodes before upgrade"
      }
    ],
    "warning_items": [
      {
        "check_id": 9,
        "name": "兼容性风险检查",
        "description": "PSP removed in v1.25, need PSA migration",
        "remediation": "Complete PSP→PSA migration before upgrade"
      }
    ]
  },
  "addon_compatibility": {
    "auto_upgraded": ["coredns", "metrics-server", "everest"],
    "needs_separate_upgrade": ["nginx-ingress"],
    "must_upgrade_before_cluster": [],
    "no_action_needed": []
  },
  "upgrade_window": {
    "control_plane_minutes": 15,
    "node_upgrade_minutes": 100,
    "addon_upgrade_minutes": 50,
    "verification_minutes": 30,
    "buffer_minutes": 40,
    "total_minutes": 240,
    "total_hours": 4,
    "recommended_start_time": "02:00",
    "recommended_end_time": "06:00",
    "batch_strategy": {
      "scope": "Cluster",
      "batch_1_nodes": 1,
      "batch_2_nodes": 4,
      "batch_3_nodes": 5,
      "max_batch_size": 20
    }
  },
  "execution_preview": {
    "phase_1_control_plane": {
      "command": "hcloud CCE UpgradeCluster --cluster_id=xxx --metadata.apiVersion=v3 --metadata.kind=UpgradeTask --spec.clusterUpgradeAction.targetVersion=v1.25 --spec.clusterUpgradeAction.strategy.type=inPlaceRollingUpdate --spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.userDefinedStep=20 --cli-region=cn-north-4",
      "estimated_time": "15 min",
      "risk": "API Server brief interruption"
    },
    "phase_2_nodes": {
      "command": "hcloud CCE UpgradeNodePool --cluster_id=xxx --nodepool_id=pool-xxx --cli-region=cn-north-4",
      "estimated_time": "100 min (3 batches)",
      "risk": "Nodes temporarily unschedulable"
    },
    "phase_3_addons": {
      "commands": [
        "hcloud CCE UpdateAddonInstance --cluster_id=xxx --addon_id=nginx-ingress-id --body.version=2.4.5 --cli-region=cn-north-4"
      ],
      "estimated_time": "10 min per addon",
      "risk": "Brief service interruption for NGINX Ingress"
    }
  },
  "rollback_plan": {
    "primary": "PauseUpgradeClusterTask if issues arise",
    "secondary": "Cancel workflow via UpgradeWorkFlowUpdate",
    "backup": "CBR/EVS backup before upgrade, etcd auto-backup during upgrade"
  },
  "post_verification": [
    "Cluster status.phase = Available",
    "All nodes Ready",
    "All addons running",
    "Business workload health (Pod status, Service connectivity)",
    "CoreDNS resolution (nslookup test)",
    "Ingress/ELB routing (curl test)"
  ]
}
```