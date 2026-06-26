## Description: <br>
Enigma lets an agent read, create, update, and delete Enigma data through the OOMOL Enigma connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Enigma through an OOMOL-connected account, including account lookup, business and list searches, GraphQL search workflows, list creation, suggestions, and guarded list deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Enigma account and may access account, billing, business, list, and search data. <br>
Mitigation: Use the skill only with trusted agents and maintain Enigma credentials and account access according to the organization's credential handling policy. <br>
Risk: Write actions can create Enigma lists or submit data correction and enrichment suggestions. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running any action tagged as write. <br>
Risk: The delete_list action can remove a user-managed Enigma list. <br>
Mitigation: Require explicit user approval for the target list before running any destructive action. <br>


## Reference(s): <br>
- [Enigma homepage](https://www.enigma.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-enigma) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions may return JSON responses from the oo CLI, including data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
