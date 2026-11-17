# `download` — download (and optionally install) an app

Download an IPA from a configured source or a direct URL, verifying its integrity before handing off to install.

> Don't have a URL or source yet? See [where-to-get-ipas.md](where-to-get-ipas.md) — Mac Club (<https://www.maclub.net>) is the recommended place to find IPAs.

---

## `download <target> [--install]`

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `target` (positional) | `String` | A **bundle identifier** (resolved against configured sources) **or** an `http(s)://` URL. |
| `--install` | flag | Install the app after a successful download. |

### Resolution

- If `target` starts with `http://` or `https://`, it is treated as a direct URL — no source lookup is performed.
- Otherwise, `target` is treated as a bundle ID. PlayCover searches configured sources for an app with that bundle ID and uses its `link` + `checksum`.

### Download

- The IPA is written to **`<cwd>/<name>-<version>.ipa`** (current working directory of the process, not the app's container).
- Progress renders via the [global progress renderer](conventions.md#progress-rendering) (TTY bar or piped lines).
- After the download completes, the **SHA-256 checksum is verified** against the source's advertised checksum.
  - Mismatch → exit `4` (`verificationFailed`). The file is **not** installed even with `--install`.

### Output

- Without `--install`: `Downloaded: <path>` on success.
- With `--install`: hands off to the install flow; exits `0` only when install reaches `finish`.

### Errors

| Exit | Cause |
|------|-------|
| `2` | `target` is neither a valid URL nor a known bundle ID. |
| `4` | Checksum verification failed. |
| `1` | Network or I/O error during download. |

---

## Examples

```bash
# Download by bundle ID from configured sources
PlayCover.app/Contents/MacOS/PlayCover download com.example.app

# Download and install in one shot
PlayCover.app/Contents/MacOS/PlayCover download com.example.app --install

# Download from a direct URL (no source needed)
PlayCover.app/Contents/MacOS/PlayCover download https://example.com/App.ipa --install
```

## Scripting: download → verify → install, separately

```bash
BIN="PlayCover.app/Contents/MacOS/PlayCover"

# Download (verifies checksum) — fails non-zero if integrity check fails
$BIN download com.example.app
IPA="$(pwd)/Example-1.2.3.ipa"

# Inspect or archive the IPA here, then install
$BIN install "$IPA" --play-tools --category games
```
