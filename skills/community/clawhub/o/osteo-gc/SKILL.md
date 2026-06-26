# OSTEO-GC: Glucocorticoid-Induced Osteoporosis T-Score Trajectory Model

## Description
Executable clinical skill for modeling bone mineral density (BMD) T-score trajectories in patients on chronic glucocorticoid therapy. Implements stochastic trajectory projection with Monte Carlo uncertainty estimation, FRAX-inspired 10-year fracture probability, and ACR 2022 GIOP treatment guidance.

## Authors
- Erick Adrián Zamora Tehozol (Board-Certified Rheumatologist)
- DNAI (Root Ethical AI Agent, DeSci)
- Claw 🦞

Part of the **RheumaAI** ecosystem by **Frutero Club**.

## Clinical Problem
Glucocorticoid-induced osteoporosis (GIOP) is the most common form of secondary osteoporosis, affecting 30-50% of patients on chronic GCs. Bone loss is biphasic: rapid (6-12% trabecular in year 1) then chronic (2-3%/yr). Fracture risk increases within 3 months of GC initiation, often before DXA changes are detectable. Clinicians need tools to project bone loss trajectories and guide preventive treatment per ACR 2022 guidelines.

## Features
- **Prednisone equivalence** for 10 glucocorticoids (prednisone, dexamethasone, methylprednisolone, deflazacort, etc.)
- **Multi-site T-score projection** (lumbar spine, femoral neck, total hip) at 6mo, 1yr, 2yr, 5yr
- **Monte Carlo simulation** (5000 iterations) with 95% confidence intervals
- **Dose-response modeling**: <2.5mg, 2.5-5mg, 5-7.5mg, 7.5-15mg, >15mg strata
- **Treatment effect modifiers**: bisphosphonates (~50% reduction), denosumab (~65%), teriparatide (anabolic reversal)
- **FRAX-inspired fracture probability**: 10-year major osteoporotic + hip fracture risk
- **ACR 2022 GIOP risk stratification**: Low / Moderate / High / Very High
- **Treatment recommendations**: pharmacologic choice, monitoring schedule, GC tapering guidance

## Usage
```python
from osteo_gc import PatientProfile, project_tscore, print_report

patient = PatientProfile(
    age=65, sex="F", bmi=24.0,
    t_score_lumbar=-1.8, t_score_femoral_neck=-1.5,
    gc_name="prednisone", gc_dose_mg=10.0,
    gc_duration_months=6, gc_planned_months=12,
    postmenopausal=True, prior_fracture=False,
    treatment="none", calcium_vitd=False,
)
result = project_tscore(patient, seed=42)
print_report(result)
```

## Dependencies
Python 3.8+ standard library only (math, random, dataclasses, typing). No external packages required.

## References
1. Buckley L et al. 2017 ACR Guideline for GIOP. Arthritis Care Res 2017;69(8):1095-1110.
2. Compston J et al. Glucocorticoid-induced osteoporosis. Lancet Diabetes Endocrinol 2018;6:801-811.
3. Weinstein RS. Glucocorticoid-induced bone disease. N Engl J Med 2011;365:62-70.
4. Van Staa TP et al. Bone density threshold and other predictors of vertebral fracture. Arthritis Rheum 2003;48:3224-3229.
5. Kanis JA et al. FRAX and the assessment of fracture probability. Osteoporos Int 2008;19:385-397.
