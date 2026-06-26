/**
 * Loop Engine — AI Replenishment Example (Claude, provider-backed)
 * 
 * Anthropic Claude analyzes inventory data and recommends a reorder.
 * A confidence-threshold guard blocks low-confidence recommendations.
 * A human-only guard ensures the final approval can't be auto-approved.
 * 
 * Requires: ANTHROPIC_API_KEY environment variable
 * 
 * Install:
 *   npm install @loop-engine/sdk @loop-engine/adapter-memory @loop-engine/adapter-anthropic
 *   npm install @anthropic-ai/sdk
 */

import { createLoopSystem, parseLoopYaml, CommonGuards } from '@loop-engine/sdk'
import { MemoryAdapter } from '@loop-engine/adapter-memory'
import { createAnthropicActorAdapter } from '@loop-engine/adapter-anthropic'

// DATA PRIVACY NOTICE: This example sends inventory context to the
// Anthropic Claude API. Review what business data you pass as evidence
// in production. See SKILL.md for full data privacy guidance.

const definition = parseLoopYaml(`
  loopId: scm.replenishment
  name: AI Replenishment
  version: 1.0.0
  initialState: idle
  states:
    - stateId: idle
      label: Idle
    - stateId: analyzing
      label: Analyzing
    - stateId: pending_approval
      label: Pending Approval
    - stateId: ordered
      label: Ordered
      terminal: true
    - stateId: rejected
      label: Rejected
      terminal: true
  transitions:
    - transitionId: start_analysis
      from: idle
      to: analyzing
      signal: start_analysis
      allowedActors: [automation]
    - transitionId: submit_recommendation
      from: analyzing
      to: pending_approval
      signal: submit_recommendation
      allowedActors: [ai-agent]
      guards:
        - guardId: confidence-threshold
          params:
            threshold: 0.75
    - transitionId: approve
      from: pending_approval
      to: ordered
      signal: approve
      allowedActors: [human]
      guards: [human-only]
    - transitionId: reject
      from: pending_approval
      to: rejected
      signal: reject
      allowedActors: [human]
      guards: [human-only]
`)

async function main() {
  // Required: ANTHROPIC_API_KEY — see SKILL.md for data privacy considerations
  if (!process.env.ANTHROPIC_API_KEY) {
    throw new Error(
      "Missing ANTHROPIC_API_KEY. This provider-backed example sends prompt/evidence context to Anthropic."
    )
  }

  const system = createLoopSystem({
    storage: new MemoryAdapter(),
    guards: CommonGuards,
  })

  const adapter = createAnthropicActorAdapter(process.env.ANTHROPIC_API_KEY, {
    modelId: 'claude-opus-4-6',
    confidenceThreshold: 0.75,
  })

  // Start the loop
  const loop = await system.startLoop({
    definition,
    context: { sku: 'SKU-4892', productName: 'Widget Pro 500ml' },
  })

  console.log(`Loop started: ${loop.loopId}`)

  // Automation triggers analysis
  await system.transition({
    loopId: loop.loopId,
    signalId: 'start_analysis',
    actor: { id: 'demand-sensor', type: 'automation' },
    evidence: {},
  })

  console.log('Analysis started — calling Claude...')

  // Claude analyzes and recommends
  const inventoryContext = {
    loopId: loop.loopId,
    loopName: 'AI Replenishment',
    currentState: 'analyzing',
    availableSignals: [
      {
        signalId: 'submit_recommendation',
        name: 'Submit Recommendation',
        allowedActors: ['ai-agent'],
      },
    ],
    instruction:
      'Analyze the inventory data and recommend whether to reorder. ' +
      'Consider current stock levels, demand forecast, and lead time.',
    evidence: {
      currentStock: 42,
      reorderPoint: 50,
      demandForecast: 0.89,
      leadTimeDays: 7,
      unitCost: 24.5,
    },
  }

  const { actor, decision } = await adapter.createSubmission(inventoryContext)

  console.log(`Claude decision: ${decision.signalId}`)
  console.log(`Confidence: ${decision.confidence}`)
  console.log(`Reasoning: ${decision.reasoning}`)

  // Submit Claude's recommendation — confidence guard evaluates
  const analysisResult = await system.transition({
    loopId: loop.loopId,
    signalId: decision.signalId,
    actor,
    evidence: {
      reasoning: decision.reasoning,
      confidence: decision.confidence,
      ...decision.dataPoints,
    },
  })

  console.log(`Analysis transition: ${analysisResult.status}`)
  console.log(`Actor provider: ${actor.provider}`)
  console.log(`Prompt hash: ${actor.promptHash}`)

  // Human approves the recommendation
  const approvalResult = await system.transition({
    loopId: loop.loopId,
    signalId: 'approve',
    actor: { id: 'supply-manager', type: 'human' },
    evidence: {
      approvalNote: 'Confirmed — reorder approved per AI recommendation',
      approvedAt: new Date().toISOString(),
    },
  })

  console.log(`Final state: ${approvalResult.newState}`)
  console.log(`Loop complete — full audit trail preserved`)
}

main().catch(console.error)
