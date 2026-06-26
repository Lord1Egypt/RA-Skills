## Description: <br>
Reverse-engineers a viral LinkedIn post URL to identify its hook formula, structure, why it worked, cautions, and a reusable blank template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and writing assistants use this skill to study a viral LinkedIn post and turn its hook and body pattern into a reusable writing template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use HarvestAPI to fetch LinkedIn post content, which can involve a third-party fetch for the submitted post URL. <br>
Mitigation: Paste the post text directly instead of a URL when avoiding third-party retrieval is required. <br>
Risk: Server metadata includes unrelated crypto and purchase capability tags that are not supported by behavior shown in the skill files. <br>
Mitigation: Treat those tags as a metadata inconsistency and review package metadata before deployment. <br>


## Reference(s): <br>
- [Hook Formula Classification Rules](references/classification-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sergebulaev/linkedin-hook-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with confidence scores, structural sections, cautions, and a reusable template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include top formula matches, post-structure labels, psychological rationale, and slot markers for adapting the pattern.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
