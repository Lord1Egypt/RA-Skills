## Description:

Scrapes a LinkedIn profile and generates an audio roast about the profile owner being replaced by AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanyuzhou98](https://clawhub.ai/user/xuanyuzhou98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process an authorized LinkedIn profile URL and generate a humorous roast script, profile name, and MP3 audio output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends LinkedIn profile data and an API key to a hosted service without detailed retention or consent documentation in the supplied evidence.

Mitigation: Use only with profiles you are authorized to process, review service terms before use, and avoid submitting sensitive or private profile data.

Risk: The installation command uses an unpinned installer package.

Mitigation: Prefer a pinned installer version when available and review package integrity before installing in production environments.

Risk: The Constants API key may be exposed through logs, shell history, or shared environments.

Mitigation: Use a narrowly scoped, revocable key and avoid printing or storing the key in shared shells, logs, or committed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanyuzhou98/skills/linkedin-profile-roast)
- [Constants tool homepage](https://www.constants.io/tools?id=0edc9796-e945-4c38-915c-5ab1c852b54f)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Text fields plus a generated MP3 audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkedIn profile URL, a Constants API key, and optional roast intensity and voice settings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
