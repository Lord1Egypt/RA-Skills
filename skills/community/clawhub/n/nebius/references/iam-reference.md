# IAM & Authentication Reference

## Initial Setup (Interactive)

For first-time setup with a browser available:

```bash
# Create profile (interactive — prompts for name, endpoint, auth)
nebius profile create

# Re-authenticate (if token expired — reopens browser)
nebius profile create

# Verify authentication
nebius iam whoami --format json

# Get user display name (note: deeply nested path)
nebius iam whoami --format json | jq -r '.user_profile.attributes.name'
# NOT .identity.display_name — that field doesn't exist

# Get current access token (valid 12 hours)
nebius iam get-access-token
```

**Important:** `nebius init` does NOT exist. Use `nebius profile create` instead.

## Non-Interactive Setup (CI/CD, Containers, Headless)

`nebius profile create` requires interactive input and cannot be scripted. For automated environments, write the config file directly:

```bash
mkdir -p ~/.nebius
cat > ~/.nebius/config.yaml << EOF
current-profile: default
profiles:
  default:
    endpoint: api.nebius.cloud
    auth-type: federation
    federation-endpoint: auth.nebius.com
    parent-id: <PROJECT_ID>
    tenant-id: <TENANT_ID>
EOF
```

Then authenticate once (requires browser the first time):

```bash
nebius profile create
```

After the first authentication, the token is cached in `~/.nebius/` and subsequent CLI calls work non-interactively until the token expires (12 hours).

## Service Account Auth (Fully Automated)

For fully automated environments with no browser access:

```bash
# 1. Create service account (run this once, interactively)
SA_ID=$(nebius iam service-account create \
  --name my-ci-sa \
  --parent-id <PROJECT_ID> \
  --format json | jq -r '.metadata.id')

# 2. Add to editors group for permissions
# (Do this in the Nebius web console)

# 3. Generate auth key pair
nebius iam auth-public-key generate \
  --parent-id $SA_ID \
  --format json > sa-key.json

# The sa-key.json contains the private key and key ID.
# Store these securely (e.g., as CI secrets).

# 4. Configure CLI profile with service account
# Write to ~/.nebius/config.yaml with auth-type: service-account
# and reference the private key file
```

See [Nebius docs on service account auth](https://docs.nebius.com/cli/configure) for the full configuration format.

## Profiles

```bash
# Create a profile (interactive — not scriptable)
nebius profile create --name <profile-name>

# For scripted profile creation, write directly to ~/.nebius/config.yaml
# See "Non-Interactive Setup" above

# List profiles
nebius profile list

# Set active profile
nebius config set profile <profile-name>

# Set project ID for current profile
nebius config set parent-id <PROJECT_ID>
```

Create a separate profile for each region/project:

```bash
nebius profile create --name eu-north1-prod
nebius config set parent-id <PROJECT_ID>
```

## Projects

```bash
# List all projects (scoped to current profile's parent)
nebius iam project list --format json

# List projects under a specific tenant (cross-region)
nebius iam project list --parent-id <TENANT_ID> --format json

# Get project IDs
nebius iam project list --format json | jq -r '.items[].metadata.id'

# Create a project
nebius iam project create --name "<name>" --parent-id <TENANT_ID> --format json

# Get project details
nebius iam project get --id <PROJECT_ID> --format json
```

## Service Accounts

```bash
# Create service account
nebius iam service-account create \
  --name <sa-name> \
  --parent-id <PROJECT_ID> \
  --format json

# List service accounts
nebius iam service-account list --format json

# Generate auth key pair for service account
nebius iam auth-public-key generate \
  --parent-id <SERVICE_ACCOUNT_ID> \
  --format json > sa-key.json

# Create access key
nebius iam access-key create \
  --parent-id <SERVICE_ACCOUNT_ID> \
  --format json
```

## Static Keys (for S3-compatible access)

```bash
# Issue a static key (for Object Storage S3 access)
nebius iam static-key issue \
  --parent-id <SERVICE_ACCOUNT_ID> \
  --format json
```

## Cross-Region Notes

- Each region may require its own project
- `nebius iam project list` is scoped to the active profile's parent
- Use `--parent-id <TENANT_ID>` to see all projects across regions
- Profiles should be region-specific for clarity

## Quick Reference Links

- [CLI Configuration](https://docs.nebius.com/cli/configure)
- [CLI Installation](https://docs.nebius.com/cli/install)
- [CLI Quickstart](https://docs.nebius.com/cli/quickstart)
- [gRPC API Auth](https://docs.nebius.com/grpc-api/auth)
