/**
 * Labor Dispute Check - Test Suite
 */

const { checkLaborIssue, calculateCompensation } = require('./scripts/labor-checker.js');

const TEST_CASES = [
  {
    name: 'Empty input',
    input: null,
    expectError: true
  },
  {
    name: 'Termination compensation - 3 years',
    input: {
      issue: 'termination',
      years: 3,
      monthlySalary: 10000
    },
    expectSuccess: true,
    expectCompensation: 30000
  },
  {
    name: 'Overtime calculation',
    input: {
      issue: 'overtime',
      hours: 10,
      monthlySalary: 10000
    },
    expectSuccess: true
  },
  {
    name: 'Probation period check - valid',
    input: {
      issue: 'probation',
      contractMonths: 12,
      probationMonths: 2
    },
    expectSuccess: true,
    expectValid: true
  },
  {
    name: 'Probation period check - invalid',
    input: {
      issue: 'probation',
      contractMonths: 6,
      probationMonths: 3
    },
    expectSuccess: true,
    expectValid: false
  }
];

function runTests() {
  console.log('=== Labor Dispute Check Test Suite ===\n');
  
  let passed = 0;
  let failed = 0;

  for (const testCase of TEST_CASES) {
    process.stdout.write('Test: ' + testCase.name + ' ... ');
    
    try {
      const result = checkLaborIssue(testCase.input);
      let testPassed = true;
      let failReason = '';

      if (testCase.expectError) {
        if (!result.error) {
          testPassed = false;
          failReason = 'Expected error but got none';
        }
      } else if (testCase.expectSuccess) {
        if (result.error) {
          testPassed = false;
          failReason = 'Unexpected error: ' + result.error;
        } else {
          if (testCase.expectCompensation && result.compensation !== testCase.expectCompensation) {
            testPassed = false;
            failReason = 'Expected compensation ' + testCase.expectCompensation + ', got ' + result.compensation;
          }
          if (testCase.expectValid !== undefined && result.valid !== testCase.expectValid) {
            testPassed = false;
            failReason = 'Expected valid=' + testCase.expectValid + ', got ' + result.valid;
          }
        }
      }

      if (testPassed) {
        console.log('✓ PASS');
        passed++;
      } else {
        console.log('✗ FAIL: ' + failReason);
        failed++;
      }
    } catch (err) {
      console.log('✗ ERROR: ' + err.message);
      failed++;
    }
  }

  console.log('\n=== Test Summary ===');
  console.log('Passed: ' + passed + '/' + TEST_CASES.length);
  console.log('Failed: ' + failed + '/' + TEST_CASES.length);
  
  if (failed === 0) {
    console.log('\n✓ All tests passed!');
    process.exit(0);
  } else {
    console.log('\n✗ Some tests failed');
    process.exit(1);
  }
}

if (require.main === module) {
  runTests();
}

module.exports = { runTests, TEST_CASES };