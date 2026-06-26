#!/usr/bin/env bash
# setup.sh — jobautopilot skill bundle first-time setup
#
# Run this once after installing the skills:
#   bash ~/.openclaw/workspace/skills/jobautopilot-bundle/setup.sh
#
# PRIVACY NOTICE:
#   This script collects personal information (name, email, phone, LinkedIn,
#   EEOC data) and writes it ONLY to the local path:
#     ~/.openclaw/users/<username>/config.sh
#   No data is sent to any network endpoint. You can verify by reading this
#   script in full before running it.
#
# What it does:
#   1. Asks you a few questions
#   2. Writes ~/.openclaw/users/<you>/config.sh with your info
#   3. Creates the workspace folders and tracker file
#   4. Copies scripts from the installed skills to the workspace
#   5. Creates two isolated browser profiles (search, apply)
#   6. Prints a quick-start guide

set -e

echo ""
echo "=== jobautopilot skill bundle — first-time setup ==="
echo ""
echo "This script only writes to local files on your machine."
echo "Nothing is sent to any external service."
echo ""

# ── 0. Check that all three skills are installed ───────────────────────────────

# This script lives at .../skills/jobautopilot-bundle/setup.sh
# Other skills are siblings: .../skills/jobautopilot-search, etc.
BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(dirname "$BUNDLE_DIR")"
SEARCH_DIR="${SKILLS_ROOT}/jobautopilot-search"
TAILOR_DIR="${SKILLS_ROOT}/jobautopilot-tailor"
SUBMITTER_DIR="${SKILLS_ROOT}/jobautopilot-submitter"

missing=()
[ -d "$SEARCH_DIR" ]    || missing+=("jobautopilot-search")
[ -d "$TAILOR_DIR" ]    || missing+=("jobautopilot-tailor")
[ -d "$SUBMITTER_DIR" ] || missing+=("jobautopilot-submitter")

