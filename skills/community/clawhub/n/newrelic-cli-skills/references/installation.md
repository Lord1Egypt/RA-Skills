# CLI installation and checksum verification

Use an explicit release from the [official release list](https://github.com/newrelic/newrelic-cli/releases).
Download its archive for your OS/architecture and its official checksum manifest.
Compute SHA-256 locally (PowerShell: `Get-FileHash -Algorithm SHA256 <archive>`;
macOS: `shasum -a 256 <archive>`; Linux: `sha256sum <archive>`). Compare against the
entry for that exact filename in the same release's manifest. Compare hexadecimal
hashes case-insensitively: PowerShell prints uppercase, while these manifests use
lowercase. If absent or different, stop. Never skip or disable checksum checks.
Only after a match, extract the archive, place `newrelic` (`newrelic.exe` on Windows)
on `PATH`, and run `newrelic --version`.
Confirm the selected release before configuring credentials or using commands.
Dataset and dataset-version commands require CLI >=v0.117.0.

## Ongoing Scoop manifest/archive mismatch

Scoop uses the bucket's default branch, not a release tag. The official bucket's
[default-branch manifest reviewed on 2026-11-24](https://github.com/newrelic/newrelic-cli/blob/1e741dd170d59df6b356a68cc7f56a0a72c98194/newrelic-cli.json)
identifies **0.117.1**, but its SHA-256 still does not match the published Windows
archive. The tag commits below carry older manifests; that release-version lag is
not itself the checksum defect. The later manifest bump does not fix the mismatch.

Each row names an immutable manifest revision and its selected Windows x86_64 ZIP.
The downloaded ZIP SHA-256 was independently recomputed and matches both that
release's official checksum manifest and GitHub asset digest, but not the Scoop hash:

| Manifest revision | Manifest version | Manifest SHA-256 | Published ZIP SHA-256 |
|---|---|---|---|
| [`05ba094109ac9db08c72c6e13f213ee8c58f0959`](https://github.com/newrelic/newrelic-cli/blob/05ba094109ac9db08c72c6e13f213ee8c58f0959/newrelic-cli.json) (v0.117.0 tag) | 0.116.4 | `3af5fd7185959f85b2780476429ab261c8df6d9b80e333087c28034a01fd4a7e` | `227993a3332e458e92f1f5eb569d051b0473a26b4b57e6f0c08b71d247e446e7` |
| [`68884ea61cd53b328e3bf391dc61995173ed8dd6`](https://github.com/newrelic/newrelic-cli/blob/68884ea61cd53b328e3bf391dc61995173ed8dd6/newrelic-cli.json) (v0.117.1 tag) | 0.117.0 | `dbe3ae9b440e15ae0f46715bf96828c520c4423307c133724f091162abf2d3c0` | `bebf021ebfa17a2119d510981c560abce7671bb96deb98ff85c6b7ceb316908d` |
| [`1e741dd170d59df6b356a68cc7f56a0a72c98194`](https://github.com/newrelic/newrelic-cli/blob/1e741dd170d59df6b356a68cc7f56a0a72c98194/newrelic-cli.json) (default branch at review) | 0.117.1 | `d91e109082cf7c1840a3b7839bbb0664ec75efc4fc66c033d4bf60ebb940b91c` | `65fed60b603b360a8b1ea547bd03e4c9a254a3b6d5016d7488eecdaef801e88d` |

Treat the Scoop route as blocked; do not bypass checksum verification. Re-evaluate
only when the exact archive selected by the current manifest matches its declared
hash and the same release's published checksum. A version bump alone is not proof.
These observations cover the three rows, not every historical or future manifest;
the cause of the mismatches has not been established.

For manual Windows x86_64 installation, the archive matching the reviewed release is:

https://github.com/newrelic/newrelic-cli/releases/download/v0.117.1/newrelic-cli_0.117.1_Windows_x86_64.zip

Its SHA-256 is the last row above; still apply the checksum and version checks at
the top of this reference. The previously verified
[v0.117.0 archive](https://github.com/newrelic/newrelic-cli/releases/download/v0.117.0/newrelic-cli_0.117.0_Windows_x86_64.zip)
is the middle row, not a v0.117.1 binary.

## Scope of evidence

The checksum check detects corruption and manifest drift; it does **not authenticate
the release**. An attacker able to replace both the archive and its adjacent checksum
manifest can make them agree. These releases also publish detached signatures, but
this procedure has not verified a signing key or signature; it makes no signature-
verification claim. Where authenticated origin is required, stop until a trusted
signing identity and verification procedure have been independently established.

The supplied [immutable source comparison](https://github.com/newrelic/newrelic-cli/compare/05ba094109ac9db08c72c6e13f213ee8c58f0959...68884ea61cd53b328e3bf391dc61995173ed8dd6)
and full-source verification of 574 Git blobs show changes only to CHANGELOG.md
and newrelic-cli.json. Runtime, commands, help, and dependencies are unchanged.
This refresh did not execute any release binary or installer. The Windows archive
checksum observations do not validate every OS artifact or establish installer
safety. Existing activation, diagnostic, security, and publication blockers remain
separate and unresolved. Raw verification evidence is retained outside this repository.
