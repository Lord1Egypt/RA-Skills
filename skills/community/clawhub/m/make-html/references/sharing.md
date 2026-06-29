# Sharing HTML Artifacts

Use PageDrop when the user asks for a hosted preview, shareable link, or cross-device review of a finished HTML artifact. PageDrop is an optional delivery path, not a replacement for local validation or the local file.

## Guardrails

- Validate the local artifact before uploading it.
- Upload only after the user asks for a hosted/shareable link or explicitly confirms third-party sharing.
- Never upload credentials, secrets, tokens, private customer data, personal data, or internal-only material. Review source excerpts, comments, metadata, embedded data, and hidden UI before sharing.
- Treat the generated URL as accessible to anyone who receives it. An expiring link is not a privacy boundary.
- Treat password protection as defense in depth, not permission to upload sensitive material.
- Keep the local `.html` file as the canonical artifact and fallback.
- Do not add PageDrop scripts, SDKs, or remote dependencies to the artifact. The upload is a separate delivery step.

## Upload

From the skill directory, use the bundled dependency-free uploader:

```bash
node scripts/pagedrop-upload.mjs /absolute/path/to/artifact.html --ttl 1h
```

Supported TTLs:

- `1h` for quick review; use this default when the user does not specify.
- `1d` or `3d` for longer review windows.
- `once` only when a single successful view is intended.

Optional sharing controls:

```bash
# Memorable URL: https://quarterly-review.pagedrop.io
node scripts/pagedrop-upload.mjs artifact.html --ttl 1d --custom-path quarterly-review

# Password protection: read the password from an environment variable
node scripts/pagedrop-upload.mjs artifact.html --ttl 1d --password-env PAGEDROP_PASSWORD

# Combine both controls
node scripts/pagedrop-upload.mjs artifact.html --ttl 1d \
  --custom-path quarterly-review \
  --password-env PAGEDROP_PASSWORD
```

Use the controls deliberately:

- Omit both controls by default.
- Use `--custom-path` only when the user asks for a memorable/custom URL. Custom paths are easier to guess and may disclose project context.
- Custom paths must be 3-63 lowercase letters, numbers, or hyphens, with no leading or trailing hyphen.
- If a requested custom path is unavailable, do not silently fall back to a random URL. Offer another path or ask the user.
- Use `--password-env` only when the user asks for password protection. The value names an environment variable containing the password; it is not the password itself.
- Passwords must be 1-128 characters. Never put a password in command arguments, logs, the HTML, the filename, the custom path, or the URL.
- If the user requests password protection without supplying a password, generate one locally and deliver it through an approved secure channel.
- Suggest password protection when a memorable path needs access control, but do not add it silently.

The script sends the HTML to `https://pagedrop.io/api/upload` and prints the returned URL. It requires Node.js and no API key. It intentionally uses Node's raw HTTPS client because PageDrop rejects browser-style `fetch` requests.

If PageDrop rejects the content, rate-limits the request, or is unavailable, do not retry aggressively. Return the local artifact and report the upload failure.

## Verify And Return

Open the returned URL in a real browser when possible and confirm the title, primary content, and one meaningful interaction. A raw HTTP client may encounter a browser security checkpoint, so do not treat a failed `curl` preview as proof that the artifact itself is broken.

Return:

- the PageDrop URL
- the selected TTL or expiry window
- whether a custom path or password protection was used
- the local artifact path
- any hosted-preview verification gap

Service references: `https://pagedrop.io/about` and `https://pagedrop.io/faq`.
