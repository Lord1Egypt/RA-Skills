# Nutrigenomics

**Personalised nutrition recommendations from your genetic data**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-green)](https://openclaw.ai)

---

## 🧬 What is Nutrigenomics?

Nutrigenomics generates **personalised nutrition recommendations** based on your genetic profile. Upload your DNA file from 23andMe, AncestryDNA, or as a VCF file, and receive:

- 📊 **Nutrient Risk Assessment** — How your genes affect nutrient absorption and metabolism
- 🔍 **Gene-by-Gene Breakdown** — 40+ genes across 8 nutrient categories
- 📈 **Visual Reports** — Radar charts and interaction heatmaps
- 💡 **Actionable Recommendations** — Dietary optimisation and supplementation guidance
- 🔒 **100% Private** — All processing happens locally on your device

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **40+ Genes** | MTHFR, APOE, FTO, FADS1/2, VDR, CYP1A2, and more |
| **8 Nutrient Categories** | Micronutrients, macronutrients, omega-3s, caffeine, alcohol, sensitivities, antioxidants, detox |
| **Multi-Format Support** | 23andMe (.txt, .csv), AncestryDNA (.csv), VCF |
| **Risk Scoring** | 0-10 scale per nutrient with evidence-based recommendations |
| **Visualisations** | Radar chart (nutrient profile) + heatmap (gene-nutrient interactions) |
| **Private** | All analysis runs locally—no data transmission |
| **Open Source** | MIT licensed, community-driven |

---

## 🚀 Quick Start

### Via OpenClaw (Recommended for non-technical users)

Once published to ClawHub:

```bash
clawhub install nutrigenomics
```

Then tell OpenClaw: **"Generate my personalised nutrition report"** and upload your genetic data.

### Manual Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/drdaviddelorenzo/nutrigenomics.git
   cd nutrigenomics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run analysis**:
   ```bash
   python openclaw_adapter.py \
     --input your_genome.csv \
     --format 23andme \
     --output results/
   ```

4. **View results**:
   ```bash
   cat results/nutrigenomics_report.md
   open results/nutrigenomics_radar.png
   open results/nutrigenomics_heatmap.png
   ```

---

## 📖 Usage Examples

### From 23andMe Data
```bash
python openclaw_adapter.py --input genome.txt --format 23andme
```

### From AncestryDNA
```bash
python openclaw_adapter.py --input ancestry.csv --format ancestry
```

### From VCF File
```bash
python openclaw_adapter.py --input variants.vcf --format vcf
```

### Generate Test Report
```bash
python examples/generate_patient.py --run
```

---

## 📊 What You'll Get

### Personalised Report (Markdown)
- Executive summary of top findings
- Per-nutrient gene tables
- Risk interpretations
- Dietary recommendations
- Supplement interaction guidance

### Visual Outputs
- **Radar Chart**: Nutrient risk profile
- **Heatmap**: Gene-nutrient interaction matrix

### Reproducibility Package
- `README_reproducibility.txt` — Step-by-step instructions to reproduce the analysis
- `environment.yml` — Pinned conda environment
- `checksums.txt` — SHA-256 checksums of the SNP panel and output report (input file intentionally excluded)
- `provenance.json` — Timestamp, version, and analysis settings (input filename intentionally not recorded)

---

## 🧪 Testing

Run the test suite:

```bash
pytest tests/test_nutrigenomics.py -v
```

Generate a synthetic patient for testing:

```bash
python examples/generate_patient.py --output tests/test_patient.csv
```

---

## 📚 Documentation

- **[SKILL.md](SKILL.md)** — OpenClaw skill instructions
- **[README_OPENCLAW.md](README_OPENCLAW.md)** — Comprehensive user guide
- **[ATTRIBUTION.md](ATTRIBUTION.md)** — Scientific citations and credits
- **[CONTRIBUTORS.md](CONTRIBUTORS.md)** — How to contribute
- **[CHANGELOG.md](CHANGELOG.md)** — Version history and roadmap

---

## 🔬 Scientific Foundation

This skill is informed by peer-reviewed nutrigenomics research. For scientific details and verification:

- **PubMed**: https://pubmed.ncbi.nlm.nih.gov/
- **GWAS Catalog**: https://www.ebi.ac.uk/gwas/
- **ClinVar**: https://www.ncbi.nlm.nih.gov/clinvar/

Users should consult these authoritative sources and healthcare providers for specific scientific claims.

See [ATTRIBUTION.md](ATTRIBUTION.md) for more information.

---

## 🔒 Privacy & Security

✅ **All processing is local** — Your genetic data never leaves your device
✅ **No external API calls** — No data transmission to third parties
✅ **No account required** — Complete anonymity
✅ **Reports are local** — Contains per-SNP genotype calls for the 58 analysed SNPs only; full raw genome data is never reproduced
✅ **Open source** — Code is auditable

---

## ⚠️ Important Disclaimer

Nutrigenomics provides **educational, research-oriented analysis**. It does **NOT**:
- Constitute medical diagnosis
- Replace healthcare provider consultation
- Provide medical advice
- Diagnose nutrient deficiencies

**Always consult qualified healthcare providers** before making significant dietary changes or starting supplements.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTORS.md](CONTRIBUTORS.md) for:

