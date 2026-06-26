#!/bin/bash
# Create Learning Pipeline
# Usage: ./create_pipeline.sh <topic-slug> [topic-display-name]
# Creates folder structure and initial state.json for a learning topic.

set -euo pipefail

TOPIC_SLUG="${1:?Usage: $0 <topic-slug> [topic-display-name]}"
TOPIC_NAME="${2:-$TOPIC_SLUG}"

# Resolve workspace-relative path
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
BASE_DIR="${WORKSPACE}/memory/learning/${TOPIC_SLUG}"

if [ -d "$BASE_DIR" ]; then
    echo "Error: Topic directory already exists: $BASE_DIR"
    echo "Remove it first or choose a different slug."
    exit 1
fi

# Create directory structure
mkdir -p "${BASE_DIR}/sessions"
mkdir -p "${BASE_DIR}/knowledge"

# Create initial state.json
NOW=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
cat > "${BASE_DIR}/state.json" << EOF
{
  "topic": "${TOPIC_NAME}",
  "topicSlug": "${TOPIC_SLUG}",
  "phase": 1,
  "curriculum": [],
  "currentSubtopicIndex": 0,
  "currentDay": 1,
  "currentSession": "S1",
  "status": "in_progress",
  "sessionTiming": {
    "dailyStartHour": 9,
    "s1ToS2Hours": 4,
    "s2ToS3Hours": 4,
    "s3ToS4Hours": 4
  },
  "notifications": {
    "deliver": false,
    "channel": null,
    "to": null
  },
  "history": [],
  "createdAt": "${NOW}",
  "updatedAt": "${NOW}"
}
EOF

# Create empty curriculum placeholder
cat > "${BASE_DIR}/curriculum.md" << 'EOF'
# Curriculum

<!-- Agent: populate this during setup with 15-20 subtopics -->
EOF

# Create empty validated knowledge file
cat > "${BASE_DIR}/knowledge/validated.md" << 'EOF'
# Validated Knowledge

<!-- Accumulated mastered content across all learning days -->
EOF

echo "Learning pipeline created: ${BASE_DIR}"
echo ""
echo "Contents:"
find "${BASE_DIR}" -type f | sort | sed "s|${BASE_DIR}/|  |"
echo ""
echo "Next: Agent should populate curriculum.md and generate playbook.md"
