## Description: <br>
Generates and edits images, videos, upscaled media, and talking-avatar outputs through a Kandinsky API service using text, image, and audio inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikolay-gerasimenko](https://clawhub.ai/user/nikolay-gerasimenko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative operators use this skill to ask an agent to generate images, edit images, upscale media, create short videos from text or images, and produce talking-avatar video through a configured Kandinsky API endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented default API endpoint uses plain HTTP and can receive an API key plus user prompts, images, audio, and generated media. <br>
Mitigation: Use an HTTPS endpoint or a trusted private/VPN endpoint, and avoid sending sensitive prompts, media, or API keys through the default plain-HTTP public IP. <br>
Risk: The skill depends on an external Kandinsky API operator for request handling and media retention practices. <br>
Mitigation: Install and use the skill only when the operator is trusted, and confirm endpoint ownership before submitting valuable or sensitive inputs. <br>


## Reference(s): <br>
- [Kandinsky API Swagger](http://87.242.117.37:5051/docs) <br>
- [Kandinsky API cheatsheet](references/api-cheatsheet.md) <br>
- [Kandinsky prompting guide](references/prompting.md) <br>
- [ClawHub skill page](https://clawhub.ai/nikolay-gerasimenko/kandinsky) <br>
- [Publisher profile](https://clawhub.ai/user/nikolay-gerasimenko) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples for producing image, video, audio-avatar, or status/result files from the Kandinsky API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KANDINSKY_API_KEY and optionally KANDINSKY_API_BASE; generated media is saved as files by the bundled Python client or API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
