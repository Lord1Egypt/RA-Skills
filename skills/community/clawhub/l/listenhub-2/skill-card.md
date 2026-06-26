## Description: <br>
Turns topics, URLs, text, and image prompts into podcasts, explainer videos, voice narration, or generated images through ListenHub scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFANGO](https://clawhub.ai/user/0xFANGO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to ask an agent to create generated media from topics, articles, pasted text, YouTube links, or image prompts. The skill routes requests through provided shell scripts for podcasts, explainer videos, text-to-speech, speech, image generation, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can modify shell startup files and may prompt package-manager installation steps. <br>
Mitigation: Review setup prompts before accepting changes, install curl and jq yourself, and inspect shell rc files for LISTENHUB_API_KEY entries when uninstalling. <br>
Risk: User text, URLs, and image prompts are sent to external ListenHub or Marswave APIs for processing. <br>
Mitigation: Do not submit confidential text, private URLs, sensitive images, or data that your organization prohibits sending to third-party services. <br>
Risk: The skill depends on a local API key for authenticated requests. <br>
Mitigation: Use a revocable ListenHub API key, avoid exposing it in logs or shared terminals, and rotate or revoke it if access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xFANGO/listenhub-2) <br>
- [ListenHub API key settings](https://listenhub.ai/settings/api-keys) <br>
- [ListenHub podcast app](https://listenhub.ai/app/podcast) <br>
- [ListenHub explainer app](https://listenhub.ai/app/explainer) <br>
- [ListenHub text-to-speech app](https://listenhub.ai/app/text-to-speech) <br>
- [Labnana image API documentation](https://docs.marswave.ai/openapi-labnana.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations, JSON status responses, URLs, and local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LISTENHUB_API_KEY, curl, and jq. Generation can take several minutes; text-to-speech input is limited to 10,000 characters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
