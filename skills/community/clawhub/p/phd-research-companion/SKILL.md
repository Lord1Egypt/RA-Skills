# PhD Research Companion v1.5.0

Professional full-stack research management skill for Computer Science PhD students, providing complete automated support from project initialization to journal submission with scientific traceability compliance.

## 🎯 Overview & Purpose

This comprehensive skill transforms the fragmented, manual process of academic research into a streamlined, trackable workflow that ensures every step meets publication standards and maintains an audit trail for reproducibility and scientific integrity.

### What It Solves
- **Literature saturation**: Systematically gather, organize, and analyze papers from multiple sources
- **Experiment design gaps**: Ensure baseline comparisons, ablation studies, and robustness tests are comprehensive  
- **Revision tracking loss**: Maintain detailed records of 6-8 improvement cycles before submission
- **Math notation inconsistencies**: Automate proof verification and symbol consistency checks
- **Submission readiness**: Validate all requirements before advisor or journal review

## 🏗️ Architecture Overview

```
phd-research-companion/
├── init_research_project.py         # Entry point - creates full research environment
├── run                              # Quick CLI wrapper for all commands  
├── scripts/                         # Core analysis & generation tools
│   ├── multi_source_search.py      # Literature collection (arXiv, SemanticScholar, DBLP)
│   ├── paper_analyzer.py           # Deep extraction of contributions/methodology  
│   ├── create_experiment_design.py # Comparison/ablation/robustness YAML configs
│   ├── generate_latex_template.py  # IEEE/ACM/NeurIPS templates with proper structure
│   ├── revision_tracker.py         # Track improvement rounds systematically
│   ├── verify_math_notation.py     # Mathematical proof consistency validator  
│   └── check_compliance.py         # Final submission readiness checker
├── references/                      # Best practices & documentation
└── SKILL.md                        # This comprehensive guide
```

## 🚀 Quick Start Guide

### Installation & Setup

```bash
# Clone or copy skill to workspace
cd /home/user/workspace/skills/phd-research-companion

# Make run script executable (one-time setup)  
chmod +x run

# Verify installation
./run --version
```

### Initialize Your Research Project

```bash
# Method 1: Interactive wrapper (recommended)  
./run init -d "machine unlearning with certified forgetting guarantees" \
            -j "IEEE TIFS" \
            -o ./my-research-project-2024

# Method 2: Direct Python execution
python3 init_research_project.py --domain "Your Research Topic"
```

**Output created:**
```
research-project-2024/
├── 00-dashboard/                    # Project overview & tracking
├── 01-literature-survey/           # BibTeX, PDFs, analysis outputs
├── 02-methodology-dev/             # Theorems, formal proofs  
├── 03-paper-drafting/              # LaTeX templates, drafts  
├── 04-experiments/                 # Designs (YAML), results archive  
├── 05-revision-rounds/             # Systematic improvement tracking  
├── 06-collaboration/               # Advisor feedback, peer reviews  
└── 07-audit-trail/                 # Scientific traceability evidence
```

---

## 📚 Complete Module Reference

### 1️⃣ Multi-Source Literature Search (`scripts/multi_source_search.py`)

Automatically collect papers from arXiv, Semantic Scholar, DBLP with deduplication and citation export.

#### Basic Usage
```bash
# Quick search (foreground - instant feedback)  
./run search -q "machine unlearning differential privacy" -l 30

# Background execution for large searches 
./run search -q "federated learning security" \
             --sources arxiv semanticscholar \
             -l 50 \
             -o ./my-project/01-literature-survey \
             --background
```

#### Advanced Filters
```bash
# Temporal filtering with keyword constraints  
./run search \
    -q "adversarial robustness certified defenses" \
    --from-year 2020 --to-year 2024 \
    --sources arxiv,ieee\dblp \
    -l 75

# Output: search-results-20240310.bibtex + search-summary.md
```

#### Background Monitoring
```bash
# Terminal 1: Start background task  
./run search -q "topic" --background -o ./results &

# Terminal 2: Monitor progress (real-time)
watch -n 5 'cat results/search-progress-search.json'

# Check completed status after finish
cat results/search-progress-search.json | grep '"summary"'
```

**Files Generated:**
- `search-results-{timestamp}.bibtex` → Import-ready citations for Zotero/Mendeley  
- `search-summary-{timestamp}.md` → Human preview with top 10 papers
- `search-progress-{taskid}.json` → Background tracking metadata

---

### 2️⃣ Paper Analysis & Deep Extraction (`scripts/paper_analyzer.py`)  

Extract key contributions, methodology components, and mathematical formalisms from downloaded papers.

#### Modes Available

**Deep Mode** (10-30 minutes for batch of 50+ papers)  
```bash
./run analyze -i ./my-project/01-literature-survey/*.pdf --mode deep --background

# Output per paper: analysis-{filename}.md with sections:
#   - Key innovations extracted  
#   - Methodology components mapped
#   - Mathematical definitions identified
#   - Limitations noted
```

