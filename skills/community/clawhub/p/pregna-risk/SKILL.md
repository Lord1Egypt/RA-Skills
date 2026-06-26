# PREGNA-RISK: Pregnancy Risk Stratification in SLE/APS

## Overview
Quantitative risk stratification tool for pregnancy in patients with Systemic Lupus Erythematosus (SLE) and/or Antiphospholipid Syndrome (APS). Computes a weighted composite score predicting adverse pregnancy outcomes (APO) including preeclampsia, fetal loss, preterm birth, and IUGR.

## Authors
- Erick Adrián Zamora Tehozol (Board-Certified Rheumatologist)
- DNAI (Distributed Neural Artificial Intelligence)
- Claw 🦞

## Clinical Problem
Pregnancy in SLE/APS carries 2-5x higher risk of adverse outcomes compared to general population. Current management relies on subjective clinical judgment. PREGNA-RISK provides an evidence-based composite score integrating serological, clinical, and treatment factors to guide preconception counseling and monitoring intensity.

## Model

### Risk Factors and Weights

Based on PROMISSE study (Buyon et al., NEJM 2015), Hopkins Lupus Cohort, and EUROAPS registry data:

| Factor | Weight | Evidence |
|--------|--------|----------|
| Active lupus nephritis (current or <6mo) | +25 | Bramham et al. 2011, Smyth et al. 2010 |
| Anti-dsDNA positive + low C3/C4 | +15 | Buyon PROMISSE 2015 |
| Triple aPL positivity (LA+aCL+aβ2GPI) | +20 | Pengo et al. 2018 |
| LA positive (isolated) | +12 | PROMISSE 2015 |
| aCL >40 GPL (isolated) | +8 | Lockshin et al. 2012 |
| Prior APO (fetal loss >10w, preeclampsia, HELLP) | +15 | Bramham 2011 |
| SLEDAI-2K >4 at conception | +10 | Clowse 2005 |
| eGFR <60 mL/min | +12 | Smyth et al. 2010 |
| Proteinuria >0.5 g/24h | +10 | Moroni et al. 2016 |
| Hypertension (pre-existing) | +8 | Ostensen et al. 2015 |
| Thrombocytopenia (<100k) | +8 | Buyon 2015 |
| On hydroxychloroquine (protective) | -10 | Leroux et al. 2015, EULAR rec |
| On low-dose aspirin (protective) | -5 | ASPRE trial extrapolation |
| On prophylactic LMWH (APS, protective) | -8 | Mak et al. 2017 |
| Disease quiescence >6mo | -12 | Ostensen 2015, EULAR 2017 |
| Age >35 | +5 | General obstetric risk |
| BMI >30 | +5 | General obstetric risk |

### Score Interpretation

$$S = \sum_{i} w_i \cdot x_i, \quad x_i \in \{0,1\}$$

| Score Range | Risk Category | Recommendation |
|-------------|---------------|----------------|
| ≤10 | Low | Standard OB monitoring + rheumatology q-trimester |
| 11–30 | Moderate | High-risk OB + monthly rheumatology + uterine Doppler q4w from wk 20 |
| 31–50 | High | MFM referral + biweekly rheumatology + uterine/umbilical Doppler q2w from wk 16 |
| >50 | Very High | Defer pregnancy. If ongoing: inpatient monitoring, multidisciplinary team, consider early delivery planning |

### Monte Carlo Uncertainty Estimation
The tool runs 10,000 simulations with ±20% perturbation on weights (uniform) to generate 95% CI for the score, capturing epistemic uncertainty in weight calibration.

## Dependencies
```
pip install numpy
```

## Usage
```bash
python3 pregna_risk.py
```

## References
1. Buyon JP et al. Predictors of Pregnancy Outcomes in Patients With Lupus (PROMISSE). Ann Intern Med. 2015;163(3):153-163.
2. Bramham K et al. Pregnancy outcome in women with chronic kidney disease. J Am Soc Nephrol. 2011;22(11):2011-22.
3. Pengo V et al. Update of the guidelines for lupus anticoagulant detection. J Thromb Haemost. 2009;7:1737-40.
4. Clowse MEB et al. The impact of increased lupus activity on obstetric outcomes. Arthritis Rheum. 2005;52:514-21.
5. Leroux M et al. Hydroxychloroquine and pregnancy outcomes. Autoimmun Rev. 2015;14(11):1013-20.
6. Tektonidou MG et al. EULAR recommendations for the management of APS in adults. Ann Rheum Dis. 2019;78:1296-1304.
7. Smyth A et al. A systematic review and meta-analysis of pregnancy outcomes in CKD. Clin J Am Soc Nephrol. 2010;5:2060-8.

## Affiliated With
RheumaAI | Frutero Club | DeSci
