import { type RedactionOptions } from "./privacy/redact.js";
import { type AccessPolicy } from "./privacy/policy.js";
/**
 * Settings, resolved from the environment.
 *
 * Everything here is read from the process environment and never from argv.
 * That is deliberate for the four privacy settings: a command-line flag can be
 * set by the model, and a page title is attacker-controlled text that reaches
 * the model. An environment variable is set by a person.
 */
export type ResolvedConfig = {
    defaultPropertyId?: string;
    defaultRowLimit: number;
    redaction: RedactionOptions;
    access: AccessPolicy;
    auditLogPath?: string;
};
export declare function configFromEnv(env: NodeJS.ProcessEnv, onWarning?: (message: string) => void): ResolvedConfig;
