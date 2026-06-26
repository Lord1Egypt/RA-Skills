# Serverless AI Endpoints Reference

## Create Endpoint

### CPU-only (with remote inference via Token Factory)

Best for agent/orchestration workloads that don't need local GPU:

```bash
WEB_PASSWORD=$(openssl rand -base64 24)
nebius ai endpoint create \
  --name "<endpoint-name>" \
  --image "<REGISTRY_IMAGE>" \
  --platform cpu-e2 \
  --container-port 8080 \
  --container-port 18789 \
  --env "TOKEN_FACTORY_API_KEY=<key>" \
  --env "TOKEN_FACTORY_URL=<TOKEN_FACTORY_URL>" \
# EU: https://api.tokenfactory.nebius.com/v1
# US (us-central1): https://api.tokenfactory.us-central1.nebius.com/v1
  --env "INFERENCE_MODEL=<model-name>" \
  --env "OPENCLAW_WEB_PASSWORD=${WEB_PASSWORD}" \
  --public
# Dashboard URL: http://<PUBLIC_IP>:18789/#token=${WEB_PASSWORD}&gatewayUrl=ws://<PUBLIC_IP>:18789
```

**Note**: Multiple `--container-port` flags are supported. Port 8080 is the health check, port 18789 is the OpenClaw dashboard.

### GPU (self-hosted inference)

For running models locally on GPU:

```bash
nebius ai endpoint create \
  --name "<endpoint-name>" \
  --image "<REGISTRY_IMAGE>" \
  --platform gpu-h100-sxm \
  --preset 1gpu-16vcpu-200gb \
  --container-port 8080 \
  --disk-size 100Gi \
  --shm-size 16Gi \
  --env "INFERENCE_MODEL=<model-name>" \
  --public \
  --auth token \
  --token "<auth-token>" \
  --subnet-id <SUBNET_ID>
```

### With vLLM for LLM inference

```bash
nebius ai endpoint create \
  --name qs-vllm-chat \
  --image vllm/vllm-openai:latest \
  --container-command "python3 -m vllm.entrypoints.openai.api_server" \
  --args "--model <MODEL_ID> --host 0.0.0.0 --port 8000" \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --public \
  --container-port 8000 \
  --auth token \
  --token "<AUTH_TOKEN>" \
  --shm-size 16Gi
```

## Key Parameters

| Parameter | Description |
|---|---|
| `--name` | Human-readable endpoint name |
| `--image` | Docker image (from Nebius registry or public) |
| `--platform` | GPU/CPU platform (see GPU platforms table) |
| `--preset` | Resource allocation (e.g., `1gpu-16vcpu-200gb`) |
| `--container-port` | Port your container listens on (repeatable for multiple ports) |
| `--container-command` | Override container entrypoint |
| `--args` | Arguments to the container command |
| `--disk-size` | Persistent disk size (e.g., `100Gi`) |
| `--shm-size` | Shared memory size (e.g., `16Gi`, important for PyTorch) |
| `--env` | Environment variables (repeatable) |
| `--public` | Expose a public URL |
| `--auth token` | Require auth token for access |
| `--token` | Set the auth token value |
| `--subnet-id` | VPC subnet for private networking |

## Manage Endpoints

```bash
# List all endpoints
nebius ai endpoint list --format json

# Get endpoint details
nebius ai endpoint get <ENDPOINT_ID> --format json

# Get endpoint by name
nebius ai endpoint get-by-name <endpoint-name> --format json

# View logs
nebius ai endpoint logs <ENDPOINT_ID>
nebius ai endpoint logs <ENDPOINT_ID> --follow --since 5m --timestamps

# Stop endpoint (pauses billing)
nebius ai endpoint stop <ENDPOINT_ID>

# Start endpoint (resume)
nebius ai endpoint start <ENDPOINT_ID>

# Delete endpoint
nebius ai endpoint delete <ENDPOINT_ID>
```

## Update Endpoint

```bash
# Update environment variables
nebius ai endpoint update <ENDPOINT_ID> --env "INFERENCE_MODEL=new-model"

# Update image
nebius ai endpoint update <ENDPOINT_ID> --image <new-image>
```

## Polling for Ready State

After creating an endpoint, poll until it's ready:

```bash
while true; do
  STATUS=$(nebius ai endpoint get <ENDPOINT_ID> --format json | jq -r '.status.state')
  echo "Status: $STATUS"
  if [ "$STATUS" = "RUNNING" ]; then
    echo "Endpoint is ready!"
    URL=$(nebius ai endpoint get <ENDPOINT_ID> --format json | jq -r '.status.url')
    echo "URL: $URL"
    break
  fi
  sleep 10
done
```

## Cost Considerations

- **CPU-only (`cpu-e2`)**: Cheapest option. Use for orchestration/agent workloads with remote inference.
- **GPU endpoints**: Billed per GPU-hour while running. Always `stop` when not in use.
- **`--public`**: Creates a public URL. Omit for internal-only access.
- **`--auth token`**: Strongly recommended for public endpoints to prevent unauthorized access.
