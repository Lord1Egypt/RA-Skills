## Description:

Play music on YouTube through a visible browser session controlled with playwright-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whodidthese](https://clawhub.ai/user/whodidthese)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to search YouTube for specific songs, artist mixes, playlists, or mood-based music and control playback in a visible browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent browser data may retain YouTube login cookies, local storage, IndexedDB, cache, and related session data.

Mitigation: Use the skill only when persistent YouTube browser state is acceptable, and clear or revoke stored browser/profile data when the session no longer needs it.

Risk: macOS permission prompts for screen recording, automation, or accessibility can grant broad local capabilities.

Mitigation: Grant only permissions you understand, verify that the requesting executable is expected, and revoke permissions when finished.

Risk: Sensitive operations such as delete-data, state-save, screenshots, close-all, and kill-all can remove session data, save authentication material, capture page contents, or interrupt browser sessions.

Mitigation: Confirm intent before using these operations, avoid capturing or saving sensitive page contents, and prefer actions scoped to the named music_player session.

## Reference(s):

- [Play Music from YouTube skill page](https://clawhub.ai/whodidthese/skills/my-play-music-from-yt)
- [Playwright CLI reference](references/playwright-ref.md)
- [YouTube result identification](references/youtube-guide.md)
- [YouTube](https://www.youtube.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Concise natural-language responses with inline playwright-cli shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a named visible browser session and persistent browser profile when opening YouTube.]

## Skill Version(s):

0.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
