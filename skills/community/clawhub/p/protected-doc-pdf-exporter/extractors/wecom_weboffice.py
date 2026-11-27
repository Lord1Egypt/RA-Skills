"""
WeCom Drive / Weboffice Canvas Tile Extractor
Specialized for drive.weixin.qq.com and weboffice.work.weixin.qq.com.
Traverses nested iframes, finds the WPS Weboffice context,
and dynamically composites arbitrary Canvas Tiles into clean vector-sharp images.
"""

import os
import time
import json
import base64
import asyncio
from .base import BaseExtractor

class WeComWebofficeExtractor(BaseExtractor):
    def __init__(self, ws, ws_url: str):
        super().__init__(ws, ws_url)
        self.ctx_id = None
        self.total_pages = 0

    @classmethod
    def can_handle(cls, url: str) -> bool:
        return any(k in url.lower() for k in [
            'drive.weixin.qq.com',
            'weboffice.work.weixin.qq.com',
            'wedrive'
        ])

    async def _eval_js(self, expr: str):
        m_id = int(time.time() * 1000) % 100000 + 200
        await self.ws.send(json.dumps({
            'id': m_id,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': expr,
                'contextId': self.ctx_id,
                'returnByValue': True,
                'awaitPromise': True
            }
        }))
        while True:
            r = json.loads(await self.ws.recv())
            if r.get('id') == m_id:
                return r.get('result', {}).get('result', {}).get('value')

    async def prepare(self) -> int:
        await self.ws.send(json.dumps({'id': 10, 'method': 'Runtime.enable'}))

        # Wait for Weboffice execution context
        start_t = time.time()
        while time.time() - start_t < 25:
            try:
                res = json.loads(await asyncio.wait_for(self.ws.recv(), timeout=2.0))
                if res.get('method') == 'Runtime.executionContextCreated':
                    ctx = res['params']['context']
                    if 'weboffice' in ctx['origin']:
                        self.ctx_id = ctx['id']
                        break
            except asyncio.TimeoutError:
                continue

        if self.ctx_id is None:
            raise RuntimeError("Weboffice iframe context not found. Make sure user has logged in.")

        # Wait for pdf-page elements
        for _ in range(30):
            self.total_pages = await self._eval_js('document.querySelectorAll(".pdf-page").length') or 0
            if self.total_pages > 0:
                break
            await asyncio.sleep(0.5)

        if self.total_pages == 0:
            raise RuntimeError("No .pdf-page elements found in document.")

        return self.total_pages

    async def extract_page(self, page_index: int, temp_dir: str) -> str:
        # Dynamic composite JS: handles arbitrary tile dimensions, orientations, and splits
        expr = f'''
        (async () => {{
            const pages = document.querySelectorAll('.pdf-page');
            if (!pages || !pages[{page_index}]) return null;
            const p = pages[{page_index}];
            p.scrollIntoView({{ behavior: 'instant', block: 'center' }});

            let tries = 0;
            while (tries < 45) {{
                const canvases = Array.from(p.querySelectorAll('canvas'));
                if (canvases.length > 0 && canvases.every(c => c.className.includes('loaded') || c.className.includes('img-loaded'))) {{
                    break;
                }}
                await new Promise(r => setTimeout(r, 150));
                tries++;
            }}

            const canvases = Array.from(p.querySelectorAll('canvas'));
            if (!canvases.length) return null;

            let minX = Infinity, minY = Infinity, maxX = 0, maxY = 0;
            const parsedTiles = canvases.map(c => {{
                const cssLeft = parseFloat(c.style.left) || 0;
                const cssTop = parseFloat(c.style.top) || 0;
                const cssW = parseFloat(c.style.width) || c.offsetWidth || (c.width / 2);
                const cssH = parseFloat(c.style.height) || c.offsetHeight || (c.height / 2);
                const scaleX = c.width / cssW;
                const scaleY = c.height / cssH;

                const x = Math.round(cssLeft * scaleX);
                const y = Math.round(cssTop * scaleY);
                const w = c.width;
                const h = c.height;

                minX = Math.min(minX, x);
                minY = Math.min(minY, y);
                maxX = Math.max(maxX, x + w);
                maxY = Math.max(maxY, y + h);

                return {{ c, x, y, w, h }};
            }});

            const totalW = maxX - minX;
            const totalH = maxY - minY;
            if (totalW <= 0 || totalH <= 0) return null;

            const out = document.createElement('canvas');
            out.width = totalW;
            out.height = totalH;
            const ctx = out.getContext('2d');
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, totalW, totalH);

            for (const tile of parsedTiles) {{
                ctx.drawImage(tile.c, tile.x - minX, tile.y - minY);
            }}

            return out.toDataURL('image/png');
        }})()
        '''

        data_url = await self._eval_js(expr)
        if not data_url:
            await asyncio.sleep(1)
            data_url = await self._eval_js(expr)

        if not data_url:
            raise RuntimeError(f"Failed to capture Canvas data for page {page_index + 1}.")

        data = base64.b64decode(data_url.split(',')[1])
        img_path = os.path.join(temp_dir, f"page_{page_index + 1:03d}.png")
        with open(img_path, 'wb') as f:
            f.write(data)

        return img_path
