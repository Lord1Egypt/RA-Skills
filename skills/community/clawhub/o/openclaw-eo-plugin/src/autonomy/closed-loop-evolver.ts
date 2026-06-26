/**
 * Closed-Loop Evolver - Hybrid Architecture (v3.1)
 * 
 * This closes the FULL loop:
 * Decision → Execute → Track → Score → Analyze → Generate Rules → 
 * → Persist Rules (JSON) → Enforce Rules (Hook + SOUL) → Verify → Repeat
 * 
 * Key innovation: HYBRID rule enforcement
 * - Mandatory rules: Hook-level enforcement (cannot be bypassed)
 * - Suggestion rules: SOUL injection (soft, can be ignored)
 * - Rules stored as JSON for easy migration/sharing
 */
import { effectTracker } from './effect-tracker.js';
import { selfOptimizer } from './optimizer.js';
import { selfEvolver } from './evolver.js';
import { saveMandatoryRules, loadMandatoryRules, appendEvolutionLog, getEvolutionLog } from './rule-persistence.js';
import { applyRulesToAllAgents, generateRulesFromEvolution } from './rule-enforcer.js';
import { getRuleStorage, type Rule } from './rule-types.js';
import { getRuleEnforcer, generateSuggestionSection } from './rule-enforcer-hybrid.js';

export class ClosedLoopEvolver {
    enabled = true;
    minDecisionsForEvolution = 20;
    cooldown = 86400000; // 24 hours
    lastEvolution = 0;
    evolutionCount = 0;
    autoEnforce = true; // Auto-enforce rules without asking

    /**
     * Main entry point: Run closed-loop evolution
     * This will:
     * 1. Analyze effect tracker data
     * 2. Generate hybrid rules (mandatory + suggestion)
     * 3. Persist rules to JSON (portable format)
     * 4. Enforce: Hook for mandatory, SOUL for suggestions
     */
    async evolve(api: any): Promise<any> {
        if (!this.enabled) {
            return { success: false, reason: 'disabled' };
        }

        const now = Date.now();

        // Check cooldown
        if (now - this.lastEvolution < this.cooldown) {
            const remainingMs = this.cooldown - (now - this.lastEvolution);
            return {
                success: false,
                reason: 'cooldown',
                remainingMs,
                remainingHours: (remainingMs / 3600000).toFixed(1),
            };
        }

        // Check minimum decisions
        const stats = effectTracker.stats();
        if (stats.total < this.minDecisionsForEvolution) {
            return {
                success: false,
                reason: 'insufficient_data',
                decisions: stats.total,
                required: this.minDecisionsForEvolution,
            };
        }

        api?.logger?.info(`[ClosedLoopEvolver] Starting evolution cycle #${this.evolutionCount + 1}`);
        api?.logger?.info(`[ClosedLoopEvolver] Stats: ${stats.total} decisions, avg=${stats.avgScore.toFixed(1)}, rate=${(stats.successRate * 100).toFixed(1)}%`);

        // Step 1: Run optimizer analysis
        const optimization = await selfOptimizer.optimize();
        api?.logger?.info(`[ClosedLoopEvolver] Optimization: ${optimization.recommendations.length} recommendations`);

        // Step 2: Run evolver to generate rules
        const evolutionResult = await selfEvolver.evolve();
        api?.logger?.info(`[ClosedLoopEvolver] Evolution: ${evolutionResult.newRules.length} new rules, ${evolutionResult.retiredRules.length} retired`);

        // Step 3: Generate HYBRID rules (mandatory + suggestion)
        const generatedRules = generateRulesFromEvolution(evolutionResult, stats);
        
        // Convert to hybrid rules
        const mandatoryRules: Rule[] = [];
        const suggestionRules: Rule[] = [];

        for (const rule of generatedRules) {
            if (rule.type === 'safety' || rule.type === 'performance') {
                // Safety and performance rules become MANDATORY (Hook enforced)
                mandatoryRules.push({
                    ...rule,
                    type: 'mandatory' as const,
                    action: rule.type === 'safety' ? 'require_confirmation' : 'warn',
                    trigger: 'tool_call' as const,
                    triggerPattern: rule.examples?.[0] || rule.name,
                });
            } else {
                // Other rules become SUGGESTIONS (SOUL injected)
                suggestionRules.push({
                    ...rule,
                    type: 'suggestion' as const,
                    action: 'suggest',
                    trigger: 'tool_call' as const,
                    triggerPattern: rule.examples?.[0] || rule.name,
                });
            }
        }

        api?.logger?.info(`[ClosedLoopEvolver] Generated ${mandatoryRules.length} mandatory (Hook), ${suggestionRules.length} suggestion (SOUL)`);

        if (mandatoryRules.length === 0 && suggestionRules.length === 0) {
            // No rules to enforce, just log and exit
            appendEvolutionLog({
                action: 'no_rules_generated',
                optimization,
                evolutionResult,
                stats,
            });
            return {
                success: true,
                rulesGenerated: 0,
                reason: 'no_rules_needed',
            };
        }

        // Step 4: Persist rules to JSON (portable format for migration)
        const ruleStorage = getRuleStorage();
        for (const rule of mandatoryRules) {
            ruleStorage.addRule(rule);
        }
        for (const rule of suggestionRules) {
            ruleStorage.addRule(rule);
        }
        api?.logger?.info(`[ClosedLoopEvolver] Rules persisted to .eo-rules/rules.json`);

        // Step 5: ENFORCE rules
        if (this.autoEnforce) {
            // 5a: Apply suggestion rules to SOUL.md files
            if (suggestionRules.length > 0) {
                const soulSection = generateSuggestionSection();
                const enforceResult = applyRulesToAllAgents([], { additionalSection: soulSection });
                api?.logger?.info(`[ClosedLoopEvolver] Suggestion rules injected to ${enforceResult.success} SOUL files`);
            }

            // 5b: Mandatory rules are enforced by Hook automatically via .eo-rules/rules.json
            api?.logger?.info(`[ClosedLoopEvolver] Mandatory rules active: ${mandatoryRules.length} (Hook enforcement)`);

            // Log the full evolution
            appendEvolutionLog({
                action: 'closed_loop_evolution',
                evolutionCount: this.evolutionCount + 1,
                optimization,
                evolutionResult,
                rulesGenerated: mandatoryRules.length + suggestionRules.length,
                mandatoryRules: mandatoryRules.length,
                suggestionRules: suggestionRules.length,
                stats,
            });

            this.lastEvolution = now;
            this.evolutionCount++;

            return {
                success: true,
                rulesGenerated: mandatoryRules.length + suggestionRules.length,
                mandatoryRules: mandatoryRules.length,
                suggestionRules: suggestionRules.length,
                rulesPath: './.eo-rules/rules.json',
                mandatoryEnforced: mandatoryRules.length,
                suggestionEnforced: suggestionRules.length,
            };
        }
        else {
            // Dry run - don't enforce, just return
            return {
                success: true,
                rulesGenerated: mandatoryRules.length + suggestionRules.length,
                mandatoryRules: mandatoryRules.length,
                suggestionRules: suggestionRules.length,
                dryRun: true,
            };
        }
    }

