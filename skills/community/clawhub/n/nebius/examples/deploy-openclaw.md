# Deploy OpenClaw on Nebius

Follow the [nebius-skill SKILL.md](../SKILL.md) to deploy OpenClaw as a serverless endpoint and connect via SSH.

## Prerequisites

**1. Install the Nebius CLI and authenticate:**
```bash
curl -sSL https://storage.eu-north1.nebius.cloud/cli/install.sh | bash
exec -l $SHELL
nebius profile create   # opens browser — log in with your Nebius account
```

**2. Get your Token Factory API key** from https://tokenfactory.nebius.com (starts with `v1.`).

**3. Confirm your SSH public key exists** (this is the key the endpoint will accept):
```bash
cat ~/.ssh/id_ed25519.pub || cat ~/.ssh/id_rsa.pub
```
If you don't have one: `ssh-keygen -t ed25519`

## Deploy

```bash
PASSWORD=$(openssl rand -hex 16)
echo "Save this password: $PASSWORD"

nebius ai endpoint create \
  --name openclaw-agent \
  --image ghcr.io/colygon/openclaw-serverless:latest \
  --platform cpu-e2 \
  --preset 2vcpu-8gb \
  --container-port 8080 \
  --container-port 18789 \
  --disk-size 250Gi \
  --env "TOKEN_FACTORY_API_KEY=<your-v1-key>" \
  --env "TOKEN_FACTORY_URL=https://api.tokenfactory.nebius.com/v1" \
  --env "INFERENCE_MODEL=zai-org/GLM-5" \
  --env "OPENCLAW_WEB_PASSWORD=$PASSWORD" \
  --public \
  --ssh-key "$(cat ~/.ssh/id_ed25519.pub)" \
  --format json
```

Wait 1-3 minutes, then get the public IP:
```bash
nebius ai endpoint get-by-name openclaw-agent --format json \
  | jq -r '.status.instances[0].public_ip' | cut -d/ -f1
```

## Connect

**SSH into the endpoint:**
```bash
nebius ai endpoint ssh <ENDPOINT_ID>
# or: ssh nebius@<PUBLIC_IP>
```

**Set up the dashboard tunnel** (from your local machine):
```bash
ssh -f -N -o StrictHostKeyChecking=no -L 28789:<PUBLIC_IP>:18789 nebius@<PUBLIC_IP>
```

**Approve device pairing** (first time only):
```bash
ssh nebius@<PUBLIC_IP> \
  "sudo docker exec \$(sudo docker ps -q | head -1) \
   env OPENCLAW_GATEWAY_TOKEN=$PASSWORD openclaw devices approve --latest"
```

**Open the dashboard:**
```
http://localhost:28789/#token=<PASSWORD>&gatewayUrl=ws://localhost:28789
```

## Headless Environments (Claude Code on the web, CI/CD)

If you can't run `nebius profile create` interactively, get your IAM token on your local machine and pass it:
```bash
# On your local machine:
nebius iam get-access-token

# In the headless environment:
export NEBIUS_IAM_TOKEN="<paste-token>"
```

> **IAM token** (`nebius iam get-access-token`) = Nebius Cloud CLI auth for creating endpoints.
> **Token Factory API key** (`v1.xxx`) = model inference inside the container. These are different credentials.

## Notes

- **Public IP quota** is 3 per tenant. Stopped endpoints still hold IPs. Delete unused ones: `nebius ai endpoint delete <ID>`
- **SSH key is set at creation only.** Use `--ssh-key` with a key from your local machine, not a generated/remote key.
- **eu-west1 uses `cpu-d3`**, not `cpu-e2`. See [SKILL.md](../SKILL.md) for region details.
- **Model IDs** use Token Factory format: `zai-org/GLM-5`, not HuggingFace format.
