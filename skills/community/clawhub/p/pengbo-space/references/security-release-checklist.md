# Pengbo Space Security Release Checklist

## P0 (same day)
- [x] Default high-risk behaviors disabled (no autostart / no forced cron / no silent daemon)
- [x] No remote download-and-execute on first run
- [x] API egress allowlist enabled (`https://pengbo.space/api/v1` only)
- [x] No generic shell passthrough; command set is explicit/whitelisted
- [ ] Update package signature verification enforced (required before update apply)

## P1 (1-3 days)
- [ ] Platform code signing:
  - [ ] Windows EV/OV
  - [ ] macOS Developer ID + notarization
  - [ ] Linux apt/rpm repo signing
- [x] Release artifact SHA256 generation script
- [x] SBOM generation script (CycloneDX, requires `cyclonedx-py`)
- [x] Release notes template includes permissions/network/update mechanism

## P2 (within 1 week)
- [x] Dependency lock check in CI
- [x] Pre-release malware scan script scaffold (YARA/ClamAV/VT hook)
- [x] False-positive appeal template prepared

---

## Mandatory release gate
A release is blocked if any of the following is true:
1. API host allowlist check fails.
2. Any non-whitelisted command execution path exists.
3. Signature verification test fails for update package.
4. Malware scan hits exceed threshold.
