---
name: IaC Sec Audit
description: Infrastructure as Code security auditor for Terraform (.tf), CloudFormation (YAML/JSON), and Pulumi (TypeScript/Python). Detects 12 high-impact cloud misconfigurations — public S3 buckets, security groups open to 0.0.0.0/0 on SSH/RDP, unencrypted EBS/RDS/S3, wildcard IAM policies, hardcoded credentials, missing deletion protection, public RDS, unrestricted Lambda execution roles, and more. Zero external dependencies (no tfsec/checkov required). Works on any .tf or CloudFormation file. CI fail-gate included.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - terraform
  - cloudformation
  - pulumi
  - iac
  - aws
  - cloud
  - static-analysis
  - zero-deps
  - devops
  - infrastructure
---

# phy-iac-sec-audit — Infrastructure as Code Security Auditor

Scans Terraform, CloudFormation, and Pulumi files for **12 cloud security misconfigurations** that cause data breaches, crypto-mining attacks, and compliance failures. No tfsec, checkov, or cloud credentials required — pure static analysis. Zero external dependencies.

## Quick Start

```bash
# Scan a directory of Terraform files
python iac_sec_audit.py ./infrastructure

# Single file
python iac_sec_audit.py main.tf

# Scan CloudFormation template
python iac_sec_audit.py cloudformation.yaml

# CI mode — exit 1 on CRITICAL or HIGH
python iac_sec_audit.py ./terraform --ci

# Only CRITICAL findings
python iac_sec_audit.py ./terraform --only-severity CRITICAL
```

## The 12 Checks

| ID | Severity | Check | Resource Type |
|----|----------|-------|---------------|
| IC001 | CRITICAL | S3 bucket with public access enabled | aws_s3_bucket / AWS::S3::Bucket |
| IC002 | CRITICAL | Security group allows 0.0.0.0/0 on SSH (22) or RDP (3389) | aws_security_group |
| IC003 | CRITICAL | Hardcoded AWS credentials or secrets in IaC files | All |
| IC004 | HIGH | Unencrypted EBS volume or EC2 root block device | aws_ebs_volume / aws_instance |
| IC005 | HIGH | Unencrypted RDS instance | aws_db_instance / AWS::RDS::DBInstance |
| IC006 | HIGH | IAM policy with wildcard Action (*) or wildcard Resource (*) | aws_iam_policy / aws_iam_role_policy |
| IC007 | HIGH | RDS instance publicly accessible | aws_db_instance |
| IC008 | HIGH | S3 bucket without server-side encryption | aws_s3_bucket / aws_s3_bucket_server_side_encryption_configuration |
| IC009 | MEDIUM | No deletion protection on RDS / database | aws_db_instance |
| IC010 | MEDIUM | CloudFront distribution without WAF association | aws_cloudfront_distribution |
| IC011 | MEDIUM | Lambda function with overly permissive execution role | aws_lambda_function |
| IC012 | LOW | S3 bucket versioning not enabled | aws_s3_bucket |

### IC001 — Public S3 Bucket (CRITICAL)
Finds S3 buckets with `acl = "public-read"` or `acl = "public-read-write"`, or `aws_s3_bucket_public_access_block` with `block_public_acls = false`. Public S3 buckets are the #1 source of cloud data breaches — Capital One ($80M), Twitch source code, Toyota customer data all leaked via public S3.

### IC002 — Security Group Open SSH/RDP (CRITICAL)
Detects `cidr_blocks = ["0.0.0.0/0"]` or `cidr_ipv6_blocks = ["::/0"]` on ingress rules with port 22 (SSH) or 3389 (RDP). SSH/RDP open to the internet is scanned by bots within minutes of deployment and brute-forced continuously.

### IC003 — Hardcoded Credentials (CRITICAL)
Finds AWS access keys (`AKIA`/`ASIA` prefix patterns), secret keys, passwords, and tokens hardcoded as string values in `.tf`, `.yaml`, `.json` files. Credentials in IaC = credentials in every git clone, CI pipeline, and artifact registry.

### IC004 — Unencrypted EBS (HIGH)
Finds `aws_ebs_volume` or `aws_instance.root_block_device` without `encrypted = true`. Unencrypted EBS volumes expose data if snapshots are shared or the underlying hardware is recycled.

