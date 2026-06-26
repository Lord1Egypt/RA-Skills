/**
 * Loop Engine — Expense Approval Example (local governance mode)
 * 
 * The simplest governed loop pattern.
 * A human-only guard ensures the approval transition can never
 * be triggered by an automation or AI actor.
 * 
 * No API key required — runs with in-memory storage.
 * 
 * Install:
 *   npm install @loop-engine/sdk @loop-engine/adapter-memory
 */

import { createLoopSystem, parseLoopYaml, CommonGuards } from '@loop-engine/sdk'
import { MemoryAdapter } from '@loop-engine/adapter-memory'

const definition = parseLoopYaml(`
  loopId: expense.approval
  name: Expense Approval
  version: 1.0.0
  initialState: submitted
  states:
    - stateId: submitted
      label: Submitted
    - stateId: approved
      label: Approved
      terminal: true
    - stateId: rejected
      label: Rejected
      terminal: true
  transitions:
    - transitionId: approve
      from: submitted
      to: approved
      signal: approve
      allowedActors: [human]
      guards: [human-only]
    - transitionId: reject
      from: submitted
      to: rejected
      signal: reject
      allowedActors: [human]
      guards: [human-only]
`)

async function main() {
  const system = createLoopSystem({
    storage: new MemoryAdapter(),
    guards: CommonGuards,
  })

  // Start the loop
  const loop = await system.startLoop({
    definition,
    context: {
      submittedBy: 'alice',
      amount: 4200,
      description: 'Team offsite — Q2 planning',
    },
  })

  console.log(`Loop started: ${loop.loopId}`)
  console.log(`Current state: ${loop.currentState}`)

  // Try automation actor — should be blocked by human-only guard
  try {
    await system.transition({
      loopId: loop.loopId,
      signalId: 'approve',
      actor: { id: 'bot-1', type: 'automation' },
      evidence: {},
    })
  } catch (err) {
    console.log(`Automation blocked: ${(err as Error).message}`)
  }

  // Human approves — guard passes
  const result = await system.transition({
    loopId: loop.loopId,
    signalId: 'approve',
    actor: { id: 'bob', type: 'human' },
    evidence: {
      reviewNote: 'Within Q2 budget policy',
      reviewedAt: new Date().toISOString(),
    },
  })

  console.log(`Transition result: ${result.status}`)
  console.log(`New state: ${result.newState}`)
  console.log(`Actor: ${result.actor.type} (${result.actor.id})`)
  console.log(`Evidence:`, result.evidence)
}

main().catch(console.error)
