import type { PluginCommandContext, PluginCommandResult } from '../types/index.js';
import { executePlan } from './plan.js';
import { executeArchitect } from './architect.js';
import { executeVerify } from './verify.js';
import { executeCodeReview } from './code-review.js';
export declare const EO_COMMANDS: readonly [{
    readonly name: "plan";
    readonly description: "Create a structured project plan with PM + Engineer + QA expert team";
    readonly acceptsArgs: true;
    readonly handler: (ctx: PluginCommandContext) => Promise<PluginCommandResult>;
}, {
    readonly name: "architect";
    readonly description: "Design system architecture with architect + tech-lead + DBA expert team";
    readonly acceptsArgs: true;
    readonly handler: (ctx: PluginCommandContext) => Promise<PluginCommandResult>;
}, {
    readonly name: "verify";
    readonly description: "Verify implementation against specifications (code, architecture, test, security, performance)";
    readonly acceptsArgs: true;
    readonly handler: (ctx: PluginCommandContext) => Promise<PluginCommandResult>;
}, {
    readonly name: "code-review";
    readonly description: "Perform code review with code-reviewer + senior-dev experts";
    readonly acceptsArgs: true;
    readonly handler: (ctx: PluginCommandContext) => Promise<PluginCommandResult>;
}];
export declare function parsePlanArgs(args: string): {
    task: string;
    team?: string[];
    constraints?: string[];
    priority?: string;
};
export declare function parseArchitectArgs(args: string): {
    task: string;
    style?: string;
    language?: string;
};
export declare function parseVerifyArgs(args: string): {
    target: string;
    type: string;
    criteria?: string[];
};
export declare function parseCodeReviewArgs(args: string): {
    files?: string[];
    prUrl?: string;
    focus?: string[];
    depth?: string;
};
export { executePlan, executeArchitect, executeVerify, executeCodeReview };
//# sourceMappingURL=index.d.ts.map