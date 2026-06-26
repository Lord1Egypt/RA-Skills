# Template `prefect.yaml`

Use this as a starting point and rename fields for the job you are introducing.

```yaml
name: your-project
prefect-version: 3.6.21

pull:
- prefect.deployments.steps.set_working_directory:
    directory: /app

deployments:
- name: your-job-scheduled
  tags: ["offline", "scheduled"]
  description: "Scheduled offline job."
  concurrency_limit:
    limit: 1
    collision_strategy: CANCEL_NEW
  schedule:
    cron: "0 * * * *"
    timezone: "UTC"
    active: false
  flow_name: your_flow_name
  entrypoint: src/prefect_flows/your_flow.py:your_flow
  work_pool:
    name: k8s-pool
    job_variables:
      image: "{{ $PREFECT_DEPLOY_IMAGE }}"
      env_from:
        - secretRef:
            name: your-runtime-secret
      resources:
        requests:
          cpu: "100m"
          memory: "512Mi"
        limits:
          cpu: "1"
          memory: "1Gi"
  parameters:
    execution_mode: scheduled
    run_at: null

- name: your-job-manual
  tags: ["offline", "manual"]
  description: "Manual run template."
  schedule: {}
  flow_name: your_flow_name
  entrypoint: src/prefect_flows/your_flow.py:your_flow
  work_pool:
    name: k8s-pool
    job_variables:
      image: "{{ $PREFECT_DEPLOY_IMAGE }}"
      env_from:
        - secretRef:
            name: your-runtime-secret
      resources:
        requests:
          cpu: "100m"
          memory: "1Gi"
        limits:
          cpu: "2"
          memory: "2Gi"
  parameters:
    execution_mode: manual
    run_at: null
    start_at: null
```

## Template usage notes

- Keep deployment behavior in `prefect.yaml`, not in CI shell logic.
- Keep runtime business env in Kubernetes via `env_from`.
- Use separate deployments when execution modes need different defaults or resources.
- If a flow fans out into heavy compute batches, consider a dedicated child deployment.
