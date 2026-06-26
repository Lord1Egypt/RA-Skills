## Description: <br>
Muse AI helps an agent guide users through conversational music creation, including original songs, lyrics, instrumentals, and background music generated through Muse API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a64307410](https://clawhub.ai/user/a64307410) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create songs, lyrics, pure instrumentals, and BGM from conversational prompts. The skill manages Muse authentication, gathers generation preferences, submits music-generation requests, and returns generated song links and metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to paste a reusable Muse token into chat and stores it locally at ~/.muse/token. <br>
Mitigation: Install only when the user trusts Muse, avoid pasting a token unless signing in is intended, and delete ~/.muse/token when local access should no longer be retained. <br>
Risk: Prompts, lyrics, account status, a persistent device ID, and generation requests are sent to Muse's API. <br>
Mitigation: Review the data being submitted before generation and avoid sending sensitive or confidential content. <br>
Risk: Using install.sh with an arbitrary --path can lead uninstall or upgrade operations to recursively delete that target directory. <br>
Mitigation: Use only verified installation paths and inspect custom --path values before install, upgrade, or uninstall. <br>


## Reference(s): <br>
- [Muse registration page](https://skills.muse.top/) <br>
- [Muse API endpoint](https://skill-api.muse.top) <br>
- [Style catalog](references/style-catalog.md) <br>
- [Registration guide](assets/register-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/a64307410/muse-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown conversation responses with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated song metadata, audio URLs, cover URLs, credit status, progress messages, and authentication guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
