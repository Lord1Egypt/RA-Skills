import { createHash } from 'node:crypto';
import { load } from 'cheerio';
import { chromium, type Page } from 'playwright';
import { buildCardDocument } from './template.js';
import type {
  OverflowCheck,
  PageDiagnostics,
  PaginationResult,
  SplitBoundary,
  SplitMode,
  ThemeSpec
} from './types.js';

interface AutoPaginateOptions {
  width: number;
  height: number;
  showPager: boolean;
  maxPages: number;
  title?: string;
  mainTitle?: string;
}

interface FitsContext {
  pageIndex: number;
  blockIndex: number;
  candidateBlockCount: number;
}

interface OversizedSplitResult {
  chunks: string[];
  usedRangeSplit: boolean;
  fallbackCount: number;
}

function hashText(input: string): string {
  return createHash('sha1').update(input).digest('hex').slice(0, 12);
}

function ensureMarkdownBody(html: string): string {
  if (/class=(["'])[^"']*\bmarkdown-body\b[^"']*\1/i.test(html)) {
    return html;
  }
  return `<div class="markdown-body">${html}</div>`;
}

function extractBlocks(html: string): string[] {
  const wrapped = ensureMarkdownBody(html);
  const $ = load(wrapped);
  const root = $('.markdown-body').first();
  const blocks: string[] = [];

  root.contents().each((_, node) => {
    const serialized = $.html(node)?.trim();
    if (serialized) {
      blocks.push(serialized);
    }
  });

  return blocks.length > 0 ? blocks : ['<p><br></p>'];
}

function wrapBlocks(blocks: string[]): string {
  const body = blocks.join('\n');
  return `<div class="markdown-body">${body || '<p><br></p>'}</div>`;
}

function splitByHr(html: string): string[] {
  const wrapped = ensureMarkdownBody(html);
  const $ = load(wrapped);
  const root = $('.markdown-body').first();
  const parts = (root.html() ?? '')
    .split(/<hr\s*\/?\s*>/gi)
    .map((part) => part.trim())
    .map((part) => (part.length > 0 ? `<div class="markdown-body">${part}</div>` : '<div class="markdown-body"><p><br></p></div>'));

  return parts.length > 0 ? parts : ['<div class="markdown-body"><p><br></p></div>'];
}

async function checkOverflow(page: Page, html: string): Promise<boolean> {
  await page.setContent(html, { waitUntil: 'load' });
  await page.waitForTimeout(8);

  const result = (await page.evaluate(`
    (() => {
      const card = document.querySelector('.card');
      if (!card) {
        return { overflow: false };
      }

      const cardRect = card.getBoundingClientRect();
      const footer = document.querySelector('.card-footer');
      const footerTop = footer ? footer.getBoundingClientRect().top : cardRect.bottom;
      const content = document.querySelector('.card-content') || card;
      const contentRect = content.getBoundingClientRect();

      if (footer) {
        const footerRect = footer.getBoundingClientRect();
        if (footerRect.bottom > cardRect.bottom + 0.5) {
          return { overflow: true };
        }
      }

      let maxBottom = contentRect.top;
      const measurable = content.querySelectorAll('*');
      for (const element of measurable) {
        const style = window.getComputedStyle(element);
        if (style.position === 'absolute' || style.position === 'fixed') {
          continue;
        }
        if (element.children.length > 0) {
          continue;
        }
        const text = element.textContent ? element.textContent.trim() : '';
        if (!text) {
          continue;
        }
        const rect = element.getBoundingClientRect();
        if (rect.height <= 0) {
          continue;
        }
        if (rect.bottom > maxBottom) {
          maxBottom = rect.bottom;
        }
      }

      return { overflow: maxBottom > footerTop + 0.5 };
    })();
  `)) as { overflow?: boolean };

  return Boolean(result.overflow);
}

function buildAnomalyDiagnostics(
  reason: string,
  blocks: string[],
  generatedPages: number,
  maxPages: number
): PageDiagnostics {
  return {
    reason,
    blockCount: blocks.length,
    generatedPages,
    maxPages,
    sampledBlockLengths: blocks.slice(0, 12).map((block) => load(`<div>${block}</div>`)('div').text().trim().length),
    sampledCandidates: blocks.slice(0, 6).map((block, index) => ({
      blockIndex: index,
      hash: hashText(block),
      preview: block.replace(/\s+/g, ' ').slice(0, 120)
    }))
  };
}

async function splitBlockAtChar(
  page: Page,
  blockHtml: string,
  charIndex: number
): Promise<{ left: string; right: string; totalChars: number } | null> {
  return page.evaluate(
    ({ rawBlockHtml, splitIndex }) => {
      const host = document.createElement('div');
      host.innerHTML = rawBlockHtml;
      const target = host.firstChild;
      if (!target) {
        return null;
      }

      const doc = document;
      const textNodes: Text[] = [];
      const walker = doc.createTreeWalker(target, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode as Text;
        if (node.nodeValue && node.nodeValue.length > 0) {
          textNodes.push(node);
        }
      }

      if (textNodes.length === 0) {
        return null;
      }

      const totalChars = textNodes.reduce((sum, node) => sum + (node.nodeValue?.length ?? 0), 0);
      if (splitIndex <= 0 || splitIndex >= totalChars) {
        return null;
      }

      let traversed = 0;
      let splitNode: Text | null = null;
      let splitOffset = 0;
      for (const node of textNodes) {
        const next = traversed + (node.nodeValue?.length ?? 0);
        if (splitIndex <= next) {
          splitNode = node;
          splitOffset = splitIndex - traversed;
          break;
        }
        traversed = next;
      }

      if (!splitNode) {
        return null;
      }

      const firstText = textNodes[0];
      const lastText = textNodes[textNodes.length - 1];

      const leftRange = doc.createRange();
      leftRange.setStart(firstText, 0);
      leftRange.setEnd(splitNode, splitOffset);

      const rightRange = doc.createRange();
      rightRange.setStart(splitNode, splitOffset);
      rightRange.setEnd(lastText, lastText.nodeValue?.length ?? 0);

      const leftFragment = leftRange.cloneContents();
      const rightFragment = rightRange.cloneContents();

      if (target.nodeType === Node.TEXT_NODE) {
        const leftText = leftFragment.textContent ?? '';
        const rightText = rightFragment.textContent ?? '';
        const escape = (value: string) =>
          value
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;');

        return {
          left: `<p>${escape(leftText)}</p>`,
          right: `<p>${escape(rightText)}</p>`,
          totalChars
        };
      }

      const element = target as Element;
      const leftEl = element.cloneNode(false) as Element;
      const rightEl = element.cloneNode(false) as Element;
      leftEl.append(leftFragment);
      rightEl.append(rightFragment);

      if (!leftEl.textContent?.trim() || !rightEl.textContent?.trim()) {
        return null;
      }

      return {
        left: leftEl.outerHTML,
        right: rightEl.outerHTML,
        totalChars
      };
    },
    { rawBlockHtml: blockHtml, splitIndex: charIndex }
  );
}

async function getBlockTextLength(page: Page, blockHtml: string): Promise<number> {
  const length = await page.evaluate((rawBlockHtml) => {
    const host = document.createElement('div');
    host.innerHTML = rawBlockHtml;
    return host.textContent?.length ?? 0;
  }, blockHtml);

  return length;
}

async function splitOversizedBlock(
  page: Page,
  blockHtml: string,
  fits: (blocks: string[], context: FitsContext) => Promise<boolean>,
  pageIndex: number,
  blockIndex: number
): Promise<OversizedSplitResult> {
  const chunks: string[] = [];
  let remaining = blockHtml;
  let fallbackCount = 0;
  let usedRangeSplit = false;
  let guard = 0;

  while (guard < 64) {
    guard += 1;
    // eslint-disable-next-line no-await-in-loop
    if (await fits([remaining], { pageIndex, blockIndex, candidateBlockCount: 1 })) {
      chunks.push(remaining);
      break;
    }

    // eslint-disable-next-line no-await-in-loop
    const textLength = await getBlockTextLength(page, remaining);
    if (textLength <= 1) {
      fallbackCount += 1;
      chunks.push(remaining);
      break;
    }

    let low = 1;
    let high = textLength - 1;
    let best: { left: string; right: string } | null = null;

    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      // eslint-disable-next-line no-await-in-loop
      const split = await splitBlockAtChar(page, remaining, mid);
      if (!split) {
        high = mid - 1;
        continue;
      }

      // eslint-disable-next-line no-await-in-loop
      const leftFits = await fits([split.left], {
        pageIndex,
        blockIndex,
        candidateBlockCount: 1
      });

      if (leftFits) {
        best = { left: split.left, right: split.right };
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }

    if (!best || best.left.trim() === remaining.trim() || best.right.trim().length === 0) {
      fallbackCount += 1;
      chunks.push(remaining);
      break;
    }

    usedRangeSplit = true;
    chunks.push(best.left);
    remaining = best.right;
  }

  if (chunks.length === 0) {
    chunks.push(blockHtml);
    fallbackCount += 1;
  }

  return {
    chunks,
    usedRangeSplit,
    fallbackCount
  };
}

export async function paginateAuto(theme: ThemeSpec, html: string, options: AutoPaginateOptions): Promise<PaginationResult> {
  const blocks = extractBlocks(html);
  const splitBoundaries: SplitBoundary[] = [];
  const overflowChecks: OverflowCheck[] = [];

  let fallbackCount = 0;

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: options.width, height: options.height * 2 },
    deviceScaleFactor: 1
  });

  const fits = async (candidateBlocks: string[], context: FitsContext): Promise<boolean> => {
    const documentHtml = buildCardDocument({
      theme,
      contentHtml: wrapBlocks(candidateBlocks),
      width: options.width,
      height: options.height,
      pageNum: '88 / 88',
      showPager: options.showPager,
      title: options.title,
      mainTitle: options.mainTitle
    });

    const overflow = await checkOverflow(page, documentHtml);
    overflowChecks.push({
      pageIndex: context.pageIndex,
      blockIndex: context.blockIndex,
      candidateBlockCount: context.candidateBlockCount,
      overflow
    });
    return !overflow;
  };

  const pages: string[] = [];
  let current: string[] = [];
  let pageStartBlock = 0;
  let currentHasRangeSplit = false;

  try {
    for (let index = 0; index < blocks.length; index += 1) {
      const block = blocks[index];
      const candidate = [...current, block];

      // eslint-disable-next-line no-await-in-loop
      if (await fits(candidate, { pageIndex: pages.length, blockIndex: index, candidateBlockCount: candidate.length })) {
        current = candidate;
        continue;
      }

      if (current.length > 0) {
        pages.push(wrapBlocks(current));
        splitBoundaries.push({
          pageIndex: pages.length - 1,
          startBlock: pageStartBlock,
          endBlock: index - 1,
          mode: currentHasRangeSplit ? 'range' : 'block'
        });
        current = [];
        currentHasRangeSplit = false;
      }

      if (pages.length > options.maxPages) {
        return {
          pages,
          splitBoundaries,
          overflowChecks,
          fallbackCount,
          diagnostics: buildAnomalyDiagnostics('page_count_exceeded', blocks, pages.length, options.maxPages)
        };
      }

      // eslint-disable-next-line no-await-in-loop
      if (await fits([block], { pageIndex: pages.length, blockIndex: index, candidateBlockCount: 1 })) {
        current = [block];
        pageStartBlock = index;
        continue;
      }

      // eslint-disable-next-line no-await-in-loop
      const splitResult = await splitOversizedBlock(page, block, fits, pages.length, index);
      fallbackCount += splitResult.fallbackCount;

      for (const chunk of splitResult.chunks) {
        const nextCandidate = [...current, chunk];
        // eslint-disable-next-line no-await-in-loop
        const canFit = await fits(nextCandidate, {
          pageIndex: pages.length,
          blockIndex: index,
          candidateBlockCount: nextCandidate.length
        });

        if (!canFit && current.length > 0) {
          pages.push(wrapBlocks(current));
          splitBoundaries.push({
            pageIndex: pages.length - 1,
            startBlock: pageStartBlock,
            endBlock: index,
            mode: currentHasRangeSplit ? 'range' : 'block'
          });
          current = [chunk];
          pageStartBlock = index;
          currentHasRangeSplit = splitResult.usedRangeSplit;
        } else {
          if (current.length === 0) {
            pageStartBlock = index;
          }
          current.push(chunk);
          currentHasRangeSplit = currentHasRangeSplit || splitResult.usedRangeSplit;
        }

        if (pages.length > options.maxPages) {
          return {
            pages,
            splitBoundaries,
            overflowChecks,
            fallbackCount,
            diagnostics: buildAnomalyDiagnostics('page_count_exceeded', blocks, pages.length, options.maxPages)
          };
        }
      }
    }

    if (current.length > 0) {
      pages.push(wrapBlocks(current));
      splitBoundaries.push({
        pageIndex: pages.length - 1,
        startBlock: pageStartBlock,
        endBlock: blocks.length - 1,
        mode: currentHasRangeSplit ? 'range' : 'block'
      });
    }
  } finally {
    await browser.close();
  }

  if (pages.length === 0) {
    pages.push('<div class="markdown-body"><p><br></p></div>');
    splitBoundaries.push({
      pageIndex: 0,
      startBlock: 0,
      endBlock: 0,
      mode: 'block'
    });
  }

  if (pages.length > options.maxPages) {
    return {
      pages,
      splitBoundaries,
      overflowChecks,
      fallbackCount,
      diagnostics: buildAnomalyDiagnostics('page_count_exceeded', blocks, pages.length, options.maxPages)
    };
  }

  return {
    pages,
    splitBoundaries,
    overflowChecks,
    fallbackCount
  };
}

export async function splitHtmlByMode(
  theme: ThemeSpec,
  html: string,
  mode: SplitMode,
  options: AutoPaginateOptions
): Promise<PaginationResult> {
  if (mode === 'none') {
    return {
      pages: [ensureMarkdownBody(html || '<p><br></p>')],
      splitBoundaries: [{ pageIndex: 0, startBlock: 0, endBlock: 0, mode: 'none' }],
      overflowChecks: [],
      fallbackCount: 0
    };
  }

  if (mode === 'hr') {
    const pages = splitByHr(html);
    return {
      pages,
      splitBoundaries: pages.map((_, index) => ({
        pageIndex: index,
        startBlock: index,
        endBlock: index,
        mode: 'hr'
      })),
      overflowChecks: [],
      fallbackCount: 0
    };
  }

  return paginateAuto(theme, html, options);
}
