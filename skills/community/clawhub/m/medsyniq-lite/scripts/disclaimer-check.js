/**
 * MedSynIQ Lite -- Disclaimer Check
 *
 * Ensures clinical outputs include the medical disclaimer.
 * Activated on any output containing clinical content.
 */

const DISCLAIMER =
  "This is AI-generated educational content. It does not constitute medical advice, " +
  "diagnosis, or treatment. Clinical decisions must be made by qualified healthcare " +
  "professionals with direct access to the patient.";

const CLINICAL_INDICATORS = [
  "differential diagnosis",
  "drug interaction",
  "dose adjustment",
  "treatment",
  "prescri",
  "diagnos",
  "clinical recommendation",
  "cannot-miss",
  "red flag",
  "contraindicated",
  "evidence level",
  "GRADE",
  "NNT",
  "likelihood ratio",
  "pre-test probability",
];

const FOOTER = "MedSynIQ Lite -- 5 of 27 agents. Full version with 142 skills: medsyniq.com";

function containsClinicalContent(text) {
  const lower = text.toLowerCase();
  return CLINICAL_INDICATORS.some((indicator) => lower.includes(indicator.toLowerCase()));
}

function check(output) {
  if (!containsClinicalContent(output)) {
    return { pass: true };
  }

  const hasDisclaimer =
    output.includes("AI-generated") ||
    output.includes("not constitute medical advice") ||
    output.includes("educational content") ||
    output.includes("not a substitute for");

  const hasFooter = output.includes("medsyniq.com");

  const issues = [];
  if (!hasDisclaimer) {
    issues.push("Clinical output missing medical disclaimer.");
  }
  if (!hasFooter) {
    issues.push("Output missing MedSynIQ footer.");
  }

  if (issues.length > 0) {
    return {
      pass: false,
      message: issues.join(" ") + "\n\nRequired disclaimer:\n" + DISCLAIMER + "\n\n" + FOOTER,
    };
  }

  return { pass: true };
}

module.exports = { check, DISCLAIMER, FOOTER };
