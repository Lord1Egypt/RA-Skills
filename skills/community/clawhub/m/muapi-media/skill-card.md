## Description: <br>
Generate AI images, videos, music, and audio from the terminal via muapi.ai; supports 100+ models including Flux, Midjourney v7, Kling 3.0, Veo3, and Suno V5. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anil-matcha](https://clawhub.ai/user/Anil-matcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to call muapi.ai from shell scripts for text-to-image, text-to-video, image-to-video, music and audio generation, and file uploads. It is suited to terminal-based media generation workflows that can send prompts and selected media files to a third-party API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media files are sent to muapi.ai, including local files when upload options are used. <br>
Mitigation: Use only non-confidential inputs and confirm that the provider terms permit the intended data sharing before running generation or upload commands. <br>
Risk: Some scripts can save MUAPI_KEY to a local .env file and all scripts load .env from the current directory. <br>
Mitigation: Prefer setting MUAPI_KEY in the shell environment, avoid the --add-key helper, and run the scripts only from directories where the .env file is trusted. <br>
Risk: The security verdict is suspicious due to credential handling and third-party content transfer. <br>
Mitigation: Review and scan the scripts before deployment, then restrict use to environments where outbound API calls and file uploads are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anil-matcha/muapi-media) <br>
- [muapi.ai API endpoint](https://api.muapi.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Terminal output, JSON API responses, generated media URLs, and optional downloaded media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MUAPI_KEY plus curl, jq, and python3; async mode returns request identifiers for later polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
