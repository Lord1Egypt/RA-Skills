# Resources and Concurrency

## Requests vs limits

- `requests` are the resources Kubernetes tries to reserve for the pod.
- `limits` are the maximum resources the container may consume.
- Exceeding `limits.memory` can OOM-kill the pod.
- Exceeding `limits.cpu` throttles the container.

## Starting pattern

- Parent or orchestration flows usually need low CPU and memory.
- Compute-heavy child flows should be sized by the largest in-memory working set and expected CPU pressure.

## Tuning loop

1. Start with a small manual run.
2. Observe memory peak, CPU usage, task duration, retries, and OOM events.
3. Tune these together:
   - batch size;
   - concurrency;
   - chunk size or per-task processing window;
   - pod requests and limits.

Do not tune resources in isolation. Throughput and memory footprint are usually coupled.

## When to split deployments

Split deployments instead of overloading one profile when:
- scheduled runs are much lighter than manual or historical runs;
- parent and child work have different resource needs;
- one execution mode needs more concurrency but another needs more memory.
