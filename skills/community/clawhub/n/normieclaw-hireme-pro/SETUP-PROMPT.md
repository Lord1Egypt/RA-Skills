# HireMe Pro — Setup Instructions

Welcome! Let's get HireMe Pro installed. Copy and paste this entire block into your agent's chat:

---

## Setup Prompt (Copy & Paste This)

```
I just purchased HireMe Pro. Please set it up for me by following these steps from the HireMe Pro package root (the folder that contains SKILL.md).
```

Your agent should then run the following steps:

### Step 1: Validate Package

```bash
set -euo pipefail

[ -f "./SKILL.md" ] || { echo "Error: Run this from the HireMe Pro package root."; exit 1; }
[ -f "./config/hireme-config.json" ] || { echo "Error: Missing ./config/hireme-config.json"; exit 1; }
[ -f "./scripts/generate-resume-pdf.sh" ] || { echo "Error: Missing ./scripts/generate-resume-pdf.sh"; exit 1; }

echo "✅ Package validated"
```

### Step 2: Copy Skill Files to Workspace

```bash
mkdir -p skills/hireme-pro/config skills/hireme-pro/scripts skills/hireme-pro/examples skills/hireme-pro/templates

cp "./SKILL.md" "skills/hireme-pro/SKILL.md"
cp "./config/hireme-config.json" "skills/hireme-pro/config/hireme-config.json"
cp "./scripts/generate-resume-pdf.sh" "skills/hireme-pro/scripts/generate-resume-pdf.sh"
cp "./examples/resume-tailoring.md" "skills/hireme-pro/examples/resume-tailoring.md"
cp "./examples/cover-letter-generation.md" "skills/hireme-pro/examples/cover-letter-generation.md"
cp "./examples/interview-prep.md" "skills/hireme-pro/examples/interview-prep.md"
cp "./templates/clean.html" "skills/hireme-pro/templates/clean.html"
cp "./templates/modern.html" "skills/hireme-pro/templates/modern.html"
cp "./templates/executive.html" "skills/hireme-pro/templates/executive.html"
cp "./templates/creative.html" "skills/hireme-pro/templates/creative.html"

echo "✅ Skill files copied"
```

### Step 3: Create Data Directories

```bash
mkdir -p skills/hireme-pro/data/resumes
mkdir -p skills/hireme-pro/data/tailored-versions
mkdir -p skills/hireme-pro/data/cover-letters
mkdir -p skills/hireme-pro/data/job-descriptions
mkdir -p skills/hireme-pro/data/interview-prep
mkdir -p skills/hireme-pro/data/negotiations

echo "✅ Data directories created"
```

### Step 4: Set Permissions

```bash
chmod 700 skills/hireme-pro/data skills/hireme-pro/data/resumes skills/hireme-pro/data/tailored-versions skills/hireme-pro/data/cover-letters skills/hireme-pro/data/job-descriptions skills/hireme-pro/data/interview-prep skills/hireme-pro/data/negotiations skills/hireme-pro/config skills/hireme-pro/scripts skills/hireme-pro/templates
chmod 600 skills/hireme-pro/config/hireme-config.json
chmod 700 skills/hireme-pro/scripts/generate-resume-pdf.sh

echo "✅ Permissions set"
```

### Step 5: Verify Installation

```bash
echo "=== HireMe Pro Installation Check ==="
echo ""
for f in SKILL.md config/hireme-config.json scripts/generate-resume-pdf.sh; do
  [ -f "skills/hireme-pro/$f" ] && echo "✅ $f" || echo "❌ MISSING: $f"
done
for d in data/resumes data/tailored-versions data/cover-letters data/job-descriptions data/interview-prep data/negotiations; do
  [ -d "skills/hireme-pro/$d" ] && echo "✅ $d/" || echo "❌ MISSING: $d/"
done
echo ""
which playwright > /dev/null 2>&1 && echo "✅ Playwright available" || echo "⚠️ Playwright not found — install with: pip3 install playwright && playwright install chromium"
echo ""
echo "=== Setup Complete ==="
```

### Step 6: Read SKILL.md and Start

After setup, the agent should read `skills/hireme-pro/SKILL.md` and confirm it's ready to build your resume. Just paste your experience, an old resume, or start chatting about your work history!

---

## What to Expect

After running the setup, your agent should confirm:
- ✅ SKILL.md copied to `skills/hireme-pro/`
- ✅ Config file in place at `skills/hireme-pro/config/hireme-config.json`
- ✅ Data directories created with proper permissions
- ✅ Scripts are executable
- ✅ Playwright is available (or instructions to install it)

Then your agent will greet you and start the resume intake process.

---

## Troubleshooting

- **"Run this from the HireMe Pro package root"** — Make sure your agent is in the directory containing the SKILL.md file from the download.
- **"Playwright not found"** — Run: `pip3 install playwright && playwright install chromium`
- **Permissions errors** — Run the chmod commands from Step 4 again.
- **Agent doesn't recognize the skill** — Make sure SKILL.md is at `skills/hireme-pro/SKILL.md` (check exact path).
