---
name: gitcode-issue-scan-report
description: Use when a user asks to scan, audit, classify, reconcile, or report GitCode Issues and linked PR states, including requests for a reviewable Issue-closing script.
metadata:
  openclaw:
    requires:
      bins:
        - python
      anyBins:
        - gitcode-npm
        - gitcode
---

# GitCode Issue Scan Report

## Overview

Use `{baseDir}/scripts/scan_gitcode_issues.py` to perform a repeatable, read-only audit of a GitCode repository's Open Issues. The report classifies RFC, Feature, Bug, and Roadmap Issues, reconciles the complete Open-Issue count, and gives each included Issue and linked PR a clickable link.

## Workflow

1. Confirm the repository (`owner/repo`), target branch, type-label names, and explicit include/exclude Issue IDs.
2. Run `python {baseDir}/scripts/scan_gitcode_issues.py --help` when choosing options.
3. Generate the Markdown report. Verify `included + excluded = open_total`, then inspect all close-ready candidates.
4. If the user explicitly wants to close eligible Issues, generate a PowerShell or Bash script with `--emit-close-script`. Give it to the user for review and manual execution; **do not execute it automatically**.
5. Add `--add-resolved` only when the user wants the generated script to add `resolved` immediately before closing.

The generated close script must remain limited to RFC/Feature candidates that have a merged linked PR targeting the requested branch and no open linked PR. It re-reads current Issue and PR state immediately before each close, skips candidates whose state changed, and verifies the final closed state.

## Example

```powershell
python {baseDir}/scripts/scan_gitcode_issues.py Ascend/msinsight `
  --output msinsight-issues.md `
  --include 564,471,466,299,238 `
  --exclude 236 `
  --target-branch master `
  --emit-close-script close-ready.ps1 `
  --shell powershell `
  --add-resolved
```

## Output checks

- Every included Issue appears exactly once as a clickable Issue link.
- Linked PRs are clickable and show target branches where relevant.
- Explicit exclusions are listed without being classified or linked.
- The close script contains only the report's close-ready Issue IDs.
- Never expose authentication tokens or treat report generation as permission to mutate GitCode.