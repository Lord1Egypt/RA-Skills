## Description: <br>
Prompt Optimizer rewrites vague user requests into clearer AI instructions across common task types with CLI, JSON, batch-file, cache, and configuration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntaffffff](https://clawhub.ai/user/ntaffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and prompt authors use this skill to turn terse or ambiguous task requests into more explicit prompts before sending them to another AI system. It supports single-prompt use, JSON output, line-based batch processing, local caching, and optional configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optimized prompts may change user intent or add constraints that are unsuitable for sensitive or high-impact tasks. <br>
Mitigation: Review generated prompts before sending them to another model, especially for sensitive or high-impact work. <br>
Risk: Custom configuration files can change task patterns, output preferences, and optimization behavior. <br>
Mitigation: Use only trusted configuration files and review configuration changes before enabling them. <br>
Risk: Batch and output-file modes can write generated prompts to local files when explicitly requested. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntaffffff/prompt-optimizer-dxx) <br>
- [Publisher profile](https://clawhub.ai/user/ntaffffff) <br>
- [Artifact documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Plain text or JSON; optimized prompts may request Markdown, code blocks, tables, lists, or other downstream formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single prompts, line-delimited batch input, optional output files, LRU caching, and optional YAML configuration.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata, config_data.py __version__, SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
