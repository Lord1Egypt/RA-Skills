import { readFileSync, readdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { ThemeMode, ThemeResolution, ThemeSpec } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const PROJECT_ROOT = resolve(__dirname, '..', '..', '..');
export const TEMPLATES_DIR = resolve(PROJECT_ROOT, 'assets', 'templates');

export const EXPECTED_THEME_IDS: string[] = [
  'alibaba',
  'apple-notes',
  'art-deco',
  'business',
  'bytedance',
  'coil-notebook',
  'cyberpunk',
  'darktech',
  'dreamy',
  'fairytale',
  'glassmorphism',
  'instagram',
  'japanese-magazine',
  'meadow-dawn',
  'minimal',
  'minimalist',
  'nature',
  'notebook',
  'pop-art',
  'traditional-chinese',
  'typewriter',
  'warm',
  'watercolor',
  'xiaohongshu'
];

const THEME_NAMES: Record<string, string> = {
  'apple-notes': '苹果备忘录',
  xiaohongshu: '小红书紫',
  instagram: 'Instagram风格',
  minimalist: '极简黑白',
  minimal: '简约高级灰',
  notebook: '笔记本',
  business: '商务简报',
  dreamy: '梦幻渐变',
  warm: '温暖柔和',
  nature: '清新自然',
  'meadow-dawn': '青野晨光',
  watercolor: '水彩艺术',
  darktech: '暗黑科技',
  cyberpunk: '赛博朋克',
  glassmorphism: '玻璃拟态',
  'art-deco': '艺术装饰',
  'pop-art': '波普艺术',
  'japanese-magazine': '日本杂志',
  'traditional-chinese': '中国传统',
  fairytale: '儿童童话',
  typewriter: '复古打字机',
  'coil-notebook': '线圈笔记本',
  bytedance: '字节范',
  alibaba: '阿里橙'
};

export interface ThemeValidationResult {
  ok: boolean;
  missing: string[];
  extra: string[];
}

function extractCss(raw: string): string {
  const match = raw.match(/<style>([\s\S]*?)<\/style>/i);
  return match ? match[1].trim() : '';
}

function extractBody(raw: string): string {
  const match = raw.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  return match ? match[1].trim() : raw;
}

function detectModes(raw: string): ThemeMode[] {
  return /dark-mode/.test(raw) ? ['light', 'dark'] : ['light'];
}

export function validateTemplateSet(): ThemeValidationResult {
  const localIds = readdirSync(TEMPLATES_DIR)
    .filter((name) => name.endsWith('.html'))
    .map((name) => name.replace(/\.html$/, ''))
    .sort();

  const expected = [...EXPECTED_THEME_IDS].sort();
  const localSet = new Set(localIds);
  const expectedSet = new Set(expected);

  const missing = expected.filter((id) => !localSet.has(id));
  const extra = localIds.filter((id) => !expectedSet.has(id));

  return {
    ok: missing.length === 0 && extra.length === 0,
    missing,
    extra
  };
}

export function ensureThemeIntegrity(): void {
  const result = validateTemplateSet();
  if (!result.ok) {
    throw new Error(
      JSON.stringify(
        {
          message: 'Template set mismatch. Must exactly match 24 built-in themes.',
          missing: result.missing,
          extra: result.extra
        },
        null,
        2
      )
    );
  }
}

export function loadThemes(): Map<string, ThemeSpec> {
  ensureThemeIntegrity();

  const themes = new Map<string, ThemeSpec>();

  for (const id of EXPECTED_THEME_IDS) {
    const filePath = resolve(TEMPLATES_DIR, `${id}.html`);
    const raw = readFileSync(filePath, 'utf-8');

    themes.set(id, {
      id,
      name: THEME_NAMES[id] ?? id,
      className: id,
      modes: detectModes(raw),
      css: extractCss(raw),
      bodyTemplate: extractBody(raw),
      rawTemplate: raw
    });
  }

  return themes;
}

function applyModeClass(bodyTemplate: string, modeClass: string): string {
  const pattern = /(<[^>]+class="[^"]*\bcard\b[^"]*)(")/i;
  return bodyTemplate.replace(pattern, (full, prefix, quote) => {
    if (prefix.includes(modeClass)) {
      return full;
    }
    return `${prefix} ${modeClass}${quote}`;
  });
}

export function resolveTheme(themes: Map<string, ThemeSpec>, themeId: string, requestedMode: ThemeMode): ThemeResolution {
  const theme = themes.get(themeId);
  if (!theme) {
    throw new Error(`Unknown theme: ${themeId}`);
  }

  const warnings: string[] = [];
  let appliedMode: ThemeMode = requestedMode;

  if (!theme.modes.includes(requestedMode)) {
    appliedMode = 'light';
    warnings.push(`Theme ${themeId} does not support ${requestedMode}; fallback to light.`);
  }

  const modeClass = appliedMode === 'dark' ? 'dark-mode' : 'light-mode';
  const modeAppliedTheme: ThemeSpec = {
    ...theme,
    bodyTemplate: applyModeClass(theme.bodyTemplate, modeClass)
  };

  return { theme: modeAppliedTheme, appliedMode, warnings };
}

export function listThemes(themes: Map<string, ThemeSpec>): Array<{ id: string; name: string; modes: ThemeMode[] }> {
  return [...themes.values()].map((theme) => ({ id: theme.id, name: theme.name, modes: theme.modes }));
}
