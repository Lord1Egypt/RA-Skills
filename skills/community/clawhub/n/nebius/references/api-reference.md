# Nebius gRPC API & SDK Reference

The `nebius` CLI wraps the gRPC API. For programmatic access — scripts, applications, CI/CD pipelines — use the Go SDK, Python SDK, Terraform provider, or raw gRPC.

**Source of truth for all proto definitions:** https://github.com/nebius/api

## When to Use API vs CLI

| Use Case | Recommended |
|---|---|
| Interactive deploys, quick tasks | `nebius` CLI |
| Application code, automation | Go SDK or Python SDK |
| Infrastructure-as-code | Terraform provider |
| Debugging, one-off queries | `grpcurl` with raw gRPC |

## API Endpoints

All services follow: `<service_name>.api.nebius.cloud:443`

| Service | Endpoint | Key Operations |
|---|---|---|
| Compute | `compute.api.nebius.cloud:443` | Instance, Disk, Filesystem, GpuCluster, Image, Platform, Node, Maintenance |
| IAM (control plane) | `cpl.iam.api.nebius.cloud:443` | Profile, Project, ServiceAccount, AccessKey, Group, Federation, Tenant, Invitation |
| IAM (tokens) | `tokens.iam.api.nebius.cloud:443` | TokenExchange |
| Kubernetes | `mk8s.api.nebius.cloud:443` | Cluster, NodeGroup |
| VPC | `vpc.api.nebius.cloud:443` | Network, Subnet, Allocation, Pool, Route, SecurityGroup, SecurityRule, TargetGroup |
| Storage | `cpl.storage.api.nebius.cloud:443` | Bucket |
| Storage Transfer | `transfer.storage.api.nebius.cloud:443` | Transfer (v1alpha1) |
| DNS | `dns.api.nebius.cloud:443` | Zone, Record |
| Registry | `registry.api.nebius.cloud:443` | Registry, Artifact |
| AI Endpoints | `apps.msp.api.nebius.cloud:443` | Endpoint, Job |
| Secrets (control) | `cpl.mysterybox.api.nebius.cloud:443` | Secret, SecretVersion |
| Secrets (data) | `dpl.mysterybox.api.nebius.cloud:443` | Payload |
| PostgreSQL | `postgresql.msp.api.nebius.cloud:443` | Cluster, Backup |
| MLflow | `mlflow.msp.api.nebius.cloud:443` | Cluster |
| Capacity Blocks | `capacity-blocks.billing-cpl.api.nebius.cloud:443` | CapacityBlockGroup, CapacityInterval |
| Capacity Advisor | `capacity-advisor.billing-cpl.api.nebius.cloud:443` | ResourceAdvice |
| Quotas | `quota-dispatcher.billing-cpl.api.nebius.cloud:443` | QuotaAllowance |
| Billing Export | `api.billing-report-exporter.billing-data-plane.api.nebius.cloud:443` | OneTimeExport |
| Billing Calculator | `api.calculator.billing-data-plane.api.nebius.cloud:443` | Calculator |
| Audit | `audit.api.nebius.cloud:443` | AuditEvent, AuditEventExport |
| K8s Applications | `deployment-manager.mkt.api.nebius.cloud:443` | K8sRelease (v1alpha1) |
| Maintenance | `maintenance.msp.api.nebius.cloud:443` | Maintenance (v1alpha1) |
| Observability | `observability-agent-manager.api.nebius.cloud:443` | Version (logging agent) |

Full endpoint list: https://github.com/nebius/api/blob/main/endpoints.md

**Note:** `OperationService` does not have its own endpoint — use the same endpoint as the service that created the operation.

## Authentication

All API calls require: `Authorization: Bearer <access_token>`

### User Account Token (dev/testing)

```bash
# Via CLI (valid ~12 hours)
ACCESS_TOKEN=$(nebius iam get-access-token)
```

### Service Account Token (production/CI)

1. Create service account and generate key pair (see [iam-reference.md](iam-reference.md)):

```bash
openssl genrsa -out private.pem 4096
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
# Upload public.pem to service account via console or CLI
```

