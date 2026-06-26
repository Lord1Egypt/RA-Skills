import { type SegmentBreakKind, type WhiteSpaceMode } from './analysis.js';
declare const preparedTextBrand: unique symbol;
type PreparedCore = {
    widths: number[];
    lineEndFitAdvances: number[];
    lineEndPaintAdvances: number[];
    kinds: SegmentBreakKind[];
    simpleLineWalkFastPath: boolean;
    segLevels: Int8Array | null;
    breakableWidths: (number[] | null)[];
    breakablePrefixWidths: (number[] | null)[];
    discretionaryHyphenWidth: number;
    tabStopAdvance: number;
    chunks: PreparedLineChunk[];
};
export type PreparedText = {
    readonly [preparedTextBrand]: true;
};
type InternalPreparedText = PreparedText & PreparedCore;
export type PreparedTextWithSegments = InternalPreparedText & {
    segments: string[];
};
export type LayoutCursor = {
    segmentIndex: number;
    graphemeIndex: number;
};
export type LayoutResult = {
    lineCount: number;
    height: number;
};
export type LayoutLine = {
    text: string;
    width: number;
    start: LayoutCursor;
    end: LayoutCursor;
};
export type LayoutLineRange = {
    width: number;
    start: LayoutCursor;
    end: LayoutCursor;
};
export type LayoutLinesResult = LayoutResult & {
    lines: LayoutLine[];
};
export type PrepareProfile = {
    analysisMs: number;
    measureMs: number;
    totalMs: number;
    analysisSegments: number;
    preparedSegments: number;
    breakableSegments: number;
};
export type PrepareOptions = {
    whiteSpace?: WhiteSpaceMode;
};
export type PreparedLineChunk = {
    startSegmentIndex: number;
    endSegmentIndex: number;
    consumedEndSegmentIndex: number;
};
export declare function profilePrepare(text: string, font: string, options?: PrepareOptions): PrepareProfile;
export declare function prepare(text: string, font: string, options?: PrepareOptions): PreparedText;
export declare function prepareWithSegments(text: string, font: string, options?: PrepareOptions): PreparedTextWithSegments;
export declare function layout(prepared: PreparedText, maxWidth: number, lineHeight: number): LayoutResult;
export declare function walkLineRanges(prepared: PreparedTextWithSegments, maxWidth: number, onLine: (line: LayoutLineRange) => void): number;
export declare function measureNaturalWidth(prepared: PreparedTextWithSegments): number;
export declare function layoutNextLine(prepared: PreparedTextWithSegments, start: LayoutCursor, maxWidth: number): LayoutLine | null;
export declare function layoutWithLines(prepared: PreparedTextWithSegments, maxWidth: number, lineHeight: number): LayoutLinesResult;
export declare function clearCache(): void;
export declare function setLocale(locale?: string): void;
export {};
