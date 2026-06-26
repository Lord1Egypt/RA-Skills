---
name: testing-and-benchmark
description: Run OceanBase performance benchmarks and functional tests using obd test. Supports Sysbench, TPC-H, TPC-C benchmarks and mysqltest functional tests. Use when users want to benchmark, stress test, run functional tests, or evaluate OceanBase cluster performance. Also use when users mention sysbench, TPC-H, TPC-C, mysqltest, or obd test.
compatibility: Requires obd CLI and a running OceanBase cluster with a test tenant.
metadata:
  author: oceanbase
  version: "1.0"
---

# OceanBase Testing & Benchmark (obd test)

Run performance benchmarks (Sysbench, TPC-H, TPC-C) and functional tests (mysqltest) on OceanBase clusters using `obd test`.

## When to Use This Skill

- Running performance benchmarks: Sysbench, TPC-H, TPC-C
- Running functional tests: mysqltest
- Evaluating cluster performance under load

**For cluster deployment and management:** Use [cluster-management](../cluster-management/SKILL.md).
**For tenant creation (needed before testing):** Use [tenant-management](../tenant-management/SKILL.md).

---

## Important Rules

1. **Do NOT install test tools via yum.** OBD auto-downloads `ob-sysbench`, `obtpch`, and `obtpcc` when online.
2. **Non-interactive mode**: Set auto-confirm before scripted runs:
   ```bash
   obd env set IO_DEFAULT_CONFIRM 1
   ```
3. **Full test suite**: Do not abort on first failure. Run all test cases to completion, then produce a single report summarizing pass/fail/skip.

---

## Test Commands

### MySQL Test (Functional)
```bash
obd test mysqltest <deploy_name> --test-set <test_set>
```

### Sysbench (Benchmark)
```bash
obd test sysbench <deploy_name> --tenant=<tenant> --script-name=<script>
```

### TPC-H (Benchmark)
```bash
obd test tpch <deploy_name> --tenant=<tenant> --remote-tbl-dir=<server_dir>
```
`--remote-tbl-dir` is **required** — specifies where TPC-H table files are stored on the server.

### TPC-C (Benchmark)
```bash
obd test tpcc <deploy_name> --tenant=<tenant> --warehouses=<n> --run-mins=<minutes>
```
Use `--run-mins` (not `--running-minutes`) to cap duration. Java may need to be installed separately.

See [references/test-commands.md](references/test-commands.md) for detailed parameters and examples.

---

## Usage Examples

### Sysbench Quick Test
```bash
obd test sysbench test-cluster --tenant=mysql --script-name=oltp_read_write.lua
```

### TPC-H Benchmark
```bash
obd test tpch test-cluster --tenant=mysql --remote-tbl-dir=/tmp/tpch
```

### TPC-C Benchmark
```bash
obd test tpcc test-cluster --tenant=mysql --warehouses=10 --run-mins=5
```

---

## Skill Functional Test

To run a full skill validation covering cluster/tenant/backup and all test types:

```text
Run all OBD functional tests covered by this skill and output a test report.
```

When testing OCP-related functionality, default to `ocp-ce`. If a test mentions `ocp-express`, note that it has been replaced by `obshell dashboard`.

---

## Related Skills

- [cluster-management](../cluster-management/SKILL.md) — Deploy and manage clusters
- [tenant-management](../tenant-management/SKILL.md) — Create test tenants
- [seekdb](../seekdb/SKILL.md) — seekdb operations
