## Description: <br>
LocalDataAI helps agents process private documents with local AI models for parsing, question answering, summarization, extraction, and search across formats such as WPS, PDF, Excel, images, and WeChat cache files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise teams can use this skill to build local document-AI workflows for private file parsing, retrieval, question answering, summarization, and structured information extraction. It is aimed at environments where documents should remain within local infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Offline, sandbox, and compliance claims may not be fully enforced by the artifacts. <br>
Mitigation: Treat the release as a local prototype until protections are independently reviewed, and run it only in a controlled environment for regulated or confidential workloads. <br>
Risk: Downloaded models and Python dependencies may introduce supply-chain, licensing, or operational risk. <br>
Mitigation: Manually vet, approve, and pin model and dependency sources before installation or deployment. <br>
Risk: Audit, checkpoint, and temporary-file persistence may expose file paths or document metadata. <br>
Mitigation: Review persistence locations, retention, and logging settings before processing sensitive files, and disable or constrain them where needed. <br>


## Reference(s): <br>
- [LocalDataAI ClawHub page](https://clawhub.ai/kaiyuelv/local-data-ai) <br>
- [Qwen2.5-3B-Instruct-GGUF model artifact](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf) <br>
- [BGE-M3 embedding model artifact](https://huggingface.co/BAAI/bge-m3/resolve/main/model.safetensors) <br>
- [PaddleOCR v4 recognition model archive](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local document-processing guidance and code-oriented outputs; downstream answers depend on local model, parser, and runtime configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
