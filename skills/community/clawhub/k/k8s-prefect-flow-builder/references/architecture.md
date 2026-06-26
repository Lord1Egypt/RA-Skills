# Architecture

## Core relationship

- Code defines flows, tasks, reusable job logic, and `prefect.yaml`.
- CI builds and pushes the image.
- CI runs `prefect deploy --prefect-file prefect.yaml --all`.
- Prefect stores deployment definitions and creates flow runs.
- A Kubernetes work pool starts pods to execute those runs.
- Runtime env comes from Kubernetes `Secret` or `ConfigMap`, not from CI.

## Deployment lifecycle

1. Implement or update flow and deployment code.
2. CI builds and pushes an image.
3. CI exports `PREFECT_API_URL` and `PREFECT_DEPLOY_IMAGE`.
4. CI runs `prefect deploy`.
5. Prefect updates deployments.
6. A schedule or operator triggers a run later.

`prefect deploy` registers deployments. It does not execute business work.

## Runtime execution model

1. A deployment is triggered by schedule or manually.
2. Prefect creates a flow run.
3. The work pool starts a Kubernetes pod for the run.
4. The pod receives runtime env through `env_from`.
5. The flow runs tasks directly, or dispatches child flows if fan-out is needed.

## Configuration ownership

- Code defaults: light runtime defaults such as retry counts.
- `prefect.yaml`: deployment behavior and operational defaults.
- CI: deploy-time values only.
- Kubernetes: runtime business configuration and secrets.
