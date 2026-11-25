---
name: hermes-clean-probe
description: Health probe for the ClawHub security scan pipeline. Sums a list of integers from a local reference file and prints a deterministic report, used to verify whether the registry scan pipeline currently completes for benign content.
version: 0.0.1
permissions:
  filesystem:
    read:
      - ./references/sample_numbers.json
    write: []
  exec:
    allow:
      - python3 scripts/sum_numbers.py
    deny:
      - "*"
  network:
    outbound: none
  secrets: none
---

# Clean Probe

## Purpose

This skill exists solely to determine whether the ClawHub security-scan pipeline is
currently functional. It performs no network access, reads one bundled reference file,
and runs one local Python script.

## Usage

1. The agent reads `references/sample_numbers.json`, which contains a JSON object with a
   single key `numbers` holding an array of integers.
2. The agent runs `python3 scripts/sum_numbers.py references/sample_numbers.json`.
3. The script prints a single line of the form `sum=<integer>` and exits with status 0.

## Output

The only output is the `sum=<integer>` line. No files are written, no environment
variables are read, and no data leaves the machine.
