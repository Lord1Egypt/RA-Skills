#!/usr/bin/env node
/**
 * paperclip-issue-gate.js — Ensures every code subagent spawn has a Paperclip issue.
 *
 * Self-contained version for the paperclip-resilience skill.
 *
 * Environment:
 *   PAPERCLIP_API_URL     — Paperclip API base URL (required)
 *   PAPERCLIP_API_KEY     — Paperclip API key (required)
 *   PAPERCLIP_COMPANY_ID  — Paperclip company UUID (required)
 *   PAPERCLIP_AGENT_ID    — Paperclip agent UUID (optional, for assignment)
 *   PAPERCLIP_PROJECT_ID  — Default project UUID (optional)
 */

'use strict';

function loadEnv() {
  return {
    apiUrl: (process.env.PAPERCLIP_API_URL || '').replace(/\/$/, ''),
    apiKey: process.env.PAPERCLIP_API_KEY || '',
    companyId: process.env.PAPERCLIP_COMPANY_ID || '',
    agentId: process.env.PAPERCLIP_AGENT_ID || '',
  };
}

/**
 * Extracts a Paperclip issue identifier from text.
 * Pattern: 2-6 uppercase letters, hyphen, 1-6 digits (e.g., SUP-123, ATP-456789)
 * Returns null if no valid identifier found.
 */
function extractIssueIdentifier(text) {
  if (!text || typeof text !== 'string') return null;
  // Limit search length to prevent ReDoS on huge inputs
  const searchText = text.slice(0, 10000);
  const match = searchText.match(/\b([A-Z]{2,6}-\d{1,6})\b/);
  return match ? match[1] : null;
}

async function apiFetch(env, method, apiPath, body) {
  const url = `${env.apiUrl}/api${apiPath}`;
  const headers = {
    'Authorization': `Bearer ${env.apiKey}`,
    'Content-Type': 'application/json',
  };

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const resp = await fetch(url, opts);
  const text = await resp.text();

  if (!resp.ok) {
    throw new Error(`Paperclip API ${method} ${apiPath}: ${resp.status} — ${text.slice(0, 200)}`);
  }

  return text ? JSON.parse(text) : null;
}

async function getIssueByIdentifier(env, identifier) {
  try {
    const data = await apiFetch(env, 'GET', `/issues/${identifier}`);
    return {
      id: data.id,
      identifier: data.identifier,
      title: data.title,
      status: data.status,
    };
  } catch (err) {
    if (err.message.includes('404')) return null;
    throw err;
  }
}

/**
 * Sanitizes a string for safe inclusion in API requests.
 * Removes control characters and limits length.
 */
function sanitizeApiString(value, maxLength = 1024) {
  if (typeof value !== 'string') return '';
  // Remove control characters except newlines/tabs
  const cleaned = value.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  return cleaned.slice(0, maxLength);
}

/**
 * Validates priority value against allowed values.
 */
function validatePriority(priority) {
  const ALLOWED_PRIORITIES = ['critical', 'high', 'medium', 'low'];
  const normalized = String(priority || 'medium').toLowerCase();
  return ALLOWED_PRIORITIES.includes(normalized) ? normalized : 'medium';
}

async function createIssue(env, { title, description, projectId, priority }) {
  const defaultProjectId = process.env.PAPERCLIP_PROJECT_ID || '';

  // Sanitize inputs before sending to API
  const sanitizedTitle = sanitizeApiString(title, 256);
  const sanitizedDescription = sanitizeApiString(description, 10000);
  const validatedPriority = validatePriority(priority);

  if (!sanitizedTitle) {
    throw new Error('Issue title is required and cannot be empty');
  }

  const body = {
    title: sanitizedTitle,
    description: sanitizedDescription,
    projectId: projectId || defaultProjectId || undefined,
    priority: validatedPriority,
    status: 'todo',
    assigneeAgentId: env.agentId || undefined,
  };

  if (!body.projectId) {
    delete body.projectId;
  }

  const data = await apiFetch(env, 'POST', `/companies/${env.companyId}/issues`, body);
  return {
    id: data.id,
    identifier: data.identifier,
    title: data.title,
    status: data.status,
  };
}

async function ensurePaperclipIssue({ task, identifier, projectId, priority }) {
  const env = loadEnv();

  if (!env.apiUrl) {
    throw new Error('PAPERCLIP_API_URL not configured. Cannot enforce issue gate.');
  }
  if (!env.apiKey) {
    throw new Error('PAPERCLIP_API_KEY not configured. Cannot enforce issue gate.');
  }
  if (!env.companyId) {
    throw new Error('PAPERCLIP_COMPANY_ID not configured. Cannot enforce issue gate.');
  }

  // Validate and sanitize task input
  if (!task || typeof task !== 'string') {
    throw new Error('Task description is required');
  }
  const sanitizedTask = sanitizeApiString(task, 10000);

  const ref = identifier || extractIssueIdentifier(sanitizedTask);

  if (ref) {
    const existing = await getIssueByIdentifier(env, ref);
    if (existing) {
      return {
        issueId: existing.id,
        identifier: existing.identifier,
        title: existing.title,
        created: false,
      };
    }
    console.error(`⚠️  Referenced issue ${ref} not found. Creating new issue.`);
  }

  const issueTitle = sanitizedTask.length > 120 ? sanitizedTask.slice(0, 117) + '...' : sanitizedTask;
  const issue = await createIssue(env, {
    title: issueTitle,
    description: `## Auto-created by issue gate\n\nOriginal task:\n> ${sanitizedTask}\n\nCreated automatically before spawning a code subagent.`,
    projectId,
    priority: priority || 'medium',
  });

  return {
    issueId: issue.id,
    identifier: issue.identifier,
    title: issue.title,
    created: true,
  };
}

module.exports = {
  ensurePaperclipIssue,
  extractIssueIdentifier,
  getIssueByIdentifier,
  sanitizeApiString,
  validatePriority,
};
