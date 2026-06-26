## Description: <br>
Moses Stamp embeds visible governance stamps in qualifying documents, including mode, posture, session ID, action number, and an integrity hash. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to append document-level provenance stamps to reports, specs, drafted emails, code deliverables, and other artifacts intended for use outside a conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stamped documents can expose provenance metadata such as session IDs, governance mode, posture, action numbers, and hashes. <br>
Mitigation: Confirm the metadata is acceptable for the intended audience before sharing, and disable or remove stamps when confidentiality or exact document contents matter. <br>
Risk: The append workflow modifies target documents and keeps a local stamp log. <br>
Mitigation: Run it on version-controlled files or copies, review diffs before distribution, and account for the local governance log in retention policies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunrisesillneversee/moses-stamp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown or plain-text governance stamp blocks with command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can append stamps to documents and records stamp events in local governance state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
