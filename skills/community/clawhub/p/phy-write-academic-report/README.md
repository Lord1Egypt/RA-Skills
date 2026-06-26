# write-academic-report

**Claude Code skill** that writes 40-100+ page academic reports (FYP, thesis, dissertation) using parallel subagents — **3-4x faster** than sequential writing.

> Research repo in → compiled LaTeX thesis out. 86 pages in ~6 hours, validated.

## What it does

Point it at your research repo. It launches parallel agents to extract data, write chapters simultaneously, compile LaTeX, and audit cross-references:



```
Wave 0: Data Preparation    Wave 1: Chapter Writing    Wave 2: Assembly
(5-6 parallel agents)       (3-4 parallel agents)      (sequential)

Codebase analysis            Ch1-2 (Intro + Lit Review)  Merge chapters
Experiment data              Ch3 (Methodology)           Cross-ref audit
Statistics                   Ch4-5 (Setup + Results)     Compile (tectonic)
Figure generation            Ch6 (Conclusion)            Quality review
```

**3-4x faster** than sequential writing. Validated on an 86-page FYP report produced in ~6 hours.

## Install

### As a Claude Code skill

```bash
# Copy to your skills directory
cp -r . ~/.claude/skills/write-report/

# Or symlink
ln -s $(pwd) ~/.claude/skills/write-report
```

### Dependencies

```bash
# LaTeX compiler (required)
brew install tectonic    # macOS
# Or: cargo install tectonic

# Python 3.10+ for scripts (included)
pip install requests   # for citation_checker.py
python3 scripts/cross_ref_audit.py --help
python3 scripts/citation_checker.py --help
```

## Usage

Invoke with `/write-report` in Claude Code, or describe your report needs and the skill will be suggested.

### Quick start

1. Have your research repo with code + results ready
2. Tell Claude: "Write my FYP report based on this repo"
3. Claude will execute the 3-wave pipeline automatically

### Citation verification

Verify all citations against 3 academic databases before submission. Catches AI-hallucinated references (6-55% of AI-generated citations are fabricated):

```bash
# Check all .bib files
python3 scripts/citation_checker.py path/to/report/

# JSON output for CI
python3 scripts/citation_checker.py references.bib --json
```

Cascading pipeline: CrossRef (140M+ DOIs) -> Semantic Scholar (200M+ papers) -> OpenAlex (240M+ works). Detects fully fabricated, chimeric (blended), and modified-real hallucinations.

### Cross-reference audit

After parallel agents write chapters, catch duplicate labels:

```bash
python3 scripts/cross_ref_audit.py path/to/report/
```

## What's included

```
write-academic-report/
  SKILL.md                              # Main skill definition
  README.md                             # This file
  references/
    writing-guide.md                    # Academic writing philosophy
    citation-workflow.md                # Citation verification pipeline
    compilation-guide.md                # LaTeX compilation (tectonic, latexmk)
    parallel-pipeline.md                # Wave architecture documentation
  templates/
    university-thesis/                  # Generic thesis LaTeX template
      main.tex                          # Master document
      preamble.tex                      # Shared packages + macros
      front_matter.tex                  # Title, abstract, acknowledgements
      chapters/ch{1-6}_*.tex            # Chapter templates with labels
      appendices/appendix_a.tex         # Appendix template
      references.bib                    # Bibliography
  scripts/
    citation_checker.py                 # Multi-source citation verifier (CrossRef + S2 + OpenAlex)
    cross_ref_audit.py                  # Cross-reference + duplicate label checker
```

## Writing philosophy

Inherited from [ml-paper-writing](https://github.com/Orchestra-Research/ml-paper-writing):

- **Narrative Principle** (Nanda): One story, one contribution, surgical precision
- **Sentence Clarity** (Gopen & Swan): 7 principles of reader expectations
- **Word Choice** (Lipton, Steinhardt): Specific, confident, consistent
- **Citation Safety**: Never hallucinate references. Always fetch programmatically.

Adapted for thesis:
- 40-100+ pages vs 8-12 page conference papers
- Full Literature Review chapter vs Related Work section
- Project schedule / Gantt chart
- Honest limitations (Claude undersells by default)

## Key lessons

1. **Data before prose** -- agents write poorly without concrete numbers
2. **Cross-ref audit is mandatory** -- parallel agents create duplicate labels
3. **Figure pipeline separate** -- generate all figures first, reference later
4. **Tectonic over BasicTeX** -- no sudo, handles packages automatically
5. **Label naming convention** -- use chapter prefixes: `fig:ch3:architecture`

## License

MIT
