import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';

import {
  buildAgentScorecard,
  buildRepairTickets,
  writeRepairTickets,
} from '../scripts/harness-improvement-lib.mjs';

test('buildAgentScorecard attaches repair action for failed and blocked lanes', () => {
  const scorecard = buildAgentScorecard({
    date: '2026-05-01',
    progressReport: {
      date: '2026-05-01',
      lanes: {
        'peter-deploy': {
          agent: 'peter',
          state: 'BLOCKED',
          agentStatus: 'FAIL',
          blocker: 'Closeout verify FAIL - count mismatch. No live URL verification receipt.',
          missing_receipts: ['peter-deploy-receipt'],
          evidenceLinks: ['/tmp/peter.json'],
          nextHandoff: 'Run closeout verify.',
        },
      },
    },
    history: [
      {
        date: '2026-04-30',
        agent: 'peter',
        lane: 'peter-deploy',
        failureClass: 'ProofMissing',
      },
    ],
  });

  const lane = scorecard.agents.peter.lanes[0];
  assert.equal(lane.repair.failureClass, 'ProofMissing');
  assert.equal(lane.repair.repairState, 'EXPERIMENT_REQUIRED');
  assert.equal(lane.repair.repeatCount7d, 2);
  assert.match(lane.repair.nextAction, /proof/i);
});

test('buildRepairTickets and writeRepairTickets create deterministic recovery ticket files', () => {
  const scorecard = buildAgentScorecard({
    date: '2026-05-01',
    progressReport: {
      lanes: {
        'elon-x': {
          agent: 'elon',
          state: 'PENDING_INPUT',
          agentStatus: 'BLOCKED_BUT_COMPLIANT',
          blocker: 'Waiting for X proof URL.',
          missing_receipts: ['elon-x-proof-receipt'],
          evidenceLinks: ['/tmp/elon.json'],
        },
      },
    },
  });

  const tickets = buildRepairTickets(scorecard);
  assert.equal(tickets.length, 1);
  assert.equal(tickets[0].ticket_id, 'rt-2026-05-01-elon-x-harness-repair');
  assert.equal(tickets[0].failureClass, 'ProofMissing');
  assert.equal(tickets[0].repairState, 'TICKET_CREATED');

  const root = mkdtempSync(resolve(tmpdir(), 'harness-repair-'));
  const written = writeRepairTickets(tickets, root);
  assert.equal(written.length, 1);

  const saved = JSON.parse(readFileSync(written[0], 'utf8'));
  assert.equal(saved.ticket_id, 'rt-2026-05-01-elon-x-harness-repair');
  assert.equal(saved.owner, 'elon');
  assert.deepEqual(saved.missingProof, ['elon-x-proof-receipt']);
});
