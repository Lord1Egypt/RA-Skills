/**
 * EO Self-Learning Tool Handler
 * Self-Learning Engine for feedback and patterns
 */
import { SelfLearningOrchestrator } from '../self-learning/orchestrator.js';
import { textResult } from '../formatters/index.js';
import { WORKSPACE } from '../config.js';
const selfLearning = new SelfLearningOrchestrator(WORKSPACE, { enabled: true });
export function handleSelfLearn(params) {
    const s = selfLearning.getStatus();
    return textResult(`Self-Learning: Enabled=${s.enabled}, Feedback=${s.feedbackCount}, Patterns=${s.patternCount}`);
}
//# sourceMappingURL=self-learn.js.map