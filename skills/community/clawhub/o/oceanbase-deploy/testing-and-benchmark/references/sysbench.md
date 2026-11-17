# Sysbench

Use Sysbench for a bounded transactional workload against an approved tenant. Read `obd test sysbench --help` and the selected Sysbench plugin before choosing options or assuming preparation behavior.

## Plan the Run

Resolve the component and test server, SQL endpoint, tenant, database, user, Sysbench executable/version, script name and script directory, table count, rows per table, threads, duration or event limit, random distribution, effective ignored-error policy, and expected write behavior.

Inspect the selected script. Names such as read-only or point-select are not sufficient proof that setup and cleanup are read-only. Verified OBD plugins can run Sysbench cleanup and prepare before the workload, replacing benchmark tables. Use a dedicated schema or separately authorized object set.

Choose either a positive bounded `--time` or a bounded event count supported by installed help. Apply the common timeout handling to preparation, cleanup, connection, child processes, restoration, and the complete invocation.

Resolve `--mysql-ignore-errors` from the installed command help and selected plugin before execution. In the reviewed V4.6.0 path, omitting it applies the default `1062` and forwards that policy to cleanup, prepare, and run. Treat every non-empty ignored-error list, including a default, as an explicit test exception: show the exact codes and obtain authorization. If the baseline requires no ignored errors, use only a version-proved no-ignore spelling; stop when the installed path cannot express or prove that policy. Do not infer a zero unexpected-error count from command success alone.

The reviewed Sysbench plugin `3.1.0` can place the password in a generated command, log that command, and execute it through a shell. Use a dedicated least-privilege short-lived test credential supplied through the most protected path the installed command supports, restrict process and log access, keep the rendered value out of reports, and revoke or rotate it afterward.

## Command Shape

Construct only from installed long options:

```bash
obd test sysbench <deploy_name> \
  --component=<component> \
  --test-server=<server> \
  --tenant=<tenant> \
  --user=<user> \
  --database=<database> \
  --script-name=<script> \
  --tables=<table_count> \
  --table-size=<rows_per_table> \
  --threads=<threads> \
  --time=<seconds> \
  --mysql-ignore-errors=<explicitly_approved_list_or_version-proved_no-ignore_value> \
  --optimization=0 \
  [version-supported credential option; value supplied only through the approved local procedure]
```

Do not include defaults merely because they appear in another release. Review the redacted command, data replacement behavior, load, and stop condition before execution.

## Stage and Accept

- **Prepare:** verify the intended tables alone were created/replaced and row counts match the plan.
- **Run:** collect transactions/events, latency distribution, all reported or ignored errors/reconnects, throughput, and cluster resource evidence; inspect raw output rather than relying on process status alone.
- **Report:** preserve raw Sysbench output and identify the script, scale, concurrency, duration, tool version, and ignored-error policy.
- **Cleanup/retain:** follow the pre-approved dataset decision. Do not run an extra Sysbench cleanup against an ambiguous schema.

Report success only when the requested workload completed, unexpected error count is zero or explicitly accepted, metrics are parseable, and post-run SQL and cluster health pass. A high throughput number does not override data or service errors.
