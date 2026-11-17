# Component Reinstallation

Use `obd cluster reinstall` only when an already deployed component must be reassigned to a specific compatible repository artifact and the installed workflow supports that operation. Reinstall can replace executables and restart services; it is not generic cleanup, restart, or upgrade.

## Decision and Artifact Gate

1. Record OBD build, deployment status, target component/servers, current component version, release, architecture, repository hash, plugin, executable checksum, process state, ports, and data paths.
2. Read installed `cluster reinstall --help` and workflow. Resolve one target repository entry by component, version, release, architecture, hash, source, and plugin compatibility.
3. Confirm the operation class:
   - use restart when no artifact changes;
   - use [upgrade](upgrade.md) when version transition checks/scripts are required;
   - use reinstall only for a supported artifact/release replacement.
4. Determine exact stop/start behavior, files replaced, configuration/data preserved, scripts omitted or invoked, and failure boundary. If this cannot be established, treat it as a full component outage and stop unless the user accepts that scope.
5. Verify redundancy/backups appropriate to the component. Record the prior compatible artifact as the possible rollback target.

Show selected servers, current and target hashes, expected outage, client/dependency impact, and recovery boundary, then obtain availability/configuration authorization.

## Execute and Accept

Use only options exposed by installed help. A verified OBD 4.7.x surface includes component and hash selectors, schematically:

```bash
obd cluster reinstall <deploy_name> \
  --component=<component> \
  --hash=<reviewed_repository_hash>
```

Never add `--force` automatically. In builds where it forces repository reassignment despite a start failure, it can preserve or deepen a broken state and requires a separate state-specific authorization.

After execution, verify registered repository hash, installed artifact checksum/version/release, PID/start time, listener ownership, component SQL/API health, dependency health, and a representative data-plane operation. A successful start does not prove selection of the intended artifact.

## Failure Handling

Freeze retries and record the trace, stage reached, current/target hashes, files replaced, configuration, real processes/listeners, and dependency state. Do not rerun with force or switch to upgrade/redeploy. Reinstall the recorded prior artifact only when the observed state and installed workflow prove that rollback safe and the user authorizes the additional outage.
