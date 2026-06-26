#!/bin/bash
# OpenClaw PII Anonymizer v1.0.2 (Ollama phi3:mini) - Anti-hallucination
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
MODEL="${MODEL:-phi3:mini}"
MAX_INPUT=10000

if [ ${#1} -gt $MAX_INPUT ]; then
  echo "Error: Input too long (max $MAX_INPUT chars)" >&2
  exit 1
fi

if ! curl -s --max-time 10 --fail "$OLLAMA_URL/v1/models" >/dev/null 2>&1; then
  echo "Error: Ollama unavailable at $OLLAMA_URL" >&2
  exit 1
fi

prompt_anonymize() {
  local input="$1"
  local response
  response=$(curl -s --max-time 30 --fail "$OLLAMA_URL/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"$MODEL\",
      \"messages\": [
        {\"role\": \"system\", \"content\": \"Strict anonymize ONLY. Replace PII with [PERSON]/[EMAIL]/[PATH]/[IP]/[PHONE]/[SSN]/[URL]/[ORG]. Output RAW cleaned text ONLY. No explanations/sentences/additions/changes. Example: 'Seth at /home' → '[PERSON] at [PATH]'.\"},
        {\"role\": \"user\", \"content\": \"$input\"}
      ],
      \"stream\": false,
      \"options\": {\"temperature\": 0.1}
    }") || {
    echo "Error: Curl failed" >&2
    exit 1
  }

  echo "$response" | jq -r '.choices[0].message.content // empty' | tr -d '\n\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || {
    echo "Error: jq parse failed" >&2
    exit 1
  }
}

if [ $# -eq 0 ]; then
  echo "Usage: $0 'your raw text'"
  exit 1
fi

prompt_anonymize "$1"
