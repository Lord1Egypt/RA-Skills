export interface MemoryMaxConfig {
    enableRulePinning?: boolean;
    enableAutoCapture?: boolean;
    enableAutoRecall?: boolean;
}
declare const memoryMaxPlugin: {
    id: string;
    name: string;
    description: string;
    configSchema: {
        type: string;
        additionalProperties: boolean;
        properties: {
            enableRulePinning: {
                type: string;
                default: boolean;
            };
            enableAutoCapture: {
                type: string;
                default: boolean;
            };
            enableAutoRecall: {
                type: string;
                default: boolean;
            };
        };
    };
    register(api: any): void;
};
export default memoryMaxPlugin;