**Quick Mode** (2-5 minutes for fast overview)  
```bash
./run analyze -i ./papers/*.pdf --mode quick

# Fast metadata extraction: title, authors, venue, year only
```

#### Batch Analysis with Progress Tracking
```bash
# Start background analysis of 100 papers
./run analyze \
    -i "./literature/*.pdf" \
    --mode deep \
    -o ./analysis-output \
    --background &

# Monitor in another terminal:
while [ -f ./analysis-output/analysis-progress-analysis.json ]; do 
    sleep 10
    cat ./analysis-output/analysis-progress-analysis.json | jq '.{progress_percent,total_papers,stage}'
done
```

**Comparison Report Generated:**
- `analysis-comparison-report.md` → Matrix of all papers with side-by-side comparisons

---

### 3️⃣ Experimental Design Generation (`scripts/create_experiment_design.py`)

Create reproducible experiment specifications in YAML format covering three key categories required for top-tier publications.

#### A) Baseline Comparison Experiments  
```bash
./run experiment \
    --type comparison \
    --datasets "CIFAR-10,Fashion-MNIST,CelebA" \
    --baselines "Retraining,SISA,NAU,Certificate-based,MF-GAN" \
    --metrics "test_accuracy,fps,latency_ms,gdpa_certificates" \
    -o ./my-project/04-experiments/design-baseline

# Output: experiment-comparison-design.yaml + report.md with:
#   - Dataset specifications (split sizes, class distributions)  
#   - Baseline paper citations and implementation references
#   - Evaluation metrics with formulas
#   - Expected compute time & GPU requirements
```

#### B) Ablation Studies  
```bash  
./run experiment \
    --type ablation \
    --components "privacy_layer,adversarial_training,noising_mechanism" \
    --base_model "ResNet-18" \
    -o ./experiments/ablation-studies

# Documents: What happens when each component is removed?  
#   Proves necessity and contribution of novel contributions
```

#### C) Robustness Stress Tests  
```bash  
./run experiment \
    --type robustness \
    --attack_types "FGSM,BIM,PGD,L0_attack" \
    --perturbation_budgets "eps=0.3,epsilon_norms=L2:Linf:8:16:32" \
    -o ./experiments/robustness-verification

# Validates: Defense effectiveness under adversarial pressure  
```

---

### 4️⃣ LaTeX Template Generation (`scripts/generate_latex_template.py`)

Generate conference/journal-ready templates with proper formatting for IEEE, ACM, NeurIPS, ICLR.

#### IEEE TIFS (Transactions)
```bash
./run template \
    --journal "IEEE-TIFS" \
    --title "Certified Machine Unlearning with Adversarial Robustness Guarantees" \
    -a "Your Name" "Coauthor Name" \
    -e "your@email.edu" "coauthor@university.edu"  
```

#### ACM Transactions on Information Systems (TISSEC)  
```bash
./run template \
    --journal "ACM-TISSEC" \
    --title "Privacy-Preserving Federated Learning Against Membership Inference Attacks" \
    -a "Lead Author" \
    --generate-empty-citations "true"  # Pre-populate with placeholder citations
```

#### NeurIPS Conference Format  
```bash
./run template \
    --journal "NeurIPS" \
    --year 2024 \
    --anonymous "true"  # Double-blind submission preparation  
```

**Key Features:**
- ✅ Proper bibliography support (biblatex with IEEEtran/ACM styles)
- ✅ Figure placement guidelines (`[htbp]` with positioning notes)
- ✅ Abstract, introduction, conclusion structure scaffolding
- ✅ Theorem/enumerate environments configured for proofs
- ✅ References section with placeholder citations ready

---

### 5️⃣ Revision Round Tracking (`scripts/revision_tracker.py`)

Systematically document every improvement round (6-8 cycles typical) before final submission.

#### Add Revision Round Entry
```bash
./run revision \
    --action add_round \
    -r 2 \
    -i "Weak baseline comparison missing; Theorem proofs incomplete; Figure quality needs enhancement" \
    -x "Added SOTA baselines (3 new); Strengthened Lemma 4 proof with additional steps; Redraw all figures in TikZ for consistency"  
    --evidence "./05-revision-rounds/round2-changes.diff" \
    -a "Advisor: Dr. Smith, PhD Student: Zhang"
```

#### Generate Revision Timeline Report
```bash  
./run revision --generate-timeline  

# Creates detailed markdown showing:
#   Round 1 → Issues identified [5] | Fixes applied [4] | Evidence file paths  
#   Round 2 → ...  
#   Summary: Total issues resolved, major improvements timeline graph
```

