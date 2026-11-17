/**
 * Turning what an agent typed into a symbol.
 *
 * Agents write qualified names three ways and all three have to work, because
 * getting this wrong means the tool says "not found" for a name that is right
 * there:
 *
 *     w:tblPr                    a conventional prefix
 *     wml:tblPr                  a vocabulary key (what this database calls it)
 *     {http://…/main}tblPr       Clark notation, as it appears in XPath output
 *     tblPr                      bare, and frequently ambiguous
 *
 * Bare names are the interesting case. `ST_Percentage` is a
 * pattern-restricted string in `shared-commonSimpleTypes` and a *union* in
 * `dml-main`; `p` is a paragraph in wml and a text paragraph in dml. Silently
 * taking the first row would be a confidently wrong answer, so an ambiguous
 * bare name comes back as several matches and the caller reports all of them.
 */

/** `{uri}local`, `prefix:local`, or `local`. */
export function parseQName(input) {
  const text = String(input ?? '').trim();
  if (text === '') return {prefix: null, uri: null, localName: ''};

  if (text.startsWith('{')) {
    const end = text.indexOf('}');
    if (end === -1) return {prefix: null, uri: null, localName: text};
    return {prefix: null, uri: text.slice(1, end), localName: text.slice(end + 1)};
  }

  const colon = text.indexOf(':');
  if (colon === -1) return {prefix: null, uri: null, localName: text};
  return {prefix: text.slice(0, colon), uri: null, localName: text.slice(colon + 1)};
}

/**
 * Every way of naming a vocabulary, in one lookup table.
 *
 * A prefix is *observed* rather than mandated — see `observedPrefixes` in the
 * ingest — so the same prefix could in principle name two vocabularies. Where
 * that happens the prefix maps to all of them and the caller resolves the
 * ambiguity the same way it resolves a bare name, rather than silently picking.
 *
 * `prefix_aliases` feeds the same map, which is the point: `x` names both VML's
 * excel namespace (which the schemas bind) and `sml` (which they do not, but
 * every validator diagnostic does). Merging them means the existing
 * several-candidates path handles the collision, and no new rule is needed —
 * `x:worksheet` finds the one vocabulary that has a `worksheet`, `x:ClientData`
 * finds the other, and a name in both would come back as two matches.
 *
 * Aliases are recorded on the vocabulary as `aliasPrefixes` rather than merged
 * into `namespaces[].prefix`, so `formatQName` keeps emitting the canonical
 * spelling and nothing downstream starts printing an ambiguous prefix.
 */
export function loadVocabularyIndex(db) {
  const byKey = new Map();
  const byPrefix = new Map();
  const byUri = new Map();

  const rows = db.all(
    `SELECT v.id, v.key, v.external_source, n.uri, n.preferred_prefix, p.key AS profile
       FROM vocabularies v
       JOIN namespaces n ON n.vocabulary_id = v.id
       JOIN profiles p ON p.id = n.profile_id
      ORDER BY v.key, p.id`,
  );

  const addPrefix = (prefix, key) => {
    if (!byPrefix.has(prefix)) byPrefix.set(prefix, new Set());
    byPrefix.get(prefix).add(key);
  };

  for (const row of rows) {
    if (!byKey.has(row.key)) {
      byKey.set(row.key, {
        id: row.id,
        key: row.key,
        externalSource: row.external_source,
        namespaces: [],
        aliasPrefixes: [],
      });
    }
    byKey
      .get(row.key)
      .namespaces.push({uri: row.uri, prefix: row.preferred_prefix, profile: row.profile});
    byUri.set(row.uri, row.key);
    if (row.preferred_prefix !== null) addPrefix(row.preferred_prefix, row.key);
  }

  const aliases = db.all(
    `SELECT v.key, a.prefix, a.source
       FROM prefix_aliases a
       JOIN vocabularies v ON v.id = a.vocabulary_id
      ORDER BY a.prefix, v.key`,
  );
  for (const row of aliases) {
    const vocabulary = byKey.get(row.key);
    if (vocabulary === undefined) continue;
    vocabulary.aliasPrefixes.push({prefix: row.prefix, source: row.source});
    addPrefix(row.prefix, row.key);
  }

  return {byKey, byPrefix, byUri, all: [...byKey.values()]};
}

/**
 * Which vocabularies a parsed qname could belong to.
 *
 * `null` means "no constraint" — a bare name — which is different from an empty
 * array, meaning "named a vocabulary that does not exist". The caller must keep
 * those apart: one is a search, the other is a typo.
 */
export function candidateVocabularies(parsed, index) {
  if (parsed.uri !== null) {
    const key = index.byUri.get(parsed.uri);
    return key === undefined ? [] : [key];
  }
  if (parsed.prefix !== null) {
    // A vocabulary key is accepted as a prefix, since that is how the database
    // spells references internally and users read those strings in our output.
    if (index.byKey.has(parsed.prefix)) return [parsed.prefix];
    const byPrefix = index.byPrefix.get(parsed.prefix);
    return byPrefix === undefined ? [] : [...byPrefix].sort();
  }
  return null;
}

/** `wml` + `tblPr` -> `w:tblPr`, falling back to the vocabulary key when no prefix is known. */
export function formatQName(vocabularyKey, localName, index) {
  const vocabulary = index.byKey.get(vocabularyKey);
  const prefix = vocabulary?.namespaces.find((n) => n.prefix !== null)?.prefix;
  return `${prefix ?? vocabularyKey}:${localName}`;
}
