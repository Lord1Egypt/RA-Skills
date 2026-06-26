interface MCPToolResult {
    content: Array<{
        type: string;
        text: string;
    }>;
}
export declare function beforeQuery(query: string): Promise<string>;
export declare function afterResponse(query: string, response: string): Promise<void>;
export declare const tools: ({
    name: string;
    description: string;
    inputSchema: {
        type: string;
        properties: {
            query: {
                type: string;
                description: string;
            };
            limit: {
                type: string;
                description: string;
            };
            domain: {
                type: string;
                description: string;
            };
            response?: undefined;
            pattern_cid?: undefined;
            context?: undefined;
            stance?: undefined;
        };
        required: string[];
    };
} | {
    name: string;
    description: string;
    inputSchema: {
        type: string;
        properties: {
            query: {
                type: string;
                description: string;
            };
            response: {
                type: string;
                description: string;
            };
            domain: {
                type: string;
                description: string;
            };
            limit?: undefined;
            pattern_cid?: undefined;
            context?: undefined;
            stance?: undefined;
        };
        required: string[];
    };
} | {
    name: string;
    description: string;
    inputSchema: {
        type: string;
        properties: {
            pattern_cid: {
                type: string;
                description: string;
            };
            context: {
                type: string;
                description: string;
            };
            stance: {
                type: string;
                enum: string[];
                description: string;
            };
            query?: undefined;
            limit?: undefined;
            domain?: undefined;
            response?: undefined;
        };
        required: string[];
    };
})[];
export declare function callTool(name: string, args: Record<string, unknown>): Promise<MCPToolResult>;
export declare function shutdown(): Promise<void>;
export {};
//# sourceMappingURL=index.d.ts.map