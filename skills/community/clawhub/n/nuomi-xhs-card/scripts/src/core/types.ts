export type ThemeMode = 'light' | 'dark';
export type SplitMode = 'auto' | 'hr' | 'none';

export interface FontConfig {
  family?: string;
  weight?: string;
  level?: number;
}

export interface ThemeSpec {
  id: string;
  name: string;
  className: string;
  modes: ThemeMode[];
  css: string;
  bodyTemplate: string;
  rawTemplate: string;
}

export interface ThemeResolution {
  theme: ThemeSpec;
  appliedMode: ThemeMode;
  warnings: string[];
}

export interface PreviewPayload {
  markdown: string;
  theme: string;
  width: number;
  height: number;
  mdxMode: boolean;
  splitMode: SplitMode;
  weChatMode: boolean;
  themeMode: ThemeMode;
  showPager: boolean;
  overHiddenMode: boolean;
  font?: FontConfig;
}

export interface PreviewMetaData {
  title?: string;
  description?: string;
}

export interface PreviewDiagnostics {
  markdownLength: number;
  htmlLength: number;
  structuredHtmlLength: number;
}

export interface PreviewResult {
  success: boolean;
  html: string;
  rawHtml: string;
  structuredHtml: string;
  preloads: string[];
  metaData: PreviewMetaData;
  warnings: string[];
  diagnostics: PreviewDiagnostics;
}

export interface SplitBoundary {
  pageIndex: number;
  startBlock: number;
  endBlock: number;
  mode: 'block' | 'range' | 'hr' | 'none';
}

export interface OverflowCheck {
  pageIndex: number;
  blockIndex: number;
  candidateBlockCount: number;
  overflow: boolean;
}

export interface PageDiagnostics {
  reason: string;
  blockCount: number;
  generatedPages: number;
  maxPages: number;
  sampledBlockLengths: number[];
  sampledCandidates?: Array<{ blockIndex: number; hash: string; preview: string }>;
}

export interface PaginationResult {
  pages: string[];
  splitBoundaries: SplitBoundary[];
  overflowChecks: OverflowCheck[];
  fallbackCount: number;
  diagnostics?: PageDiagnostics;
}

export interface RenderResult {
  imagePath: string;
  success: boolean;
  index: number;
}
