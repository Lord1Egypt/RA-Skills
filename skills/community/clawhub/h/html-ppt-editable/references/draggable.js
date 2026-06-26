/**
 * 拖拽文字框扩展
 * 在 SlideEditor 初始化后调用 setupDraggable(el) 即可
 */
class DraggableText {
    constructor(el) {
        this.el = el;
        this.isDragging = false;
        this.offsetX = 0;
        this.offsetY = 0;
        this.init();
    }

    init() {
        this.el.style.cursor = 'grab';
        this.el.style.position = 'absolute';
        this.el.style.userSelect = 'none';

        this.el.addEventListener('mousedown', (e) => {
            if (e.target.closest('input, select, button, [contenteditable]' === 'true')) return;
            this.startDrag(e);
        });

        document.addEventListener('mousemove', (e) => this.onDrag(e));
        document.addEventListener('mouseup', () => this.stopDrag());
    }

    startDrag(e) {
        this.isDragging = true;
        const slide = this.el.closest('.slide');
        const slideRect = slide.getBoundingClientRect();
        const elRect = this.el.getBoundingClientRect();
        this.offsetX = e.clientX - (elRect.left - slideRect.left);
        this.offsetY = e.clientY - (elRect.top - slideRect.top);
        this.el.style.cursor = 'grabbing';
        this.el.style.zIndex = '999';
    }

    onDrag(e) {
        if (!this.isDragging) return;
        const slide = this.el.closest('.slide');
        const slideRect = slide.getBoundingClientRect();
        this.el.style.left = (e.clientX - slideRect.left - this.offsetX) + 'px';
        this.el.style.top = (e.clientY - slideRect.top - this.offsetY) + 'px';
    }

    stopDrag() {
        this.isDragging = false;
        this.el.style.cursor = 'grab';
        this.el.style.zIndex = '';
    }
}

// 使用方式：
// new DraggableText(document.querySelector('.slide-content'));
