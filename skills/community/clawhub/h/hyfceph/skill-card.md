## Description:

HYFCeph runs cephalometric analysis through the HYFCeph portal by uploading one or two local lateral ceph images and returning supported metrics, annotated image artifacts, reports, or overlap traces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyuanfeng45](https://clawhub.ai/user/huyuanfeng45)

### License/Terms of Use:

MIT-0

## Use Case:

External users and clinicians use this skill to submit lateral cephalometric images to HYFCeph for measurement, clinical summary, report links, and optional image overlays or two-image overlap comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends cephalometric images and optional patient names to the HYFCeph service and report destinations.

Mitigation: Use only when the user is comfortable with that transfer, and review the service, retention, consent, and access-control model before using regulated patient data.

Risk: The service client can save a reusable API key on the local machine.

Mitigation: Use the skill on a private machine and clear the saved API key when access is no longer needed.

Risk: Shareable report links and generated artifacts may expose dental-imaging results beyond the local conversation.

Mitigation: Share report links and artifact paths only with intended recipients and avoid posting raw JSON or credentials in user-facing replies.

Risk: Custom portal URLs can redirect uploads and API-key validation to an unexpected service.

Mitigation: Avoid custom portal URLs unless you operate and trust the destination.

## Reference(s):

- [HYFCeph portal](https://hyfceph.52ortho.com/)
- [ClawHub skill page](https://clawhub.ai/huyuanfeng45/skills/hyfceph)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Analysis, Configuration instructions]

**Output Format:** [Markdown replies with concise Chinese clinical summaries, metric values, report links, and local image or JSON artifact paths when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local result JSON, annotated PNG/SVG, contour PNG/SVG, PDF reports, QR code images, and a reusable local API key state file.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
