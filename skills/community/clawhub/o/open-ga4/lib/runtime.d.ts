import { type CredentialProbe } from "./auth/credentials.js";
import { type Ga4Client, type MetadataResponse } from "./ga4/client.js";
import type { FetchLike } from "./ga4/http.js";
import { type AuditLogger } from "./privacy/audit.js";
import type { ResolvedConfig } from "./config.js";
/**
 * Lazily assembled per-process state.
 *
 * Nothing here runs at startup. Credentials are read the first time a command
 * actually needs them, so installing the skill does not touch a key file, and
 * an OpenClaw instance that never asks an analytics question never opens one.
 */
export type Ga4Runtime = {
    config: ResolvedConfig;
    /** Opt-in local record of what was asked. Never records what came back. */
    audit: AuditLogger;
    client(): Promise<Ga4Client>;
    /** The service-account address, for "grant access to X" messages. */
    principal(): string | undefined;
    probes(): CredentialProbe[];
    resolveProperty(explicit?: string): string;
    metadata(propertyId: string, signal?: AbortSignal): Promise<MetadataResponse>;
    /**
     * Dimension names this property, specifically, treats as person-identifying:
     * its user-scoped custom definitions and every deprecated alias of anything
     * the policy blocks. Names a shipped list cannot know.
     */
    userIdentifyingDimensions(propertyId: string, signal?: AbortSignal): Promise<Set<string>>;
};
export type RuntimeOptions = {
    config: ResolvedConfig;
    env?: NodeJS.ProcessEnv;
    fetchImpl?: FetchLike;
    onWarning?: (message: string) => void;
};
export declare function createRuntime(options: RuntimeOptions): Ga4Runtime;
