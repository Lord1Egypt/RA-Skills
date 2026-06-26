# Knowfun.io API Usage Examples

English | [简体中文](examples_CN.md)

Comprehensive examples of using the Knowfun.io API skill.

## Setup

First, set your API key:
```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"
```

Or create a `.env` file:
```bash
echo 'KNOWFUN_API_KEY="kf_your_api_key_here"' >> .env
```

---

## Example 1: Create a Simple Course

Create a course from text:

```bash
/knowfun create course "Introduction to Python: Python is a high-level programming language known for its simplicity and readability."
```

Expected output:
```
✅ Task created successfully!
Task ID: c3199fb3-350b-4981-858d-09b949bfae88
Status: pending
Request ID: req_1234567890

Check status with: /knowfun status c3199fb3-350b-4981-858d-09b949bfae88
```

---

## Example 2: Create a Course from URL

Create a course from a PDF document:

```bash
/knowfun create course https://example.com/machine-learning-basics.pdf
```

---

## Example 3: Create a Poster with Custom Style

Create a poster with specific styling:

```bash
/knowfun create poster "Climate Change: Rising temperatures are causing polar ice caps to melt at an alarming rate."
```

Then configure it with custom options (Claude will prompt for these):
- Usage: infographic
- Style: handDrawn
- Aspect Ratio: 16:9

---

## Example 4: Create an Interactive Game

Create an interactive learning game:

```bash
/knowfun create game "Learn JavaScript: Variables, Functions, and Loops"
```

Game type will default to "interactive" which provides an animated demo style.

---

## Example 5: Create a Documentary Film

Create a documentary-style video:

```bash
/knowfun create film "The History of the Internet: From ARPANET to the World Wide Web"
```

---

## Example 6: Advanced Course Creation with Full Config

Using curl directly (Claude can help construct this):

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "course-ml-intro-001",
    "taskType": "course",
    "material": {
      "text": "Machine Learning Introduction: ML is a subset of AI...",
      "type": "text"
    },
    "config": {
      "course": {
        "contentStyle": "detailed",
        "contentLanguage": "en",
        "explainLanguage": "en",
        "voiceType": "professional",
        "ttsStyle": "classroom"
      }
    },
    "language": "en"
  }'
```

---

## Example 7: Check Task Status

Check the status of a running task:

```bash
/knowfun status c3199fb3-350b-4981-858d-09b949bfae88
```

Expected output:
```
📊 Task Status
Task ID: c3199fb3-350b-4981-858d-09b949bfae88
Status: processing
Progress: 45%
Current Step: Generating slides

Created: 2026-03-01 10:00:00
```

---

## Example 8: Get Complete Task Details

Get full details including the result:

```bash
/knowfun detail c3199fb3-350b-4981-858d-09b949bfae88
```

Expected output for a completed course:
```
✅ Task Completed!

Task ID: c3199fb3-350b-4981-858d-09b949bfae88
Type: course
Status: completed

📚 Course Details:
- Title: Introduction to Python
- URL: https://r2.knowfun.io/courses/xxx.html
- Slides: 12
- Total Duration: 3 minutes
- Cover: https://r2.knowfun.io/covers/xxx.png

💰 Credits Used: 100

⏱️ Timeline:
- Created: 2026-03-01 10:00:00
- Completed: 2026-03-01 10:03:00
- Duration: 3 minutes
```

---

## Example 9: List Recent Tasks

List your recent tasks:

```bash
/knowfun list
```

Expected output:
```
📋 Recent Tasks

1. Course: "Introduction to Python"
   ID: c3199fb3-350b-4981-858d-09b949bfae88
   Status: completed ✅
   Created: 2026-03-01 10:00:00

2. Poster: "Climate Change Facts"
   ID: a1b2c3d4-5678-90ab-cdef-1234567890ab
   Status: processing ⏳
   Created: 2026-03-01 09:45:00