#### Track Specific Issue Resolution
```bash
./run revision \
    --issue-id "ABS-2024-03" \
    --status resolved \
    -x "Fixed abstract to better motivate problem significance and highlight key contributions"
```

---

### 6️⃣ Mathematical Notation Verification (`scripts/verify_math_notation.py`)

Automate detection of undefined symbols, inconsistent notation, or missing proofs.

#### Full Scan  
```bash
./run math \
    --input "./03-paper-drafting/main-paper.tex" \
    --verbose

# Output: Symbol consistency report  
#   - Undefined in LaTeX preamble but used in theorem statements  
#   - Conflicting notation (e.g., bold vs italic for random variables)
#   - Missing proof references for cited theorems
```

#### Specific Checks
```bash
./run math --file "theorems.tex" --check-inconsistency-only
```

---

### 7️⃣ Final Compliance Check (`scripts/check_compliance.py`)

Run systematic verification before advisor review or journal submission.

#### Full Audit  
```bash
./run check --project-dir ./my-research-project

# Checks:
#   ☑ Literature survey comprehensive (≥50 papers with citation coverage)  
#   ☜ Experimental design complete (comparisons + ablations + robustness)
#   ☑ LaTeX structure meets journal standards  
#   ☑ Revision rounds ≥6 documented with evidence links 
#   ☜ Mathematical proofs complete and consistent  
#   ☑ All figures high-resolution (≥300 DPI for IEEE TIFS requirement)
```

#### Generate Submission Readiness Report
```bash  
./run check --project-dir ./my-project --report-format compliance-audit  

# Creates PDF report with checklist completion status + recommendations
```

---

## 🛠️ Automation & Integration

### Daily Literature Watch Updates
Set up cron job for continuous domain monitoring:

```bash
cd /home/user/workspace/skills/phd-research-companion/scripts
crontab -e

# Add daily at 8 AM (local time)
0 8 * * * python multi_source_search.py \
    -q "your research topic" \
    -l 5 \
    --sources arxiv \
    > /dev/null  
```

### Bash Automation Wrapper Example
```bash
#!/bin/bash
# Full PhD pipeline automation for research assistant

TOPIC="machine unlearning certified forgetting"
PROJECT_DIR="./my-project-$TOPIC-slug"

echo "🚀 Starting automated PhD workflow..."

./run init -d "$TOPIC" -j "IEEE TIFS" -o $PROJECT_DIR
cd $PROJECT_DIR

# Stage 1: Literature (background)  
../scripts/multi_source_search.py -q "$TOPIC" --sources arxiv semanticscholar -l 30 \
    -o 01-literature-survey/ --background &

sleep 2

echo "Literature search running in background..."

# Stage 2: LaTeX template while waiting  
../scripts/generate_latex_template.py --journal "IEEE-TIFS" \
    -t "$TOPIC (formatted title)" \
    -a "Your Name" \
    -o 03-paper-drafting/

echo "Template created. Waiting for literature to complete..."

# Check when literature finishes  
until [ ! -f "01-literature-survey/search-progress-search.json" ]; do 
    sleep 30
done

# Next: Analyze papers found  
../scripts/paper_analyzer.py --mode deep \
    -i "01-literature-survey/*.pdf" \
    -o 02-analysis/

echo "All stages completed. Open dashboard to review:"
open 00-dashboard/index.html
```

---

## 🔍 Troubleshooting

### Literature Search Issues
```bash
# If no papers found, try broader query or reduce year filter
./run search -q "unlearning" --from-year 2019 -l 50

# Check sources availability  
curl "http://export.arxiv.org/api/query?search_query=all:machine_learning&max_results=1"

# Verify output directory write permissions  
ls -la ./01-literature-survey
```

### LaTeX Compilation Errors
```bash
# Common fix: Install missing packages or update template macros
sudo apt-get install texlive-latex-recommended texlive-science

# Verify template syntax
pdflatex --interaction=nonstopmode 03-paper-drafting/paper.tex 2>&1 | less 
```

---

## 📊 Status & Maintenance Information

**Version:** 1.5.0 (March 2026)  
**Tested With:** Python 3.8+, IEEE LaTeX template v2.4, arXiv API v2  
**Supported Venues:** IEEE TIFS/TIP/TKDE, ACM TISSEC/CSUR, NeurIPS/ICLR/AAAI  

### Update Check
```bash
# Check for newer versions online
curl -s https://api.github.com/repos/openclaw/phd-research-companion/releases/latest | jq '.tag_name'

# Compare local version
grep "Version:" run
```

---

## 📬 Support & Attribution

**OpenClaw AI Lab Research Tools**  
This skill is released under MIT License for academic research purposes.  

**For questions:**  
- Review SKILL.md examples in this directory  
- Check individual script `--help` documentation  
- Contact: research-tools@openclaw.ai (not affiliated with any specific university)

---
*Designed for reproducible, traceable science in Computer Science PhD research programs.*