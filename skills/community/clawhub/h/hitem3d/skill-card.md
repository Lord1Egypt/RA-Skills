## Description:

Generate production-grade 3D models from images with the Hitem3D API, including single-image, portrait, multi-view, printable, AR-ready, batch, balance, wait, and download workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihuihui-bj](https://clawhub.ai/user/lihuihui-bj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, 3D production teams, e-commerce visual teams, game or toy concept teams, 3D printing users, and AR content teams use this skill to turn images or folders of images into downloadable 3D assets with sensible defaults, cost awareness, and completed submit-wait-download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials or bearer tokens may be exposed through command output, terminal logs, or process monitoring.

Mitigation: Provide credentials through environment variables, avoid running authentication in logged terminals, use scoped short-lived tokens when available, and rotate Hitem3D credentials if exposure is suspected.

Risk: Input images are sent to the Hitem3D service for generation.

Mitigation: Use only images that are approved for upload to Hitem3D and avoid confidential, regulated, or rights-restricted content unless appropriate agreements and approvals are in place.

Risk: Generation jobs consume Hitem3D credits, especially batch, high-resolution, multi-format, or repeated-variant requests.

Mitigation: Confirm large or expensive jobs before execution, check balance when cost matters, and report estimated credits per task or batch.

Risk: The artifact notes that end-to-end live validation was blocked because real Hitem3D API credentials were unavailable.

Mitigation: Complete the live-validation checklist with valid AK/SK credentials before claiming fully production-proven reliability.

## Reference(s):

- [Hitem3D homepage](https://hitem3d.ai)
- [ClawHub skill page](https://clawhub.ai/lihuihui-bj/skills/hitem3d)
- [Hitem3D API Reference](artifact/references/api.md)
- [Hitem3D Product Guide](artifact/references/product-guide.md)
- [Hitem3D Live Validation Plan](artifact/references/live-validation.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text responses with shell command usage and downloaded 3D asset files such as GLB, OBJ, STL, FBX, or USDZ.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, final status, saved file paths, selected model, resolution, output format, preview URLs, balance information, and estimated credit cost.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
