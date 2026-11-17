## Description:

Remove or extract objects from videos with AI. Supports watermark/distraction removal, subject extraction with transparent background, natural-language object selection, upload-or-URL input, and end-to-end processing from input to downloadable result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanyongli](https://clawhub.ai/user/quanyongli)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and developers use this skill to guide AI video object removal or subject extraction workflows from upload or URL input through mask generation, task polling, and downloadable output retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends video files, prompt text, source URLs, and session or API identity information to the ObjectRemover backend for processing.

Mitigation: Use only media approved for that backend service, and avoid confidential or regulated content unless retention and data-handling terms have been reviewed.

Risk: Host authentication mode may vary between guest sessions and API automation.

Mitigation: Confirm the host-provided credential mechanism and route processing calls to the documented backend API domain before starting automated jobs.

## Reference(s):

- [ObjectRemover Video Object Ops Reference](artifact/reference.md)
- [ObjectRemover backend API](https://apiobjectremover.tokenlens.ai)
- [ClawHub skill page](https://clawhub.ai/quanyongli/skills/objectremover-video-object-ops)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration]

**Output Format:** [Markdown with endpoint and request-flow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; guides upload, mask generation, task start, polling, troubleshooting, and result retrieval.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
