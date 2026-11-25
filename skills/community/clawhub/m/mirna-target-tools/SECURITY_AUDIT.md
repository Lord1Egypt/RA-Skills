# Security Audit — mirna-target-tools 3.2.2

Date: 2026-11-25
Scope: all Python/shell/R entry points in `scripts/`, with focus on command
execution, network access, archive handling, temporary files, path handling and
data export.

## Verdict

No critical or high-severity issues remain in the reviewed code. The code-level
issues found during the audit were fixed and re-tested. Residual risks are
supply-chain/reference-integrity and deployment-environment risks, listed below.

## Fixed during this audit

| # | Severity | Finding | Fix |
|---|----------|---------|-----|
| 1 | High | R package checks interpolated strings into `Rscript -e` | Constant R expression + package names passed as `argv`; `--vanilla` everywhere |
| 2 | High | `--prefix` could contain `../` or separators and write outside `--outdir` | `safe_name()` / `safe_prefix()` reject separators, `..`, NUL, tab, newline |
| 3 | High | Unbounded HTTP reads (memory exhaustion / oversized reference files) | HTTPS-only, `Content-Length` + streaming byte cap, atomic replace, `.part` cleanup, FASTA sanity check |
| 4 | High | Installer could build third-party source and originally used `sudo` | No sudo, no source-build fallback; real miRanda 3.3a is installed from bioconda and version-checked |
| 5 | Medium | Silent fallback from real miRanda to seed/RNAhybrid | Real miRanda 3.3a is required by `--method auto`; explicit `seed`/`rnahybrid` opt-outs only |
| 6 | Medium | miRanda invoked with invalid `-score` flag; `>>` summary duplicated hits | `-sc`; summary lines skipped; parser tested against miRanda 3.3a |
| 7 | Medium | `merge_targets.py` crashed on NaN/empty gene fields | NaN-safe cell access + TSV control-character cleanup |
| 8 | Medium | Spreadsheet formula injection in annotation exports | Cells starting with `= + - @` are prefixed with `'` (`--no-formula-guard` opts out) |
| 9 | Low | `fetch_mirnas.py` imported `urllib.parse` only under `__main__` | Import moved to module scope |
| 10 | Low | Temporary directories could leak on failure | `finally` cleanup in all `mkdtemp` users |
| 11 | Low | Cache/downloaded FASTA was not sanity-checked | Require plausible size and leading `>`; invalid cache triggers re-download |
| 12 | Low | SIF node labels could contain whitespace/control characters | Labels sanitized; empty labels dropped |
| 13 | Low | `check_env.py` reported miRanda as optional and did not validate version | miRanda 3.3a is required and version-checked |
| 14 | Low | Installer/README did not enforce a real binary | Pinned conda installer (`miranda=3.3a`) and `--check` verification |

## Residual risks

### Medium — reference integrity and supply chain

- Ensembl cDNA/GTF and miRBase files are downloaded over HTTPS but their
  published checksums are not verified. A compromised mirror or TLS interception
  could substitute reference data.
- `conda`, CRAN and PyPI dependencies are not pinned to content hashes.
- Recommendation: use a conda lockfile / private mirror, and verify Ensembl
  `CHECKSUMS` or miRBase MD5 in high-assurance environments.

### Low — same-user cache tampering

- `~/.cache/mirna-target-tools` is user-controlled; a process running as the
  same user could influence cached files. Mitigation: keep the cache directory
  `0700` and avoid following symlinks when writing (future hardening).

### Low — decompression memory limits

- FASTA input is capped (`MIRNA_MAX_FASTA_BASES`, default 3 Gb), but a
  maliciously huge GTF can still consume memory during annotation parsing.
  Only use trusted GTF files, or add a GTF line/base cap if untrusted input is
  expected.

### Low — external binary trust

- miRanda, RNAhybrid, TargetScan and Rscript are resolved from `PATH` or common
  conda prefixes. Their integrity depends on the local installation; conda
  packages are hash-verified by conda but not signature-checked by this skill.

### Informational — data egress

- `annotate_targets.py` sends the supplied gene list to the g:Profiler REST API
  over HTTPS. Do not submit sensitive gene lists to a third-party service.

## Verified controls

- No `shell=True`, `os.system`, `eval`, `pickle` or disabled TLS verification.
- All external programs use argv lists; the installer has no source-build path.
- Downloads are HTTPS-only, capped and atomically written.
- `--prefix` traversal guards tested for stage 1, refinement, annotation and
  conservation.
- Real miRanda 3.3a + real RNAhybrid end-to-end test passed; missing-miRanda
  behavior fails closed with an installation hint.
- 18 synthetic-data assertions plus real-binary refinement tests passed.

## Reproduction

```bash
python3 scripts/check_env.py
bash scripts/install_miranda_conda.sh --check
python3 -m py_compile scripts/*.py
bash -n scripts/*.sh
```
