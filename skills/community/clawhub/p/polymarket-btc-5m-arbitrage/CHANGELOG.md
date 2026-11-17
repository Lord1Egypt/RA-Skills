# Changelog

## 1.0.2 - security review remediation

- Removed the bundled third-party billing integration and all billing endpoints.
- Removed the hardcoded billing API key and billing environment variable.
- Reframed the package as a read-only market scanner; it does not place orders or make markets.
- Removed private-key and Polymarket API-key configuration because the bundled code never implemented order execution.
- Added explicit network, filesystem, secret, and external-write capability declarations.
- Added warnings about real-money risk, secret handling, compliance, and the non-guaranteed nature of displayed edges.
- Corrected the candidate calculation to compare complementary Up/Down asks instead of a single token bid/ask.
- Made one-shot scanning the safe default; continuous polling requires an explicit interval.
