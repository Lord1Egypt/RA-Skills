import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { CONFIG_PATTERNS } from '../src/configPatterns.js';
import { extractConfigFiles } from '../src/extract.js';
import type { DiscoveredFile, ConfigCategory } from '../src/types.js';

// ---------------------------------------------------------------------------
// Helper: build a single-file DiscoveredFile array
// ---------------------------------------------------------------------------
function makeFiles(content: string, path = 'src/app.ts'): DiscoveredFile[] {
  return [{ path, content }];
}

// ---------------------------------------------------------------------------
// CONFIG_PATTERNS — regex matching per category
// ---------------------------------------------------------------------------

describe('CONFIG_PATTERNS', () => {
  /** Test that a pattern in the given category matches the input string. */
  function matches(category: ConfigCategory, input: string): boolean {
    return CONFIG_PATTERNS
      .filter((p) => p.category === category)
      .some((p) => p.regex.test(input));
  }

  describe('dotenv', () => {
    it('matches .env', () => {
      assert.ok(matches('dotenv', 'readFile(".env")'));
    });

    it('matches .env.local', () => {
      assert.ok(matches('dotenv', 'loadConfig(".env.local")'));
    });

    it('matches .env.production', () => {
      assert.ok(matches('dotenv', 'path: ".env.production"'));
    });

    it('matches .env.development', () => {
      assert.ok(matches('dotenv', '.env.development'));
    });

    it('matches .env.test', () => {
      assert.ok(matches('dotenv', "config({ path: '.env.test' })"));
    });

    it('matches .env at start of line', () => {
      assert.ok(matches('dotenv', '.env'));
    });

    it('matches .env in path context', () => {
      assert.ok(matches('dotenv', 'path/to/.env.local'));
    });
  });

  describe('yaml', () => {
    it('matches .yml files', () => {
      assert.ok(matches('yaml', 'config.yml'));
    });

    it('matches .yaml files', () => {
      assert.ok(matches('yaml', 'docker-compose.yaml'));
    });

    it('matches quoted yaml reference', () => {
      assert.ok(matches('yaml', '"config.yaml"'));
    });

    it('does NOT match MIME type text/yaml', () => {
      assert.ok(!matches('yaml', 'Content-Type: text/yaml'));
    });

    it('does NOT match MIME type application/yaml', () => {
      assert.ok(!matches('yaml', 'Accept: application/yaml'));
    });
  });

  describe('json', () => {
    it('matches tsconfig.json', () => {
      assert.ok(matches('json', 'tsconfig.json'));
    });

    it('matches package.json', () => {
      assert.ok(matches('json', '"package.json"'));
    });

    it('matches .prettierrc.json', () => {
      assert.ok(matches('json', '.prettierrc.json'));
    });

    it('matches config.json', () => {
      assert.ok(matches('json', "readFile('config.json')"));
    });

    it('does NOT match MIME type application/json', () => {
      assert.ok(!matches('json', 'Content-Type: application/json'));
    });

    it('does NOT match bare json-schema', () => {
      // "json-schema" has a filename char before .json? No — "json-schema" does not end in .json
      // The concern is things like "application/json" being a false positive
      assert.ok(!matches('json', 'application/json'));
    });

    it('does NOT match application/json in header', () => {
      assert.ok(!matches('json', "headers: { 'Content-Type': 'application/json' }"));
    });
  });

  describe('ini', () => {
    it('matches .ini files', () => {
      assert.ok(matches('ini', 'php.ini'));
    });

    it('matches .cfg files', () => {
      assert.ok(matches('ini', 'setup.cfg'));
    });

    it('matches quoted ini reference', () => {
      assert.ok(matches('ini', '"database.ini"'));
    });
  });

  describe('toml', () => {
    it('matches .toml files', () => {
      assert.ok(matches('toml', 'config.toml'));
    });

    it('matches Cargo.toml', () => {
      assert.ok(matches('toml', 'Cargo.toml'));
    });

    it('matches pyproject.toml', () => {
      assert.ok(matches('toml', 'pyproject.toml'));
    });

    it('matches quoted toml reference', () => {
      assert.ok(matches('toml', '"settings.toml"'));
    });
  });

  describe('rc-files', () => {
    it('matches .eslintrc', () => {
      assert.ok(matches('rc-files', '.eslintrc'));
    });

    it('matches .babelrc', () => {
      assert.ok(matches('rc-files', '.babelrc'));
    });

    it('matches .npmrc', () => {
      assert.ok(matches('rc-files', '.npmrc'));
    });

    it('matches quoted rc reference', () => {
      assert.ok(matches('rc-files', "readFile('.eslintrc')"));
    });
  });
});

// ---------------------------------------------------------------------------
// extractConfigFiles — integration-level tests
// ---------------------------------------------------------------------------

