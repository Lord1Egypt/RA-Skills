#!/usr/bin/env node
/**
 * inject-spawn-requirements.js
 *
 * Injects mandatory PR/test/review requirements into code spawn tasks.
 * Called by spawn-code-subagent.lobster after detect-code-task.js.
 *
 * Configuration (via skill config.json → spawnTaskInjection):
 *   rulesTemplatePath            - Optional path to the injected rules template
 *   detectionKeywords.ui        - Optional UI-work keyword list
 *   sections.paperclipIssue     - Toggle Paperclip issue section
 *   sections.problemSolving     - Toggle rules template section
 *   sections.prRequirements     - Toggle PR/test requirements section
 *   sections.uiNudge            - Toggle UX design nudge section
 *
 * Input (via env):
 *   TASK            - Original task description
 *   IS_CODE_TASK    - "true" if code work detected (from detect-code-task.js)
 *   PROJECT_ID      - Optional Paperclip project UUID for auto-created issues
 *   ISSUE_PRIORITY  - Optional Paperclip issue priority (critical|high|medium|low)
 *
 * Output (stdout JSON):
 *   {
 *     enhancedTask: string,
 *     enhancedTaskPath: string,
 *     injected: bool,
 *     requirements: string[],
 *     paperclip: { issueId, identifier, title, created } | null
 *   }
 *
 * Side effect:
 *   Writes the enhanced task to a temp file (for @file passthrough to spawn-with-fallback.js)
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { ensurePaperclipIssue } = require('./lib/paperclip-issue-gate');
const { getSpawnTaskInjectionConfig } = require('./lib/spawn-task-injection-config');

const task = process.env.TASK || '';
const isCodeTask = process.env.IS_CODE_TASK === 'true';
const projectId = (process.env.PROJECT_ID || '').trim() || undefined;
const priority = (process.env.ISSUE_PRIORITY || '').trim() || undefined;
const injectionConfig = getSpawnTaskInjectionConfig();

function loadRulesTemplate(rulesTemplatePath = injectionConfig.rulesTemplatePath) {
  try {
    if (!rulesTemplatePath || !fs.existsSync(rulesTemplatePath)) return '';
    return fs.readFileSync(rulesTemplatePath, 'utf8');
  } catch {
    return '';
  }
}

function buildProblemSolvingSection(rulesTemplate, rulesTemplatePath = injectionConfig.rulesTemplatePath) {
  if (!rulesTemplate) return '';

  const templateLabel = path.basename(rulesTemplatePath || 'rules template');
  return `

---
## 📋 Problem-Solving (auto-loaded from ${templateLabel})

${rulesTemplate}
`;
}

function buildIssueSection(paperclip) {
  if (!paperclip) return '';

  return `

---
## 🎫 Paperclip Issue (required)

- Issue identifier: ${paperclip.identifier}
- Issue ID: ${paperclip.issueId}
- Issue title: ${paperclip.title}
- Issue source: ${paperclip.created ? 'auto-created before spawn' : 'existing issue referenced by task'}

Branch naming requirement: your git branch MUST include ${paperclip.identifier} (example: ${paperclip.identifier}/short-slug).
PR requirement: reference ${paperclip.identifier} in the PR title or body.
`;
}

function detectUiTask(taskText, uiKeywords = injectionConfig.detectionKeywords.ui) {
  const lower = taskText.toLowerCase();
  const hits = uiKeywords.filter((kw) => lower.includes(kw.toLowerCase()));
  return { isUiTask: hits.length > 0, hits };
}

function buildUiNudge(uiDetection) {
  if (!uiDetection.isUiTask) return '';
  return `

---
## ⚠️ UI Work Detected — UX Design Pass Required

This task touches user-facing interface work (detected: ${uiDetection.hits.slice(0, 5).join(', ')}).
Before implementing AND before signoff, adopt the BMAD-method UX designer lens:
- **Primary flow:** What is the user journey and success state?
- **States:** Empty, loading, error, and edge states covered?
- **Copy:** Labels, instructions, and calls to action clear?
- **Responsive:** Mobile and responsive behavior addressed?
- **Accessibility:** Visual hierarchy and accessibility considered?

Do not treat a screen as done just because it compiles — it must make sense to a real person.
`;
}

function buildPrRequirements(paperclip) {
  const identifier = paperclip?.identifier || 'SUP-XX';

  return `

---
## ⚠️ Required Deliverables

These requirements are non-negotiable and apply to ALL code changes:

1. **Feature branch** — all changes on a dedicated branch, never commit directly to \`main\`
2. **Branch naming** — branch name must include \`${identifier}\` (example: \`${identifier}/short-slug\`)
3. **One feature per PR** — no bundling unrelated changes; if you find separate issues, create separate branches/PRs
4. **Create a PR** — use \`gh pr create\` when work is complete; do not leave changes unsubmitted
5. **Tests must pass** — run existing tests before submitting; fix failures before requesting review
6. **PR review required** — wait for clean review from Codex or CodeRabbit before merging
7. **Fix ALL review comments** — resolve every P1/P2 (Critical/High) comment before merge; never merge with unresolved critical issues
8. **CI must be green** — all required checks must pass before merge
9. **Blocker routing** — if you hit a blocker or need-Andrew item, write it to Project Board + Live Plan + Tasks.md + today's journal; do NOT report completion until all 4 are written

**Completion report must include:**
- Paperclip issue: ${identifier}
- Branch name and PR number (or reason if no PR needed)
- Test results summary
- Any unresolved issues or blockers
`;
}

const REQUIREMENTS_LIST = [
  'Paperclip issue required before code spawn',
  'Feature branch required (never commit to main)',
  'Branch name must include issue identifier',
  'One feature per PR',
  'gh pr create when done',
  'Tests pass before review',
  'PR review from Codex or CodeRabbit',
  'Fix P1/P2 comments before merge',
  'CI must be green',
  'Blocker routing to 4 artifacts',
];

function buildEnhancedTask({
  taskText,
  isCodeTask,
  paperclip,
  rulesTemplate,
  config = injectionConfig,
}) {
  const uiDetection = detectUiTask(taskText, config.detectionKeywords.ui);
  const sections = [];

  if (isCodeTask && config.sections.paperclipIssue) {
    sections.push(buildIssueSection(paperclip));
  }

  if (isCodeTask && config.sections.problemSolving) {
    sections.push(buildProblemSolvingSection(rulesTemplate, config.rulesTemplatePath));
  }

  if (isCodeTask && config.sections.prRequirements) {
    sections.push(buildPrRequirements(paperclip));
  }

  if (config.sections.uiNudge) {
    sections.push(buildUiNudge(uiDetection));
  }

  return taskText + sections.join('');
}

async function run({
  taskText = task,
  codeTask = isCodeTask,
  codeProjectId = projectId,
  issuePriority = priority,
  config = injectionConfig,
} = {}) {
  let paperclip = null;

  if (codeTask) {
    paperclip = await ensurePaperclipIssue({
      task: taskText,
      projectId: codeProjectId,
      priority: issuePriority,
    });
  }

  const rulesTemplate = config.sections.problemSolving
    ? loadRulesTemplate(config.rulesTemplatePath)
    : '';

  const enhancedTask = buildEnhancedTask({
    taskText,
    isCodeTask: codeTask,
    paperclip,
    rulesTemplate,
    config,
  });

  const requirements = codeTask ? REQUIREMENTS_LIST : [];

  const tmpPath = path.join(os.tmpdir(), `spawn-task-${Date.now()}.txt`);
  fs.writeFileSync(tmpPath, enhancedTask, 'utf8');

  return {
    enhancedTask,
    enhancedTaskPath: tmpPath,
    injected: codeTask,
    requirements,
    paperclip,
  };
}

async function main() {
  const result = await run();
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  process.exit(0);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(JSON.stringify({
      error: err.message,
      taskPreview: task.slice(0, 160),
      isCodeTask,
    }));
    process.exit(1);
  });
}

module.exports = {
  REQUIREMENTS_LIST,
  buildEnhancedTask,
  buildIssueSection,
  buildProblemSolvingSection,
  buildPrRequirements,
  buildUiNudge,
  detectUiTask,
  loadRulesTemplate,
  run,
};
