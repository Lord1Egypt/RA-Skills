import { type LayoutCursor, type LayoutResult } from './layout.js';
declare const preparedInlineFlowBrand: unique symbol;
export type InlineFlowItem = {
    text: string;
    font: string;
    break?: 'normal' | 'never';
    extraWidth?: number;
};
export type PreparedInlineFlow = {
    readonly [preparedInlineFlowBrand]: true;
};
export type InlineFlowCursor = {
    itemIndex: number;
    segmentIndex: number;
    graphemeIndex: number;
};
export type InlineFlowFragment = {
    itemIndex: number;
    text: string;
    gapBefore: number;
    occupiedWidth: number;
    start: LayoutCursor;
    end: LayoutCursor;
};
export type InlineFlowLine = {
    fragments: InlineFlowFragment[];
    width: number;
    end: InlineFlowCursor;
};
export declare function prepareInlineFlow(items: InlineFlowItem[]): PreparedInlineFlow;
export declare function layoutNextInlineFlowLine(prepared: PreparedInlineFlow, maxWidth: number, start?: InlineFlowCursor): InlineFlowLine | null;
export declare function walkInlineFlowLines(prepared: PreparedInlineFlow, maxWidth: number, onLine: (line: InlineFlowLine) => void): number;
export declare function measureInlineFlow(prepared: PreparedInlineFlow, maxWidth: number, lineHeight: number): LayoutResult;
export {};
