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

function formatCriteria(criteria: PromptContext['contract']['eval_strategy']['criteria']): string {
  return criteria
    .map((c) => `- [${c.id}] ${c.desc} (method: ${c.method} ; threshold: ${c.threshold})`)
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

function generatorVars(context: PromptContext): Record<string, string> {
  return {
    TASK_NAME: context.task.name,
    SCOPE_FILES: formatList(context.contract.scope.files),
    DELIVERABLES: formatList(context.contract.deliverables),
    CRITERIA_PREVIEW: formatCriteria(context.contract.eval_strategy.criteria),
    GIT_COMMIT_CMD: context.gitCommitCmd,
    EVAL_RESULT_PATH: context.evalResultPath,
    RELEVANT_LESSONS: formatLessons(context.lessons),
  };
}

export function renderGeneratorPrompt(context: PromptContext): string {
  const isWriting = context.contract.type === 'creative';
  const templateName = isWriting ? 'generator-writing.md' : 'generator-coding.md';
  const template = loadTemplate(templateName);
  return applyVariables(template, generatorVars(context));
}

export function renderEvaluatorPrompt(context: PromptContext): string {
  const template = loadTemplate('evaluator.md');
  return applyVariables(template, {
    CRITERIA_PREVIEW: formatCriteria(context.contract.eval_strategy.criteria),
    EVAL_RESULT_PATH: context.evalResultPath,
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
