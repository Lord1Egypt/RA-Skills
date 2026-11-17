---
name: testing-and-benchmark
description: Run OceanBase functional tests and performance benchmarks through obd test, including mysqltest, Sysbench, TPC-H, and TPC-C. Use for correctness testing, benchmark preparation, load execution, result analysis, or cleanup. Do not use for ordinary tenant or cluster lifecycle work.
metadata:
  author: oceanbase
  version: "2.0.3"
---

<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="oceanbase-testing-benchmark-obd-test"></a>
<a id="oceanbase-testing--benchmark-obd-test"></a>
<a id="when-to-use-this-skill"></a>
<a id="important-rules"></a>
<a id="test-commands"></a>
<a id="mysql-test-functional"></a>
<a id="sysbench-benchmark"></a>
<a id="tpc-h-benchmark"></a>
<a id="tpc-h-benchmark-1"></a>
<a id="tpc-c-benchmark"></a>
<a id="tpc-c-benchmark-1"></a>
<a id="usage-examples"></a>
<a id="sysbench-quick-test"></a>
<a id="skill-functional-test"></a>
<a id="related-skills"></a>

# OceanBase Testing and Benchmarking

Before resolving or acquiring any test prerequisite, read the shared [deployment package closure](../references/deployment-package-sets.md) and expand the selected test into its complete controller-side toolchain and runtime dependencies.

Before any package network request, select the effective artifact source before the acquisition mechanism and apply the shared [fixed package-source workflow](../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order). This applies to every test prerequisite. A `.repo` file is configuration rather than a package source; prove the effective package URL, and keep operating-system dependency repositories separate. For a missing prerequisite such as `ob-sysbench`, remain on the current required source while trying applicable controller-local OBD/tool, `curl`, `wget`, or package-manager paths. Verify and import/register the exact artifact locally before retrying `obd test`. Do not move OBD or test execution off the selected controller, and never use `obd mirror` as a network downloader.

Read [common-workflow.md](references/common-workflow.md) for every test. Then read exactly the selected tool reference:

| Test | Required reference |
|---|---|
| Sysbench | [sysbench.md](references/sysbench.md) |
| TPC-H | [tpch.md](references/tpch.md) |
| TPC-C | [tpcc.md](references/tpcc.md) |
| mysqltest | [mysqltest.md](references/mysqltest.md) |

## Shared Gates

- Before selecting syntax, plugins, or artifacts, read [product and capability resolution](../references/product-and-capability-resolution.md).
- Before any live controller/host/deployment query, SSH/SQL/API/network access, tool discovery that may install, data preparation, parameter change, external action, or load execution, read the [operation contract](../references/operation-contract.md).
- Before reporting a test successful, read the [completion criteria](../references/completion-criteria.md).
- After a failed, timed-out, interrupted, or mixed run, read [failure recovery and evidence](../references/failure-recovery-and-evidence.md) before retrying or cleaning.
- Before removing a dataset, database object, generated file, tool, cache, or result, read [cleanup and ownership boundaries](../references/cleanup-boundaries.md).

## Hard Boundaries

- Benchmark preparation and workload execution can create, update, or delete tenant data. Use an approved test tenant and dataset; do not infer permission to load a production tenant.
- For Sysbench, TPC-H, and TPC-C, pass the installed command's long optimization option explicitly. Use the no-OBD-optimization level for the default baseline; any parameter mutation or restart requires separate authorization. Do not add this benchmark-only option to mysqltest.
- For Sysbench, TPC-H, and TPC-C, keep the built-in cluster status check enabled unless the user explicitly accepts a reviewed equivalent check. MySQLtest has a different option set. Never reuse a short option from a deployment command in an `obd test` command.
- Track tool availability, prerequisite installation, test preparation, execution, result collection, and cleanup as distinct stages and results.
- Check the test toolchain before or during the supported OBD test workflow. If OBD installs a missing tool, JRE, OBClient, link, or profile entry as part of the requested test, record and verify that prerequisite change instead of treating it as a separate discovery gate.
- For mysqltest, keep the installed long option equivalent to `--disable-reboot` enabled unless the user separately authorizes the exact snapshot/redeploy behavior. In verified current plugins, an ordinary failed case can otherwise lead to a forced redeploy even without auto-retry.
- Do not put database passwords in reusable commands, output, or reports.

For tenant creation or backup, use [tenant-management](../tenant-management/SKILL.md). For deployment, component, or cluster lifecycle work, use [cluster-management](../cluster-management/SKILL.md).
