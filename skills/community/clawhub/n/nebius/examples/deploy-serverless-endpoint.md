# Deploy a Serverless AI Endpoint on Nebius

This example deploys an AI agent container as a serverless endpoint on Nebius AI Cloud.

## Option A: CPU-only with Remote Inference (Cheapest)

Uses Token Factory for inference - no GPU quota needed.

### Prerequisites

- Nebius CLI installed and authenticated
- Docker installed
- A Dockerfile for your application
- Token Factory API key (get from Nebius console)

### Steps

```bash
# 1. Set variables
PROJECT_ID=$(nebius config get parent-id)
REGION="eu-north1"
ENDPOINT_NAME="my-agent"
TOKEN_FACTORY_KEY="<your-token-factory-api-key>"
MODEL="deepseek-ai/DeepSeek-R1-0528"

# Token Factory URL — US region uses a different endpoint:
if [[ "$REGION" == "us-central1" ]]; then
  TOKEN_FACTORY_URL="https://api.tokenfactory.us-central1.nebius.com/v1"
else
  TOKEN_FACTORY_URL="https://api.tokenfactory.nebius.com/v1"
fi

# 2. Check for existing registry or create one
REGISTRY_ID=$(nebius registry list --format json \
  | jq -r '.items[] | select(.metadata.name=="my-registry") | .metadata.id')

if [ -z "$REGISTRY_ID" ]; then
  REGISTRY_ID=$(nebius registry create \
    --name my-registry \
    --parent-id $PROJECT_ID \
    --format json | jq -r '.metadata.id')
  echo "Created registry: $REGISTRY_ID"
else
  echo "Using existing registry: $REGISTRY_ID"
fi

# 3. Authenticate Docker
nebius iam get-access-token | docker login cr.${REGION}.nebius.cloud \
  --username iam --password-stdin

# 4. Build and push image
IMAGE="cr.${REGION}.nebius.cloud/${REGISTRY_ID}/${ENDPOINT_NAME}:latest"
docker build -t $IMAGE .
docker push $IMAGE

# 5. Deploy endpoint (CPU-only)
# Generate a dashboard password for the OpenClaw Control UI
WEB_PASSWORD=$(openssl rand -base64 24)
echo "Dashboard password: $WEB_PASSWORD"

nebius ai endpoint create \
  --name "$ENDPOINT_NAME" \
  --image "$IMAGE" \
  --platform cpu-e2 \
  --container-port 8080 \
  --container-port 18789 \
  --env "TOKEN_FACTORY_API_KEY=${TOKEN_FACTORY_KEY}" \
  --env "TOKEN_FACTORY_URL=${TOKEN_FACTORY_URL}" \
  --env "INFERENCE_MODEL=${MODEL}" \
  --env "OPENCLAW_WEB_PASSWORD=${WEB_PASSWORD}" \
  --public

# Note: --container-port 18789 exposes the OpenClaw dashboard directly.
# Access it at: http://<PUBLIC_IP>:18789/#token=${WEB_PASSWORD}&gatewayUrl=ws://<PUBLIC_IP>:18789

# 6. Wait for endpoint to be ready
ENDPOINT_ID=$(nebius ai endpoint get-by-name $ENDPOINT_NAME --format json | jq -r '.metadata.id')
echo "Waiting for endpoint ${ENDPOINT_ID} to be ready..."
while true; do
  STATUS=$(nebius ai endpoint get $ENDPOINT_ID --format json | jq -r '.status.state')
  echo "  Status: $STATUS"
  if [ "$STATUS" = "RUNNING" ]; then
    URL=$(nebius ai endpoint get $ENDPOINT_ID --format json | jq -r '.status.url')
    echo "Endpoint ready at: $URL"
    break
  fi
  sleep 10
done
```

## Option B: GPU with Self-Hosted Inference

Runs vLLM locally on the endpoint for inference.

```bash
# Same steps 1-4 as above, then:

# 5. Create networking (required for GPU endpoints)
NETWORK_ID=$(nebius vpc network create \
  --name ${ENDPOINT_NAME}-net \
  --parent-id $PROJECT_ID \
  --format json | jq -r '.metadata.id')

SUBNET_ID=$(nebius vpc subnet create \
  --name ${ENDPOINT_NAME}-subnet \
  --parent-id $PROJECT_ID \
  --network-id $NETWORK_ID \
  --ipv4-cidr-blocks '["10.0.0.0/24"]' \
  --format json | jq -r '.metadata.id')

# 6. Deploy GPU endpoint
AUTH_TOKEN=$(openssl rand -hex 32)
echo "Auth token: $AUTH_TOKEN"

nebius ai endpoint create \
  --name "$ENDPOINT_NAME" \
  --image "$IMAGE" \
  --platform gpu-h100-sxm \
  --preset 1gpu-16vcpu-200gb \
  --container-port 8080 \
  --disk-size 100Gi \
  --shm-size 16Gi \
  --env "INFERENCE_MODEL=${MODEL}" \
  --public \
  --auth token \
  --token "$AUTH_TOKEN" \
  --subnet-id $SUBNET_ID
```

## Managing Your Endpoint

```bash
# View logs
nebius ai endpoint logs $ENDPOINT_ID --follow --since 5m --timestamps

# Stop (pause billing)
nebius ai endpoint stop $ENDPOINT_ID

# Restart
nebius ai endpoint start $ENDPOINT_ID

# Update model
nebius ai endpoint update $ENDPOINT_ID --env "INFERENCE_MODEL=new-model"

# Delete
nebius ai endpoint delete $ENDPOINT_ID
```
