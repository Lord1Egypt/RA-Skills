---
name: openclaw-pii-anonymizer
description: Privacy pipeline for OpenClaw - Hybrid regex + Qwen2.5 LLM to scrub PII (names/emails/SSNs/phones/wallets/IPs/paths) before external AI processing. Script works perfectly; auto-hook interception needs debugging.
metadata:
  openclaw:
    requires: { bins: [jq, curl, bash, sed], env: [OLLAMA_URL] }
    install:
      - { id: jq, kind: apt, package: jq }
      - { id: curl, kind: apt, package: curl }
      - { id: ollama, kind: manual, label: "Install Ollama and pull qwen2.5:3b" }
homepage: https://github.com/solmas/openclaw-pii-anonymizer
user-invocable: true
---

# OpenClaw PII Anonymizer v2.0

**Status:** ⚠️ **Partially Working**
- ✅ Script works perfectly (manual invocation)
- ❌ Auto-hook interception needs debugging

Hybrid regex + Qwen2.5:3b LLM to scrub PII before external AI calls.

## Quick Start

```bash
# 1. Install Ollama model
ollama pull qwen2.5:3b

# 2. Test the script
cd ~/.openclaw/workspace/skills/openclaw-pii-anonymizer
bash privacy-anonymize-v2.sh "My name is John Doe, SSN 123-45-6789"
# Output: My name is [NAME], SSN [SSN]
```

## What It Does

**Replaces PII with tokens:**
- Names → `[NAME]`
- SSNs → `[SSN]`  
- Emails → `[EMAIL]`
- Phones → `[PHONE]`
- Wallets → `[WALLET]`
- IPs → `[IP]`
- Paths → `[PATH]`

**Two-layer approach:**
1. **Regex (fast, <1ms)** - Structured PII (SSN, email, phone, etc.)
2. **Qwen2.5:3b (2-3s)** - Contextual names (zero hallucination)

## Usage

### Manual (Working Now)

```bash
# In scripts/workflows
ANONYMIZED=$(bash privacy-anonymize-v2.sh "$USER_INPUT")
echo "$ANONYMIZED" | external-api-call
```

### Automatic Hook (TODO)

Hook installed at `~/.openclaw/workspace/hooks/pii-shield/` but doesn't fire on messages yet. Debugging needed.

## Requirements

- **Ollama** running at `http://localhost:11434`
- **Model:** `qwen2.5:3b` (1.9GB) - Better instruction-following than phi3:mini
- **RAM:** 16GB recommended (6GB minimum but tight)
- **Dependencies:** `bash`, `curl`, `jq`, `sed`

## Why Qwen2.5:3b?

Tested alternatives:
- ❌ **phi3:mini** - Hallucinates extra content, too chatty
- ✅ **qwen2.5:3b** - Zero hallucination, task-focused, smaller (1.9GB vs 2.2GB)
- Alternative: `llama3.2:3b` (similar performance)

## Performance

- **Regex layer:** <1ms
- **LLM layer:** 2-3s (only runs if names detected)
- **Optimization:** Skips LLM for short messages or already-anonymized text

## Known Issues

1. **Hook system** - `message:preprocessed` event doesn't fire (needs investigation)
2. **Auto-interception** - Messages not automatically scrubbed yet
3. **Re-contextualization** - Not implemented (responses stay anonymized)

## For Production

Consider **NemoClaw** for production deployments:
- Built-in PII handling at architecture level
- Enterprise-grade from Nvidia
- No hook debugging needed

**This skill:** Development/testing, manual workflows  
**NemoClaw:** Production with real customer PII

## Testing

```bash
# Test 1: Structured PII
bash privacy-anonymize-v2.sh "SSN 123-45-6789, email test@example.com"
# Expected: SSN [SSN], email [EMAIL]

# Test 2: Names
bash privacy-anonymize-v2.sh "Hi, I'm Alice Johnson"
# Expected: Hi, I'm [NAME]

# Test 3: Complex
bash privacy-anonymize-v2.sh "John Smith (john@test.com), SSN 987-65-4321, wallet 0x1234567890abcdef1234567890abcdef12345678"
# Expected: [NAME] ([EMAIL]), SSN [SSN], wallet [WALLET]
```

## Files

- **privacy-anonymize-v2.sh** - Main script (hybrid approach)
- **privacy-anonymize.sh** - Old v1 (phi3:mini, deprecated)
- **hooks/pii-shield/** - Auto-interception hook (needs debugging)
- **README.md** - Full documentation

## Configuration

```bash
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2.5:3b
```

## Roadmap

- [ ] Fix hook system for auto-interception
- [ ] Re-contextualization (restore real names in responses)
- [ ] Expanded regex patterns (international formats)
- [ ] Async LLM (non-blocking)
- [ ] Caching for repeated phrases

## Version

**v2.0** (March 17, 2026)
- Hybrid regex + Qwen2.5:3b
- Script works perfectly
- Hook needs debugging

**v1.0.2** (March 1, 2026)
- phi3:mini based
- Hallucination issues

---

**License:** MIT  
**Author:** Solmas (Seth Blakely)  
**Homepage:** https://github.com/solmas/openclaw-pii-anonymizer