2. Generate JWT (RS256) with claims:
   - `iss`: service account ID
   - `sub`: service account ID
   - `kid`: authorized key ID
   - `exp`: short expiry (5 min — used only for token exchange)

```bash
jwt encode \
  --alg RS256 \
  --kid <authorized_key_ID> \
  --iss <service_account_ID> \
  --sub <service_account_ID> \
  --exp="$(date --date='+5minutes' +%s)" \
  --secret @private.pem
```

3. Exchange JWT for access token via gRPC:

```bash
grpcurl -d '{
  "grantType": "urn:ietf:params:oauth:grant-type:token-exchange",
  "requestedTokenType": "urn:ietf:params:oauth:token-type:access_token",
  "subjectToken": "<JWT>",
  "subjectTokenType": "urn:ietf:params:oauth:token-type:jwt"
}' \
  tokens.iam.api.nebius.cloud:443 \
  nebius.iam.v1.TokenExchangeService/Exchange
```

Or via HTTP:

```bash
curl -X POST https://auth.eu.nebius.com:443/oauth2/token/exchange \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer" \
  -d "assertion=${JWT}"
```

4. Response returns `accessToken` (valid 12 hours / 43,200s), `expiresIn`, `tokenType: Bearer`. Refresh before expiry.

**SDKs handle this automatically** when initialized with service account credentials.

### Raw gRPC Example

```bash
ACCESS_TOKEN=$(nebius iam get-access-token)

grpcurl -rpc-header "Authorization: Bearer ${ACCESS_TOKEN}" \
  cpl.iam.api.nebius.cloud:443 \
  nebius.iam.v1.ProfileService/Get
```

---

## Using grpcurl

### Workflow

