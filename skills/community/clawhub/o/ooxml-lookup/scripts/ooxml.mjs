#!/usr/bin/env node

/**
 * The `ooxml-lookup` CLI.
 *
 * Runs from a bare checkout: no package.json, no install, no node_modules.
 * Node 24+ and nothing else. Every module it imports is either a `node:`
 * builtin or a relative path, and that is a property `core/skill-cli.test.mjs`
 * asserts rather than trusts.
 *
 * **Everything it prints on stdout is JSON.** That is the contract, and it is
 * why the experimental-warning filter is load-bearing here rather than
 * cosmetic: without it `node:sqlite` writes a paragraph of English to stderr on
 * the first call, and an agent piping this into a parser sees noise.
 */
import {explainDiagnostic, parseDiagnosticText} from './explain.mjs';
import {createGraph, PROFILE_KEYS} from './graph.mjs';

const USAGE = `ooxml — query the ECMA-376 schema graph, offline.

  ooxml element    <qname>      what a name is: kind, type, namespace, profiles
  ooxml type       <qname>      a complexType/simpleType: derivation and shape
  ooxml children   <qname>      legal children, in order, with cardinality
  ooxml attributes <qname>      attributes, inherited and attributeGroups expanded
  ooxml enum       <qname>      enumeration values of a simple type
  ooxml values     <qname>      the whole value space: facets, patterns, unions
  ooxml namespace  <uri|prefix> namespace <-> vocabulary, both directions
  ooxml search     <substring>  find symbols by name (substring, not semantic)
  ooxml diff       <qname>      what Transitional adds to Strict for this symbol
  ooxml explain    <json|text>  resolve a validator diagnostic against the schema
  ooxml sql        <select>     read-only SQL against the graph (advanced)

Options:
  --profile <transitional|strict>   default: transitional
  --limit <1-200>                   search/sql only
  --compact                         force compact JSON (default when not a TTY)

Names may be written w:tblPr, wml:tblPr, {namespace-uri}tblPr, or bare.
A bare name that means several things returns all of them.`;

/** Flags that stand alone. Every other flag takes a value. */
const SWITCHES = new Set(['compact', 'help']);

/**
 * `--flag value` and `--flag=value`, with everything else positional. A flag
 * that takes a value and has none is a usage error: read as undefined,
 * `ooxml element w:p --profile` answered for Transitional without a word.
 */
function parseArgv(argv) {
  const positional = [];
  const options = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      positional.push(arg);
      continue;
    }
    const eq = arg.indexOf('=');
    if (eq !== -1) {
      options[arg.slice(2, eq)] = arg.slice(eq + 1);
    } else if (SWITCHES.has(arg.slice(2))) {
      options[arg.slice(2)] = true;
    } else {
      const value = argv[i + 1];
      if (value === undefined || value.startsWith('--')) {
        throw new UsageError(`${arg} needs a value`);
      }
      options[arg.slice(2)] = value;
      i += 1;
    }
  }
  return {positional, options};
}

/** The MCP surface caps search at 200 too, so both surfaces answer identically. */
const MAX_LIMIT = 200;

/**
 * `--limit`, validated. Unchecked, `Number('abc')` made `sql` report rows it
 * then did not return, and made `search` fail with a bare SQLite "datatype
 * mismatch". Without a fallback an absent `--limit` stays absent, and the core
 * applies its own default.
 *
 * @param {string | undefined} raw
 * @param {number} [fallback]
 */
function limitOf(raw, fallback) {
  if (raw === undefined) return fallback;
  const n = Number(raw);
  if (!Number.isInteger(n) || n < 1 || n > MAX_LIMIT) {
    throw new UsageError(`--limit must be an integer from 1 to ${MAX_LIMIT}, got "${raw}"`);
  }
  return n;
}

