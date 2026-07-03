# Output Schema

`huawei_storage_failure_diagnose` returns structured JSON with the final customer report embedded in `report_markdown`.

```json
{
  "success": true,
  "action": "huawei_storage_failure_diagnose",
  "region": "cn-north-4",
  "cluster_id": "cluster-id",
  "namespace": "default",
  "conclusion": "high signal conclusion",
  "confidence": "High",
  "findings": [
    {
      "stage": "Mount stage failure",
      "type": "EVSNodeAttachLimitExceeded",
      "title": "VolumeAttachment Attached=false; error indicates ECS per-node attached cloud disk count has reached the upper limit",
      "confidence": 0.94,
      "severity": "critical",
      "evidence": [],
      "recommendation": []
    }
  ],
  "top_causes": [],
  "snapshot": {
    "inputs": {},
    "pvcs": [],
    "pvs": [],
    "storage_classes": [],
    "pods": [],
    "nodes": [],
    "events": [],
    "volume_attachments": [],
    "network_policies": [],
    "node_stats": {},
    "pvc_volume_stats": [],
    "csi_logs": {},
    "cloud_storage": {}
  },
  "report_markdown": "# CCE Storage Failure Automated Diagnosis Report\n..."
}
```

## Markdown Sections

`report_markdown` must contain the following headings:

- `# CCE Storage Failure Automated Diagnosis Report`
- `## 1. Diagnosis Overview`
- `## 2. Investigation Process`
- `## 3. Key Object Relationships`
- `## 4. Evidence Matrix`
- `## 5. Diagnosis Conclusion`
- `## 6. Recommended Actions and Verification Standards`
- `## 7. Data Gaps and Manual Confirmation`

## Finding Types

Common `type` values:

- `NormalWaitForFirstConsumer`
- `EVSQuotaExceeded`
- `SFSSubnetIPInsufficient`
- `OBSBucketNameInvalid`
- `EVSAvailabilityZoneSchedulingConflict`
- `LocalPVNodeOffline`
- `VolumeAttachmentNotCreated`
- `EVSNodeAttachLimitExceeded`
- `EVSResidualAttachmentLock`
- `EVSAttachFailed`
- `HostKernelMountFailed`
- `SFSNfsNetworkBlocked`
- `OBSCredentialInvalid`
- `StoragePermissionDenied`
- `PVCCapacityExhausted`
- `PVCInodeExhausted`
- `ReadOnlyFilesystemProtection`
- `ConfigMapSecretSubPathDeadlock`
- `PVCProtectionBlocked`
- `StorageIOError`