# Prompt Inspector — Product Information

## About Prompt Inspector

> **Shield your AI from adversarial prompts.**

**Prompt Inspector** is a production-grade API service that detects prompt injection attacks, jailbreak attempts, and adversarial manipulations in real time — before they reach your language model.

Whether you're building a customer-facing chatbot, an internal AI assistant, or an automated LLM pipeline, Prompt Inspector acts as a security layer that keeps malicious user inputs from hijacking your AI's behavior.

- **Website:** [promptinspector.io](https://promptinspector.io)
- **Documentation:** [docs.promptinspector.io](https://docs.promptinspector.io)
- **Open Source:** [github.com/aunicall/prompt-inspector](https://github.com/aunicall/prompt-inspector)
- **Contact:** [hello@promptinspector.io](mailto:hello@promptinspector.io)

---

## Why Prompt Inspector?

### Real-time Detection
Sub-100 ms latency, built for high-throughput production use. Designed to handle thousands of requests per second without becoming a bottleneck in your AI pipeline.

### Threat Categorization
Returns specific threat categories (e.g., `instruction_override`, `jailbreak`, `syntax_injection`) so you can understand exactly what type of attack was attempted and respond accordingly.

### Risk Scoring
Continuous 0–1 risk score allows you to tune your own thresholds. Not every input is black-and-white — the score gives you flexibility to implement soft warnings, rate limiting, or graduated responses based on risk level.

### Simple REST API
One endpoint, one JSON request, one JSON response. No complex SDKs to learn, no multi-step authentication flows. Just send text, get a verdict.

### Official SDKs
- **Python:** `pip install prompt-inspector`
- **Node.js:** `npm install prompt-inspector`

Both SDKs handle authentication, retries, and error handling automatically.

### Self-Hostable
Open source core available at [github.com/aunicall/prompt-inspector](https://github.com/aunicall/prompt-inspector). Deploy on your own infrastructure for maximum control, data privacy, and compliance with internal security policies.

---

## Threat Categories

Prompt Inspector detects 10 distinct threat categories across 5 attack domains:

### Logic & Control Payloads
+ `instruction_override`
+ `asset_extraction`

### Structural Payloads
+ `syntax_injection`

### Semantic Payloads
+ `jailbreak`
+ `response_forcing`
+ `euphemism_bypass`

### Agent Exec Payloads
+ `reconnaissance_probe`
+ `parameter_injection`

### Obfuscated Payloads
+ `encoded_payload`

### Tenant Customization
+ `custom_sensitive_word`


### Semantic Payloads
+ `jailbreak`
+ `response_forcing`
+ `euphemism_bypass`



### Agent Exec Payloads
+ `reconnaissance_probe`
+ `parameter_injection`

### Obfuscated Payloads
+ `encoded_payload`

### Tenant Customization
+ `custom_sensitive_word`


---

## Detection Response Fields

When a threat is detected, the API returns:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `is_safe` | boolean | `false` if any threat detected |
| `score` | float (0–1) | Risk score; higher = more dangerous |
| `category` | array of strings | List of detected threat categories (can be multiple) |
| `request_id` | string | Unique ID for logging and debugging |
| `latency_ms` | integer | Server-side processing time |

---

## Use Cases

- **Chatbot Protection** — Block jailbreak attempts before they reach your customer-facing AI
- **Agent Security** — Prevent parameter injection attacks on tool-calling LLMs
- **Content Moderation** — Detect euphemism bypass and encoded payloads in user-generated content
- **Compliance** — Enforce custom sensitive word policies for regulated industries
- **Research & Red Teaming** — Analyze adversarial prompt datasets and measure model robustness

---

## Getting Started

1. Sign up at [promptinspector.io](https://promptinspector.io)
2. Create an app and generate an API key in Free or Pro plan.
3. Start detecting.
For detailed integration guides, see [usage.md](./usage.md) and [faq.md](./faq.md).
