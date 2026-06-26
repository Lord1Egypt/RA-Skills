# Protein Family Phylogenetic Analysis - Implementation Guide

## For AI Agents

This skill provides a complete workflow for protein family evolutionary analysis. When a user requests phylogenetic analysis:

1. **Read SKILL.md** - Understand the workflow
2. **Check dependencies** - Ensure tools are installed
3. **Run workflow** - Execute scripts in order
4. **Generate report** - Create publication-ready document

## Quick Implementation

```bash
# Full workflow (one command)
bash scripts/run_full_workflow.sh sequences.fasta output/ "Family Name"

# Or step-by-step
bash scripts/01_quality_control.sh sequences.fasta output/qc/
bash scripts/02_conservation.sh output/qc/final.fasta output/conservation/
bash scripts/03_coevolution.sh output/qc/final.fasta output/coevolution/
bash scripts/04_phylogeny.sh output/qc/final.fasta output/phylogeny/
bash scripts/05_visualize.sh output/ output/figures/
bash scripts/06_report.sh output/ "Family Name" output/report.md
```

## Key Scripts

All scripts are in `scripts/` directory:
- `run_full_workflow.sh` - Complete pipeline
- `01_quality_control.sh` - 8-stage QC
- `02_conservation.sh` - Shannon entropy analysis
- `03_coevolution.sh` - NMI coevolution network
- `04_phylogeny.sh` - IQ-TREE maximum likelihood
- `05_visualize.sh` - Publication figures (17 plots)
- `06_report.sh` - Markdown report generation

## Key References

Load these as needed:
- `references/01-quality-control.md` - Detailed QC methodology
- `references/02-conservation.md` - Conservation analysis
- `references/03-coevolution.md` - Coevolution networks
- `references/04-phylogeny.md` - Phylogenetic methods
- `references/05-visualization.md` - Figure generation
- `references/06-report.md` - Report structure

## Common Patterns

### Pattern 1: User provides FASTA file

```
User: "Analyze these protein sequences [file.fasta]"

Agent:
1. Save file to workspace
2. Run: bash scripts/run_full_workflow.sh file.fasta output/ "Protein Family"
3. Monitor progress
4. Present results
```

### Pattern 2: User wants specific analysis

```
User: "Find conserved residues in these sequences"

Agent:
1. Run QC first: bash scripts/01_quality_control.sh input.fasta qc/
2. Run conservation: bash scripts/02_conservation.sh qc/final.fasta conservation/
3. Report conserved positions
```

### Pattern 3: User wants publication report

```
User: "Create a publication-ready phylogenetic analysis report"

Agent:
1. Run full workflow
2. Generate Feishu document:
   lark-cli docs +create --title "Analysis" --markdown "@output/report.md"
3. Upload figures:
   for fig in output/figures/*.png; do
     lark-cli docs +media-insert --doc <doc_id> --file $fig
   done
```

## Error Handling

### Script fails at QC stage
- Check input FASTA format
- Verify CD-HIT installed
- Try relaxed parameters

### Phylogeny takes too long
- Use `-fast` mode in IQ-TREE
- Reduce bootstrap replicates
- Check sequence count (> 1000 may be slow)

### Figures don't generate
- Check Python dependencies (matplotlib, seaborn)
- Verify intermediate files exist
- Check file permissions

## Token Optimization

**Don't read scripts unless:**
- User asks for customization
- Script fails and needs debugging
- Parameters need adjustment

**Progressive loading:**
1. Start with SKILL.md (workflow overview)
2. Load specific reference only when needed
3. Execute scripts without reading (trust they work)

## Customization

Users may request:
- Different CD-HIT threshold → Edit `scripts/01_quality_control.sh`
- Alternative phylogeny method → See `references/04-phylogeny.md`
- Custom figure style → Edit `scripts/05_visualize.sh`
- Different report format → Edit `scripts/06_report.sh`

## Success Criteria

Analysis is complete when:
- ✅ QC reduces sequences to high-quality subset
- ✅ Conservation identifies < 20% highly conserved positions
- ✅ Coevolution finds hub residues
- ✅ Phylogeny has bootstrap convergence > 0.99
- ✅ All 17 figures generated (300 DPI)
- ✅ Report includes all sections with results

## Example Output Structure

```
output/
├── qc/
│   ├── final.fasta (high-quality sequences)
│   └── qc_report.json (statistics)
├── conservation/
│   ├── conservation.csv (entropy per position)
│   └── conserved_positions.txt (H < 0.3)
├── coevolution/
│   ├── coevolution_pairs.csv (MI scores)
│   └── hub_positions.txt (top hubs)
├── phylogeny/
│   ├── tree.treefile (ML tree)
│   ├── tree.contree (bootstrap consensus)
│   └── tree.iqtree (full log)
├── figures/
│   ├── figure_01_workflow.png
│   ├── figure_02_conservation.png
│   └── ... (17 total)
└── report.md (complete analysis)
```

## Based on Real Project

This skill is based on successful analysis of example protein family:
- Input: 1,000 sequences
- Output: 100 high-quality sequences
- Results: 32 conserved positions, 9,552 coevolved pairs, 0.992 bootstrap convergence
- Time: ~2 hours total
- Publication-ready: Yes

## Notes for Skill Maintenance

When updating this skill:
1. Test on diverse protein families (enzymes, receptors, transporters)
2. Validate against published phylogenies
3. Ensure all scripts have error handling
4. Keep references concise (< 10k words each)
5. Update citations when tools are updated
