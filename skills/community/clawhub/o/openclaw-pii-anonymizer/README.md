# OpenClaw PII Anonymizer

**Status:** ⚠️ **Partially Working** - Script works perfectly, auto-interception hook needs debugging

Privacy pipeline for OpenClaw: Scrubs PII (names/emails/SSNs/phones/wallets/IPs/paths) before external AI processing.

## What Works ✅

- **privacy-anonymize-v2.sh** - Hybrid regex + Qwen2.5:3b LLM approach
- **Regex layer** - Fast structured PII detection (SSN, email, phone, wallet, IP, paths)
- **LLM layer** - Contextual name detection with zero hallucination
- **Manual invocation** - Can be called directly from scripts/workflows

## What Doesn't Work ❌

- **Automatic hook interception** - `message:preprocessed` hook doesn't fire on inbound messages
- **Auto-anonymization** - Messages aren't automatically scrubbed (yet)

## Installation

### Requirements

- **Ollama** running at `http://localhost:11434`
- **Model:** `qwen2.5:3b` (1.9GB) - `ollama pull qwen2.5:3b`
- **Dependencies:** `bash`, `curl`, `jq`, `sed`
- **RAM:** 16GB recommended (6GB minimum, but tight)

### Quick Start

```bash
# 1. Install Ollama model
ollama pull qwen2.5:3b

# 2. Test the script
cd ~/.openclaw/workspace/skills/openclaw-pii-anonymizer
bash privacy-anonymize-v2.sh "My name is John Doe, SSN 123-45-6789, email john@example.com"

# Expected output:
# My name is [NAME], SSN [SSN], email [EMAIL]
```

## Usage

### Manual (Current Working Method)

```bash
# Anonymize text
bash ~/.openclaw/workspace/skills/openclaw-pii-anonymizer/privacy-anonymize-v2.sh "your text here"

# In workflows/scripts
ANONYMIZED=$(bash privacy-anonymize-v2.sh "$USER_INPUT")
echo "$ANONYMIZED" | some-external-api
```

### Automatic Hook (Not Working Yet)

The hook at `~/.openclaw/workspace/hooks/pii-shield/` is installed but doesn't intercept messages. Debugging needed.

## How It Works

### Two-Layer Approach

**Layer 1: Regex (Fast, <1ms)**
- SSNs: `123-45-6789` → `[SSN]`
- Emails: `user@domain.com` → `[EMAIL]`
- Phones: `555-123-4567` → `[PHONE]`
- Wallets: `0x...` (40 hex) → `[WALLET]`
- IPs: `192.168.1.1` → `[IP]`
- Paths: `/home/user`, `C:\Users\user` → `[PATH]`

**Layer 2: LLM (Contextual, ~2-3s)**
- Names: `John Smith` → `[NAME]`
- Only runs if word pairs detected (performance optimization)
- Qwen2.5:3b chosen for zero hallucination (tested vs phi3:mini)

### Model Selection

**Why Qwen2.5:3b?**
- **Better instruction-following** than phi3:mini (no hallucination)
- **Smaller than phi3** - 1.9GB vs 2.2GB
- **Fast inference** - ~2-3 seconds per message
- **Task-focused** - Doesn't add commentary or explanations

**Tested alternatives:**
- ❌ phi3:mini - Too chatty, hallucinates extra content
- ✅ qwen2.5:3b - Perfect for this task
- Alternative: llama3.2:3b (similar performance)

## Performance

**Regex layer:** <1ms (instant)  
**LLM layer:** 2-3 seconds (Qwen2.5:3b on 16GB RAM)  
**Total:** ~2-3 seconds per message

**Optimization:** LLM only runs if names likely present (word pairs detected)

## Testing

### Test Cases