    /**
     * Force evolution (bypass cooldown) - for testing
     */
    async forceEvolve(api: any): Promise<any> {
        const prevCooldown = this.cooldown;
        this.cooldown = 0;
        const result = await this.evolve(api);
        this.cooldown = prevCooldown;
        return result;
    }

    /**
     * Check if evolution should run
     */
    shouldEvolve(): boolean {
        const stats = effectTracker.stats();
        return stats.total >= this.minDecisionsForEvolution;
    }

    /**
     * Get evolution status
     */
    getStatus(): any {
        const stats = effectTracker.stats();
        const now = Date.now();
        const timeSinceLastEvolution = now - this.lastEvolution;
        const timeUntilNextEvolution = Math.max(0, this.cooldown - timeSinceLastEvolution);
        
        // Get rule counts from hybrid system
        const enforcer = getRuleEnforcer();
        const ruleStats = enforcer.getStats();

        return {
            enabled: this.enabled,
            evolutionCount: this.evolutionCount,
            lastEvolution: this.lastEvolution,
            timeUntilNextEvolution,
            cooldownHours: (this.cooldown / 3600000).toFixed(1),
            minDecisionsRequired: this.minDecisionsForEvolution,
            currentDecisions: stats.total,
            hasEnoughData: stats.total >= this.minDecisionsForEvolution,
            autoEnforce: this.autoEnforce,
            totalRules: ruleStats.total,
            mandatoryRules: ruleStats.mandatory,
            suggestionRules: ruleStats.suggestion,
        };
    }

    /**
     * Enable/disable auto-enforce
     */
    setAutoEnforce(enabled: boolean): void {
        this.autoEnforce = enabled;
    }

    /**
     * Get current mandatory rules
     */
    getCurrentRules(): any[] {
        const enforcer = getRuleEnforcer();
        return enforcer.getActiveRules();
    }

    /**
     * Get evolution history
     */
    getEvolutionHistory(limit: number = 20): any[] {
        return getEvolutionLog(limit);
    }

    /**
     * Export rules for migration
     */
    exportRules(agentId: string): any {
        const enforcer = getRuleEnforcer();
        return enforcer.exportRules(agentId);
    }

    /**
     * Import rules from package
     */
    importRules(pkg: any, strategy: 'merge' | 'replace' = 'merge'): void {
        const enforcer = getRuleEnforcer();
        enforcer.importRules(pkg, strategy);
    }

    /**
     * Manually trigger rule enforcement
     */
    enforceRulesNow(rules: any[], api: any): any {
        if (!rules || rules.length === 0) {
            return { success: false, error: 'No rules provided' };
        }
        const result = applyRulesToAllAgents(rules);
        appendEvolutionLog({
            action: 'manual_enforcement',
            rulesEnforced: result.success,
            details: result,
        });
        return result;
    }
}

export const closedLoopEvolver = new ClosedLoopEvolver();