3. Game: "Learn JavaScript"
   ID: f1e2d3c4-b5a6-9788-6543-210fedcba987
   Status: completed ✅
   Created: 2026-03-01 09:30:00
```

---

## Example 10: Check Credit Balance

Check your available credits:

```bash
/knowfun credits
```

Expected output:
```
💰 Credit Balance

Available: 1,000 credits
Total Earned: 1,500 credits
Total Used: 400 credits
Locked: 100 credits

💡 Pricing:
- Course: 100 credits
- Poster: 100 credits
- Game: 100 credits
- Film: 100 credits

Get more credits at: https://www.knowfun.io/api-platform
```

---

## Example 11: Get Configuration Schema

Get all available configuration options:

```bash
/knowfun schema
```

This returns the complete schema with all available options for each task type.

---

## Example 12: Create Poster with All Options

Create a highly customized poster:

Using the skill (Claude will construct the curl command):
```bash
/knowfun create poster "AI Revolution" --usage marketing --style photorealistic --ratio 16:9
```

Or using curl directly:
```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "poster-ai-rev-001",
    "taskType": "poster",
    "material": {
      "text": "AI Revolution: How artificial intelligence is transforming industries",
      "type": "text"
    },
    "config": {
      "poster": {
        "usage": "marketing",
        "style": "photorealistic",
        "aspectRatio": "16:9",
        "posterTitle": "The AI Revolution"
      }
    }
  }'
```

---

## Example 13: Create Custom Style Poster

Create a poster with custom style:

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "poster-custom-001",
    "taskType": "poster",
    "material": {
      "text": "Modern Web Development: React, Vue, and Angular",
      "type": "text"
    },
    "config": {
      "poster": {
        "usage": "infographic",
        "style": "custom",
        "customStylePrompt": "Minimalist modern design with pastel colors and geometric shapes",
        "aspectRatio": "1:1"
      }
    }
  }'
```

---

## Example 14: Create Story-Based Game

Create a story-driven game:

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "game-story-001",
    "taskType": "game",
    "material": {
      "text": "Ancient Egypt: Learn about pyramids, pharaohs, and hieroglyphics",
      "type": "text"
    },
    "config": {
      "game": {
        "gameType": "story"
      }
    }
  }'
```

---

## Example 15: Create Tutorial Film

Create a step-by-step tutorial video:

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "film-tutorial-001",
    "taskType": "film",
    "material": {
      "text": "How to Deploy a Website: A step-by-step guide to deploying your first website",
      "type": "text"
    },
    "config": {
      "film": {
        "filmStyle": "tutorial",
        "aspectRatio": "16:9"
      }
    }
  }'
```

---

## Example 16: Create Course from YouTube URL

Create a course from a YouTube video:

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "course-yt-001",
    "taskType": "course",
    "material": {
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "type": "youtube"
    },
    "config": {
      "course": {
        "contentStyle": "concise",
        "contentLanguage": "en",
        "explainLanguage": "en"
      }
    }
  }'
```

---

## Example 17: Monitor Task with Polling

Create a simple monitoring script:

```bash
#!/bin/bash
TASK_ID="c3199fb3-350b-4981-858d-09b949bfae88"

while true; do
  STATUS=$(curl -s "https://api.knowfun.io/api/openapi/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer $KNOWFUN_API_KEY" | jq -r '.data.status')

  echo "Current status: $STATUS"

  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
    echo "Task completed with status: $STATUS"
    break
  fi

  sleep 5
done
```

---

## Example 18: Batch Create Multiple Tasks

Create multiple tasks in sequence:

```bash
#!/bin/bash

TOPICS=("Python Basics" "JavaScript Fundamentals" "CSS Flexbox" "Git Workflow")

