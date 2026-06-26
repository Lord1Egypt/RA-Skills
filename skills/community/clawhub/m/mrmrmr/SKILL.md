---
metadata: {"name": "mragent", "description": "LLM-powered automated Mendelian Randomization for causal discovery in biomedical research", "version": "0.2.5", "author": "MRAgent Team", "openclaw": {"requires": {"bins": ["python", "Rscript"], "env": ["OPENAI_API_KEY", "OPENGWAS_JWT"]}, "primaryEnv": "OPENAI_API_KEY", "category": "biomedical", "emoji": "🧬"}}
---

# MRAgent - Automated Mendelian Randomization Analysis Agent

## Description

MRAgent is an intelligent agent that automates the entire process of Mendelian randomization analysis for causal discovery in biomedical research. It:

1. **Knowledge Discovery Mode (KD)**: Given a disease (outcome), automatically scans PubMed literature to discover potential modifiable exposure (risk factor) that have correlation but no established causal inference, then performs comprehensive Mendelian randomization analysis using OpenGWAS data to identify novel causal relationships.

2. **Causal Validation Mode (CV)**: Directly test whether a user-specified exposure (e.g., "body mass index") has a causal effect on a specific outcome (e.g., "type 2 diabetes") using two-sample Mendelian randomization.

MRAgent handles all steps automatically:
- PubMed literature crawling
- LLM-based extraction of candidate exposure-outcome pairs
- Check for existing MR studies via PubMed search
- Optional STROBE-MR quality assessment of existing studies
- UMLS medical synonym expansion
- OpenGWAS database query for GWAS summary statistics
- LLM selection of most appropriate GWAS datasets
- Multiple MR methods: Inverse variance weighted, MR-Egger, weighted median, etc.
- Heterogeneity analysis and pleiotropy sensitivity testing
- MRlap correction for sample overlap
- Automatic generation of publication-ready PDF reports with LLM-written interpretation

## Requirements

- **Python** packages (install via `pip install -r {baseDir}/requirements.txt`)
- **R** language (>= 4.3.4) with the following packages installed:
  - `TwoSampleMR` - core Mendelian randomization
  - `ieugwasr` - OpenGWAS interface
  - `vcfR` - required for MRlap (optional)
  - `MRlap` - sample overlap correction (optional)
  - `jsonlite` - JSON processing (required for MRlap)
- `OPENAI_API_KEY` environment variable must be set (OpenAI API key)
- `OPENGWAS_JWT` environment variable (optional, for OpenGWAS access token)

## Usage

### Knowledge Discovery Mode (recommended for novel discoveries)

Discover novel causal relationships starting from a disease:

```bash
python {baseDir}/run_mragent.py --mode KD --outcome "back pain" --num-pubmed 100 --bidirectional
```

Discover novel causal relationships starting from an exposure:

(Currently the CLI implements KD starting from outcome; for exposure-based discovery use the Python API directly)

### Causal Validation Mode

Validate a specific hypothesis: does `exposure` causally affect `outcome`?

```bash
python {baseDir}/run_mragent.py --mode CV --exposure "body mass index" --outcome "type 2 diabetes"
```

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--mode KD\|CV` | **Required**. `KD`=knowledge discovery, `CV`=causal validation | `--mode CV` |
| `--outcome NAME` | **Required**. Outcome (disease) to study | `--outcome "back pain"` |
| `--exposure NAME` | Required in CV mode. Exposure factor to test | `--exposure "osteoporosis"` |
| `--num-pubmed N` | Number of papers to fetch from PubMed (default: 100) | `--num-pubmed 50` |
| `--model MR\|MR_MOE` | MR model type. `MR`=standard, `MR_MOE`=mixture of experts | `--model MR_MOE` |
| `--bidirectional` | Perform bidirectional analysis (also test outcome → exposure) | `--bidirectional` |
| `--no-synonyms` | Disable synonym expansion (faster) | `--no-synonyms` |
| `--strobe-mr` | Enable STROBE-MR quality assessment of existing studies | `--strobe-mr` |
| `--mrlap` | Enable MRlap sample overlap correction | `--mrlap` |
| `--output-dir DIR` | Output directory (default: `./output`) | `--output-dir /tmp/mragent-out` |
| `--steps 1,2,3` | Only run specific steps (for debugging/intervention) | `--steps 1,2` |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENGWAS_JWT` | Optional | OpenGWAS JWT access token |
| `LLM_MODEL` | No | LLM model name (default: `gpt-4o`) |
| `LLM_PROVIDER` | No | `openai` or `ollama` (default: `openai`) |
| `OPENAI_BASE_URL` | No | Custom base URL for OpenAI-compatible API |
| `MRAGENT_SOURCE_PATH` | No | Path to original MRAgent source if not installed globally |

## Output

MRAgent outputs a JSON summary to stdout with:
- `success`: boolean indicating success
- `output_directory`: directory containing all results
- `discovered_pairs`: number of candidate exposure-outcome pairs found
- `selected_for_mr`: number of pairs selected for MR analysis
- `reports`: list of paths to generated PDF files (Report.pdf, Introduction.pdf, Conclusion.pdf, etc.)

Example output:
```json
{
  "success": true,
  "mode": "CV",
  "outcome": "back pain",
  "exposure": "osteoarthritis",
  "output_directory": "./output/osteoarthritis_back_pain_gpt-4o",
  "discovered_pairs": 1,
  "selected_for_mr": 1,
  "reports": [
    "./output/osteoarthritis_back_pain_gpt-4o/osteoarthritis_back_pain/Introduction.pdf",
    "./output/osteoarthritis_back_pain_gpt-4o/osteoarthritis_back_pain/osteoarthritis_back_pain/MR_ieu-a-2_ieu-a-1008/Report.pdf",
    "./output/osteoarthritis_back_pain_gpt-4o/osteoarthritis_back_pain/Conclusion.pdf"
  ]
}
```

## Workflow Steps

When running all steps (default):

| Step | Description |
|------|-------------|
| 1 | Crawl PubMed, extract candidate exposure-outcome pairs |
| 2 | Check if each pair already has MR studies in literature |
| 3 | Extract unique terms, expand with medical synonyms |
| 4 | Check which terms have available GWAS data in OpenGWAS |
| 5 | LLM selects most appropriate GWAS IDs for each term |
| 6 | Generate all combinations of exposure-outcome pairs |
| 7 | Check new combinations for existing MR studies |
| 8 | Select final set of novel pairs for analysis |
| 9 | Run MR analysis, generate plots and LLM-interpreted PDF reports |

## Notes

- This is a computationally intensive process. The full analysis can take tens of minutes to hours depending on the number of pairs.
- All intermediate results are saved as CSV files in the output directory, allowing manual editing and intervention between steps.
- MRAgent requires R to be installed with the necessary packages, because the actual MR analysis is performed by R's TwoSampleMR package.
