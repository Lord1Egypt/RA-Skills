#!/usr/bin/env python3
"""
OSTEO-GC: Glucocorticoid-Induced Osteoporosis T-Score Trajectory Model
with Monte Carlo Uncertainty Estimation and ACR 2022 GIOP Treatment Guidance.

Authors: Erick Adrián Zamora Tehozol, DNAI, Claw 🦞
Part of the RheumaAI / Frutero Club DeSci ecosystem.

References:
  [1] Buckley L et al. 2017 ACR Guideline for Prevention and Treatment of GIOP. Arthritis Care Res 2017;69(8):1095-1110.
  [2] Compston J et al. Glucocorticoid-induced osteoporosis. Lancet Diabetes Endocrinol 2018;6:801-811.
  [3] Weinstein RS. Glucocorticoid-induced bone disease. N Engl J Med 2011;365:62-70.
  [4] Van Staa TP et al. Bone density threshold and other predictors of vertebral fracture in patients receiving oral glucocorticoid therapy. Arthritis Rheum 2003;48:3224-3229.
  [5] Kanis JA et al. FRAX and the assessment of fracture probability in men and women from the UK. Osteoporos Int 2008;19:385-397.
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Dict

# ── Prednisone equivalence table (mg → prednisone-equivalent mg) ──
GC_EQUIVALENCE = {
    "prednisone": 1.0,
    "prednisolone": 1.0,
    "methylprednisolone": 1.25,   # 4mg methylpred = 5mg pred
    "dexamethasone": 6.67,        # 0.75mg dexa = 5mg pred
    "deflazacort": 0.83,          # 6mg deflaz = 5mg pred
    "hydrocortisone": 0.25,       # 20mg HC = 5mg pred
    "cortisone": 0.2,             # 25mg cortisone = 5mg pred
    "betamethasone": 8.33,        # 0.6mg beta = 5mg pred
    "triamcinolone": 1.25,        # 4mg triam = 5mg pred
    "budesonide_oral": 0.5,       # ~3mg budes ≈ partial systemic
}

# ── Annual bone loss rates (fraction of T-score per year) ──
# Rapid phase (year 1): 6-12% trabecular → ~0.2-0.4 T-score decline
# Chronic phase (year 2+): 2-3% → ~0.05-0.1 T-score decline
# Rates vary by site and dose. These are T-score decrements per year.
# Sources: Weinstein 2011, Compston 2018

def _annual_tscore_loss(pred_eq_mg: float, year: int, site: str = "lumbar") -> float:
    """Return expected annual T-score decrement for given dose and year on GC."""
    # Dose-response: <5mg minimal, 5-7.5mg moderate, >7.5mg high
    if pred_eq_mg < 2.5:
        dose_factor = 0.3
    elif pred_eq_mg < 5.0:
        dose_factor = 0.6
    elif pred_eq_mg < 7.5:
        dose_factor = 1.0
    elif pred_eq_mg < 15.0:
        dose_factor = 1.4
    else:
        dose_factor = 1.8

    # Site factor: lumbar (trabecular) loses more than femoral neck
    site_factor = {"lumbar": 1.0, "femoral_neck": 0.75, "total_hip": 0.65}.get(site, 1.0)

    # Phase: rapid year 1, then chronic
    if year == 0:  # first year
        base_loss = 0.25  # ~0.25 T-score units
    else:
        base_loss = 0.08  # chronic phase

    return base_loss * dose_factor * site_factor


# ── Treatment effect modifiers ──
TREATMENT_EFFECTS = {
    "none": 1.0,              # no protection
    "calcium_vitd": 0.90,     # minimal ~10% reduction
    "alendronate": 0.45,      # ~55% reduction in bone loss
    "risedronate": 0.47,
    "zoledronic_acid": 0.40,
    "denosumab": 0.35,        # ~65% reduction
    "teriparatide": -0.20,    # REVERSES loss (anabolic)
    "romosozumab": -0.15,     # anabolic
}


@dataclass
class PatientProfile:
    """Patient profile for GIOP risk assessment."""
    age: int
    sex: str  # "M" or "F"
    bmi: float
    t_score_lumbar: float
    t_score_femoral_neck: Optional[float] = None
    t_score_total_hip: Optional[float] = None
    gc_name: str = "prednisone"
    gc_dose_mg: float = 5.0           # daily dose of the named GC
    gc_duration_months: int = 0        # how long already on GC
    gc_planned_months: int = 12        # planned additional duration
    prior_fracture: bool = False
    family_hip_fracture: bool = False
    smoking: bool = False
    alcohol_3plus: bool = False        # ≥3 units/day
    postmenopausal: bool = False
    rheumatoid_arthritis: bool = False
    calcium_vitd: bool = False
    treatment: str = "none"            # key from TREATMENT_EFFECTS
    secondary_osteoporosis: bool = False  # e.g., hypogonadism, hyperthyroidism

    @property
    def pred_equivalent_mg(self) -> float:
        factor = GC_EQUIVALENCE.get(self.gc_name.lower(), 1.0)
        return self.gc_dose_mg * factor

    @property
    def min_t_score(self) -> float:
        scores = [self.t_score_lumbar]
        if self.t_score_femoral_neck is not None:
            scores.append(self.t_score_femoral_neck)
        if self.t_score_total_hip is not None:
            scores.append(self.t_score_total_hip)
        return min(scores)


def _frax_inspired_fracture_prob(p: PatientProfile) -> Tuple[float, float]:
    """
    Simplified FRAX-inspired 10-year fracture probability.
    Returns (major_osteoporotic_pct, hip_fracture_pct).
    Based on Kanis et al. 2008 with GC adjustment.
    """
    # Base hazard by age and sex (approximate UK data)
    if p.sex == "F":
        base_major = 0.02 * math.exp(0.04 * (p.age - 50)) if p.age > 50 else 2.0
        base_hip = 0.005 * math.exp(0.05 * (p.age - 50)) if p.age > 50 else 0.5
    else:
        base_major = 0.015 * math.exp(0.035 * (p.age - 50)) if p.age > 50 else 1.5
        base_hip = 0.003 * math.exp(0.045 * (p.age - 50)) if p.age > 50 else 0.3

    # T-score effect: each unit below -2.5 roughly doubles risk
    t = p.min_t_score
    t_rr = math.exp(-0.55 * (t + 1.0))  # ~1.7x per SD decrease

    # Clinical risk factors (relative risks)
    rr = 1.0
    if p.prior_fracture:
        rr *= 2.0
    if p.family_hip_fracture:
        rr *= 1.5
    if p.smoking:
        rr *= 1.3
    if p.alcohol_3plus:
        rr *= 1.4
    if p.rheumatoid_arthritis:
        rr *= 1.3
    if p.secondary_osteoporosis:
        rr *= 1.2

    # BMI adjustment (low BMI increases risk)
    if p.bmi < 20:
        rr *= 1.4
    elif p.bmi < 25:
        rr *= 1.0
    else:
        rr *= 0.9

    # GC dose adjustment (ACR: ≥7.5mg increases fracture risk ~2-5x)
    gc_rr = 1.0 + 0.15 * p.pred_equivalent_mg  # linear approximation
    gc_rr = min(gc_rr, 5.0)

    major = min(base_major * t_rr * rr * gc_rr, 80.0)
    hip = min(base_hip * t_rr * rr * gc_rr, 50.0)

    return round(major, 1), round(hip, 1)


def project_tscore(
    p: PatientProfile,
    timepoints_months: List[int] = None,
    n_simulations: int = 5000,
    seed: Optional[int] = None
) -> Dict:
    """
    Project T-score trajectory with Monte Carlo uncertainty.

    Returns dict with:
      - projections: list of {month, mean, ci_lower, ci_upper} for each site
      - fracture_prob: {major_10yr, hip_10yr}
      - risk_category: Low/Moderate/High/Very High
      - acr_recommendation: treatment guidance per ACR 2022 GIOP
    """
    if seed is not None:
        random.seed(seed)
    if timepoints_months is None:
        timepoints_months = [6, 12, 24, 60]

    sites = {"lumbar": p.t_score_lumbar}
    if p.t_score_femoral_neck is not None:
        sites["femoral_neck"] = p.t_score_femoral_neck
    if p.t_score_total_hip is not None:
        sites["total_hip"] = p.t_score_total_hip

    treatment_factor = TREATMENT_EFFECTS.get(p.treatment, 1.0)
    if p.calcium_vitd and p.treatment != "calcium_vitd":
        treatment_factor *= 0.95  # additive minor benefit

    projections = {}

    for site, baseline_t in sites.items():
        site_proj = []
        for target_month in timepoints_months:
            sims = []
            for _ in range(n_simulations):
                t = baseline_t
                # Already elapsed months (prior GC use)
                elapsed_years = p.gc_duration_months / 12.0

                for m in range(1, target_month + 1):
                    current_year = int((p.gc_duration_months + m) / 12)
                    annual_loss = _annual_tscore_loss(p.pred_equivalent_mg, current_year, site)
                    monthly_loss = annual_loss / 12.0

                    # Apply treatment
                    if treatment_factor < 0:
                        # Anabolic: gain bone
                        monthly_change = -monthly_loss * abs(treatment_factor)
                        t += monthly_change  # net gain
                    else:
                        monthly_loss *= treatment_factor

                    # Stochastic noise (SD ~0.02 T-score/month biological variability)
                    noise = random.gauss(0, 0.015)

                    if treatment_factor >= 0:
                        t -= monthly_loss
                    t += noise

                sims.append(t)

            sims.sort()
            mean_t = sum(sims) / len(sims)
            ci_lower = sims[int(0.025 * n_simulations)]
            ci_upper = sims[int(0.975 * n_simulations)]

            site_proj.append({
                "month": target_month,
                "mean": round(mean_t, 2),
                "ci_lower": round(ci_lower, 2),
                "ci_upper": round(ci_upper, 2),
            })
        projections[site] = site_proj

    # Fracture probability
    major_10yr, hip_10yr = _frax_inspired_fracture_prob(p)

    # Risk category (ACR 2022 GIOP thresholds)
    # Low: FRAX major <10%, hip <1%, T-score > -1.0
    # Moderate: FRAX major 10-19%, hip 1-3%, or T-score -1.0 to -2.5
    # High: FRAX major ≥20%, hip ≥3%, or T-score ≤-2.5, or prior fragility fracture
    # Very High: T-score ≤-2.5 + fracture, or multiple fractures, or GC ≥30mg
    if (p.min_t_score <= -2.5 and p.prior_fracture) or p.pred_equivalent_mg >= 30:
        risk = "Very High"
    elif major_10yr >= 20 or hip_10yr >= 3.0 or p.min_t_score <= -2.5 or p.prior_fracture:
        risk = "High"
    elif major_10yr >= 10 or hip_10yr >= 1.0 or p.min_t_score <= -1.0:
        risk = "Moderate"
    else:
        risk = "Low"

    # ACR 2022 GIOP recommendation
    rec = _acr_recommendation(p, risk)

    return {
        "patient_summary": {
            "age": p.age,
            "sex": p.sex,
            "gc": f"{p.gc_name} {p.gc_dose_mg}mg/d (pred-eq: {p.pred_equivalent_mg:.1f}mg)",
            "gc_duration_months": p.gc_duration_months,
            "min_t_score": p.min_t_score,
            "current_treatment": p.treatment,
        },
        "projections": projections,
        "fracture_probability": {
            "major_osteoporotic_10yr_pct": major_10yr,
            "hip_10yr_pct": hip_10yr,
        },
        "risk_category": risk,
        "acr_recommendation": rec,
    }


def _acr_recommendation(p: PatientProfile, risk: str) -> Dict:
    """ACR 2022 GIOP treatment recommendation."""
    recs = {
        "calcium_vitamin_d": True,  # ALL patients on GC ≥3 months
        "lifestyle": "Weight-bearing exercise, fall prevention, smoking cessation, limit alcohol",
        "pharmacologic": "",
        "monitoring": "",
        "details": "",
    }

    if p.pred_equivalent_mg >= 2.5 and (p.gc_duration_months + p.gc_planned_months) >= 3:
        # ≥3 months of GC: pharmacologic prevention indicated based on risk
        if risk == "Low":
            recs["pharmacologic"] = "Optimize calcium (1000-1200mg/d) + vitamin D (600-800 IU/d). Reassess in 12 months."
            recs["monitoring"] = "DXA at baseline + 12 months. FRAX reassessment annually."
        elif risk == "Moderate":
            if p.age >= 40:
                recs["pharmacologic"] = "Oral bisphosphonate (alendronate 70mg/wk or risedronate 35mg/wk) recommended. Alternative: IV zoledronic acid 5mg/yr."
            else:
                recs["pharmacologic"] = "Oral bisphosphonate preferred. Consider if benefits outweigh risks in premenopausal women/younger men."
            recs["monitoring"] = "DXA at baseline, 6-12 months. Reassess fracture risk annually."
        elif risk == "High":
            recs["pharmacologic"] = "Oral bisphosphonate strongly recommended. If intolerant or failing: IV zoledronic acid or denosumab. Teriparatide if very high fracture risk."
            recs["monitoring"] = "DXA at baseline, 6 months, then annually. Consider VFA or lateral spine X-ray."
        elif risk == "Very High":
            recs["pharmacologic"] = "Teriparatide (preferred) or romosozumab (if no high CV risk) as first-line anabolic. Transition to antiresorptive after anabolic course. If anabolics unavailable: denosumab or IV zoledronic acid."
            recs["monitoring"] = "DXA at baseline, 6 months, annually. VFA at baseline. BTMs (P1NP, CTX) at baseline and 3-6 months."

        # GC dose reduction always recommended
        recs["details"] = (
            f"Current prednisone-equivalent: {p.pred_equivalent_mg:.1f} mg/day. "
            f"Strongly recommend tapering to lowest effective dose. "
            f"GC-sparing agents (e.g., methotrexate, azathioprine, mycophenolate) should be considered "
            f"to minimize cumulative GC exposure."
        )
    else:
        recs["pharmacologic"] = "Short-course GC (<3 months) or very low dose: optimize calcium/vitamin D, monitor."
        recs["monitoring"] = "DXA if additional risk factors present."

    return recs


def print_report(result: Dict):
    """Pretty-print the OSTEO-GC report."""
    ps = result["patient_summary"]
    print("=" * 70)
    print("  OSTEO-GC: Glucocorticoid-Induced Osteoporosis Risk Report")
    print("=" * 70)
    print(f"  Patient: {ps['age']}{ps['sex']}, BMI not shown, {ps['gc']}")
    print(f"  GC duration: {ps['gc_duration_months']} months | Min T-score: {ps['min_t_score']}")
    print(f"  Current treatment: {ps['current_treatment']}")
    print("-" * 70)

    print(f"\n  RISK CATEGORY: {result['risk_category']}")
    fp = result["fracture_probability"]
    print(f"  10-Year Fracture Probability:")
    print(f"    Major osteoporotic: {fp['major_osteoporotic_10yr_pct']}%")
    print(f"    Hip fracture:       {fp['hip_10yr_pct']}%")

    print(f"\n  PROJECTED T-SCORE TRAJECTORIES (95% CI):")
    for site, projs in result["projections"].items():
        print(f"\n    {site.replace('_', ' ').title()}:")
        for tp in projs:
            print(f"      {tp['month']:>3}mo: {tp['mean']:+.2f}  [{tp['ci_lower']:+.2f}, {tp['ci_upper']:+.2f}]")

    rec = result["acr_recommendation"]
    print(f"\n  ACR 2022 GIOP RECOMMENDATION:")
    print(f"    Calcium/Vitamin D: {'Yes' if rec['calcium_vitamin_d'] else 'No'}")
    print(f"    Lifestyle: {rec['lifestyle']}")
    print(f"    Pharmacologic: {rec['pharmacologic']}")
    print(f"    Monitoring: {rec['monitoring']}")
    if rec["details"]:
        print(f"    Details: {rec['details']}")
    print("=" * 70)


# ── Demo / Test ──
if __name__ == "__main__":
    print("\n*** SCENARIO 1: 65F, T-score -1.8 lumbar, prednisone 10mg/d x 6mo, postmenopausal, no treatment ***\n")
    p1 = PatientProfile(
        age=65, sex="F", bmi=24.0,
        t_score_lumbar=-1.8, t_score_femoral_neck=-1.5,
        gc_name="prednisone", gc_dose_mg=10.0,
        gc_duration_months=6, gc_planned_months=12,
        postmenopausal=True, prior_fracture=False,
        treatment="none", calcium_vitd=False,
    )
    r1 = project_tscore(p1, seed=42)
    print_report(r1)
    assert r1["risk_category"] in ("High", "Moderate"), f"Expected High/Moderate, got {r1['risk_category']}"
    print("✅ Scenario 1 PASSED\n")

    print("\n*** SCENARIO 2: 45M, T-score -0.5, prednisone 5mg/d x 3mo, on alendronate ***\n")
    p2 = PatientProfile(
        age=45, sex="M", bmi=27.0,
        t_score_lumbar=-0.5,
        gc_name="prednisone", gc_dose_mg=5.0,
        gc_duration_months=3, gc_planned_months=12,
        treatment="alendronate", calcium_vitd=True,
    )
    r2 = project_tscore(p2, seed=42)
    print_report(r2)
    assert r2["risk_category"] in ("Low", "Moderate"), f"Expected Low/Moderate, got {r2['risk_category']}"
    print("✅ Scenario 2 PASSED\n")

    print("\n*** SCENARIO 3: 70F, T-score -2.8 femoral neck, prednisone 15mg/d x 24mo, prior VFx, no treatment ***\n")
    p3 = PatientProfile(
        age=70, sex="F", bmi=21.0,
        t_score_lumbar=-2.2, t_score_femoral_neck=-2.8, t_score_total_hip=-2.4,
        gc_name="prednisone", gc_dose_mg=15.0,
        gc_duration_months=24, gc_planned_months=12,
        prior_fracture=True, family_hip_fracture=True,
        postmenopausal=True, smoking=False, alcohol_3plus=False,
        rheumatoid_arthritis=True,
        treatment="none", calcium_vitd=False,
    )
    r3 = project_tscore(p3, seed=42)
    print_report(r3)
    assert r3["risk_category"] == "Very High", f"Expected Very High, got {r3['risk_category']}"
    print("✅ Scenario 3 PASSED\n")

    print("All scenarios passed. OSTEO-GC operational.")
