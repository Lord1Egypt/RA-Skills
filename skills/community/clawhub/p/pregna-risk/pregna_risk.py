#!/usr/bin/env python3
"""
PREGNA-RISK: Pregnancy Risk Stratification in SLE/APS
Authors: Erick Adrián Zamora Tehozol, DNAI, Claw 🦞
Affiliated: RheumaAI | Frutero Club | DeSci

Composite weighted score with Monte Carlo uncertainty estimation
for adverse pregnancy outcome (APO) risk in SLE/APS patients.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Tuple, List
import json
import sys

# --- Risk Factor Definitions ---

RISK_FACTORS: Dict[str, Dict] = {
    "active_nephritis": {
        "label": "Active lupus nephritis (current or <6 months)",
        "weight": 25,
        "category": "renal"
    },
    "anti_dsdna_low_complement": {
        "label": "Anti-dsDNA positive + low C3/C4",
        "weight": 15,
        "category": "serological"
    },
    "triple_apl": {
        "label": "Triple aPL positivity (LA + aCL + aβ2GPI)",
        "weight": 20,
        "category": "serological"
    },
    "la_positive": {
        "label": "Lupus anticoagulant positive (isolated)",
        "weight": 12,
        "category": "serological"
    },
    "acl_high": {
        "label": "aCL >40 GPL (isolated)",
        "weight": 8,
        "category": "serological"
    },
    "prior_apo": {
        "label": "Prior APO (fetal loss >10w, preeclampsia, HELLP)",
        "weight": 15,
        "category": "obstetric_history"
    },
    "sledai_gt4": {
        "label": "SLEDAI-2K >4 at conception",
        "weight": 10,
        "category": "disease_activity"
    },
    "egfr_low": {
        "label": "eGFR <60 mL/min",
        "weight": 12,
        "category": "renal"
    },
    "proteinuria": {
        "label": "Proteinuria >0.5 g/24h",
        "weight": 10,
        "category": "renal"
    },
    "hypertension": {
        "label": "Pre-existing hypertension",
        "weight": 8,
        "category": "comorbidity"
    },
    "thrombocytopenia": {
        "label": "Thrombocytopenia (<100k)",
        "weight": 8,
        "category": "hematological"
    },
    "on_hcq": {
        "label": "On hydroxychloroquine (protective)",
        "weight": -10,
        "category": "treatment"
    },
    "on_aspirin": {
        "label": "On low-dose aspirin (protective)",
        "weight": -5,
        "category": "treatment"
    },
    "on_lmwh": {
        "label": "On prophylactic LMWH (protective)",
        "weight": -8,
        "category": "treatment"
    },
    "disease_quiescent_6mo": {
        "label": "Disease quiescence >6 months (protective)",
        "weight": -12,
        "category": "disease_activity"
    },
    "age_over_35": {
        "label": "Age >35",
        "weight": 5,
        "category": "demographic"
    },
    "bmi_over_30": {
        "label": "BMI >30",
        "weight": 5,
        "category": "demographic"
    },
}


def classify_risk(score: float) -> Tuple[str, str]:
    """Classify score into risk category with recommendation."""
    if score <= 10:
        return "LOW", "Standard OB monitoring + rheumatology every trimester"
    elif score <= 30:
        return "MODERATE", ("High-risk OB + monthly rheumatology + "
                           "uterine Doppler q4w from week 20")
    elif score <= 50:
        return "HIGH", ("MFM referral + biweekly rheumatology + "
                        "uterine/umbilical Doppler q2w from week 16")
    else:
        return "VERY HIGH", ("Defer pregnancy if possible. If ongoing: "
                             "inpatient monitoring, multidisciplinary team, "
                             "consider early delivery planning")


def compute_score(patient: Dict[str, bool]) -> float:
    """Compute deterministic PREGNA-RISK score."""
    score = 0.0
    for factor_key, present in patient.items():
        if present and factor_key in RISK_FACTORS:
            score += RISK_FACTORS[factor_key]["weight"]
    return max(score, 0)  # floor at 0


def monte_carlo_ci(patient: Dict[str, bool],
                   n_simulations: int = 10000,
                   perturbation: float = 0.20,
                   seed: int = 42) -> Dict:
    """
    Run Monte Carlo simulation with uniform ±perturbation on weights.
    Returns point estimate, mean, median, 2.5th and 97.5th percentiles.
    """
    rng = np.random.default_rng(seed)
    active_factors = [k for k, v in patient.items() if v and k in RISK_FACTORS]
    base_weights = np.array([RISK_FACTORS[k]["weight"] for k in active_factors])

    # Perturb each weight uniformly within ±perturbation
    perturbations = rng.uniform(1 - perturbation, 1 + perturbation,
                                size=(n_simulations, len(active_factors)))
    simulated_weights = base_weights * perturbations
    simulated_scores = np.maximum(simulated_weights.sum(axis=1), 0)

    point = compute_score(patient)
    return {
        "point_estimate": round(point, 1),
        "mc_mean": round(float(np.mean(simulated_scores)), 1),
        "mc_median": round(float(np.median(simulated_scores)), 1),
        "ci_2_5": round(float(np.percentile(simulated_scores, 2.5)), 1),
        "ci_97_5": round(float(np.percentile(simulated_scores, 97.5)), 1),
        "n_simulations": n_simulations,
        "perturbation_pct": perturbation * 100
    }


def generate_report(patient: Dict[str, bool], patient_id: str = "ANON") -> str:
    """Generate a full clinical report."""
    score = compute_score(patient)
    category, recommendation = classify_risk(score)
    mc = monte_carlo_ci(patient)

    lines = [
        "=" * 60,
        "PREGNA-RISK — Pregnancy Risk Stratification (SLE/APS)",
        "=" * 60,
        f"Patient ID: {patient_id}",
        "",
        "ACTIVE RISK FACTORS:",
    ]

    positive = []
    protective = []
    for k, v in patient.items():
        if v and k in RISK_FACTORS:
            f = RISK_FACTORS[k]
            entry = f"  {'(+)' if f['weight'] > 0 else '(−)'} {f['label']} [{f['weight']:+d}]"
            if f["weight"] > 0:
                positive.append(entry)
            else:
                protective.append(entry)

    if positive:
        lines.append("  Risk factors:")
        lines.extend(positive)
    if protective:
        lines.append("  Protective factors:")
        lines.extend(protective)
    if not positive and not protective:
        lines.append("  (none)")

    lines.extend([
        "",
        f"COMPOSITE SCORE: {score:.0f}",
        f"RISK CATEGORY: {category}",
        "",
        f"Monte Carlo 95% CI: [{mc['ci_2_5']}, {mc['ci_97_5']}] "
        f"(mean {mc['mc_mean']}, n={mc['n_simulations']} simulations, "
        f"±{mc['perturbation_pct']:.0f}% weight perturbation)",
        "",
        f"RECOMMENDATION: {recommendation}",
        "",
        "MONITORING TIMELINE:",
    ])

    if category == "LOW":
        lines.extend([
            "  • Preconception: confirm disease quiescence, check aPL panel",
            "  • Q-trimester rheumatology visits",
            "  • Standard prenatal labs + aPL at 12w and 28w",
        ])
    elif category == "MODERATE":
        lines.extend([
            "  • Preconception: optimize disease control, start HCQ if not on it",
            "  • Monthly rheumatology + high-risk OB co-management",
            "  • Uterine artery Doppler from week 20 (q4w)",
            "  • Serial fetal growth scans q4w from week 24",
            "  • aPL + complement monthly",
        ])
    elif category == "HIGH":
        lines.extend([
            "  • Preconception counseling: discuss risks, optimize meds",
            "  • MFM referral immediately upon pregnancy confirmation",
            "  • Biweekly rheumatology visits",
            "  • Uterine/umbilical Doppler from week 16 (q2w)",
            "  • Weekly fetal monitoring from week 28",
            "  • aPL + complement + anti-dsDNA biweekly",
            "  • Plan delivery by 37 weeks if stable",
        ])
    else:
        lines.extend([
            "  ⚠️  DEFER PREGNANCY if planning stage",
            "  • If already pregnant: inpatient or close outpatient (2x/week)",
            "  • Multidisciplinary: rheumatology, MFM, nephrology, hematology",
            "  • Continuous fetal monitoring from viability",
            "  • Weekly labs (aPL, complement, CBC, CMP, urinalysis)",
            "  • Antenatal corticosteroids at 24w for lung maturity",
            "  • Plan delivery by 34-36 weeks",
        ])

    lines.extend([
        "",
        "DISCLAIMER: This tool supports clinical decision-making.",
        "It does not replace physician judgment or multidisciplinary assessment.",
        "=" * 60,
        "Authors: Zamora-Tehozol EA, DNAI, Claw 🦞",
        "RheumaAI | Frutero Club | DeSci",
    ])

    return "\n".join(lines)


# --- Demo Scenarios ---

def demo():
    """Run three clinical scenarios demonstrating the tool."""

    # Scenario 1: Low-risk SLE, well-controlled
    patient_1 = {
        "active_nephritis": False,
        "anti_dsdna_low_complement": False,
        "triple_apl": False,
        "la_positive": False,
        "acl_high": False,
        "prior_apo": False,
        "sledai_gt4": False,
        "egfr_low": False,
        "proteinuria": False,
        "hypertension": False,
        "thrombocytopenia": False,
        "on_hcq": True,
        "on_aspirin": True,
        "on_lmwh": False,
        "disease_quiescent_6mo": True,
        "age_over_35": False,
        "bmi_over_30": False,
    }

    # Scenario 2: Moderate-risk — APS with isolated LA, prior loss
    patient_2 = {
        "active_nephritis": False,
        "anti_dsdna_low_complement": False,
        "triple_apl": False,
        "la_positive": True,
        "acl_high": False,
        "prior_apo": True,
        "sledai_gt4": False,
        "egfr_low": False,
        "proteinuria": False,
        "hypertension": False,
        "thrombocytopenia": False,
        "on_hcq": True,
        "on_aspirin": True,
        "on_lmwh": True,
        "disease_quiescent_6mo": True,
        "age_over_35": True,
        "bmi_over_30": False,
    }

    # Scenario 3: Very high risk — active nephritis, triple aPL, active disease
    patient_3 = {
        "active_nephritis": True,
        "anti_dsdna_low_complement": True,
        "triple_apl": True,
        "la_positive": False,  # subsumed by triple
        "acl_high": False,
        "prior_apo": True,
        "sledai_gt4": True,
        "egfr_low": True,
        "proteinuria": True,
        "hypertension": True,
        "thrombocytopenia": True,
        "on_hcq": True,
        "on_aspirin": True,
        "on_lmwh": True,
        "disease_quiescent_6mo": False,
        "age_over_35": True,
        "bmi_over_30": True,
    }

    scenarios = [
        ("Low-risk: quiescent SLE on HCQ + aspirin", patient_1, "SLE-LOW-001"),
        ("Moderate-risk: APS with LA + prior loss, on triple therapy", patient_2, "APS-MOD-002"),
        ("Very high: active nephritis + triple aPL + multi-organ", patient_3, "SLE-APS-VH-003"),
    ]

    for title, patient, pid in scenarios:
        print(f"\n{'#' * 60}")
        print(f"# SCENARIO: {title}")
        print(f"{'#' * 60}")
        print(generate_report(patient, pid))
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON mode for API integration
        data = json.loads(sys.stdin.read())
        patient = data.get("factors", {})
        pid = data.get("patient_id", "ANON")
        score = compute_score(patient)
        cat, rec = classify_risk(score)
        mc = monte_carlo_ci(patient)
        result = {
            "patient_id": pid,
            "score": score,
            "category": cat,
            "recommendation": rec,
            "monte_carlo": mc,
        }
        print(json.dumps(result, indent=2))
    else:
        demo()
