# Expose Service Reference

## OpsRequest API Reference

Full API docs: https://kubeblocks.io/docs/preview/user_docs/references/api-reference/operations

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

## Service Types

| Type | External IP | Port Range | Use Case |
|------|------------|------------|----------|
| LoadBalancer | Cloud LB assigns public/private IP | Any | Cloud environments (AWS, Azure, GCP, Alibaba) |
| NodePort | Node IP + assigned port | 30000-32767 | On-premises, bare-metal, local dev |
| ClusterIP | None (internal only) | Any | Default, no action needed |

## Role Selectors

| roleSelector | Behavior | Use Case |
|-------------|----------|----------|
| `primary` | Routes to the current primary/leader node | Read-write access, single endpoint |
| (omitted) | Routes to all pods in the component | Read scaling with client-side routing |

## Cloud Provider Annotations

### AWS (Network Load Balancer)

```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: nlb
  service.beta.kubernetes.io/aws-load-balancer-internal: "false"
```

Internal NLB (VPC-only access):

```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: nlb
  service.beta.kubernetes.io/aws-load-balancer-internal: "true"
```

### Azure

```yaml
annotations:
  service.beta.kubernetes.io/azure-load-balancer-internal: "false"
```

Internal LB:

```yaml
annotations:
  service.beta.kubernetes.io/azure-load-balancer-internal: "true"
```

### GCP

```yaml
annotations:
  networking.gke.io/load-balancer-type: External
```

Internal LB:

```yaml
annotations:
  networking.gke.io/load-balancer-type: Internal
```

### Alibaba Cloud

Internet-facing:

```yaml
annotations:
  service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: internet
```

Intranet (VPC-only):

```yaml
annotations:
  service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: intranet
```

## Engine-Specific Default Ports

| Engine | Default Port | Service Name Pattern |
|--------|-------------|---------------------|
| MySQL | 3306 | `<cluster>-mysql-internet` |
| PostgreSQL | 5432 | `<cluster>-postgresql-internet` |
| Redis | 6379 | `<cluster>-redis-internet` |
| MongoDB | 27017 | `<cluster>-mongodb-internet` |
| Kafka | 9092 | `<cluster>-kafka-combine-internet` |
| Elasticsearch | 9200 | `<cluster>-elasticsearch-internet` |

## Exposing Multiple Components

You can expose multiple components in a single OpsRequest:

```yaml
spec:
  clusterName: my-cluster
  type: Expose
  expose:
    - componentName: mysql
      switch: Enable
      services:
        - name: my-cluster-mysql-internet
          roleSelector: primary
          serviceType: LoadBalancer
    - componentName: proxysql
      switch: Enable
      services:
        - name: my-cluster-proxysql-internet
          serviceType: LoadBalancer
```

## Exposing Read Replicas

To expose read replicas separately for read-scaling:

```yaml
  expose:
    - componentName: mysql
      switch: Enable
      services:
        - name: my-cluster-mysql-primary
          roleSelector: primary
          serviceType: LoadBalancer
        - name: my-cluster-mysql-readonly
          roleSelector: secondary
          serviceType: LoadBalancer
```

## Connection Examples After Exposure

### LoadBalancer

```bash
# Get the external IP
kubectl get svc -n <ns> | grep internet

# MySQL
mysql -h <EXTERNAL-IP> -P 3306 -u root -p

# PostgreSQL
psql -h <EXTERNAL-IP> -p 5432 -U postgres

# Redis
redis-cli -h <EXTERNAL-IP> -p 6379 -a <password>

# MongoDB
mongosh "mongodb://<user>:<password>@<EXTERNAL-IP>:27017"
```

### NodePort

```bash
# Get node IP and assigned port
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
NODE_PORT=$(kubectl get svc <svc-name> -n <ns> -o jsonpath='{.spec.ports[0].nodePort}')

mysql -h $NODE_IP -P $NODE_PORT -u root -p
```

## Local Development (No Cloud LB)

For local Kind/Minikube/k3d clusters without a cloud LB controller:

**Option 1: Use NodePort instead of LoadBalancer**

**Option 2: Install MetalLB for local LoadBalancer support**

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml
kubectl wait --for=condition=Ready pods --all -n metallb-system --timeout=120s
```

Then configure an IP address pool matching your local network.

**Option 3: Use kubectl port-forward (simplest for development)**

```bash
kubectl port-forward svc/<cluster>-<component> -n <ns> <local-port>:<db-port>
```

## Security Considerations

- LoadBalancer services are **publicly accessible** by default on cloud providers
- Use internal LB annotations for VPC-only access when possible
- Always combine with TLS (see configure-tls skill) for encrypted connections
- Set firewall rules / security groups to restrict source IPs
- Consider using Kubernetes NetworkPolicies for additional access control

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `EXTERNAL-IP` stuck in `<pending>` | No LB controller (local cluster) or cloud quota | Use NodePort, install MetalLB, or check cloud quotas |
| Connection timeout | Firewall/security group blocking | Open the database port in cloud security groups |
| Service exists but no endpoints | Pod selector mismatch or pods not running | Check pod status and labels |
| Wrong node receives traffic (NodePort) | Normal — NodePort routes via kube-proxy | Use `externalTrafficPolicy: Local` for direct routing |

## Documentation Links

| Resource | URL |
|----------|-----|
| MySQL expose service | https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/04-operations/05-manage-loadbalancer |
| PostgreSQL expose service | https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/04-operations/05-manage-loadbalancer |
| Redis expose service | https://kubeblocks.io/docs/preview/kubeblocks-for-redis/04-operations/05-manage-loadbalancer |
| MongoDB expose service | https://kubeblocks.io/docs/preview/kubeblocks-for-mongodb/04-operations/05-manage-loadbalancer |
| Kafka expose service | https://kubeblocks.io/docs/preview/kubeblocks-for-kafka/04-operations/05-manage-loadbalancer |
| Redis network modes blog | https://kubeblocks.io/blog/5-network-modes-for-kubeblocks-for-redis |
| Operations API | https://kubeblocks.io/docs/preview/user_docs/references/api-reference/operations |
