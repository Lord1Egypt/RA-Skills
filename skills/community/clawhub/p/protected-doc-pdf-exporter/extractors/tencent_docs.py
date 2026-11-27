"""
Tencent Docs (docs.qq.com / doc.weixin.qq.com) Extractor
Handles standard Tencent Docs online presentations, Word docs, and canvas-rendered pages.
"""

import os
import time
import json
import base64
import asyncio
from .base import BaseExtractor

class TencentDocsExtractor(BaseExtractor):
    def __init__(self, ws, ws_url: str):
        super().__init__(ws, ws_url)
        self.total_pages = 0

    @classmethod
    def can_handle(cls, url: str) -> bool:
        return any(k in url.lower() for k in [
            'docs.qq.com',
            'doc.weixin.qq.com'
        ])

    async def _eval_js(self, expr: str):
        m_id = int(time.time() * 1000) % 100000 + 600
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
        await self.ws.send(json.dumps({'id': 15, 'method': 'Page.enable'}))
        await self.ws.send(json.dumps({'id': 16, 'method': 'DOM.enable'}))

        # Wait for Tencent Docs canvas or page container to stabilize
        await asyncio.sleep(2)

        # Remove watermark and floating banners
        clean_script = '''
        (() => {
            const style = document.createElement('style');
            style.textContent = `
                .watermark-container, [class*="watermark"],
                .title-bar, .doc-header, .dui-toast-container {
                    display: none !important;
                }
            `;
            document.head.appendChild(style);
        })()
        '''
        await self._eval_js(clean_script)

        # Check for slide count or pages
        page_count = await self._eval_js('''
        (() => {
            // Check slide pages
            const slides = document.querySelectorAll('.slide-thumb-item, .page-item, .thumbnail-item');
            if (slides.length > 0) return slides.length;
            const canvases = document.querySelectorAll('canvas');
            if (canvases.length > 0) return canvases.length;
            return 1;
        })()
        ''')
        self.total_pages = max(1, page_count or 1)
        return self.total_pages

    async def extract_page(self, page_index: int, temp_dir: str) -> str:
        # Trigger page switch if slides exist
        await self._eval_js(f'''
        (() => {{
            const thumbs = document.querySelectorAll('.slide-thumb-item, .page-item, .thumbnail-item');
            if (thumbs && thumbs[{page_index}]) {{
                thumbs[{page_index}].click();
            }}
        }})()
        ''')
        await asyncio.sleep(0.6)

        # Capture main viewport/canvas
        shot_id = int(time.time() * 1000) % 100000 + 700
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
