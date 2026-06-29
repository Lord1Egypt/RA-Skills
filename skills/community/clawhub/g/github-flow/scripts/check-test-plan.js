/**
 * Check PR body for incomplete Test Plan checkboxes.
 * Rules:
 * - [general] / [일반] or [UI] checkboxes must be checked ([x]).
 * - [post-merge] / [머지 후] / [deploy] checkboxes are allowed to be incomplete ([ ]).
 * - Checkboxes without prefix are treated as [general] and must be checked.
 * - Auto-generated checkboxes (e.g. CI, lint) are not part of manually checked plans but if they exist, they must be checked unless post-merge.
 */

const fs = require('fs');

function checkBody(body) {
  const lines = body.split('\n');
  let inTestPlan = false;
  const incomplete = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Section entry — "Test Plan" / "Test plan" / "체크리스트"
    if (line.match(/^##?\s*Test\s*[pP]lan/i) || line.match(/^##?\s*체크리스트/i)) {
      inTestPlan = true;
      continue;
    }

    // Heading exit (except sub-headings inside Test Plan if any)
    if (line.match(/^##?\s+/) && inTestPlan) {
      // If it's a completely new major section, we might have left the Test Plan.
      // But usually Test Plan goes until the end or next main heading.
      // We will check if the heading is not related to Test Plan
      if (!line.match(/test/i) && !line.match(/check/i) && !line.match(/검증/i)) {
        inTestPlan = false;
      }
    }

    // Match unchecked checkbox: - [ ] or * [ ]
    const checkboxMatch = line.match(/^[-*]\s*\[\s*\]\s*(.*)/);
    if (checkboxMatch) {
      const content = checkboxMatch[1].trim();

      // Post-merge and deploy items are explicitly allowed to remain unchecked.
      // Accept both the English prefix ([post-merge]) and the legacy Korean
      // prefix ([머지 후]), with or without surrounding backticks. [deploy]
      // is treated like [post-merge] per merge.md prefix table.
      const isPostMerge =
        content.includes('[post-merge]') || content.includes('`[post-merge]`') ||
        content.includes('[머지 후]') || content.includes('`[머지 후]`') ||
        content.includes('[deploy]') || content.includes('`[deploy]`');

      if (!isPostMerge && inTestPlan) {
        incomplete.push({
          lineNum: i + 1,
          content: content
        });
      }
    }
  }

  return incomplete;
}

function runMain(body) {
  const incompleteItems = checkBody(body);

  if (incompleteItems.length > 0) {
    console.error('❌ Incomplete Test Plan checkboxes found (excluding [post-merge] / [머지 후] / [deploy] items):');
    incompleteItems.forEach(item => {
      console.error(`  Line ${item.lineNum}: ${item.content}`);
    });
    process.exit(1);
  } else {
    console.log('✅ All required Test Plan checkboxes are completed!');
    process.exit(0);
  }
}

// Support three invocation forms:
//   1. PR_BODY environment variable (used by GitHub Actions)
//   2. File path as first CLI argument (used in local scripts)
//   3. Piped body via stdin (used by `gh pr view ... | node check-test-plan.js`)
if (require.main === module) {
  if (process.env.PR_BODY) {
    runMain(process.env.PR_BODY);
  } else if (process.argv[2]) {
    const filePath = process.argv[2];
    if (fs.existsSync(filePath)) {
      runMain(fs.readFileSync(filePath, 'utf8'));
    } else {
      console.error(`File not found: ${filePath}`);
      process.exit(1);
    }
  } else if (!process.stdin.isTTY) {
    // Read piped stdin (no env, no argv, stdin is not a TTY → pipe input).
    let body = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { body += chunk; });
    process.stdin.on('end', () => { runMain(body); });
  } else {
    console.error('Usage: node check-test-plan.js <path_to_pr_body_file>');
    console.error('       set PR_BODY env var, or pipe the PR body via stdin');
    process.exit(1);
  }
}

module.exports = { checkBody };
