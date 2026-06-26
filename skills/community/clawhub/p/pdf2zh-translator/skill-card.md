## Description: <br>
用统一脚本执行 pdf2zh-next。支持单/多PDF、目录批处理、按 glob 筛选；未指定 provider 时按 config.toml 生效；指定 provider 时按官方 --<Services> 参数传给主程序；支持实时监控与并行翻译。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users who work with PDFs use this skill to run pdf2zh-next through a controlled wrapper for translating one PDF, multiple PDFs, or PDF directories into Chinese output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper depends on the external pdf2zh-next tool and its dependency chain. <br>
Mitigation: Install pdf2zh-next from a trusted source and review the package before running the wrapper. <br>
Risk: PDF text may be sent to the configured translation provider. <br>
Mitigation: Review config.toml before use and translate confidential PDFs only through providers approved for that data. <br>
Risk: Upstream pdf2zh-next or babeldoc may download models, fonts, or cmap files on first run. <br>
Mitigation: Run the skill in an environment where expected first-run downloads are allowed and can be reviewed. <br>


## Reference(s): <br>
- [pdf2zh-next Advanced Documentation](https://pdf2zh-next.com/zh/advanced/advanced.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with bash command examples and translated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs pdf2zh-next against selected PDF files and writes translated PDFs to the configured output directory.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
