# Common Errors

| Symptom | Likely cause | Checks | Fix |
|---|---|---|---|
| Admission webhook says traffic percent must sum to 100 | `spec.traffic` totals less or more than 100 | `kubectl apply --dry-run=server -f service.yaml` | Adjust traffic entries so totals equal 100 |
| `RevisionMissing` or Route not ready | Traffic points to a missing/deleted Revision | `kubectl get route -o yaml`; `kubectl get revision` | Point traffic to existing ready Revision or deploy a new one |
| Service has URL but curl fails externally | DNS/load balancer/ingress issue | `kubectl get route`; ingress service external IP; ingress logs | Fix DNS/LB/ingress config, not app manifest first |
| Service stays `RevisionMissing` or `ConfigurationReady=False` | New Revision failed to become ready | `kubectl get configuration,revision -o yaml` | Inspect Revision conditions and Pod failures |
| Pod `ImagePullBackOff` | Bad image, missing registry auth, or wrong tag | `kubectl describe pod`; events | Fix image reference or `imagePullSecrets` |
| Pod `CrashLoopBackOff` | App exits or liveness probe restarts it | `kubectl logs -p`; `kubectl describe pod` | Fix app startup, command/args, env, or liveness probe |
| Revision never ready with probe failures | App not listening on port/path, readiness too strict | Pod events, queue-proxy logs, probe config | Align `containerPort`, app bind address, and probe path |
| Requests hang or high latency after setting concurrency | Hard `containerConcurrency` too low or target too aggressive | Revision spec, queue-proxy logs, latency metrics | Raise hard limit, use soft target, or add min-scale |
| No scale to zero | `min-scale` set, global scale-to-zero disabled, or HPA class | Revision annotations, `config-autoscaler`, autoscaler class | Remove/adjust min-scale, enable global setting, use KPA where appropriate |
| Cold starts unacceptable | Service scales to zero or activation capacity too small | PodAutoscaler, min-scale, activation-scale | Set `min-scale: "1"` or tune activation/retention |
| CPU metric ignored | Using KPA class for CPU/memory metric | Revision annotations | Set HPA class and ensure resource requests/metrics support |
| RPS target ignored | Missing `autoscaling.knative.dev/metric: rps` | Revision annotations | Set both metric and target |
| `containerConcurrency` change did not affect existing Revision | Field was not changed in `spec.template`, or traffic still points to old Revision | Service YAML, Revisions, traffic | Update template and route traffic to the new Revision |
| Cluster-local service not reachable externally | `networking.knative.dev/visibility=cluster-local` label | Service/Route labels, Route URL | Remove cluster-local label or call from inside cluster |
| Private Service becomes reachable on public hostname | DomainMapping was created for a cluster-local target | `kubectl get domainmapping -A`; DNS; Service labels | Remove DomainMapping or confirm public exposure is intended |
| DomainMapping not ready | Missing ClusterDomainClaim, DNS, ingress, or TLS secret | `kubectl describe domainmapping`; `config-network`; ingress IP; certificates | Create/allow claim, fix DNS/LB, or provide valid TLS secret |
| Pod ready but Knative Revision is not ready | Queue-proxy readiness, rewritten readiness probe, ServerlessService, or ingress not ready | Revision conditions, queue-proxy logs, SKS/Ingress status | Fix the first failing Knative condition rather than only Pod state |
| `kn` command works but YAML drift appears | Imperative update changed live spec but repo YAML was not updated | `kn service describe`; `kubectl get ksvc -o yaml` | Backport live changes into declarative manifests |
| Unknown field or unsupported feature | Installed Knative version/feature flags do not support it | `kubectl explain`; CRD schema; feature ConfigMap | Remove field or enable supported feature gate |
| PVC volume rejected | PersistentVolumeClaim feature flags disabled | Admission error; `config-features` | Enable required feature flags or use supported volume types |
