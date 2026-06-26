/**
 * Loop Engine — Fraud Review Loop (Grok / xAI, provider-backed)
 * 
 * Grok 3 scores a flagged transaction for fraud indicators.
 * A confidence guard determines whether to auto-dismiss or escalate.
 * A human risk analyst reviews escalated cases and records final disposition.
 * 
 * Requires: XAI_API_KEY environment variable
 * 
 * Install:
 *   npm install @loop-engine/sdk @loop-engine/adapter-memory @loop-engine/adapter-grok
 */

import { createLoopSystem, parseLoopYaml, CommonGuards } from '@loop-engine/sdk'
import { MemoryAdapter } from '@loop-engine/adapter-memory'
import { createGrokActorAdapter } from '@loop-engine/adapter-grok'

// DATA PRIVACY NOTICE: This example sends transaction context to the
// xAI Grok API. In production, redact or tokenize PII before passing
// as evidence. See SKILL.md for full data privacy guidance.

const definition = parseLoopYaml(`
  loopId: fraud.review
  name: Fraud Review Loop
  version: 1.0.0
  initialState: idle
  states:
    - stateId: idle
      label: Idle
    - stateId: flagged
      label: Flagged
    - stateId: scoring
      label: AI Scoring
    - stateId: pending_review
      label: Pending Analyst Review
    - stateId: reviewed
      label: Reviewed
      terminal: true
    - stateId: dismissed
      label: Dismissed
      terminal: true
  transitions:
    - transitionId: flag_transaction
      from: idle
      to: flagged
      signal: flag_transaction
      allowedActors: [automation]
    - transitionId: start_scoring
      from: flagged
      to: scoring
      signal: start_scoring
      allowedActors: [automation]
    - transitionId: escalate
      from: scoring
      to: pending_review
      signal: escalate
      allowedActors: [ai-agent]
      guards:
        - guardId: confidence-threshold
          params:
            threshold: 0.60
        - guardId: evidence-required
          params:
            requiredFields: [fraud_score, flagged_patterns]
    - transitionId: dismiss
      from: scoring
      to: dismissed
      signal: dismiss
      allowedActors: [ai-agent]
      guards:
        - guardId: confidence-threshold
          params:
            threshold: 0.80
    - transitionId: confirm_fraud
      from: pending_review
      to: reviewed
      signal: confirm_fraud
      allowedActors: [human]
      guards: [human-only]
    - transitionId: clear_transaction
      from: pending_review
      to: reviewed
      signal: clear_transaction
      allowedActors: [human]
      guards: [human-only]
`)

async function main() {
  // Required: XAI_API_KEY — see SKILL.md for data privacy considerations
  if (!process.env.XAI_API_KEY) {
    throw new Error(
      "Missing XAI_API_KEY. This provider-backed example sends prompt/evidence context to xAI Grok."
    )
  }

  const system = createLoopSystem({
    storage: new MemoryAdapter(),
    guards: CommonGuards,
  })

  const adapter = createGrokActorAdapter(process.env.XAI_API_KEY, {
    modelId: 'grok-3',
    confidenceThreshold: 0.60,
  })

  // The flagged transaction
  const transaction = {
    transactionId: 'TXN-9847263',
    amount: 4750.00,
    currency: 'USD',
    merchantName: 'Electronics Depot Online',
    merchantCountry: 'US',
    cardLast4: '7291',
    cardholderName: 'SYNTHETIC-TEST-USER', // redact real names in production
    timestamp: new Date().toISOString(),
  }

  const loop = await system.startLoop({
    definition,
    context: transaction,
  })

  console.log(`Transaction flagged: ${transaction.transactionId}`)
  console.log(`Amount: $${transaction.amount}`)

  // Fraud detection system flags the transaction
  await system.transition({
    loopId: loop.loopId,
    signalId: 'flag_transaction',
    actor: { id: 'fraud-detector', type: 'automation' },
    evidence: {
      flagReason: 'Amount exceeds 3x 30-day average',
      ruleId: 'RULE-AMT-3X',
    },
  })

  // Move to scoring
  await system.transition({
    loopId: loop.loopId,
    signalId: 'start_scoring',
    actor: { id: 'fraud-orchestrator', type: 'automation' },
    evidence: {},
  })

  console.log('Scoring with Grok 3...')

  const { actor, decision } = await adapter.createSubmission({
    loopId: loop.loopId,
    loopName: 'Fraud Review Loop',
    currentState: 'scoring',
    availableSignals: [
      {
        signalId: 'escalate',
        name: 'Escalate to Human Review',
        description: 'Fraud indicators present — route to analyst',
        allowedActors: ['ai-agent'],
      },
      {
        signalId: 'dismiss',
        name: 'Dismiss — Low Risk',
        description: 'No significant fraud indicators — auto-dismiss',
        allowedActors: ['ai-agent'],
      },
    ],
    instruction:
      'Analyze this transaction for fraud indicators. ' +
      'Consider velocity, merchant risk, geographic anomalies, and behavioral patterns. ' +
      'Score fraud probability from 0 (legitimate) to 1 (confirmed fraud). ' +
      'Escalate if score >= 0.6. Dismiss if score < 0.6 with high confidence.',
    evidence: {
      // NOTE: deviceFingerprint and cardholderName are synthetic in this example
      // Replace with anonymized or tokenized values in production
      ...transaction,
      cardholderAvgMonthlySpend: 1580,
      cardholderAvg30DayTransaction: 1420,
      previousTransactionsToday: 2,
      merchantRiskScore: 0.12,
      ipCountry: 'US',
      deviceFingerprint: 'known-device-7f3a',
      velocityAlerts: 1,
      isNewMerchant: false,
      cardholderTravelHistory: ['US', 'CA', 'MX'],
    },
  })

  console.log(`Grok decision: ${decision.signalId}`)
  console.log(`Fraud score confidence: ${decision.confidence}`)
  console.log(`Analysis: ${decision.reasoning}`)

  // Submit Grok's scoring decision
  const scoringResult = await system.transition({
    loopId: loop.loopId,
    signalId: decision.signalId,
    actor,
    evidence: {
      fraud_score: decision.dataPoints?.fraud_score ?? decision.confidence,
      flagged_patterns: decision.dataPoints?.flagged_patterns ?? ['amount_velocity'],
      reasoning: decision.reasoning,
      confidence: decision.confidence,
      model: actor.modelId,
      provider: actor.provider,
      promptHash: actor.promptHash,
    },
  })

  console.log(`Scoring result: ${scoringResult.status} → ${scoringResult.newState}`)

  if (scoringResult.newState === 'pending_review') {
    console.log('Escalated to human analyst...')

    // Risk analyst reviews and makes final call
    const reviewResult = await system.transition({
      loopId: loop.loopId,
      signalId: 'confirm_fraud',
      actor: { id: 'risk-analyst-02', type: 'human' },
      evidence: {
        analystNote: 'Confirmed fraud — amount and merchant pattern match known scheme.',
        disposition: 'fraud_confirmed',
        actionTaken: 'card_blocked',
        reviewedAt: new Date().toISOString(),
      },
    })

    console.log(`Final disposition: ${reviewResult.newState}`)
  } else {
    console.log(`Auto-dismissed — below fraud threshold`)
  }

  console.log('Fraud review complete — full audit trail preserved')
  console.log(`AI scored → human reviewed → disposition recorded`)
}

main().catch(console.error)
