/**
 * Loop Engine — Infrastructure Change Approval (OpenAI GPT-4o, provider-backed)
 * 
 * GPT-4o analyzes the blast radius of a proposed infrastructure change.
 * A confidence guard blocks high-risk changes from auto-proceeding.
 * A human SRE must approve before any rollout begins.
 * 
 * Requires: OPENAI_API_KEY environment variable
 * 
 * Install:
 *   npm install @loop-engine/sdk @loop-engine/adapter-memory @loop-engine/adapter-openai
 *   npm install openai
 */

import { createLoopSystem, parseLoopYaml, CommonGuards } from '@loop-engine/sdk'
import { MemoryAdapter } from '@loop-engine/adapter-memory'
import { createOpenAIActorAdapter } from '@loop-engine/adapter-openai'

// DATA PRIVACY NOTICE: This example sends infrastructure change metadata
// to the OpenAI API. Review what system details you pass as evidence
// in production. See SKILL.md for full data privacy guidance.

const definition = parseLoopYaml(`
  loopId: infra.change.approval
  name: Infrastructure Change Approval
  version: 1.0.0
  initialState: idle
  states:
    - stateId: idle
      label: Idle
    - stateId: analyzing
      label: Analyzing Blast Radius
    - stateId: pending_approval
      label: Pending SRE Approval
    - stateId: rolling_out
      label: Rolling Out
    - stateId: complete
      label: Complete
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
    - transitionId: submit_analysis
      from: analyzing
      to: pending_approval
      signal: submit_analysis
      allowedActors: [ai-agent]
      guards:
        - guardId: confidence-threshold
          params:
            threshold: 0.70
        - guardId: evidence-required
          params:
            requiredFields: [blast_radius_score, affected_services, rollback_plan]
    - transitionId: approve
      from: pending_approval
      to: rolling_out
      signal: approve
      allowedActors: [human]
      guards: [human-only]
    - transitionId: reject
      from: pending_approval
      to: rejected
      signal: reject
      allowedActors: [human]
      guards: [human-only]
    - transitionId: complete_rollout
      from: rolling_out
      to: complete
      signal: complete_rollout
      allowedActors: [automation]
`)

async function main() {
  // Required: OPENAI_API_KEY — see SKILL.md for data privacy considerations
  if (!process.env.OPENAI_API_KEY) {
    throw new Error(
      "Missing OPENAI_API_KEY. This provider-backed example sends prompt/evidence context to OpenAI."
    )
  }

  const system = createLoopSystem({
    storage: new MemoryAdapter(),
    guards: CommonGuards,
  })

  const adapter = createOpenAIActorAdapter(process.env.OPENAI_API_KEY, {
    modelId: 'gpt-4o',
    confidenceThreshold: 0.70,
  })

  // The proposed change
  const changeRequest = {
    changeId: 'CHG-2847',
    description: 'Upgrade PostgreSQL from 14.8 to 15.4 on production cluster',
    requestedBy: 'platform-team',
    environment: 'production',
    estimatedDowntime: '~5 minutes',
    affectedRegions: ['us-east-1', 'us-west-2'],
  }

  const loop = await system.startLoop({
    definition,
    context: changeRequest,
  })

  console.log(`Change request: ${changeRequest.changeId}`)
  console.log(`Loop started: ${loop.loopId}`)

  // Trigger automated analysis
  await system.transition({
    loopId: loop.loopId,
    signalId: 'start_analysis',
    actor: { id: 'change-orchestrator', type: 'automation' },
    evidence: { changeRequest },
  })

  console.log('Analyzing blast radius with GPT-4o...')

  const { actor, decision } = await adapter.createSubmission({
    loopId: loop.loopId,
    loopName: 'Infrastructure Change Approval',
    currentState: 'analyzing',
    availableSignals: [
      {
        signalId: 'submit_analysis',
        name: 'Submit Blast Radius Analysis',
        allowedActors: ['ai-agent'],
      },
    ],
    instruction:
      'Analyze the blast radius of this infrastructure change. ' +
      'Identify affected services, assess risk, and provide a rollback plan. ' +
      'Score the blast radius from 0 (no impact) to 1 (critical impact).',
    evidence: {
      ...changeRequest,
      currentConnections: 847,
      dependentServices: ['api-gateway', 'auth-service', 'billing-service'],
      lastMajorOutage: '2025-11-12',
      recentChangeFailureRate: 0.04,
    },
  })

  console.log(`GPT-4o analysis: ${decision.signalId}`)
  console.log(`Confidence: ${decision.confidence}`)
  console.log(`Reasoning: ${decision.reasoning}`)

  // Submit analysis — evidence-required guard checks for blast_radius_score,
  // affected_services, and rollback_plan
  const analysisResult = await system.transition({
    loopId: loop.loopId,
    signalId: decision.signalId,
    actor,
    evidence: {
      blast_radius_score: 0.35,
      affected_services: ['api-gateway', 'auth-service', 'billing-service'],
      rollback_plan: 'pg_upgrade --revert within 10 minutes if health checks fail',
      reasoning: decision.reasoning,
      confidence: decision.confidence,
      model: actor.modelId,
      promptHash: actor.promptHash,
    },
  })

  console.log(`Analysis submitted: ${analysisResult.status}`)
  console.log('Awaiting SRE approval...')

  // SRE reviews and approves
  const approvalResult = await system.transition({
    loopId: loop.loopId,
    signalId: 'approve',
    actor: { id: 'sre-oncall', type: 'human' },
    evidence: {
      sreNote: 'Blast radius acceptable. Maintenance window confirmed. Proceed.',
      maintenanceWindow: '2026-03-14T02:00:00Z',
      approvedAt: new Date().toISOString(),
    },
  })

  console.log(`SRE approved: ${approvalResult.newState}`)

  // Automation completes the rollout
  const rolloutResult = await system.transition({
    loopId: loop.loopId,
    signalId: 'complete_rollout',
    actor: { id: 'deploy-bot', type: 'automation' },
    evidence: {
      deployedAt: new Date().toISOString(),
      newVersion: '15.4',
      healthChecksPassed: true,
      rolloutDuration: '4m 32s',
    },
  })

  console.log(`Change complete: ${rolloutResult.newState}`)
  console.log(`Full audit trail: AI analysis → SRE approval → automated rollout`)
}

main().catch(console.error)
