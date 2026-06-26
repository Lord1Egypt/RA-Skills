## Description: <br>
Build respectful multi-touch outreach sequences with channel mix, follow-up timing, objection handling, and logging templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to draft structured outreach cadences from an offer, target persona, channel plan, timeline, proof assets, and stated boundaries. It produces first-pass messaging, follow-up branches, a tracking table, and a testing plan for review before external use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can overwrite an existing JSON file if the selected output path already exists. <br>
Mitigation: Choose an explicit output path that will not overwrite important files before running the script. <br>
Risk: Generated outreach could contain inaccurate claims or violate consent, anti-spam, or legal requirements if sent without review. <br>
Mitigation: Review generated outreach for accuracy, consent, and applicable requirements before using it externally. <br>
Risk: The skill may be asked to fill missing proof, metrics, credentials, or legal certainty that were not provided. <br>
Mitigation: Keep assumptions explicit and mark uncertain fields for confirmation instead of fabricating evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/outreach-sequence-crafter) <br>
- [README](artifact/README.md) <br>
- [Example prompt](artifact/examples/example-prompt.md) <br>
- [Cadence presets](artifact/resources/cadence_presets.yaml) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON draft files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local Python helper to write an outreach_sequence.json draft to an explicit output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
