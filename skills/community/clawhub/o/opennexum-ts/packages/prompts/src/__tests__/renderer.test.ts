import { describe, it, expect } from 'vitest';
import { renderGeneratorPrompt, renderEvaluatorPrompt, renderRetryPrompt } from '../renderer';
import type { PromptContext } from '../types';
import { existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname_test = dirname(fileURLToPath(import.meta.url));
// src/__tests__ -> src -> packages/prompts -> dist/index.js
const distIndexPath = resolve(__dirname_test, '../../dist/index.js');

const baseContract = {
  id: 'NX-TEST',
  name: 'Test Task',
  type: 'coding' as const,
  scope: {
    files: ['src/foo.ts', 'src/bar.ts'],
  },
  deliverables: ['Deliver X', 'Deliver Y'],
  eval_strategy: {
    criteria: [
      { id: 'C1', desc: 'Output is correct', method: 'unit', threshold: 'pass' },
      { id: 'C2', desc: 'Tests pass', method: 'unit', threshold: 'pass' },
    ],
  },
};

const baseContext: PromptContext = {
  contract: baseContract,
  task: { id: 'NX-TEST', name: 'Test Task' },
  gitCommitCmd: 'git add -- src/foo.ts && git commit -m "feat(nx-test): implement test"',
  evalResultPath: 'nexum/runtime/eval/NX-TEST.json',
  lessons: [],
};

describe('renderGeneratorPrompt', () => {
  it('replaces all template variables with no residual {{...}} placeholders', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).not.toMatch(/\{\{[^}]+\}\}/);
  });

  it('contains task name in output', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).toContain('Test Task');
  });

  it('contains scope files in output', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).toContain('src/foo.ts');
    expect(result).toContain('src/bar.ts');
  });

  it('contains deliverables in output', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).toContain('Deliver X');
    expect(result).toContain('Deliver Y');
  });

  it('contains criteria in output', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).toContain('Output is correct');
  });

  it('contains git commit command in output', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).toContain('git add -- src/foo.ts');
  });

  it('uses generator-coding template for type=coding', () => {
    const result = renderGeneratorPrompt(baseContext);
    // coding template should contain "coding" context
    expect(typeof result).toBe('string');
    expect(result.length).toBeGreaterThan(0);
  });

  it('uses generator-writing template for type=creative', () => {
    const creativeContext: PromptContext = {
      ...baseContext,
      contract: { ...baseContract, type: 'creative' },
    };
    const codingResult = renderGeneratorPrompt(baseContext);
    const writingResult = renderGeneratorPrompt(creativeContext);
    // writing template should differ from coding template
    expect(writingResult).not.toBe(codingResult);
  });

  it('uses generator-coding template for type=task', () => {
    const taskContext: PromptContext = {
      ...baseContext,
      contract: { ...baseContract, type: 'task' },
    };
    const codingResult = renderGeneratorPrompt(baseContext);
    const taskResult = renderGeneratorPrompt(taskContext);
    // task type uses same coding template
    expect(taskResult).toBe(codingResult);
  });

  it('includes lessons when provided', () => {
    const contextWithLessons: PromptContext = {
      ...baseContext,
      lessons: ['Lesson one about X', 'Lesson two about Y'],
    };
    const result = renderGeneratorPrompt(contextWithLessons);
    expect(result).toContain('Lesson one about X');
    expect(result).toContain('Lesson two about Y');
  });

  it('renders without errors when lessons is empty', () => {
    const result = renderGeneratorPrompt(baseContext);
    expect(result).not.toMatch(/\{\{[^}]+\}\}/);
  });
});

describe('renderEvaluatorPrompt', () => {
  it('replaces all template variables with no residual {{...}} placeholders', () => {
    const result = renderEvaluatorPrompt(baseContext);
    expect(result).not.toMatch(/\{\{[^}]+\}\}/);
  });

  it('contains criteria in output', () => {
    const result = renderEvaluatorPrompt(baseContext);
    expect(result).toContain('Output is correct');
    expect(result).toContain('Tests pass');
  });

  it('contains eval result path in output', () => {
    const result = renderEvaluatorPrompt(baseContext);
    expect(result).toContain('nexum/runtime/eval/NX-TEST.json');
  });
});

describe('renderRetryPrompt', () => {
  it('contains verdict in output', () => {
    const result = renderRetryPrompt(baseContext, 'fail', 'The output was wrong', ['C1']);
    expect(result).toContain('fail');
  });

  it('contains feedback in output', () => {
    const result = renderRetryPrompt(baseContext, 'fail', 'The output was wrong', ['C1']);
    expect(result).toContain('The output was wrong');
  });

  it('contains failed criteria list in output', () => {
    const result = renderRetryPrompt(baseContext, 'fail', 'The output was wrong', ['C1', 'C2']);
    expect(result).toContain('C1');
    expect(result).toContain('C2');
  });

  it('includes generator prompt content plus retry block', () => {
    const generatorResult = renderGeneratorPrompt(baseContext);
    const retryResult = renderRetryPrompt(baseContext, 'fail', 'Fix needed', ['C1']);
    expect(retryResult).toContain(generatorResult);
  });

  it('has no residual {{...}} placeholders', () => {
    const result = renderRetryPrompt(baseContext, 'fail', 'Fix needed', ['C1']);
    expect(result).not.toMatch(/\{\{[^}]+\}\}/);
  });
});

describe('built artifact (dist/index.js)', () => {
  it('dist/index.js exists after build', () => {
    expect(existsSync(distIndexPath)).toBe(true);
  });

  it('dist/templates/ directory exists after build', () => {
    const distTemplatesDir = resolve(__dirname_test, '../../dist/templates');
    expect(existsSync(distTemplatesDir)).toBe(true);
  });

  it('renderGeneratorPrompt from built artifact works for coding type', async () => {
    const fileUrl = new URL(`file://${distIndexPath}`).href;
    const mod = await import(/* @vite-ignore */ fileUrl);
    const result = mod.renderGeneratorPrompt(baseContext);
    expect(result).not.toMatch(/\{\{[^}]+\}\}/);
    expect(result).toContain('Test Task');
  });

  it('renderGeneratorPrompt from built artifact works for creative type', async () => {
    const fileUrl = new URL(`file://${distIndexPath}`).href;
    const mod = await import(/* @vite-ignore */ fileUrl);
    const creativeContext: PromptContext = {
      ...baseContext,
      contract: { ...baseContract, type: 'creative' },
    };
    const codingResult = mod.renderGeneratorPrompt(baseContext);
    const writingResult = mod.renderGeneratorPrompt(creativeContext);
    expect(writingResult).not.toBe(codingResult);
    expect(writingResult).not.toMatch(/\{\{[^}]+\}\}/);
  });

  it('renderEvaluatorPrompt from built artifact outputs YAML format', async () => {
    const fileUrl = new URL(`file://${distIndexPath}`).href;
    const mod = await import(/* @vite-ignore */ fileUrl);
    const result = mod.renderEvaluatorPrompt(baseContext);
    expect(result).not.toMatch(/\{\{[^}]+\}\}/);
    expect(result).toContain('yaml');
    expect(result).toContain('verdict');
    expect(result).not.toContain('JSON');
  });

  it('renderRetryPrompt from built artifact includes feedback', async () => {
    const fileUrl = new URL(`file://${distIndexPath}`).href;
    const mod = await import(/* @vite-ignore */ fileUrl);
    const result = mod.renderRetryPrompt(baseContext, 'fail', 'Fix this issue', ['C1']);
    expect(result).toContain('fail');
    expect(result).toContain('Fix this issue');
    expect(result).toContain('C1');
  });
});
