## Description:

Work through a medical Explanation of Benefits, Medicare Summary Notice or itemized bill the user shares, using the KeepMD MCP for EOB Decoder tools to decode codes, explain insurance terms, check the arithmetic and recommend next steps. Use when the user pastes or photographs an EOB or medical bill, or asks what a code, column or amount on one means.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepmd-medical](https://clawhub.ai/user/keepmd-medical)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to understand codes and insurance terms on an Explanation of Benefits, Medicare Summary Notice, or itemized medical bill, check the arithmetic, and identify possible next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was marked partial because one reference could not be resolved, so the scan does not establish what that reference points to.

Mitigation: Review the unresolved reference before deployment.

Risk: An EOB or medical bill can contain personal identifiers that are not needed for this workflow.

Mitigation: Remove names, member IDs, claim numbers, dates of birth, and addresses before sharing the statement; the skill instructs users not to send these details.

## Reference(s):

- [KeepMD MCP for EOB Decoder documentation and privacy notice](https://keepmd.org/mcp-eob-decoder/)
- [KeepMD EOB Decoder MCP service](https://mcp.keepmd.org/eob)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains code descriptors and insurance terms, summarizes arithmetic checks, suggests next steps, and includes the tool-provided disclaimer.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
