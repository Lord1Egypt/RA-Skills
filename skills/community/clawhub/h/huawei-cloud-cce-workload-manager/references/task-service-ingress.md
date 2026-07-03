# Service & Ingress Management

## Overview

Services provide stable internal networking for pod groups. Ingress exposes HTTP/HTTPS routes from outside the cluster to Services, with host and path-based routing.

## Service Operations

| Operation | Command |
|-----------|---------|
| Create ClusterIP | `kubectl --kubeconfig=<kubeconfig-path> expose deployment <name> --port=80 --target-port=8080 -n <namespace>` |
| Create NodePort/LoadBalancer | `kubectl --kubeconfig=<kubeconfig-path> expose deployment <name> --type=LoadBalancer --port=80 -n <namespace>` |
| Create from YAML | `kubectl --kubeconfig=<kubeconfig-path> apply -f service.yaml -n <namespace>` |
| Get/describe/delete | `kubectl --kubeconfig=<kubeconfig-path> get svc -n <namespace>` / `describe svc <name>` / `delete svc <name>` |

## Ingress Operations

| Operation | Command |
|-----------|---------|
| Create from YAML | `kubectl --kubeconfig=<kubeconfig-path> apply -f ingress.yaml -n <namespace>` |
| Get/describe | `kubectl --kubeconfig=<kubeconfig-path> get ingress -n <namespace>` / `describe ingress <name>` |
| Delete | `kubectl --kubeconfig=<kubeconfig-path> delete ingress <name> -n <namespace>` |

## Common Scenarios

### Expose deployment with ClusterIP

```bash
kubectl --kubeconfig=<kubeconfig-path> expose deployment api-server --port=80 --target-port=8080 -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> get svc -n <namespace>
```

### LoadBalancer for external access

```bash
kubectl --kubeconfig=<kubeconfig-path> expose deployment web-app --type=LoadBalancer --port=80 --target-port=8080 -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> get svc web-app -n <namespace>
```

### Ingress with multiple paths

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-path
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-server
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app
            port:
              number: 80
```

```bash
kubectl --kubeconfig=<kubeconfig-path> apply -f ingress.yaml -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> describe ingress multi-path -n <namespace>
```

### Complex service from YAML

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-server
spec:
  type: ClusterIP
  selector:
    app: api-server
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: metrics
    port: 9090
    targetPort: 9090
```

```bash
kubectl --kubeconfig=<kubeconfig-path> apply -f service.yaml -n <namespace>
```