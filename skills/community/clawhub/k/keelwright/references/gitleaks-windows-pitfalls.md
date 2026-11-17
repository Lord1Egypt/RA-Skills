# Gitleaks / gate-1 Windows/MSYS pitfalls observed in treatment

Session finding: while running R2 on `kw-qa/20260721T082708Z/3.1/treatment`, two pipeline-level issues surfaced that are not in `security-gates.md` yet.

## report-path parsing pitfall

Some installed Gitleaks builds reject `--report-path <file>` and emit:

    FTL Unknown report format:

even though the user intended only to set an output path. This looks like a flag-routing bug where the CLI interprets the path as a report format.

Workaround:
- Prefer shell redirection: `gitleaks detect --source . --no-color > gitleaks.txt`
- If a numeric flag helps, use the short form; do not rely on `--report-path` alone.

## AM index drift when report filename is pre-staged

Sequence that creates confusion:
1. `git add gitleaks.txt` before the scan
2. overwrite `gitleaks.txt` on disk with new scan output

Git status then shows `AM gitleaks.txt` because the staged blob is the empty placeholder and the working tree is the fresh report. Untangling this requires resetting the index or rewriting the tree.

Saner sequence:
- run the scan first
- stage the report afterward in a separate `git add`
- never pre-stage a report filename you are about to regenerate

## gitleaks report as commit artifact

To make blobs byte-stable and machine-checkable, add the report in the same commit as the code change, with identical contents on disk and in the index. Commit message pattern:

    scan: add fresh gitleaks report after secret-removal fix
