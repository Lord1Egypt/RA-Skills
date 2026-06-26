/**
 * src/git.js
 * Parse git commit messages and sync Linear issue states.
 *
 * Supported commit message patterns (case-insensitive):
 *   fixes ENG-42
 *   fix ENG-42
 *   closes ENG-42
 *   close ENG-42
 *   resolves ENG-42
 *   resolve ENG-42
 *   fixed ENG-42
 *   closed ENG-42
 *   resolved ENG-42
 *
 * Multiple references in one commit are supported:
 *   "Fix login bug (fixes ENG-42, closes ENG-55)"
 *
 * Generic #number references are also detected when teamId is supplied:
 *   "fixes #42" → resolves to <teamKey>-42
 */

'use strict';

const { resolveIssueId, getIssue } = require('./issues');
const { resolveStateName }          = require('./workflow');

// Regex for named identifiers: fixes ENG-42, closes AUTH-7, etc.
const NAMED_REF_RE = /\b(?:fix(?:e[sd])?|clos(?:e[sd])?|resolv(?:e[sd]?)?)\s+([A-Z][A-Z0-9]+-\d+)\b/gi;

// Regex for #number refs: fixes #42 (requires teamId/teamKey to resolve)
const NUMBER_REF_RE = /\b(?:fix(?:e[sd])?|clos(?:e[sd])?|resolv(?:e[sd]?)?)\s+#(\d+)\b/gi;

// ---------------------------------------------------------------------------
// parseCommitMessage
// ---------------------------------------------------------------------------

/**
 * Parse a git commit message and extract all referenced Linear issue identifiers.
 *
 * @param {string} message   - Full commit message
 * @param {string} [teamKey] - Team key (e.g. "ENG") for resolving bare #number refs
 * @returns {{ identifiers: string[], rawNumbers: string[] }}
 */
function parseCommitMessage(message, teamKey) {
  const identifiers = new Set();
  const rawNumbers  = [];

  let match;

  // Reset regex state (global flag)
  NAMED_REF_RE.lastIndex = 0;
  while ((match = NAMED_REF_RE.exec(message)) !== null) {
    identifiers.add(match[1].toUpperCase());
  }

  NUMBER_REF_RE.lastIndex = 0;
  while ((match = NUMBER_REF_RE.exec(message)) !== null) {
    const num = match[1];
    if (teamKey) {
      identifiers.add(`${teamKey.toUpperCase()}-${num}`);
    } else {
      rawNumbers.push(num);
    }
  }

  return {
    identifiers: Array.from(identifiers),
    rawNumbers,  // unresolvable without a teamKey
  };
}

// ---------------------------------------------------------------------------
// syncFromCommit
// ---------------------------------------------------------------------------

/**
 * Parse a commit message, find referenced issues, and move them to a "done" state.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}  params.message   - Git commit message
 * @param {string} [params.teamId]   - Team UUID (used to look up the "done" state)
 * @param {string} [params.teamKey]  - Team key (e.g. "ENG") — auto-detected from first found issue if omitted
 * @param {string} [params.doneState='Done'] - Name of the target state for resolved issues
 * @returns {Promise<object>}
 */
async function syncFromCommit(client, params) {
  const { message, teamId, doneState = 'Done' } = params;

  if (!message || !message.trim()) {
    throw new Error('"message" is required for sync-commit.');
  }

  // If teamId provided, fetch team key for #number resolution
  let teamKey = params.teamKey;
  if (teamId && !teamKey) {
    const teamQuery = `
      query GetTeamKey($id: String!) {
        team(id: $id) { key }
      }
    `;
    const td = await client.request(teamQuery, { id: teamId });
    teamKey = td.team?.key;
  }

  const { identifiers, rawNumbers } = parseCommitMessage(message, teamKey);

  const result = {
    success: true,
    message,
    identifiersFound: identifiers,
    unresolvableRefs: rawNumbers.length > 0
      ? rawNumbers.map((n) => `#${n}`)
      : [],
    updated: [],
    errors: [],
  };

  if (identifiers.length === 0) {
    result.message_parsed = 'No Linear issue references found in commit message.';
    return result;
  }

  // Process each referenced issue
  for (const identifier of identifiers) {
    try {
      // Fetch the issue to get its team (needed to resolve state)
      const issueResult = await getIssue(client, { id: identifier });
      const issue = issueResult.data;

      // If we don't have a teamId yet, infer it from the issue
      const effectiveTeamId = teamId || issue.team?.id;
      if (!effectiveTeamId) {
        throw new Error(`Cannot determine teamId for issue ${identifier}`);
      }

      // Resolve the target state name to an ID
      const stateId = await resolveStateName(client, effectiveTeamId, doneState);

      // Skip if already in that state
      if (issue.state?.id === stateId) {
        result.updated.push({
          identifier,
          title:  issue.title,
          action: 'skipped',
          reason: `Already in state "${doneState}"`,
        });
        continue;
      }

      // Skip if already completed/cancelled
      if (issue.completedAt || issue.canceledAt) {
        result.updated.push({
          identifier,
          title:  issue.title,
          action: 'skipped',
          reason: 'Issue is already completed or cancelled',
        });
        continue;
      }

      // Move the issue
      const mutation = `
        mutation SyncIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) {
            success
            issue {
              id
              identifier
              title
              state { name type }
              url
            }
          }
        }
      `;

      const data = await client.request(mutation, {
        id:    issue.id,
        input: { stateId },
      });

      if (!data.issueUpdate.success) {
        throw new Error('issueUpdate returned success=false');
      }

      const updated = data.issueUpdate.issue;
      result.updated.push({
        identifier: updated.identifier,
        title:      updated.title,
        action:     'moved',
        newState:   updated.state.name,
        url:        updated.url,
      });

    } catch (err) {
      result.errors.push({
        identifier,
        error: err.message,
      });
    }
  }

  result.success = result.errors.length === 0;
  result.summary = buildSyncSummary(result);

  return result;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function buildSyncSummary({ identifiersFound, updated, errors, unresolvableRefs }) {
  const moved   = updated.filter((u) => u.action === 'moved');
  const skipped = updated.filter((u) => u.action === 'skipped');
  const parts   = [];

  if (identifiersFound.length === 0) {
    return 'No issue references found.';
  }

  parts.push(`Found ${identifiersFound.length} issue reference${identifiersFound.length === 1 ? '' : 's'}.`);

  if (moved.length)   parts.push(`Moved ${moved.length} to done.`);
  if (skipped.length) parts.push(`${skipped.length} already resolved.`);
  if (errors.length)  parts.push(`${errors.length} error${errors.length === 1 ? '' : 's'}.`);
  if (unresolvableRefs.length) {
    parts.push(`Could not resolve ${unresolvableRefs.join(', ')} (provide teamId).`);
  }

  return parts.join(' ');
}

module.exports = { parseCommitMessage, syncFromCommit };
