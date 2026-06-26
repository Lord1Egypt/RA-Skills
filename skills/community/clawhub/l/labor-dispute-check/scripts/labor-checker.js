/**
 * Labor Dispute Checker
 * 
 * Checks common labor law issues and calculates employee rights.
 * This is an informational tool and does not constitute legal advice.
 */

function checkLaborIssue(input) {
  if (!input || typeof input !== 'object') {
    return {
      error: 'Invalid input: issue details required',
      result: null
    };
  }

  const { issue, years, monthlySalary, hours, contractMonths, probationMonths } = input;

  switch (issue) {
    case 'termination':
      return checkTermination(years, monthlySalary);
    case 'overtime':
      return checkOvertime(hours, monthlySalary);
    case 'probation':
      return checkProbation(contractMonths, probationMonths);
    default:
      return {
        error: 'Unknown issue type: ' + issue,
        result: null
      };
  }
}

function checkTermination(years, monthlySalary) {
  if (!years || !monthlySalary) {
    return {
      error: 'Years of service and monthly salary required',
      result: null
    };
  }

  const compensation = years * monthlySalary;
  
  return {
    issue: 'termination',
    compensation: compensation,
    explanation: 'Economic compensation: ' + years + ' years × ' + monthlySalary + ' = ' + compensation,
    note: 'N+1 rule: ' + years + ' months salary as compensation, plus 1 month for notice (if no notice given)',
    disclaimer: 'This is an estimate. Actual compensation may vary based on specific circumstances.'
  };
}

function checkOvertime(hours, monthlySalary) {
  if (!hours || !monthlySalary) {
    return {
      error: 'Overtime hours and monthly salary required',
      result: null
    };
  }

  const hourlyRate = monthlySalary / 21.75 / 8;
  const overtimePay = hours * hourlyRate * 1.5;

  return {
    issue: 'overtime',
    hourlyRate: Math.round(hourlyRate * 100) / 100,
    overtimePay: Math.round(overtimePay * 100) / 100,
    hours: hours,
    explanation: 'Standard overtime (150%): ' + hours + ' hours × ' + Math.round(hourlyRate * 100) / 100 + '/hour × 1.5',
    note: 'Monthly overtime capped at 36 hours by law',
    disclaimer: 'This is an estimate. Actual rates may vary.'
  };
}

function checkProbation(contractMonths, probationMonths) {
  if (!contractMonths || !probationMonths) {
    return {
      error: 'Contract duration and probation period required',
      result: null
    };
  }

  let maxProbation = 0;
  if (contractMonths < 12) {
    maxProbation = 1;
  } else if (contractMonths < 36) {
    maxProbation = 2;
  } else {
    maxProbation = 6;
  }

  const valid = probationMonths <= maxProbation;

  return {
    issue: 'probation',
    valid: valid,
    maxAllowed: maxProbation,
    requested: probationMonths,
    explanation: valid 
      ? 'Probation period is valid (' + probationMonths + ' months ≤ ' + maxProbation + ' months max)'
      : 'Probation period exceeds maximum allowed (' + probationMonths + ' months > ' + maxProbation + ' months max)',
    note: 'Contract < 12 months: max 1 month probation\nContract 12-36 months: max 2 months probation\nContract > 36 months: max 6 months probation',
    disclaimer: 'Check local regulations for additional rules.'
  };
}

function calculateCompensation(years, monthlySalary) {
  return years * monthlySalary;
}

module.exports = { checkLaborIssue, calculateCompensation };