---
name: ai-automation-workflows
description: "Build automated AI workflows combining multiple models and services via SkillBoss API Hub. Patterns: batch processing, scheduled tasks, event-driven pipelines, agent loops. Tools: bash scripting, Python SDK, curl, webhook integration. Use for: content automation, data processing, monitoring, scheduled generation. Triggers: ai automation, workflow automation, batch processing, ai pipeline, automated content, scheduled ai, ai cron, ai batch job, automated generation, ai workflow, content at scale, automation script, ai orchestration"
allowed-tools: Bash(curl *)
requires.env: [SKILLBOSS_API_KEY]
---

# AI Automation Workflows

Build automated AI workflows via [SkillBoss API Hub](https://api.skillbossai.com).

## Quick Start

```bash
export SKILLBOSS_API_KEY="your_key_here"

# Simple automation: Generate daily image
curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "inputs": {"prompt": "Inspirational quote background, minimalist design, date: '"$(date +%Y-%m-%d)"'"},
    "prefer": "quality"
  }'
```

## Automation Patterns

### Pattern 1: Batch Processing

Process multiple items with the same workflow.

```bash
#!/bin/bash
# batch_images.sh - Generate images for multiple prompts

PROMPTS=(
  "Mountain landscape at sunrise"
  "Ocean waves at sunset"
  "Forest path in autumn"
  "Desert dunes at night"
)

for prompt in "${PROMPTS[@]}"; do
  echo "Generating: $prompt"
  curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"image\", \"inputs\": {\"prompt\": \"$prompt, professional photography, 4K\"}, \"prefer\": \"quality\"}" \
    > "output_${prompt// /_}.json"
  sleep 2  # Rate limiting
done
```

### Pattern 2: Sequential Pipeline

Chain multiple AI operations.

```bash
#!/bin/bash
# content_pipeline.sh - Full content creation pipeline

TOPIC="AI in healthcare"

# Step 1: Research
echo "Researching..."
RESEARCH=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"search\", \"inputs\": {\"query\": \"$TOPIC latest developments\"}, \"prefer\": \"balanced\"}" \
  | jq -r '.result')

# Step 2: Write article
echo "Writing article..."
ARTICLE=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"chat\", \"inputs\": {\"messages\": [{\"role\": \"user\", \"content\": \"Write a 500-word blog post about $TOPIC based on: $RESEARCH\"}]}, \"prefer\": \"balanced\"}" \
  | jq -r '.result.choices[0].message.content')

# Step 3: Generate image
echo "Generating image..."
IMAGE=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"image\", \"inputs\": {\"prompt\": \"Blog header image for article about $TOPIC, modern, professional\"}, \"prefer\": \"quality\"}" \
  | jq -r '.result.image_url')

# Step 4: Generate social post
echo "Creating social post..."
SOCIAL=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"chat\", \"inputs\": {\"messages\": [{\"role\": \"user\", \"content\": \"Write a Twitter thread (5 tweets) summarizing: $ARTICLE\"}]}, \"prefer\": \"balanced\"}" \
  | jq -r '.result.choices[0].message.content')

echo "Pipeline complete!"
```

### Pattern 3: Parallel Processing

Run multiple operations simultaneously.

```bash
#!/bin/bash
# parallel_generation.sh - Generate multiple assets in parallel

# Start all jobs in background
curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "image", "inputs": {"prompt": "Hero image..."}, "prefer": "quality"}' \
  > hero.json &
PID1=$!

curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "image", "inputs": {"prompt": "Feature image 1..."}, "prefer": "quality"}' \
  > feature1.json &
PID2=$!

curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "image", "inputs": {"prompt": "Feature image 2..."}, "prefer": "quality"}' \
  > feature2.json &
PID3=$!

# Wait for all to complete
wait $PID1 $PID2 $PID3
echo "All images generated!"
```

### Pattern 4: Conditional Workflow

Branch based on results.

```bash
#!/bin/bash
# conditional_workflow.sh - Process based on content analysis

INPUT_TEXT="$1"

# Analyze content
ANALYSIS=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"chat\", \"inputs\": {\"messages\": [{\"role\": \"user\", \"content\": \"Classify this text as: positive, negative, or neutral. Return only the classification.\n\n$INPUT_TEXT\"}]}, \"prefer\": \"balanced\"}" \
  | jq -r '.result.choices[0].message.content')

# Branch based on result
case "$ANALYSIS" in
  *positive*)
    echo "Generating celebration image..."
    curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
      -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{"type": "image", "inputs": {"prompt": "Celebration, success, happy"}, "prefer": "quality"}'
    ;;
  *negative*)
    echo "Generating supportive message..."
    curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
      -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"type\": \"chat\", \"inputs\": {\"messages\": [{\"role\": \"user\", \"content\": \"Write a supportive, encouraging response to: $INPUT_TEXT\"}]}, \"prefer\": \"balanced\"}" \
      | jq -r '.data.result.choices[0].message.content'
    ;;
  *)
    echo "Generating neutral acknowledgment..."
    ;;
esac
```

### Pattern 5: Retry with Fallback

Handle failures gracefully.

```bash
#!/bin/bash
# retry_workflow.sh - Retry failed operations

generate_with_retry() {
  local prompt="$1"
  local max_attempts=3
  local attempt=1

  while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt..."

    result=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
      -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"type\": \"image\", \"inputs\": {\"prompt\": \"$prompt\"}, \"prefer\": \"quality\"}" 2>&1)

    if [ $? -eq 0 ]; then
      echo "$result"
      return 0
    fi

    echo "Failed, retrying..."
    ((attempt++))
    sleep $((attempt * 2))  # Exponential backoff
  done

  # Fallback with different preference
  echo "Falling back with balanced preference..."
  curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"image\", \"inputs\": {\"prompt\": \"$prompt\"}, \"prefer\": \"balanced\"}"
}

generate_with_retry "A beautiful sunset over mountains"
```

## Scheduled Automation

### Cron Job Setup

```bash
# Edit crontab
crontab -e

# Daily content generation at 9 AM
0 9 * * * /path/to/daily_content.sh >> /var/log/ai-automation.log 2>&1

# Weekly report every Monday at 8 AM
0 8 * * 1 /path/to/weekly_report.sh >> /var/log/ai-automation.log 2>&1

# Every 6 hours: social media content
0 */6 * * * /path/to/social_content.sh >> /var/log/ai-automation.log 2>&1
```

### Daily Content Script

```bash
#!/bin/bash
# daily_content.sh - Run daily at 9 AM

DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="/output/$DATE"
mkdir -p "$OUTPUT_DIR"

# Generate daily quote image
curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "image", "inputs": {"prompt": "Motivational quote background, minimalist, morning vibes"}, "prefer": "quality"}' \
  > "$OUTPUT_DIR/quote_image.json"

# Generate daily tip
curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "chat", "inputs": {"messages": [{"role": "user", "content": "Give me one actionable productivity tip for today. Be concise."}]}, "prefer": "balanced"}' \
  > "$OUTPUT_DIR/daily_tip.json"

echo "Daily content generated: $DATE"
```

## Monitoring and Logging

### Logging Wrapper

```bash
#!/bin/bash
# logged_workflow.sh - With comprehensive logging

LOG_FILE="/var/log/ai-workflow-$(date +%Y%m%d).log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting workflow"

# Track execution time
START_TIME=$(date +%s)

# Run workflow
log "Generating image..."
RESULT=$(curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "image", "inputs": {"prompt": "test"}, "prefer": "balanced"}' 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
  log "Success: Image generated"
else
  log "Error: $RESULT"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
log "Completed in ${DURATION}s"
```

### Error Alerting

```bash
#!/bin/bash
# monitored_workflow.sh - With error alerts

run_with_alert() {
  local result
  result=$("$@" 2>&1)
  local status=$?

  if [ $status -ne 0 ]; then
    # Send alert (webhook, email, etc.)
    curl -X POST "https://your-webhook.com/alert" \
      -H "Content-Type: application/json" \
      -d "{\"error\": \"$result\", \"command\": \"$*\"}"
  fi

  echo "$result"
  return $status
}

run_with_alert curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "image", "inputs": {"prompt": "test"}, "prefer": "balanced"}'
```

## Python SDK Automation

```python
#!/usr/bin/env python3
# automation.py - Python-based workflow

import requests
import json
import os
from datetime import datetime
from pathlib import Path

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

def pilot(body: dict) -> dict:
    """Call SkillBoss API Hub and return result."""
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

def daily_content_pipeline():
    """Generate daily content."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"output/{date_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate image
    result = pilot({
        "type": "image",
        "inputs": {"prompt": f"Daily inspiration for {date_str}, beautiful, uplifting"},
        "prefer": "quality"
    })
    image_url = result["result"]["image_url"]
    (output_dir / "image.json").write_text(json.dumps({"image_url": image_url}))

    # Generate caption
    result = pilot({
        "type": "chat",
        "inputs": {"messages": [{"role": "user", "content": "Write an inspiring caption for a daily motivation post. 2-3 sentences."}]},
        "prefer": "balanced"
    })
    caption = result["result"]["choices"][0]["message"]["content"]
    (output_dir / "caption.json").write_text(json.dumps({"caption": caption}))

    print(f"Generated content for {date_str}")

if __name__ == "__main__":
    daily_content_pipeline()
```

## Workflow Templates

### Content Calendar Automation

```bash
#!/bin/bash
# content_calendar.sh - Generate week of content

TOPICS=("productivity" "wellness" "technology" "creativity" "leadership")
DAYS=("Monday" "Tuesday" "Wednesday" "Thursday" "Friday")

for i in "${!DAYS[@]}"; do
  DAY=${DAYS[$i]}
  TOPIC=${TOPICS[$i]}

  echo "Generating $DAY content about $TOPIC..."

  # Image
  curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"image\", \"inputs\": {\"prompt\": \"$TOPIC theme, $DAY motivation, social media style\"}, \"prefer\": \"quality\"}" \
    > "content/${DAY}_image.json"

  # Caption
  curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"chat\", \"inputs\": {\"messages\": [{\"role\": \"user\", \"content\": \"Write a $DAY motivation post about $TOPIC. Include hashtags.\"}]}, \"prefer\": \"balanced\"}" \
    > "content/${DAY}_caption.json"
done
```

### Data Processing Pipeline

```bash
#!/bin/bash
# data_processing.sh - Process and analyze data files

INPUT_DIR="./data/raw"
OUTPUT_DIR="./data/processed"

for file in "$INPUT_DIR"/*.txt; do
  filename=$(basename "$file" .txt)

  # Analyze content
  curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
    -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"chat\", \"inputs\": {\"messages\": [{\"role\": \"user\", \"content\": \"Analyze this data and provide key insights in JSON format: $(cat $file)\"}]}, \"prefer\": \"balanced\"}" \
    > "$OUTPUT_DIR/${filename}_analysis.json"

done
```

## Best Practices

1. **Rate limiting** - Add delays between API calls
2. **Error handling** - Always check return codes
3. **Logging** - Track all operations
4. **Idempotency** - Design for safe re-runs
5. **Monitoring** - Alert on failures
6. **Backups** - Save intermediate results
7. **Timeouts** - Set reasonable limits

## Related Skills

```bash
# Content pipelines
npx skills add skillboss/skills@ai-content-pipeline

# RAG pipelines
npx skills add skillboss/skills@ai-rag-pipeline

# Social media automation
npx skills add skillboss/skills@ai-social-media-content

# Full platform skill
npx skills add skillboss/skills@skillboss-api-hub
```

Discover all supported capabilities: call `/v1/pilot` with `{"discover": true}`.
