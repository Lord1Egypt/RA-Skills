# Recovery Playbook

Step-by-step recovery guides for common production accidents.
Claude should reference this when something has gone wrong and suggest the appropriate steps.

---

## Incident Severity Classification 🆕

Before starting recovery, classify the incident to prioritize response speed and communication.

| Severity | Definition | Response Time | Examples |
|---|---|---|---|
| **SEV-1 (Critical)** | Production down, data loss in progress, or active security breach | Immediate (< 5 min) | DB dropped, prod wiped, credentials leaked and actively used |
| **SEV-2 (High)** | Significant production degradation, potential data loss, or suspected compromise | Urgent (< 15 min) | Deployment causing 50%+ error rate, malicious package installed |
| **SEV-3 (Medium)** | Partial production impact, no data loss, recoverable | Standard (< 1 hour) | One service down, accidental config change |
| **SEV-4 (Low)** | Minor impact, fully recoverable, no user-facing effect | Normal (< 4 hours) | Dev/staging accident, non-critical resource deleted |

### SEV-1 / SEV-2 Immediate Actions (Any Incident)
1. **STOP** — Halt all further execution immediately.
2. **ISOLATE** — If a security incident: isolate the affected system (revoke credentials, block network access).
3. **ASSESS** — What exactly happened? What is the current state?
4. **COMMUNICATE** — Notify the on-call engineer and team lead immediately. Do not handle silently.
5. **PRESERVE** — Do not delete logs, error output, or artifacts from the incident.
6. **RECOVER** — Follow the relevant scenario below.
7. **POST-MORTEM** — Document what happened, why, and how to prevent recurrence.

---

## 🔴 GENERAL FIRST RESPONSE (Any Accident)

1. **STOP** — Do not run any more commands.
2. **ASSESS** — What exactly happened? What is the current state?
3. **COMMUNICATE** — Notify the team immediately (do not hide the issue).
4. **PRESERVE** — Do not delete logs, error output, or any artifacts from the incident.
5. **RECOVER** — Follow the relevant section below.
6. **POST-MORTEM** — Document what happened, why, and how to prevent recurrence.

---

## Scenario 1: Accidental Database Deletion / Table Drop

### Immediate Steps
1. Do NOT run any more queries on the database.
2. Check if database has Point-In-Time Recovery (PITR) enabled.
3. Identify the last known-good backup timestamp.

### Recovery Options (in order of preference)
1. **PITR Restore** — Restore to a point just before the delete.
   - AWS RDS: `aws rds restore-db-instance-to-point-in-time`
   - GCP Cloud SQL: Use Cloud Console → Backups → Point-in-time recovery
   - PostgreSQL: Use `pg_basebackup` + WAL replay if self-hosted

2. **Snapshot Restore** — Restore the latest automated snapshot.
   - Identify the snapshot: `aws rds describe-db-snapshots`
   - Restore: `aws rds restore-db-instance-from-db-snapshot`

3. **Logical Backup** — Restore from `pg_dump` / `mysqldump` backup.
   - `pg_restore -d <new_db> backup.dump`
   - `mysql -u root -p <db> < backup.sql`

4. **Binlog Recovery (MySQL)** — Replay binary logs from last backup.
   - `mysqlbinlog --start-datetime="..." binlog.* | mysql -u root -p`

### Prevention Going Forward
- Enable automated backups with retention ≥ 7 days.
- Enable PITR on all production databases.
- Add `sql_safe_updates=1` (MySQL) to block mass updates without WHERE.

---

## Scenario 2: Accidental Mass Record DELETE/UPDATE (Data Still in DB)

### If Inside a Transaction (Best Case)
```sql
ROLLBACK;  -- Immediately rolls back changes if transaction is open
```

### If Already Committed
1. Check if binlog / WAL is available for replay.
2. Restore from most recent backup.
3. If partial data is recoverable, extract from backup into temp table, then merge.

```sql
-- Merge recovered data from backup table
INSERT INTO production_table
SELECT * FROM recovered_backup_table
WHERE id NOT IN (SELECT id FROM production_table);
```

---

## Scenario 3: Accidental `rm -rf` on Production Files

### Immediate Steps
1. Stop any processes that may be overwriting blocks on disk.
2. **Do NOT write anything new to the filesystem** — deleted files may still be recoverable.

### Recovery Options
1. **File system snapshot / volume snapshot** — Most cloud volumes take periodic snapshots.
   - AWS EBS: `aws ec2 describe-snapshots` → create volume from snapshot → mount and copy
   - GCP: Restore from persistent disk snapshot

2. **ext4 / ext3 recovery** (Linux, self-hosted):
   ```bash
   # Install extundelete
   apt-get install extundelete
   extundelete /dev/sdX --restore-all --output-dir /mnt/recovery
   ```

