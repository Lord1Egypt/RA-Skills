#!/usr/bin/env bash
curl http://localhost:11434/api/chat -H "Content-Type: application/json" -d '{
  "model": "gemma3",
  "messages": [{"role": "user", "content": "Hello!"}],
  "stream": false
}'
