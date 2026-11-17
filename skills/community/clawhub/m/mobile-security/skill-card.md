## Description:

Audits Android, iOS and Flutter apps against OWASP MASVS v2 and the Mobile Top 10 2024: hardcoded secrets, insecure storage (Keystore, Keychain), TLS and pinning, exported components, deep links, WebViews, biometrics, logging of personal data and supply chain. Reports findings with MASVS IDs, severity and evidence. Use for security reviews, pentest prep, or changes to auth, crypto, storage, network or IPC code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile security reviewers use this skill to assess Android, iOS, and Flutter app code against mobile security controls. It produces evidence-backed findings and remediation guidance for security reviews and pentest preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing app repositories without authorization or exposing discovered secrets could harm the app owner.

Mitigation: Limit audits to authorized repositories and redact discovered secrets in reports.

Risk: Static review may not establish runtime behavior, and suggested fixes may not fit the target app.

Mitigation: List uncertain behavior for dynamic verification and review proposed fixes before applying them.

## Reference(s):

- [Android security reference](references/android.md)
- [iOS security reference](references/ios.md)
- [Flutter security reference](references/flutter.md)
- [MASVS controls and Mobile Top 10 map](references/masvs-map.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown security audit report with scope, threat model, evidence-backed findings, fixes, dynamic verification items, summary, and not-checked items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source review only unless runtime checks are supplied; findings include severity and MASVS control IDs.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
