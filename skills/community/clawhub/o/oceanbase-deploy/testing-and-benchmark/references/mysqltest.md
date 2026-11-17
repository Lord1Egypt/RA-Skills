# mysqltest Functional Testing

mysqltest is a functional-test workflow, not a performance benchmark. It can execute DDL/DML and, in some plugin versions, an ordinary case failure, a named reboot case, a periodic psmall boundary, retry behavior, or initialization can lead to a snapshot reload or forced cluster redeploy. Inspect the installed plugin before execution.

## Select Test Inputs

Read `obd test mysqltest --help` and resolve the component/server, endpoint, compatibility mode, effective tenant mapping, base user, database, mysqltest and OBClient binaries, test source, expected-result source, temporary/var/log paths, and result/record paths.

For custom tests, inventory and validate:

- `.test` files and any sourced files;
- matching expected `.result` files;
- suite directory layout and suite list;
- initialization SQL and its database/account/tenant mutations;
- test/result/record suffixes and output directories;
- filters, exclusions, slices, case timeout, and log collection scope.

For the simple non-suite path documented by OBD V4.6.0, use this minimum layout after confirming the installed plugin preserves the same result mapping:

```text
mysql_test/
├── t/
│   └── smoke.test
├── r/
│   └── mysql/
│       └── smoke.result
├── tmp/
└── var/
```

`smoke.test` is mysqltest input, for example a bounded `SELECT 1;`. `smoke.result` must contain the mysqltest-formatted expected output for that exact input, client, mode, and server version; do not invent it from ordinary SQL-client display. For a named suite, map `<suite-dir>/<suite>/t/<case>.test` to `<suite-dir>/<suite>/r/<mode>/<case>.result`. Current inspected plugin code adds the `mysql` or `oracle` result subdirectory even though the command guide describes only the root `--result-dir` default. Verify this installed behavior before creating or selecting expected results.

Determine precedence among `--suite`, `--test-pattern`, `--test-set`, and all-cases options from installed help. Do not combine selectors whose documented semantics override one another.

Never enable a retry, reboot, snapshot, or periodic-reboot mode as generic test recovery. Initialization, result recording, component restart, broad log collection, snapshot load, and redeploy each require their own reviewed impact and authorization.

## Reboot and Redeploy Gate

Verified current mysqltest code can set `need_reboot` after a normal failed case even when auto-retry is disabled. It can also adopt `./mysql_test/rebootcases.py` implicitly when that file exists, and psmall configuration can request periodic reboots. The OBD core can satisfy such a reboot by calling cluster redeploy with force-kill, force, and force-delete behavior.

Therefore use the installed long option `--disable-reboot` as the safe default and inventory the working directory, reboot-case input, psmall configuration, auto-retry, fast-reboot/snapshot, and initialization settings before execution. Do not omit `--disable-reboot` unless every triggering case has been reviewed and the user separately authorizes the exact snapshot or destructive redeploy behavior, target paths/data, outage, and recovery plan. A test-execution confirmation alone is not that authorization.

## Tenant Identity Gate

For an OceanBase component in the reviewed OBD V4.6.0/mysqltest `3.1.0` path, the public command exposes `--mode` and `--user` but no independent tenant selector. The plugin appends `@mysql` or `@oracle` to the supplied base username according to the effective case mode. Therefore:

- `--mode=mysql` may target only the literal `mysql` tenant, and `--user` must be a base username with no `@` suffix;
- `--mode=oracle` may target only the literal `oracle` tenant, and `--user` must be a base username with no `@` suffix;
- `--mode=both` requires separate authenticated preflights for both literal tenants and a reviewed per-case mode mapping.

Before initialization or any case, authenticate through the exact endpoint and verify the database-reported current tenant and current user match that mapping. If another tenant is required, stop unless the selected installed command exposes and its implementation honors a separate tenant selector. Do not invent `--tenant` and do not encode a tenant in `--user`; in the reviewed path that produces a double suffix such as `user@tenant@mysql`.

## Credential Exposure

Inspect how the selected plugin constructs and logs its mysqltest/OBClient commands. Verified current code places the password in process arguments and records the constructed command in verbose/result state. If no protected credential channel is proven, use only an approved dedicated short-lived test credential under the common exposure gate; restrict logs and process visibility and revoke/rotate the credential afterward. Never include the value in a reusable command or report.

## Command Shape

For a bounded built-in or custom selection, treat `--case-timeout` as a per-case bound only. Use the common timeout handling for the suite, initialization, result comparison, log collection, and recovery/finalization:

```bash
obd test mysqltest <deploy_name> \
  --component=<component> \
  --test-server=<server> \
  --mode=mysql \
  --user=<base_user_without_at_sign> \
  --database=<database> \
  --mysqltest-bin=<absolute_mysqltest_binary> \
  --obclient-bin=<absolute_obclient_binary> \
  --test-set=<comma_separated_cases> \
  --test-dir=<reviewed_test_dir> \
  --result-dir=<reviewed_result_dir> \
  --tmp-dir=<absolute_run_owned_path> \
  --var-dir=<absolute_run_owned_var_path> \
  --case-timeout=<seconds> \
  --disable-reboot \
  [version-supported credential option; value supplied only through the approved local procedure]
```

Omit `--test-dir` or `--result-dir` when intentionally using installed built-ins and confirmed help defines that fallback. Use a suite or pattern command instead of `--test-set` when that is the reviewed selection; do not include all selectors in a reusable template. In V4.6.0, `--test-pattern` overrides `--test-set`, and `--auto-retry` means failed tests may redeploy the cluster. Keep `--auto-retry` absent under the reboot/redeploy gate.

## Execute and Report

Run initialization only when its exact SQL and objects are approved. For the selected cases, preserve per-case pass/fail/skip status, duration, actual/expected result identity, diff, stdout/stderr, logs, and tool/plugin versions.

Continue independent requested cases after an ordinary assertion failure only when `--disable-reboot` is effective, cluster health and test isolation remain sound, and the installed workflow does not force recovery before the next case. Stop the suite when a case leaves unknown server-side state, damages the fixture, requests an unapproved restart/redeploy, or makes later results invalid.

Recording mode creates or replaces expected-result artifacts in some versions; treat it as a write to the test corpus, not ordinary execution. Keep generated records separate from authoritative expected results until reviewed.

Success requires every requested case to have a terminal classification, no unexplained harness failure, complete result artifacts, and healthy post-test SQL/cluster state. Cleanup only run-owned temp/log files and explicitly disposable test objects; preserve failing results and diffs needed for diagnosis.