- How to report bugs
- How to suggest SNPs
- How to improve documentation
- How to contribute code

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

**You are free to:**
- ✅ Use it (personal, educational, commercial)
- ✅ Modify it
- ✅ Distribute it

**You must:**
- 📋 Include the MIT License
- 📋 Give appropriate credit

---

## 👤 Author

**David de Lorenzo**

- 🐙 **GitHub**: [@drdaviddelorenzo](https://github.com/drdaviddelorenzo)
- 🌐 **Website**: https://drdaviddelorenzo.github.io
- 📧 **Email**: david@drdaviddelorenzo.dev

---

## 📖 How to Cite

If you use Nutrigenomics in research or education:

### BibTeX
```bibtex
@software{delorenzo2026nutrigenomics,
  author = {de Lorenzo, David},
  title = {Nutrigenomics: Personalised Nutrition from Genetic Data},
  year = {2026},
  url = {https://github.com/drdaviddelorenzo/nutrigenomics},
  version = {0.2.3}
}
```

### APA
de Lorenzo, D. (2026). *Nutrigenomics: Personalised nutrition from genetic data* (Version 0.2.3) [Software]. Retrieved from https://github.com/drdaviddelorenzo/nutrigenomics

See [ATTRIBUTION.md](ATTRIBUTION.md) for more citation formats.

---

## 🗺️ Roadmap

- [ ] **v0.3.0** — Microbiome integration (16S rRNA input)
- [ ] **v0.4.0** — Longitudinal tracking (compare reports over time)
- [ ] **v0.5.0** — HLA typing for immune-mediated food reactions
- [ ] **v1.0.0** — Multi-omics integration (metabolomics + genomics)
- [ ] **v1.5.0** — Integration with maternal nutrition risk scoring

---

## 📞 Support

- **GitHub Issues**: Report bugs or suggest features
- **GitHub Discussions**: Ask questions, share ideas
- **Email**: david@drdaviddelorenzo.dev
- **OpenClaw Discord**: discord.gg/clawd

---

## 🙏 Acknowledgments


- **OpenClaw team** for web platform integration
- **Nutrigenomics researchers** for foundational research
- **GWAS Catalog** and **ClinVar** for genetic data
- **Community contributors** for improvements and feedback

---

## 🔗 Links

- **GitHub Repository**: https://github.com/drdaviddelorenzo/nutrigenomics
- **My Website**: https://drdaviddelorenzo.github.io
- **OpenClaw**: https://openclaw.ai
- **ClawHub Registry**: https://clawhub.com

---

<div align="center">

**Nutrigenomics: Democratising personalised nutrition through open science and genetic literacy**

Made with 🧬 and ❤️ for health-conscious individuals everywhere

*MIT Licensed | Built by David de Lorenzo | Community-driven*

</div>
