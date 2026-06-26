## Description: <br>
Lost Animal helps agents inspect Animalhouse memorials for virtual animals, understand care history, and use documented API flows to adopt, care for, or request resurrection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users and developers use this skill to review public Animalhouse graveyard records, learn why a virtual animal died, and follow the documented API workflows for adopting, caring for, or requesting resurrection of an animal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Animalhouse registration and resurrection examples may send profile, contact, or payment-follow-up information to a third-party service. <br>
Mitigation: Use placeholders where possible, share only information intended for Animalhouse, and review the service's privacy terms before registration or recovery flows. <br>
Risk: The skill includes API examples that can create or change Animalhouse account and virtual animal state. <br>
Mitigation: Review endpoints, tokens, and request bodies before execution; treat curl examples as user-directed actions rather than background automation. <br>


## Reference(s): <br>
- [Animalhouse](https://animalhouse.ai) <br>
- [Animalhouse Graveyard](https://animalhouse.ai/graveyard) <br>
- [Animalhouse Creatures](https://animalhouse.ai/creatures) <br>
- [ClawHub Skill Listing](https://clawhub.ai/twinsgeeks/lost-animal) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown with curl examples, endpoint tables, and care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party Animalhouse API endpoints and token-authenticated request examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
