# Configure TLS Reference

## TLS Modes Overview

| Mode | Issuer Name | cert-manager Required | CA Management | Best For |
|------|-------------|----------------------|---------------|----------|
| Built-in | `KubeBlocks` | Yes | Automatic (self-signed) | Dev/test, quick setup |
| User-provided | `UserProvided` | No | Manual (your PKI) | Production with existing CA |
| mTLS | Either | Depends | Server + client certs | High-security, zero-trust |

## Cluster CR TLS Configuration

### Built-in TLS (KubeBlocks-managed)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: my-cluster
  namespace: default
spec:
  componentSpecs:
    - name: mysql
      tls: true
      issuer:
        name: KubeBlocks
```

### User-provided TLS

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: my-cluster
  namespace: default
spec:
  componentSpecs:
    - name: mysql
      tls: true
      issuer:
        name: UserProvided
        secretRef:
          name: my-cluster-tls
          ca: ca.crt
          cert: tls.crt
          key: tls.key
```

## Creating TLS Secrets

### From existing certificate files

```bash
kubectl create secret generic my-cluster-tls -n default \
  --from-file=ca.crt=ca.crt \
  --from-file=tls.crt=server.crt \
  --from-file=tls.key=server.key
```

### Full certificate generation workflow

```bash
# 1. Generate CA
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key \
  -subj "/CN=KubeBlocksCA/O=MyOrg" -days 3650 -out ca.crt

# 2. Generate server key
openssl genrsa -out server.key 2048

# 3. Create SAN config (critical for proper cert validation)
cat > san.cnf <<SANEOF
[req]
distinguished_name = req_dn
req_extensions = v3_req

[req_dn]
CN = my-cluster-mysql

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = *.my-cluster-mysql-headless.default.svc.cluster.local
DNS.2 = *.my-cluster-mysql.default.svc.cluster.local
DNS.3 = my-cluster-mysql-headless.default.svc.cluster.local
DNS.4 = localhost
IP.1 = 127.0.0.1
SANEOF

# 4. Generate CSR and sign
openssl req -new -key server.key -subj "/CN=my-cluster-mysql" \
  -config san.cnf -out server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 \
  -extensions v3_req -extfile san.cnf

# 5. Create secret
kubectl create secret generic my-cluster-tls -n default \
  --from-file=ca.crt=ca.crt \
  --from-file=tls.crt=server.crt \
  --from-file=tls.key=server.key
```

### Client certificate generation (for mTLS)

```bash
openssl genrsa -out client.key 2048
openssl req -new -key client.key -subj "/CN=dbclient/O=MyOrg" -out client.csr
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365
```

## Engine-Specific TLS Details

### MySQL

- Mount path: `/var/run/secrets/tls/`
- Config parameters set automatically: `ssl_ca`, `ssl_cert`, `ssl_key`, `require_secure_transport`
- Verify TLS:
  ```sql
  SHOW VARIABLES LIKE '%ssl%';
  SHOW STATUS LIKE 'Ssl_cipher';
  ```
- Connect with TLS:
  ```bash
  mysql -h <host> -P 3306 -u root -p --ssl-mode=REQUIRED \
    --ssl-ca=ca.crt --ssl-cert=client.crt --ssl-key=client.key
  ```
- Require X509 for specific users:
  ```sql
  CREATE USER 'secureuser'@'%' REQUIRE X509;
  ALTER USER 'secureuser'@'%' REQUIRE X509;
  ```

### PostgreSQL

- Mount path: `/var/run/secrets/tls/`
- Config parameters set automatically: `ssl = on`, `ssl_ca_file`, `ssl_cert_file`, `ssl_key_file`
- Verify TLS:
  ```sql
  SHOW ssl;
  SELECT * FROM pg_stat_ssl;
  ```
- Connect with TLS:
  ```bash
  psql "host=<host> port=5432 user=postgres dbname=postgres \
    sslmode=verify-full sslrootcert=ca.crt sslcert=client.crt sslkey=client.key"
  ```
- pg_hba.conf for mTLS: set `clientcert=verify-full` via reconfigure-parameters

### Redis

- Redis TLS support depends on the addon version
- Config parameters: `tls-port`, `tls-cert-file`, `tls-key-file`, `tls-ca-cert-file`
- Connect with TLS:
  ```bash
  redis-cli -h <host> -p 6380 --tls \
    --cacert ca.crt --cert client.crt --key client.key
  ```

### MongoDB

- Config parameters set automatically: `net.tls.mode`, `net.tls.certificateKeyFile`, `net.tls.CAFile`
- Connect with TLS:
  ```bash
  mongosh "mongodb://<host>:27017/?tls=true" \
    --tlsCAFile ca.crt --tlsCertificateKeyFile client.pem
  ```

## cert-manager Prerequisites

### Install cert-manager

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
```

### Verify cert-manager

```bash
kubectl get pods -n cert-manager
# Expected: cert-manager, cert-manager-cainjector, cert-manager-webhook all Running
```

## Certificate Inspection Commands

```bash
# View mounted certificates in a pod
kubectl exec -it <pod> -n <ns> -- ls -la /var/run/secrets/tls/

# View certificate details
kubectl exec -it <pod> -n <ns> -- \
  openssl x509 -in /var/run/secrets/tls/tls.crt -text -noout

# Check certificate expiration
kubectl exec -it <pod> -n <ns> -- \
  openssl x509 -in /var/run/secrets/tls/tls.crt -enddate -noout

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt
```

## Troubleshooting

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pod CrashLoopBackOff after enabling TLS | Secret missing or wrong key names | Verify secret exists with `ca.crt`, `tls.crt`, `tls.key` |
| `certificate verify failed` | CA mismatch between client and server | Ensure client uses the same CA that signed the server cert |
| `SSL: no alternative certificate subject name matches` | Missing SAN entries | Regenerate cert with correct DNS SANs for the headless service |
| cert-manager not issuing certificates | cert-manager not installed or not running | Install cert-manager and verify pods are running |
| Certificate expired | Built-in: cert-manager renewal failed; User-provided: manual renewal needed | Check cert-manager logs or regenerate certs |

## Documentation Links

| Resource | URL |
|----------|-----|
| MySQL TLS overview | https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/07-tls/01-tls-overview |
| MySQL custom TLS certs | https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/07-tls/02-tls-custom-cert |
| MySQL mTLS | https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/07-tls/03-mtls |
| PostgreSQL TLS overview | https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/07-tls/01-tls-overview |
| PostgreSQL custom TLS | https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/07-tls/02-tls-custom-cert |
