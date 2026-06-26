# Container Registry Reference

## Create Registry

```bash
nebius registry create \
  --name <registry-name> \
  --parent-id <PROJECT_ID> \
  --format json
```

## List Registries

```bash
nebius registry list --format json
```

## Docker Authentication

Authenticate Docker to push/pull images from Nebius Container Registry:

```bash
# Login using IAM token
nebius iam get-access-token | docker login cr.<REGION>.nebius.cloud \
  --username iam \
  --password-stdin
```

Replace `<REGION>` with:
- `eu-north1` for Finland
- `eu-west1` for Paris
- `us-central1` for US

## Build and Push Image

```bash
# Set registry URL
REGISTRY_URL="cr.<REGION>.nebius.cloud/<REGISTRY_ID>"

# Build image
docker build -t ${REGISTRY_URL}/my-app:latest .

# Push image
docker push ${REGISTRY_URL}/my-app:latest
```

## Full Workflow (Create Registry + Push Image)

```bash
# 1. Create registry
REGISTRY_ID=$(nebius registry create \
  --name my-registry \
  --parent-id $PROJECT_ID \
  --format json | jq -r '.metadata.id')

# 2. Authenticate Docker
nebius iam get-access-token | docker login cr.eu-north1.nebius.cloud \
  --username iam \
  --password-stdin

# 3. Build and push
IMAGE="cr.eu-north1.nebius.cloud/${REGISTRY_ID}/my-app:latest"
docker build -t $IMAGE .
docker push $IMAGE

echo "Image pushed: $IMAGE"
```

## Check for Existing Registry

```bash
EXISTING=$(nebius registry list --format json \
  | jq -r '.items[] | select(.metadata.name=="my-registry") | .metadata.id')
if [ -n "$EXISTING" ]; then
  echo "Registry already exists: $EXISTING"
  REGISTRY_ID=$EXISTING
fi
```

## Image Management

```bash
# List images in registry
nebius registry image list --parent-id <REGISTRY_ID> --format json

# Delete image
nebius registry image delete --id <IMAGE_ID>
```
