#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';

function has(filePath) {
  return existsSync(filePath);
}

function read(filePath) {
  return readFileSync(filePath, 'utf-8');
}

function safeCountLines(filePath) {
  if (!has(filePath)) return 0;
  return read(filePath).split('\n').length;
}

function scoreSkill(skillDir) {
  const result = {
    score: 0,
    passed: [],
    failed: [],
    details: {}
  };

  const skillMd = join(skillDir, 'SKILL.md');
  const refs = join(skillDir, 'references');
  const templates = join(skillDir, 'assets', 'templates');
  const checklists = join(skillDir, 'assets', 'checklists');
  const evals = join(skillDir, 'assets', 'evals');
  const onboardingRef = join(skillDir, 'references', 'onboarding-zero-to-one.md');
  const firstExercise = join(skillDir, 'assets', 'templates', 'first-skill-exercise.md');

  const checks = [
    { key: 'skill_md_exists', points: 10, ok: has(skillMd), msg: '存在 SKILL.md' },
    { key: 'references_exists', points: 8, ok: has(refs), msg: '存在 references/' },
    { key: 'templates_exists', points: 8, ok: has(templates), msg: '存在 assets/templates/' },
    { key: 'checklists_exists', points: 8, ok: has(checklists), msg: '存在 assets/checklists/' },
    { key: 'evals_exists', points: 8, ok: has(evals), msg: '存在 assets/evals/' },
    { key: 'onboarding_ref_exists', points: 6, ok: has(onboardingRef), msg: '存在 onboarding 引导文档' },
    { key: 'first_exercise_exists', points: 4, ok: has(firstExercise), msg: '存在首个练习模板' },
  ];

  for (const check of checks) {
    if (check.ok) {
      result.score += check.points;
      result.passed.push(`${check.msg} (+${check.points})`);
    } else {
      result.failed.push(`${check.msg} (0)`);
    }
    result.details[check.key] = check.ok;
  }

  if (has(skillMd)) {
    const content = read(skillMd);
    const lineCount = safeCountLines(skillMd);

    const frontmatterOk = content.startsWith('---');
    const hasName = /^name:\s*[a-z0-9-]+/m.test(content);
    const hasDescription = /^description:\s*.+/m.test(content);
    const hasFlow = /执行流程|workflow|步骤/i.test(content);
    const hasSafety = /安全|risk|approval|确认/i.test(content);

    const contentChecks = [
      { key: 'frontmatter', points: 10, ok: frontmatterOk, msg: '有 frontmatter' },
      { key: 'name', points: 6, ok: hasName, msg: '有 name 字段' },
      { key: 'description', points: 6, ok: hasDescription, msg: '有 description 字段' },
      { key: 'flow', points: 10, ok: hasFlow, msg: '有流程定义' },
      { key: 'safety', points: 10, ok: hasSafety, msg: '有安全约束' },
      { key: 'line_budget', points: 6, ok: lineCount <= 500, msg: 'SKILL.md <= 500 行' }
    ];

    for (const check of contentChecks) {
      if (check.ok) {
        result.score += check.points;
        result.passed.push(`${check.msg} (+${check.points})`);
      } else {
        result.failed.push(`${check.msg} (0)`);
      }
      result.details[check.key] = check.ok;
    }

    result.details.skill_md_lines = lineCount;
  }

  // Bonus: supporting files count (max 8 points)
  let supportFileCount = 0;
  const supportDirs = [refs, templates, checklists, evals];
  for (const dir of supportDirs) {
    if (!has(dir)) continue;
    for (const name of readdirSync(dir)) {
      const full = join(dir, name);
      if (statSync(full).isFile()) supportFileCount += 1;
    }
  }
  const bonus = Math.min(8, supportFileCount * 2);
  result.score += bonus;
  result.details.support_files = supportFileCount;
  if (bonus > 0) {
    result.passed.push(`supporting files 数量奖励 (+${bonus})`);
  }

  result.level =
    result.score >= 90 ? 'L4-Production' :
    result.score >= 75 ? 'L3-Advanced' :
    result.score >= 55 ? 'L2-Intermediate' : 'L1-Basic';

  return result;
}

function main() {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('Usage: node scripts/score-skill.js <skill-dir>');
    process.exit(1);
  }

  const target = resolve(process.cwd(), inputPath);
  if (!has(target)) {
    console.error(`Skill directory not found: ${target}`);
    process.exit(1);
  }

  const report = scoreSkill(target);
  console.log(JSON.stringify(report, null, 2));
}

main();