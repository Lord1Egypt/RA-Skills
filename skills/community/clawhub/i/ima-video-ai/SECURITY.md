# Security Disclosure: ima-video-ai

The detailed security policy lives in the layered references, but the release-facing summary is:

- `api.imastudio.com` handles product lookup, task creation, and polling.
- `imapi.liveme.com` handles upload-token requests when local media or derived cover uploads are needed.
- Binary uploads go to the pre-signed HTTPS storage URL returned by the upload-token API.
- User-supplied remote media is limited to direct public HTTPS URLs and may be downloaded locally into the OS temp directory for probing, validation, and video-cover extraction before the temp files are deleted.

Further details:

- Network endpoints, credential flow, temp-file behavior, and privacy notes: `references/shared/security-and-network.md`
- API failure translation and user-visible error handling: `references/shared/error-policy.md`
- Task create and polling contract: `references/operations/api-contract-and-errors.md`

This repo remains video-only. No additional capability-specific security surface is documented outside those files.
