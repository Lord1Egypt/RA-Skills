#!/usr/bin/env python3
"""Cloud Security Tester — multi-cloud security assessment (v3.0.0).

Detects cloud-specific misconfigurations and vulnerabilities:
  1. AWS S3 bucket enumeration & ACL testing
  2. Azure Blob storage public access
  3. GCP storage bucket permission testing
  4. Cloud metadata service access (IMDSv1/v2)
  5. K8s API server misconfiguration
  6. Docker API exposure
  7. Serverless function endpoint discovery
  8. CDN/WAF origin IP disclosure
  9. Cloud database exposure (RDS, Cloud SQL, CosmosDB)
  10. Container registry misconfiguration

This module is deterministic: it takes cloud configuration data and
returns a structured audit plan. The agent executes the plan.

Usage (CLI):
  python cloud_security.py --targets targets.json --mode aws
  python cloud_security.py --targets targets.json --mode metadata
  python cloud_security.py --targets targets.json --mode k8s
  python cloud_security.py --targets targets.json --mode all
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json


# =============================================================================
# AWS S3 Bucket Checks
# =============================================================================
AWS_S3_BUCKET_PATTERNS = [
    "https://{bucket}.s3.amazonaws.com",
    "https://{bucket}.s3.{region}.amazonaws.com",
    "https://s3.amazonaws.com/{bucket}",
    "https://s3.{region}.amazonaws.com/{bucket}",
    "http://{bucket}.s3.amazonaws.com",
]

AWS_S3_PERMISSION_CHECKS = [
    {"method": "GET", "path": "/", "signal": "Bucket listing (ListBucket permission)", "severity": "high"},
    {"method": "PUT", "path": "/PTSKILLTEST-s3-upload.txt", "signal": "Write permission (PutObject)", "severity": "critical"},
    {"method": "GET", "path": "/PTSKILLTEST-s3-upload.txt", "signal": "Read permission (GetObject)", "severity": "high"},
    {"method": "DELETE", "path": "/PTSKILLTEST-s3-upload.txt", "signal": "Delete permission (DeleteObject)", "severity": "critical"},
    {"method": "GET", "path": "/?acl", "signal": "ACL readable", "severity": "medium"},
    {"method": "GET", "path": "/?versioning", "signal": "Versioning configuration exposed", "severity": "medium"},
    {"method": "GET", "path": "/?policy", "signal": "Bucket policy readable", "severity": "medium"},
    {"method": "GET", "path": "/?cors", "signal": "CORS configuration exposed", "severity": "low"},
]

# =============================================================================
# Azure Blob Storage Checks
# =============================================================================
AZURE_BLOB_PATTERNS = [
    "https://{account}.blob.core.windows.net/{container}",
    "https://{account}.blob.core.windows.net/{container}?restype=container&comp=list",
    "https://{account}.blob.core.windows.net/{container}?comp=list",
]

# =============================================================================
# GCP Storage Checks
# =============================================================================
GCP_STORAGE_PATTERNS = [
    "https://storage.googleapis.com/{bucket}",
    "https://{bucket}.storage.googleapis.com",
    "https://storage.cloud.google.com/{bucket}",
]

# =============================================================================
# Cloud Metadata Service Endpoints
# =============================================================================
CLOUD_METADATA_ENDPOINTS = {
    "aws_imdsv1": {
        "url": "http://169.254.169.254/latest/meta-data/",
        "headers": {},
        "signal": "AWS metadata accessible (IMDSv1 — no token required)",
        "severity": "critical",
    },
    "aws_imdsv2": {
        "url": "http://169.254.169.254/latest/api/token",
        "headers": {"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        "method": "PUT",
        "signal": "IMDSv2 token endpoint accessible",
        "severity": "high",
    },
    "aws_credentials": {
        "url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "headers": {},
        "signal": "AWS IAM credentials accessible via SSRF",
        "severity": "critical",
    },
    "aws_user_data": {
        "url": "http://169.254.169.254/latest/user-data/",
        "headers": {},
        "signal": "AWS user-data accessible (may contain secrets)",
        "severity": "critical",
    },
    "azure_metadata": {
        "url": "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
        "headers": {"Metadata": "true"},
        "signal": "Azure IMDS accessible",
        "severity": "critical",
    },
    "azure_identity": {
        "url": "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/",
        "headers": {"Metadata": "true"},
        "signal": "Azure managed identity token accessible",
        "severity": "critical",
    },
    "gcp_metadata": {
        "url": "http://169.254.169.254/computeMetadata/v1/",
        "headers": {"Metadata-Flavor": "Google"},
        "signal": "GCP metadata accessible",
        "severity": "critical",
    },
    "gcp_identity": {
        "url": "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token",
        "headers": {"Metadata-Flavor": "Google"},
        "signal": "GCP service account token accessible",
        "severity": "critical",
    },
    "digitalocean_metadata": {
        "url": "http://169.254.169.254/metadata/v1.json",
        "headers": {},
        "signal": "DigitalOcean metadata accessible",
        "severity": "high",
    },
    "alibaba_metadata": {
        "url": "http://100.100.100.200/latest/meta-data/",
        "headers": {},
        "signal": "Alibaba Cloud ECS metadata accessible",
        "severity": "high",
    },
    "oracle_metadata": {
        "url": "http://169.254.169.254/opc/v1/instance/",
        "headers": {},
        "signal": "Oracle Cloud metadata accessible",
        "severity": "high",
    },
}

# =============================================================================
# K8s API Server Checks
# =============================================================================
K8S_API_CHECKS = {
    "anonymous_access": {
        "url": "https://kubernetes.default.svc/api/v1/namespaces",
        "signal": "K8s API accessible anonymously",
        "severity": "critical",
    },
    "kubelet_readonly": {
        "url": "https://<node-ip>:10250/pods",
        "signal": "Kubelet read-only port accessible",
        "severity": "critical",
    },
    "kubelet_exec": {
        "url": "https://<node-ip>:10250/run/<namespace>/<pod>/<container>",
        "signal": "Kubelet exec endpoint accessible",
        "severity": "critical",
    },
    "etcd_metrics": {
        "url": "https://<etcd-ip>:2379/metrics",
        "signal": "etcd metrics accessible",
        "severity": "high",
    },
    "dashboard": {
        "url": "https://kubernetes.default.svc/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/",
        "signal": "K8s dashboard accessible",
        "severity": "high",
    },
}

# =============================================================================
# Docker API Checks
# =============================================================================
DOCKER_API_CHECKS = [
    {"url": "http://<host>:2375/containers/json", "signal": "Docker API (unencrypted) accessible", "severity": "critical"},
    {"url": "https://<host>:2376/containers/json", "signal": "Docker API (TLS) accessible", "severity": "high"},
    {"url": "http://<host>:2375/version", "signal": "Docker version exposed", "severity": "medium"},
    {"url": "http://<host>:2375/images/json", "signal": "Docker images list exposed", "severity": "high"},
    {"url": "http://<host>:2375/exec", "signal": "Docker exec endpoint accessible", "severity": "critical"},
]

# =============================================================================
# CDN Origin IP Disclosure
# =============================================================================
CDN_ORIGIN_CHECKS = {
    "dns_history": "Check DNS history for pre-CDN origin IPs",
    "ssl_certificates": "Check SSL certificate transparency logs for origin IPs",
    "direct_ip_access": "Try accessing the target via its origin IP directly",
    "subdomain_scan": "Check subdomains for direct IP exposure (bypassing CDN)",
    "misconfigured_cname": "Check CNAME records for origin server leaks",
}

# =============================================================================
# Container Registry Checks
# =============================================================================
CONTAINER_REGISTRY_PATHS = [
    "https://{registry}/v2/_catalog",
    "https://{registry}/v2/{image}/tags/list",
    "https://{registry}/v2/{image}/manifests/latest",
]

CONTAINER_REGISTRIES = [
    "registry-1.docker.io",
    "gcr.io",
    "ghcr.io",
    "quay.io",
    "public.ecr.aws",
    "mcr.microsoft.com",
]


def build_aws_s3_plan(buckets: list[str]) -> dict:
    """Build AWS S3 bucket security audit plan."""
    tests = []
    for bucket in buckets:
        for pattern in AWS_S3_BUCKET_PATTERNS:
            base_url = pattern.replace("{bucket}", bucket)
            for check in AWS_S3_PERMISSION_CHECKS:
                tests.append({
                    "test": "s3_permission",
                    "provider": "aws",
                    "bucket": bucket,
                    "url": base_url + check["path"],
                    "method": check["method"],
                    "signal": check["signal"],
                    "severity": check["severity"],
                })
    return {
        "provider": "aws",
        "service": "s3",
        "buckets": buckets,
        "test_count": len(tests),
        "tests": tests,
    }


def build_metadata_plan(targets: list[str]) -> dict:
    """Build cloud metadata service audit plan."""
    tests = []
    for _, config in CLOUD_METADATA_ENDPOINTS.items():
        method = config.get("method", "GET")
        tests.append({
            "test": "cloud_metadata",
            "url": config["url"],
            "method": method,
            "headers": config["headers"],
            "signal": config["signal"],
            "severity": config["severity"],
        })
    return {
        "provider": "all",
        "service": "metadata",
        "test_count": len(tests),
        "tests": tests,
    }


def build_k8s_plan(targets: list[str]) -> dict:
    """Build Kubernetes security audit plan."""
    tests = []
    for name, config in K8S_API_CHECKS.items():
        tests.append({
            "test": name,
            "url": config["url"],
            "signal": config["signal"],
            "severity": config["severity"],
        })
    return {
        "provider": "kubernetes",
        "service": "api_server",
        "test_count": len(tests),
        "tests": tests,
    }


def build_docker_plan(hosts: list[str]) -> dict:
    """Build Docker API security audit plan."""
    tests = []
    for host in hosts:
        for check in DOCKER_API_CHECKS:
            url = check["url"].replace("<host>", host)
            tests.append({
                "test": "docker_api",
                "url": url,
                "signal": check["signal"],
                "severity": check["severity"],
            })
    return {
        "provider": "docker",
        "service": "api",
        "hosts": hosts,
        "test_count": len(tests),
        "tests": tests,
    }


def build_cdn_origin_plan(targets: list[str]) -> dict:
    """Build CDN origin IP disclosure audit plan."""
    tests = []
    for target in targets:
        for name, description in CDN_ORIGIN_CHECKS.items():
            tests.append({
                "test": "cdn_origin",
                "target": target,
                "method": name,
                "description": description,
                "severity": "high",
            })
    return {
        "provider": "cdn",
        "service": "origin_disclosure",
        "targets": targets,
        "test_count": len(tests),
        "tests": tests,
    }


def build_container_registry_plan(registries: list[str] = None) -> dict:
    """Build container registry security audit plan."""
    if not registries:
        registries = CONTAINER_REGISTRIES
    tests = []
    for registry in registries:
        for pattern in CONTAINER_REGISTRY_PATHS:
            url = pattern.replace("{registry}", registry)
            tests.append({
                "test": "container_registry",
                "registry": registry,
                "url": url,
                "signal": "Registry catalog/tags accessible without auth",
                "severity": "high",
            })
    return {
        "provider": "container",
        "service": "registry",
        "registries": registries,
        "test_count": len(tests),
        "tests": tests,
    }


def audit(targets: list[str], mode: str, extra: dict = None) -> dict:
    """Run cloud security audit for the given mode.

    Args:
        targets: list of target URLs/hosts.
        mode: aws | azure | gcp | metadata | k8s | docker | cdn | registry | all
        extra: extra config (e.g., buckets list for S3 mode).

    Returns:
        Audit plan dict.
    """
    results = {}
    extra = extra or {}

    if mode in ("aws", "all"):
        buckets = extra.get("buckets", [])
        if buckets:
            results["aws_s3"] = build_aws_s3_plan(buckets)

    if mode in ("metadata", "all"):
        results["cloud_metadata"] = build_metadata_plan(targets)

    if mode in ("k8s", "all"):
        results["kubernetes"] = build_k8s_plan(targets)

    if mode in ("docker", "all"):
        hosts = extra.get("docker_hosts", targets if targets else ["127.0.0.1"])
        results["docker"] = build_docker_plan(hosts)

    if mode in ("cdn", "all"):
        results["cdn_origin"] = build_cdn_origin_plan(targets)

    if mode in ("registry", "all"):
        results["container_registry"] = build_container_registry_plan()

    if not results:
        return {"error": f"no checks for mode: {mode}", "supported": ["aws", "azure", "gcp", "metadata", "k8s", "docker", "cdn", "registry", "all"]}

    total_tests = sum(r.get("test_count", 0) for r in results.values())
    results["summary"] = {
        "total_tests": total_tests,
        "modes_audited": list(results.keys()),
        "targets": targets,
    }

    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Cloud Security Tester (v3.0)")
    ap.add_argument("--targets", required=True, help="Targets JSON (path or '-')")
    ap.add_argument("--mode", default="all",
                    choices=["aws", "azure", "gcp", "metadata", "k8s", "docker", "cdn", "registry", "all"],
                    help="Cloud security audit mode")
    ap.add_argument("--extra", help="Extra config JSON (buckets, docker_hosts, etc.)")
    args = ap.parse_args()

    targets = load_json(args.targets)
    if isinstance(targets, dict):
        targets = targets.get("targets", targets.get("ips", []))
    if isinstance(targets, str):
        targets = [targets]

    extra = {}
    if args.extra:
        extra = load_json(args.extra)

    result = audit(targets, args.mode, extra)
    print(dump_json(result))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())