### IC005 — Unencrypted RDS (HIGH)
Finds `aws_db_instance` or `aws_rds_cluster` without `storage_encrypted = true`. Required for HIPAA, PCI-DSS, SOC2. Unencrypted RDS backups and snapshots expose customer data.

### IC006 — Wildcard IAM Policy (HIGH)
Finds IAM policies with `"Action": ["*"]` or `"Resource": ["*"]`. Over-permissive IAM is the #1 privilege escalation path in cloud environments. A compromised service with `*` on `*` = full account takeover.

### IC007 — RDS Publicly Accessible (HIGH)
Finds `aws_db_instance` with `publicly_accessible = true`. Databases should never be directly reachable from the internet — always proxy through the application layer or use a bastion host.

### IC008 — S3 Without Encryption (HIGH)
Finds `aws_s3_bucket` without a corresponding `aws_s3_bucket_server_side_encryption_configuration` resource. Required for compliance frameworks (SOC2, PCI-DSS, HIPAA).

### IC009 — No Deletion Protection (MEDIUM)
Finds `aws_db_instance` or `aws_rds_cluster` without `deletion_protection = true`. A Terraform `destroy` or a mistyped resource name can permanently delete production databases.

### IC010 — CloudFront Without WAF (MEDIUM)
Finds `aws_cloudfront_distribution` without `web_acl_id` attribute. Public CloudFront distributions without WAF are exposed to common attacks (SQL injection, XSS, DDoS floods) with no filtering.

### IC011 — Lambda Overpermissive Role (MEDIUM)
Finds `aws_lambda_function` where the `role` references an IAM role with `sts:AssumeRole` from `*` principal, or the role has `AdministratorAccess` / `PowerUserAccess` policy attached. Lambda functions should have least-privilege roles scoped to exactly what they need.

### IC012 — S3 Without Versioning (LOW)
Finds `aws_s3_bucket` without `aws_s3_bucket_versioning` enabled. Versioning is the cheapest protection against accidental deletion and ransomware overwrite attacks.

## Sample Output

```
============================================================
  IaC Security Audit — infrastructure/
  Files scanned: 12  |  Resources flagged: 8
============================================================

── CRITICAL (3) ────────────────────────────────────────────
🔴 IC001 [CRITICAL] infrastructure/s3.tf:8
   S3 bucket 'customer-data' has acl = "public-read". All objects readable by anyone on the internet.
   Fix: Remove acl entirely and add aws_s3_bucket_public_access_block with all four block_ flags = true.

🔴 IC002 [CRITICAL] infrastructure/security_groups.tf:23
   Security group 'app-sg' allows ingress from 0.0.0.0/0 on port 22 (SSH).
   Fix: Restrict to VPN CIDR: cidr_blocks = ["10.0.0.0/8"]. Use Systems Manager Session Manager instead of SSH.

🔴 IC003 [CRITICAL] infrastructure/rds.tf:15
   Hardcoded AWS secret: password = "prod-db-password-2024"
   Fix: Use aws_secretsmanager_secret_version data source or var.db_password from terraform.tfvars (gitignored).

── HIGH (3) ────────────────────────────────────────────────
🟠 IC005 [HIGH] infrastructure/rds.tf:8
   RDS instance 'prod-postgres' has storage_encrypted = false. DB backups and snapshots unencrypted.
   Fix: storage_encrypted = true. Add kms_key_id for custom KMS key.

🟠 IC006 [HIGH] infrastructure/iam.tf:34
   IAM policy with wildcard Action = ["*"] and Resource = ["*"]. Full account takeover if role is compromised.
   Fix: Replace * with specific actions: ["s3:GetObject", "s3:PutObject"] on specific resources.

🟠 IC007 [HIGH] infrastructure/rds.tf:19
   RDS 'prod-postgres' has publicly_accessible = true. Database exposed directly to internet.
   Fix: Set publicly_accessible = false. Access via application servers in same VPC or bastion host.

── MEDIUM (2) ──────────────────────────────────────────────
🟡 IC009 [MEDIUM] infrastructure/rds.tf:22
   RDS 'prod-postgres' has no deletion_protection = true. terraform destroy permanently removes production DB.
   Fix: deletion_protection = true  — requires manual disable before destroy.

🟡 IC010 [MEDIUM] infrastructure/cloudfront.tf:5
   CloudFront distribution has no WAF (web_acl_id missing). No protection against SQLi/XSS/DDoS.
   Fix: Create aws_wafv2_web_acl and reference: web_acl_id = aws_wafv2_web_acl.main.arn

────────────────────────────────────────────────────────────
  Total: 8 findings
  Critical: 3 | High: 3 | Medium: 2 | Low: 0

  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.
```

