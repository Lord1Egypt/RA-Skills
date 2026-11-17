# TPC-C

TPC-C is a write-intensive benchmark with a Java/BenchmarkSQL or packaged TPC-C toolchain. Validate the selected OBD plugin and toolchain before preparing data.

## Toolchain and Scale

Read installed help and plugin evidence to resolve the OBClient path, Java executable and version, architecture, required JRE/JDK compatibility, TPC-C package or BenchmarkSQL directory/JAR/libraries, SQL templates, and output directory. Do not require a specific Java version without version-matched evidence.

Perform Java resolution under the same controller user, `OBD_HOME`, working environment, and non-secret `PATH`/`JAVA_HOME` that will invoke OBD. Resolve the exact executable passed through `--java-bin` (or the installed plugin's documented fallback), verify its file identity and execution permission, and run its read-only version check in that same context. Then validate the selected JAR/classpath, required libraries, and the plugin's expected entry classes. Do not assume that `java` in an operator's login shell is the executable the TPC-C plugin will use.

Record warehouses, load workers, terminals, duration, tenant capacity, expected database size, and result path. Check constraints between terminals and warehouses from the installed plugin. If reusing data through a supported test-only mode, prove that the existing warehouse count and schema match exactly.

Inspect the build and run plugins, not only CLI help. Verified current TPC-C build executes `tableDrops.sql` before creation and performs a major freeze; the run path performs another major freeze, including with `--test-only`. Thus an initialize-and-run workflow can freeze twice, while a proven test-only workflow can still freeze once. Freeze scope is plugin-version dependent: inspected 3.1 code uses a cluster-level form and later 4.x code can use a tenant-scoped form. Present the exact schema objects replaced, the number and scope of freezes, and their I/O/compaction impact; obtain dataset-replacement and major-freeze authorization separately from permission to generate load.

Verified current plugins can also write the database password in plaintext to `<tmp-dir>/props.oceanbase` and construct OBClient commands with a password argument. Use a new canonical run-owned directory with restrictive permissions and the common dedicated short-lived credential procedure. Before execution decide whether the properties file must be retained for audit or removed after the run; verify that exact disposition and revoke/rotate the credential. Never treat the temporary directory as non-sensitive output.

## Command Shape

```bash
obd test tpcc <deploy_name> \
  --component=<component> \
  --test-server=<server> \
  --tenant=<tenant> \
  --user=<user> \
  --database=<database> \
  --warehouses=<warehouses> \
  --terminals=<terminals> \
  --run-mins=<minutes> \
  --java-bin=<reviewed_java_path> \
  --tmp-dir=<absolute_run_owned_path> \
  --optimization=0 \
  [reviewed load or test-only options] \
  [version-supported credential option; value supplied only through the approved local procedure]
```

Use `--run-mins` only when installed help confirms it; do not substitute a remembered option name. It bounds the BenchmarkSQL/TPC-C workload, not tenant connectivity, major compaction, or every Java subprocess. Apply the common timeout handling to the complete invocation.

## Stage and Accept

- **Prepare/load:** verify the authorized drop/recreate scope, schema, warehouse count, row-count invariants, load errors, load duration, and any first authorized major freeze.
- **Run:** verify the additional authorized major freeze, then record transaction counts, throughput, latency, rollback/error counts, result directory, and server health during the interval.
- **Report:** preserve raw BenchmarkSQL/TPC-C output and identify non-standard configuration or reused data.
- **Cleanup/retain:** retain or remove the schema, sensitive `props.oceanbase`, and generated tool files exactly as approved; do not drop an ambiguous database or broadly delete the temporary directory.

Do not report success from process exit alone. Require parseable terminal results, expected transaction mix, accepted error/rollback behavior, complete duration, and healthy SQL/cluster state afterward.
