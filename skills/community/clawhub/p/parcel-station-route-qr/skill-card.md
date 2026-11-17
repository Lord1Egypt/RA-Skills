## Description:

Add shelf route guidance and QR code scanning to a parcel station chatbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and parcel-station operators use this skill to add shelf route guidance, QR scanning, and optional HTTPS support to a parcel station chatbot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated Notion sync script that can read local credentials and read or write Notion data.

Mitigation: Remove or clearly separate the Notion sync script unless it is intended, and do not run it until the Notion token and database targets are understood.

Risk: QR payloads may be sent into the chatbot workflow without an operator review step.

Mitigation: Add a confirmation step before submitting scanned QR content.

Risk: Generated TLS keys may be stored alongside source files.

Mitigation: Store generated certificate keys outside the source tree with restrictive file permissions.

Risk: Runtime dependencies may change if they are not pinned.

Mitigation: Pin npm dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeremycooper2077/skills/parcel-station-route-qr)
- [jsQR 1.4.0 CDN Source](https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js)
- [Bundled jsQR Reference](artifact/references/jsqr.min.js)
- [Bundled HTTPS Certificate Helper](artifact/references/gen-cert.js)
- [Bundled Notion Sync Script](artifact/references/notion-sync.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes route guidance logic, QR scanning implementation notes, HTTPS setup guidance, and UI theme guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
