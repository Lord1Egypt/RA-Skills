# Deployment Patterns

## Single deployment

Use one deployment when:
- scheduled and manual runs share a similar resource profile;
- one operational identity is enough;
- there is no need to split scaling or failure boundaries.

## Separate scheduled and manual deployments

Split deployments when:
- scheduled runs are lightweight but manual or historical runs are heavier;
- schedules and manual triggers need different defaults;
- concurrency or resource policy should differ.

## Parent and child deployments

Use a parent flow plus child flow when:
- one orchestration run must fan out into multiple independent batches;
- child work needs its own pod resources;
- child failures should be isolated and visible.

Keep deployment names in `prefect.yaml`. Use deployment names for operational identity and flow names for logical identity.

## Work pool and runtime env

In this repository, deployments should rely on:
- `work_pool.name` in `prefect.yaml`;
- `job_variables.image: "{{ $PREFECT_DEPLOY_IMAGE }}"`;
- `job_variables.env_from` pointing to Kubernetes runtime config.

The work pool `base_job_template` must support `env_from` and map it to Kubernetes `envFrom`.

## Concurrency policies

Use deployment-level `concurrency_limit` when one deployment must serialize itself.
Typical pattern:

```yaml
concurrency_limit:
  limit: 1
  collision_strategy: CANCEL_NEW
```

This applies to one deployment only. Do not treat it as a cross-deployment global lock.
