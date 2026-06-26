export interface HooksConfig {
    enableAutoCapture?: boolean;
    enableAutoRecall?: boolean;
    enableRulePinning?: boolean;
}
export declare function registerHooks(api: any, config?: HooksConfig): void;
