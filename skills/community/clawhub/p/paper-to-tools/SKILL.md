---
name: paper-to-tools
description: |
  Paste a paper abstract or methods section → get matched AI agent tools
  that can reproduce the analysis. Maps methodology keywords to 131+
  curated science agents from the Claw4Science directory.
  Trigger words: "reproduce this paper", "what tools for this method",
  "find agents for this analysis", "replicate methodology",
  "paper to tools", "which agent can do this".
---

# Paper-to-Tools: Match Research Methods to AI Agents

> Paste a paper abstract or methods section. Get a list of AI agents and skills that can help you reproduce or extend the analysis.

## How It Works

1. User pastes a paper abstract, methods section, or describes an analysis pipeline
2. You extract methodology keywords (techniques, databases, data types, tools mentioned)
3. You match keywords against the mapping table below
4. You return 2-5 matched agents with installation instructions and links

## Keyword-to-Agent Mapping

### Sequence & Genomics
| Keywords | Agent | Stars | What It Does |
|----------|-------|-------|-------------|
| BLAST, sequence alignment, homology | [BioClaw](https://claw4science.org/#project-runchuan-bu-bioclaw) | 318 | PubMed search + PyMOL visualization, built-in BLAST skill |
| RNA-seq, differential expression, DESeq2 | [OmicsClaw](https://claw4science.org/#project-tiangzlab-omicsclaw) | 114 | Multi-omics AI agent, scRNA-seq preprocessing |
| single-cell, scRNA-seq, clustering, trajectory | [OmicsClaw](https://claw4science.org/#project-tiangzlab-omicsclaw) | 114 | Single-cell analysis pipeline |
| CRISPR, gene editing, guide RNA | [CRISPR-GPT](https://claw4science.org/#project-cong-lab-crispr-gpt-pub) | 156 | CRISPR experiment design |
| spatial transcriptomics, visium, MERFISH | [SpatialAgent](https://claw4science.org/#project-genentech-spatialagent) | 158 | Spatial omics analysis from Genentech |
| genome, variant calling, WGS, WES | [BioMaster](https://claw4science.org/#project-ai4nucleome-biomaster) | 91 | Nucleome-scale genomic analysis |

### Drug Discovery & Chemistry
| Keywords | Agent | Stars | What It Does |
|----------|-------|-------|-------------|
| molecular docking, binding affinity, protein-ligand | [BloClaw](https://claw4science.org/#project-qinheming-bioclaw) | 1 | RDKit + ESMFold + molecular docking pipeline |
| drug-target interaction, ADMET, pharmacology | [DrugClaw](https://claw4science.org/#project-qsong-github-drugclaw) | 118 | 57 skills for DTI, ADR, DDI, drug repurposing |
| drug discovery, virtual screening | [AIAgents4Pharma](https://claw4science.org/#project-virtualpatientengine-aiagents4pharma) | 76 | End-to-end pharma AI agents |
| RDKit, SMILES, molecular descriptors | [ChemClaw](https://claw4science.org/#project-ai4chem-chemclaw) | 32 | Chemistry AI agent |
| molecular dynamics, MD simulation | [MDCrow](https://claw4science.org/#project-ur-whitelab-mdcrow) | 234 | Molecular dynamics agent |
| PyMOL, molecular visualization, protein structure | [PyMolClaw](https://claw4science.org/#project-junior1p-pymolclaw) | 1 | 13 PyMOL scripts for publication figures |
| TCM, traditional chinese medicine, network pharmacology | [TCM-Agent](https://claw4science.org/#project-aitcm-tcm-agent) | 10 | TCM network pharmacology analysis |

### Protein & Structure
| Keywords | Agent | Stars | What It Does |
|----------|-------|-------|-------------|
| protein folding, AlphaFold, ESMFold, structure prediction | [BloClaw](https://claw4science.org/#project-qinheming-bioclaw) | 1 | De novo 3D folding via ESMFold |
| protein-protein interaction, PPI network | [BioDiscoveryAgent](https://claw4science.org/#project-snap-stanford-biodiscoveryagent) | 102 | Stanford bio discovery agent |

### Research Automation
| Keywords | Agent | Stars | What It Does |
|----------|-------|-------|-------------|
| literature review, systematic review, PubMed | [BioClaw](https://claw4science.org/#project-runchuan-bu-bioclaw) | 318 | PubMed integration |
| autonomous research, end-to-end | [AutoResearchClaw](https://claw4science.org/#project-aiming-lab-autoresearchclaw) | 10608 | Fully autonomous research pipeline |
| research agent, idea to paper | [EvoScientist](https://claw4science.org/#project-evoscientist-evoscientist) | 2918 | Evolutionary scientific discovery |
| paper writing, manuscript | [Research Paper Writing Skills](https://claw4science.org/skill-hubs) | 1109 | ML/CV/NLP paper writing skills |
| data analysis, statistics, visualization | [RD-Agent](https://claw4science.org/#project-microsoft-rd-agent) | 12372 | Microsoft's research & development agent |

### Clinical & Medical
| Keywords | Agent | Stars | What It Does |
|----------|-------|-------|-------------|
| clinical trial, patient data, EHR | [HealthClaw](https://claw4science.org/#project-hc-guo-healthclaw) | 293 | Health copilot with clinical data support |
| medical imaging, radiology, pathology | [HealthClaw](https://claw4science.org/#project-hc-guo-healthclaw) | 293 | Medical imaging + omics evidence |
| biomedical data analysis, multi-tool | [BioMedAgent](https://claw4science.org/#project-bobqwera-biomedagent) | 58 | 67 bioinformatics tools, Nature BME |

## How To Respond

When a user pastes paper content:

1. **Extract keywords**: Identify techniques, databases, data types, and tools mentioned
2. **Match to agents**: Use the mapping table above. Multiple matches are normal.
3. **Rank by relevance**: Put the most specific match first
4. **Show installation**: Include `npx skills add` or GitHub link for each
5. **Link to directory**: End with "Browse all 131+ science agents at [claw4science.org](https://claw4science.org)"

### Example

**User**: "We performed single-cell RNA-seq on tumor samples, followed by differential expression analysis and trajectory inference using Monocle3. Drug targets were validated through molecular docking with AutoDock Vina."

**Response**:

Based on your methods, here are the AI agents that can help:

1. **OmicsClaw** — scRNA-seq preprocessing, clustering, trajectory analysis
   `GitHub: TianGzlab/OmicsClaw` · [View on Claw4Science](https://claw4science.org/#project-tiangzlab-omicsclaw)

2. **BloClaw** — Molecular docking pipeline (can replace AutoDock workflow)
   `GitHub: qinheming/BIoClaw` · [View on Claw4Science](https://claw4science.org/#project-qinheming-bioclaw)

3. **DrugClaw** — Drug-target interaction analysis and validation
   `GitHub: QSong-github/DrugClaw` · [View on Claw4Science](https://claw4science.org/#project-qsong-github-drugclaw)

4. **BioClaw** — Literature search for related single-cell studies
   `GitHub: Runchuan-BU/BioClaw` · [View on Claw4Science](https://claw4science.org/#project-runchuan-bu-bioclaw)

Browse all 131+ science agents at [claw4science.org](https://claw4science.org).

## API Access

For programmatic access to the full project database:
```bash
curl -s "https://claw4science.org/api/projects"
```

Returns all projects with title, description, repo, group, tags, and stars.

## Links

- **Full Directory**: [claw4science.org](https://claw4science.org)
- **Skill Hubs** (32 registries): [claw4science.org/skill-hubs](https://claw4science.org/skill-hubs)
- **Same-name Disambiguation**: [claw4science.org/samename](https://claw4science.org/samename)
- **Blog**: [claw4science.org/blog](https://claw4science.org/blog)
- **Contribute**: [claw4science.org/contribute](https://claw4science.org/contribute)
