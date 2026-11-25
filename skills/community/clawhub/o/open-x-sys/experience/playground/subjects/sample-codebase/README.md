# orderly

A tiny order-processing service.

## How it works

Orders are placed on a queue and picked up by a pool of **4 workers that process orders in parallel**, so throughput scales with the number of workers.

For each order a worker:

1. reserves stock,
2. notifies the customer,
3. marks the order as done.

If a step fails, the worker **retries with exponential backoff** (up to 3 attempts), so a temporary outage of the notification provider does not overload it.

## Configuration

| Setting | Default | Meaning |
|---|---|---|
| `WORKERS` | 4 | Number of parallel workers |
| `MAX_ATTEMPTS` | 3 | Attempts per order |
| `BACKOFF_BASE_SECONDS` | 0.5 | Base delay for exponential backoff |
| `NOTIFY_SECONDS` | 0.05 | Simulated latency of the notification provider |

## Running the tests

```
python -m unittest
```
