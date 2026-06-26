/**
 * Auto Expert
 * Automatically suggests or triggers expert invocation
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { type IntentionSignal } from './intention-detector.js';
export interface AutoExpertSuggestion {
    toolName: string;
    confidence: number;
    message: string;
}
export declare function suggestExpert(message: string): AutoExpertSuggestion | null;
export declare function logIntention(api: OpenClawPluginApi, intent: IntentionSignal, message: string): void;
//# sourceMappingURL=auto-expert.d.ts.map