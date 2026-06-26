/**
 * Pretext 测试脚本
 * 测试文本测量和布局功能
 */
// 模拟 Canvas API（用于测试，实际环境需要浏览器）
class MockCanvas {
    constructor(width, height) {
        this.ctx = new MockContext(width, height);
    }
    get context() {
        return this.ctx;
    }
    toDataURL(type) {
        return `data:${type || 'image/png'};base64,iVBORw0KG...`;
    }
}
class MockContext {
    constructor(width, height) {
        this.fillColor = '#000000';
        this.font = '16px Inter';
        this.textAlign = 'left';
        this.textBaseline = 'top';
        this.content = [];
        this.fillStyle = this.fillColor;
        this.width = width;
        this.height = height;
    }
    get canvas() {
        return {
            width: this.width,
            height: this.height,
        };
    }
    fillText(text, x, y) {
        this.content.push(`fillText: "${text}" at (${x}, ${y})`);
    }
    fillRect(x, y, w, h) {
        this.content.push(`fillRect: (${x}, ${y}, ${w}, ${h})`);
    }
    set fillStyle(value) {
        this.fillColor = value;
    }
    fillText(text, x, y) {
        this.content.push(`fillText: "${text}" at (${x}, ${y})`);
    }
    measureText(text) {
        // 简单估算：每个字符约 8px 宽
        const width = text.length * 8;
        return {
            width,
            actualBoundingBoxLeft: 0,
            actualBoundingBoxRight: width,
            actualBoundingBoxAscent: 14,
            actualBoundingBoxDescent: 4,
            fontBoundingBoxAscent: 14,
            fontBoundingBoxDescent: 4,
        };
    }
}
// 导出 MockCanvas
export { MockCanvas, MockContext };
