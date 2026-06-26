## Description: <br>
Recommend music based on your current mood, activity, or conversation context. Returns a curated track list you can search on Spotify, YouTube, or Apple Music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to turn conversation context, mood, activity, or time of day into a short curated music recommendation list. The recommendations are intended to be searched manually on Spotify, YouTube, or Apple Music and do not require platform credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague activation language could cause the skill to be used when the user did not intend to request music recommendations. <br>
Mitigation: Invoke the skill explicitly for music recommendations based on mood, activity, or conversation context. <br>
Risk: Users may expect the skill to remember preferences or create platform playlists. <br>
Mitigation: Treat outputs as curated track lists to search manually, and do not expect preference storage or generated playlist links unless separately documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/mood-music) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Publisher GitHub profile](https://github.com/TheShadowRose) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown-style curated track lists with detected mood labels and artist-track pairs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API credentials required; platform names indicate where users can search for tracks, not generated playlist links.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
