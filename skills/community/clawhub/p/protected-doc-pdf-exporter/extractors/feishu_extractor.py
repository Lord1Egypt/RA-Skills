"""
Feishu / Lark Document & Slide Extractor
Supports Feishu DocX, Wiki, Docs, Slides, and Cloud Drive file previews.
Handles both slide-based presentations and continuous long documents (with auto-A4 slicing).
"""

import os
import time
import json
import base64
import asyncio
from typing import List
from .base import BaseExtractor

class FeishuExtractor(BaseExtractor):
    def __init__(self, ws, ws_url: str):
        super().__init__(ws, ws_url)
        self.doc_type = 'unknown'  # 'slides', 'docx', 'file_pdf'
        self.total_pages = 1

    @classmethod
    def can_handle(cls, url: str) -> bool:
        url_l = url.lower()
        return any(k in url_l for k in [
            'feishu.cn',
            'larksuite.com',
            'feishu.net'
        ])

    async def _eval_js(self, expr: str):
        m_id = int(time.time() * 1000) % 100000 + 800
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
        await self.ws.send(json.dumps({'id': 20, 'method': 'Page.enable'}))
        await self.ws.send(json.dumps({'id': 21, 'method': 'DOM.enable'}))

        # Wait for page to initialize
        await asyncio.sleep(3)

        # Inject universal Feishu clean-up styles (hides watermarks, headers, sidebars, toolbars)
        clean_css = '''
        (() => {
            const style = document.createElement('style');
            style.textContent = `
                /* Hide watermarks */
                .watermark-wrapper, .doc-watermark, [class*="watermark"],
                [class*="water-mark"], [id*="watermark"], div[style*="pointer-events: none"] {
                    display: none !important;
                    opacity: 0 !important;
                }
                /* Hide fixed headers & navbars */
                .suite-navigation-wrapper, .doc-header, .header-wrapper,
                .wiki-sidebar, .doc-catalog, .catalog-wrapper,
                .quick-action-bar, .comment-bubble, .selection-toolbar {
                    display: none !important;
                }
                /* Expand main container */
                .bear-web-docx, .render-unit-wrapper, .docx-editor {
                    margin: 0 auto !important;
                    padding-top: 20px !important;
                }
            `;
            document.head.appendChild(style);
        })()
        '''
        await self._eval_js(clean_css)

        # Detect Feishu doc type
        detect_script = '''
        (() => {
            const path = window.location.pathname.toLowerCase();
            if (path.includes('/slides/') || path.includes('/presentation/')) {
                const thumbs = document.querySelectorAll('.slide-thumb-item, .page-item, .thumbnail-item');
                return { type: 'slides', count: Math.max(1, thumbs.length) };
            }
            if (path.includes('/file/') || path.includes('/drive/')) {
                const pdfPages = document.querySelectorAll('.pdf-page, .page');
                if (pdfPages.length > 0) {
                    return { type: 'file_pdf', count: pdfPages.length };
                }
            }
            // Continuous DocX / Wiki document
            // Calculate total scroll height
            const docContainer = document.querySelector('.bear-web-docx') ||
                                 document.querySelector('.render-unit-wrapper') ||
                                 document.body;
            const scrollH = Math.max(docContainer.scrollHeight, document.documentElement.scrollHeight, document.body.scrollHeight);
            const viewH = window.innerHeight || 900;
            const pageEstimate = Math.max(1, Math.ceil(scrollH / viewH));
            return { type: 'docx', count: pageEstimate, scrollH, viewH };
        })()
        '''
        info = await self._eval_js(detect_script)
        if info:
            self.doc_type = info.get('type', 'docx')
            self.total_pages = info.get('count', 1)
        else:
            self.doc_type = 'docx'
            self.total_pages = 1

        print(f"[*] Feishu Document Type: {self.doc_type.upper()} (Estimated pages/screens: {self.total_pages})")

        # For docx documents, scroll through smoothly to trigger lazy-load / block hydration
        if self.doc_type == 'docx':
            print("[*] Pre-scrolling document to trigger lazy-loaded blocks & images...")
            await self._eval_js('''
            (async () => {
                const step = 800;
                const maxScroll = document.body.scrollHeight;
                for (let y = 0; y < maxScroll; y += step) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 60));
                }
                window.scrollTo(0, 0);
            })()
            ''')
            await asyncio.sleep(1)

        return self.total_pages

    async def extract_page(self, page_index: int, temp_dir: str) -> str:
        shot_id = int(time.time() * 1000) % 100000 + 850

        if self.doc_type == 'slides':
            # Switch to slide
            await self._eval_js(f'''
            (() => {{
                const thumbs = document.querySelectorAll('.slide-thumb-item, .page-item, .thumbnail-item');
                if (thumbs && thumbs[{page_index}]) {{
                    thumbs[{page_index}].click();
                }}
            }})()
            ''')
            await asyncio.sleep(0.5)

            # Capture slide viewport
            await self.ws.send(json.dumps({
                'id': shot_id,
                'method': 'Page.captureScreenshot',
                'params': {'format': 'png'}
            }))

        elif self.doc_type == 'file_pdf':
            # Scroll pdf page into view
            rect = await self._eval_js(f'''
            (() => {{
                const pages = document.querySelectorAll('.pdf-page, .page');
                if (!pages || !pages[{page_index}]) return null;
                const p = pages[{page_index}];
                p.scrollIntoView({{ behavior: 'instant', block: 'center' }});
                const r = p.getBoundingClientRect();
                return {{ x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height), scale: 2 }};
            }})()
            ''')
            await asyncio.sleep(0.4)
            req = {'id': shot_id, 'method': 'Page.captureScreenshot', 'params': {'format': 'png'}}
            if rect and rect.get('width') > 100:
                req['params']['clip'] = rect
            await self.ws.send(json.dumps(req))

        else:
            # Continuous DocX / Wiki: scroll to viewport chunk
            await self._eval_js(f'''
            (() => {{
                const viewH = window.innerHeight || 900;
                window.scrollTo({{ top: {page_index} * viewH, behavior: 'instant' }});
            }})()
            ''')
            await asyncio.sleep(0.4)

            # Capture viewport screenshot
            await self.ws.send(json.dumps({
                'id': shot_id,
                'method': 'Page.captureScreenshot',
                'params': {'format': 'png'}
            }))

        while True:
            r = json.loads(await self.ws.recv())
            if r.get('id') == shot_id:
                data = base64.b64decode(r['result']['data'])
                break

        img_path = os.path.join(temp_dir, f"page_{page_index + 1:03d}.png")
        with open(img_path, 'wb') as f:
            f.write(data)

        return img_path
