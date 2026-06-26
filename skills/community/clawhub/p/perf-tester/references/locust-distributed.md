# Locust Distributed Mode

Reference: https://docs.locust.io/en/stable/running-distributed.html

## Architecture

```
Master (coordinator) ←→ Worker 1
                     ←→ Worker 2
                     ←→ Worker N
```

- Master: distributes load, collects stats, serves Web UI
- Workers: generate actual HTTP traffic

## Running Distributed

```bash
# Terminal 1: Start master
locust -f test_perf.py --master --host=https://api.example.com

# Terminal 2-N: Start workers
locust -f test_perf.py --worker --master-host=<master-ip>

# Headless distributed (CI)
locust -f test_perf.py --master --headless -u 1000 -r 100 --run-time 15m \
  --expect-workers 4 --csv=results --host=https://api.example.com
```

## Docker Compose

```yaml
version: "3"
services:
  master:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/test_perf.py --master -H https://api.example.com

  worker:
    image: locustio/locust
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/test_perf.py --worker --master-host master
    deploy:
      replicas: 4
```

```bash
docker-compose up --scale worker=8
```

## Custom Shape (Programmatic Load)

```python
from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    """Step load: increase users every 2 minutes."""
    step_time = 120    # seconds per step
    step_load = 50     # users added per step
    spawn_rate = 10    # users/sec spawn rate
    time_limit = 600   # total test time

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.time_limit:
            return None
        current_step = run_time // self.step_time + 1
        return (current_step * self.step_load, self.spawn_rate)
```

## Scaling Guidelines

| Users | Workers | Notes |
|-------|---------|-------|
| < 500 | 1 (single mode) | No distribution needed |
| 500-2000 | 2-4 | One per CPU core |
| 2000-10000 | 4-8 | Monitor worker CPU |
| > 10000 | 8+ | Separate machines recommended |