1. Find the service and endpoint on [GitHub endpoints list](https://github.com/nebius/api/blob/main/endpoints.md)
2. Check the `*_service.proto` file in [nebius/api](https://github.com/nebius/api) for request/response structure
3. Construct the endpoint: find `api_service_name` in the proto → `{api_service_name}.api.nebius.cloud:443`
4. Invoke the method:

```bash
ACCESS_TOKEN=$(nebius iam get-access-token)

# List VMs in a project
grpcurl -rpc-header "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d '{"parent_id": "project-e00000000000000"}' \
  compute.api.nebius.cloud:443 \
  nebius.compute.v1.InstanceService/List

# Create an AI endpoint
grpcurl -rpc-header "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d '{
    "metadata": {"parent_id": "project-e00000000000000", "name": "my-endpoint"},
    "spec": {"...": "..."}
  }' \
  apps.msp.api.nebius.cloud:443 \
  nebius.ai.v1.EndpointService/Create

# Get operation status (use same endpoint as the service that created it)
grpcurl -rpc-header "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d '{"id": "operation-id"}' \
  compute.api.nebius.cloud:443 \
  nebius.common.v1.OperationService/Get
```

### Key Flags

| Flag | Purpose |
|---|---|
| `-rpc-header "Authorization: Bearer $TOKEN"` | Auth header |
| `-d '{...}'` | JSON request body |
| `-format json` | JSON output (default) |
| `-plaintext` | Disable TLS (not needed for Nebius — always uses TLS on :443) |

---

## Generating Clients from Proto Files

Use the [Buf CLI](https://buf.build/docs/installation) to generate typed gRPC clients from Nebius proto definitions.

### Setup

```bash
# Install Buf
brew install bufbuild/buf/buf  # macOS/Linux

# Clone proto definitions
git clone https://github.com/nebius/api.git
cd api
```

### Generate

Edit `buf.gen.yaml` in the repo root to specify your target language, then run:

```bash
buf generate
```

Generated code appears in `gen/<language>/` (e.g., `gen/java/`, `gen/python/`, `gen/go/`).

### When to Use

- You need typed clients in a language without an official SDK (Java, C++, Rust, etc.)
- You want to pin to a specific API version
- You need proto definitions for code generation pipelines

For Go and Python, prefer the official SDKs below — they handle auth, retries, and pagination.

---

## Go SDK

**Repository:** https://github.com/nebius/gosdk
**Minimum Go:** 1.24

### Installation

```bash
go get github.com/nebius/gosdk
```

### Authentication

```go
import "github.com/nebius/gosdk"

// Option 1: IAM token (dev/testing)
sdk, err := gosdk.New(ctx, gosdk.WithCredentials(gosdk.IAMToken(token)))

// Option 2: Service account key file (production)
import "github.com/nebius/gosdk/auth"
creds := gosdk.ServiceAccountReader(
    auth.NewServiceAccountCredentialsFileParser(nil, "credentials.json"),
)
sdk, err := gosdk.New(ctx, gosdk.WithCredentials(creds))
```

### Service Access Pattern

Services follow the proto directory structure:

```go
// nebius/compute/v1/ → sdk.Services().Compute().V1()
instanceSvc := sdk.Services().Compute().V1().Instance()
mk8sSvc     := sdk.Services().MK8S().V1().Cluster()
iamSvc      := sdk.Services().IAM().V1().ServiceAccount()
aiSvc       := sdk.Services().AI().V1().Endpoint()
```

### CRUD Operations

```go
import computev1 "github.com/nebius/gosdk/proto/nebius/compute/v1"

// Create (returns Operation — call Wait for completion)
op, err := instanceSvc.Create(ctx, &computev1.CreateInstanceRequest{
    Metadata: &computev1.InstanceMetadata{
        ParentId: projectID,
        Name:     "my-instance",
    },
    Spec: &computev1.InstanceSpec{
        // ...
    },
})
instance, err := op.Wait(ctx)

// Get by ID
instance, err := instanceSvc.Get(ctx, &computev1.GetInstanceRequest{Id: instanceID})

// Get by name
instance, err := instanceSvc.GetByName(ctx, &computev1.GetByNameRequest{
    ParentId: projectID,
    Name:     "my-instance",
})

// Update (full-replace, SDK manages X-ResetMask automatically)
op, err := instanceSvc.Update(ctx, &computev1.UpdateInstanceRequest{
    Metadata: &computev1.InstanceMetadata{Id: instanceID},
    Spec:     &computev1.InstanceSpec{/* updated fields */},
})

// List (with pagination)
resp, err := instanceSvc.List(ctx, &computev1.ListInstancesRequest{
    ParentId: projectID,
})

// Filter (range-based iteration across all pages)
iter := instanceSvc.Filter(ctx, &computev1.ListInstancesRequest{ParentId: projectID})
for iter.Next() {
    instance := iter.Value()
    // ...
}

// Delete
op, err := instanceSvc.Delete(ctx, &computev1.DeleteInstanceRequest{Id: instanceID})
op.Wait(ctx)
```

---

## Python SDK

**Repository:** https://github.com/nebius/pysdk
**Docs:** https://nebius.github.io/pysdk/apiReference.html

### Installation

```bash
pip install nebius
```

### Authentication

```python
from nebius.sdk import SDK

# Option 1: IAM token from env var (reads NEBIUS_IAM_TOKEN)
sdk = SDK()

# Option 2: Explicit IAM token
sdk = SDK(credentials="your-iam-token")

# Option 3: From CLI config (~/.nebius/config.yaml)
from nebius.sdk.config import Config
sdk = SDK(config_reader=Config())

# Option 4: Service account key file (production)
sdk = SDK(
    credentials_file_name="credentials.json"
)

# Option 5: Service account with explicit params
sdk = SDK(
    service_account_private_key_file_name="private.pem",
    service_account_public_key_id="key-id",
    service_account_id="sa-id",
)
```

### Service Access Pattern

```python
from nebius.api.nebius.compute.v1 import InstanceServiceClient, ListInstancesRequest
from nebius.api.nebius.ai.v1 import EndpointServiceClient, ListEndpointsRequest
from nebius.api.nebius.storage.v1 import BucketServiceClient, GetBucketRequest

# Create service client
instance_svc = InstanceServiceClient(sdk)
ai_svc = EndpointServiceClient(sdk)

# Async (default)
instances = await instance_svc.list(ListInstancesRequest(parent_id=project_id))

# Sync fallback
result = instance_svc.list(ListInstancesRequest(parent_id=project_id)).wait()
```

### CRUD Operations

```python
from nebius.api.nebius.compute.v1 import (
    CreateInstanceRequest, InstanceMetadata, InstanceSpec,
    GetInstanceRequest, DeleteInstanceRequest,
)

# Create (returns Operation)
op = await instance_svc.create(CreateInstanceRequest(
    metadata=InstanceMetadata(parent_id=project_id, name="my-instance"),
    spec=InstanceSpec(...)
))
result = await op.wait()
instance_id = op.resource_id

# Get
instance = await instance_svc.get(GetInstanceRequest(id=instance_id))

# Delete
op = await instance_svc.delete(DeleteInstanceRequest(id=instance_id))
await op.wait()

# Test credentials
whoami = await sdk.whoami()
```

### Configuration

```python
# Custom timeouts
sdk = SDK(
    credentials="token",
    max_retry_timeout=120,  # seconds (default: 60)
    auth_timeout=900,       # seconds (default: 15 min)
)
```

---

## Terraform Provider

**Source:** `terraform-provider.storage.eu-north1.nebius.cloud/nebius/nebius`
**Docs:** https://docs.nebius.com/terraform-provider

### Setup

```hcl
terraform {
  required_providers {
    nebius = {
      source  = "terraform-provider.storage.eu-north1.nebius.cloud/nebius/nebius"
      version = ">= 0.5.55"
    }
  }
}

provider "nebius" {
  # Service account auth (recommended)
  service_account = {
    private_key_file_env = "NB_AUTHKEY_PRIVATE_PATH"
    public_key_id_env    = "NB_AUTHKEY_PUBLIC_ID"
    account_id_env       = "NB_SA_ID"
  }
}
```

### Resource Naming

Resources follow: `nebius_{service}_{version}_{resource}`

```hcl
resource "nebius_compute_v1_instance" "gpu_vm" {
  # ...
}

resource "nebius_mk8s_v1_cluster" "k8s" {
  # ...
}

resource "nebius_registry_v1_registry" "images" {
  # ...
}
```

---

## API Design Patterns

| Pattern | Details |
|---|---|
| **Operations** | Most mutating methods return `Operation`. Call `Wait()` to poll until complete. |
| **Update semantics** | Full-replace (not patch). `X-ResetMask` header controls which default-valued fields get cleared. SDKs handle automatically. |
| **Idempotency** | Use `X-Idempotency-Key` header (UUID) for safe retries. Ignored for reads. |
| **No concurrent ops** | Multiple simultaneous operations on the same resource may error or abort earlier ones. |
| **Error handling** | `google.rpc.Status` with `nebius.common.v1.ServiceError` details (BadRequest, QuotaFailure, TooManyRequests, etc.) |

## Available Proto Services

**Stable (v1):** ai (Endpoint, Job), compute (Instance, Disk, Filesystem, GpuCluster, Image, Platform), dns (Zone, Record), iam v1 + v2 (Profile, Project, ServiceAccount, AccessKey, Group, Federation, Tenant, Invitation, TokenExchange), mk8s (Cluster, NodeGroup), vpc (Network, Subnet, Allocation, SecurityGroup, SecurityRule), storage (Bucket), registry (Registry, Artifact), mysterybox/secrets (Secret, SecretVersion, Payload), quotas (QuotaAllowance), audit v2 (AuditEvent, AuditEventExport), logging (Version), capacity (CapacityBlockGroup, CapacityInterval, ResourceAdvice)

**Alpha (v1alpha1):** compute (additional Instance/Disk fields), mk8s (additional Cluster/NodeGroup fields), vpc (additional networking), storage (Transfer), billing (OneTimeExport, Calculator), managed PostgreSQL (Cluster, Backup), managed MLflow (Cluster), k8s applications (K8sRelease), maintenance (Maintenance)

## CLI Exit Codes (for error handling)

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Unknown error |
| 2 | Invalid input (bad flags, args) |
| 3 | Invalid value |
| 4 | Configuration issue |
| 7 | Authentication failure |
| 13 | Not found |
| 14 | Already exists |
| 15 | Permission denied |
| 16 | Resource exhausted (quota) |
| 24 | Quota failure |
| 25 | Not enough resources |

Use exit codes to handle errors programmatically in scripts.
