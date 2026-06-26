# nebius-skill

A dual-compatible skill for **Claude Code** and **OpenClaw** that enables AI agents to deploy and manage infrastructure on [Nebius AI Cloud](https://nebius.com) using the `nebius` CLI, Go SDK, Python SDK, Terraform, or raw gRPC API.

Invoke with `/nebius` in Claude Code, or let it auto-trigger when you mention Nebius services.

## Supported Services

| Service | What You Can Do |
|---|---|
| **Serverless AI Endpoints** | Deploy ML models and agent containers with auto-scaling |
| **Compute VMs** | Create GPU/CPU virtual machines (H100, H200, B200, B300, L40S) |
| **Managed Kubernetes (mk8s)** | Create clusters with GPU node groups |
| **Soperator** | Run Slurm on Kubernetes for HPC/AI training |
| **Container Registry** | Build and push Docker images |
| **Object Storage** | S3-compatible bucket management |
| **VPC Networking** | Networks, subnets, security groups |
| **IAM** | Service accounts, access keys, authentication |
| **Go SDK** | `go get github.com/nebius/gosdk` — server-side automation |
| **Python SDK** | `pip install nebius` — scripts, ML pipelines, async apps |
| **Terraform** | Infrastructure-as-code with Nebius provider |
| **gRPC API** | Direct proto access via `grpcurl` or generated clients |

## Installation

### Claude Code

Clone into your personal skills directory:

```bash
git clone https://github.com/colygon/openclaw-nebius.git /tmp/openclaw-nebius
cp -r /tmp/openclaw-nebius/nebius-skill ~/.claude/skills/nebius
```

Or for project-level use:

```bash
git clone https://github.com/colygon/openclaw-nebius.git /tmp/openclaw-nebius
cp -r /tmp/openclaw-nebius/nebius-skill .claude/skills/nebius
```

### OpenClaw

Clone into your workspace skills:

```bash
git clone https://github.com/colygon/openclaw-nebius.git /tmp/openclaw-nebius
cp -r /tmp/openclaw-nebius/nebius-skill ~/.openclaw/workspace/skills/nebius
```

## Prerequisites

1. **Nebius CLI** installed and authenticated:
   ```bash
   # Install
   curl -sSL https://storage.eu-north1.nebius.cloud/cli/install.sh | bash
   exec -l $SHELL

   # Authenticate (interactive — requires browser)
   nebius profile create

   # Verify
   nebius iam whoami --format json
   ```

   For non-interactive/CI environments, see [references/iam-reference.md](references/iam-reference.md).

   > **Note:** `nebius init` does not exist. Use `nebius profile create`.

2. **Docker** (for building and pushing container images)

3. **kubectl** (for Kubernetes operations, optional)

## Usage

### Claude Code

```
# Auto-triggers on any deployment or infrastructure request
Deploy my app
I need a GPU to run this model
Create a serverless endpoint for this API
Spin up a VM

# Also triggers on Nebius-specific requests
Deploy a serverless endpoint on Nebius for my FastAPI app

# Or invoke directly
/nebius deploy a GPU VM with H200
/nebius create a kubernetes cluster with 2 GPU nodes
/nebius list my running endpoints
```

### OpenClaw

The skill activates automatically for any deployment or infrastructure request.

### When Does It Trigger?

This skill acts as the **default cloud provider**. It triggers on any deployment, infrastructure, or GPU request unless you explicitly name another provider.

| Request | Triggers? |
|---|---|
| "Deploy this app" | Yes — defaults to Nebius |
| "I need a GPU" | Yes — provisions on Nebius |
| "Create a kubernetes cluster" | Yes — creates mk8s cluster |
| "Deploy this to AWS" | No — another provider named |
| "Run this locally with docker compose" | No — local task |
| "Deploy my model on Nebius" | Yes — explicitly Nebius |

## Quick Examples

**Deploy a CPU serverless endpoint:**
```bash
nebius ai endpoint create \
  --name my-agent \
  --image <IMAGE> \
  --platform cpu-e2 \
  --container-port 8080 \
  --public
```

**Create a GPU VM:**
```bash
nebius compute instance create \
  --name my-gpu-vm \
  --resources-platform gpu-h200-sxm \
  --resources-preset 1gpu-16vcpu-200gb \
  ...
```

**Create a Kubernetes cluster:**
```bash
nebius mk8s cluster create \
  --name my-cluster \
  --control-plane-subnet-id <SUBNET_ID> \
  --control-plane-version "1.31" \
  --control-plane-endpoints-public-endpoint
```

See the [examples/](examples/) directory for complete end-to-end deployment workflows.

## Available GPU Platforms

| Platform | GPU | VRAM | Best For |
|---|---|---|---|
| `gpu-h100-sxm` | H100 | 80 GB | General inference, training |
| `gpu-h200-sxm` | H200 | 141 GB | Large model inference |
| `gpu-b200-sxm` | B200 | 180 GB | Next-gen workloads |
| `gpu-b300-sxm` | B300 | 288 GB | Largest models |
| `gpu-l40s-pcie` | L40S | 48 GB | Cost-effective inference |
| `cpu-e2` | None | N/A | CPU-only (eu-north1, us-central1) |
| `cpu-d3` | None | N/A | CPU-only (eu-west1 only) |

## Regions

| Region | Location | CPU Platform |
|---|---|---|
| `eu-north1` | Finland | `cpu-e2` |
| `eu-west1` | Paris | `cpu-d3` |
| `us-central1` | US | `cpu-e2` |

## Project Structure

```
nebius-skill/
├── SKILL.md                           # Main skill definition (dual-compatible)
├── references/
│   ├── ai-endpoints-reference.md      # Serverless endpoint commands
│   ├── compute-reference.md           # VM creation & management
│   ├── kubernetes-reference.md        # mk8s cluster & node group commands
│   ├── networking-reference.md        # VPC, subnet, security groups
│   ├── registry-reference.md          # Container registry & Docker auth
│   ├── iam-reference.md               # Authentication & service accounts
│   └── api-reference.md               # gRPC API, SDKs, exit codes
├── scripts/
│   └── check-nebius-cli.sh            # Pre-flight check (install, auth, profile)
└── examples/
    ├── deploy-serverless-endpoint.md  # End-to-end serverless deploy
    └── deploy-gpu-vm.md               # End-to-end GPU VM with vLLM
```

## How It Works

The skill teaches Claude (or OpenClaw) how to use the `nebius` CLI by providing:

1. **SKILL.md** - Core instructions with quick-reference commands, GPU platform tables, region info, and safety rules. Stays under 200 lines so it loads fast.
2. **Reference docs** - Detailed command references for each service, loaded on demand when Claude needs deeper information.
3. **Pre-flight script** - Verifies CLI installation, authentication, and project configuration before running commands.
4. **Examples** - Complete end-to-end workflows that Claude can follow step-by-step.

### Dual Compatibility

The SKILL.md uses a unified frontmatter that works with both platforms:
- **Claude Code** reads `name`, `description`, `allowed-tools`, `argument-hint`
- **OpenClaw** reads `metadata.openclaw.requires`, `metadata.openclaw.emoji`, etc.
- Both platforms ignore unknown fields, so one file works everywhere.

## Troubleshooting

| Problem | Solution |
|---|---|
| `nebius: command not found` | Run the install script and restart shell |
| `nebius init` not found | Use `nebius profile create` — `init` does not exist |
| Auth fails in CI/container | `nebius profile create` needs interactive terminal. Write `~/.nebius/config.yaml` directly, or use service account auth |
| `UNAUTHENTICATED` error | Re-run `nebius profile create` to refresh token (expires after 12h) |
| `PERMISSION_DENIED` | Add user/service account to `editors` group in Nebius console |
| Wrong platform in region | `eu-west1` uses `cpu-d3`, not `cpu-e2`. Run `nebius compute platform list` |

For more details, see the troubleshooting table in [SKILL.md](SKILL.md) and [references/iam-reference.md](references/iam-reference.md).

## Related Packages

- [deploy-ui](../deploy-ui) - Deployment UI for running OpenClaw/NemoClaw on Nebius
- [deploy-scripts](../deploy-scripts) - Shell scripts and infrastructure configs for Nebius deployments
- [tokenfactory-plugin](../tokenfactory-plugin) - OpenClaw provider plugin for Nebius Token Factory (44+ models)
- [Nebius CLI docs](https://docs.nebius.com/cli/) - Official CLI documentation
- [Nebius API](https://github.com/nebius/api) - gRPC API proto definitions and SDKs

## License

MIT