3. **S3 Versioning** — If files were in S3 and versioning was enabled:
   ```bash
   aws s3api list-object-versions --bucket my-bucket --prefix path/
   aws s3api get-object --bucket my-bucket --key path/file --version-id <id> output.file
   ```

4. **Git recovery** — If files were tracked in git:
   ```bash
   git checkout HEAD -- <path>
   git stash pop
   ```

---

## Scenario 4: Terraform Destroy Ran in Production

### Immediate Steps
1. Check if resources are still in the process of being destroyed — if so, do NOT interrupt Terraform (can leave partial state).
2. Check Terraform state file for what was destroyed.
3. Check cloud provider for any resources that may still be running.

### Recovery Options
1. **Re-apply Terraform** — If state is intact and resources are recoverable:
   ```bash
   terraform plan    # See what needs to be re-created
   terraform apply   # Recreate resources
   ```

2. **Restore from Snapshots / Backups** — Re-provision databases, volumes from backups.

3. **Terraform state import** — If resources partially exist:
   ```bash
   terraform import <resource_type>.<name> <cloud_resource_id>
   ```

4. **Contact cloud provider** — Some providers can recover resources within a window (e.g., AWS EBS volume recovery within 24h for some resource types).

### Prevention
- Use Terraform `prevent_destroy = true` lifecycle rule on critical resources.
- Use separate state files for prod vs non-prod.
- Require MFA or approval for `terraform destroy` in prod.

```hcl
resource "aws_db_instance" "prod" {
  lifecycle {
    prevent_destroy = true
  }
}
```

---

## Scenario 5: Force Push Rewrote Git History on Main/Master

### Immediate Steps
1. Do NOT let others pull the new history — coordinate with the team immediately.
2. Find the last good commit SHA using `git reflog` on any local clone.

### Recovery Steps
```bash
# On a local clone that still has the old history
git reflog                         # Find the SHA of the last good commit
git checkout -b recovery-branch <SHA>

# Force push the recovery branch to origin
git push origin recovery-branch

# Reset main to the good SHA (requires force push access)
git push origin recovery-branch:main --force
```

### Prevention
- Enable branch protection rules on `main` / `master` (no force push, require PR + review).
- Use `--force-with-lease` instead of `--force` (safer: fails if remote has new commits).

---

## Scenario 6: Kubernetes Namespace or Deployment Deleted

### If Deployment (Pods Still Exist Briefly)
- Kubernetes will reschedule pods — re-apply the deployment manifest:
  ```bash
  kubectl apply -f deployment.yaml
  ```

### If Namespace Deleted (All Resources Gone)
1. Re-create the namespace: `kubectl create namespace <ns>`
2. Re-apply all manifests from Git: `kubectl apply -f ./k8s/`
3. Restore PersistentVolumes from snapshots if data was lost.

### If PersistentVolumeClaim Deleted (Data Loss)
1. Check if the underlying PV still exists: `kubectl get pv`
2. If PV has `Retain` reclaim policy — re-create PVC pointing to the PV.
3. If PV was deleted — restore from volume snapshot.

### Prevention
- Use `kubectl apply --dry-run=client` before real apply.
- Add `finalizers` to critical namespaces.
- Never run `kubectl delete` against prod without `--dry-run` first.

---

## Scenario 7: Redis FLUSHALL / FLUSHDB on Production

### Recovery Options
1. **RDB snapshot** — If Redis has `save` configured, check `/var/lib/redis/dump.rdb`.
   ```bash
   redis-server --dbfilename dump.rdb --dir /var/lib/redis  # Restart with snapshot
   ```
2. **AOF log replay** — If AOF is enabled, replay the append-only log.
3. **Rebuild from source of truth** — Re-populate cache from the primary database.

### Prevention
- Use `rename-command FLUSHALL ""` in `redis.conf` to disable the command in production.
- Use Redis ACLs to restrict FLUSH commands to admin users only.

---

## Scenario 8: Secrets / API Keys Accidentally Deleted or Exposed

### If Exposed (Leaked to Logs, Git, Slack, etc.)
1. **Rotate immediately** — Treat the secret as compromised.
2. Generate new credentials from the provider (AWS IAM, Google Cloud, GitHub, etc.).
3. Update the secret in your secrets manager (AWS Secrets Manager, Vault, GCP Secret Manager).
4. Audit access logs for any unauthorized use of the compromised key.
5. Notify security team.

### If Accidentally Deleted from Secrets Manager
1. Check if versioning is enabled — most secret managers keep previous versions.
   - AWS: `aws secretsmanager list-secret-version-ids --secret-id <n>`
   - AWS: `aws secretsmanager get-secret-value --secret-id <n> --version-id <id>`
2. Recreate the secret if versions are gone — rotate all dependent services.

