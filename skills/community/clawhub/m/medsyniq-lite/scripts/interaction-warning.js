/**
 * MedSynIQ Lite -- Drug Interaction Warning
 *
 * Flags dangerous drug combinations when detected in output.
 * Covers contraindicated and major severity interactions.
 */

const CONTRAINDICATED_PAIRS = [
  ["maoi", "ssri"],
  ["maoi", "snri"],
  ["maoi", "tramadol"],
  ["maoi", "meperidine"],
  ["maoi", "linezolid"],
  ["simvastatin", "itraconazole"],
  ["simvastatin", "ketoconazole"],
  ["simvastatin", "ritonavir"],
  ["simvastatin", "clarithromycin"],
  ["lovastatin", "itraconazole"],
  ["lovastatin", "ketoconazole"],
  ["lovastatin", "ritonavir"],
  ["cisapride", "ketoconazole"],
  ["pimozide", "clarithromycin"],
  ["ergotamine", "ritonavir"],
  ["colchicine", "clarithromycin"],
];

const MAJOR_INTERACTIONS = [
  {
    drugs: ["warfarin", "amiodarone"],
    warning: "CYP2C9 inhibition -- INR elevation. Reduce warfarin 30-50%, monitor INR weekly for 6-8 weeks.",
  },
  {
    drugs: ["simvastatin", "amiodarone"],
    warning: "CYP3A4 inhibition -- rhabdomyolysis risk. Max simvastatin 20mg/day or switch to pravastatin/rosuvastatin.",
  },
  {
    drugs: ["clozapine", "fluvoxamine"],
    warning: "CYP1A2 inhibition -- 5-10x clozapine level increase. Potentially fatal.",
  },
  {
    drugs: ["methotrexate", "trimethoprim"],
    warning: "Reduced renal clearance -- methotrexate toxicity risk. Avoid combination or monitor closely.",
  },
  {
    drugs: ["lithium", "nsaid"],
    warning: "Reduced renal lithium clearance -- toxicity risk. Monitor lithium levels closely.",
  },
  {
    drugs: ["digoxin", "amiodarone"],
    warning: "P-gp inhibition -- digoxin level increase. Reduce digoxin dose 50%, monitor levels.",
  },
];

const QT_PROLONGING = [
  "amiodarone", "sotalol", "dronedarone", "quinidine",
  "haloperidol", "ziprasidone", "pimozide",
  "erythromycin", "clarithromycin", "moxifloxacin",
  "ondansetron", "domperidone", "methadone",
  "fluconazole",
];

const SEROTONERGIC = [
  "ssri", "snri", "fluoxetine", "sertraline", "paroxetine",
  "citalopram", "escitalopram", "venlafaxine", "duloxetine",
  "tramadol", "fentanyl", "linezolid", "maoi",
  "st john", "triptans",
];

function detectDrugsInText(text) {
  const lower = text.toLowerCase();
  const found = [];

  const drugTerms = [
    ...new Set([
      ...CONTRAINDICATED_PAIRS.flat(),
      ...MAJOR_INTERACTIONS.flatMap((i) => i.drugs),
      ...QT_PROLONGING,
      ...SEROTONERGIC,
    ]),
  ];

  for (const drug of drugTerms) {
    if (lower.includes(drug)) {
      found.push(drug);
    }
  }

  return found;
}

function checkInteractions(text) {
  const drugs = detectDrugsInText(text);
  const warnings = [];

  // Check contraindicated pairs
  for (const [a, b] of CONTRAINDICATED_PAIRS) {
    if (drugs.includes(a) && drugs.includes(b)) {
      warnings.push(`CONTRAINDICATED: ${a} + ${b}. Do not use together.`);
    }
  }

  // Check major interactions
  for (const interaction of MAJOR_INTERACTIONS) {
    const [a, b] = interaction.drugs;
    if (drugs.includes(a) && drugs.includes(b)) {
      warnings.push(`MAJOR: ${a} + ${b}. ${interaction.warning}`);
    }
  }

  // Check QT prolongation (2+ QT drugs)
  const qtDrugsFound = QT_PROLONGING.filter((d) => drugs.includes(d));
  if (qtDrugsFound.length >= 2) {
    warnings.push(
      `QT RISK: Multiple QT-prolonging drugs detected (${qtDrugsFound.join(", ")}). ` +
      `Monitor ECG, correct electrolytes (K, Mg). Avoid combination if possible.`
    );
  }

  return warnings;
}

module.exports = { checkInteractions, detectDrugsInText };
