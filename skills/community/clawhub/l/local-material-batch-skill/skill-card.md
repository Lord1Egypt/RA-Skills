## Description:

Converts already-downloaded local video, audio, image, Markdown, and text-note materials into reusable text assets through an inbox, dry-run, processing, and manifest-output workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

Creators, researchers, operations teams, and content teams use this skill to intake local files they already possess, preview the batch with a dry run, and generate reusable text outputs for downstream content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the local batch script can unintentionally copy files outside the intended inbox.

Mitigation: Run dry-run first, keep the workflow in a dedicated directory, and avoid preserving symlinks in Inbox when processing untrusted archives or shared folders.

Risk: The security summary says generated CSV output from filenames can be risky.

Mitigation: Inspect generated CSV files before opening them in spreadsheet applications.

## Reference(s):

- [Output Contract](references/output-contract.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated Markdown, JSON, and CSV files from the batch script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow writes per-item text.md and text.json files plus batch-level manifest.json and summary.csv outputs; media and image extraction require configured OCR or ASR backends.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
