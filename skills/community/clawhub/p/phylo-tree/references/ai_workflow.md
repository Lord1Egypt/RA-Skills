# AI Workflow

## For AI Agents Using This Skill

**Goal:** Generate a scientific report without parsing log files.

---

## Step 1: Run Analysis

```bash
python3 scripts/run_v2.py --query "enzyme name" --output ./output
```

---

## Step 2: Generate JSON Summary

```bash
python3 scripts/generate_summary.py ./output
```

**Output:** `./output/analysis_summary.json`

---

## Step 3: Read Structured Data

```bash
# Read JSON summary
cat ./output/analysis_summary.json

# Read conclusions
cat ./output/conclusions.md
```

---

## Step 4: Use Report Template

**Template location:** `references/report_template.md`

**Fill in:**
- `{num_sequences}` from JSON
- `{num_species}` from JSON
- `{best_model}` from JSON
- `{support_percentage}` from JSON
- Key findings from `conclusions.md`

---

## Example JSON Structure

```json
{
  "iqtree": {
    "best_model": "Q.PFAM+R7",
    "log_likelihood": -53461.908,
    "num_sequences": 487
  },
  "support": {
    "high_support_percentage": 62.6
  },
  "taxonomy": {
    "num_species": 121,
    "top_genera": ["Escherichia", "Pseudomonas", "Klebsiella"]
  }
}
```

---

## No Need To:

- ❌ Parse IQ-TREE log files
- ❌ Parse MAFFT output
- ❌ Calculate statistics manually
- ❌ Extract support values from tree

**Everything is in JSON!**

---

## Report Generation Flow

```
Run analysis → Generate JSON → Read JSON + conclusions.md → Fill template → Done
```

**Time:** < 1 minute (after analysis completes)
