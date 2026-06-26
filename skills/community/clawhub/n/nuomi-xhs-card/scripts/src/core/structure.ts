import { load } from 'cheerio';

export interface StructureOptions {
  editorMode?: boolean;
  processRemoteImages?: boolean;
}

export interface StructuredHtmlResult {
  html: string;
  preloads: string[];
  warnings: string[];
}

function ensureMarkdownBody(html: string): string {
  if (/class=(["'])[^"']*\bmarkdown-body\b[^"']*\1/i.test(html)) {
    return html;
  }
  return `<div class="markdown-body">${html}</div>`;
}

async function fetchRemoteImageAsDataUrl(url: string): Promise<string> {
  const response = await fetch(url, {
    redirect: 'follow',
    cache: 'force-cache'
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch image: ${response.status}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  const contentType = response.headers.get('content-type') || 'image/png';
  const base64 = Buffer.from(arrayBuffer).toString('base64');
  return `data:${contentType};base64,${base64}`;
}

export async function restructureMarkdownHtml(inputHtml: string, options: StructureOptions = {}): Promise<StructuredHtmlResult> {
  const warnings: string[] = [];
  const wrappedHtml = ensureMarkdownBody(inputHtml);
  const $ = load(wrappedHtml);
  const root = $('.markdown-body').first();

  const preloads: string[] = [];
  root.find('link').each((_, node) => {
    preloads.push($.html(node));
    $(node).remove();
  });

  if (options.editorMode) {
    root.find('h1,h2,h3').each((_, node) => {
      const $heading = $(node);
      const content = $heading.html() ?? '';
      $heading.html(`<span class="prefix"></span><span class="content">${content}</span><span class="suffix"></span>`);
    });
  } else {
    root.find('h1,h2,h3').each((_, node) => {
      const $heading = $(node);
      $heading.attr('data-text', $heading.text().trim());
    });
  }

  root.find('ol').each((_, listNode) => {
    const $list = $(listNode);
    const startValue = Number.parseInt($list.attr('start') ?? '1', 10);
    const start = Number.isFinite(startValue) ? startValue : 1;

    $list.children('li').each((index, liNode) => {
      $(liNode).attr('data-index', String(start + index));
    });
  });

  const imageNodes = root.find('img').toArray();
  for (const imageNode of imageNodes) {
    const $image = $(imageNode);
    const src = $image.attr('src') ?? '';
    if (!src) {
      continue;
    }

    if (src.includes('data:image/svg+xml')) {
      warnings.push('Encountered inline SVG image; kept original data URI for rendering.');
      continue;
    }

    if (options.processRemoteImages && /^https?:\/\//i.test(src)) {
      try {
        const dataUrl = await fetchRemoteImageAsDataUrl(src);
        $image.attr('src', dataUrl);
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        warnings.push(`Remote image fallback to original URL: ${src} (${message})`);
      }
    }
  }

  const innerHtml = root.html() ?? '<p><br></p>';
  return {
    html: `<div class="markdown-body">${innerHtml.replace(/\n/g, '')}</div>`,
    preloads,
    warnings
  };
}
