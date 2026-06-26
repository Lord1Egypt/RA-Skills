/**
 * src/workflow.js
 * Workflow state operations — list states, move issues through states.
 *
 * Linear workflow state types:
 *   triage | backlog | unstarted | started | completed | cancelled
 */

'use strict';

const { resolveIssueId } = require('./issues');

// ---------------------------------------------------------------------------
// listWorkflowStates
// ---------------------------------------------------------------------------

/**
 * List all workflow states for a team, ordered by position.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} params.teamId
 * @returns {Promise<object>}
 */
async function listWorkflowStates(client, params) {
  const { teamId } = params;
  if (!teamId) throw new Error('"teamId" is required for list-states.');

  const query = `
    query ListWorkflowStates($filter: WorkflowStateFilter) {
      workflowStates(filter: $filter) {
        nodes {
          id
          name
          type
          color
          position
          description
          team {
            id
            name
            key
          }
        }
      }
    }
  `;

  const data = await client.request(query, {
    filter: { team: { id: { eq: teamId } } },
  });

  return {
    success: true,
    data: data.workflowStates.nodes,
    count: data.workflowStates.nodes.length,
  };
}

// ---------------------------------------------------------------------------
// moveIssue
// ---------------------------------------------------------------------------

/**
 * Move an issue to a different workflow state.
 *
 * You can target the state either by:
 *  - stateId:   direct UUID of the target state
 *  - stateName: human-readable name (e.g. "In Progress") — requires teamId
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}  params.id         - Issue UUID or identifier
 * @param {string} [params.stateId]   - Target state UUID
 * @param {string} [params.stateName] - Target state name (case-insensitive)
 * @param {string} [params.teamId]    - Required when using stateName
 * @returns {Promise<object>}
 */
async function moveIssue(client, params) {
  const { id, stateId, stateName, teamId } = params;

  if (!id) throw new Error('"id" is required to move an issue.');
  if (!stateId && !stateName) {
    throw new Error('Either "stateId" or "stateName" (+ "teamId") is required to move an issue.');
  }

  // Resolve identifier → UUID for the issue
  const resolvedIssueId = await resolveIssueId(client, id);

  // Resolve state name → state UUID if needed
  let resolvedStateId = stateId;
  if (!resolvedStateId) {
    if (!teamId) {
      // Try to fetch teamId from the issue itself
      const issueQuery = `
        query GetIssueTeam($id: String!) {
          issue(id: $id) {
            team { id }
          }
        }
      `;
      const issueData = await client.request(issueQuery, { id: resolvedIssueId });
      const inferredTeamId = issueData.issue?.team?.id;
      if (!inferredTeamId) {
        throw new Error('"teamId" is required when using "stateName" to move an issue.');
      }
      resolvedStateId = await resolveStateName(client, inferredTeamId, stateName);
    } else {
      resolvedStateId = await resolveStateName(client, teamId, stateName);
    }
  }

  const mutation = `
    mutation MoveIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue {
          id
          identifier
          title
          state {
            id
            name
            type
            color
          }
          updatedAt
          url
        }
      }
    }
  `;

  const data = await client.request(mutation, {
    id: resolvedIssueId,
    input: { stateId: resolvedStateId },
  });

  if (!data.issueUpdate.success) {
    throw new Error('Linear returned success=false for issueUpdate (move).');
  }

  return {
    success: true,
    data: data.issueUpdate.issue,
    message: `Issue ${data.issueUpdate.issue.identifier} moved to "${data.issueUpdate.issue.state.name}".`,
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Resolve a state name (case-insensitive) to its UUID for a given team.
 *
 * @param {LinearClient} client
 * @param {string} teamId
 * @param {string} name
 * @returns {Promise<string>} State UUID
 */
async function resolveStateName(client, teamId, name) {
  const statesResult = await listWorkflowStates(client, { teamId });
  const states = statesResult.data;

  const match = states.find(
    (s) => s.name.toLowerCase() === name.toLowerCase()
  );

  if (!match) {
    const available = states.map((s) => `"${s.name}"`).join(', ');
    throw new Error(
      `Workflow state "${name}" not found. Available states: ${available}`
    );
  }

  return match.id;
}

module.exports = { listWorkflowStates, moveIssue, resolveStateName };
