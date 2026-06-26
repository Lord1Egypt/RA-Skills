## Description: <br>
Full-featured YAML toolkit for validating, formatting, converting, merging, and querying YAML files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate, format, convert, query, patch, merge, lint, and minify YAML and JSON configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility can write transformed output to a file path supplied with --output. <br>
Mitigation: Use --output only with paths intended for creation or replacement, preferably a new file, and review diffs before using the result in production. <br>
Risk: The utility depends on PyYAML being available in the Python environment. <br>
Mitigation: Install PyYAML from a trusted Python environment if it is not already available. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-oriented output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled command-line utility writes transformed YAML or JSON to stdout by default and can write to a specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
