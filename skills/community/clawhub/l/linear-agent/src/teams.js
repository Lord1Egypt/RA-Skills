/**
 * src/teams.js
 * Team listing and backlog summary generation.
 */

'use strict';

const PRIORITY_LABELS = {
  0: 'No priority',
  1: 'Urgent',
  2: 'High',
  3: 'Medium',
  4: 'Low',
};

// ---------------------------------------------------------------------------
// listTeams
// ---------------------------------------------------------------------------

/**
 * List all teams in the workspace.
 *
 * @param {LinearClient} client
 * @returns {Promise<object>}
 */
async function listTeams(client) {
  const query = `
    query ListTeams {
      teams {
        nodes {
          id
          name
          key
          description
          color
          timezone
          issueCount
          memberCount: members {
            nodes { id }
          }
          activeCycle {
            id
            name
            number
            startsAt
            endsAt
            progress
          }
        }
      }
    }
  `;

  const data = await client.request(query);

  // Clean up the memberCount field returned as { nodes: [] }
  const teams = data.teams.nodes.map((t) => ({
    ...t,
    memberCount: t.memberCount?.nodes?.length ?? 0,
  }));

  return {
    success: true,
    data: teams,
    count: teams.length,
  };
}

// ---------------------------------------------------------------------------
// backlogSummary
// ---------------------------------------------------------------------------

/**
 * Fetch all non-completed issues for a team and produce a plain-English summary.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} params.teamId
 * @param {number} [params.first=100]
 * @returns {Promise<object>} - Contains both structured `data` and human-readable `summary`
 */
