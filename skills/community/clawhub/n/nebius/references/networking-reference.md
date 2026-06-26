# Networking (VPC) Reference

## Create Network

```bash
nebius vpc network create \
  --name <network-name> \
  --parent-id <PROJECT_ID> \
  --format json
```

## Create Subnet

```bash
nebius vpc subnet create \
  --name <subnet-name> \
  --parent-id <PROJECT_ID> \
  --network-id <NETWORK_ID> \
  --ipv4-cidr-blocks '["10.0.0.0/24"]' \
  --format json
```

## List and Get

```bash
# List networks
nebius vpc network list --format json

# List subnets
nebius vpc subnet list --format json

# Get subnet by name
nebius vpc subnet get-by-name <subnet-name> --format json
```

## Security Groups

```bash
# Create security group
nebius vpc security-group create \
  --name <sg-name> \
  --parent-id <PROJECT_ID> \
  --format json

# List security groups
nebius vpc security-group list --format json

# Create security rule (allow inbound SSH)
nebius vpc security-rule create \
  --parent-id <SECURITY_GROUP_ID> \
  --direction ingress \
  --protocol tcp \
  --port 22 \
  --cidr "0.0.0.0/0" \
  --format json
```

## Public IP Allocations

```bash
# Allocate public IP
nebius vpc allocation create \
  --parent-id <PROJECT_ID> \
  --format json

# List allocations
nebius vpc allocation list --format json
```

## Typical Setup Pattern

Most deployments need a network + subnet before creating VMs or endpoints:

```bash
# 1. Create network
NETWORK_ID=$(nebius vpc network create \
  --name my-network \
  --parent-id $PROJECT_ID \
  --format json | jq -r '.metadata.id')

# 2. Create subnet
SUBNET_ID=$(nebius vpc subnet create \
  --name my-subnet \
  --parent-id $PROJECT_ID \
  --network-id $NETWORK_ID \
  --ipv4-cidr-blocks '["10.0.0.0/24"]' \
  --format json | jq -r '.metadata.id')

echo "Network: $NETWORK_ID"
echo "Subnet: $SUBNET_ID"
```

## Check for Existing Resources

Before creating, check if resources already exist:

```bash
# Check for existing subnets
EXISTING=$(nebius vpc subnet list --format json | jq -r '.items[] | select(.metadata.name=="my-subnet") | .metadata.id')
if [ -n "$EXISTING" ]; then
  echo "Subnet already exists: $EXISTING"
  SUBNET_ID=$EXISTING
fi
```
