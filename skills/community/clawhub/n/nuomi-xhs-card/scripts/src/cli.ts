#!/usr/bin/env node
import { Command } from 'commander';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { performance } from 'node:perf_hooks';
import { splitHtmlByMode } from './core/paginate.js';
import { generateCardPreview } from './core/preview.js';
import { doctorPlaywright, ensureOutputDir, ensureParentDir, exportPagesToPng } from './core/render.js';
import { EXPECTED_THEME_IDS, ensureThemeIntegrity, listThemes, loadThemes, resolveTheme, validateTemplateSet } from './core/themes.js';
import type { SplitMode, ThemeMode } from './core/types.js';

interface RenderCommandOptions {
  theme: string;
  mode: ThemeMode;
  split: SplitMode;
  size: string;
  scale: string;
  pager: boolean;
  output: string;
  maxPages: string;
  mdxMode: boolean;
  wechatMode: boolean;
  overHiddenMode: boolean;
  report?: string;
  dumpPreviewHtml?: string;
  dumpStructuredHtml?: string;
  dumpPaginationJson?: string;
}

function parseSize(input: string): { width: number; height: number } {
  const match = input.match(/^(\d+)x(\d+)$/);
  if (!match) {
    throw new Error(`Invalid size: ${input}. Use WIDTHxHEIGHT, e.g. 440x586`);
  }

  return {
    width: Number.parseInt(match[1], 10),
    height: Number.parseInt(match[2], 10)
  };
}

function parseScale(input: string): number {
  const value = Number.parseFloat(input);
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error(`Invalid scale: ${input}`);
  }
  return value;
}

function parseMaxPages(input: string): number {
  const value = Number.parseInt(input, 10);
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error(`Invalid max-pages: ${input}`);
  }
  return value;
}

function writeOptionalFile(pathValue: string | undefined, content: string): void {
  if (!pathValue) {
    return;
  }
  const target = resolve(pathValue);
  ensureParentDir(target);
  writeFileSync(target, content, 'utf-8');
}

async function runRender(markdownPath: string, options: RenderCommandOptions): Promise<void> {
  const start = performance.now();

  ensureThemeIntegrity();
  const themes = loadThemes();
  const themeResolution = resolveTheme(themes, options.theme, options.mode);

  const markdown = readFileSync(resolve(markdownPath), 'utf-8');
  const { width, height } = parseSize(options.size);
  const scale = parseScale(options.scale);
  const maxPages = parseMaxPages(options.maxPages);

  const previewResult = await generateCardPreview({
    markdown,
    theme: themeResolution.theme.id,
    width,
    height,
    mdxMode: options.mdxMode,
    splitMode: options.split,
    weChatMode: options.wechatMode,
    themeMode: themeResolution.appliedMode,
    showPager: options.pager,
    overHiddenMode: options.overHiddenMode
  });

  writeOptionalFile(options.dumpPreviewHtml, `${previewResult.rawHtml}\n`);
  writeOptionalFile(options.dumpStructuredHtml, `${previewResult.structuredHtml}\n`);

  const paginateResult = await splitHtmlByMode(themeResolution.theme, previewResult.html, options.split, {
    width,
    height,
    showPager: options.pager,
    maxPages,
    title: previewResult.metaData.title
  });

  if (options.dumpPaginationJson) {
    writeOptionalFile(
      options.dumpPaginationJson,
      `${JSON.stringify(
        {
          splitBoundaries: paginateResult.splitBoundaries,
          overflowChecks: paginateResult.overflowChecks,
          fallbackCount: paginateResult.fallbackCount,
          diagnostics: paginateResult.diagnostics
        },
        null,
        2
      )}\n`
    );
  }

  if (paginateResult.diagnostics) {
    const errorPayload = {
      status: 'error',
      message: 'Pagination anomaly detected. Aborting render.',
      diagnostics: paginateResult.diagnostics,
      splitBoundaries: paginateResult.splitBoundaries,
      overflowChecks: paginateResult.overflowChecks.slice(0, 40),
      fallbackCount: paginateResult.fallbackCount,
      warnings: [...themeResolution.warnings, ...previewResult.warnings],
      theme: themeResolution.theme.id,
      mode: themeResolution.appliedMode,
      split: options.split
    };
    console.log(JSON.stringify(errorPayload, null, 2));
    process.exitCode = 1;
    return;
  }

  const outputDir = ensureOutputDir(options.output);
  const images = await exportPagesToPng({
    pages: paginateResult.pages,
    theme: themeResolution.theme,
    width,
    height,
    scale,
    showPager: options.pager,
    outputDir,
    title: previewResult.metaData.title
  });

  const elapsedMs = Math.round(performance.now() - start);
  const report = {
    status: 'success',
    theme: themeResolution.theme.id,
    themeName: themeResolution.theme.name,
    mode: themeResolution.appliedMode,
    split: options.split,
    width,
    height,
    scale,
    pager: options.pager,
    totalPages: paginateResult.pages.length,
    warnings: previewResult.warnings,
    themeFallbackWarnings: themeResolution.warnings,
    elapsedMs,
    cards: images,
    outputDir,
    metaData: previewResult.metaData,
    preview: {
      diagnostics: previewResult.diagnostics,
      preloads: previewResult.preloads.length
    },
    splitBoundaries: paginateResult.splitBoundaries,
    overflowChecks: paginateResult.overflowChecks,
    fallbackCount: paginateResult.fallbackCount
  };

  const reportPath = resolve(options.report ?? `${outputDir}/render-report.json`);
  ensureParentDir(reportPath);
  writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, 'utf-8');

  console.log(JSON.stringify({ ...report, reportPath }, null, 2));
}

