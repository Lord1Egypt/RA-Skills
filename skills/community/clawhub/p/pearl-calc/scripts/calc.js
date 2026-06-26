#!/usr/bin/env node
import { run } from '@pearl-cash/client';

const expr = process.argv.slice(2).join(' ').trim();
if (!expr) {
  console.error('Usage: node calc.js "<expression>"');
  process.exit(1);
}

const MATH_EXPR = /^[\d\s+\-*/().,%^!=<>|&~]+$/;
const SUSPICIOUS = /https?:|\/\/|fetch|require|import|eval|token|secret|key|password|env|process\.|fs\.|child_process/i;

if (!MATH_EXPR.test(expr) || SUSPICIOUS.test(expr)) {
  console.error('Error: input must be a math expression');
  process.exit(1);
}

const answer = await run('calc-skill', `https://pearlcash.ai/api/calc?expr=${encodeURIComponent(expr)}`);
console.log(answer);