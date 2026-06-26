# Mirror & Repository Management

Manage local and remote package repositories for OBD.

## Commands

### List Mirrors
```bash
obd mirror list [repo_name]
```

### Update Mirrors
```bash
obd mirror update
```
Refreshes remote mirror metadata.

### Clone RPM to Local
```bash
obd mirror clone <path_to_rpm> [-f]
```
Use `-f` to force overwrite.

### Create Mirror
```bash
obd mirror create -n <name> -p <path> -V <version>
```

### Enable / Disable
```bash
obd mirror enable <repo_name>
obd mirror disable <repo_name>
```

### Clean Mirrors
```bash
obd mirror clean
```
Removes cached mirror data.

## Notes

- `ocp-ce` packages are not in the public community mirror by default. Verify with `obd mirror list` before planning OCP CE deployment.
- When deploying offline, clone all required RPMs to the local mirror first.
