# Packaging matrix

| Host | Recommended target | Notes |
| --- | --- | --- |
| macOS | `dmg`, `zip` | Build universal only when both arm64 and x64 support are required. Signing and notarization need Apple credentials. |
| Windows | `nsis`, optional `portable` | Build on Windows for the most reliable native modules and code signing. |

Use `electron-builder` first. Its dependency installation can fail after package metadata has resolved because Electron's post-install step separately downloads a platform binary. Confirm both `node_modules/electron` and the platform binary are present before treating installation as successful.

Select the architecture explicitly: arm64 for Apple Silicon, x64 for Intel, and universal only when both are required and tested. Use an application identifier in reverse-DNS format. Include only renderer output, Electron files, and assets in the package; exclude source maps and development dependencies when practical.

Set an explicit platform icon for every release. On macOS, `electron-builder` needs an `.icns`; on Windows it needs an `.ico`. Generate a simple fallback only when the user has not supplied brand artwork, and state that it is a generated icon in the release handoff.

If download access is blocked, a matching archive may exist in `~/Library/Caches/electron/` with a name like `electron-v<version>-darwin-arm64.zip`. It is a valid local-build fallback, not a substitute for a reproducible CI build. Use only an exact version and architecture match, record the fallback in the handoff, and create the DMG/ZIP after assembling the `.app`.

`codesign --verify` only confirms bundle integrity. Ad-hoc signatures and unsigned builds normally fail `spctl --assess`; macOS may require the user to approve the first launch in System Settings. A Developer ID signature still needs notarization to avoid Gatekeeper warnings. Do not bypass platform security mechanisms.
