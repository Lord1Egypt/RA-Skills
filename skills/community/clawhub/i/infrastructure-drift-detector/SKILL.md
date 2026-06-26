---
name: infrastructure-drift-detector
description: Detect drift between Infrastructure-as-Code definitions (Terraform, Pulumi, CloudFormation, CDK) and actual deployed state. Identify untracked resources, manual changes, and configuration discrepancies.
---

# Infrastructure Drift Detector

Detect when your deployed infrastructure has drifted from its IaC definitions. Finds manual changes, untracked resources, stale state, and configuration mismatches across Terraform, Pulumi, CloudFormation, and CDK.

Use when: "check for drift", "has anything changed outside terraform", "infrastructure audit", "find manual cloud changes", "state vs reality", "drift report", or before IaC refactors to ensure the state file is accurate.

## Commands

### 1. `detect` — Full Drift Analysis

#### Step 1: Identify IaC Tool

```bash
# Check which IaC tools are in use
ls -la *.tf terraform.tfstate .terraform 2>/dev/null && echo "TERRAFORM"
ls -la Pulumi.yaml Pulumi.*.yaml 2>/dev/null && echo "PULUMI"
ls -la template.yaml template.json cdk.json 2>/dev/null && echo "CLOUDFORMATION/CDK"
ls -la *.bicep 2>/dev/null && echo "BICEP"
```

#### Step 2: Terraform Drift Detection

If Terraform is detected:

```bash
# Refresh state without applying (safe, read-only)
terraform plan -refresh-only -detailed-exitcode 2>&1
# Exit code 0 = no drift, 2 = drift detected

# List all resources in state
terraform state list 2>&1

# Show detailed plan for any drifted resources
terraform plan -no-color 2>&1 | head -500
```

Parse the plan output and categorize drift:

| Category | Description | Risk |
|----------|-------------|------|
| **Attribute drift** | A value changed outside TF (e.g., security group rule added manually) | High |
| **Resource missing** | State says it exists, but it's been deleted | Critical |
| **Untracked resource** | Exists in cloud but not in any .tf file | Medium |
| **State stale** | State file hasn't been refreshed in >30 days | Low |

#### Step 3: Pulumi Drift Detection

If Pulumi is detected:

```bash
# Preview to detect drift
pulumi preview --diff --refresh 2>&1

# Export current state
pulumi stack export 2>&1 | python3 -c "
import json, sys
state = json.load(sys.stdin)
resources = state.get('deployment', {}).get('resources', [])
print(f'Total resources in state: {len(resources)}')
for r in resources:
    print(f'  {r.get(\"type\", \"?\")} :: {r.get(\"urn\", \"?\").split(\"::\")[-1]}')
"
```

#### Step 4: CloudFormation Drift Detection

```bash
# Detect drift on all stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE | \
  python3 -c "
import json, sys
stacks = json.load(sys.stdin)['StackSummaries']
for s in stacks:
    print(s['StackName'])
"

# For each stack, trigger drift detection
aws cloudformation detect-stack-drift --stack-name <STACK_NAME>
# Wait, then check results
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id <ID>
aws cloudformation describe-stack-resource-drifts --stack-name <STACK_NAME> --stack-resource-drift-status-filters MODIFIED DELETED
```

#### Step 5: Cross-Tool Analysis

Regardless of IaC tool, also check:

```bash
# Recent cloud changes (AWS example — last 24h)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ReadOnly,AttributeValue=false \
  --start-time $(date -d '24 hours ago' -u +%Y-%m-%dT%H:%M:%SZ) \
  --max-results 50 2>&1

# Find resources not in any .tf/.yaml IaC file
# List all TF-managed resource types
grep -rh 'resource "' *.tf **/*.tf 2>/dev/null | sed 's/resource "//;s/".*//' | sort -u
```

#### Step 6: Generate Report

Produce a structured drift report:

```markdown
# Infrastructure Drift Report — [date]

## Summary
- **Tool:** Terraform/Pulumi/CloudFormation
- **Total managed resources:** N
- **Drifted resources:** N (X critical, Y high, Z medium)
- **Untracked resources:** N
- **Last state refresh:** [date]

## Critical Drift (fix immediately)
- [resource]: [what changed] — Risk: manual security group change bypasses review

## High-Risk Drift (fix this sprint)
- [resource]: [attribute changed from X to Y]

## Recommended Actions
1. Import untracked resources: `terraform import <type>.<name> <id>`
2. Refresh state: `terraform apply -refresh-only`
3. Add lifecycle rules for expected drift: `ignore_changes = [tags]`
4. Set up drift detection in CI: scheduled `terraform plan -detailed-exitcode`
```

### 2. `monitor` — Set Up Continuous Drift Detection

Create a CI job or cron that runs drift detection on a schedule:

```yaml
# GitHub Actions example
name: Drift Detection
on:
  schedule:
    - cron: '0 6 * * 1-5'  # Weekday mornings
jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan -refresh-only -detailed-exitcode
        continue-on-error: true
      - if: steps.plan.outcome == 'failure'
        run: echo "::warning::Infrastructure drift detected!"
```

Recommend monitoring thresholds:
- **Alert immediately:** Security group, IAM, or network changes
- **Alert daily:** Any resource attribute drift
- **Weekly review:** Untracked resources, state staleness

### 3. `reconcile` — Generate Fix Plan

For each drifted resource, suggest one of:
1. **Accept drift** — update IaC to match reality (`terraform import`, update .tf)
2. **Revert drift** — apply IaC to restore intended state (`terraform apply -target`)
3. **Ignore drift** — add `lifecycle { ignore_changes }` for expected variance

Output a step-by-step remediation script with `terraform import` commands for untracked resources and `terraform apply -target` commands for reverts.
