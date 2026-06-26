## Description: <br>
高光集锦 helps agents use Sparki to turn sports, event, speech, or recap videos into tighter highlight reels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and video operators use this skill to guide an agent through Sparki setup, video upload, prompt-driven editing, and highlight-reel creation for matches, events, talks, and recaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos are uploaded to Sparki for cloud processing. <br>
Mitigation: Install and use the skill only when Sparki is trusted to process the chosen videos, and avoid uploading material that should not leave the local environment. <br>
Risk: API keys and local project history may be stored under the OpenClaw configuration directory. <br>
Mitigation: Prefer environment variables for SPARKI_API_KEY on shared systems, and protect or clear OpenClaw configuration files on machines that are shared or backed up. <br>
Risk: Base URL overrides can redirect API requests and uploaded video data away from the default Sparki endpoint. <br>
Mitigation: Use the default Sparki API endpoint unless the alternate endpoint is controlled and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/highlight-reels-zh) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPARKI_API_KEY and uv; commands may upload selected video files to Sparki and download generated results.] <br>

## Skill Version(s): <br>
1.0.12 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
