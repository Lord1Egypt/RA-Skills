# Structured report schema

The scanner should build one JSON result model before rendering any report. The model is the stable input for Markdown export, JSON artifacts, and future scan diffs.

```json
{
  "schemaVersion": "1.0",
  "scan": {
    "projectName": "example-app",
    "scope": "repository",
    "packageManager": "npm",
    "completedAt": "2026-09-18T12:00:00+08:00",
    "networkChecks": {"executed": false, "commands": [], "note": "Registry checks were skipped."}
  },
  "dependencies": [{"name": "example", "version": "1.2.3", "kind": "runtime", "path": "app"}],
  "findings": [{
    "id": "lifecycle-script:example:postinstall",
    "ruleId": "lifecycle-script",
    "severity": "High",
    "title": "Install-time script requires review",
    "packagePath": "example",
    "evidence": "package.json scripts.postinstall",
    "confidence": "confirmed",
    "impact": "Code runs during installation.",
    "action": "Review the script and pin or remove it if unnecessary.",
    "verify": "npm view example scripts --json",
    "blastRadius": "Install and CI environments"
  }],
  "actions": ["Review the install-time script before upgrading."]
}
```

Finding IDs must be deterministic from rule ID, package name/path, and other stable evidence. Do not use timestamps or finding array positions. Keep network-check context explicit so a report never implies registry-backed coverage when it was skipped.

Use `scripts/export_report.py` only after the user requests an export or a report/CI mode explicitly enables it:

```bash
python3 scripts/export_report.py --input scan-result.json
python3 scripts/export_report.py --input scan-result.json --format json --output-dir reports
```

The default output is Markdown. The exporter writes a timestamped `npm-package-scan-<project>-YYYYMMDD-HHmm.<ext>` file unless `--output` is supplied.
