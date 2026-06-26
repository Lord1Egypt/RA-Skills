/**
 * src/projects.js
 * Project CRUD operations.
 *
 * Linear project states: planned | started | paused | completed | cancelled
 */

'use strict';

const PROJECT_FRAGMENT = `
  id
  name
  description
  state
  url
  startedAt
  completedAt
  canceledAt
  targetDate
  createdAt
  updatedAt
  progress
  lead {
    id
    name
    email
  }
  teams {
    nodes {
      id
      name
      key
    }
  }
  members {
    nodes {
      id
      name
    }
  }
  issueCountByState: issues {
    nodes {
      state { type }
    }
  }
`;

// ---------------------------------------------------------------------------
// createProject
// ---------------------------------------------------------------------------

/**
 * Create a new Linear project.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}   params.name       - Project name (required)
 * @param {string[]} params.teamIds    - Array of team UUIDs (required)
 * @param {string}  [params.description]
 * @param {string}  [params.state]     - planned|started|paused|completed|cancelled
 * @param {string}  [params.leadId]    - User UUID
 * @param {string}  [params.targetDate]- ISO date string
 * @returns {Promise<object>}
 */
async function createProject(client, params) {
  const { name, teamIds, description, state, leadId, targetDate } = params;

  if (!name)    throw new Error('"name" is required to create a project.');
  if (!teamIds || !teamIds.length) {
    throw new Error('"teamIds" (array) is required to create a project.');
  }

  const mutation = `
    mutation CreateProject($input: ProjectCreateInput!) {
      projectCreate(input: $input) {
        success
        project {
          id
          name
          description
          state
          url
          targetDate
          createdAt
          teams {
            nodes { id name key }
          }
        }
      }
    }
  `;

  const input = { name, teamIds };
  if (description !== undefined) input.description = description;
  if (state       !== undefined) input.state       = state;
  if (leadId      !== undefined) input.leadId      = leadId;
  if (targetDate  !== undefined) input.targetDate  = targetDate;

  const data = await client.request(mutation, { input });

  if (!data.projectCreate.success) {
    throw new Error('Linear returned success=false for projectCreate.');
  }

  return {
    success: true,
    data: data.projectCreate.project,
  };
}

// ---------------------------------------------------------------------------
// updateProject
// ---------------------------------------------------------------------------

/**
 * Update an existing project.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}  params.id
 * @param {string} [params.name]
 * @param {string} [params.description]
 * @param {string} [params.state]
 * @param {string} [params.leadId]
 * @param {string} [params.targetDate]
 * @returns {Promise<object>}
 */
async function updateProject(client, params) {
  const { id, name, description, state, leadId, targetDate } = params;
  if (!id) throw new Error('"id" is required to update a project.');

  const mutation = `
    mutation UpdateProject($id: String!, $input: ProjectUpdateInput!) {
      projectUpdate(id: $id, input: $input) {
        success
        project {
          id
          name
          description
          state
          url
          targetDate
          updatedAt
        }
      }
    }
  `;

  const input = {};
  if (name        !== undefined) input.name        = name;
  if (description !== undefined) input.description = description;
  if (state       !== undefined) input.state       = state;
  if (leadId      !== undefined) input.leadId      = leadId;
  if (targetDate  !== undefined) input.targetDate  = targetDate;

  if (Object.keys(input).length === 0) {
    throw new Error('No fields provided to update. Pass at least one of: name, description, state, leadId, targetDate.');
  }

  const data = await client.request(mutation, { id, input });

  if (!data.projectUpdate.success) {
    throw new Error('Linear returned success=false for projectUpdate.');
  }

  return {
    success: true,
    data: data.projectUpdate.project,
  };
}

// ---------------------------------------------------------------------------
// listProjects
// ---------------------------------------------------------------------------

/**
 * List all projects, optionally filtered by team.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} [params.teamId]
 * @param {number} [params.first=50]
 * @returns {Promise<object>}
 */
async function listProjects(client, params = {}) {
  const { teamId, first = 50 } = params;

  const query = `
    query ListProjects($filter: ProjectFilter, $first: Int) {
      projects(filter: $filter, first: $first, orderBy: updatedAt) {
        nodes {
          ${PROJECT_FRAGMENT}
        }
      }
    }
  `;

  const filter = {};
  if (teamId) filter.teams = { some: { id: { eq: teamId } } };

  const data = await client.request(query, {
    filter: Object.keys(filter).length ? filter : undefined,
    first: Number(first),
  });

  // Attach a quick issue-count-by-state summary
  const projects = data.projects.nodes.map((p) => {
    const issueNodes = p.issueCountByState?.nodes ?? [];
    const stateCount = issueNodes.reduce((acc, i) => {
      const t = i.state?.type ?? 'unknown';
      acc[t] = (acc[t] || 0) + 1;
      return acc;
    }, {});
    return {
      ...p,
      issueCountByState: stateCount,
      totalIssues: issueNodes.length,
    };
  });

  return {
    success: true,
    data: projects,
    count: projects.length,
  };
}

module.exports = { createProject, updateProject, listProjects };
