/**
 * Parser — converts natural language test descriptions into structured step objects.
 *
 * Step schema:
 * {
 *   action: 'click' | 'fill' | 'press' | 'navigate' | 'wait' | 'assert' | 'hover' | 'select' | 'check' | 'uncheck' | 'screenshot',
 *   target: string,          // CSS selector, role hint, or element description
 *   value?: string,          // Input value or expected assertion value
 *   key?: string,            // Keyboard key (for press actions)
 *   url?: string,            // Target URL (for navigate)
 *   duration?: number,       // ms (for wait)
 *   options?: object
 * }
 */

const ACTION_PATTERNS = [
  {
    action: 'navigate',
    patterns: [
      /^(?:go to|navigate to|visit|open|load)\s+(https?:\/\/[^\s]+)/i,
      /^(?:go to|navigate to|visit|open|load)\s+(?:the\s+)?([^\s]+(?:\.[^\s]+)+)/i,
      /^(?:go to|navigate to|visit|open|load)\s+(?:the\s+)?([/.][^\s]*|[^\s]+\.[^\s]+)/i
    ],
    extract: (match) => ({ url: match[1] })
  },
  {
    action: 'click',
    patterns: [
      /click\s+(?:the\s+)?(?:button\s+)?(?:with\s+(?:id\s+)?["']?([^"'\s]+)["']?|(?:on\s+)?(.+))/i,
      /^click\s+(?:the\s+)?(.+?)(?:\s+button)?$/i,
      /^(?:tap|press\s+the\s+button)\s+(?:on\s+)?(.+)$/i
    ],
    extract: (match) => ({ target: (match[1] || match[2] || '').trim() })
  },
  {
    action: 'fill',
    patterns: [
      // "fill [in] [the] field with 'value'" — quoted value (standard order)
      /(?:fill|type|enter)\s+(?:in\s+)?(?:the\s+)?(\w+)\s+(?:field\s+)?with\s+['\"]([^'\" ]+)['\"]/i,
      // "fill [in] [the] field with value" — unquoted value (single word)
      /(?:fill|type|enter)\s+(?:in\s+)?(?:the\s+)?(\w+)\s+(?:field\s+)?with\s+(\w+)/i,
      // "enter 'value' in field" — quoted value first
      /(?:fill|type|enter)\s+['\"]([^'\"]+)['\"]\s+in\s+(?:the\s+)?(\w+)/i,
      // "fill field 'value'" — quoted value last
      /(?:fill|type|enter)\s+(\w+)\s+['\"]([^'\" ]+)['\"]/i,
      // "fill field value" — unquoted (simple)
      /(?:fill|type|enter)\s+(\w+)\s+(\w+)(?!\s+in\s+)/i,
    ],
    extract: (match, pi) => {
      const groups = match.slice(1).filter(Boolean);
      // Pattern index 2 = "enter 'value' in field" — groups are [value, field], swap
      if (pi === 2 && groups.length >= 2) {
        return { target: groups[1], value: groups[0] };
      }
      // All other patterns: [field, value]
      if (groups.length >= 2) {
        return { target: groups[0], value: groups[groups.length - 1] };
      }
      return { target: groups[0] || '', value: '' };
    }
  },
  {
    action: 'press',
    patterns: [
      /press\s+(?:the\s+)?(?:key\s+)?(.+?)(?:\s+key)?$/i,
      /hit\s+(?:the\s+)?(?:key\s+)?(.+)$/i
    ],
    extract: (match) => {
      const key = (match[1] || '').trim();
      const KEY_MAP = {
        'enter': 'Enter', 'tab': 'Tab', 'escape': 'Escape', 'esc': 'Escape',
        'space': ' ', 'spacebar': ' ', 'backspace': 'Backspace',
        'arrowup': 'ArrowUp', 'arrowdown': 'ArrowDown',
        'arrowleft': 'ArrowLeft', 'arrowright': 'ArrowRight',
        'up': 'ArrowUp', 'down': 'ArrowDown', 'left': 'ArrowLeft', 'right': 'ArrowRight'
      };
      return { key: KEY_MAP[key.toLowerCase()] || key };
    }
  },
  {
    action: 'wait',
    patterns: [
      /wait\s+(?:for\s+)?(\d+)\s*(?:seconds?|secs?|ms|milliseconds?)/i,
      /wait\s+(?:for\s+)?(?:the\s+)?(.+?)(?:\s+to\s+(?:appear|be\s+(?:visible|ready)))?$/i
    ],
    extract: (match) => {
      const num = parseInt(match[1]);
      if (!isNaN(num)) {
        if (match[0].toLowerCase().includes('second') || match[0].toLowerCase().includes('sec')) {
          return { duration: num * 1000 };
        }
        return { duration: num };
      }
      return { target: match[1].trim() };
    }
  },
  {
    action: 'assert',
    patterns: [
      // "verify title is 'Home'"
      /(?:verify|check|assert|ensure)\s+(?:that\s+)?(?:the\s+)?(?:page\s+)?title\s+(?:is|equals?|contains?)\s+["']([^"']+)["']/i,
      // "verify title is 'Home'"
      /(?:verify|check|assert|ensure)\s+(?:that\s+)?(?:the\s+)?(.+?)\s+(?:is|equals?|contains?|shows?)\s+["']([^"']+)["']/i,
      // "verify title contains text"
      /(?:verify|check|assert|ensure)\s+(?:that\s+)?(?:the\s+)?(.+?)\s+(?:is|should\s+be|equals?)\s+.+/i
    ],
    extract: (match, pi) => {
      // Pattern 0: [value] only (title assertion); Pattern 1: [target, value]; Pattern 2: [target] only
      if (pi === 0) {
        return { target: 'page title', value: (match[1] || '').trim() };
      }
      if (pi === 2) {
        return { target: match[1].trim(), value: '' };
      }
      return { target: match[1].trim(), value: (match[2] || '').trim() };
    }
  },
  {
    action: 'hover',
    patterns: [
      /hover\s+(?:over\s+)?(?:the\s+)?(?:over\s+)?(.+)$/i,
      /mouseover\s+(?:the\s+)?(.+)$/i
    ],
    extract: (match) => ({ target: match[1].trim() })
  },
  {
    action: 'select',
    patterns: [
      /select\s+(?:option\s+)?["']([^"']+)["']\s+(?:from|in)\s+(?:the\s+)?(.+)/i,
      /choose\s+["']([^"']+)["']\s+(?:from|in)\s+(?:the\s+)?(.+)/i
    ],
    extract: (match) => ({ value: match[1], target: match[2].trim() })
  },
  {
    action: 'check',
    patterns: [
      /check\s+(?:the\s+)?(?:checkbox\s+)?(?:with\s+(?:id\s+)?)?(.+)/i,
      /(?:check|tick)\s+(?:the\s+)?(.+?)\s*$/i
    ],
    extract: (match) => ({ target: match[1].trim() })
  },
  {
    action: 'uncheck',
    patterns: [
      /uncheck\s+(?:the\s+)?(.+)$/i
    ],
    extract: (match) => ({ target: match[1].trim() })
  },
  {
    action: 'screenshot',
    patterns: [
      /take\s+(?:a\s+)?screenshot(?:\s+(?:of\s+)?(?:the\s+)?(.+))?$/i,
      /capture\s+(?:the\s+)?(?:page\s+)?screenshot/i
    ],
    extract: (match) => ({ target: match[1] || 'page' })
  }
];

/** Convert a camelCase/PascalCase string to snake_case */
export function toSnakeCase(str) {
  return str
    .replace(/([A-Z])/g, '_$1')
    .replace(/[\s-_]+/g, '_')
    .replace(/^_|_$/g, '')
    .toLowerCase();
}

/** Convert a string to PascalCase */
export function toPascalCase(str) {
  // Handle camelCase by inserting a split before each uppercase letter
  const withBreaks = str.replace(/([a-z])([A-Z])/g, '$1 $2');
  return withBreaks
    .split(/[\s_\-]+/)
    .filter(Boolean)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join('');
}

/** Infer selector type and build selector string from natural language target */
function buildSelector(target) {
  if (!target) return '';

  // data-testid
  if (target.match(/test[_-]?id|data-testid/i)) {
    const match = target.match(/(?:test[_-]?id|data-testid)[=:]["' ]?([^"')\s]+)/i);
    if (match) return `[data-testid="${match[1]}"]`;
  }

  // id
  if (target.match(/\bid\s*[=:]\s*/i) || target.startsWith('#')) {
    const id = target.match(/#?([^\s#.]+)/)?.[1];
    return `#${id}`;
  }

  // class
  if (target.match(/\bclass\b/i) || target.startsWith('.')) {
    const cls = target.match(/\.([^\s.]+)/)?.[1] || target.replace('.', '');
    return `.${cls}`;
  }

  // role-based
  const roleMatch = target.match(/(?:button|link|input|checkbox|radio|menuitem|tab|dialog)/i);
  if (roleMatch) {
    const role = roleMatch[0].toLowerCase();
    const nameMatch = target.match(/(?:named?|called?|labeled?)\s+["']([^"']+)["']/i);
    if (nameMatch) return `${role}[name*="${nameMatch[1]}"]`;
    return role;
  }

  // plain text
  const textMatch = target.match(/["']([^"']+)["']/);
  if (textMatch) return `text="${textMatch[1]}"`;

  // fallback: convert to snake_case for data-testid
  return `[data-testid="${toSnakeCase(target)}"]`;
}

/** Parse natural language into structured steps */

export function parse(input) {
  if (!input || typeof input !== 'string' || !input.trim()) {
    throw new Error('Empty input: please provide a test description');
  }

  const steps = [];
  // Split on commas first, then on periods (outside URLs and quoted strings)
  // Strategy: comma-split, then for each segment split on periods that are NOT inside URLs
  const commaParts = input.split(/,(?:\s*and\s*)?/);
  const rawSteps = [];
  for (const part of commaParts) {
    // For each comma-segment, further split on period if not inside a URL or quoted string
    let segment = '';
    let inQuote = false;
    for (let i = 0; i < part.length; i++) {
      const ch = part[i];
      if (ch === '"' || ch === "'") inQuote = !inQuote;
      if (!inQuote && (ch === '.' || part.slice(i, i + 5).toLowerCase() === ' then') && i + 1 < part.length && (part[i + 1] === ' ' || ch === ' ')) {
        // Period followed by space = end of sentence
        const trimmed = segment.trim();
        if (trimmed) rawSteps.push(trimmed);
        segment = '';
        i++; // skip the period
      } else {
        segment += ch;
      }
    }
    const trimmed = segment.trim();
    if (trimmed) rawSteps.push(trimmed);
  }

  for (const raw of rawSteps) {
    let matched = false;

    for (const { action, patterns, extract } of ACTION_PATTERNS) {
      for (let pi = 0; pi < patterns.length; pi++) {
        const pattern = patterns[pi];
        const match = raw.match(pattern);
        if (match) {
          const extracted = extract(match, pi);
          const step = {
            action,
            target: extracted.target || extracted.selector || '',
            value: extracted.value || '',
            key: extracted.key || '',
            url: extracted.url || '',
            duration: extracted.duration || 0,
            selector: buildSelector(extracted.target || '')
          };
          steps.push(step);
          matched = true;
          break;
        }
      }
      if (matched) break;
    }

    // Fallback: if nothing matched, treat as a comment/warning
    if (!matched) {
      steps.push({
        action: 'comment',
        target: raw,
        value: '',
        selector: ''
      });
    }
  }

  return steps;
}

export class Parser {
  parse = parse;
}

/** Convert step action to Playwright method name */
export function actionToMethod(action) {
  const map = {
    click: 'click',
    fill: 'fill',
    press: 'press',
    navigate: 'goto',
    wait: 'waitForTimeout',
    assert: 'expect',
    hover: 'hover',
    select: 'selectOption',
    check: 'check',
    uncheck: 'uncheck',
    screenshot: 'screenshot'
  };
  return map[action] || action;
}

/** Build Playwright code snippet from a single step */
export function stepToCode(step, indent = '    ') {
  const { action, selector, value, key, duration, url } = step;

  switch (action) {
    case 'navigate':
      return `${indent}await page.goto('${url || step.target || selector}');`;
    case 'click':
      return `${indent}await page.click('${selector || value}');`;
    case 'fill':
      return `${indent}await page.fill('${selector || value}', '${step.value}');`;
    case 'press':
      return `${indent}await page.keyboard.press('${key || value}');`;
    case 'wait':
      return `${indent}await page.waitForTimeout(${duration || 1000});`;
    case 'hover':
      return `${indent}await page.hover('${selector || value}');`;
    case 'select':
      return `${indent}await page.selectOption('${selector || value}', '${value}');`;
    case 'check':
      return `${indent}await page.check('${selector || value}');`;
    case 'uncheck':
      return `${indent}await page.uncheck('${selector || value}');`;
    case 'screenshot':
      return `${indent}await page.screenshot({ path: '${selector || 'screenshot.png'}' });`;
    case 'assert':
      return `${indent}await expect(page).toHaveTitle(/${value}/);`;
    default:
      return `${indent}// TODO: ${selector || value}`;
  }
}
