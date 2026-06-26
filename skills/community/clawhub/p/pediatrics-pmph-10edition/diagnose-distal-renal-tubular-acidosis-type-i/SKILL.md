---
name: Diagnose Distal Renal Tubular Acidosis Type I (RTA-I) in Children
description: Use this skill to evaluate pediatric patients suspected of having distal renal tubular acidosis (RTA-I) when they present with growth failure, hypokalemia, bone disease, or urinary stones alongside hyperchloremic metabolic acidosis. Apply only after excluding glomerular and systemic diseases.
version: 1.0.0
---

# Diagnose Distal Renal Tubular Acidosis Type I (RTA-I) in Children

## When to Use
Use this skill **if** a child exhibits:
- Chronic hyperchloremic metabolic acidosis **and**
- One or more of: growth retardation, hypokalemia (e.g., muscle weakness, periodic paralysis), bone manifestations (rickets, bone pain, fractures, delayed dentition), or urinary symptoms (hematuria, dysuria, polyuria/polydipsia).

Do **not** use if the patient has significant pre-existing acidosis (pH < 7.2 or HCO₃⁻ < 15 mmol/L) or if glomerular disease or systemic conditions (e.g., SLE, Sjögren’s syndrome) have not been ruled out.

## Diagnostic Workflow

### 1. Perform Initial Clinical Screening
Assess for:
- Symptoms of chronic metabolic acidosis (anorexia, vomiting, poor growth)
- Signs of electrolyte imbalance (hypokalemia-related weakness)
- Skeletal abnormalities or history of nephrolithiasis

### 2. Conduct Core Laboratory Tests
Collect blood and urine samples to evaluate:
- **Blood**: low pH / HCO₃⁻ (or CO₂CP), elevated Cl⁻, normal anion gap, low K⁺/Na⁺, elevated ALP
- **Urine**: pH > 5.5 despite systemic acidosis, low specific gravity, increased Ca²⁺/Na⁺/K⁺ excretion, reduced ammonia

### 3. Calculate FE HCO₃⁻
Compute fractional excretion of bicarbonate:
```
FE HCO₃⁻ = (urine[HCO₃⁻] / serum[HCO₃⁻]) ÷ (urine[Cr] / serum[Cr]) × 100%
```
- **RTA-I criterion**: FE HCO₃⁻ < 5%

### 4. Consider Confirmatory Testing (Only if Clinically Stable)
- **NH₄Cl loading test**: Administer NH₄Cl 0.1 g/kg orally; once serum HCO₃⁻ drops below 20 mmol/L, measure urine pH.
  - **Positive (supports RTA-I)**: urine pH > 5.5
  - **Negative (excludes RTA-I)**: urine pH ≤ 5.5
- **Contraindication**: Do not perform if baseline acidosis is severe.

### 5. Support with Imaging
Obtain X-rays to check for:
- Osteopenia or rachitic changes
- Nephrocalcinosis or urinary calculi

### 6. Exclude Secondary Causes
Rule out drug toxicity, autoimmune disorders, or genetic syndromes before confirming primary RTA-I.

## Output Interpretation
Return:
- “符合RTA-I诊断” if all criteria align (clinical + lab + FE HCO₃⁻ < 5% ± positive NH₄Cl test)
- “不符合” if urine pH appropriately acidifies (<5.5) during acidosis or FE HCO₃⁻ ≥ 5%

Always list key supporting or excluding laboratory findings in the output.