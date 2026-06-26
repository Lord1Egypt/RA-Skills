## Description: <br>
Inkwell bootstraps a three-layer OpenClaw memory system with PARA knowledge files, QMD search setup, daily consolidation, transcript verification, and sign-off workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidkim01](https://clawhub.ai/user/davidkim01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use Inkwell to initialize a persistent local memory workspace, organize knowledge with PARA, configure QMD search, and add optional daily consolidation, transcript verification, and sign-off routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory, transcript storage, and session indexing can retain sensitive conversations or operational details. <br>
Mitigation: Decide what data may be captured before enabling automation, avoid storing secrets, keep transcripts local and gitignored, and periodically delete old transcript and memory files. <br>
Risk: Daily consolidation can promote incorrect or overbroad session details into long-term memory. <br>
Mitigation: Review the cron prompt and memory updates, restrict consolidation scope where possible, and correct or remove inaccurate entries during routine maintenance. <br>
Risk: The QMD setup guide includes a curl-to-bash installer path for Bun. <br>
Mitigation: Inspect installer commands before use or replace them with a verified package manager or organization-approved installation method. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidkim01/inkwell) <br>
- [QMD Setup Guide](references/qmd-setup.md) <br>
- [Daily Consolidation](references/consolidation.md) <br>
- [Transcript Verification System](references/transcripts.md) <br>
- [Sign-Off Routine](references/sign-off.md) <br>
- [Bun Installer](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or guides creation of local memory files, PARA folders, QMD configuration, cron setup, transcript handling, and sign-off routines.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