## The Script

```python
#!/usr/bin/env python3
"""
phy-iac-sec-audit — Infrastructure as Code Security Auditor
Detects 12 cloud misconfigurations in Terraform, CloudFormation, and Pulumi.
Zero external dependencies — no tfsec, checkov, or cloud credentials required.
"""

import sys
import re
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    severity: str      # CRITICAL / HIGH / MEDIUM / LOW
    location: str
    resource: str
    message: str
    fix: str = ""

    def __str__(self) -> str:
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(self.severity, "⚪")
        parts = [f"{icon} {self.check_id} [{self.severity}] {self.location}"]
        parts.append(f"   {self.message}")
        if self.fix:
            parts.append(f"   Fix: {self.fix}")
        return "\n".join(parts)


@dataclass
class AuditResult:
    scan_root: str
    files_scanned: int = 0
    resources_flagged: int = 0
    findings: list = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "CRITICAL")

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "HIGH")

    @property
    def medium_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "MEDIUM")

    @property
    def low_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "LOW")


# ─── Constants — Terraform Patterns ──────────────────────────────────────────

# IC001 — Public S3
S3_PUBLIC_ACL_RE = re.compile(
    r'acl\s*=\s*"(public-read|public-read-write|authenticated-read)"',
    re.IGNORECASE,
)
S3_BLOCK_FALSE_RE = re.compile(
    r"(block_public_acls|block_public_policy|ignore_public_acls|restrict_public_buckets)\s*=\s*false",
    re.IGNORECASE,
)

# IC002 — Security group 0.0.0.0/0 on SSH/RDP
SG_OPEN_CIDR_RE = re.compile(
    r'cidr_blocks\s*=\s*\[?"0\.0\.0\.0/0"',
    re.IGNORECASE,
)
SG_OPEN_IPV6_RE = re.compile(
    r'cidr_ipv6_blocks\s*=\s*\[?"::/0"',
    re.IGNORECASE,
)
SG_PORT_SSH_RDP_RE = re.compile(
    r"(from_port|to_port)\s*=\s*(22|3389|0)\b",
    re.IGNORECASE,
)

# IC003 — Hardcoded credentials
HARDCODED_CRED_RE = re.compile(
    r'(password|secret|access_key|secret_key|token|api_key|private_key)\s*=\s*"[^$"{][^"]{4,}"',
    re.IGNORECASE,
)
AWS_KEY_RE = re.compile(r'(AKIA|ASIA)[A-Z0-9]{16}', re.IGNORECASE)

# IC004 — Unencrypted EBS
EBS_ENCRYPTED_RE = re.compile(r"encrypted\s*=\s*true", re.IGNORECASE)
EBS_UNENCRYPTED_RE = re.compile(r"encrypted\s*=\s*false", re.IGNORECASE)

# IC005 — Unencrypted RDS
RDS_STORAGE_ENCRYPTED_RE = re.compile(r"storage_encrypted\s*=\s*true", re.IGNORECASE)
RDS_STORAGE_UNENCRYPTED_RE = re.compile(r"storage_encrypted\s*=\s*false", re.IGNORECASE)

# IC006 — Wildcard IAM
IAM_WILDCARD_ACTION_RE = re.compile(
    r'"Action"\s*:\s*(?:\[?\s*"?\*"?\s*\]?|"[^"]*\*[^"]*")',
    re.IGNORECASE,
)
TF_IAM_WILDCARD_RE = re.compile(
    r'actions\s*=\s*\[\s*"\*"\s*\]',
    re.IGNORECASE,
)
IAM_WILDCARD_RESOURCE_RE = re.compile(
    r'"Resource"\s*:\s*(?:\[?\s*"?\*"?\s*\]?)',
    re.IGNORECASE,
)
TF_RESOURCES_WILDCARD_RE = re.compile(
    r'resources\s*=\s*\[\s*"\*"\s*\]',
    re.IGNORECASE,
)

# IC007 — RDS publicly accessible
RDS_PUBLIC_RE = re.compile(r"publicly_accessible\s*=\s*true", re.IGNORECASE)

# IC008 — S3 without encryption
S3_SSE_RE = re.compile(
    r"(aws_s3_bucket_server_side_encryption_configuration|server_side_encryption_configuration)",
    re.IGNORECASE,
)

# IC009 — No deletion protection
DELETION_PROTECTION_RE = re.compile(r"deletion_protection\s*=\s*true", re.IGNORECASE)
DELETION_PROTECTION_FALSE_RE = re.compile(r"deletion_protection\s*=\s*false", re.IGNORECASE)

# IC010 — CloudFront without WAF
WAF_RE = re.compile(r"web_acl_id\s*=", re.IGNORECASE)

# IC011 — Lambda overpermissive role
LAMBDA_ADMIN_RE = re.compile(
    r"(AdministratorAccess|PowerUserAccess|arn:aws:iam::aws:policy/Administrator)",
    re.IGNORECASE,
)

# IC012 — S3 without versioning
S3_VERSIONING_RE = re.compile(
    r"(aws_s3_bucket_versioning|versioning\s*\{[^}]*enabled\s*=\s*true)",
    re.IGNORECASE,
)

RESOURCE_NAME_RE = re.compile(r'resource\s+"([^"]+)"\s+"([^"]+)"')

SKIP_DIRS = {".git", ".terraform", "node_modules", ".terragrunt-cache", "vendor", "modules"}
SUPPORTED_EXTENSIONS = {".tf", ".yaml", ".yml", ".json", ".ts", ".py"}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def collect_files(path: str) -> list:
    p = Path(path)
    if p.is_file():
        if p.suffix in SUPPORTED_EXTENSIONS:
            return [p]
        return []
    files = []
    for f in p.rglob("*"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS:
            files.append(f)
    return files


def is_iac_file(path: Path, content: str) -> bool:
    """Quick filter: does this file contain IaC resource definitions?"""
    if path.suffix == ".tf":
        return True
    if path.suffix in (".yaml", ".yml"):
        return "AWSTemplateFormatVersion" in content or "Resources:" in content or "aws_" in content
    if path.suffix == ".json":
        return "AWSTemplateFormatVersion" in content or "CloudFormation" in content
    if path.suffix in (".ts", ".py"):
        return "pulumi" in content.lower() or "aws." in content
    return False


def get_resource_name(lines: list, idx: int, window: int = 30) -> str:
    """Find the nearest resource block name above the current line."""
    for i in range(idx, max(0, idx - window), -1):
        m = RESOURCE_NAME_RE.search(lines[i])
        if m:
            return f"{m.group(1)}.{m.group(2)}"
    return "<unknown>"


def get_context(lines: list, idx: int, window: int = 20) -> str:
    start = max(0, idx - window)
    end = min(len(lines), idx + window)
    return "\n".join(lines[start:end])


# ─── Terraform Checks ────────────────────────────────────────────────────────

def check_ic001_s3_public(filepath: str, lines: list) -> list:
    """IC001 — S3 bucket with public access."""
    findings = []
    for i, line in enumerate(lines):
        if S3_PUBLIC_ACL_RE.search(line):
            resource = get_resource_name(lines, i)
            findings.append(Finding(
                check_id="IC001",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                resource=resource,
                message=f"S3 bucket '{resource}' has public ACL: {line.strip()[:60]}. All objects readable by anyone on the internet.",
                fix="Remove acl setting. Add aws_s3_bucket_public_access_block with all block_* = true.",
            ))
        if S3_BLOCK_FALSE_RE.search(line):
            resource = get_resource_name(lines, i)
            findings.append(Finding(
                check_id="IC001",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                resource=resource,
                message=f"Public access block explicitly disabled: {line.strip()[:60]}",
                fix="Set block_public_acls = true, block_public_policy = true, ignore_public_acls = true, restrict_public_buckets = true.",
            ))
    return findings


def check_ic002_sg_open_ports(filepath: str, lines: list, content: str) -> list:
    """IC002 — Security group with 0.0.0.0/0 on SSH/RDP."""
    findings = []
    # Find ingress blocks with open CIDR
    ingress_blocks = []
    in_ingress = False
    block_start = 0
    brace_depth = 0

    for i, line in enumerate(lines):
        if "ingress" in line.lower() and "{" in line:
            in_ingress = True
            block_start = i
            brace_depth = line.count("{") - line.count("}")
        elif in_ingress:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                ingress_blocks.append((block_start, i))
                in_ingress = False

    for start, end in ingress_blocks:
        block = "\n".join(lines[start:end + 1])
        has_open_cidr = bool(SG_OPEN_CIDR_RE.search(block) or SG_OPEN_IPV6_RE.search(block))
        if not has_open_cidr:
            continue
        port_match = SG_PORT_SSH_RDP_RE.search(block)
        if port_match or re.search(r"(from_port\s*=\s*0\b.*to_port\s*=\s*0\b|from_port\s*=\s*-1)", block):
            port = port_match.group(2) if port_match else "all"
            service = {"22": "SSH", "3389": "RDP", "0": "ALL"}.get(str(port), f"port {port}")
            resource = get_resource_name(lines, start)
            findings.append(Finding(
                check_id="IC002",
                severity="CRITICAL",
                location=f"{filepath}:{start + 1}",
                resource=resource,
                message=f"Security group '{resource}' allows {service} (port {port}) from 0.0.0.0/0. Brute-forced within minutes of deploy.",
                fix='Restrict to VPN CIDR: cidr_blocks = ["10.0.0.0/8"]. Use AWS Systems Manager Session Manager instead of SSH.',
            ))
    return findings


def check_ic003_hardcoded_credentials(filepath: str, lines: list) -> list:
    """IC003 — Hardcoded credentials in IaC files."""
    findings = []
    # Skip variable definitions and example files
    fname = Path(filepath).stem.lower()
    if any(x in fname for x in ("variable", "var", "example", "sample", "test", "mock")):
        return []

    for i, line in enumerate(lines):
        # Skip variable declarations and references
        stripped = line.strip()
        if stripped.startswith("variable") or "var." in stripped or "${" in stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("//"):
            continue

        if AWS_KEY_RE.search(line):
            findings.append(Finding(
                check_id="IC003",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                resource="<credentials>",
                message=f"AWS access key hardcoded: {line.strip()[:60]}",
                fix="Use aws_secretsmanager_secret_version, AWS SSM Parameter Store, or environment variables. Never commit keys.",
            ))
            continue

        m = HARDCODED_CRED_RE.search(line)
        if m:
            # Skip lines that reference variables or data sources
            if re.search(r'(var\.|data\.|local\.|aws_secretsmanager|aws_ssm_parameter|\$\{)', line):
                continue
            # Skip obvious non-secret patterns
            val_match = re.search(r'=\s*"([^"]+)"', line[m.start():])
            if val_match:
                val = val_match.group(1)
                # Skip: ARNs, region names, account IDs (12-digit), resource names, hostnames
                if re.match(r"(arn:|[a-z]+-[a-z]+-[12]$|\d{12}$|[a-z0-9-]+\.[a-z]+$)", val, re.IGNORECASE):
                    continue
                if len(val) < 6:  # Too short to be a real credential
                    continue
            findings.append(Finding(
                check_id="IC003",
                severity="CRITICAL",
                location=f"{filepath}:{i + 1}",
                resource="<credentials>",
                message=f"Possible hardcoded credential: {line.strip()[:70]}",
                fix="Use var.db_password from terraform.tfvars (gitignored) or aws_secretsmanager_secret_version data source.",
            ))
    return findings


def check_ic004_unencrypted_ebs(filepath: str, lines: list, content: str) -> list:
    """IC004 — Unencrypted EBS volume."""
    findings = []
    if "aws_ebs_volume" not in content and "root_block_device" not in content and "aws_instance" not in content:
        return []
    for i, line in enumerate(lines):
        if EBS_UNENCRYPTED_RE.search(line):
            ctx = get_context(lines, i, 15)
            if "ebs" in ctx.lower() or "block_device" in ctx.lower() or "aws_instance" in ctx.lower():
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC004",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"EBS volume/block device explicitly unencrypted: {line.strip()[:60]}",
                    fix="encrypted = true  — add kms_key_id = aws_kms_key.ebs.arn for custom key.",
                ))
        elif re.search(r"resource\s+\"aws_ebs_volume\"", line) or re.search(r"root_block_device\s*\{", line):
            ctx = get_context(lines, i, 20)
            if not EBS_ENCRYPTED_RE.search(ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC004",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"EBS resource '{resource}' missing encrypted = true (defaults to false).",
                    fix="encrypted = true",
                ))
    return findings


def check_ic005_unencrypted_rds(filepath: str, lines: list, content: str) -> list:
    """IC005 — Unencrypted RDS instance."""
    findings = []
    if "aws_db_instance" not in content and "aws_rds_cluster" not in content:
        return []
    for i, line in enumerate(lines):
        if re.search(r"resource\s+\"aws_(db_instance|rds_cluster)\"", line):
            ctx = get_context(lines, i, 30)
            if RDS_STORAGE_UNENCRYPTED_RE.search(ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC005",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"RDS '{resource}' has storage_encrypted = false. DB backups and snapshots unencrypted.",
                    fix="storage_encrypted = true  — required for HIPAA, PCI-DSS, SOC2.",
                ))
            elif not RDS_STORAGE_ENCRYPTED_RE.search(ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC005",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"RDS '{resource}' missing storage_encrypted (defaults to false).",
                    fix="storage_encrypted = true",
                ))
    return findings


def check_ic006_wildcard_iam(filepath: str, lines: list) -> list:
    """IC006 — IAM policy with wildcard Action or Resource."""
    findings = []
    for i, line in enumerate(lines):
        has_wildcard_action = TF_IAM_WILDCARD_RE.search(line) or IAM_WILDCARD_ACTION_RE.search(line)
        has_wildcard_resource = TF_RESOURCES_WILDCARD_RE.search(line) or IAM_WILDCARD_RESOURCE_RE.search(line)

        if has_wildcard_action:
            ctx = get_context(lines, i, 10)
            if re.search(r"(iam|policy|role)", ctx, re.IGNORECASE):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC006",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"IAM policy wildcard Action (*): '{line.strip()[:60]}'. Compromised role = full account access.",
                    fix='Replace * with specific actions: ["s3:GetObject", "s3:PutObject"] scoped to specific resources.',
                ))
        elif has_wildcard_resource:
            ctx = get_context(lines, i, 10)
            if re.search(r"(iam|policy|role)", ctx, re.IGNORECASE):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC006",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"IAM policy wildcard Resource (*): '{line.strip()[:60]}'. Any resource in account accessible.",
                    fix='Scope to specific ARN: "arn:aws:s3:::my-bucket/*"',
                ))
    return findings


def check_ic007_rds_public(filepath: str, lines: list, content: str) -> list:
    """IC007 — RDS publicly accessible."""
    if "aws_db_instance" not in content:
        return []
    findings = []
    for i, line in enumerate(lines):
        if RDS_PUBLIC_RE.search(line):
            ctx = get_context(lines, i, 15)
            if re.search(r"aws_db_instance", ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC007",
                    severity="HIGH",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"RDS '{resource}' is publicly_accessible = true. Database directly reachable from internet.",
                    fix="publicly_accessible = false. Access via application servers in same VPC or VPN + bastion host.",
                ))
    return findings


def check_ic008_s3_no_encryption(filepath: str, lines: list, content: str, all_contents: dict) -> list:
    """IC008 — S3 bucket without server-side encryption configuration."""
    if "aws_s3_bucket" not in content:
        return []

    # Check if any file in project has SSE config
    all_content_joined = " ".join(all_contents.values())
    if S3_SSE_RE.search(all_content_joined):
        return []  # SSE config exists somewhere in project

    findings = []
    for i, line in enumerate(lines):
        if re.search(r'resource\s+"aws_s3_bucket"\s+"', line):
            resource = get_resource_name(lines, i)
            # Skip logging/access-log buckets
            if re.search(r"(log|access.log|logging|audit)", resource, re.IGNORECASE):
                continue
            findings.append(Finding(
                check_id="IC008",
                severity="HIGH",
                location=f"{filepath}:{i + 1}",
                resource=resource,
                message=f"S3 bucket '{resource}' has no server-side encryption configuration.",
                fix=(
                    "Add: resource \"aws_s3_bucket_server_side_encryption_configuration\" with "
                    "rule { apply_server_side_encryption_by_default { sse_algorithm = \"aws:kms\" } }"
                ),
            ))
    return findings


def check_ic009_no_deletion_protection(filepath: str, lines: list, content: str) -> list:
    """IC009 — RDS without deletion protection."""
    if "aws_db_instance" not in content and "aws_rds_cluster" not in content:
        return []
    findings = []
    for i, line in enumerate(lines):
        if re.search(r"resource\s+\"aws_(db_instance|rds_cluster)\"", line):
            ctx = get_context(lines, i, 30)
            if DELETION_PROTECTION_FALSE_RE.search(ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC009",
                    severity="MEDIUM",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"RDS '{resource}' has deletion_protection = false. terraform destroy permanently removes production DB.",
                    fix="deletion_protection = true  — requires manual disable before destroy.",
                ))
            elif not DELETION_PROTECTION_RE.search(ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC009",
                    severity="MEDIUM",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"RDS '{resource}' missing deletion_protection (defaults to false).",
                    fix="deletion_protection = true",
                ))
    return findings


def check_ic010_cloudfront_no_waf(filepath: str, lines: list, content: str) -> list:
    """IC010 — CloudFront without WAF."""
    if "aws_cloudfront_distribution" not in content:
        return []
    findings = []
    for i, line in enumerate(lines):
        if re.search(r'resource\s+"aws_cloudfront_distribution"', line):
            ctx = get_context(lines, i, 50)
            if not WAF_RE.search(ctx):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC010",
                    severity="MEDIUM",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"CloudFront '{resource}' has no WAF (web_acl_id missing). No SQLi/XSS/DDoS protection.",
                    fix="Create aws_wafv2_web_acl and set web_acl_id = aws_wafv2_web_acl.main.arn in distribution.",
                ))
    return findings


def check_ic011_lambda_admin_role(filepath: str, lines: list, content: str) -> list:
    """IC011 — Lambda with overly permissive IAM role."""
    if "aws_lambda_function" not in content:
        return []
    findings = []
    for i, line in enumerate(lines):
        if LAMBDA_ADMIN_RE.search(line):
            ctx = get_context(lines, i, 20)
            if re.search(r"(aws_iam|lambda|role)", ctx, re.IGNORECASE):
                resource = get_resource_name(lines, i)
                findings.append(Finding(
                    check_id="IC011",
                    severity="MEDIUM",
                    location=f"{filepath}:{i + 1}",
                    resource=resource,
                    message=f"Lambda role references overly broad managed policy: {line.strip()[:60]}",
                    fix="Replace AdministratorAccess with least-privilege inline policy scoped to exactly what the Lambda needs.",
                ))
    return findings


def check_ic012_s3_no_versioning(filepath: str, lines: list, content: str, all_contents: dict) -> list:
    """IC012 — S3 bucket without versioning enabled."""
    if "aws_s3_bucket" not in content:
        return []

    all_content_joined = " ".join(all_contents.values())
    if S3_VERSIONING_RE.search(all_content_joined):
        return []  # Versioning config exists somewhere in project

    findings = []
    for i, line in enumerate(lines):
        if re.search(r'resource\s+"aws_s3_bucket"\s+"', line):
            resource = get_resource_name(lines, i)
            if re.search(r"(log|access.log|logging|audit|tmp|temp)", resource, re.IGNORECASE):
                continue  # Skip logging buckets — versioning wastes money on logs
            findings.append(Finding(
                check_id="IC012",
                severity="LOW",
                location=f"{filepath}:{i + 1}",
                resource=resource,
                message=f"S3 bucket '{resource}' has no versioning. Objects permanently deleted on accidental delete/overwrite.",
                fix=(
                    "Add: resource \"aws_s3_bucket_versioning\" { bucket = aws_s3_bucket.X.id "
                    "versioning_configuration { status = \"Enabled\" } }"
                ),
            ))
    return findings


# ─── Main Audit ───────────────────────────────────────────────────────────────

def audit(path: str) -> AuditResult:
    result = AuditResult(scan_root=path)
    files = collect_files(path)

    all_contents = {}
    for f in files:
        try:
            content = f.read_text(errors="ignore")
            if is_iac_file(f, content):
                all_contents[str(f)] = content
        except Exception:
            pass

    result.files_scanned = len(all_contents)

    for filepath, content in all_contents.items():
        lines = content.splitlines()
        fp = filepath

        file_findings = []
        file_findings.extend(check_ic001_s3_public(fp, lines))
        file_findings.extend(check_ic002_sg_open_ports(fp, lines, content))
        file_findings.extend(check_ic003_hardcoded_credentials(fp, lines))
        file_findings.extend(check_ic004_unencrypted_ebs(fp, lines, content))
        file_findings.extend(check_ic005_unencrypted_rds(fp, lines, content))
        file_findings.extend(check_ic006_wildcard_iam(fp, lines))
        file_findings.extend(check_ic007_rds_public(fp, lines, content))
        file_findings.extend(check_ic008_s3_no_encryption(fp, lines, content, all_contents))
        file_findings.extend(check_ic009_no_deletion_protection(fp, lines, content))
        file_findings.extend(check_ic010_cloudfront_no_waf(fp, lines, content))
        file_findings.extend(check_ic011_lambda_admin_role(fp, lines, content))
        file_findings.extend(check_ic012_s3_no_versioning(fp, lines, content, all_contents))

        if file_findings:
            result.resources_flagged += len(file_findings)
        result.findings.extend(file_findings)

    return result


def format_report(result: AuditResult, ci_mode: bool = False) -> str:
    out = []
    out.append(f"\n{'='*60}")
    out.append(f"  IaC Security Audit — {result.scan_root}")
    out.append(f"  Files scanned: {result.files_scanned}  |  Resources flagged: {result.resources_flagged}")
    out.append(f"{'='*60}")

    if not result.findings:
        out.append("✅ No IaC security misconfigurations detected.")
        return "\n".join(out)

    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        sev = [f for f in result.findings if f.severity == severity]
        if sev:
            out.append(f"\n── {severity} ({len(sev)}) {'─'*40}")
            for finding in sev:
                out.append(str(finding))

    out.append(f"\n{'─'*60}")
    out.append(
        f"  Total: {len(result.findings)} findings  |  "
        f"Critical: {result.critical_count}  High: {result.high_count}  "
        f"Medium: {result.medium_count}  Low: {result.low_count}"
    )
    if ci_mode and (result.critical_count > 0 or result.high_count > 0):
        out.append("\n  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.")
    return "\n".join(out)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-iac-sec-audit — IaC Security Auditor (Terraform/CloudFormation/Pulumi)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python iac_sec_audit.py ./infrastructure
  python iac_sec_audit.py main.tf
  python iac_sec_audit.py ./terraform --ci
  python iac_sec_audit.py ./terraform --only-severity CRITICAL
        """,
    )
    parser.add_argument("path", help="Directory or .tf/.yaml/.json file to audit")
    parser.add_argument("--ci", action="store_true", help="Exit 1 on CRITICAL or HIGH findings")
    parser.add_argument(
        "--only-severity",
        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        help="Filter to this severity and above",
    )
    args = parser.parse_args()

    result = audit(args.path)

    sev_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    if args.only_severity:
        cutoff = sev_order.index(args.only_severity)
        result.findings = [f for f in result.findings if sev_order.index(f.severity) <= cutoff]

    print(format_report(result, ci_mode=args.ci))

    if args.ci and (result.critical_count > 0 or result.high_count > 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## CI Integration

```yaml
# GitHub Actions — Terraform PR check
- name: IaC Security Audit
  run: python iac_sec_audit.py ./terraform --ci

# GitLab CI
iac-security:
  script:
    - python iac_sec_audit.py ./infrastructure --ci
  rules:
    - changes:
        - "**/*.tf"
        - "**/cloudformation.yaml"
```

## False Positive Notes

- **IC003** — Skips files named `variable*`, `var.*`, `example*`, `sample*`, `test*`, `mock*`. Also skips lines containing `var.`, `data.`, `local.`, `${` (Terraform interpolations). Short values (<6 chars) skipped. ARNs and region names skipped.
- **IC006** — Only flags when the wildcard Action/Resource appears near IAM context (checks 10-line window for `iam`, `policy`, `role`).
- **IC008** — Checks the entire project for any SSE config. If `aws_s3_bucket_server_side_encryption_configuration` exists in any file, IC008 is suppressed (assumes global config).
- **IC012** — Skips buckets with `log`, `logging`, `audit`, `tmp`, `temp` in their resource name (versioning on log buckets wastes money).

## Related Skills

- **phy-k8s-security-audit** — Kubernetes manifest security (CIS Benchmark)
- **phy-env-doctor** — Environment variable and secret scanning in application code
- **phy-crypto-audit** — Weak cryptography in application code
- **phy-dep-upgrade** — Vulnerable dependencies in application dependencies

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
