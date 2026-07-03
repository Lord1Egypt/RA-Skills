# Job & CronJob Management

## Overview

Jobs run one-time batch tasks to completion. CronJobs schedule Jobs on a recurring timetable. Both ensure work finishes with retry and cleanup controls.

## Job Operations

| Operation | Command |
|-----------|---------|
| Create from YAML | `kubectl --kubeconfig=<kubeconfig-path> apply -f job.yaml -n <namespace>` |
| Create inline | `kubectl --kubeconfig=<kubeconfig-path> create job <name> --image=<image> -n <namespace>` |
| Get status | `kubectl --kubeconfig=<kubeconfig-path> get jobs -n <namespace>` |
| View logs | `kubectl --kubeconfig=<kubeconfig-path> logs job/<name> -n <namespace>` |
| Delete | `kubectl --kubeconfig=<kubeconfig-path> delete job <name> -n <namespace>` |

## CronJob Operations

| Operation | Command |
|-----------|---------|
| Create from YAML | `kubectl --kubeconfig=<kubeconfig-path> apply -f cronjob.yaml -n <namespace>` |
| Get/list | `kubectl --kubeconfig=<kubeconfig-path> get cronjobs -n <namespace>` |
| Suspend | `kubectl --kubeconfig=<kubeconfig-path> patch cronjob <name> --type merge --patch-file=suspend.json -n <namespace>` |
| Resume | `kubectl --kubeconfig=<kubeconfig-path> patch cronjob <name> --type merge --patch-file=resume.json -n <namespace>` |
| Delete | `kubectl --kubeconfig=<kubeconfig-path> delete cronjob <name> -n <namespace>` |

## Common Scenarios

### One-time batch job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
spec:
  backoffLimit: 3
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: migrator
        image: migrator:latest
        command: ["./migrate.sh"]
```

```bash
kubectl --kubeconfig=<kubeconfig-path> apply -f job.yaml -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> get jobs -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> logs job/data-migration -n <namespace>
```

### Scheduled cleanup CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: cleaner
            image: cleaner:latest
            command: ["./cleanup.sh"]
```

```bash
kubectl --kubeconfig=<kubeconfig-path> apply -f cronjob.yaml -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> get cronjobs -n <namespace>
```

### Suspend CronJob for maintenance

> **Note**: On Windows (PowerShell), inline `-p` JSON patches have escaping issues. Use `--patch-file` instead.

Create patch files first:

```bash
# suspend.json
echo '{"spec":{"suspend":true}}' > suspend.json

# resume.json
echo '{"spec":{"suspend":false}}' > resume.json
```

Apply patches:

```bash
kubectl --kubeconfig=<kubeconfig-path> patch cronjob cleanup --type merge --patch-file=suspend.json -n <namespace>
kubectl --kubeconfig=<kubeconfig-path> patch cronjob cleanup --type merge --patch-file=resume.json -n <namespace>
```

On Linux/macOS bash, inline `-p` also works:

```bash
kubectl --kubeconfig=<kubeconfig-path> patch cronjob cleanup -p '{"spec":{"suspend":true}}' -n <namespace>
```