function main(argv) {
  const {positional, options} = parseArgv(argv);
  const [command, ...rest] = positional;

  if (command === undefined || options.help === true || command === 'help') {
    process.stdout.write(`${USAGE}\n`);
    return 0;
  }

  const profile = options.profile;
  if (profile !== undefined && !PROFILE_KEYS.includes(profile)) {
    throw new UsageError(`--profile must be one of ${PROFILE_KEYS.join(', ')}, got "${profile}"`);
  }
  // Indentation is for a human at a terminal. Piped into an agent's context it
  // is pure cost, and this tool is used in a loop.
  const indent = options.compact === true || !process.stdout.isTTY ? 0 : 2;
  const emit = (value) => process.stdout.write(`${JSON.stringify(value, null, indent)}\n`);

  const graph = createGraph();
  try {
    const argument = rest.join(' ');
    const need = (what) => {
      if (argument === '') throw new UsageError(`${command} needs ${what}`);
      return argument;
    };

    if (Object.hasOwn(QNAME_COMMANDS, command)) {
      emit(graph[QNAME_COMMANDS[command]](need('a name'), {profile}));
      return 0;
    }
    switch (command) {
      case 'namespace':
        emit(graph.namespace(need('a URI, prefix or vocabulary')));
        return 0;
      case 'search':
        emit(
          graph.search(need('a substring'), {
            profile,
            limit: limitOf(options.limit),
          }),
        );
        return 0;
      case 'diff':
      case 'diff-profiles':
        emit(graph.diff_profiles(need('a name')));
        return 0;
      case 'explain':
        emit(explainDiagnostic(graph, parseDiagnostic(need('a diagnostic')), {profile}));
        return 0;
      case 'sql':
        emit(runSql(graph, need('a SELECT statement'), limitOf(options.limit, MAX_LIMIT)));
        return 0;
      default:
        throw new UsageError(`unknown command "${command}"`);
    }
  } finally {
    graph.close();
  }
}

class UsageError extends Error {}

/** The commands that take one name and a profile, and the core method that answers each. */
const QNAME_COMMANDS = /** @type {const} */ ({
  element: 'element',
  type: 'type',
  children: 'children',
  attributes: 'attributes',
  enum: 'enum',
  values: 'values',
});

/**
 * The diagnostic, as JSON or as pasted text. JSON may be a whole
 * `ooxml-validate` report, of which the first diagnostic is taken, because that
 * is what people actually have in hand — but the four fields are still all that
 * is read (see core/explain.mjs). Anything that does not start like JSON is
 * read as text.
 */
function parseDiagnostic(text) {
  if (!/^\s*[[{]/.test(text)) return parseDiagnosticText(text);
  let value;
  try {
    value = JSON.parse(text);
  } catch {
    // It started like JSON, so a parse failure is a typo, not a pasted message.
    throw new UsageError(
      'explain could not parse that JSON. Pass the diagnostic object from an ooxml-validate ' +
        'report, e.g. \'{"id":"Sch_UndeclaredAttribute","description":"...","xpath":"/w:document[1]"}\'',
    );
  }
  if (Array.isArray(value)) return value[0] ?? {};
  if (Array.isArray(value?.diagnostics)) return value.diagnostics[0] ?? {};
  return value;
}

/**
 * Read-only SQL, the escape hatch the subcommands do not cover.
 *
 * This is the skill's real advantage over the MCP surface: the agent has a
 * shell and the database is right there, so a documented schema plus a query
 * runner beats any fixed set of subcommands for the question nobody anticipated.
 *
 * The connection is opened read-only, so this cannot write whatever it is
 * asked; the statement check below is about giving a clear error rather than a
 * SQLite one, and about not pretending a multi-statement script will work.
 */
function runSql(graph, statement, limit) {
  const trimmed = statement.trim().replace(/;\s*$/, '');
  if (!/^(select|with)\b/i.test(trimmed)) {
    throw new UsageError(
      'sql accepts a single SELECT (or WITH ... SELECT); the database is read-only',
    );
  }
  if (trimmed.includes(';')) {
    throw new UsageError('sql runs one statement at a time');
  }

  // The cap is the database's job, not a slice afterwards: a missing join
  // predicate is an ordinary mistake, and materialising its cross product
  // exhausts memory long before any slice runs. One row past the limit is what
  // tells a complete result from a cut one. The closing parenthesis gets its
  // own line so a trailing `-- comment` cannot swallow it.
  const rows = graph._internal.handle.all(`SELECT * FROM (${trimmed}\n) LIMIT ${limit + 1}`);
  const truncated = rows.length > limit;
  return {
    sql: trimmed,
    count: Math.min(rows.length, limit),
    // Truncation is reported rather than silent — a quietly cut result set is
    // indistinguishable from a complete one.
    truncated,
    rows: rows.slice(0, limit),
  };
}

try {
  process.exitCode = main(process.argv.slice(2));
} catch (error) {
  const usage = error instanceof UsageError;
  const message = error instanceof Error ? error.message : String(error);
  process.stderr.write(`${message}\n${usage ? `\n${USAGE}\n` : ''}`);
  process.exitCode = usage ? 2 : 1;
}
