/**
 * src/cycles.js
 * Cycle (sprint) operations for Linear.
 *
 * Linear cycles are time-boxed sprints associated with a team.
 * Each cycle has a start/end date, a progress float (0–1), and a set of issues.
 */

'use strict';

const CYCLE_FRAGMENT = `
  id
  name
  number
  startsAt
  endsAt
  completedAt
  progress
  scopeHistory
  completedScopeHistory
  team {
    id
    name
    key
  }
`;

const CYCLE_ISSUES_FRAGMENT = `
  issues(first: 250) {
    nodes {
      id
      identifier
      title
      priority
      priorityLabel
      estimate
      completedAt
      canceledAt
      state {
        id
        name
        type
      }
      assignee {
        id
        name
      }
    }
  }
`;

// ---------------------------------------------------------------------------
// listCycles
// ---------------------------------------------------------------------------

/**
 * List cycles for a given team, optionally filtering to the active cycle only.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string}  params.teamId
 * @param {boolean} [params.active=false] - When true, return only the current active cycle
 * @returns {Promise<object>}
 */
async function listCycles(client, params) {
  const { teamId, active = false } = params;
  if (!teamId) throw new Error('"teamId" is required for list-cycles.');

  const query = `
    query ListCycles($filter: CycleFilter, $first: Int) {
      cycles(filter: $filter, first: $first, orderBy: updatedAt) {
        nodes {
          ${CYCLE_FRAGMENT}
        }
      }
    }
  `;

  const filter = { team: { id: { eq: teamId } } };

  // Add "active" filter: cycles that have started but not yet ended
  if (active) {
    const now = new Date().toISOString();
    filter.startsAt = { lte: now };
    filter.endsAt   = { gte: now };
  }

  const data = await client.request(query, { filter, first: active ? 1 : 50 });
  const cycles = data.cycles.nodes;

  return {
    success: true,
    data: cycles,
    count: cycles.length,
  };
}

// ---------------------------------------------------------------------------
// getCycle
// ---------------------------------------------------------------------------

/**
 * Get a single cycle by ID, including all its issues.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} params.id - Cycle UUID
 * @returns {Promise<object>}
 */
async function getCycle(client, params) {
  const { id } = params;
  if (!id) throw new Error('"id" is required for get-cycle.');

  const query = `
    query GetCycle($id: String!) {
      cycle(id: $id) {
        ${CYCLE_FRAGMENT}
        ${CYCLE_ISSUES_FRAGMENT}
      }
    }
  `;

  const data = await client.request(query, { id });

  if (!data.cycle) {
    throw new Error(`Cycle not found: ${id}`);
  }

  return {
    success: true,
    data: {
      ...data.cycle,
      issues: data.cycle.issues.nodes,
    },
  };
}

// ---------------------------------------------------------------------------
// cycleProgress
// ---------------------------------------------------------------------------

/**
 * Get completion progress for a cycle.
 * If `id` is provided, uses that cycle.
 * If only `teamId` is provided, finds the active cycle for the team.
 *
 * @param {LinearClient} client
 * @param {object} params
 * @param {string} [params.id]     - Cycle UUID
 * @param {string} [params.teamId] - Team UUID (used when id is not provided)
 * @returns {Promise<object>}
 */
async function cycleProgress(client, params) {
  const { id, teamId } = params;

  if (!id && !teamId) {
    throw new Error('Either "id" or "teamId" is required for cycle-progress.');
  }

  let cycleId = id;

  // Resolve active cycle from teamId if no direct ID was given
  if (!cycleId) {
    const now = new Date().toISOString();
    const query = `
      query ActiveCycle($filter: CycleFilter) {
        cycles(filter: $filter, first: 1) {
          nodes { id }
        }
      }
    `;
    const filter = {
      team:     { id: { eq: teamId } },
      startsAt: { lte: now },
      endsAt:   { gte: now },
    };
    const data = await client.request(query, { filter });
    const cycles = data.cycles.nodes;
    if (cycles.length === 0) {
      return {
        success: true,
        data: null,
        message: 'No active cycle found for this team.',
      };
    }
    cycleId = cycles[0].id;
  }

  // Fetch full cycle with issues
  const cycleResult = await getCycle(client, { id: cycleId });
  const cycle = cycleResult.data;

  const issues = cycle.issues || [];
  const total  = issues.length;
  const done   = issues.filter((i) => i.completedAt && !i.canceledAt).length;
  const cancelled = issues.filter((i) => i.canceledAt).length;
  const inProgress = issues.filter(
    (i) => !i.completedAt && !i.canceledAt && i.state?.type === 'started'
  ).length;
  const notStarted = total - done - cancelled - inProgress;

  // Story-point velocity if estimates are present
  const totalPoints    = issues.reduce((sum, i) => sum + (i.estimate ?? 0), 0);
  const completedPoints = issues
    .filter((i) => i.completedAt)
    .reduce((sum, i) => sum + (i.estimate ?? 0), 0);

  // Days remaining
  const now = new Date();
  const end = cycle.endsAt ? new Date(cycle.endsAt) : null;
  const daysRemaining = end
    ? Math.max(0, Math.ceil((end - now) / (1000 * 60 * 60 * 24)))
    : null;

  const progressPct = total > 0 ? Math.round((done / total) * 100) : 0;

  return {
    success: true,
    data: {
      cycle: {
        id:     cycle.id,
        name:   cycle.name,
        number: cycle.number,
        team:   cycle.team,
        startsAt: cycle.startsAt,
        endsAt:   cycle.endsAt,
      },
      progress: {
        total,
        done,
        inProgress,
        notStarted,
        cancelled,
        progressPercent: progressPct,
        daysRemaining,
      },
      points: totalPoints > 0
        ? { total: totalPoints, completed: completedPoints, remaining: totalPoints - completedPoints }
        : null,
      summary: buildProgressSummary({ cycle, total, done, inProgress, notStarted, cancelled, progressPct, daysRemaining }),
    },
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function buildProgressSummary({ cycle, total, done, inProgress, notStarted, cancelled, progressPct, daysRemaining }) {
  const parts = [
    `Cycle ${cycle.number}${cycle.name ? ` (${cycle.name})` : ''} is ${progressPct}% complete.`,
    `${done}/${total} issues done`,
  ];
  if (inProgress > 0) parts.push(`${inProgress} in progress`);
  if (notStarted > 0) parts.push(`${notStarted} not started`);
  if (cancelled > 0)  parts.push(`${cancelled} cancelled`);
  if (daysRemaining !== null) {
    parts.push(daysRemaining === 0 ? 'cycle ends today' : `${daysRemaining} day${daysRemaining === 1 ? '' : 's'} remaining`);
  }
  return parts.join(', ') + '.';
}

module.exports = { listCycles, getCycle, cycleProgress };
