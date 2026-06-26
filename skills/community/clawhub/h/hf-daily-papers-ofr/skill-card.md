## Description: <br>
Filters daily Hugging Face and arXiv CS.CV papers into OFR-focused research categories and generates Markdown or Telegram digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscffaa](https://clawhub.ai/user/wscffaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers and developers tracking old-film restoration and related computer-vision work use this skill to generate a daily digest grouped by restoration, video, efficiency, backbone, frequency, and generative-prior topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram delivery can send the digest to the wrong chat or channel if the target is misconfigured. <br>
Mitigation: Confirm the target chat or channel and test privately before enabling scheduled sending. <br>
Risk: Paper-fetching traffic may be routed through the configured proxy. <br>
Mitigation: Review the optional proxy setting and use only a proxy the user controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wscffaa/hf-daily-papers-ofr) <br>
- [Hugging Face Daily Papers](https://huggingface.co/papers) <br>
- [arXiv API](https://arxiv.org/help/api/index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest files and optional Telegram-ready plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated recommendation files under recommendations/ and can send a Telegram digest when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
