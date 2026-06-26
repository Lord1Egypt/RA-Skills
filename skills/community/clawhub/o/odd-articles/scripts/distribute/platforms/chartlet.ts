/**
 * WeChat Chartlet (图片消息/贴图) publisher.
 *
 * Chartlet = 长图形式的图片消息，适合微贴图轮播图等内容
 *
 * Degradation strategy:
 *   L0: WeChat API → push directly to drafts (no browser needed)
 *   L1: CDP automation → Chrome-based
 *   L3: Manual → output file path for copy-paste
 */

import fs from 'node:fs';
import path from 'node:path';
import type { Manifest, PublishResult } from '../cdp-utils.ts';
import { loadCredentials, getAccessToken, uploadContentImage, fetchWithRetry, BUN_FETCH_OPTS } from '../wechat-api.ts';

const WECHAT_API_BASE = 'https://api.weixin.qq.com';

export async function publishChartlet(manifest: Manifest, preview: boolean): Promise<PublishResult> {
  const chartletData = manifest.outputs.chartlet;
  if (!chartletData) {
    return { platform: 'chartlet', status: 'skipped', message: 'No chartlet content in manifest' };
  }

  if (!chartletData.images || chartletData.images.length === 0) {
    return { platform: 'chartlet', status: 'manual', message: 'No images provided for chartlet' };
  }

  const existingImages: string[] = [];
  for (const img of chartletData.images) {
    if (fs.existsSync(img)) {
      existingImages.push(img);
    }
  }

  if (existingImages.length === 0) {
    return { platform: 'chartlet', status: 'manual', message: 'No valid image files found' };
  }

  // L0: Try WeChat API direct push
  if (!preview) {
    try {
      const result = await publishChartletViaApi(manifest, existingImages);
      return {
        platform: 'chartlet',
        status: 'success',
        message: `Chartlet pushed to drafts via API (media_id: ${result.mediaId})`,
      };
    } catch (err) {
      const reason = err instanceof Error ? err.message : String(err);
      console.log(`  [chartlet] API mode failed, falling back: ${reason}`);
    }
  }

  // L1/L3: Manual fallback - output image paths for user to upload manually
  return {
    platform: 'chartlet',
    status: preview ? 'manual' : 'manual',
    message: `Please upload these images to WeChat manually:\n${existingImages.map(p => `  - ${path.basename(p)}`).join('\n')}`,
  };
}

interface ChartletDraftResult {
  mediaId: string;
}

async function publishChartletViaApi(manifest: Manifest, imagePaths: string[]): Promise<ChartletDraftResult> {
  const chartletData = manifest.outputs.chartlet!;
  
  // 1. Load credentials
  const creds = loadCredentials();
  if (!creds) throw new Error('No WeChat API credentials configured');

  console.log('  [chartlet] Starting API publish flow...');

  // 2. Get access token
  const token = await getAccessToken(creds);

  // 3. Upload images and build content with img tags
  console.log(`  [chartlet] Uploading ${imagePaths.length} image(s)...`);
  const uploadedUrls: string[] = [];

  for (const imgPath of imagePaths) {
    try {
      const url = await uploadContentImage(token, imgPath);
      uploadedUrls.push(url);
      console.log(`  [chartlet]   ✓ ${path.basename(imgPath)}`);
    } catch (err) {
      console.warn(`  [chartlet]   ✗ ${path.basename(imgPath)}: ${err instanceof Error ? err.message : err}`);
    }
  }

  if (uploadedUrls.length === 0) {
    throw new Error('Failed to upload any images');
  }

  // 4. Build content - embed images as single column
  const title = chartletData.title || manifest.title;
  const author = chartletData.author || 'oddmeta';
  
  // For chartlet, we create a simple HTML with images stacked
  const content = buildChartletContent(uploadedUrls);

  // 5. Create draft with chartlet content
  console.log('  [chartlet] Creating chartlet draft...');
  const draft = await createChartletDraft(token, {
    title,
    author,
    content,
  });

  console.log(`  [chartlet] Draft created successfully (media_id: ${draft.media_id})`);
  return { mediaId: draft.media_id };
}

function buildChartletContent(imageUrls: string[]): string {
  // Build HTML content with images stacked vertically
  // Each image takes full width
  const imagesHtml = imageUrls
    .map(url => `<img src="${url}" style="width:100%;display:block;" />`)
    .join('');
  
  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
${imagesHtml}
</body>
</html>`;
}

async function createChartletDraft(
  token: string,
  article: {
    title: string;
    author: string;
    content: string;
  },
): Promise<{ media_id: string }> {
  const url = `${WECHAT_API_BASE}/cgi-bin/draft/add?access_token=${token}`;

  // For chartlet, we use the same draft API but with image-based content
  // The content_source_url is required but can be empty
  const body = {
    articles: [
      {
        title: article.title,
        author: article.author,
        digest: '',
        content: article.content,
        content_source_url: '',
        thumb_media_id: '', // Chartlet doesn't need cover
        need_open_comment: 0,
        only_fans_can_comment: 0,
      },
    ],
  };

  const res = await fetchWithRetry(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    ...BUN_FETCH_OPTS,
  });

  if (!res.ok) throw new Error(`draft/add failed: HTTP ${res.status}`);

  const data = await res.json() as { media_id?: string; errcode?: number; errmsg?: string };
  if (data.errcode && data.errcode !== 0) {
    throw new Error(`draft/add error ${data.errcode}: ${data.errmsg}`);
  }
  if (!data.media_id) throw new Error('draft/add: no media_id returned');

  return { media_id: data.media_id };
}
