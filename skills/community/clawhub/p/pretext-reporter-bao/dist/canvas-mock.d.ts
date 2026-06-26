/**
 * Pretext 测试脚本
 * 测试文本测量和布局功能
 */
declare class MockCanvas {
    private ctx;
    constructor(width: number, height: number);
    get context(): MockContext;
    toDataURL(type?: string): string;
}
declare class MockContext {
    private width;
    private height;
    private fillColor;
    private font;
    private textAlign;
    private textBaseline;
    private content;
    constructor(width: number, height: number);
    get canvas(): {
        width: number;
        height: number;
    };
    fillRect(x: number, y: number, w: number, h: number): void;
    fillStyle: string;
    set fillStyle(value: string);
    measureText(text: string): {
        width: number;
        actualBoundingBoxLeft: number;
        actualBoundingBoxRight: number;
        actualBoundingBoxAscent: number;
        actualBoundingBoxDescent: number;
        fontBoundingBoxAscent: number;
        fontBoundingBoxDescent: number;
    };
}
export { MockCanvas, MockContext };
//# sourceMappingURL=canvas-mock.d.ts.map