# aws-cli

## Overview

Repackaged AWS CLI v2 for OpenClaw gateway containers. Unlike Go-based skills (compiled
from source) or npm skills (bundled with esbuild), this skill downloads and repackages
the official AWS binary distribution.

## Architecture

- `version.txt` tracks the skill packaging version (not the upstream AWS CLI version)
- `scripts/package.sh` downloads, installs, and tarballs the AWS CLI for a given arch
- No source code to compile. No package manager.

## Build

```bash
bash scripts/package.sh --version 0.1.0 --arch amd64
bash scripts/package.sh --version 0.1.0 --arch arm64
```

Produces `dist/aws-cli_0.1.0_linux_<arch>.tar.gz`.

## How it works

The AWS CLI v2 includes a standalone installer that bundles Python and all dependencies.
The `package.sh` script downloads this installer, runs it to a staging directory, and
packages the result as a tarball. The consumer extracts the tarball and symlinks `aws`
into their PATH.

## Credentials

Uses the AWS default credential provider chain. On EC2, this resolves via IMDS.
The instance IMDS hop limit must be 2+ for Docker containers (handled by PAN-52).

## Release

Release-please uses `release-type: "simple"` with `version.txt`. On release, `package.sh`
runs for both arm64 and amd64. The publish job uses QEMU for arm64 cross-build on the
x86_64 GitHub Actions runner.
