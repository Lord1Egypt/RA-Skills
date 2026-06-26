import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { chromium } from 'playwright';
import { buildCardDocument } from './template.js';
import type { RenderResult, ThemeSpec } from './types.js';

interface ExportPagesArgs {
  pages: string[];
  theme: ThemeSpec;
  width: number;
  height: number;
  scale: number;
  showPager: boolean;
  outputDir: string;
  title?: string;
  mainTitle?: string;
}

export async function exportPagesToPng(args: ExportPagesArgs): Promise<RenderResult[]> {
  mkdirSync(args.outputDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: args.width, height: args.height },
    deviceScaleFactor: args.scale
  });

  const total = args.pages.length;
  const results: RenderResult[] = [];

  try {
    for (let index = 0; index < total; index += 1) {
      const pageNumber = index + 1;
      const documentHtml = buildCardDocument({
        theme: args.theme,
        contentHtml: args.pages[index],
        width: args.width,
        height: args.height,
        pageNum: `${pageNumber} / ${total}`,
        showPager: args.showPager,
        title: index === 0 ? args.title : undefined,
        mainTitle: index === 0 ? args.mainTitle : undefined
      });

      const outputPath = resolve(args.outputDir, `card_${pageNumber}.png`);
      await page.setContent(documentHtml, { waitUntil: 'load' });
      await page.waitForTimeout(30);
      await page.screenshot({
        path: outputPath,
        type: 'png',
        clip: { x: 0, y: 0, width: args.width, height: args.height },
        animations: 'disabled'
      });

      results.push({
        index: pageNumber,
        imagePath: outputPath,
        success: true
      });
    }
  } finally {
    await browser.close();
  }

  return results;
}

export async function doctorPlaywright(): Promise<{ ok: boolean; message: string }> {
  try {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 200, height: 100 } });
    await page.setContent('<html><body><div>ok</div></body></html>', { waitUntil: 'load' });
    await browser.close();
    return { ok: true, message: 'Playwright Chromium is ready.' };
  } catch (error) {
    return {
      ok: false,
      message: `Playwright Chromium unavailable: ${error instanceof Error ? error.message : String(error)}`
    };
  }
}

export function ensureOutputDir(pathValue: string): string {
  const outputDir = resolve(pathValue);
  mkdirSync(outputDir, { recursive: true });
  return outputDir;
}

export function ensureParentDir(pathValue: string): void {
  mkdirSync(dirname(pathValue), { recursive: true });
}
