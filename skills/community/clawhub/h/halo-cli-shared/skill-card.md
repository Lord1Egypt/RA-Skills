## Description: <br>
Use when a task broadly involves Halo CLI and the correct command area is not yet clear, or when you need shared rules for profiles, JSON output, help discovery, config paths, and destructive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruibaby](https://clawhub.ai/user/ruibaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to orient Halo CLI work, choose the right command area, and apply shared rules for authentication profiles, JSON output, help discovery, configuration paths, and destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or invoking the Halo CLI could trust an npm package source or local binary the user did not intend to use. <br>
Mitigation: Install the Halo CLI only from a trusted npm package source and verify the binary with halo --version and halo --help before using it. <br>
Risk: Authenticated profiles may have broad access to Halo content, operations, moderation, or backup actions. <br>
Mitigation: Use least-privileged Halo profiles and specify --profile when multiple profiles exist. <br>
Risk: Publish, delete, backup, moderation, or --force commands can make destructive or externally visible changes. <br>
Mitigation: Manually confirm these commands before execution, especially in non-interactive workflows that require --force. <br>


## Reference(s): <br>
- [Halo site](https://www.halo.run) <br>
- [ClawHub skill page](https://clawhub.ai/ruibaby/halo-cli-shared) <br>
- [Publisher profile](https://clawhub.ai/user/ruibaby) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend Halo CLI commands and profile/configuration paths for follow-up agent execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
