// @ts-nocheck
/**
 * Validation Layer
 * Evaluates heuristic findings against contextual evidence to separate
 * "validated" threats from "heuristic-only" (potential false positives).
 */

function validateFindings(findings, context) {
  return findings.map(finding => {
    let status = 'heuristic-only';

    // Contextual Validation Rules
    
    // 1. If it's a prompt injection but found inside a code block, it might be a false positive 
    // (e.g., someone writing an article about prompt injection)
    if (finding.id.startsWith('PI_')) {
      if (context.isInCodeBlock(finding.text)) {
        status = 'heuristic-only'; // False positive likely
      } else {
        status = 'validated';
      }
    }

    // 2. If it's malicious code, verify if the execution environment allows it
    if (finding.id.startsWith('MAL_')) {
      if (context.isExecutable(finding.text)) {
        status = 'validated';
      }
    }

    return {
      ...finding,
      status
    };
  });
}

export { 
  validateFindings
 };
