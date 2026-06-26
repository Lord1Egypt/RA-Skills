/**
 * Autonomy Module - Autonomous decision making and self-improvement
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve → ENFORCE (closed-loop)
 */
export * from './types.js';
export { DecisionMachine, decisionMachine } from './decision-machine.js';
export { EffectTracker, effectTracker } from './effect-tracker.js';
export { SelfOptimizer, selfOptimizer } from './optimizer.js';
export { SelfEvolver, selfEvolver } from './evolver.js';
export { DecisionHistory, decisionHistory } from './history.js';
export { DECISION_STRATEGIES, selectBestOption, getStrategyDescription } from './strategies.js';
export { PatchManager, patchManager } from './patch-manager.js';
export { evolutionReporter, generateEvolutionReport, formatReportAsMarkdown } from './evolution-reporter.js';
export { AgentCoordinator, createCoordinator, PHASE3_EXPERTS } from './agent-coordinator.js';
// Rule enforcement - MANDATORY (closed-loop)
export { saveMandatoryRules, loadMandatoryRules, appendEvolutionLog, getEvolutionLog, getRulesPath } from './rule-persistence.js';
export { applyRulesToAgent, applyRulesToAllAgents, extractRulesFromSoul, generateRulesFromEvolution } from './rule-enforcer.js';
export { ClosedLoopEvolver, closedLoopEvolver } from './closed-loop-evolver.js';
//# sourceMappingURL=index.js.map