if [ ${#missing[@]} -gt 0 ]; then
  echo "❌  Missing skill(s): ${missing[*]}"
  echo "    Please install them first:"
  for s in "${missing[@]}"; do
    echo "      clawhub install ${s}"
  done
  exit 1
fi

# ── 1. Collect user info ───────────────────────────────────────────────────────

read -rp "Choose a username (used for local config path, e.g. your system username): " OPENCLAW_USER
read -rp "First name: " USER_FIRST_NAME
read -rp "Last name:  " USER_LAST_NAME
read -rp "Email:      " USER_EMAIL
read -rp "Phone (e.g. +1-212-555-0000): " USER_PHONE
read -rp "LinkedIn URL: " USER_LINKEDIN
echo ""
read -rp "Resume folder (where your original .docx resumes live) [~/Documents/jobs/]: " RESUME_DIR
RESUME_DIR="${RESUME_DIR:-$HOME/Documents/jobs/}"
read -rp "Tailored output folder [~/Documents/jobs/tailored/]: " RESUME_OUTPUT_DIR
RESUME_OUTPUT_DIR="${RESUME_OUTPUT_DIR:-$HOME/Documents/jobs/tailored/}"
echo ""
read -rp "Job search location [New York City]: " JOB_SEARCH_LOCATION
JOB_SEARCH_LOCATION="${JOB_SEARCH_LOCATION:-New York City}"
read -rp "Search keywords (space-separated) [software engineer python]: " JOB_SEARCH_KEYWORDS
JOB_SEARCH_KEYWORDS="${JOB_SEARCH_KEYWORDS:-software engineer python}"
read -rp "Minimum base salary (leave blank to skip): " JOB_SEARCH_MIN_SALARY
read -rp "Max listing age in days [90]: " JOB_SEARCH_MAX_AGE_DAYS
JOB_SEARCH_MAX_AGE_DAYS="${JOB_SEARCH_MAX_AGE_DAYS:-90}"
echo ""

# ── EEOC fields ────────────────────────────────────────────────────────────────
# These are standard fields required by US job application forms (Equal Employment
# Opportunity Commission). Your answers are stored locally and supplied only to
# the forms you explicitly ask the agent to fill. They are not sent anywhere else.
echo "--- EEOC defaults (US job application form fields) ---"
echo "    Your answers are stored locally and used only on forms you approve."
echo ""
read -rp "Gender (e.g. Male / Female / Prefer not to say): " USER_GENDER
read -rp "Race/Ethnicity (e.g. Asian / White / Hispanic / Prefer not to say): " USER_RACE
read -rp "Hispanic or Latino origin? (Yes / No / Prefer not to say): " USER_HISPANIC
read -rp "Veteran status (e.g. 'I have no military service'): " USER_VETERAN
read -rp "Disability status (e.g. No / Yes / Prefer not to say): " USER_DISABILITY
read -rp "Work authorized in US? (Yes / No): " USER_WORK_AUTH
read -rp "Require visa sponsorship? (Yes / No): " USER_NEED_SPONSOR

# ── 1.5. Validate inputs ─────────────────────────────────────────────────────
# OPENCLAW_USER is used in file paths — restrict to safe characters only.
if ! echo "$OPENCLAW_USER" | grep -qE '^[a-zA-Z0-9_.-]+$'; then
  echo "❌  Invalid username: only letters, numbers, underscores, hyphens, and dots are allowed."
  exit 1
fi
if [ -z "$OPENCLAW_USER" ]; then
  echo "❌  Username cannot be empty."
  exit 1
fi
# Sanitize all text inputs: remove shell metacharacters that could cause
# injection when the config file is sourced. Only allow printable ASCII
# minus backticks, $, and backslashes.
sanitize() {
  printf '%s' "$1" | tr -d '`$\\";'
}
USER_FIRST_NAME="$(sanitize "$USER_FIRST_NAME")"
USER_LAST_NAME="$(sanitize "$USER_LAST_NAME")"
USER_EMAIL="$(sanitize "$USER_EMAIL")"
USER_PHONE="$(sanitize "$USER_PHONE")"
USER_LINKEDIN="$(sanitize "$USER_LINKEDIN")"
RESUME_DIR="$(sanitize "$RESUME_DIR")"
RESUME_OUTPUT_DIR="$(sanitize "$RESUME_OUTPUT_DIR")"
JOB_SEARCH_LOCATION="$(sanitize "$JOB_SEARCH_LOCATION")"
JOB_SEARCH_KEYWORDS="$(sanitize "$JOB_SEARCH_KEYWORDS")"
JOB_SEARCH_MIN_SALARY="$(sanitize "$JOB_SEARCH_MIN_SALARY")"
JOB_SEARCH_MAX_AGE_DAYS="$(sanitize "$JOB_SEARCH_MAX_AGE_DAYS")"
USER_GENDER="$(sanitize "$USER_GENDER")"
USER_RACE="$(sanitize "$USER_RACE")"
USER_HISPANIC="$(sanitize "$USER_HISPANIC")"
USER_VETERAN="$(sanitize "$USER_VETERAN")"
USER_DISABILITY="$(sanitize "$USER_DISABILITY")"
USER_WORK_AUTH="$(sanitize "$USER_WORK_AUTH")"
USER_NEED_SPONSOR="$(sanitize "$USER_NEED_SPONSOR")"

# ── 2. Create directories ──────────────────────────────────────────────────────

WORKSPACE="$HOME/.openclaw/workspace/job_search"
SCRIPTS_DIR="$HOME/.openclaw/workspace/job_sub_agent/scripts"
CONFIG_DIR="$HOME/.openclaw/users/${OPENCLAW_USER}"

mkdir -p "$WORKSPACE"
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$RESUME_DIR"
mkdir -p "$RESUME_OUTPUT_DIR"

# ── 3. Write config.sh ────────────────────────────────────────────────────────

cat > "$CONFIG_DIR/config.sh" << EOF
# jobautopilot skill bundle — user config
# Generated by setup.sh on $(date +%Y-%m-%d)
# Edit any value here; re-run setup.sh to regenerate from scratch.
# This file is read-only by the agent. Nothing in it is sent to any network.

export OPENCLAW_USER="${OPENCLAW_USER}"
export OPENCLAW_PROFILE="apply"        # browser profile used for submitting applications

# Personal info
export USER_FIRST_NAME="${USER_FIRST_NAME}"
export USER_LAST_NAME="${USER_LAST_NAME}"
export USER_EMAIL="${USER_EMAIL}"
export USER_PHONE="${USER_PHONE}"
export USER_LINKEDIN="${USER_LINKEDIN}"

# File paths
export RESUME_DIR="${RESUME_DIR}"
export RESUME_OUTPUT_DIR="${RESUME_OUTPUT_DIR}"
export RESUME_TEMPLATE="\$HOME/.openclaw/workspace/job_sub_agent/scripts/sample_placeholders.docx"
export MD_TO_DOCX_SCRIPT="\$HOME/.openclaw/workspace/job_sub_agent/scripts/md_to_docx.py"
export TRACKER_PATH="\$HOME/.openclaw/workspace/job_search/job_application_tracker.md"
export JOB_SEARCH_TRACKER="\$TRACKER_PATH"  # alias used by search and tailor skills

# Search settings
export JOB_SEARCH_LOCATION="${JOB_SEARCH_LOCATION}"
export JOB_SEARCH_KEYWORDS="${JOB_SEARCH_KEYWORDS}"
export JOB_SEARCH_MIN_SALARY="${JOB_SEARCH_MIN_SALARY}"
export JOB_SEARCH_MAX_AGE_DAYS="${JOB_SEARCH_MAX_AGE_DAYS}"
export JOB_SEARCH_HANDOFF="\$HOME/.openclaw/workspace/job_search/SEARCH_AGENT_HANDOFF.md"

# EEOC defaults (supplied only to US job application forms on your request)
export USER_GENDER="${USER_GENDER}"
export USER_RACE="${USER_RACE}"
export USER_HISPANIC="${USER_HISPANIC}"
export USER_VETERAN="${USER_VETERAN}"
export USER_DISABILITY="${USER_DISABILITY}"
export USER_WORK_AUTH="${USER_WORK_AUTH}"
export USER_NEED_SPONSOR="${USER_NEED_SPONSOR}"
EOF

echo "✅  Config written to $CONFIG_DIR/config.sh"

# Restrict permissions — config contains PII (name, email, phone, EEOC fields)
chmod 600 "$CONFIG_DIR/config.sh"
echo "✅  Permissions set to owner-only (chmod 600)"

# ── 4. Copy tailor scripts to workspace ──────────────────────────────────────
# The tailor skill needs md_to_docx.py and its template in a shared workspace
# location. This is a local file copy — no network involved.
# Note: submitter scripts are used directly from the installed skill directory
# and do not need to be copied.

copy_script() {
  local src="$1" dst_dir="$2" label="$3"
  if [ -f "$src" ]; then
    if cp "$src" "$dst_dir/"; then
      echo "✅  Copied $label"
    else
      echo "⚠️   Failed to copy $label — check permissions on $dst_dir"
    fi
  else
    echo "⚠️   Source not found: $src"
    echo "     Re-run: clawhub install $(basename "$(dirname "$(dirname "$src")")")"
  fi
}

copy_script "$TAILOR_DIR/scripts/md_to_docx.py"                    "$SCRIPTS_DIR" "md_to_docx.py"
copy_script "$TAILOR_DIR/scripts/sample_placeholders.docx"          "$SCRIPTS_DIR" "sample_placeholders.docx"

# ── 5. Browser profiles (manual step) ────────────────────────────────────────
# Two isolated browser profiles keep job-site sessions separate from your
# personal browser. You can inspect or delete them at any time with:
#   openclaw browser profile list

echo ""
echo "==> Browser profiles needed: 'search' and 'apply'"
echo "    Create them manually if they don't exist:"
echo ""
echo "    openclaw browser profile create search"
echo "    openclaw browser profile create apply"
echo ""
echo "    (These are local browser profiles — not accounts or network services.)"
echo "    Check existing profiles: openclaw browser profile list"

# ── 6. Init tracker and handoff files ─────────────────────────────────────────

TRACKER="$WORKSPACE/job_application_tracker.md"
HANDOFF="$WORKSPACE/SEARCH_AGENT_HANDOFF.md"

if [ ! -f "$TRACKER" ]; then
cat > "$TRACKER" << 'EOF'
# Job Application Tracker

| Company | Title | Location | URL | Posted | Salary | Status | Notes |
|---------|-------|----------|-----|--------|--------|--------|-------|
EOF
  echo "✅  Tracker created at $TRACKER"
else
  echo "⏭   Tracker already exists — not overwritten"
fi

if [ ! -f "$HANDOFF" ]; then
  echo "# Search Agent Handoff" > "$HANDOFF"
  echo "✅  Handoff file created"
fi

# ── 7. Quick-start guide ──────────────────────────────────────────────────────

echo ""
echo "============================================================"
echo "  Setup complete! Quick-start guide:"
echo "============================================================"
echo ""
echo "  STEP 1 — Search for jobs"
echo "    Tell OpenClaw: 'Search for ${JOB_SEARCH_KEYWORDS} jobs'"
echo "    Agent reads your resume pool, searches job sites,"
echo "    and writes results to your tracker."
echo ""
echo "  STEP 2 — Tailor your resume"
echo "    Tell OpenClaw: 'Tailor my resume for the shortlisted jobs'"
echo "    Agent rewrites bullet points to match each JD,"
echo "    and saves .docx files to your output folder."
echo ""
echo "  STEP 3 — Submit applications"
echo "    Tell OpenClaw: 'Submit applications for all resume-ready jobs'"
echo "    Agent fills and submits forms for resume-ready jobs."
echo ""
echo "  Your config: $CONFIG_DIR/config.sh"
echo "  Tracker:     $TRACKER"
echo "  Outputs:     $RESUME_OUTPUT_DIR"
echo ""
echo "  To update your info later, edit config.sh directly"
echo "  or re-run: bash ~/.openclaw/workspace/skills/jobautopilot-bundle/setup.sh"
echo "============================================================"