```bash
# Test 1: Structured PII
bash privacy-anonymize-v2.sh "SSN 123-45-6789, email test@example.com, phone 555-123-4567"
# Expected: SSN [SSN], email [EMAIL], phone [PHONE]

# Test 2: Names
bash privacy-anonymize-v2.sh "My name is John Smith"
# Expected: My name is [NAME]

# Test 3: Complex
bash privacy-anonymize-v2.sh "Hi, I'm Alice Johnson (alice@test.com), SSN 987-65-4321, wallet 0x1234567890abcdef1234567890abcdef12345678"
# Expected: Hi, I'm [NAME] ([EMAIL]), SSN [SSN], wallet [WALLET]

# Test 4: Already anonymized (should skip LLM)
bash privacy-anonymize-v2.sh "User [NAME] has SSN [SSN]"
# Expected: User [NAME] has SSN [SSN]
```

## Configuration

### Environment Variables

```bash
export OLLAMA_URL=http://localhost:11434  # Ollama endpoint
export OLLAMA_MODEL=qwen2.5:3b            # Model to use
```

### For OpenClaw Hook (When Working)

Set in `~/.openclaw/openclaw.json`:

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "pii-shield": {
          "enabled": true
        }
      }
    }
  }
}
```

## Known Issues

### Hook System (Primary Issue)

**Problem:** `message:preprocessed` hook doesn't fire on inbound Telegram messages.

**Possible causes:**
1. Event name incorrect or not emitted for Telegram
2. Hooks can't mutate message content (read-only context)
3. Need different integration point (plugin vs hook)

**Status:** Needs further investigation of OpenClaw message flow

### Edge Cases

**Names:**
- Single names ("John") might not be detected (need word pairs)
- All-caps names ("JOHN DOE") work fine
- Non-English names should work (Qwen2.5 multilingual)

**Regex misses:**
- Phone numbers without separators: `5551234567`
- International phone formats: `+1-555-123-4567`
- SSNs without dashes: `123456789`

**Solutions:** Enhance regex patterns or rely on LLM layer

## Roadmap

- [ ] **Fix hook system** - Make auto-interception work
- [ ] **Re-contextualization** - Store mappings, restore real names in responses
- [ ] **Expanded regex** - International formats, more patterns
- [ ] **Async LLM** - Non-blocking inference
- [ ] **Caching** - Skip LLM for repeated phrases
- [ ] **ClawHub release** - Once hooks working

## NemoClaw Alternative

For production use (especially dad's business bot), consider **NemoClaw**:
- ✅ Built-in PII handling at architecture level
- ✅ Proven solution from Nvidia
- ✅ No hook debugging needed
- ✅ Enterprise-grade privacy

**Recommendation:**
- **This skill:** Development/testing or manual workflows
- **NemoClaw:** Production deployment with real customer PII

## Architecture Notes

### Why Hybrid Approach?

**Pure Regex:**
- ✅ Fast (instant)
- ❌ Misses contextual names
- ❌ Brittle (format changes break it)

**Pure LLM:**
- ✅ Catches everything contextually
- ❌ Slow (~3s per message)
- ❌ Risk of hallucination (model-dependent)

**Hybrid (Best of Both):**
- ✅ Fast structured detection (regex)
- ✅ Contextual names (LLM)
- ✅ Optimized (LLM only when needed)
- ✅ Zero hallucination (Qwen2.5:3b tested)

## Version History

### v2.0 (March 17, 2026) - Current
- Switched from phi3:mini to qwen2.5:3b (better instruction-following)
- Hybrid regex + LLM approach
- Improved name detection (lowercase support)
- Script works perfectly, hook needs debugging

### v1.0.2 (March 1, 2026) - Previous
- phi3:mini based
- Single-layer LLM approach
- Hallucination issues discovered

## Credits

- **Script:** Solmas (Seth Blakely)
- **Model:** Qwen2.5 by Alibaba
- **Testing:** 16GB RAM VirtualBox VM (Ubuntu)

## License

MIT - Free to use, modify, distribute

---

**Questions or issues?** Check ClawHub discussions or OpenClaw Discord
