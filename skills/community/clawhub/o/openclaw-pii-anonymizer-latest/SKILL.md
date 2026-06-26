---
name: openclaw-pii-anonymizer
description: Privacy pipeline for OpenClaw: Scrubs PII (names/emails/paths/IPs) with Ollama before external models (Grok/OpenRouter). Host/VM compatible. Use for memory_search, tool calls, HEARTBEAT.md sanitization.
metadata:
  openclaw:
    requires: { bins: [jq, curl], env: [OLLAMA_URL] }
    install:
      - { id: jq, kind: apt, package: jq }
      - { id: curl, kind: apt, package: curl }
homepage: https://github.com/solmas/openclaw-pii-anonymizer
user-invocable: false

# OpenClaw PII Anonymizer

**Protects MEMORY.md/workspace from leaks**: Pipes prompts through Ollama (phi3:mini) → [PERSON]/[PATH]/[EMAIL].

## Usage
```
./privacy-anonymize.sh "Seth at /home/derenger email@example.com"
→ "[PERSON] at [PATH] [EMAIL]"
```

## Integration
- **HEARTBEAT.md**: `Task: ./privacy-anonymize.sh "$(memory_get MEMORY.md)"`
- **Cron**: Sanitize before web_search/exec.
- **OLLAMA_URL**: `localhost:11434` (VM) or `10.0.2.2:11434` (host).

## Install Ollama Model
```
ollama pull phi3:mini
```

## Files
- `privacy-anonymize.sh`: Core script.