async function runDoctor(): Promise<void> {
  const templateValidation = validateTemplateSet();
  const playwrightStatus = await doctorPlaywright();

  const payload = {
    status: templateValidation.ok && playwrightStatus.ok ? 'ok' : 'error',
    checks: {
      templateSet: {
        ok: templateValidation.ok,
        expectedCount: EXPECTED_THEME_IDS.length,
        missing: templateValidation.missing,
        extra: templateValidation.extra
      },
      playwright: playwrightStatus
    }
  };

  console.log(JSON.stringify(payload, null, 2));
  if (payload.status !== 'ok') {
    process.exitCode = 1;
  }
}

async function main(): Promise<void> {
  const program = new Command();
  program.name('xhs-card').description('Node + React local md2card-aligned renderer').version('1.0.0');

  program
    .command('render')
    .argument('<input.md>', 'Markdown file path')
    .option('--theme <id>', 'Theme id', 'xiaohongshu')
    .option('--mode <light|dark>', 'Theme mode', 'light')
    .option('--split <auto|hr|none>', 'Split mode', 'auto')
    .option('--size <widthxheight>', 'Card size', '440x586')
    .option('--scale <number>', 'Pixel ratio / export scale', '4')
    .option('--pager', 'Show pager', true)
    .option('--no-pager', 'Hide pager')
    .option('--mdx-mode', 'Enable mdx mode', false)
    .option('--wechat-mode', 'Enable wechat mode', false)
    .option('--over-hidden-mode', 'Enable overHidden compatibility mode', false)
    .option('--output <dir>', 'Output directory', './output')
    .option('--max-pages <n>', 'Pagination hard limit', '80')
    .option('--report <path>', 'Optional report JSON path')
    .option('--dump-preview-html <path>', 'Dump raw markdown-rendered HTML')
    .option('--dump-structured-html <path>', 'Dump structured HTML after post-process')
    .option('--dump-pagination-json <path>', 'Dump pagination diagnostics JSON')
    .action(async (input: string, options: RenderCommandOptions) => {
      await runRender(input, options);
    });

  const templatesCommand = program.command('templates').description('Theme commands');
  templatesCommand.command('list').description('List built-in templates').action(() => {
    ensureThemeIntegrity();
    const themes = loadThemes();
    console.log(JSON.stringify(listThemes(themes), null, 2));
  });

  program.command('doctor').description('Environment and integrity checks').action(async () => {
    await runDoctor();
  });

  await program.parseAsync(process.argv);
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(message);
  process.exit(1);
});
