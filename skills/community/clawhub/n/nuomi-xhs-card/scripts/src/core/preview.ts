import { load } from 'cheerio';
import { markdownToHtml } from './markdown.js';
import { restructureMarkdownHtml } from './structure.js';
import type { PreviewMetaData, PreviewPayload, PreviewResult } from './types.js';

function extractPreviewMetaData(structuredHtml: string): PreviewMetaData {
  const $ = load(structuredHtml);
  const root = $('.markdown-body').first();

  const title = root.find('h1,h2,h3').first().text().trim();
  const description = root.find('p').first().text().trim();

  return {
    title: title || undefined,
    description: description || undefined
  };
}

function extractTitleIntoTemplate(structuredHtml: string): { html: string; metaData: PreviewMetaData } {
  const $ = load(structuredHtml);
  const root = $('.markdown-body').first();
  const firstHeading = root.children('h1,h2,h3').first();

  let title: string | undefined;
  if (firstHeading.length > 0) {
    title = firstHeading.text().trim() || undefined;
    firstHeading.remove();
  }

  const description = root.find('p').first().text().trim() || undefined;

  return {
    html: $.html(root) || '<div class="markdown-body"><p><br></p></div>',
    metaData: {
      title,
      description
    }
  };
}

export async function generateCardPreview(payload: PreviewPayload): Promise<PreviewResult> {
  const markdownResult = await markdownToHtml(payload.markdown, { mdxMode: payload.mdxMode });
  const structuredResult = await restructureMarkdownHtml(markdownResult.html, {
    editorMode: false,
    processRemoteImages: payload.weChatMode
  });

  const titleExtracted = extractTitleIntoTemplate(structuredResult.html);
  const warnings = [...markdownResult.warnings, ...structuredResult.warnings];
  const metaData = {
    ...extractPreviewMetaData(titleExtracted.html),
    ...titleExtracted.metaData
  };

  return {
    success: true,
    html: titleExtracted.html,
    rawHtml: markdownResult.html,
    structuredHtml: titleExtracted.html,
    preloads: structuredResult.preloads,
    metaData,
    warnings,
    diagnostics: {
      markdownLength: payload.markdown.length,
      htmlLength: markdownResult.html.length,
      structuredHtmlLength: titleExtracted.html.length
    }
  };
}