---

## Scenario 9: Compromised Dependency / Supply Chain Attack 🆕

**Severity: SEV-1 or SEV-2 depending on data access scope.**

### Signs of a Compromised Package
- Unexpected outbound network connections from the application
- Secrets or environment variables sent to unknown external hosts
- Unexplained processes spawned by the application
- New files written outside the application directory
- Package version was recently updated and behavior changed
- `npm audit` / `pip-audit` reports a newly disclosed malicious package

### Immediate Steps
1. **STOP all deployments** that include the suspect package.
2. **Isolate** any systems that ran the compromised package:
   - Revoke all credentials (API keys, DB passwords, cloud credentials) that were accessible to the process.
   - Take the affected instances offline if active exfiltration is suspected.
3. **Determine blast radius** — What secrets / data were accessible at runtime?
   - Environment variables
   - Mounted secrets files
   - IAM role permissions (if cloud instance)
   - Database connection strings

### Identification & Containment
```bash
# Check what the package actually does
npm pack <package>@<version>         # Download tarball without executing
tar xf <tarball> -C /tmp/inspect/
grep -r "curl\|wget\|fetch\|exec\|eval\|child_process" /tmp/inspect/

# Check for outbound connections the package may have made
# (on Linux)
ss -tnp | grep <process>             # Active connections
journalctl -u <service> | grep curl  # Logged outbound requests

# Check environment variable access in Python package
grep -r "os.environ\|getenv\|os.getenv" /tmp/inspect/
```

### Recovery Steps
1. **Pin to a known-safe version** or remove the package.
   ```bash
   npm install <package>@<last-safe-version>
   pip install <package>==<last-safe-version>
   ```
2. **Rotate all potentially exposed credentials** — assume everything accessible was stolen.
3. **Redeploy from a clean build** — do not patch in place.
4. **Check git history** for any secrets that may have been committed.
   ```bash
   truffleHog git --since-commit <affected-deploy-commit> .
   gitleaks detect --source .
   ```
5. **Review access logs** in your cloud provider for the period since the compromised package was deployed.
6. **File a security advisory** with the package registry (npm advisory, PyPI report).

### Prevention
- Use `npm ci` (not `npm install`) in CI/CD — installs from lockfile exactly.
- Enable Dependabot or Renovate for automated dependency updates with security alerts.
- Use `npm audit --audit-level=high` as a CI gate.
- Subscribe to security advisories for critical dependencies.

---

## Scenario 10: Malicious Container Image Deployed 🆕

**Severity: SEV-1 if running in production with access to secrets.**

### Signs of a Malicious Image
- Unexpected processes inside the container (e.g., crypto miner, reverse shell)
- Unexplained outbound connections to unknown IPs
- Image digest does not match the expected build output
- Image pulled from an unverified registry or with `:latest` tag
- Trivy/Grype scan reveals known-malicious CVEs or suspicious layers

### Immediate Steps
1. **Stop / remove the container immediately.**
   ```bash
   kubectl scale deployment <name> --replicas=0    # Kubernetes
   docker stop <container_id>                      # Docker
   aws ecs update-service --desired-count 0        # ECS
   ```
2. **Revoke all credentials** accessible from within the container (same as Scenario 9).
3. **Preserve evidence** — do not delete the image yet:
   ```bash
   docker save <image> -o /tmp/evidence-image.tar  # Preserve for forensics
   ```

### Investigation
```bash
# Inspect image layers for suspicious commands
docker history <image>:<tag> --no-trunc
docker inspect <image>:<tag>

# Scan the image for malware / known-bad binaries
trivy image --scanners vuln,secret,misconfig <image>
grype <image>

# Check what the ENTRYPOINT / CMD does
docker inspect <image> --format '{{.Config.Entrypoint}} {{.Config.Cmd}}'

# Run the image in an isolated sandbox (no network, no secrets)
docker run --network none --rm <image> /bin/sh -c "find / -name '*.sh' | head -20"
```

### Recovery Steps
1. **Identify the correct, safe image version** and redeploy.
   ```bash
   docker pull <registry>/<image>:<known-safe-tag>@sha256:<known-digest>
   ```
2. **Rotate all credentials** that were accessible in the container's environment.
3. **Audit the image build pipeline** — how did the malicious image get built and pushed?
4. **Add image signing and verification** to the pipeline going forward (cosign / sigstore).
5. **Add Trivy/Grype scanning** as a CI gate — fail builds on HIGH/CRITICAL findings.

### Prevention
- Never use `:latest` in production. Always pin by digest.
- Scan images before deploy: `trivy image <image>` must pass before `kubectl apply`.
- Use a private registry with image signing (ECR with Cosign, GCR with Binary Authorization).
- Enable Binary Authorization (GCP) or AWS ECR image scanning on push.
