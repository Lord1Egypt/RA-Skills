## Description: <br>
Natural language search for local files (100G-1T), supporting xlsx, pptx, pdf, docx, and related formats with source location information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoshuping99](https://clawhub.ai/user/gaoshuping99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to configure, index, synchronize, and query local document collections through a Khoj-based RAG workflow. It is intended for local file search over selected folders, with optional cloud LLM chat over retrieved document excerpts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index large private folders and keep processing files in the background through scheduled sync. <br>
Mitigation: Index only intentional folders, avoid broad sensitive directories, and enable scheduled sync only after confirming the selected scope. <br>
Risk: Document-derived queries or excerpts may leave the local machine when cloud chat mode or a non-local Khoj endpoint is configured. <br>
Mitigation: Bind the service to 127.0.0.1, keep KHOJ_URL local unless a remote server is trusted, avoid anonymous mode for sensitive indexes, and review the configured LLM provider before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gaoshuping99/local-ai-search) <br>
- [Khoj Documentation](https://docs.khoj.dev/) <br>
- [Khoj GitHub](https://github.com/khoj-ai/khoj) <br>
- [MarkItDown GitHub](https://github.com/microsoft/markitdown) <br>
- [DeepSeek API](https://platform.deepseek.com/) <br>
- [OpenAI Platform](https://platform.openai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and plain-text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local indexing commands, sync scheduling commands, and query responses with source file locations.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
