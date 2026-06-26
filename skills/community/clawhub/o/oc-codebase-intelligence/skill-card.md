## Description: <br>
Intelligent codebase analysis and understanding with caching for exploring project structure, identifying modules, analyzing dependencies, and answering codebase questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to index a codebase, inspect project structure, trace dependencies and symbols, answer codebase questions, and generate architecture diagrams during onboarding, refactoring, and code review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loading an existing .codebase-intelligence/codebase_index.pkl cache can execute code through Python pickle. <br>
Mitigation: Before running the skill in a repository, inspect or delete any existing .codebase-intelligence/codebase_index.pkl file unless the repository and cache are trusted. <br>
Risk: The skill persists code previews and indexes in the analyzed project. <br>
Mitigation: Add .codebase-intelligence/ to .gitignore and remove cached indexes when working with sensitive or shareable repositories. <br>
Risk: Optional parser-loading behavior can execute local code. <br>
Mitigation: Review the skill before installation and run it only in trusted or isolated workspaces when analyzing untrusted repositories. <br>
Risk: Question-answering output may be inaccurate in this version. <br>
Mitigation: Treat answers as navigation guidance and verify conclusions against the source code before making changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michealxie001/oc-codebase-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON exports, Mermaid or DOT diagrams, and command-line answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write .codebase-intelligence cache files and optional exported index files in the analyzed project.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
