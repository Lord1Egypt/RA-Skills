/**
 * Locator Extractor — parses HTML and generates robust Playwright selectors.
 *
 * Priority order:
 * 1. data-testid (most reliable, explicit)
 * 2. id (unique per page)
 * 3. role + accessible name (a11y-first)
 * 4. label → for (form associations)
 * 5. CSS class combinations
 * 6. XPath (last resort)
 */

import * as cheerio from 'cheerio';

export class LocatorExtractor {
  /**
   * Extract locators from HTML string.
   * Returns { locators: { name: selector }, elements: [] }
   */
  static extract(html) {
    if (!html || typeof html !== 'string') {
      return { locators: {}, elements: [] };
    }

    const $ = cheerio.load(html, { ignoreWhitespace: true });
    const locators = {};
    const elements = [];

    $('*').each((_, el) => {
      const node = $(el);
      const tag = el.tagName.toLowerCase();
      const attribs = el.attribs || {};

      // Skip script/style tags
      if (['script', 'style', 'noscript', 'meta', 'link'].includes(tag)) return;

      let name = '';
      let selector = '';

      // 1. data-testid (highest priority)
      if (attribs['data-testid']) {
        name = attribs['data-testid'];
        selector = `[data-testid="${name}"]`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 1 });
        return;
      }

      // 2. id
      if (attribs.id) {
        name = attribs.id;
        selector = `#${name}`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 2 });
        return;
      }

      // 3. data-* attributes
      for (const [attr, val] of Object.entries(attribs)) {
        if (attr.startsWith('data-') && attr !== 'data-testid') {
          name = val;
          selector = `[${attr}="${val}"]`;
          locators[val] = selector;
          elements.push({ tag, name, selector, priority: 3 });
          return;
        }
      }

      // 4. label → for association (form inputs)
      if (tag === 'label' && attribs.for) {
        name = attribs.for;
        selector = `#${name}`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 4 });
        return;
      }

      // 5. aria-label
      if (attribs['aria-label']) {
        name = attribs['aria-label'].replace(/\s+/g, '_').toLowerCase();
        selector = `[aria-label="${attribs['aria-label']}"]`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 5 });
        return;
      }

      // 6. role + text for buttons/links
      if (attribs.role && attribs.role !== 'presentation') {
        const text = node.text().trim().substring(0, 30).replace(/\s+/g, '_').toLowerCase();
        name = text || `${attribs.role}_${Object.keys(locators).length}`;
        const textPart = text ? `[name="${text}"]` : '';
        selector = `${tag}[role="${attribs.role}"]${textPart}`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 6 });
        return;
      }

      // 7. Interactive elements with text content
      if (['button', 'a', 'input', 'select', 'textarea'].includes(tag)) {
        const text = node.text().trim().substring(0, 30).replace(/\s+/g, '_').toLowerCase();
        if (text) {
          name = text;
          if (tag === 'input') {
            const type = attribs.type || 'text';
            selector = `input[type="${type}"]`;
          } else {
            selector = `${tag}:text-is("${node.text().trim()}")`;
          }
          locators[name] = selector;
          elements.push({ tag, name, selector, priority: 7 });
          return;
        }

        // placeholder
        if (attribs.placeholder) {
          name = attribs.placeholder.replace(/\s+/g, '_').toLowerCase();
          selector = `[placeholder="${attribs.placeholder}"]`;
          locators[name] = selector;
          elements.push({ tag, name, selector, priority: 8 });
          return;
        }
      }

      // 8. name attribute (for form elements)
      if (attribs.name) {
        name = attribs.name;
        selector = `[name="${name}"]`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 9 });
        return;
      }

      // 9. type attribute for inputs
      if (tag === 'input' && attribs.type) {
        name = `${attribs.type}_input_${Object.keys(locators).length}`;
        selector = `input[type="${attribs.type}"]`;
        locators[name] = selector;
        elements.push({ tag, name, selector, priority: 10 });
      }
    });

    return { locators, elements };
  }

  /**
   * Get the best selector for a given element description.
   */
  static getBestSelector(locators, elementHint) {
    if (!locators || !elementHint) return null;

    const hint = elementHint.toLowerCase().replace(/\s+/g, '_');

    // Exact match
    if (locators[hint]) return locators[hint];

    // Partial match
    for (const [name, selector] of Object.entries(locators)) {
      if (name.includes(hint) || hint.includes(name)) {
        return selector;
      }
    }

    return null;
  }

  /**
   * Generate a Playwright Page Object from locators.
   */
  static toPageObject(locators, pageName) {
    const pascalName = pageName
      .split(/[\s_-]+/)
      .map(w => w.charAt(0).toUpperCase() + w.slice(1))
      .join('');

    const lines = [
      `class ${pascalName}Page {`,
      '  constructor(page) {',
      '    this.page = page;',
      '  }',
      ''
    ];

    for (const [name, selector] of Object.entries(locators)) {
      const methodName = name.replace(/[\s_-]+/g, '_').toLowerCase();
      lines.push(`  get ${methodName}() {`);
      lines.push(`    return this.page.locator('${selector}');`);
      lines.push('  }');
      lines.push('');
    }

    lines.push('}');
    lines.push(`export default ${pascalName}Page;`);

    return lines.join('\n');
  }
}

export default LocatorExtractor;
