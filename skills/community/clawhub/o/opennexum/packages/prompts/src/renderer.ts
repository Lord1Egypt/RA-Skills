import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import type { PromptContext } from './types.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TEMPLATES_DIR = join(__dirname, 'templates');

function loadTemplate(name: string): string {
  return readFileSync(join(TEMPLATES_DIR, name), 'utf-8');
}

function formatList(items: string[]): string {
  return items.map((item) => `- ${item}`).join('\n');
}

function formatDeliverables(deliverables: PromptContext['contract']['deliverables']): string {
  return deliverables
    .map((deliverable) =>
      deliverable.path
        ? `- ${deliverable.path}: ${deliverable.description}`
        : `- ${deliverable.description}`
    )
    .join('\n');
}

function formatCriteria(criteria: PromptContext['contract']['eval_strategy']['criteria']): string {
  return criteria
    .map((criterion) => {
      const details = [
        criterion.method ? `method: ${criterion.method}` : '',
        criterion.threshold ? `threshold: ${criterion.threshold}` : '',
        criterion.weight != null ? `weight: ${criterion.weight}` : '',
      ].filter(Boolean);

      return details.length > 0
        ? `- [${criterion.id}] ${criterion.desc} (${details.join(' ; ')})`
        : `- [${criterion.id}] ${criterion.desc}`;
    })
    .join('\n');
}

function formatLessons(lessons: string[]): string {
  if (lessons.length === 0) return '（无）';
  return lessons.map((l) => `- ${l}`).join('\n');
}

function applyVariables(template: string, vars: Record<string, string>): string {
  return Object.entries(vars).reduce(
    (result, [key, value]) => result.replaceAll(`{{${key}}}`, value),
    template,
  );
}

function isAsciiOnly(value: string): boolean {
  return /^[\x00-\x7F]+$/.test(value);
}

function taskIdToKebabSlug(taskId: string): string {
  return taskId.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function generatorVars(context: PromptContext): Record<string, string> {
  return {
    TASK_NAME: context.task.name,
    TASK_NAME_EN: isAsciiOnly(context.task.name)
      ? context.task.name
      : taskIdToKebabSlug(context.task.id),
    TASK_ID: context.task.id,
    PROJECT_DIR: context.projectDir ?? process.cwd(),
    SCOPE_FILES: formatList(context.contract.scope.files),
    DELIVERABLES: formatDeliverables(context.contract.deliverables),
    CRITERIA_PREVIEW: formatCriteria(context.contract.eval_strategy.criteria),
    GIT_COMMIT_CMD: context.gitCommitCmd,
    EVAL_RESULT_PATH: context.evalResultPath,
    FIELD_REPORT_PATH: context.fieldReportPath,
    RELEVANT_LESSONS: formatLessons(context.lessons),
  };
}

export function renderGeneratorPrompt(context: PromptContext): string {
  const template = loadTemplate('generator.md');
  return applyVariables(template, generatorVars(context));
}

export function renderEvaluatorPrompt(context: PromptContext): string {
  const template = loadTemplate('evaluator.md');
  return applyVariables(template, {
    TASK_NAME: context.task.name,
    SCOPE_FILES: formatList(context.contract.scope.files),
    DELIVERABLES: formatDeliverables(context.contract.deliverables),
    CRITERIA_PREVIEW: formatCriteria(context.contract.eval_strategy.criteria),
    EVAL_RESULT_PATH: context.evalResultPath,
    FIELD_REPORT_PATH: context.fieldReportPath,
    TASK_ID: context.contract.id,
    PROJECT_DIR: context.projectDir ?? '',
  });
}

export function renderRetryPrompt(
  context: PromptContext,
  verdict: string,
  feedback: string,
  failedCriteria: string[],
): string {
  const generatorPrompt = renderGeneratorPrompt(context);
  const retryBlock = [
    '',
    '---',
    '',
    '## Retry Context',
    '',
    `**Verdict:** ${verdict}`,
    '',
    `**Feedback:** ${feedback}`,
    '',
    '**Failed Criteria:**',
    failedCriteria.map((c) => `- ${c}`).join('\n'),
    '',
    '请根据以上反馈重新实现，确保所有失败的 criteria 得到修复。',
  ].join('\n');

  return generatorPrompt + retryBlock;
}
