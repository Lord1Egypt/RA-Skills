/**
 * Decision Machine - Core decision engine
 */

import type { Decision, DecisionContext, DecisionOption } from './types.js'
import { selectBestOption } from './strategies.js'

let counter = 0

export class DecisionMachine {
  async decide(context: DecisionContext): Promise<Decision | null> {
    const options = context.options || []
    if (options.length === 0) return null
    
    const selected = selectBestOption(options, context)
    if (!selected) return null

    return {
      id: `dec_${Date.now()}_${++counter}`,
      timestamp: Date.now(),
      context,
      options,
      selectedOption: selected.option,
      reasoning: `[${selected.option.type}] ${selected.option.name}: 风险${(selected.option.estimatedRisk*100).toFixed(0)}% 评分${(selected.score*100).toFixed(1)}%`,
      score: selected.score,
    }
  }
}

export const decisionMachine = new DecisionMachine()
