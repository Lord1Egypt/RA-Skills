import type { ConfigCategory } from './types.js';

// WHY: Regexes anchor on path separators, leading dots, quotes, or start-of-string
// to avoid substring false positives (e.g. "application/json" should not match).
export const CONFIG_PATTERNS: readonly { regex: RegExp; category: ConfigCategory }[] = [
  { regex: /(?:^|[/'"`\s])\.env(?:\.[a-zA-Z0-9_]+)?(?=[/'"`\s,;)\]}]|$)/,       category: 'dotenv' },
  { regex: /(?:^|[/'"`\s])[\w.\-]+\.ya?ml(?=[/'"`\s,;)\]}]|$)/,                  category: 'yaml' },
  { regex: /(?:^|[/'"`\s])[\w.\-]+\.json(?=[/'"`\s,;)\]}]|$)/,                    category: 'json' },
  { regex: /(?:^|[/'"`\s])[\w.\-]+\.ini(?=[/'"`\s,;)\]}]|$)/,                     category: 'ini' },
  { regex: /(?:^|[/'"`\s])[\w.\-]+\.cfg(?=[/'"`\s,;)\]}]|$)/,                     category: 'ini' },
  { regex: /(?:^|[/'"`\s])[\w.\-]+\.toml(?=[/'"`\s,;)\]}]|$)/,                    category: 'toml' },
  { regex: /(?:^|[/'"`\s])\.[\w\-]*rc(?=[/'"`\s,;)\]}]|$)/,                       category: 'rc-files' },
];
