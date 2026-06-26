## Description: <br>
NotebookLM RAG Line syncs NotebookLM answers into a local SQLite vector RAG store and serves LINE chatbot responses with follow-up question suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claws-peak](https://clawhub.ai/user/claws-peak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to populate a local RAG knowledge base from NotebookLM and connect it to a LINE chatbot for teaching assistant, support, or personal knowledge workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can operate inside a logged-in NotebookLM session. <br>
Mitigation: Use a dedicated Chrome profile with only the needed notebook access and review each configured notebook ID before running. <br>
Risk: The script can install browser automation dependencies at runtime. <br>
Mitigation: Preinstall, pin, and review dependencies in the deployment environment instead of relying on runtime installation. <br>
Risk: Retrieved NotebookLM answers are written to local SQLite and JSON files. <br>
Mitigation: Store only approved content and protect the local database and output files according to the sensitivity of the source material. <br>
Risk: Scheduled execution may repeatedly update the local knowledge base without direct supervision. <br>
Mitigation: Enable scheduled tasks only when recurring background updates are intended and monitor logs and output files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claws-peak/notebooklm-rag-line) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples; runtime components produce JSON files and HTTP JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local configuration for Chrome profile, NotebookLM notebook ID, Ollama models, SQLite paths, and the RAG server port.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
