---
name: AWS CLI
description: AWS CLI v2 for OpenClaw agents (repackaged official binary)
version: 0.1.0
author: panthrocorp
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - aws
    emoji: "☁️"
    homepage: https://github.com/PanthroCorp-Limited/openclaw-skills
    os: ["linux"]
---

# AWS CLI Skill

Repackaged AWS CLI v2 for use inside the OpenClaw gateway container. Contains the
official AWS binary with its bundled Python runtime. No additional dependencies required.

## Installation

Download the release tarball for your architecture and extract:

```bash
TAG=$(curl -fsSL "https://api.github.com/repos/PanthroCorp-Limited/openclaw-skills/releases" \
  | grep -o '"tag_name":"aws-cli/v[^"]*"' | head -1 | cut -d'"' -f4)
VERSION=${TAG#aws-cli/v}
ARCH=$(uname -m); [ "$ARCH" = "aarch64" ] && ARCH="arm64" || ARCH="amd64"
curl -fsSL "https://github.com/PanthroCorp-Limited/openclaw-skills/releases/download/${TAG}/aws-cli_${VERSION}_linux_${ARCH}.tar.gz" \
  | tar -xz -C ~/.openclaw/
ln -sf ~/.openclaw/aws-cli/v2/current/bin/aws ~/.openclaw/bin/aws
```

Or install into the gateway container via docker exec:

```bash
docker exec openclaw-gateway bash -c '
  curl -fsSL "<tarball-url>" | tar -xz -C ~/.openclaw/
  ln -sf ~/.openclaw/aws-cli/v2/current/bin/aws ~/.openclaw/bin/aws
'
```

## Usage

```bash
aws s3 ls s3://my-bucket/
aws s3api list-objects-v2 --bucket my-bucket --prefix parsed/
aws s3 cp s3://my-bucket/key.json /tmp/key.json
aws sts get-caller-identity
```

## Authentication

Credentials resolve via the AWS SDK default credential provider chain. In an EC2/ECS
environment this uses IMDS (Instance Metadata Service) automatically.

Ensure the EC2 instance IMDS hop limit is set to 2 or higher when running inside Docker.
Without this, the container cannot reach the metadata endpoint for credentials.

Verify credentials are working:

```bash
aws sts get-caller-identity
```

## Important

- This package contains the official AWS CLI v2 with its bundled Python runtime.
- No system Python or additional libraries are required.
- The binary runs as any user (UID 1000 in the gateway container).
- Available for both arm64 (Graviton) and amd64 architectures.
