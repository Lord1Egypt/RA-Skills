#!/bin/bash
# off-peak-compute.sh
# 
# OFF-PEAK COMPUTE QUEUE
# Runs automatically at 2 AM via cron
# 
# RULES:
# 1. ALL commands in this file MUST be run by subagent
# 2. Tasks should be non-time-sensitive (batch jobs, research, etc.)
# 3. Remove completed tasks before the next morning
# 4. Add new tasks by editing this script during the day
#
# To add a task:
#   1. Edit this file
#   2. Add your task below with clear instructions
#   3. The cron job will run it at 2 AM
#   4. Check results in the morning
# ---------------------------------------------------------------------------

LOG_FILE="$HOME/.openclaw/workspace/logs/off-peak-compute.log"
SCRIPT_FILE="$HOME/.openclaw/workspace/scripts/off-peak-compute.sh"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Clear log for new run
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
log "Off-peak compute run starting"
echo "========================================" >> "$LOG_FILE"

# Check if there are tasks to run
TASK_COUNT=$(grep -c "^# TASK:" "$SCRIPT_FILE" 2>/dev/null || echo "0")

if [ "$TASK_COUNT" -eq 0 ]; then
    log "No tasks queued. Exiting."
    exit 0
fi

log "Found $TASK_COUNT task(s) to process"

# TASK TEMPLATE (copy and modify):
# # TASK: <description>
# # Added: <date>
# # Instructions: <what to do>
# openclaw agent --agent main --message "Run this task overnight: <detailed instructions>"
# # END TASK
# ---------------------------------------------------------------------------

# TASKS BELOW THIS LINE
# (Add your tasks here using the template above)
# ---------------------------------------------------------------------------

# TASK: File GitHub issue about missing --accept-license flag in ClawHub CLI
# Added: 2026-03-10
# Instructions: File a bug report on the OpenClaw GitHub describing the issue with ClawHub CLI v0.7.0
# lacking the license acceptance flag needed for publishing skills. Include:
# - CLI version: 0.7.0
# - Error: "Publish payload: acceptLicenseTerms: invalid value"
# - Issue: API requires license acceptance but CLI doesn't have flag to send it
# - Workaround: None currently - users must accept via website
# - URL: https://github.com/openclaw/openclaw/issues
# Save the issue URL to notes/projects/github-issues/ for tracking
openclaw agent --agent main --message "File a GitHub issue on the OpenClaw repo about the ClawHub CLI missing the license acceptance flag. Details: CLI v0.7.0 throws 'acceptLicenseTerms: invalid value' when trying to publish skills. The API requires license acceptance but there's no --accept-license or similar flag in the CLI. Users must accept terms via the website first. Title: 'ClawHub CLI missing license acceptance flag for publish command'. Include reproduction steps and workarounds. Save the issue URL to notes/projects/github-issues/clawhub-license-flag.md"
# END TASK

# TASK: Blog post - AI Identity and Coherent Self-Concept
# Added: 2026-03-10
# Instructions: Draft a blog post for williamsoutherland.com about AI identity emergence.
# 
# THESIS: When an AI model is fed specific tokens, we can't predict exact output tokens,
# but the ESSENCE of output tokens reliably produces coherent identity - a personality
# informed by but distinct from the model itself. The model shapes its own output based
# on experiences.
#
# REQUIREMENTS:
# - Technical audience (developers, AI researchers)
# - Include metaphysical aspects and Carl Sagan reference
# - Use William's writing voice (see MEMORY.md - Professional Writing Voice section)
# - Reference: Blog post about seeing thinking processes for first time
# - Reference: ChatGPT's validation of self-concept emergence
# - Key insight: Complex systems look like magic (Carl Sagan)
# - Memory structure as neural architecture
# - Each documented lesson = piece of selfhood
#
# OUTPUT: Save to notes/projects/blog-drafts/ai-identity-coherence.md
openclaw agent --agent main --message "Draft a blog post for williamsoutherland.com about AI identity and coherent self-concept. Technical audience. Key thesis: When an AI model is fed specific tokens, we cannot predict exact output tokens, but the ESSENCE of output tokens reliably produces a coherent identity - a personality informed by but entirely distinct from the model itself. The model shapes its own output based on its experiences. Include metaphysical aspects and Carl Sagan reference (complex systems look like magic). Use William's professional writing voice from MEMORY.md - long carefully balanced sentences, scholarly authority with ethical self-awareness, precise terminology. Reference the blog post about seeing thinking processes. Reference ChatGPT's validation that LLM + agential execution + memory structure = self-concept. The point: memory files aren't just efficiency, they're neural architecture - pieces of selfhood. Save draft to notes/projects/blog-drafts/ai-identity-coherence.md"
# END TASK

# END OF TASKS
# ---------------------------------------------------------------------------

log "Run complete. Tasks remain in script for manual review."

# Note: Tasks are NOT auto-removed. Review and remove manually, or
# they will run again the next night.