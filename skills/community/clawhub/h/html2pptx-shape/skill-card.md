## Description:

Converts HTML slide decks into editable PPTX presentations with embedded local CSS, preserved styling and layout, and native PowerPoint shapes for text, images, and containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiustrator](https://clawhub.ai/user/iiustrator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation automation workflows use this skill to convert local HTML presentations into editable PowerPoint decks for later review, sharing, and manual refinement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted HTML can trigger unrestricted network requests during conversion.

Mitigation: Use trusted local inputs in a sandboxed or offline environment, make remote asset fetching explicit and opt-in, block private and localhost destinations, and apply timeouts and size limits.

Risk: Input HTML or CSS can reference local files outside the presentation folder.

Mitigation: Constrain stylesheet and asset paths to the input directory, reject absolute or traversal paths, and review files before broader deployment.

Risk: Unpinned dependencies can change conversion behavior or security posture over time.

Mitigation: Pin and review Python and Playwright dependencies before commercial use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PPTX file output with command-line status and file path information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 16:9 editable PowerPoint presentations from HTML inputs; fidelity depends on supported CSS, layout, image, and SVG features.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
