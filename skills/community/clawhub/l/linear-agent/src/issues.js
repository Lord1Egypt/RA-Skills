/**
 * src/issues.js
 * CRUD operations for Linear issues.
 *
 * Priority encoding (Linear convention):
 *   0 = No priority
 *   1 = Urgent
 *   2 = High
 *   3 = Medium
 *   4 = Low
 */

'use strict';

// ---------------------------------------------------------------------------
// Fragments reused across queries
// ---------------------------------------------------------------------------

const ISSUE_FRAGMENT = `
  id
  identifier
  title
  description
  priority
  priorityLabel
  estimate
  dueDate
  url
  createdAt
  updatedAt
  completedAt
  canceledAt
  state {
    id
    name
    type
    color
  }
  assignee {
    id
    name
    email
    avatarUrl
  }
  team {
    id
    name
    key
  }
  labels {
    nodes {
      id
      name
      color
    }
  }
  cycle {
    id
    name
    number
    startsAt
    endsAt
  }
  project {
    id
    name
    state
  }
  comments {
    nodes {
      id
      body
      createdAt
      user { id name }
    }
  }
`;

// ---------------------------------------------------------------------------
// createIssue
// ---------------------------------------------------------------------------

/**
 * Create a new Linear issue.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}   params.title       - Issue title (required)
 * @param {string}   params.teamId      - Team ID (required)
 * @param {string}  [params.description]- Markdown body
 * @param {number}  [params.priority]   - 0-4
 * @param {string}  [params.assigneeId] - User ID
 * @param {string}  [params.stateId]    - Workflow state ID
 * @param {string[]}[params.labelIds]   - Label IDs
 * @param {string}  [params.dueDate]    - ISO date string
 * @param {number}  [params.estimate]   - Story points
 * @returns {Promise<object>} structured result
 */
async function createIssue(client, params) {
  const { title, teamId, description, priority, assigneeId, stateId, labelIds, dueDate, estimate } = params;

  if (!title)  throw new Error('"title" is required to create an issue.');
  if (!teamId) throw new Error('"teamId" is required to create an issue.');

  const mutation = `
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue {
          ${ISSUE_FRAGMENT}
        }
      }
    }
  `;

  // Build input object — omit undefined fields so Linear uses defaults
  const input = { title, teamId };
  if (description !== undefined) input.description = description;
  if (priority    !== undefined) input.priority    = Number(priority);
  if (assigneeId  !== undefined) input.assigneeId  = assigneeId;
  if (stateId     !== undefined) input.stateId     = stateId;
  if (labelIds    !== undefined) input.labelIds    = labelIds;
  if (dueDate     !== undefined) input.dueDate     = dueDate;
  if (estimate    !== undefined) input.estimate    = Number(estimate);

  const data = await client.request(mutation, { input });

  if (!data.issueCreate.success) {
    throw new Error('Linear returned success=false for issueCreate.');
  }

  return {
    success: true,
    data: data.issueCreate.issue,
  };
}

// ---------------------------------------------------------------------------
// updateIssue
// ---------------------------------------------------------------------------

/**
 * Update an existing issue.
 * Accepts either a UUID (id) or an identifier string like "ENG-123".
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}   params.id          - Issue UUID or identifier
 * @param {string}  [params.title]
 * @param {string}  [params.description]
 * @param {string}  [params.stateId]
 * @param {number}  [params.priority]
 * @param {string}  [params.assigneeId]
 * @param {string[]}[params.labelIds]
 * @param {string}  [params.dueDate]
 * @param {number}  [params.estimate]
 * @returns {Promise<object>}
 */
async function updateIssue(client, params) {
  const { id, title, description, stateId, priority, assigneeId, labelIds, dueDate, estimate } = params;

  if (!id) throw new Error('"id" is required to update an issue.');

  // Resolve identifier -> UUID if necessary
  const resolvedId = await resolveIssueId(client, id);

  const mutation = `
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue {
          ${ISSUE_FRAGMENT}
        }
      }
    }
  `;

  const input = {};
  if (title       !== undefined) input.title       = title;
  if (description !== undefined) input.description = description;
  if (stateId     !== undefined) input.stateId     = stateId;
  if (priority    !== undefined) input.priority    = Number(priority);
  if (assigneeId  !== undefined) input.assigneeId  = assigneeId;
  if (labelIds    !== undefined) input.labelIds    = labelIds;
  if (dueDate     !== undefined) input.dueDate     = dueDate;
  if (estimate    !== undefined) input.estimate    = Number(estimate);

  if (Object.keys(input).length === 0) {
    throw new Error('No fields provided to update. Pass at least one of: title, description, stateId, priority, assigneeId, labelIds, dueDate, estimate.');
  }

  const data = await client.request(mutation, { id: resolvedId, input });

  if (!data.issueUpdate.success) {
    throw new Error('Linear returned success=false for issueUpdate.');
  }

  return {
    success: true,
    data: data.issueUpdate.issue,
  };
}

