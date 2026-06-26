import { CompressedMessage, CompressionResult, ContextMessage } from './types';
export declare class ContextCompressor {
    private maxMessages;
    private keepRecentCount;
    private enableCompression;
    setMaxMessages(max: number): void;
    setKeepRecentCount(count: number): void;
    setEnableCompression(enabled: boolean): void;
    compress(messages: ContextMessage[]): CompressionResult;
    private classifyMessages;
    private categorizeMessage;
    private compressMessages;
    private shouldPreserve;
    private summarize;
    getPreservedMessages(compressed: CompressedMessage[]): ContextMessage[];
    private isMeaningless;
    private isGreeting;
    private isConfirmation;
    private containsKeywords;
}
//# sourceMappingURL=compressor.d.ts.map