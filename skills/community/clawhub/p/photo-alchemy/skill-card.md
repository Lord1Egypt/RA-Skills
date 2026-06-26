## Description: <br>
Transform any photo into surrealist AI art using Claude to write a story about the photo and Gemini to generate a reimagined version in one of 35+ visual styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hbmartin](https://clawhub.ai/user/hbmartin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use photo-alchemy to turn local photos or Apple Photos album selections into AI-generated surrealist artwork, manage visual styles and character mappings, and optionally automate output to a Photos album for Apple TV screensavers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private photos and face names may be sent to external AI services during generation. <br>
Mitigation: Use dedicated input albums, avoid sensitive Photos albums, and configure character mappings when real names should not be shared. <br>
Risk: API keys and run history may be stored locally or used by scheduled background runs. <br>
Mitigation: Use dedicated Anthropic and Gemini API keys, protect or remove ~/.imagemine.db when finished, and enable launchd scheduling only when ongoing API use is intended. <br>
Risk: Installation depends on an external package or installer. <br>
Mitigation: Install only when the external imagemine package and installer are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hbmartin/photo-alchemy) <br>
- [Project homepage](https://github.com/hbmartin/imagemine) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Images, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated image files and optional JSON output from the underlying CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Anthropic and Gemini API keys; Apple Photos and launchd automation features require macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
