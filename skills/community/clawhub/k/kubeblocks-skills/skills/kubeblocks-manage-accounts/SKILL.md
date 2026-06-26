---
name: kubeblocks-manage-accounts
metadata:
  version: "0.1.0"
description: Manage database accounts and passwords for KubeBlocks clusters. Configure custom root passwords at cluster creation time and define password generation policies (length, complexity). Use when the user wants to set, change, reset, rotate, or customize database passwords, credentials, or account security policies. NOT for managing TLS/SSL certificates (see configure-tls) or for application-level database user management via SQL (connect directly to the database instead).
---

# Manage Database Accounts and Passwords

## Overview

KubeBlocks automatically creates database accounts (e.g., root, admin) when provisioning a cluster. Credentials are stored in Kubernetes Secrets. You can:

- Retrieve current credentials
- Set a custom password via Secret reference
- Configure password generation policies (length, complexity)

Official docs: https://kubeblocks.io/docs/preview/user_docs/connect-databases/overview

## Workflow

```
- [ ] Step 1: Get current credentials
- [ ] Step 2: (Optional) Set custom password or password policy
```

## Step 1: Get Current Credentials

### Find Account Secrets

KubeBlocks stores account credentials in Secrets following the naming pattern `<cluster>-<component>-account-<account>`:

```bash
kubectl get secrets -n <ns> | grep <cluster>.*account
```

Example output:

```
mycluster-mysql-account-root     Opaque   2    5m
```

### Retrieve Password

```bash
kubectl get secrets -n <ns> <cluster>-<component>-account-root \
  -o jsonpath='{.data.password}' | base64 -d
```

### Retrieve Username

```bash
kubectl get secrets -n <ns> <cluster>-<component>-account-root \
  -o jsonpath='{.data.username}' | base64 -d
```

### Quick Connection Test

```bash
# MySQL
kubectl exec -it <cluster>-<component>-0 -n <ns> -- \
  mysql -u root -p$(kubectl get secrets -n <ns> <cluster>-<component>-account-root -o jsonpath='{.data.password}' | base64 -d)

# PostgreSQL
kubectl exec -it <cluster>-<component>-0 -n <ns> -- \
  psql -U postgres

# Redis
kubectl exec -it <cluster>-<component>-0 -n <ns> -- \
  redis-cli -a $(kubectl get secrets -n <ns> <cluster>-<component>-account-root -o jsonpath='{.data.password}' | base64 -d)
```

## Step 2: Customize Passwords

### Option A: Custom Password via Secret Reference

Create a Secret with the desired password, then reference it in the Cluster CR:

**1. Create the password Secret:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <cluster>-custom-password
  namespace: <ns>
type: Opaque
stringData:
  password: "MySecureP@ssw0rd!"
```

```bash
kubectl apply -f custom-password-secret.yaml
```

**2. Reference in Cluster CR `systemAccounts`:**

```yaml
spec:
  componentSpecs:
  - name: <component>
    systemAccounts:
    - name: root
      secretRef:
        name: <cluster>-custom-password
        namespace: <ns>
```

This tells KubeBlocks to use the password from the referenced Secret instead of auto-generating one.

### Option B: Password Generation Policy

Configure automatic password generation rules in the Cluster CR:

```yaml
spec:
  componentSpecs:
  - name: <component>
    systemAccounts:
    - name: root
      passwordConfig:
        length: 16
        numDigits: 4
        numSymbols: 2
        letterCase: MixedCases
```

Password policy fields:

| Field | Description | Default |
|-------|-------------|---------|
| `length` | Total password length | 16 |
| `numDigits` | Minimum number of digits | 4 |
| `numSymbols` | Minimum number of symbols | 0 |
| `letterCase` | Letter case: `UpperCases`, `LowerCases`, `MixedCases` | `MixedCases` |

### Option C: Change Password After Cluster Creation

To change the password of an existing cluster, update the Secret directly:

```bash
# Encode the new password
NEW_PASSWORD=$(echo -n "NewSecureP@ss123!" | base64)

# Patch the existing secret
kubectl patch secret <cluster>-<component>-account-root -n <ns> \
  --type merge -p "{\"data\":{\"password\":\"$NEW_PASSWORD\"}}"
```

Then execute the password change in the database:

```bash
# MySQL
kubectl exec -it <cluster>-<component>-0 -n <ns> -- \
  mysql -u root -p<old-password> -e "ALTER USER 'root'@'%' IDENTIFIED BY 'NewSecureP@ss123!';"

# PostgreSQL
kubectl exec -it <cluster>-<component>-0 -n <ns> -- \
  psql -U postgres -c "ALTER USER postgres PASSWORD 'NewSecureP@ss123!';"
```

## Troubleshooting

**Secret not found:**
- Verify cluster and component names: `kubectl get cluster <cluster> -n <ns> -o jsonpath='{.spec.componentSpecs[*].name}'`
- Secrets are created when the cluster is first provisioned

**Password doesn't work:**
- Ensure the Secret and the actual database password are in sync
- If you changed the Secret, you also need to change the password in the database itself

**Custom password not applied on new cluster:**
- Ensure the Secret exists **before** creating the Cluster CR
- Verify the `secretRef` namespace and name are correct

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.
