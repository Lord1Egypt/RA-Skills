/**
 * OpenClaw tools that the agent can call to interact with personal data.
 */
import type { HubClient } from './hub-client.js';
/**
 * Tool parameter schemas using plain JSON Schema objects
 * (compatible with @sinclair/typebox Type.Object format).
 */
export declare const PULL_TOOL_SCHEMA: {
    type: "object";
    properties: {
        source: {
            type: "string";
            description: string;
        };
        type: {
            type: "string";
            description: string;
        };
        query: {
            type: "string";
            description: string;
        };
        limit: {
            type: "number";
            description: string;
        };
        purpose: {
            type: "string";
            description: string;
        };
    };
    required: readonly ["source", "purpose"];
};
export declare const PROPOSE_TOOL_SCHEMA: {
    type: "object";
    properties: {
        source: {
            type: "string";
            description: string;
        };
        action_type: {
            type: "string";
            description: string;
        };
        to: {
            type: "string";
            description: string;
        };
        subject: {
            type: "string";
            description: string;
        };
        body: {
            type: "string";
            description: string;
        };
        in_reply_to: {
            type: "string";
            description: string;
        };
        purpose: {
            type: "string";
            description: string;
        };
    };
    required: readonly ["source", "action_type", "to", "subject", "body", "purpose"];
};
/**
 * Create the personal_data_pull tool definition.
 */
export declare function createPullTool(client: HubClient): {
    name: string;
    label: string;
    description: string;
    parameters: {
        type: "object";
        properties: {
            source: {
                type: "string";
                description: string;
            };
            type: {
                type: "string";
                description: string;
            };
            query: {
                type: "string";
                description: string;
            };
            limit: {
                type: "number";
                description: string;
            };
            purpose: {
                type: "string";
                description: string;
            };
        };
        required: readonly ["source", "purpose"];
    };
    execute(_toolCallId: string, args: Record<string, unknown>): Promise<{
        content: {
            type: "text";
            text: string;
        }[];
    }>;
};
/**
 * Create the personal_data_propose tool definition.
 */
export declare function createProposeTool(client: HubClient): {
    name: string;
    label: string;
    description: string;
    parameters: {
        type: "object";
        properties: {
            source: {
                type: "string";
                description: string;
            };
            action_type: {
                type: "string";
                description: string;
            };
            to: {
                type: "string";
                description: string;
            };
            subject: {
                type: "string";
                description: string;
            };
            body: {
                type: "string";
                description: string;
            };
            in_reply_to: {
                type: "string";
                description: string;
            };
            purpose: {
                type: "string";
                description: string;
            };
        };
        required: readonly ["source", "action_type", "to", "subject", "body", "purpose"];
    };
    execute(_toolCallId: string, args: Record<string, unknown>): Promise<{
        content: {
            type: "text";
            text: string;
        }[];
    }>;
};
