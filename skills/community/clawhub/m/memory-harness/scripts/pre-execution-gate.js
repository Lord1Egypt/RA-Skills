/**
 * Pre-Execution Recall Gate
 * 
 * Runs before execution-like actions to check for constraints,
 * conflicts, and safety issues.
 */

/**
 * Pre-execution recall gate
 * @param {Object} plan - Execution plan
 * @param {Object[]} constraints - Known constraints
 * @returns {Object} Check result
 */
function preExecutionGate(plan, constraints = []) {
  const result = {
    proceed: true,
    warnings: [],
    constraints: [],
    conflicts: [],
  };
  
  // Check for safety issues
  const safetyCheck = checkSafetyConstraints(plan);
  if (safetyCheck.hasIssues) {
    result.warnings.push(...safetyCheck.warnings);
  }
  
  // Check for conflicts
  const conflictCheck = checkConflicts(plan, constraints);
  if (conflictCheck.hasConflicts) {
    result.conflicts.push(...conflictCheck.conflicts);
    result.warnings.push(...conflictCheck.conflicts);
  }
  
  // Add relevant constraints
  result.constraints = constraints.filter(c => isRelevantToPlan(c, plan));
  
  return result;
}

function checkSafetyConstraints(plan) {
  const warnings = [];
  const dangerousPatterns = [
    /\brm\s+-rf/,
    /\bdrop\s+table/i,
    /\bdelete\s+from/i,
    /eval\s*\(/,
    /exec\s*\(/,
  /child_process/,
  ];
  
  for (const pattern of dangerousPatterns) {
    if (pattern.test(plan.description)) {
      warnings.push(`Potentially dangerous operation: ${pattern.source}`);
    }
  }
  
  if (plan.scope === 'system') {
    warnings.push('System-wide changes require extra caution');
  }
  
  return { hasIssues: warnings.length > 0, warnings };
}

function checkConflicts(plan, constraints) {
  const conflicts = [];
  
  for (const constraint of constraints) {
    if (constraint.type === 'constraint') {
      const negationPatterns = ['must not', 'should not', 'never', 'avoid'];
      for (const pattern of negationPatterns) {
        if (constraint.summary.toLowerCase().includes(pattern)) {
          const forbidden = constraint.summary.toLowerCase().replace(pattern, '').trim();
          if (forbidden && plan.description.toLowerCase().includes(forbidden.split(' ')[0])) {
            conflicts.push(`May violate: ${constraint.summary}`);
          }
        }
      }
    }
  }
  
  return { hasConflicts: conflicts.length > 0, conflicts };
}

function isRelevantToPlan(constraint, plan) {
  const planText = (plan.description + ' ' + (plan.affectedFiles || []).join(' ')).toLowerCase();
  const keywords = constraint.summary.toLowerCase().split(/\s+/).filter(w => w.length > 3);
  return keywords.some(k => planText.includes(k));
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  let planJson = null;
  let constraintsJson = [];
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--plan' && args[i + 1]) {
      planJson = JSON.parse(args[++i]);
    } else if (args[i] === '--constraints' && args[i + 1]) {
      constraintsJson = JSON.parse(args[++i]);
    }
  }
  
  if (!planJson) {
    console.error('Usage: node pre-execution-gate.js --plan \'{"action":"file_edit","description":"..."}\'');
    process.exit(1);
  }
  
  console.log(JSON.stringify(preExecutionGate(planJson, constraintsJson), null, 2));
}

module.exports = { preExecutionGate };
