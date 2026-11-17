---
name: pscale-service-token
description: Create, show, list, and manage service tokens for CI/CD authentication. Use when setting up automated deployments, configuring CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI, etc.), creating non-interactive authentication, inspecting service token metadata, or rotating CI/CD credentials. Preferred over passwords for production automation. Triggers on service token, service-token show, CI/CD auth, automation token, pipeline authentication.
---

# pscale service-token

Create, list, and manage service tokens for CI/CD and automation.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Common Commands

```bash
# Create service token
pscale service-token create --org <org>

# List service tokens
pscale service-token list --org <org>

# Show safe metadata for one service token
pscale service-token show <token-id> --org <org> --format json

# Delete service token
pscale service-token delete <token-id> --org <org>
```

## Workflows

### CI/CD Setup (GitHub Actions)

```bash
# 1. Create service token
pscale service-token create --org my-org

# Returns:
#   TOKEN_ID: xxxxx
#   TOKEN: yyyyy

# 2. Add to GitHub Secrets
#   PLANETSCALE_SERVICE_TOKEN_ID = xxxxx
#   PLANETSCALE_SERVICE_TOKEN = yyyyy

# 3. Use in workflow
# .github/workflows/deploy.yml
# env:
#   PLANETSCALE_SERVICE_TOKEN_ID: ${{ secrets.PLANETSCALE_SERVICE_TOKEN_ID }}
#   PLANETSCALE_SERVICE_TOKEN: ${{ secrets.PLANETSCALE_SERVICE_TOKEN }}
# run: |
#   pscale deploy-request deploy my-db my-branch
```

### CI/CD Pipeline Integration

```bash
# 1. Create service token
pscale service-token create --org my-org

# 2. Add to your CI/CD secrets/variables
#   PLANETSCALE_SERVICE_TOKEN_ID
#   PLANETSCALE_SERVICE_TOKEN

# 3. Use in your pipeline config (.github/workflows, .gitlab-ci.yml, etc.)
# deploy:
#   script:
#     - pscale deploy-request create $DATABASE $BRANCH_NAME
```

### Token Rotation

```bash
# 1. List existing tokens
pscale service-token list --org my-org

# 2. Create new token
pscale service-token create --org my-org

# 3. Update CI/CD secrets

# 4. Review cleanup under the safety gates; verify replacement access and obtain approval
pscale service-token delete <old-token-id> --org my-org
```

### Inspect a service token

`pscale service-token show` returns safe service-token metadata such as ID, name, creation time, expiry, last-used time, last-used IP, and last-used network organization. It does not print the token secret and does not include access grants; use `show-access` when grants are needed.

```bash
pscale service-token show <token-id> --org <org> --format json
pscale service-token show-access <token-id> --org <org> --format json
```

List/show human and CSV output uses `last_used_ip` and `last_used_organization` columns. JSON uses nullable `last_used_ip` and `last_used_asn_organization`; the latter identifies the IP's network/ASN organization, not the PlanetScale organization or an access grant. Missing values display as empty strings in the table; JSON retains nulls. Do not infer misuse, current permissions, or safety to delete from last-use metadata alone. Protect IP/network metadata in incident evidence and avoid publishing it.

Treat token IDs and grant details as sensitive operational metadata. Never ask the user to paste a service token secret into chat; use environment variables or a secrets manager.

## Troubleshooting

### Token authentication fails

**Error:** `401 Unauthorized`

**Solutions:**
- Verify both TOKEN_ID and TOKEN are set correctly
- Check token hasn't been deleted: `pscale service-token list`
- Ensure token has required permissions
- Try creating new token (old may be expired)

### Token not showing in list

**Cause:** Tokens are organization-scoped

**Solution:**
```bash
# Ensure correct org
pscale org show

# List tokens for specific org
pscale service-token list --org <correct-org>
```

## Security Best Practices

1. **Rotate tokens regularly** (every 90 days recommended)
2. **Use separate tokens** for different CI/CD systems
3. **Review tokens for cleanup under the safety gates**; verify CI/CD dependencies before approving deletion
4. **Never commit tokens** to version control
5. **Use secrets management** (GitHub Secrets, environment variables, vault systems)
6. **Limit token scope** if possible (coming in future PlanetScale updates)

## Related Skills

- **pscale-auth** - Interactive authentication (development)
- **pscale-deploy-request** - Automated deployments via tokens
- **gitlab-cli-skills** - GitLab CI integration
- **github** - GitHub Actions integration

## References

See `references/commands.md` for complete command reference.
