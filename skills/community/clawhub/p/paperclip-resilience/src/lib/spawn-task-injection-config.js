#!/usr/bin/env node
/**
 * spawn-task-injection-config.js
 *
 * Resolves configuration for task injection from the skill config
 * with safe defaults. Self-contained version for the paperclip-resilience skill.
 */

'use strict';

const os = require('os');
const path = require('path');
const { getConfig, SKILL_ROOT } = require('./config');

const DEFAULT_UI_KEYWORDS = [
  'ui', 'ux', 'screen', 'page', 'layout', 'component', 'form', 'button',
  'modal', 'dialog', 'navigation', 'dashboard', 'landing page', 'onboarding',
  'responsive', 'mobile', 'empty state', 'error state', 'loading state',
  'sidebar', 'header', 'footer', 'card', 'table view', 'list view',
  'settings page', 'profile page', 'sign up', 'sign in', 'login',
];

const DEFAULT_SECTIONS = {
  paperclipIssue: true,
  problemSolving: true,
  prRequirements: true,
  uiNudge: true,
};

function expandTilde(value) {
  if (typeof value !== 'string') return value;
  if (value === '~') return os.homedir();
  if (value.startsWith('~/') || value.startsWith('~\\')) {
    return path.join(os.homedir(), value.slice(2));
  }
  return value;
}

function normalizeStringArray(value, fallback) {
  if (!Array.isArray(value)) return [...fallback];
  const normalized = value
    .filter((entry) => typeof entry === 'string')
    .map((entry) => entry.trim())
    .filter(Boolean);
  return normalized.length > 0 ? normalized : [...fallback];
}

function normalizeSections(value) {
  const sections = { ...DEFAULT_SECTIONS };
  if (!value || typeof value !== 'object' || Array.isArray(value)) return sections;
  for (const key of Object.keys(DEFAULT_SECTIONS)) {
    if (typeof value[key] === 'boolean') {
      sections[key] = value[key];
    }
  }
  return sections;
}

function resolveTemplatePath(rawPath, workspaceRoot = SKILL_ROOT) {
  const fallback = path.join(workspaceRoot, 'PROBLEM-SOLVING.md');
  if (typeof rawPath !== 'string' || rawPath.trim() === '') return fallback;
  const expanded = expandTilde(rawPath.trim());
  if (path.isAbsolute(expanded)) return expanded;
  return path.resolve(workspaceRoot, expanded);
}

function resolveSpawnTaskInjectionConfig(config = getConfig(), workspaceRoot = SKILL_ROOT) {
  const raw = (config && typeof config.spawnTaskInjection === 'object' && config.spawnTaskInjection) || {};
  const detectionKeywords =
    raw.detectionKeywords && typeof raw.detectionKeywords === 'object' && !Array.isArray(raw.detectionKeywords)
      ? raw.detectionKeywords
      : {};

  return {
    rulesTemplatePath: resolveTemplatePath(raw.rulesTemplatePath, workspaceRoot),
    detectionKeywords: {
      ui: normalizeStringArray(detectionKeywords.ui, DEFAULT_UI_KEYWORDS),
    },
    sections: normalizeSections(raw.sections),
  };
}

function getSpawnTaskInjectionConfig() {
  return resolveSpawnTaskInjectionConfig(getConfig(), SKILL_ROOT);
}

module.exports = {
  DEFAULT_SECTIONS,
  DEFAULT_UI_KEYWORDS,
  expandTilde,
  getSpawnTaskInjectionConfig,
  normalizeSections,
  normalizeStringArray,
  resolveSpawnTaskInjectionConfig,
  resolveTemplatePath,
};
