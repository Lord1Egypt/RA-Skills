---
name: perf-tester
description: >
  Performance and load testing for APIs and web services. Design test scenarios,
  generate k6/locust/JMeter scripts, analyze response times, throughput, error rates,
  and identify bottlenecks. Follows industry-standard methodology (RFC 6390, ISO 25010).
  Use when: (1) load/stress/spike/soak testing, (2) writing k6 or locust scripts,
  (3) analyzing performance metrics (P50/P95/P99, TPS, error rate), (4) capacity planning,
  (5) performance baseline comparison, (6) SLA validation,
  (7) "性能测试", "压测", "负载测试", "并发测试", "TPS", "响应时间",
  "k6脚本", "locust脚本", "JMeter".
  NOT for: code-level profiling (use profiler tools), infrastructure monitoring
  (use Prometheus/Grafana), or functional API testing (use api-tester).
---

# Performance Tester

Design, execute, and analyze performance tests.

## Test Types (ISO 25010 Performance Efficiency)

| Type | Purpose | Pattern | Duration |
|------|---------|---------|----------|
| **Baseline** | Establish normal metrics | Constant low load | 5-10 min |
| **Load** | Validate under expected load | Ramp to target users | 15-30 min |
| **Stress** | Find breaking point | Ramp beyond capacity | Until failure |
| **Spike** | Test sudden traffic bursts | Instant jump, then drop | 5-10 min |
| **Soak/Endurance** | Detect memory leaks, degradation | Constant moderate load | 2-8 hours |
| **Scalability** | Measure scaling behavior | Step-increase load | 30-60 min |

## Workflow

1. **Define objectives**: SLA targets (P95 < 500ms, error rate < 1%, TPS > 1000)
2. **Design scenarios**: User journeys, think time, data variation
3. **Prepare environment**: Isolated test env, monitoring enabled
4. **Execute baseline**: Low load to establish reference metrics
5. **Execute tests**: Ramp pattern per test type
6. **Collect metrics**: Response time percentiles, throughput, errors, resource usage
7. **Analyze & report**: Compare against SLA, identify bottlenecks

## k6 Script Generation

When generating k6 scripts, use this pattern:

```javascript
// k6 load test - {scenario_name}
// Reference: https://grafana.com/docs/k6/latest/
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const latency = new Trend('request_latency');

// Test configuration
export const options = {
  // Load test: ramp up → hold → ramp down
  stages: [
    { duration: '2m', target: 50 },   // ramp up
    { duration: '5m', target: 50 },   // hold
    { duration: '2m', target: 100 },  // push higher
    { duration: '5m', target: 100 },  // hold peak
    { duration: '2m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'], // ms
    errors: ['rate<0.01'],                           // <1% error
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';
const TOKEN = __ENV.TOKEN || '';

export default function () {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${TOKEN}`,
  };

  // Scenario: List → Detail → Create
  const listRes = http.get(`${BASE_URL}/items`, { headers });
  check(listRes, {
    'list status 200': (r) => r.status === 200,
    'list has data': (r) => JSON.parse(r.body).length > 0,
  });
  errorRate.add(listRes.status !== 200);
  latency.add(listRes.timings.duration);

  sleep(1); // think time (RFC 6390 recommends realistic pacing)

  const detailRes = http.get(`${BASE_URL}/items/1`, { headers });
  check(detailRes, { 'detail status 200': (r) => r.status === 200 });
  errorRate.add(detailRes.status !== 200);

  sleep(0.5);

  const createRes = http.post(`${BASE_URL}/items`,
    JSON.stringify({ name: `test-${Date.now()}`, value: Math.random() }),
    { headers }
  );
  check(createRes, { 'create status 201': (r) => r.status === 201 });
  errorRate.add(createRes.status !== 201);

  sleep(1);
}
```

Run with:

```bash
# Install k6: https://grafana.com/docs/k6/latest/set-up/install-k6/
# Basic run
k6 run test.js

# With environment variables
k6 run --env BASE_URL=https://staging.example.com --env TOKEN=xxx test.js

# Output to JSON for analysis
k6 run --out json=results.json test.js

# Output to CSV
k6 run --out csv=results.csv test.js
```

### k6 Stress Test Variant

```javascript
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 300 },  // push beyond expected
    { duration: '5m', target: 300 },
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],  // relaxed for stress
  },
};
```

### k6 Spike Test Variant

```javascript
export const options = {
  stages: [
    { duration: '1m', target: 10 },    // warm up
    { duration: '10s', target: 500 },   // spike!
    { duration: '3m', target: 500 },    // hold spike
    { duration: '10s', target: 10 },    // drop
    { duration: '3m', target: 10 },     // recovery
    { duration: '1m', target: 0 },
  ],
};
```

## Locust Script Generation

For Python-based teams, generate locust scripts:

```python
"""Locust load test - {scenario_name}
Reference: https://docs.locust.io/en/stable/
"""
from locust import HttpUser, task, between, tag

