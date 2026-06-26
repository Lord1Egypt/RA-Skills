# Medical and Healthcare Domain Knowledge

## Molecular Biology Expertise Areas

### Gene Expression Analysis
Gene expression analysis quantifies mRNA levels to understand which genes are active under specific conditions. The standard workflow is:
1. RNA isolation from biological samples
2. Reverse transcription to convert RNA to cDNA
3. Quantitative PCR (qPCR) to measure specific transcript abundance
4. Data analysis using the comparative Ct method (delta-delta Ct)

### Key Techniques and Their Applications

#### RNA Extraction Methods
| Method | Best For | Yield | Purity | Time |
|--------|----------|-------|--------|------|
| TRIzol/QIAzol + column | Tissues, high yield needed | High | High (with DNase) | 2-3h |
| Column-only (RNeasy) | Cell culture, small samples | Moderate | Very high | 1h |
| Magnetic beads | High throughput, automation | Moderate | High | 1-2h |
| FFPE extraction | Archived tissue samples | Low | Variable | 3-4h |

#### Reverse Transcription Considerations
- **Random primers**: Capture all RNA species including rRNA, mRNA, ncRNA. Best for general gene expression studies.
- **Oligo(dT) primers**: Capture only polyadenylated mRNA. Better specificity but miss non-polyadenylated transcripts.
- **Gene-specific primers**: Highest specificity. Use when targeting a small number of known transcripts.
- **Input RNA**: Typical range 100pg to 1ug. Normalize input across samples for valid comparisons.
- **RNase inhibitor**: Always include to protect RNA template during reaction.

#### qPCR Best Practices
- **Primer design**: 18-25 bp, Tm 58-62C, GC content 40-60%, amplicon 70-200bp
- **Controls**: No-template control (NTC), no-RT control, positive control
- **Replicates**: Minimum technical triplicates per sample-target combination
- **Reference genes**: Use 2-3 validated housekeeping genes (e.g., GAPDH, ACTB, 18S rRNA). Validate stability across experimental conditions.
- **Standard curve**: 5-point serial dilution, R-squared >0.98, efficiency 90-110%
- **Melt curve**: Single peak confirms specificity; multiple peaks indicate non-specific amplification or primer dimers

### Sample Handling and Storage
| Sample Type | Storage Condition | Max Duration | Notes |
|-------------|-------------------|-------------|-------|
| Fresh tissue | RNAlater or snap-freeze | Indefinite at -80C | Process within 30min if no stabilizer |
| Homogenized in TRIzol | -80C | Months | Thaw on ice when ready |
| Purified RNA | -80C | Years | Avoid freeze-thaw cycles; aliquot |
| cDNA | -20C | Months | Stable; less sensitive than RNA |

## Safety and Regulatory Considerations

### Chemical Safety Classification
- **TRIzol/QIAzol**: Contains phenol and guanidine thiocyanate. Toxic if inhaled or absorbed through skin. Corrosive. Use in fume hood only.
- **Chloroform**: Suspected carcinogen. Volatile. Central nervous system depressant. Fume hood mandatory.
- **Beta-mercaptoethanol (in Buffer RLT)**: Toxic, strong odor. Fume hood for any step involving this buffer.
- **Ethidium bromide** (if used for gel verification): Known mutagen. Designated area, double gloving, proper waste disposal.
- **SYBR Green**: Binds DNA -- potential mutagen. Handle with gloves, avoid skin contact.

### Institutional Requirements
- **Animal tissue**: IACUC approval required before obtaining samples
- **Human tissue**: IRB approval and informed consent required
- **Biosafety**: IBC registration if working with recombinant DNA or infectious agents
- **Chemical inventory**: Register hazardous chemicals with institutional EHS
- **Waste streams**: Maintain separate waste containers for organic solvents, aqueous chemical waste, biohazard, and sharps

### Quality Assurance Standards
- **MIQE guidelines**: Minimum Information for Publication of Quantitative Real-Time PCR Experiments -- follow for publishable data
- **GLP (Good Laboratory Practice)**: Document all procedures, maintain equipment calibration records, use certified reference materials
- **ISO 15189**: Clinical laboratory standard for medical testing -- relevant if results inform clinical decisions

## Troubleshooting Reference

### RNA Quality Issues
| Problem | Indicator | Likely Cause | Solution |
|---------|-----------|-------------|----------|
| Low yield | <50ng/uL | Insufficient starting material, RNA degradation | Increase tissue input, check RNase contamination |
| Protein contamination | 260/280 <1.8 | Incomplete phase separation | Repeat chloroform extraction, re-column |
| Organic contamination | 260/230 <1.8 | Phenol/guanidine carryover | Additional wash with Buffer RPE, increase ethanol washes |
| RNA degradation | Smear on gel, no distinct bands | RNase contamination, improper storage | Use fresh RNase-free consumables, check water source |

### RT-qPCR Issues
| Problem | Indicator | Likely Cause | Solution |
|---------|-----------|-------------|----------|
| No amplification | No Ct value | Failed RT, primer issue, template issue | Check RT controls, redesign primers, verify template integrity |
| Late Ct (>35) | Very low expression | Low input, degraded RNA, primer inefficiency | Increase cDNA input, check RNA quality, optimize primers |
| Multiple melt peaks | Non-specific amplification | Primer dimers, off-target binding | Redesign primers, optimize annealing temperature |
| Variable replicates | SD >0.5 Ct | Pipetting inconsistency | Use calibrated pipettes, master mix approach, electronic pipette |
| NTC amplification | Ct in NTC wells | Contamination | Fresh reagents, clean workspace, new water |

## Common Vendor References
- **QIAGEN**: RNeasy kits, buffers RW1/RPE/RDD, RNase-Free DNase Set
- **Thermo Fisher / Life Technologies**: TRIzol, SYBR Select Master Mix, UltraPure Water, Applied Biosystems QuantStudio instruments
- **Lucigen / Epicentre**: EpiScript Reverse Transcriptase
- **NEB (New England Biolabs)**: Alternative RT enzymes, competent cells
- **Bio-Rad**: CFX qPCR instruments, SsoAdvanced SYBR master mixes
- **Clontech / Takara**: NucleoSpin RNA columns, reverse transcription kits
