# aws-s3

## Overview

Self-contained AWS S3 SDK bundle for OpenClaw agents. Unlike the Go-based skills in this
repo, this is an npm package that bundles `@aws-sdk/client-s3` with all transitive
dependencies into a single CommonJS file using esbuild.

## Architecture

- `src/index.mjs` barrel re-exports everything from `@aws-sdk/client-s3`
- `esbuild.config.mjs` bundles `src/index.mjs` into `dist/index.cjs` (CommonJS, Node 22 target)
- `dist/index.cjs` (built, gitignored) is the complete bundled SDK
- `test/exports.test.mjs` validates the bundle exports expected symbols using `node:test`

## Build

```bash
npm ci && npm run build
```

## Test

```bash
npm test
```

Tests require a prior build as they validate the `dist/index.cjs` output.

## How it works

The gateway container has Node.js but no internet and no `@aws-sdk` installed. This package
bundles `@aws-sdk/client-s3` and all its transitive dependencies into a single CJS file
using esbuild. The tarball from `npm pack` is installed into the container via
`npm install <tarball>`.

## Credentials

Uses the AWS SDK default credential provider chain. On EC2/ECS this resolves via IMDS
automatically. No environment variables are required for authentication. The IMDS hop
limit must be 2+ when running inside Docker (handled by PAN-52).

## Release

Release-please uses `release-type: "node"` to version this package. On release, `npm pack`
produces a tarball that is uploaded to the GitHub release and published to clawhub.
