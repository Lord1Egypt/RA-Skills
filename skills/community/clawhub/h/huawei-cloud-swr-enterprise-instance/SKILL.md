---
name: huawei-cloud-swr-enterprise-instance
description: |
  Huawei Cloud SWR enterprise instance lifecycle management via hcloud CLI.
  Trigger: "SWR enterprise instance", "SWR 企业实例", "SWR 企业版", "企业仓库实例", "swr.ee", "实例管理"
tags: [swr, enterprise-instance, container-registry, registry, domain]
---

# Huawei Cloud SWR Enterprise Instance Management

## Overview

This skill provides lifecycle management for Huawei Cloud SWR (Software Repository for Container)
enterprise instances using `hcloud` CLI. Enterprise instances provide dedicated, isolated container
registry environments with security scanning, replication, and custom domain support.

**Architecture**: hcloud CLI → SWR API → Instance/Namespace/Registry/Repository/Artifact/Credential/Endpoint/Domain

**Related Skills**:

- `huawei-cloud-swr-image-management` - Image lifecycle (basic SWR namespaces, repos, tags, auth, quotas)
- `huawei-cloud-swr-image-governance` - Image governance (permissions, retention, sharing, immutable rules)
- `huawei-cloud-swr-image-automation` - Image automation ops (sync, triggers, domains)

**Capabilities**:

- Instance lifecycle: create/list/show/delete/update configuration
- Namespace management with security scanning and vulnerability blocking
- Registry management for cross-instance image sync
- Repository and artifact management with vulnerability scanning
- Credential management (long-term and temporary)
- Network access (VPC internal endpoints, public access with whitelist)
- Custom domain management
- Statistics and job monitoring

## Prerequisites

### 0. Enterprise Repository Service Authorization (MANDATORY)

You **must** authorize the SWR Enterprise Repository feature before using this skill.
Visit [https://console.huaweicloud.com/swr-instance](https://console.huaweicloud.com/swr-instance)
to complete authorization. If any API returns an authorization error, direct the user to this link
and wait for confirmation.

### 1. hcloud CLI Requirements (MANDATORY)

- hcloud CLI installed (version >= 7.2.2)
- Run `hcloud version` to verify; first-time: `printf "y\n" | hcloud version`

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode via environment variables)
- Never expose AK/SK in code, conversation, or commands
- Use env vars: `HUAWEI_CLOUD_AK`, `HUAWEI_CLOUD_SK`, `HUAWEI_CLOUD_REGION`
- Prefer IAM users over root account; enable MFA for sensitive operations

```bash
export HUAWEI_CLOUD_AK=<your-ak>
export HUAWEI_CLOUD_SK=<your-sk>
export HUAWEI_CLOUD_REGION=cn-north-4
```

### 3. IAM Permission Requirements

See [IAM Permission Policies](references/iam-policies.md) for complete permission list and policy JSON.

**Permission Failure Handling**:

1. When any command fails due to permission errors, read `references/iam-policies.md`
2. Display the required permission list and policy JSON to the user
3. Guide the user to create a custom policy in IAM console
4. Wait for user confirmation that permissions have been granted

## Core Commands

See [Command Reference](references/command-reference.md) for full command examples and naming rules.

**⚠️ hcloud CLI CreateInstance Bug**: `hcloud SWR CreateInstance` has a duplicate `--project_id`
parameter bug (`重复的参数:project_id`). Use the Python SDK script instead:

```bash
python scripts/swr_instance_helper.py create --name=my-instance --spec=swr.ee.basic \
    --vpc_id=<vpc-id> --subnet_id=<subnet-id> \
    --enterprise_project_id=0 --description="My enterprise registry"
```

All other lifecycle commands (List/Show/Update/Delete) work fine with hcloud CLI.

**Resource Types and Commands**:

