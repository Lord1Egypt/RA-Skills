## Description:

Organizes local knowledge bases by guiding file merging, renaming, deduplication, and index updates for Markdown, scripts, and configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheney87](https://clawhub.ai/user/cheney87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to clean up local documentation repositories by finding duplicate or related content, consolidating files, standardizing names, and refreshing README indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides local file renames, merges, and removals that can change or delete knowledge-base content.

Mitigation: Run dry-run or review steps first, make backups, and explicitly confirm the exact files before allowing rename or deletion actions.

Risk: Chinese-language instructions may be misunderstood by users who cannot reliably read the source guidance.

Mitigation: Install and use the skill only when reviewers are comfortable validating the Chinese-language workflow and its proposed file operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and file organization guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested local file renames, merges, deletions, README index updates, and optional dry-run script usage.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
