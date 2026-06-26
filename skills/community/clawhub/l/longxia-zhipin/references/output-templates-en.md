# English Output Templates

## Template A: Recommendation (Before Install)

```text
Company/Industry Snapshot
- Company: {company_name_or_type}
- Primary Business: {business_summary}
- Stage/Scale: {company_stage}
- Key Hiring/Team Needs: {team_needs}

Candidate Skills (by Role)
- Business Role
  - {skill_name}: {purpose} | Fit: {fit_reason} | Install ID: {install_id}
- Delivery Role
  - {skill_name}: {purpose} | Fit: {fit_reason} | Install ID: {install_id}
- Growth Role
  - {skill_name}: {purpose} | Fit: {fit_reason} | Install ID: {install_id}

Longxia One-Click Package
- Base Pack:
  - {skill_name_1}
  - {skill_name_2}
- Enhancement Pack:
  - {skill_name_3}
  - {skill_name_4}
- Install Order: Base Pack -> Enhancement Pack

Please Confirm
Do you want me to install this package now?
Reply with: Confirm Install / Revise Plan
```

## Template B: Install Result

```text
Installation Summary
- Installed:
  - {skill_name}
- Failed:
  - {skill_name}: {failure_reason}
- Skipped:
  - {skill_name}: {skip_reason}

Next Action
- {next_step_1}
- {next_step_2}
```

## Template C: Fallback Install Confirmation

```text
Fallback Plan Detected
Some skills failed to install. I mapped backup skills for the same roles.

Backup Mapping
- {failed_skill} -> {backup_skill}

Do you want me to continue with fallback installation?
Reply with: Continue Fallback Install / Pause
```