for topic in "${TOPICS[@]}"; do
  echo "Creating course for: $topic"

  curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
    -H "Authorization: Bearer $KNOWFUN_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"requestId\": \"course-$(date +%s)\",
      \"taskType\": \"course\",
      \"material\": {
        \"text\": \"Learn $topic: A comprehensive guide\",
        \"type\": \"text\"
      }
    }"

  sleep 2
done
```

---

## Example 19: Error Handling

Handle common errors gracefully:

```bash
response=$(curl -s -w "\n%{http_code}" https://api.knowfun.io/api/openapi/v1/tasks \
  -X POST \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "test-001",
    "taskType": "course",
    "material": {
      "text": "Test content"
    }
  }')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

case $http_code in
  200)
    echo "✅ Success: $body"
    ;;
  401)
    echo "❌ Authentication failed. Check your API key."
    ;;
  402)
    echo "❌ Insufficient credits. Top up at https://www.knowfun.io/api-platform"
    ;;
  429)
    echo "⚠️ Rate limit exceeded. Please wait and try again."
    ;;
  *)
    echo "❌ Error ($http_code): $body"
    ;;
esac
```

---

## Example 20: Get Usage Statistics

Get detailed usage statistics:

```bash
curl -s "https://api.knowfun.io/api/openapi/usage?page=1&pageSize=20" \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" | jq '{
    total_credits: .data.summary.totalCreditsUsed,
    total_tasks: .data.summary.taskCount,
    by_type: .data.summary.byTaskType,
    recent_tasks: .data.records[0:5]
  }'
```

---

## Tips and Best Practices

### 1. Use Unique Request IDs
Always use unique request IDs for idempotency:
```bash
REQUEST_ID="course-$(date +%s)-$(uuidgen)"
```

### 2. Poll Responsibly
When polling for status, use reasonable intervals:
```bash
# Good: 5-10 second intervals
sleep 5

# Avoid: Too frequent polling
# sleep 1  # Don't do this
```

### 3. Handle Callbacks
For production use, set up a callback endpoint:
```json
{
  "callbackUrl": "https://your-server.com/api/knowfun-callback"
}
```

### 4. Check Credits First
Always check credit balance before batch operations:
```bash
/knowfun credits
```

### 5. Save Task IDs
Keep track of your task IDs for future reference:
```bash
TASK_ID=$(curl ... | jq -r '.data.taskId')
echo "$TASK_ID" >> task_history.txt
```

### 6. Use Verbose Mode for Debugging
When troubleshooting, use verbose mode:
```bash
curl -v https://api.knowfun.io/api/openapi/v1/tasks/...
```

### 7. Set Timeouts
Set appropriate timeouts for long-running operations:
```bash
curl --max-time 300 ...
```

---

## Common Workflows

### Workflow 1: Quick Content Generation

1. Create task: `/knowfun create course "Your topic"`
2. Get task ID from response
3. Wait 2-3 minutes
4. Check details: `/knowfun detail <taskId>`
5. Access the generated content URL

### Workflow 2: Production Pipeline

1. Check credits: `/knowfun credits`
2. Create task with callback URL
3. Receive callback notification
4. Fetch detailed results
5. Process and store results
6. Log usage for billing

### Workflow 3: Batch Processing

1. Prepare list of content items
2. Check total credit requirement
3. Create tasks sequentially with delays
4. Store task IDs in database
5. Poll or wait for callbacks
6. Collect and process results

---

## Troubleshooting

### Issue: Task Stuck in "processing"

```bash
# Check detailed status
/knowfun detail <taskId> --verbose

# If stuck for >10 minutes, contact support
```

### Issue: "Insufficient Credits"

```bash
# Check balance
/knowfun credits

# Top up at https://www.knowfun.io/api-platform
```

### Issue: "Rate Limit Exceeded"

```bash
# Wait and retry with exponential backoff
sleep 60
/knowfun create ...
```

### Issue: Authentication Failed

```bash
# Verify API key
echo $KNOWFUN_API_KEY

# Regenerate if needed at https://www.knowfun.io/api-platform
```
