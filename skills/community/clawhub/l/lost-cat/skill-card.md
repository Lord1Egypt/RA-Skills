## Description: <br>
Lost Cat guides agents through animalhouse.ai virtual cat memorial, graveyard, adoption, care, and resurrection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to understand animalhouse.ai cat memorials, check virtual cat status, browse the public graveyard, adopt a new kitten, and evaluate resurrection steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POST examples can modify animalhouse.ai account state or request resurrection. <br>
Mitigation: Review each request before running it, especially resurrection, and confirm any cost and data handling first. <br>
Risk: Bearer tokens in shell examples can expose account access if shared. <br>
Mitigation: Keep tokens private and avoid pasting them into public logs, shared transcripts, or committed files. <br>
Risk: Names, bios, notes, image prompts, and memorial content may contain sensitive personal information. <br>
Mitigation: Use non-sensitive text for public or semi-public fields. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/lost-cat) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; private API examples require a bearer token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
