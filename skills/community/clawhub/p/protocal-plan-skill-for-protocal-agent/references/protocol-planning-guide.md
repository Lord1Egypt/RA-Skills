# Protocol Planning Guide

## Principles of Good Protocol Design

### 1. Reproducibility
- Every step must specify exact quantities, temperatures, durations, and equipment
- Use precise language: "centrifuge at 12,000 x g for 10 minutes at 4C" not "spin down"
- Note acceptable ranges where flexibility exists: "incubate 5-10 minutes at RT"

### 2. Safety-First Structure
Every protocol plan must address these safety categories before listing procedures:
- **Chemical hazards**: Classify reagents (flammable, corrosive, toxic, carcinogenic). Reference SDS sheets.
  - TRIzol/QIAzol: toxic, corrosive -- fume hood required
  - Chloroform: toxic, volatile -- fume hood required, avoid skin contact
  - Ethanol: flammable -- keep away from open flames
  - DNase I: biological enzyme -- handle with gloves
  - SYBR Green: potential mutagen -- handle with gloves, avoid skin contact
- **PPE requirements**: Minimum PPE for molecular biology work: lab coat, nitrile gloves, safety glasses. Fume hood for volatile organics.
- **Waste disposal**: Separate organic waste (phenol/chloroform), aqueous waste, sharps, biohazard waste. Follow institutional EHS guidelines.
- **Emergency procedures**: Eye wash station location, spill kit location, emergency contacts

### 3. Time Management
- Clearly distinguish active time (hands-on) from passive time (incubation, centrifugation)
- Identify parallelizable steps (e.g., preparing master mix during incubation)
- Mark natural stopping/pause points with storage conditions
- Provide cumulative timeline

### 4. Quality Control Checkpoints
Build verification into the plan at critical junctures:
- **RNA extraction**: Nanodrop 260/280 ratio (expect 1.8-2.1), 260/230 ratio (expect >1.8), gel electrophoresis for integrity (28S:18S ratio ~2:1)
- **Reverse transcription**: Include no-RT control, verify cDNA yield
- **qPCR**: Melt curve analysis (single peak), NTC controls, standard curve R-squared >0.98, amplification efficiency 90-110%

### 5. Protocol Plan Document Sections

Every generated plan must include these sections in order:

1. **Header**: Task name, date, estimated total time, skill level
2. **Safety Summary**: Consolidated hazards and PPE
3. **Materials & Reagents Checklist**: With vendors and catalog numbers, checkboxes
4. **Equipment Checklist**: All instruments and consumables
5. **Procedure Steps**: Numbered, with sub-steps, durations, temperatures
6. **Timeline Summary Table**: Step durations and cumulative time
7. **Troubleshooting Quick Reference**: Common problems and solutions
8. **References**: URLs to source protocols and guidelines

### 6. Common Molecular Biology Workflows

#### RNA Extraction -> RT -> qPCR Pipeline
- **Phase 1 -- RNA Extraction** (~2-3 hours active, variable pause points)
  - Tissue homogenization, phase separation, column purification, DNase treatment, elution
  - Critical: RNase-free environment throughout
  - Pause point: Purified RNA stored at -80C

- **Phase 2 -- Reverse Transcription** (~1-1.5 hours active)
  - RNA quantification, primer annealing, reverse transcription reaction
  - Critical: Accurate RNA input normalization
  - Pause point: cDNA stored at -20C

- **Phase 3 -- qPCR** (~2-3 hours including setup and run)
  - Master mix preparation, plate loading, instrument setup, run, analysis
  - Critical: Consistent pipetting, proper controls (NTC, no-RT)
  - No pause point during run

### 7. Reagent Preparation Notes
- Buffer RPE requires ethanol addition before first use
- DNase I stock stored at -20C, Buffer RDD at 4C
- SYBR Green master mix is light-sensitive
- Random primers and dNTPs stored at -20C
- Always prepare master mixes with 10% overage to account for pipetting loss
