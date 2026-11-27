"""
Universal DOM & Viewport Stepper Extractor
Fallback for web presentations, slide readers, Feishu, Baidu Wenku,
and custom online documents using DOM elements or keyboard paging.
"""

import os
import time
import json
import base64
import asyncio
from .base import BaseExtractor

class DOMStepperExtractor(BaseExtractor):
    def __init__(self, ws, ws_url: str):
        super().__init__(ws, ws_url)
        self.page_selector = None
        self.total_pages = 0

    @classmethod
    def can_handle(cls, url: str) -> bool:
        # Generic fallback that can handle any web document
        return True

    async def _eval_js(self, expr: str):
        m_id = int(time.time() * 1000) % 100000 + 300
        await self.ws.send(json.dumps({
            'id': m_id,
            'method': 'Runtime.evaluate',
            'params': {'expression': expr, 'returnByValue': True, 'awaitPromise': True}
        }))
        while True:
            r = json.loads(await self.ws.recv())
            if r.get('id') == m_id:
                return r.get('result', {}).get('result', {}).get('value')

    async def prepare(self) -> int:
        await self.ws.send(json.dumps({'id': 11, 'method': 'Page.enable'}))
        await self.ws.send(json.dumps({'id': 12, 'method': 'DOM.enable'}))

        # Hide watermarks and fixed navigation bars
        clean_css = '''
        (() => {
            const style = document.createElement('style');
            style.textContent = `
                [class*="watermark"], [class*="water-mark"], [id*="watermark"],
                .reader-watermark, .doc-watermark, .fixed-watermark {
                    display: none !important;
                    opacity: 0 !important;
                }
            `;
            document.head.appendChild(style);
        })()
        '''
        await self._eval_js(clean_css)

        # Detect candidate page containers
        detect_script = '''
        (() => {
            const selectors = [
                '.pdf-page', '.page', '.reader-page', '.slide-item',
                '.ppt-page', '[data-page-index]', '[data-page]',
                '.canvas-container', '.page-container'
            ];
            for (const sel of selectors) {
                const count = document.querySelectorAll(sel).length;
                if (count > 1) {
                    return { selector: sel, count };
                }
            }
            return { selector: null, count: 1 };
        })()
        '''
        info = await self._eval_js(detect_script)
        if info and info.get('selector'):
            self.page_selector = info['selector']
            self.total_pages = info['count']
        else:
            self.total_pages = 1

        return self.total_pages

    async def extract_page(self, page_index: int, temp_dir: str) -> str:
        if self.page_selector:
            # Scroll page element into view and get its bounding rect
            rect = await self._eval_js(f'''
            (() => {{
                const els = document.querySelectorAll('{self.page_selector}');
                if (!els || !els[{page_index}]) return null;
                const el = els[{page_index}];
                el.scrollIntoView({{ behavior: 'instant', block: 'center' }});
                const r = el.getBoundingClientRect();
                return {{
                    x: Math.round(r.x),
                    y: Math.round(r.y),
                    width: Math.round(r.width),
                    height: Math.round(r.height),
                    scale: 2
                }};
            }})()
            ''')
            await asyncio.sleep(0.4)

            shot_id = int(time.time() * 1000) % 100000 + 400
            clip_params = rect if rect and rect.get('width') > 50 else None
            req = {
                'id': shot_id,
                'method': 'Page.captureScreenshot',
                'params': {'format': 'png'}
            }
            if clip_params:
                req['params']['clip'] = clip_params

            await self.ws.send(json.dumps(req))
            while True:
                r = json.loads(await self.ws.recv())
                if r.get('id') == shot_id:
                    data = base64.b64decode(r['result']['data'])
                    break
        else:
            # Single viewport screenshot
            shot_id = int(time.time() * 1000) % 100000 + 500
            await self.ws.send(json.dumps({'id': shot_id, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}))
            while True:
                r = json.loads(await self.ws.recv())
                if r.get('id') == shot_id:
                    data = base64.b64decode(r['result']['data'])
                    break

        img_path = os.path.join(temp_dir, f"page_{page_index + 1:03d}.png")
        with open(img_path, 'wb') as f:
            f.write(data)

        return img_path
