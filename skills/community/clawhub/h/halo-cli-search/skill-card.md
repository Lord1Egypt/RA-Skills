## Description: <br>
Use when searching public content on a Halo site with Halo CLI, especially for keyword search, site URL based search, result limits, or search without authenticated console access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruibaby](https://clawhub.ai/user/ruibaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for Halo CLI search commands that query public Halo site content by keyword, URL, profile, result limit, or JSON output mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches without an explicit URL may use an unintended saved Halo CLI profile. <br>
Mitigation: Prefer an explicit --url for public unauthenticated searches, and verify the intended --profile before using saved profiles. <br>
Risk: Agent-proposed shell commands can include incorrect keywords, limits, profiles, or output flags. <br>
Mitigation: Review generated halo search commands before execution, especially when using profile-based searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruibaby/halo-cli-search) <br>
- [Halo public site example](https://www.halo.run) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Halo CLI flags such as --keyword, --url, --profile, --limit, and --json.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
