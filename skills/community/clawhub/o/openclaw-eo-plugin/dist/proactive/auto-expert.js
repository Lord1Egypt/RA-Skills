/**
 * Auto Expert
 * Automatically suggests or triggers expert invocation
 */
import { detectIntention } from './intention-detector.js';
export function suggestExpert(message) {
    const intent = detectIntention(message);
    if (intent.score < 0.3 || !intent.suggestedCommand) {
        return null;
    }
    const toolMessages = {
        eo_collab: '🎯 I notice you might benefit from our multi-expert collaboration system. Try: eo_collab',
        eo_plan: '📋 I can invoke a Planner expert to help structure your project. Try: eo_plan task=<your task>',
        eo_architect: '🏗️ I can invoke an Architect expert to design your system. Try: eo_architect task=<your system>',
        eo_code_review: '🔍 I can invoke CodeReviewer experts to analyze your code. Try: eo_code_review path=<path>',
        eo_verify: '✅ I can invoke QA experts to verify your checkpoint. Try: eo_verify checkpoint=<name>',
    };
    return {
        toolName: intent.suggestedCommand,
        confidence: intent.score,
        message: toolMessages[intent.suggestedCommand] || `💡 Try: ${intent.suggestedCommand}`,
    };
}
export function logIntention(api, intent, message) {
    if (intent.score >= 0.2) {
        api.logger.debug(`[EO Proactive] Intention detected: score=${intent.score.toFixed(2)} signals=[${intent.signals.join(', ')}]`);
    }
}
//# sourceMappingURL=auto-expert.js.map