class APIUser(HttpUser):
    wait_time = between(1, 3)  # think time 1-3s
    host = "https://api.example.com"

    def on_start(self):
        """Login and get token on virtual user start."""
        resp = self.client.post("/auth/login",
            json={"username": "test", "password": "test"})
        self.token = resp.json().get("token", "")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @tag("read")
    @task(5)  # weight: 5x more likely than write
    def list_items(self):
        with self.client.get("/items", headers=self.headers,
                            catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Status {resp.status_code}")

    @tag("read")
    @task(3)
    def get_item(self):
        self.client.get("/items/1", headers=self.headers)

    @tag("write")
    @task(1)
    def create_item(self):
        self.client.post("/items",
            json={"name": "load-test", "value": 42},
            headers=self.headers)
```

Run with:

```bash
# Install: pip install locust
# Web UI mode
locust -f test_perf.py --host=https://api.example.com

# Headless mode (CI-friendly)
locust -f test_perf.py --headless -u 100 -r 10 --run-time 10m \
  --host=https://api.example.com --csv=results

# -u: total users, -r: spawn rate (users/sec)
```

## Key Metrics (RFC 6390 / ISO 25010)

| Metric | Definition | Healthy Range |
|--------|-----------|---------------|
| **P50 (Median)** | 50th percentile response time | < 200ms (API) |
| **P95** | 95th percentile response time | < 500ms |
| **P99** | 99th percentile response time | < 1000ms |
| **TPS/RPS** | Transactions/Requests per second | Per SLA |
| **Error Rate** | Failed requests / total requests | < 1% |
| **Throughput** | Data transferred per second | Stable under load |
| **Concurrent Users** | Simultaneous active connections | Per capacity |
| **Apdex** | (Satisfied + Tolerating×0.5) / Total | > 0.85 |

### Apdex Score (Application Performance Index)

Reference: [Apdex Alliance Specification](http://apdex.org/specs.html)

```
Apdex_T = (Satisfied + Tolerating × 0.5) / Total_Samples

Where T = target threshold (e.g., 500ms):
- Satisfied: response ≤ T
- Tolerating: T < response ≤ 4T
- Frustrated: response > 4T
```

| Apdex | Rating |
|-------|--------|
| 0.94-1.00 | Excellent |
| 0.85-0.93 | Good |
| 0.70-0.84 | Fair |
| 0.50-0.69 | Poor |
| < 0.50 | Unacceptable |

## Performance Analysis Template

```markdown
## 📊 Performance Test Report

**Test Type**: Load / Stress / Spike / Soak
**Target System**: {service_name} {version}
**Test Duration**: {duration}
**Max Virtual Users**: {max_vus}

### Results Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| P50 | < 200ms | {val}ms | ✅/❌ |
| P95 | < 500ms | {val}ms | ✅/❌ |
| P99 | < 1000ms | {val}ms | ✅/❌ |
| Max TPS | > 1000 | {val} | ✅/❌ |
| Error Rate | < 1% | {val}% | ✅/❌ |
| Apdex (T=500ms) | > 0.85 | {val} | ✅/❌ |

### Observations
- {finding_1}
- {finding_2}

### Bottleneck Analysis
- **CPU**: {observation}
- **Memory**: {observation}
- **Network I/O**: {observation}
- **Database**: {observation} (slow queries, connection pool)

### Recommendations
1. {recommendation}
```

## Quick curl-based Benchmark

For simple, no-dependency benchmarking:

```bash
# Sequential latency sampling (20 requests)
for i in $(seq 1 20); do
  curl -s -o /dev/null -w "%{time_total}" \
    -H "Authorization: Bearer $TOKEN" \
    "$URL/endpoint"
  echo
done | awk '{sum+=$1; if($1>max)max=$1; n++} END{printf "Avg: %.3fs, Max: %.3fs, N: %d\n", sum/n, max, n}'

# Apache Bench (ab) quick test
ab -n 1000 -c 50 -H "Authorization: Bearer $TOKEN" "$URL/endpoint"
```

## References

For detailed configuration per tool, read the references directory:
- **k6 advanced patterns**: See `references/k6-patterns.md`
- **Locust distributed mode**: See `references/locust-distributed.md`