// ---------------------------------------------------------------------------
// getIssue
// ---------------------------------------------------------------------------

/**
 * Fetch a single issue by UUID or identifier (e.g. "ENG-123").
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} params.id
 * @returns {Promise<object>}
 */
async function getIssue(client, params) {
  const { id } = params;
  if (!id) throw new Error('"id" is required.');

  // If it looks like an identifier (e.g. ENG-123), use issueByIdentifier query
  if (isIdentifier(id)) {
    return getIssueByIdentifier(client, id);
  }

  const query = `
    query GetIssue($id: String!) {
      issue(id: $id) {
        ${ISSUE_FRAGMENT}
      }
    }
  `;

  const data = await client.request(query, { id });

  if (!data.issue) {
    throw new Error(`Issue not found: ${id}`);
  }

  return { success: true, data: data.issue };
}

// ---------------------------------------------------------------------------
// listIssues
// ---------------------------------------------------------------------------

/**
 * List issues with optional filters.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}  [params.teamId]
 * @param {string}  [params.assigneeId]
 * @param {string}  [params.stateType]  - triage|backlog|unstarted|started|completed|cancelled
 * @param {string}  [params.cycleId]
 * @param {string}  [params.projectId]
 * @param {number}  [params.priority]
 * @param {number}  [params.first]      - defaults to 50
 * @returns {Promise<object>}
 */
async function listIssues(client, params = {}) {
  const { teamId, assigneeId, stateType, cycleId, projectId, priority, first = 50 } = params;

  // Build the IssueFilter object
  const filter = {};
  if (teamId)     filter.team     = { id: { eq: teamId } };
  if (assigneeId) filter.assignee = { id: { eq: assigneeId } };
  if (stateType)  filter.state    = { type: { eq: stateType } };
  if (cycleId)    filter.cycle    = { id: { eq: cycleId } };
  if (projectId)  filter.project  = { id: { eq: projectId } };
  if (priority !== undefined) filter.priority = { eq: Number(priority) };

  const query = `
    query ListIssues($filter: IssueFilter, $first: Int) {
      issues(filter: $filter, first: $first, orderBy: updatedAt) {
        nodes {
          ${ISSUE_FRAGMENT}
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `;

  const data = await client.request(query, { filter, first: Number(first) });

  return {
    success: true,
    data: data.issues.nodes,
    pageInfo: data.issues.pageInfo,
    count: data.issues.nodes.length,
  };
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/**
 * Detect if a string is a Linear issue identifier like "ENG-123".
 */
function isIdentifier(str) {
  return /^[A-Z][A-Z0-9]+-\d+$/i.test(str.trim());
}

/**
 * Look up an issue by its human-readable identifier (e.g. "ENG-42").
 */
async function getIssueByIdentifier(client, identifier) {
  const query = `
    query GetIssueByIdentifier($id: String!) {
      issue(id: $id) {
        ${ISSUE_FRAGMENT}
      }
    }
  `;
  // Linear accepts identifiers directly in the issue(id:) query
  const data = await client.request(query, { id: identifier });

  if (!data.issue) {
    throw new Error(`Issue not found: ${identifier}`);
  }

  return { success: true, data: data.issue };
}

/**
 * Resolve either a UUID or identifier to a UUID.
 * Linear's mutationfields require a UUID, not an identifier string.
 */
async function resolveIssueId(client, idOrIdentifier) {
  if (!isIdentifier(idOrIdentifier)) return idOrIdentifier; // Already a UUID

  const result = await getIssueByIdentifier(client, idOrIdentifier);
  return result.data.id;
}

module.exports = { createIssue, updateIssue, getIssue, listIssues, resolveIssueId, isIdentifier };
