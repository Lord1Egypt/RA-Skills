# ClawHub Scan Report

Scan ID: skill:li-wps-mod:1.0.0
Status: succeeded

This archive contains the stored security scan results for the submitted ClawHub version.

## How to read this report

Start with `clawscan.json`. ClawScan is the primary security verdict for the submitted artifact. Its `summary` field is the short explanation of what triggered the result, and `guidance` explains what to change before uploading a fixed version.

- `malicious` means ClawHub blocked the submitted version from public install surfaces.
- `suspicious` means ClawHub found behavior that needs review before users should rely on it.
- `clean` means ClawHub did not find blocking security issues in this scan.

VirusTotal results are supporting reputation telemetry. They can help explain a risk signal, but they are not the sole source of ClawHub's final verdict.

## Files

- `manifest.json`: artifact identity, scan status, timestamps, and writeback state.
- `clawscan.json`: final ClawScan verdict, summary, guidance, and findings.
- `skillspector.json`: SkillSpector structure and agentic-risk signals when available.
- `static-analysis.json`: deterministic scanner findings, reason codes, and static summary.
- `virustotal.json`: external reputation counts and status when available.
- `README.md`: this interpretation guide.
