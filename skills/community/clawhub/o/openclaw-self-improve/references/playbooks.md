# Improvement Playbooks

This document provides metric selection guidance for common improvement objectives.

## Reliability Playbook

**Objective**: Reduce errors, failures, and flaky behavior.

**Primary Metrics**:
- Failed run count (absolute and percentage)
- Retry count per session
- Error rate by type
- Mean time to recovery (MTTR)
- Flaky test count and pass rate

**Baseline Measurement**:
```bash
# Run 100 representative sessions and count failures
for i in {1..100}; do
  run-session.sh >> session_results.log 2>&1
done
grep -c "ERROR" session_results.log
grep -c "RETRY" session_results.log
```

**Validation Gate**:
```bash
# Run tests with retry and measure flakiness
pnpm test -- --retries 3 --reporter json > test_results.json
```

**Success Criteria**: Error rate reduced by at least 50%, no increase in flaky tests.

## Performance Playbook

**Objective**: Reduce latency, startup time, or resource usage.

**Primary Metrics**:
- Latency (p50, p95, p99)
- Startup time
- Memory usage
- CPU usage
- Token consumption (for LLM calls)
- Request throughput

**Baseline Measurement**:
```bash
# Measure startup time
time pnpm start -- --no-watch

# Measure latency for 1000 requests
ab -n 1000 -c 10 http://localhost:3000/api/endpoint
```

**Validation Gate**:
```bash
# Measure performance with load testing
pnpm run benchmark -- --duration 60s --concurrency 10
```

**Success Criteria**: Latency reduced by at least 30%, no memory regression.

## Quality Playbook

**Objective**: Improve code quality, test coverage, or reduce defects.

**Primary Metrics**:
- Test coverage percentage
- Regression count
- Code quality score
- Defect density
- Type safety violations

**Baseline Measurement**:
```bash
# Measure test coverage
pnpm test -- --coverage --reporters=json > coverage.json

# Measure code quality
eslint src/ --format json > quality.json
```

**Validation Gate**:
```bash
# Run full test suite with coverage
pnpm test -- --coverage --minCoveragePercentage=80
```

**Success Criteria**: Coverage increased by at least 10%, no quality score decrease.

## Cost Playbook

**Objective**: Reduce token usage, API calls, or computational cost.

**Primary Metrics**:
- Tokens per session
- API call count
- Cost per operation
- Unnecessary tool invocations
- Cache hit rate

**Baseline Measurement**:
```bash
# Run representative sessions and measure token usage
export MEASURE_TOKENS=true
for i in {1..100}; do
  run-session.sh 2>&1 | grep "tokens_used"
done | awk '{sum+=$NF} END {print "Average:", sum/NR}'
```

**Validation Gate**:
```bash
# Measure token usage in production-like conditions
pnpm run measure-cost -- --sessions 100 --output cost_report.json
```

**Success Criteria**: Token usage reduced by at least 20%, no functionality loss.

## Safety Playbook

**Objective**: Improve security, reduce vulnerabilities, or enhance safety.

**Primary Metrics**:
- Vulnerability count by severity
- Security test pass rate
- Unsafe API usage count
- Input validation coverage
- Rate limit violations

**Baseline Measurement**:
```bash
# Scan for vulnerabilities
npm audit --json > audit.json

# Run security tests
pnpm test -- --testPathPattern=security
```

**Validation Gate**:
```bash
# Security scan and validation
npm audit --audit-level=moderate
pnpm run security-check
```

**Success Criteria**: All high/critical vulnerabilities fixed, no new vulnerabilities introduced.

## UX Playbook

**Objective**: Improve user experience, reduce friction, or enhance usability.

**Primary Metrics**:
- User satisfaction score
- Task completion rate
- Time to completion
- Error recovery rate
- Feature adoption rate

**Baseline Measurement**:
```bash
# Collect user feedback
survey-tool.sh --users 50 --questions "satisfaction,ease-of-use,friction"

# Measure task completion
usability-test.sh --tasks 10 --users 20 > ux_baseline.json
```

**Validation Gate**:
```bash
# Validate UX improvements
usability-test.sh --tasks 10 --users 20 --compare ux_baseline.json
```

**Success Criteria**: Satisfaction increased by at least 15%, completion rate improved.

## Scalability Playbook

**Objective**: Handle increased load, more users, or larger datasets.

**Primary Metrics**:
- Throughput (requests per second)
- Latency under load (p95, p99)
- Resource scaling factor
- Error rate under load
- Connection pool utilization

**Baseline Measurement**:
```bash
# Load test with increasing concurrency
for concurrency in 10 50 100 500; do
  ab -n 1000 -c $concurrency http://localhost:3000/api/endpoint
done
```

**Validation Gate**:
```bash
# Load test with target concurrency
ab -n 10000 -c 500 http://localhost:3000/api/endpoint
```

**Success Criteria**: Handle 5x current load with <10% latency increase.

## Selecting Your Playbook

1. **Identify your objective**: What aspect of OpenClaw needs improvement?
2. **Choose primary metrics**: Pick 1-3 metrics that directly measure success
3. **Establish baseline**: Measure current state before improvements
4. **Define validation gate**: Specify exact commands to run after changes
5. **Set success criteria**: Be explicit about what constitutes success
6. **Document assumptions**: Record environment, load, and other assumptions

## Combining Playbooks

For complex improvements, combine metrics from multiple playbooks:

**Example**: "Improve reliability and performance"
- Primary: Error rate reduction (Reliability)
- Secondary: Latency reduction (Performance)
- Validation: Run tests + load test
- Success: Error rate -50% AND latency -30%

## Common Pitfalls

- **Measuring the wrong thing**: Ensure metrics align with objective
- **Insufficient baseline**: Measure enough samples for statistical significance
- **Ignoring side effects**: Monitor for regressions in other metrics
- **Unrealistic targets**: Set achievable goals based on current state
- **Forgetting environment**: Document hardware, network, and software versions
