#!/bin/bash
# OpenClaw PII Anonymizer v2.0 - Hybrid (regex + qwen2.5:3b)
# Fast regex for structured PII, LLM for names/context

OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
MODEL="${MODEL:-qwen2.5:3b}"
MAX_INPUT=10000

if [ ${#1} -gt $MAX_INPUT ]; then
  echo "Error: Input too long (max $MAX_INPUT chars)" >&2
  exit 1
fi

input="$1"

# Step 1: Fast regex pass for structured PII
# SSN: XXX-XX-XXXX
output=$(echo "$input" | sed -E 's/\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b/[SSN]/g')

# Email addresses
output=$(echo "$output" | sed -E 's/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/[EMAIL]/g')

# Phone: Various formats (XXX-XXX-XXXX, (XXX) XXX-XXXX, XXX.XXX.XXXX)
output=$(echo "$output" | sed -E 's/\b[0-9]{3}[-. ][0-9]{3}[-. ][0-9]{4}\b/[PHONE]/g')
output=$(echo "$output" | sed -E 's/\([0-9]{3}\) [0-9]{3}-[0-9]{4}/[PHONE]/g')

# Ethereum/crypto wallet addresses: 0x + 40 hex chars
output=$(echo "$output" | sed -E 's/\b0x[a-fA-F0-9]{40}\b/[WALLET]/g')

# IP addresses: XXX.XXX.XXX.XXX
output=$(echo "$output" | sed -E 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/[IP]/g')

# File paths: /home/username, /Users/username, C:\Users\username
output=$(echo "$output" | sed -E 's/\/home\/[a-zA-Z0-9_-]+/[PATH]/g')
output=$(echo "$output" | sed -E 's/\/Users\/[a-zA-Z0-9_-]+/[PATH]/g')
output=$(echo "$output" | sed -E 's/C:\\Users\\[a-zA-Z0-9_-]+/[PATH]/g')

# Step 2: Only use LLM if names might be present
# Skip LLM if message is very short
if [ ${#output} -lt 15 ]; then
  # Too short, return regex result
  echo "$output"
  exit 0
fi

# Check if likely contains names (capitalized or lowercase patterns)
# Skip if already fully anonymized (all PII replaced)
if ! echo "$output" | grep -qE '(^|[[:space:]])[a-zA-Z]{2,}[[:space:]][a-zA-Z]{2,}' || \
   echo "$output" | grep -qE '^\[.*\]$'; then
  # No word pairs (no names) or fully anonymized, return regex result
  echo "$output"
  exit 0
fi

# Step 3: LLM pass for names and contextual PII
if ! curl -s --max-time 5 --fail "$OLLAMA_URL/v1/models" >/dev/null 2>&1; then
  # Ollama unavailable, return regex result
  echo "$output"
  exit 0
fi

llm_result=$(curl -s --max-time 20 --fail "$OLLAMA_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {\"role\": \"system\", \"content\": \"You are a PII redaction tool. Replace person names with [NAME]. Keep already anonymized tokens like [SSN], [EMAIL], [PHONE], [WALLET], [IP], [PATH]. Output ONLY the redacted text with NO explanations.\"},
      {\"role\": \"user\", \"content\": \"$(echo "$output" | sed 's/"/\\"/g' | tr '\n' ' ')\"}
    ],
    \"stream\": false,
    \"options\": {\"temperature\": 0.0}
  }") || {
  # LLM failed, return regex result
  echo "$output"
  exit 0
}

final=$(echo "$llm_result" | jq -r '.choices[0].message.content // empty' | tr -d '\n\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [ -n "$final" ] && [ "$final" != "null" ]; then
  echo "$final"
else
  echo "$output"
fi
