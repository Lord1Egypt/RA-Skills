## Description:

Security audit for external resources (GitHub repos, downloaded skills, files). Detects malicious code, suspicious executables, and content mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ithacajason](https://clawhub.ai/user/ithacajason)

### License/Terms of Use:

MIT License

## Use Case:

Developers and agents use this skill to run a lightweight static security review of external repositories, downloaded skills, files, or scripts before execution. It helps surface suspicious file types, obfuscated content, README/content mismatches, and safe/warning/critical audit guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can incorrectly label risky packages as safe.

Mitigation: Treat results as lightweight triage, review suspicious code manually, and do not execute downloaded code solely because the scan is clean.

Risk: The audit may inspect local directory contents.

Mitigation: Run it only on directories intended for review and disclosure to the scanner.

Risk: Using --output carelessly could overwrite an important file.

Mitigation: Choose a dedicated report path and check before writing audit output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ithacajason/skills/jasonlai-security-audit)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain-text terminal report with optional saved report file and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize total files scanned, source files, high-risk files, suspicious patterns, README mismatches, and a safe, warning, or critical recommendation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
