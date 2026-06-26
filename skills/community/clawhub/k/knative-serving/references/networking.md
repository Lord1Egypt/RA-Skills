# Networking

## Contents

- [Request path](#request-path)
- [URLs and routes](#urls-and-routes)
- [Private and cluster-local services](#private-and-cluster-local-services)
- [Domains](#domains)
- [Ingress class](#ingress-class)
- [TLS](#tls)
- [Debugging network reachability](#debugging-network-reachability)

## Request path

Typical Serving request flow:

external client -> ingress gateway/controller -> Knative Route/Ingress -> Activator if scaled to zero or overloaded -> queue-proxy -> user container.

The exact ingress layer depends on the installed networking provider, commonly Kourier, Istio, or Contour.

## URLs and routes

```bash
kubectl get ksvc <service> -n <namespace>
kubectl get route <service> -n <namespace>
kn service describe <service> -n <namespace> -o url
```

Route status is the source for URL readiness and traffic targets.

## Private and cluster-local services

Make a Service cluster-local:

```yaml
metadata:
  labels:
    networking.knative.dev/visibility: cluster-local
```

Cluster-local Services are intended for in-cluster callers and should return a `.svc.cluster.local` URL. Current docs label the Knative Service or Route:

```bash
kubectl label kservice <service> networking.knative.dev/visibility=cluster-local -n <namespace>
kubectl label route <route> networking.knative.dev/visibility=cluster-local -n <namespace>
```

Tagged traffic targets can also create Kubernetes Services for in-cluster access. Label the generated Kubernetes Service only when that is the object you intend to constrain.

## Domains

Default domains are controlled by `config-domain`. Per-host custom domains use `DomainMapping` when the feature is installed/enabled:

```bash
kubectl get configmap config-domain -n knative-serving -o yaml
kubectl get domainmapping -A
kubectl explain domainmapping.spec
```

DomainMapping maps a single non-wildcard domain to an addressable target such as a Knative Service or Route:

```yaml
apiVersion: serving.knative.dev/v1beta1
kind: DomainMapping
metadata:
  name: app.example.com
  namespace: default
spec:
  ref:
    apiVersion: serving.knative.dev/v1
    kind: Service
    name: hello
```

Safety:

- Confirm DNS points at the cluster ingress.
- Confirm ClusterDomainClaim/autocreate policy if the cluster requires it.
- Do not map a public domain to a private Service unless public access is intended.
- Add `spec.tls.secretName` only when a valid TLS secret exists for that hostname.

`kn` can manage DomainMappings:

```bash
kn domain create app.example.com --ref ksvc:hello --namespace default
kn domain list -A
kn domain describe app.example.com -n default
```

## Ingress class

Some clusters allow per-Service ingress class:

```yaml
metadata:
  annotations:
    networking.knative.dev/ingress-class: "kourier.ingress.networking.knative.dev"
```

Confirm supported values with cluster configuration:

```bash
kubectl get configmap config-network -n knative-serving -o yaml
kubectl get pods -n knative-serving
kubectl get pods -A | grep -E 'kourier|istio|contour'
```

## TLS

TLS may be provided externally by the ingress/load balancer or by Knative integration with certificate providers. Check:

```bash
kubectl get configmap config-network -n knative-serving -o yaml
kubectl get certificates -A
kubectl get challenges -A
kubectl get domainmapping -A
```

Do not assume cert-manager is installed.

Cluster-local domain TLS and system-internal TLS can be experimental depending on version and provider. Verify `config-network`, cert-manager integration, and whether Kourier/Istio/Contour support the requested mode before enabling it.

## Debugging network reachability

```bash
kubectl get route <service> -n <namespace> -o yaml
kubectl get ingress -n <namespace>
kubectl get sks -n <namespace>
kubectl get svc -A | grep -E 'ingress|kourier|istio|contour'
```

For Istio:

```bash
kubectl get svc -n istio-system istio-ingressgateway
kubectl describe svc -n istio-system istio-ingressgateway
```

For Kourier:

```bash
kubectl get svc -n kourier-system
kubectl get pods -n kourier-system
```

When the external URL fails but Pods are ready, check DNS, load balancer external IP, Route status, and ingress controller logs before changing the Service template.