| Resource          | Key Commands                                                     | Reference                                                 |
| ----------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| Instance          | Create (SDK), List, Show, UpdateConfig, Delete                  | [Task: Lifecycle](references/task-instance-lifecycle.md)  |
| Namespace         | Create, List, Show, Update, Delete                               | [Task: Namespaces](references/task-instance-namespaces.md) |
| Registry          | Create, List, Show, Update, Delete                               | [Task: Registries](references/task-instance-registries.md) |
| Repository        | List, Show, Update, Delete                                       | [Task: Registries](references/task-instance-registries.md) |
| Artifact          | List, Show, Scan, Delete                                         | [Task: Artifacts](references/task-instance-artifacts.md)   |
| Credential        | CreateLt, CreateTemp, List, Update, Delete                      | [Task: Credentials](references/task-instance-credentials.md) |
| Endpoint          | CreateInternal, List, Show, Delete, Policy CRUD                 | [Task: Endpoints](references/task-instance-endpoints.md)   |
| Domain            | Add, List, Show, Delete, Update                                  | [Task: Domains](references/task-instance-domains.md)       |
| Statistics/Jobs   | ListStatistics, ListJobs, ShowJob, DeleteJob                     | [Command Reference](references/command-reference.md)       |

## Parameter Reference

See [Parameter Reference](references/parameter-reference.md) for detailed parameter tables
(Common, Instance Creation, Namespace, Registry, Endpoint Whitelist).

## Output Format

See [Output Format](references/output-format.md) for response format examples.

## Verification

See [Verification Method](references/verification-method.md) for step-by-step verification.

## Best Practices

1. **Instance naming**: Use descriptive names reflecting environment (`prod-instance`, `dev-instance`)
2. **VPC selection**: Choose VPC/subnet matching your workload deployment
3. **Namespace security**: Enable `auto_scan=true` and `prevent_vul=true` for production
4. **Severity blocking**: `high`/`critical` for production; `none`/`low` for development
5. **Registry credentials**: Store securely; rotate access keys periodically
6. **Public access**: Always configure IP whitelist when enabling public access
7. **Custom domains**: Use SCM certificates for HTTPS
8. **Delete with caution**: Instance/namespace/artifact deletion is irreversible
9. **Credentials**: LtCredential for CI/CD; TempCredential for temporary access
10. **Spec selection**: `swr.ee.basic` for small teams; `swr.ee.professional` for enterprise

## Reference Documents

| Document                                                          | Description                               |
| ----------------------------------------------------------------- | ----------------------------------------- |
| [Command Reference](references/command-reference.md)              | Full CLI examples and naming rules        |
| [Parameter Reference](references/parameter-reference.md)          | Parameter tables (Instance, Namespace, Registry, Endpoint) |
| [SWR Instance API Guide](references/swr-instance-api-guide.md)   | hcloud SWR instance API reference         |
| [SDK Helper Script](scripts/swr_instance_helper.py)               | Python SDK for CreateInstance (bypasses hcloud bug) |
| [Output Format](references/output-format.md)                     | Response format examples                  |
| [IAM Permission Policies](references/iam-policies.md)             | Required permissions and policy JSON      |
| [Verification Method](references/verification-method.md)          | Step-by-step verification                 |
| [Common Pitfalls](references/common-pitfalls.md)                  | Troubleshooting guides                    |
| [Task: Instance Lifecycle](references/task-instance-lifecycle.md) | Instance create, list, show, update config |
| [Task: Instance Namespaces](references/task-instance-namespaces.md) | Namespace CRUD workflows                |
| [Task: Instance Registries](references/task-instance-registries.md) | Registry CRUD and repositories           |
| [Task: Instance Artifacts](references/task-instance-artifacts.md) | Artifact management and scanning          |
| [Task: Instance Credentials](references/task-instance-credentials.md) | Credential management workflows      |
| [Task: Instance Endpoints](references/task-instance-endpoints.md) | Internal and public access configuration  |
| [Task: Instance Domains](references/task-instance-domains.md)     | Custom domain management                  |

## Notes

- **Instance deletion is irreversible** — removes ALL data permanently
- **Namespace deletion is irreversible** — removes all repositories and artifacts
- **Artifact deletion is irreversible** — the image version cannot be recovered
- **Default domain cannot be deleted** — only custom domains can be removed
- **AK/SK must never be hardcoded** — use environment variables only
- **hcloud CLI CreateInstance bug** — use Python SDK script as alternative
- **Pagination**: `offset` must be 0 or a multiple of `limit`
- **Registry access_secret is sensitive** — never expose or log

## Common Pitfalls

See [Common Pitfalls](references/common-pitfalls.md) for detailed troubleshooting guides.

Key pitfalls: invalid instance name format, VPC/subnet not found, instance still creating,
offset not multiple of limit, registry credential wrong, domain cert not found,
cannot delete default domain, public whitelist format, hcloud CreateInstance bug,
SWR service quota exceeded.