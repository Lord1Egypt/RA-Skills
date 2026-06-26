# 🎓 PhD Research Companion v1.5.0

**Full-Stack Academic Research Management for Computer Science PhD Students**

---

## ⚡ Quick Start (3 Commands)

```bash
# 1️⃣ Clone & initialize project  
./run init -d "machine unlearning" -j "IEEE TIFS"

# 2️⃣ Auto literature search (background execution enabled)  
./run search -q "certified forgetting differential privacy" -l 30

# 3️⃣ Generate IEEE LaTeX template ready for writing
./run template --journal "IEEE-TIFS" -t "Your Paper Title" -a "Author Name"
```

---

## 🛠️ Available Commands

| Command | Purpose | Example |  
|---------|------|--------|  
| `init` / `project` | Create full research directory structure | `./run init -d "topic here"` |  
| `search` / `lit` | Auto-discover papers (arXiv, Semantic Scholar) | `./run search -q "federated learning"` |  
| `analyze` / `papers` | Extract contributions & methodology from PDFs | `./run analyze -i ./literature/*.pdf --mode deep` |
| `experiment` / `exp` | Generate comparison/ablation/robustness YAML configs | `./run exp --type ablation` |  
| `template` / `latex` | Create IEEE/ACM/NeurIPS LaTeX templates | `./run template --journal "NeurIPS"` |  
| `revision` / `track` | Document 6-8 improvement rounds | `./run revision -r 1 -i "issues fixed"` |  
| `math` / `symbols` | Verify mathematical notation consistency | `./run math --input ./03-paper-drafting/main.tex` |  
| `check` / `compliance` | Final pre-submission audit | `./run check --project-dir ./my-project`  

---

## 📖 Detailed Documentation

See **[SKILL.md](./SKILL.md)** for:
- 7-module comprehensive guide (5000+ words)
- All command examples with advanced parameters  
- Background execution & progress monitoring setup
- Bash automation pipeline templates
- Troubleshooting common issues

---

## 📦 Project Structure After `init`

```
my-research-project/
├── 00-dashboard/              # Overview & tracking dashboard  
├── 01-literature-survey/      # BibTeX + PDFs + analysis outputs  
├── 02-methodology-dev/        # Theorem formalization & proofs  
├── 03-paper-drafting/         # LaTeX drafts (IEEE/ACM templates)
├── 04-experiments/            # YAML experiment designs + results archive  
├── 05-revision-rounds/        # Systematic improvement tracking (6-8 cycles)  
├── 06-collaboration/          # Advisor feedback & peer reviews  
└── 07-audit-trail/            # Scientific traceability evidence
```

---

## ⚙️ Background Execution & Automation

### Literature Search in Background
```bash
./run search -q "topic" --background -o ./my-search &
watch -n 5 'cat my-search/search-progress-search.json'
```

### Cron Job for Daily Updates  
```bash
# Edit crontab: crontab -e
# Add: 0 8 * * * /path/to/run search --background -q "your_topic" > /dev/null
```

See **SKILL.md** Section 1 & 6 for complete automation setup.

---

## ✨ Unique Features

✅ **Scientific Traceability**: Every experiment, revision, and proof tracked with timestamps  
✅ **Multi-Source Literature**: arXiv + Semantic Scholar + DBLP automatic aggregation with deduplication  
✅ **Revision Rounds Systematic Tracking**: Document 6-8 improvement cycles (standard IEEE/ACM process)  
✅ **LaTeX Templates for Major Venues**: IEEE TIFS/TIP, ACM TISSEC/CSUR, NeurIPS/ICLR pre-formatted  
✅ **Background Execution Ready**: All long-running tasks support progress file monitoring  

---

## 🖥️ System Requirements

- **Python**: 3.8+ (only stdlib + common packages: `requests`, `PyPDF2`)
- **LaTeX Engine**: TeX Live or MacTeX with IEEEtran/ACM article classes  
- **Disk Space**: ~500 MB for typical literature collection (adjustable)

---

## 📄 License & Attribution

**MIT License** — Open source academic research tool  
By **OpenClaw AI Lab** — Research automation solutions  

This skill is independent and not affiliated with any specific university or institution. Designed to support reproducible, traceable scientific practice in Computer Science PhD programs worldwide.

---

## 🆘 Quick Help

```bash
# Show all commands with examples  
./run help

# Debug an error in literature search  
python3 scripts/multi_source_search.py --help

# Check LaTeX compilation step-by-step  
pdflatex 03-paper-drafting/paper.tex 2>&1 | less 
```

---
*Last updated: March 2026 • Designed for systematic PhD research excellence*