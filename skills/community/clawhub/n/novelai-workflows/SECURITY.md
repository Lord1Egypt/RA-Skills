# Security policy

## Credential handling

Never open an issue or pull request containing a NovelAI token, password, cookie, Authorization header, `.env` file, or private generation output. The live test script reads credentials from the process environment and is designed not to print or persist them.

If a credential is exposed, revoke it in the provider account immediately and create a replacement.

## Reporting a vulnerability

For a security issue in this repository, use a private GitHub Security Advisory for the repository when available. If that channel is not available, contact the repository maintainer privately before posting details publicly.

Include a minimal reproduction, affected file or version, impact, and a suggested mitigation. Do not include live credentials or private user data.