async function backlogSummary(client, params) {
  const { teamId, first = 100 } = params;
  if (!teamId) throw new Error('"teamId" is required for backlog-summary.');

  // Fetch team name first
  const teamQuery = `
    query GetTeam($id: String!) {
      team(id: $id) {
        id
        name
        key
      }
    }
  `;
  const teamData = await client.request(teamQuery, { id: teamId });
  const team = teamData.team;
  if (!team) throw new Error(`Team not found: ${teamId}`);

  // Fetch active backlog/in-progress issues (exclude completed & cancelled)
  const issuesQuery = `
    query BacklogIssues($filter: IssueFilter, $first: Int) {
      issues(filter: $filter, first: $first, orderBy: updatedAt) {
        nodes {
          id
          identifier
          title
          priority
          priorityLabel
          estimate
          dueDate
          state {
            name
            type
          }
          assignee {
            id
            name
          }
          cycle {
            id
            name
            number
          }
          labels {
            nodes { name }
          }
        }
      }
    }
  `;

  const filter = {
    team: { id: { eq: teamId } },
    state: {
      type: {
        nin: ['completed', 'cancelled'],
      },
    },
  };

  const data = await client.request(issuesQuery, { filter, first: Number(first) });
  const issues = data.issues.nodes;

  // ---------------------------------------------------------------------------
  // Aggregate statistics
  // ---------------------------------------------------------------------------

  const byState    = groupBy(issues, (i) => i.state.type);
  const byPriority = groupBy(issues, (i) => i.priority ?? 0);
  const byAssignee = groupBy(issues, (i) => i.assignee?.name ?? 'Unassigned');
  const byCycle    = groupBy(issues, (i) => i.cycle ? `Cycle ${i.cycle.number}: ${i.cycle.name}` : 'No cycle');

  const urgentCount  = (byPriority[1] || []).length;
  const highCount    = (byPriority[2] || []).length;
  const mediumCount  = (byPriority[3] || []).length;
  const lowCount     = (byPriority[4] || []).length;
  const noPriorCount = (byPriority[0] || []).length;

  const inProgressCount = ((byState['started'] || []).length);
  const triageCount     = ((byState['triage']   || []).length);
  const unstartedCount  = ((byState['unstarted'] || []) .length + (byState['backlog'] || []).length);

  // Find overdue issues
  const now = new Date();
  const overdue = issues.filter((i) => i.dueDate && new Date(i.dueDate) < now);

  // Top assignees by load
  const assigneeLoad = Object.entries(byAssignee)
    .map(([name, items]) => ({ name, count: items.length }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  // ---------------------------------------------------------------------------
  // Build plain-English summary
  // ---------------------------------------------------------------------------

  const lines = [];
  lines.push(`## Backlog Summary — ${team.name} (${team.key})`);
  lines.push('');
  lines.push(`**Total open issues: ${issues.length}**`);
  lines.push('');

  lines.push('### Status breakdown');
  if (triageCount)     lines.push(`- **Triage**: ${triageCount} issue${s(triageCount)} awaiting assessment`);
  if (unstartedCount)  lines.push(`- **Not started**: ${unstartedCount} issue${s(unstartedCount)} in the backlog`);
  if (inProgressCount) lines.push(`- **In progress**: ${inProgressCount} issue${s(inProgressCount)} actively being worked on`);
  lines.push('');

  lines.push('### Priority breakdown');
  if (urgentCount)  lines.push(`- **Urgent**: ${urgentCount} issue${s(urgentCount)} — needs immediate attention`);
  if (highCount)    lines.push(`- **High**: ${highCount} issue${s(highCount)}`);
  if (mediumCount)  lines.push(`- **Medium**: ${mediumCount} issue${s(mediumCount)}`);
  if (lowCount)     lines.push(`- **Low**: ${lowCount} issue${s(lowCount)}`);
  if (noPriorCount) lines.push(`- **No priority**: ${noPriorCount} issue${s(noPriorCount)} — consider triaging`);
  lines.push('');

  if (overdue.length > 0) {
    lines.push(`### ⚠ Overdue (${overdue.length})`);
    overdue.slice(0, 5).forEach((i) => {
      const due = new Date(i.dueDate).toLocaleDateString();
      lines.push(`- **${i.identifier}**: ${i.title} *(due ${due})*`);
    });
    if (overdue.length > 5) lines.push(`- … and ${overdue.length - 5} more`);
    lines.push('');
  }

  if (assigneeLoad.length > 0) {
    lines.push('### Team workload');
    assigneeLoad.forEach(({ name, count }) => {
      lines.push(`- **${name}**: ${count} issue${s(count)}`);
    });
    lines.push('');
  }

  if (Object.keys(byCycle).length > 1 || !byCycle['No cycle']) {
    lines.push('### Cycle / Sprint');
    Object.entries(byCycle).forEach(([cycleName, items]) => {
      lines.push(`- **${cycleName}**: ${items.length} issue${s(items.length)}`);
    });
    lines.push('');
  }

  if (urgentCount > 0) {
    lines.push('### Urgent issues');
    (byPriority[1] || []).slice(0, 5).forEach((i) => {
      const who = i.assignee ? ` *(${i.assignee.name})*` : ' *(unassigned)*';
      lines.push(`- **${i.identifier}**: ${i.title}${who}`);
    });
    if (urgentCount > 5) lines.push(`- … and ${urgentCount - 5} more`);
    lines.push('');
  }

  const summary = lines.join('\n');

  return {
    success: true,
    summary,
    data: {
      team,
      totalOpen: issues.length,
      byState:    countEntries(byState),
      byPriority: countEntries(byPriority),
      byAssignee: countEntries(byAssignee),
      byCycle:    countEntries(byCycle),
      overdue:    overdue.map((i) => ({ id: i.id, identifier: i.identifier, title: i.title, dueDate: i.dueDate })),
    },
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function groupBy(arr, keyFn) {
  return arr.reduce((acc, item) => {
    const key = keyFn(item);
    (acc[key] = acc[key] || []).push(item);
    return acc;
  }, {});
}

function countEntries(grouped) {
  return Object.fromEntries(Object.entries(grouped).map(([k, v]) => [k, v.length]));
}

/** Pluralize helper — returns 's' when count !== 1 */
function s(count) {
  return count === 1 ? '' : 's';
}

module.exports = { listTeams, backlogSummary };
