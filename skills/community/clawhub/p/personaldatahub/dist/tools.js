/**
 * OpenClaw tools that the agent can call to interact with personal data.
 */
/**
 * Tool parameter schemas using plain JSON Schema objects
 * (compatible with @sinclair/typebox Type.Object format).
 */
export const PULL_TOOL_SCHEMA = {
    type: 'object',
    properties: {
        source: {
            type: 'string',
            description: 'The data source to pull from (e.g., "gmail")',
        },
        type: {
            type: 'string',
            description: 'The data type to pull (e.g., "email"). Optional.',
        },
        query: {
            type: 'string',
            description: 'Search query in source-native syntax (e.g., Gmail search syntax: "is:unread from:alice"). Optional.',
        },
        limit: {
            type: 'number',
            description: 'Maximum number of results to return. Optional.',
        },
        purpose: {
            type: 'string',
            description: 'A clear description of why this data is needed. Required for transparency and audit.',
        },
    },
    required: ['source', 'purpose'],
};
export const PROPOSE_TOOL_SCHEMA = {
    type: 'object',
    properties: {
        source: {
            type: 'string',
            description: 'The source service for this action (e.g., "gmail")',
        },
        action_type: {
            type: 'string',
            description: 'The type of action to propose (e.g., "draft_email", "send_email", "reply_email")',
        },
        to: {
            type: 'string',
            description: 'Recipient email address',
        },
        subject: {
            type: 'string',
            description: 'Email subject line',
        },
        body: {
            type: 'string',
            description: 'Email body content',
        },
        in_reply_to: {
            type: 'string',
            description: 'Message ID to reply to (for reply_email and threaded draft_email). Optional.',
        },
        purpose: {
            type: 'string',
            description: 'A clear description of why this action is being proposed. Required for transparency and audit.',
        },
    },
    required: ['source', 'action_type', 'to', 'subject', 'body', 'purpose'],
};
/**
 * Create the personal_data_pull tool definition.
 */
export function createPullTool(client) {
    return {
        name: 'personal_data_pull',
        label: 'Pull Personal Data',
        description: 'Pull personal data from a source through the PersonalDataHub access control gateway. ' +
            'Data is filtered, redacted, and shaped according to the owner\'s access control policy. ' +
            'Always provide a clear purpose explaining why the data is needed.',
        parameters: PULL_TOOL_SCHEMA,
        async execute(_toolCallId, args) {
            const source = args.source;
            const purpose = args.purpose;
            const type = args.type;
            const query = args.query;
            const limit = args.limit;
            const params = {};
            if (query)
                params.query = query;
            if (limit)
                params.limit = limit;
            const result = await client.pull({
                source,
                type,
                params: Object.keys(params).length > 0 ? params : undefined,
                purpose,
            });
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify(result, null, 2),
                    },
                ],
            };
        },
    };
}
/**
 * Create the personal_data_propose tool definition.
 */
export function createProposeTool(client) {
    return {
        name: 'personal_data_propose',
        label: 'Propose Personal Data Action',
        description: 'Propose an outbound action (e.g., draft email, send email) through the PersonalDataHub access control gateway. ' +
            'The action is staged for owner review — it will NOT execute until the owner approves it in the PersonalDataHub GUI. ' +
            'Always provide a clear purpose explaining why this action is being proposed.',
        parameters: PROPOSE_TOOL_SCHEMA,
        async execute(_toolCallId, args) {
            const source = args.source;
            const action_type = args.action_type;
            const purpose = args.purpose;
            const action_data = {
                to: args.to,
                subject: args.subject,
                body: args.body,
            };
            if (args.in_reply_to) {
                action_data.in_reply_to = args.in_reply_to;
            }
            const result = await client.propose({
                source,
                action_type,
                action_data,
                purpose,
            });
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify(result, null, 2),
                    },
                ],
            };
        },
    };
}