describe('extractConfigFiles', () => {
  it('returns entries for .env, .env.local, .env.production variants', () => {
    const files = makeFiles([
      'import dotenv from "dotenv";',
      'dotenv.config({ path: ".env" });',
      'dotenv.config({ path: ".env.local" });',
      'dotenv.config({ path: ".env.production" });',
    ].join('\n'));

    const entries = extractConfigFiles(files);
    const patterns = entries.map((e) => e.matchedPattern);

    assert.ok(patterns.includes('.env'), 'should find .env');
    assert.ok(patterns.includes('.env.local'), 'should find .env.local');
    assert.ok(patterns.includes('.env.production'), 'should find .env.production');

    for (const entry of entries) {
      assert.equal(entry.configCategory, 'dotenv');
    }
  });

  it('detects JSON config files with correct category', () => {
    const files = makeFiles([
      'const tsconfig = require("./tsconfig.json");',
      'const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));',
      'loadConfig("config.json");',
    ].join('\n'));

    const entries = extractConfigFiles(files);
    const jsonEntries = entries.filter((e) => e.configCategory === 'json');
    const patterns = jsonEntries.map((e) => e.matchedPattern);

    assert.ok(patterns.includes('tsconfig.json'));
    assert.ok(patterns.includes('package.json'));
    assert.ok(patterns.includes('config.json'));
  });

  it('detects YAML, TOML, INI, and RC config references', () => {
    const files = makeFiles([
      'const yml = readFile("config.yml");',
      'const toml = readFile("pyproject.toml");',
      'const ini = readFile("database.ini");',
      'const rc = readFile(".eslintrc");',
    ].join('\n'));

    const entries = extractConfigFiles(files);
    const categories = new Set(entries.map((e) => e.configCategory));

    assert.ok(categories.has('yaml'), 'should detect yaml');
    assert.ok(categories.has('toml'), 'should detect toml');
    assert.ok(categories.has('ini'), 'should detect ini');
    assert.ok(categories.has('rc-files'), 'should detect rc-files');
  });

  it('does NOT false-positive on MIME types', () => {
    const files = makeFiles([
      "headers['Content-Type'] = 'application/json';",
      "accept: 'text/yaml'",
      "contentType: 'application/yaml'",
    ].join('\n'));

    const entries = extractConfigFiles(files);
    assert.equal(entries.length, 0, `expected 0 entries but got: ${JSON.stringify(entries)}`);
  });

  it('each entry has sourceFile, matchedPattern, lineNumber, configCategory', () => {
    const files = makeFiles('loadConfig("tsconfig.json");\n', 'src/loader.ts');
    const entries = extractConfigFiles(files);

    assert.ok(entries.length > 0, 'should find at least one entry');
    const entry = entries[0];
    assert.equal(entry.sourceFile, 'src/loader.ts');
    assert.equal(entry.matchedPattern, 'tsconfig.json');
    assert.equal(entry.lineNumber, 1);
    assert.equal(entry.configCategory, 'json');
  });

  it('reports correct line numbers', () => {
    const files = makeFiles([
      '// first line',
      '// second line',
      'loadYaml("config.yaml");',
    ].join('\n'));

    const entries = extractConfigFiles(files);
    assert.ok(entries.length > 0);
    assert.equal(entries[0].lineNumber, 3);
  });

  it('accepts DiscoveredFile[] and returns ConfigFileEntry[]', () => {
    const files: DiscoveredFile[] = [{ path: 'a.ts', content: '"package.json"' }];
    const result = extractConfigFiles(files);
    assert.ok(Array.isArray(result));
    assert.ok(result.length > 0);
    assert.ok('sourceFile' in result[0]);
    assert.ok('matchedPattern' in result[0]);
    assert.ok('lineNumber' in result[0]);
    assert.ok('configCategory' in result[0]);
  });

  it('deduplicates same match on same line', () => {
    const files = makeFiles('.env');
    const entries = extractConfigFiles(files);
    // Should only appear once even though the pattern might match
    const envEntries = entries.filter((e) => e.matchedPattern === '.env');
    assert.equal(envEntries.length, 1);
  });

  it('handles multiple files', () => {
    const files: DiscoveredFile[] = [
      { path: 'a.ts', content: 'load(".env")' },
      { path: 'b.ts', content: 'load("config.yaml")' },
    ];
    const entries = extractConfigFiles(files);
    const sources = new Set(entries.map((e) => e.sourceFile));
    assert.ok(sources.has('a.ts'));
    assert.ok(sources.has('b.ts'));
  });

  it('handles empty input', () => {
    const entries = extractConfigFiles([]);
    assert.deepEqual(entries, []);
  });

  it('handles files with no config references', () => {
    const files = makeFiles('const x = 1 + 2;\nconsole.log(x);\n');
    const entries = extractConfigFiles(files);
    assert.equal(entries.length, 0);
  });
});
