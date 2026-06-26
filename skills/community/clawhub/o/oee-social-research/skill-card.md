## Description: <br>
Conducts tiered social media research on X/Twitter and web sources, then compiles public discussion into structured briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OdinBot33](https://clawhub.ai/user/OdinBot33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to gather public discussion about a topic from X/Twitter and web search sources, then produce a concise social research briefing with sentiment, narratives, and notable posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and briefings may be sent to third-party social and search services. <br>
Mitigation: Use the skill only for topics that are appropriate to share with public search and social services. <br>
Risk: Research terms, usage logs, cached results, and compiled briefings may remain on disk under the skill directory. <br>
Mitigation: Review and clear the skill's local cache, log, and briefing directories when retention is not desired. <br>
Risk: The reviewed package has an import path issue that could load code outside the reviewed artifact files. <br>
Mitigation: Verify the installed package layout before use so the skill imports the bundled fxtwitter.py module. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/OdinBot33/oee-social-research) <br>
- [Publisher profile](https://clawhub.ai/user/OdinBot33) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Structured briefing printed to stdout and saved as a text briefing file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cache retrieved results and write usage logs and briefing files under the skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
