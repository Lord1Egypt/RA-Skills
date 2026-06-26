## Description: <br>
AI security toolkit for deepfake detection, prompt injection scanning, malware and phishing URL scanning, and AI text detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Canvinus](https://clawhub.ai/user/Canvinus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and external users use this skill to run user-invoked checks on media, prompts, URLs, and text for likely AI manipulation, prompt injection, phishing, malware, or AI-generated writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, media, and URLs may be sent to third-party analysis providers. <br>
Mitigation: Scan only content approved for third-party processing and review each provider's terms before use. <br>
Risk: Secrets, regulated content, private media, tokenized links, or internal incident-response URLs could be exposed if submitted for scanning. <br>
Mitigation: Do not scan sensitive material unless provider processing and possible retention are acceptable. <br>
Risk: Broadly configured API credentials increase exposure across modules that are not being used. <br>
Mitigation: Set only the API keys needed for the specific checks being run. <br>


## Reference(s): <br>
- [Mind Security ClawHub Page](https://clawhub.ai/Canvinus/mind-security) <br>
- [Mind Security Homepage](https://github.com/mind-sec/mind-security) <br>
- [AI Text Detection Reference](references/ai-text-detection.md) <br>
- [Deepfake Detection Reference](references/deepfake-detection.md) <br>
- [URL Threat Scanning Reference](references/malware-scanning.md) <br>
- [Prompt Injection Detection Reference](references/prompt-injection.md) <br>
- [BitMind](https://bitmind.ai) <br>
- [GPTZero Documentation](https://gptzero.me/docs) <br>
- [VirusTotal](https://virustotal.com) <br>
- [URLScan.io](https://urlscan.io) <br>
- [Google Safe Browsing](https://safebrowsing.google.com) <br>
- [ProtectAI Prompt Injection Model](https://huggingface.co/ProtectAI/deberta-v3-base-prompt-injection-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON analysis results from invoked scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some checks require API keys and send selected user-provided text, media, or URLs to named third-party services.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
