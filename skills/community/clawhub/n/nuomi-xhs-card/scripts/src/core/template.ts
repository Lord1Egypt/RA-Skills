import { renderBrowserPage } from '../browser/page.js';
import type { ThemeSpec } from './types.js';

const BASE_STYLE = `
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { overflow: hidden; }
img { max-width: 100%; height: auto; }
.text {
  white-space: normal;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.text > .markdown-body {
  color: inherit;
  font: inherit;
  line-height: inherit;
}
.markdown-body {
  color: inherit;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  letter-spacing: inherit;
  font-weight: inherit;
  word-break: break-word;
  white-space: normal;
  overflow-wrap: anywhere;
}
.markdown-body > :first-child { margin-top: 0 !important; }
.markdown-body > :last-child { margin-bottom: 0 !important; }
.markdown-body p,
.markdown-body ul,
.markdown-body ol,
.markdown-body blockquote,
.markdown-body pre,
.markdown-body table,
.markdown-body hr {
  margin: 0.95em 0 0;
}
.markdown-body li + li { margin-top: 0.35em; }
.markdown-body li > ul,
.markdown-body li > ol { margin: 0.45em 0 0; }
.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin: 1.2em 0 0.55em;
  line-height: 1.35;
  font-weight: 700;
}
.markdown-body h1 { font-size: 2em; }
.markdown-body h2 { font-size: 1.55em; }
.markdown-body h3 { font-size: 1.3em; }
.markdown-body h4 { font-size: 1.1em; }
.markdown-body h5 { font-size: 1em; }
.markdown-body h6 { font-size: 0.92em; opacity: 0.8; }
.markdown-body blockquote {
  padding: 0.2em 0 0.2em 1em;
  border-left: 0.25em solid rgba(0, 0, 0, 0.18);
  background: rgba(0, 0, 0, 0.03);
  border-radius: 0.5em;
  opacity: 0.92;
}
.markdown-body hr {
  border: none;
  border-top: 1px solid rgba(0, 0, 0, 0.16);
}
.markdown-body pre {
  white-space: pre-wrap;
  word-break: normal;
  overflow-wrap: normal;
  overflow: auto;
  padding: 0.85em 1em;
  border-radius: 0.7em;
  background: rgba(0, 0, 0, 0.06);
}
.markdown-body code,
.markdown-body pre code {
  font-family: "SFMono-Regular", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
.markdown-body code:not(pre code) {
  padding: 0.12em 0.35em;
  border-radius: 0.35em;
  background: rgba(0, 0, 0, 0.06);
  font-size: 0.92em;
}
.markdown-body strong,
.text .markdown-body strong {
  font-weight: 700;
}
.markdown-body a {
  color: inherit;
  text-decoration: underline;
  text-decoration-thickness: 0.08em;
  text-underline-offset: 0.14em;
}
.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.95em;
}
.markdown-body th,
.markdown-body td {
  border: 1px solid rgba(0, 0, 0, 0.14);
  padding: 0.35em 0.5em;
  vertical-align: top;
}
.markdown-body th { text-align: left; }
.markdown-body ul,
.markdown-body ol { padding-left: 1.5em; }
.markdown-body img {
  display: block;
  margin: 1em auto 0;
  max-width: 100%;
}
`;

function htmlEscape(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function maybeHtml(value: string): string {
  return /<\/?[a-z][\s\S]*>/i.test(value) ? value : htmlEscape(value).replaceAll('\n', '<br>');
}

interface BuildDocumentArgs {
  theme: ThemeSpec;
  contentHtml: string;
  width: number;
  height: number;
  pageNum: string;
  showPager: boolean;
  title?: string;
  mainTitle?: string;
}

export function buildCardDocument(args: BuildDocumentArgs): string {
  const {
    theme,
    contentHtml,
    width,
    height,
    pageNum,
    showPager,
    title = '',
    mainTitle = ''
  } = args;

  const cssText = theme.css
    .replaceAll('{{CARD_WIDTH}}', String(width))
    .replaceAll('{{CARD_HEIGHT}}', String(height));

  const normalizedContent = /class=(["'])[^"']*\bmarkdown-body\b[^"']*\1/i.test(contentHtml)
    ? contentHtml
    : `<div class="markdown-body">${contentHtml}</div>`;

  const bodyHtml = theme.bodyTemplate
    .replaceAll('{{CARD_WIDTH}}', String(width))
    .replaceAll('{{CARD_HEIGHT}}', String(height))
    .replaceAll('{{MAIN_TITLE}}', mainTitle ? `<div class="main-title">${maybeHtml(mainTitle)}</div>` : '')
    .replaceAll('{{TITLE}}', title ? `<div class="title">${maybeHtml(title)}</div>` : '')
    .replaceAll('{{TEXT}}', maybeHtml(normalizedContent))
    .replaceAll('{{PAGE_NUM}}', showPager ? pageNum : '');

  return renderBrowserPage(`${BASE_STYLE}\n${cssText}`, bodyHtml);
}
