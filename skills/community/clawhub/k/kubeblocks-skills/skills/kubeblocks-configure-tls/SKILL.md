---
name: kubeblocks-configure-tls
metadata:
  version: "0.1.0"
description: Configure TLS encryption for KubeBlocks database clusters. Supports built-in certificates (auto-managed via cert-manager), user-provided certificates (bring your own CA/PKI), and mTLS (mutual TLS with client certificates). Use when the user wants to enable TLS, SSL, encryption, HTTPS, or secure database connections with certificates. NOT for managing database passwords (see manage-accounts) or exposing services externally (see expose-service).
---

# Configure TLS Encryption

## Overview

KubeBlocks supports TLS encryption for database connections. Three modes are available:

- **Built-in TLS**: KubeBlocks generates and manages certificates automatically (requires cert-manager)
- **User-provided TLS**: Use your own CA and certificates
- **mTLS (Mutual TLS)**: Both server and client authenticate with certificates

Official docs: https://kubeblocks.io/docs/preview/user_docs/connect-databases/tls-connection

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

For built-in TLS mode, verify cert-manager is installed:

```bash
kubectl get pods -n cert-manager
```

## Workflow

```
- [ ] Step 1: Choose TLS mode
- [ ] Step 2: Configure TLS in Cluster CR
- [ ] Step 3: Verify TLS connection
```

## Step 1: Choose TLS Mode

| Mode | Certificate Management | Use Case |
|------|----------------------|----------|
| Built-in (KubeBlocks) | Automatic via cert-manager | Quick setup, dev/test |
| User-provided | Manual (bring your own CA) | Production with existing PKI |
| mTLS | Manual + client certs | High-security environments |

### Why Use cert-manager for Built-in TLS?

cert-manager automates the entire certificate lifecycle — issuance, renewal, and rotation — so you never end up with an expired certificate causing a production outage at 3 AM. Manually managed certificates are fine when you already have a PKI team and established rotation processes, but for most users, cert-manager eliminates a whole class of operational risk. KubeBlocks integrates with cert-manager's `Issuer` and `Certificate` CRDs, so enabling TLS is a single field toggle rather than a multi-step manual process.

TLS docs: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/07-tls/01-tls-overview

### Prerequisites for Built-in TLS

The built-in mode requires **cert-manager**. Install it if not present:

```bash
# Check if cert-manager is installed
kubectl get pods -n cert-manager

# Install cert-manager if needed
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
```

Wait for cert-manager pods to be ready:

```bash
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
```

## Step 2: Configure TLS

### Option A: Built-in TLS (KubeBlocks Managed)

Add TLS configuration to the component spec in the Cluster CR:

```yaml
spec:
  componentSpecs:
  - name: <component>
    tls: true
    issuer:
      name: KubeBlocks
```

This tells KubeBlocks to use cert-manager to automatically generate a self-signed CA and server certificates.

### Option B: User-Provided Certificates

**1. Generate certificates (if you don't have them):**

```bash
# Generate CA key and certificate
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -subj "/CN=MyDatabaseCA" -days 3650 -out ca.crt

# Generate server key and CSR
openssl genrsa -out server.key 2048
openssl req -new -key server.key -subj "/CN=<cluster>-<component>" -out server.csr

# Sign server certificate with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 \
  -extfile <(printf "subjectAltName=DNS:*.<cluster>-<component>-headless.<ns>.svc.cluster.local,DNS:*.<cluster>-<component>.<ns>.svc.cluster.local")
```

**2. Create TLS Secret:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <cluster>-tls
  namespace: <ns>
type: kubernetes.io/tls
data:
  ca.crt: <base64-encoded-ca.crt>
  tls.crt: <base64-encoded-server.crt>
  tls.key: <base64-encoded-server.key>
```

Or create it with kubectl:

```bash
kubectl create secret generic <cluster>-tls -n <ns> \
  --from-file=ca.crt=ca.crt \
  --from-file=tls.crt=server.crt \
  --from-file=tls.key=server.key
```

**3. Reference in Cluster CR:**

```yaml
spec:
  componentSpecs:
  - name: <component>
    tls: true
    issuer:
      name: UserProvided
      secretRef:
        name: <cluster>-tls
        ca: ca.crt
        cert: tls.crt
        key: tls.key
```

### Option C: mTLS (Mutual TLS)

mTLS uses the same server-side TLS configuration (Option A or B), plus requires client certificates.

**1. Configure server-side TLS** using Option A or B above.

**2. Generate client certificates:**

```bash
# Generate client key and CSR
openssl genrsa -out client.key 2048
openssl req -new -key client.key -subj "/CN=dbclient" -out client.csr

# Sign client certificate with the same CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365
```

**3. Configure the database to require client certificates:**

```bash
# MySQL: create user requiring X509
kubectl exec -it <pod> -n <ns> -- mysql -u root -p --ssl -e \
  "CREATE USER 'secureuser'@'%' REQUIRE X509; GRANT ALL ON *.* TO 'secureuser'@'%';"

# PostgreSQL: edit pg_hba.conf to require clientcert=verify-full
# This is typically handled via parameter reconfiguration
```

## Step 3: Verify TLS Connection

### Check TLS is Enabled

```bash
# MySQL
kubectl exec -it <pod> -n <ns> -- mysql -u root -p --ssl -e "SHOW VARIABLES LIKE '%ssl%';"

# PostgreSQL
kubectl exec -it <pod> -n <ns> -- psql -U postgres -c "SHOW ssl;"
```

### Connect with TLS from Outside

```bash
# MySQL with TLS
mysql -h <host> -P 3306 -u root -p --ssl-mode=REQUIRED \
  --ssl-ca=ca.crt --ssl-cert=client.crt --ssl-key=client.key

# PostgreSQL with TLS
psql "host=<host> port=5432 user=postgres sslmode=verify-full sslrootcert=ca.crt sslcert=client.crt sslkey=client.key"
```

### Verify Certificate Details

```bash
# Check the mounted certificates in the pod
kubectl exec -it <pod> -n <ns> -- ls -la /var/run/secrets/tls/

# View certificate info
kubectl exec -it <pod> -n <ns> -- openssl x509 -in /var/run/secrets/tls/tls.crt -text -noout
```

## Troubleshooting

**TLS not enabling (pods crashing):**
- Check cert-manager is running (for built-in mode)
- Verify the TLS Secret exists and has correct keys: `kubectl describe secret <cluster>-tls -n <ns>`
- Check pod logs: `kubectl logs <pod> -n <ns>`

**Certificate expired:**
- Built-in mode: cert-manager handles renewal automatically
- User-provided: regenerate certificates and update the Secret

**Client cannot connect with TLS:**
- Verify the CA certificate matches: client's `ca.crt` must match the server's CA
- Check SAN (Subject Alternative Names) in the server certificate

## Additional Resources

For engine-specific TLS configuration details, full certificate generation workflows with SANs, and troubleshooting matrix, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
