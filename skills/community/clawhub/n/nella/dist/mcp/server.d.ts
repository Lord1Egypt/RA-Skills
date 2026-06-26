#!/usr/bin/env node
import { ContextManager } from '@usenella/core';

/**
 * Challenge-Response Heartbeat
 *
 * Lightweight challenge-response mechanism to verify trust chain continuity
 * between tool calls. If an injection hijacks the agent's behavior, the
 * challenge-response will fail on the next tool call.
 *
 * Flow:
 * 1. nella_get_context issues the first challenge
 * 2. Agent includes the challenge response in its next nella tool call
 * 3. System verifies and issues a new challenge
 * 4. If verification fails → warning (trust chain may be compromised)
 *
 * Part of the prompt injection defense system (Layer 4 upgrade).
 */

interface ChallengeState {
    /** Current active challenge the agent should respond to */
    currentChallenge: string;
    /** Number of successful verifications in this session */
    verifiedCount: number;
    /** Number of failed verifications */
    failedCount: number;
    /** Whether the last verification succeeded */
    lastVerified: boolean;
    /** Timestamp of last verification */
    lastVerifiedAt?: string;
}

/**
 * Nella MCP Server
 *
 * Model Context Protocol server that exposes Nella's codebase intelligence
 * to AI agents like Claude.
 *
 * Usage:
 *   npx -y @getnella/mcp --workspace /path/to/project  # direct stdio entrypoint
 *   nella mcp --workspace /path/to/project            # via CLI subcommand
 */

interface ServerContext {
    workspacePath: string;
    contextManager: ContextManager;
    /** Per-session trust token for prompt injection defense (L4) */
    sessionToken?: string;
    /** HMAC signing key derived from session token (L4+) */
    hmacKey?: Buffer;
    /** Challenge-response state for trust chain verification (L4+) */
    challengeState?: ChallengeState;
}
declare function startMcpServer(args: {
    workspace?: string;
    help?: boolean;
}): Promise<void>;

export { type ServerContext, startMcpServer };
