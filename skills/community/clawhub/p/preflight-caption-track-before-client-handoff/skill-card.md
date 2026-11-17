## Description:

Preflights frozen WebVTT, SRT, and TTML/IMSC caption tracks against a selected delivery profile before client handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, localization leads, and delivery teams use this skill to check frozen caption files against a named destination profile, record measured findings, and prepare a handoff report that separates file-level checks from human media review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party PowMCP service that may process submitted caption files or public URLs remotely.

Mitigation: Confirm trust in PowMCP before installation and do not submit private, credentialed, or sensitive URLs unless sharing that caption content with the service is intended.

Risk: A clean preflight result is limited to selected source-file checks and the named profile.

Mitigation: Complete separate human review for language accuracy, media synchronization, destination acceptance, positioning, styling, and any requirements outside the selected file checks.

Risk: Unsupported formats, failed fetches, size bounds, or reported truncation can leave caption content unassessed.

Mitigation: Record unassessed content as not checked, provide a supported attached file or accessible public HTTP(S) URL, and rerun the same check before treating the track as clean.

## Reference(s):

- [Caption File Check reference](references/caption-file-check.md)
- [Caption File Check](https://powmcp.com/apps/caption-file-check/)
- [Netflix Timed Text Style Guide, General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)
- [Netflix Timed Text Style Guide, Subtitle Timing Guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)
- [Common subtitle format errors](https://subtitletoolkit.tools/guides/common-subtitle-format-errors-and-fixes/)
- [WebVTT validator documentation](https://subtitletoolkit.tools/tools/webvtt-validator/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes measured findings, verb-first fixes, rerun status, and not-checked items; does not assess platform acceptance, language quality, media synchronization, positioning, or styling.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version: 2026.09.10+caption-file-check@0.3.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
