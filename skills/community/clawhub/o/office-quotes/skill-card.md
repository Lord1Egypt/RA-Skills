## Description: <br>
Generate random quotes from The Office (US). Provides access to 326 offline quotes plus online mode with SVG cards, character avatars, and full episode metadata via the akashrajpurohit API. Use for fun, icebreakers, or any task requiring The Office quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and end users use this skill to add random The Office (US) quotes to chats, icebreakers, or generated content. API mode can also produce quote cards, character avatars, and episode metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode contacts a third-party quote service and may depend on external service availability. <br>
Mitigation: Use offline/local mode for routine use and enable API mode only when third-party network access is acceptable. <br>
Risk: Image-rendering helpers create temporary render files and process SVG content. <br>
Mitigation: Run the skill in a constrained workspace, avoid untrusted URLs, and review the SVG-rendering path before automated workflows. <br>
Risk: The npm package is third-party owned. <br>
Mitigation: Install only after trusting the npm publisher, and pin or review the package for production deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gumadeiras/office-quotes) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gumadeiras) <br>
- [npm package @gumadeiras/office-quotes](https://www.npmjs.com/package/@gumadeiras/office-quotes) <br>
- [Office Quotes API](https://officeapi.akashrajpurohit.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration] <br>
**Output Format:** [Plain text, JSON, SVG, PNG, JPG, or WebP output from the office-quotes CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline/local mode is available by default; API mode may contact a third-party service and create temporary render files.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
