# Self-Hosted Langfuse

Use this reference when the target Langfuse deployment is not the default cloud environment.

## Treat self-hosting as a first-class path

Do not leave examples hardcoded to `cloud.langfuse.com` if the user runs a private deployment.

Always swap in the real deployment URL for:

- SDK initialization
- environment variables
- API examples
- setup docs
- troubleshooting steps

## Environment guidance

Prefer the currently documented environment variable:

```bash
LANGFUSE_BASE_URL="https://langfuse.internal.example.com"
```

Typical self-hosted example:

```bash
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_BASE_URL="https://langfuse.internal.example.com"
```

If an existing codebase uses another host variable naming convention, do not churn it blindly. First confirm which SDK version and wrapper layer the project actually uses.

## Compatibility checks

Langfuse documentation notes self-hosted compatibility requirements for full feature support:

- Python SDK v3 requires Langfuse platform version `>= 3.125.0`
- TypeScript SDK v4 requires Langfuse platform version `>= 3.95.0`

When a self-hosted installation behaves oddly, check platform version before assuming the instrumentation code is wrong.

## Common self-hosted failure points

Separate infrastructure problems from application-instrumentation problems.

Likely infra issues:

- wrong base URL
- internal DNS mismatch
- reverse proxy path or header issues
- TLS/certificate problems
- auth keys from the wrong project/environment
- stale self-hosted platform version
- network egress/ingress restrictions between app and Langfuse

Likely app issues:

- missing flush in short-lived processes
- instrumentation not initialized early enough
- env vars not loaded in the real runtime
- missing user/session identifiers
- traces created but not nested meaningfully

## Example adaptation pattern

### Cloud default

```bash
LANGFUSE_BASE_URL="https://cloud.langfuse.com"
```

### Self-hosted

```bash
LANGFUSE_BASE_URL="https://langfuse.internal.example.com"
```

### Public API example

```bash
curl -u public-key:secret-key \
  https://langfuse.internal.example.com/api/public/projects
```

## Agent behavior rules

When building examples, docs, or patches for self-hosted users:

1. Use the real host everywhere.
2. Keep auth examples the same unless the deployment truly differs.
3. Mention version compatibility when debugging unexplained missing features.
4. Call out private-network assumptions clearly.
5. Do not imply EU/US cloud region selection if the deployment is self-hosted.
