---
name: kubeblocks-expose-service
metadata:
  version: "0.1.0"
description: Expose KubeBlocks database clusters externally via LoadBalancer or NodePort services using the Expose OpsRequest. Includes cloud-specific annotations for AWS NLB, Azure LB, GCP, and Alibaba Cloud. Use when the user wants to access the database from outside the Kubernetes cluster, expose a service externally, set up external connectivity, or create a public endpoint. NOT for configuring internal ClusterIP services (default behavior) or setting up TLS for connections (see configure-tls).
---

# Expose Database Service Externally

## Overview

By default, KubeBlocks database clusters are only accessible within the Kubernetes cluster. Use the `Expose` OpsRequest to create external-facing services via LoadBalancer or NodePort, allowing access from outside the cluster.

Official docs: https://kubeblocks.io/docs/preview/user_docs/connect-databases/expose-database-service

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Check current services for the cluster:

```bash
kubectl get svc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## Workflow

```
- [ ] Step 1: Choose exposure method
- [ ] Step 2: Create Expose OpsRequest
- [ ] Step 3: Verify external service
- [ ] Step 4: Connect from outside
```

## Step 1: Choose Exposure Method

| Method | Use Case | Requirements |
|--------|----------|-------------|
| LoadBalancer | Cloud environments (AWS, Azure, GCP, Alibaba) | Cloud LB controller |
| NodePort | On-premises or local clusters | None |

## Step 2: Create Expose OpsRequest

### Enable External Access

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-expose
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Expose
  expose:
  - componentName: <component>
    switch: Enable
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
```

- `switch`: `Enable` to create the service, `Disable` to remove it
- `roleSelector`: `primary` exposes only the primary node (recommended for writes)
- `serviceType`: `LoadBalancer` or `NodePort`

### Cloud Provider Annotations

Add annotations for cloud-specific load balancer configuration:

**AWS (Network Load Balancer):**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: nlb
        service.beta.kubernetes.io/aws-load-balancer-internal: "false"
```

**Azure:**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        service.beta.kubernetes.io/azure-load-balancer-internal: "false"
```

**GCP:**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        networking.gke.io/load-balancer-type: External
```

**Alibaba Cloud:**

```yaml
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
      annotations:
        service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: internet
```

### NodePort (for local / on-premises clusters)

```yaml
    services:
    - name: <cluster>-<component>-nodeport
      roleSelector: primary
      serviceType: NodePort
```

Before applying, validate with dry-run:

```bash
kubectl apply -f expose-ops.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f expose-ops.yaml
kubectl get ops <cluster>-expose -n <ns> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 1-2min | **If stuck >5min:** `kubectl describe ops <cluster>-expose -n <ns>`

### Disable External Access

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-unexpose
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Expose
  expose:
  - componentName: <component>
    switch: Disable
    services:
    - name: <cluster>-<component>-internet
      roleSelector: primary
      serviceType: LoadBalancer
```

## Step 3: Verify External Service

```bash
kubectl get svc -n <ns> | grep internet
```

Expected output (LoadBalancer):

```
mycluster-mysql-internet   LoadBalancer   10.96.x.x   a1b2c3.elb.amazonaws.com   3306:30123/TCP   2m
```

Wait for the `EXTERNAL-IP` to be assigned (may take 1-2 minutes on cloud providers).

For NodePort:

```bash
kubectl get svc -n <ns> | grep nodeport
```

```
mycluster-mysql-nodeport   NodePort   10.96.x.x   <none>   3306:31234/TCP   2m
```

## Step 4: Connect from Outside

### LoadBalancer

```bash
# MySQL
mysql -h <EXTERNAL-IP> -P 3306 -u root -p

# PostgreSQL
psql -h <EXTERNAL-IP> -p 5432 -U postgres

# Redis
redis-cli -h <EXTERNAL-IP> -p 6379 -a <password>

# MongoDB
mongosh mongodb://<user>:<password>@<EXTERNAL-IP>:27017
```

### NodePort

```bash
# Use any node's IP + the assigned NodePort
mysql -h <NODE-IP> -P <NODE-PORT> -u root -p
```

Get a node's IP:

```bash
kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}'
```

## Troubleshooting

**LoadBalancer EXTERNAL-IP stuck in `<pending>`:**
- Ensure cloud LB controller is running
- Check cloud provider quotas
- For local clusters, use MetalLB or switch to NodePort

**Connection timeout:**
- Check security groups / firewall rules on the cloud provider
- Verify the service is pointing to a healthy pod: `kubectl describe svc <svc-name> -n <ns>`
- Ensure the database is listening on the exposed port

## Additional Resources

For complete cloud provider annotations, exposing read replicas, local development without cloud LB (MetalLB, port-forward), and security considerations, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
