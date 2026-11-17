# Validation record

## Functional checks

- Node.js 22.23.2 on macOS: `node --test tests/magbox.test.mjs`, nine suites pass.
- Real loopback HTTP requests cover ranges, malformed encoding, nonregular files,
  symlink swaps, quoted multipart boundaries, binary delimiter lookalikes, filename
  rejection, concurrent collisions, Host/Origin checks, byte/concurrency/time
  limits, interrupted bodies, interrupted saving, and full-disk rollback.
- Injected download failures close the open file descriptor and leave the server
  available. Files still being saved are absent from lists and blocked for download.
- Browser smoke check: dark grid, white upload page, hostile filename displayed
  literally, raster preview, successful upload, duplicate upload displayed as
  `upload-me-v2.txt`, and inbox counts/total bytes. No browser errors observed.
- `plutil -lint templates/magbox.plist` passes. Tests check both service templates'
  paths, loopback defaults, and user-service configuration. No service was installed;
  live Linux/systemd startup remains untested on this macOS host.
- SKILL.md frontmatter parsed with standard-library YAML and its name, description,
  version, and declared settings checked. The optional Python validation helper
  could not start because its YAML module was unavailable; no dependency was added.

## Scanner scope and result

The five literal substrings supplied in the handoff were checked case-insensitively
across **every file in this package**, including documentation and tests: zero hits.
That check alone is not a ClawHub compatibility claim.

The public ClawHub prepublication static engine **v2.4.26**, pinned at commit
`e769826f1f951c5fb7d4838bab1cc03a9ee31d53`, was run locally with the package's full
file contents and actual frontmatter. Result: **clean, zero findings**.

The first static pass flagged broad environment access combined with browser
network code in the single server file. Configuration now reads only the eight
explicit application settings, all declared in metadata; it never passes the
whole environment to configuration. No source was obscured or omitted.

Source references:

- [Static rules](https://github.com/openclaw/clawhub/blob/e769826f1f951c5fb7d4838bab1cc03a9ee31d53/convex/lib/moderationEngine.ts)
- [Static publish wiring](https://github.com/openclaw/clawhub/blob/e769826f1f951c5fb7d4838bab1cc03a9ee31d53/convex/lib/staticPublishScan.ts)
- [Hosted worker](https://github.com/openclaw/clawhub/blob/e769826f1f951c5fb7d4838bab1cc03a9ee31d53/scripts/security/run-codex-scan-worker.ts)
- [Scan CLI documentation](https://github.com/openclaw/clawhub/blob/e769826f1f951c5fb7d4838bab1cc03a9ee31d53/docs/cli.md)

The published source uses contextual rules, not the reported five-token list.
Hosted processing also invokes additional scanners and a final judge. Its deployed
revision and full verdict were not verified. The CLI documentation says local-path
hosted scans are unavailable. **Hosted compatibility remains unverified.** No file
was submitted to ClawHub, and no publication or hosted scan was attempted.
