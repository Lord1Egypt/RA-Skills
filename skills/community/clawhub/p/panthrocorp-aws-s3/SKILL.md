---
name: AWS S3
description: Self-contained AWS S3 SDK bundle for OpenClaw agents
version: 0.2.1 # x-release-please-version
author: panthrocorp
license: MIT-0
metadata:
  openclaw:
    requires:
      npm:
        - "@openclaw/aws-s3"
    emoji: "🪣"
    homepage: https://github.com/PanthroCorp-Limited/openclaw-skills
    os: ["linux"]
---

# AWS S3 Skill

Pre-bundled AWS S3 SDK for use inside the OpenClaw gateway container. All transitive
dependencies are bundled. No internet access required at install time.

## Installation

Install from the release tarball into the gateway container:

```bash
TAG=$(curl -fsSL "https://api.github.com/repos/PanthroCorp-Limited/openclaw-skills/releases" \
  | grep -o '"tag_name":"aws-s3/v[^"]*"' | head -1 | cut -d'"' -f4)
VERSION=${TAG#aws-s3/v}
URL="https://github.com/PanthroCorp-Limited/openclaw-skills/releases/download/${TAG}/openclaw-aws-s3-${VERSION}.tgz"
docker exec openclaw-gateway npm install "$URL" --prefix /home/node/.openclaw/bin/.npm-global
```

Or from a downloaded tarball:

```bash
docker exec openclaw-gateway npm install /path/to/openclaw-aws-s3-0.1.0.tgz \
  --prefix /home/node/.openclaw/bin/.npm-global
```

## Usage

```js
const { S3Client, ListObjectsV2Command, GetObjectCommand } = require("@openclaw/aws-s3");

const client = new S3Client({});

const list = await client.send(new ListObjectsV2Command({
  Bucket: process.env.EMAIL_BUCKET_NAME,
  Prefix: `parsed/${agentName}/`,
}));

const obj = await client.send(new GetObjectCommand({
  Bucket: process.env.EMAIL_BUCKET_NAME,
  Key: "parsed/agent/email.json",
}));
const body = await obj.Body.transformToString();
```

## Authentication

Credentials resolve via the AWS SDK default credential provider chain. In an EC2/ECS
environment this uses IMDS (Instance Metadata Service) automatically. Ensure the IMDS
hop limit is set to 2 or higher when running inside Docker.

No environment variables are required for authentication. `AWS_REGION` should be set
if the region cannot be inferred from instance metadata.

## Important

- This package bundles `@aws-sdk/client-s3` with all transitive dependencies.
- No network access is needed at install time.
- The gateway container must have Node.js available.
- All S3 commands from the SDK are available, not just the ones shown above.
