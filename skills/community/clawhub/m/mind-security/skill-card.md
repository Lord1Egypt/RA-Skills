## Description:

Mind Security helps agents run deepfake detection, prompt-injection scanning, malware and phishing URL checks, and AI-generated text detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canvinus](https://clawhub.ai/user/canvinus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to screen media, text, and URLs for AI-generation signals, prompt-injection attempts, and malware or phishing risk before relying on or forwarding content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned text, URLs, images, and videos may be sent to third-party analysis services.

Mitigation: Avoid submitting secrets, confidential business material, regulated personal data, or private media unless the organization approves those providers and their retention policies; use local-only modes where available for sensitive inputs.

Risk: Optional ML prompt-injection detection uses the llm-guard dependency and a downloaded model when enabled.

Mitigation: Pin and review the optional llm-guard dependency before enabling ML scanning in controlled environments.

Risk: Detection verdicts are screening signals and may be incorrect or incomplete.

Mitigation: Review high-impact findings before action and combine results with application-level security controls and human judgment.

## Reference(s):

- [Mind Security ClawHub Page](https://clawhub.ai/canvinus/skills/mind-security)
- [Mind Security Homepage](https://github.com/mind-sec/mind-security)
- [Deepfake Detection](references/deepfake-detection.md)
- [Prompt Injection Detection](references/prompt-injection.md)
- [URL Threat Scanning](references/malware-scanning.md)
- [AI-Generated Text Detection](references/ai-text-detection.md)
- [BitMind](https://bitmind.ai)
- [GPTZero Documentation](https://gptzero.me/docs)
- [ProtectAI Prompt Injection Model](https://huggingface.co/ProtectAI/deberta-v3-base-prompt-injection-v2)
- [VirusTotal](https://virustotal.com)
- [URLScan.io](https://urlscan.io)
- [Google Safe Browsing](https://safebrowsing.google.com)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON objects from command-line scripts, with Markdown reference documentation for setup and interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; API-backed modes use BITMIND_API_KEY, GPTZERO_API_KEY, VIRUSTOTAL_API_KEY, URLSCAN_API_KEY, or GOOGLE_SAFE_BROWSING_KEY when configured.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
