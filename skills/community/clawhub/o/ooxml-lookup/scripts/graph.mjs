/**
 * The tools. One implementation, two surfaces.
 *
 * Four rules govern every response here, and each exists because breaking it
 * produces a *confidently wrong* answer rather than a visible failure:
 *
 * 1. **Always name the profile.** Something true in Transitional and false in
 *    Strict, returned unlabelled, is a wrong answer.
 * 2. **Always resolve, never hand back a raw ref.** A `type_ref` string or an
 *    unexpanded `attributeGroup` ref makes the agent do the join, badly.
 * 3. **Absent is not prohibited.** "Not in this profile" and "no such symbol"
 *    lead to opposite next actions, so they are never the same response.
 * 4. **No raw XSD.** If a tool wants to quote, it quotes structured fields.
 */
import {DEFAULT_DB_PATH, openGraph} from './db.mjs';
import {candidateVocabularies, formatQName, loadVocabularyIndex, parseQName} from './qname.mjs';

export const PROFILE_KEYS = ['transitional', 'strict'];
export const DEFAULT_PROFILE = 'transitional';

/** Content models nest; groups reference groups. Bounded, and truncation is always reported. */
const MAX_DEPTH = 12;

export function createGraph({path = DEFAULT_DB_PATH, db = null} = {}) {
  const handle = db ?? openGraph(path);
  const index = loadVocabularyIndex(handle);
  const profiles = new Map(
    handle.all('SELECT id, key, label FROM profiles ORDER BY id').map((p) => [p.key, p]),
  );

  const profileId = (key) => {
    const profile = profiles.get(key);
    if (profile === undefined) {
      throw new Error(
        `unknown profile "${key}" — expected one of: ${[...profiles.keys()].join(', ')}`,
      );
    }
    return profile.id;
  };

  // ---------------------------------------------------------------- lookup --

  const SYMBOL_SELECT = `SELECT s.id, s.local_name, s.kind, s.parent_symbol_id, s.type_ref,
                                s.type_symbol_id, s.is_anonymous, v.key AS vocabulary
                           FROM symbols s JOIN vocabularies v ON v.id = s.vocabulary_id`;

  /** `?, ?, ?` for an `IN (…)` over `list`. */
  const placeholders = (list) => list.map(() => '?').join(', ');

  /**
   * Symbols matching a qname.
   *
   * Deliberately returns *every* match rather than the best one. A bare name is
   * routinely ambiguous, and local element declarations mean even a qualified
   * name can name several symbols — `w:p` is declared inside more than one
   * type. Collapsing that to one row is how a tool ends up describing a
   * different element than the one asked about.
   *
   * @param {string} qname
   * @param {{kind?: string | string[] | null, includeAnonymous?: boolean}} [options]
   */
  function lookup(qname, {kind = null, includeAnonymous = false} = {}) {
    const parsed = parseQName(qname);
    if (parsed.localName === '') return {parsed, vocabularies: null, rows: []};
    const vocabularies = candidateVocabularies(parsed, index);
    if (vocabularies !== null && vocabularies.length === 0) {
      return {parsed, vocabularies, rows: []};
    }

    const clauses = [];
    const params = [];
    if (vocabularies !== null) {
      clauses.push(`v.key IN (${placeholders(vocabularies)})`);
      params.push(...vocabularies);
    }
    if (kind !== null) {
      const kinds = [kind].flat();
      clauses.push(`s.kind IN (${placeholders(kinds)})`);
      params.push(...kinds);
    }
    if (!includeAnonymous) clauses.push('s.is_anonymous = 0');

    // XML names are case-sensitive, so the exact spelling wins outright: `Types`
    // is the content-types root and `w:types` is an unrelated wml element, and
    // folding case made them one ambiguous answer. Case is folded only when
    // nothing matches exactly, so `tblpr` still finds `w:tblPr`.
    const select = (nameClause) =>
      handle.all(
        `${SYMBOL_SELECT}
          WHERE ${[nameClause, ...clauses].join(' AND ')}
          ORDER BY s.parent_symbol_id, v.key, s.kind, s.id`,
        parsed.localName,
        ...params,
      );
    const exact = select('s.local_name = ?');
    const rows = exact.length > 0 ? exact : select('s.local_name = ? COLLATE NOCASE');
    return {parsed, vocabularies, rows};
  }

  const symbolById = (id) => handle.get(`${SYMBOL_SELECT} WHERE s.id = ?`, id);

  /** The derivation edge of a type in a profile, or undefined. At most one exists. */
  const baseOf = (symbolId, pid) =>
    handle.get(
      `SELECT relation, content_model, base_type_ref, base_symbol_id FROM inheritance_edges
        WHERE symbol_id = ? AND profile_id = ?`,
      symbolId,
      pid,
    );

  const enumValuesOf = (symbolId, pid) =>
    handle
      .all(
        'SELECT value FROM enums WHERE symbol_id = ? AND profile_id = ? ORDER BY order_index',
        symbolId,
        pid,
      )
      .map((row) => row.value);

  const childEdgeCount = (symbolId, pid) =>
    handle.get(
      'SELECT COUNT(*) AS n FROM child_edges WHERE parent_symbol_id = ? AND profile_id = ?',
      symbolId,
      pid,
    ).n;

  /** The type or group a local declaration sits in, or null for a global one. */
  const declaredInName = (row) =>
    row.parent_symbol_id === 0 ? null : display(symbolById(row.parent_symbol_id));

  const symbolProfiles = (id) =>
    handle
      .all(
        `SELECT p.key FROM symbol_profiles sp JOIN profiles p ON p.id = sp.profile_id
          WHERE sp.symbol_id = ? ORDER BY p.id`,
        id,
      )
      .map((r) => r.key);

  const namespaceOf = (vocabularyKey, profile) =>
    index.byKey.get(vocabularyKey)?.namespaces.find((n) => n.profile === profile) ?? null;

  const display = (row) => formatQName(row.vocabulary, row.local_name, index);

  /**
   * Where a vocabulary ECMA-376 only references is really defined, or null.
   * Carried on every answer about one of its symbols, because "no type" from
   * such a symbol means "not recorded here", not "has none".
   */
  const externalSource = (vocabularyKey) => index.byKey.get(vocabularyKey)?.externalSource ?? null;
  const externalNote = (vocabularyKey) => {
    const source = externalSource(vocabularyKey);
    return source === null ? {} : {external_source: source};
  };

  /**
   * A stored reference, rewritten for a reader.
   *
   * The database spells references `vocabularyKey:localName` (`wml:CT_P`)
   * because the vocabulary is the identity. Nobody writes documents that way —
   * they write `w:CT_P` — so every ref leaving this module goes through here.
   * Rule 2 is about resolution, but a resolved answer in an unfamiliar spelling
   * is still work pushed back onto the caller.
   */
  const displayRef = (ref) => {
    if (ref === null || ref === undefined) return ref;
    const colon = ref.indexOf(':');
    if (colon === -1) return ref;
    const vocabulary = ref.slice(0, colon);
    if (vocabulary === 'xsd' || vocabulary === 'xml') return ref;
    if (!index.byKey.has(vocabulary)) return ref;
    return formatQName(vocabulary, ref.slice(colon + 1), index);
  };

  /** A type reference, resolved. Built-ins stay named but carry no symbol. */
  function describeType(typeRef, typeSymbolId) {
    if (typeRef === null) return null;
    if (typeSymbolId === null) return {qname: displayRef(typeRef), builtin: true};
    const target = symbolById(typeSymbolId);
    return {qname: display(target), kind: target.kind, builtin: false, id: target.id};
  }

  function describeSymbol(row, profile) {
    const owner = declaredInName(row);
    const namespace = namespaceOf(row.vocabulary, profile);
    return {
      id: row.id,
      qname: display(row),
      name: row.local_name,
      kind: row.kind,
      vocabulary: row.vocabulary,
      namespace: namespace === null ? null : {uri: namespace.uri, prefix: namespace.prefix},
      profiles: symbolProfiles(row.id),
      scope: owner === null ? 'global' : {declared_in: owner},
      type: describeType(row.type_ref, row.type_symbol_id),
      ...externalNote(row.vocabulary),
    };
  }

  /**
   * The envelope every tool returns for a name it could not resolve.
   *
   * Rule 3 lives here: different "no" answers, because the next action
   * differs. Nothing found at all is a typo; found but not in this profile is a
   * profile switch; found, but not as a kind this tool takes, is a different
   * tool; a named vocabulary that does not exist is a bad prefix.
   *
   * `found` is the caller's own lookup, filtered by the caller's `kind`, with
   * no row in `profile`. Judging the profile from those rows rather than an
   * unfiltered lookup is the point: `w:p` is in both profiles, so the
   * type-only miss of `type('w:p')` must not read as a profile miss.
   *
   * @param {string} qname
   * @param {{parsed: any, vocabularies: string[] | null, rows: any[]}} found
   * @param {string} profile
   * @param {{kind?: string[] | null, expected?: string}} [options]
   */
  function notFound(qname, {parsed, vocabularies, rows}, profile, {kind = null, expected} = {}) {
    if (vocabularies !== null && vocabularies.length === 0) {
      return {
        found: false,
        reason: 'unknown_vocabulary',
        message:
          `no vocabulary is named "${parsed.prefix ?? parsed.uri}". ` +
          `Known prefixes: ${knownPrefixes().join(', ')}.`,
      };
    }
    const others = [...new Set(rows.flatMap((row) => symbolProfiles(row.id)))].filter(
      (key) => key !== profile,
    );
    if (others.length > 0) {
      return {
        found: false,
        reason: 'not_in_profile',
        message: `"${qname}" exists, but not in the ${profile} profile. It is in: ${others.join(', ')}.`,
        profiles: others,
      };
    }
    if (kind !== null) {
      const any = lookup(qname).rows;
      if (any.length > 0) return wrongKind(qname, inProfile(any, profile), any, expected);
    }
    return {
      found: false,
      reason: 'unknown_symbol',
      message: `no symbol named "${parsed.localName}" — this is a name lookup, not a search. Try search("${parsed.localName}").`,
    };
  }

  const KIND_NOUNS = {
    element: 'an element',
    attribute: 'an attribute',
    complexType: 'a complex type',
    simpleType: 'a simple type',
    group: 'a model group',
    attributeGroup: 'an attribute group',
  };

  /**
   * The miss for a name that exists, but not as a kind the tool takes.
   *
   * Neither a typo nor a profile switch helps here, so the message names what
   * the symbol is and the call that does answer it. `rows` are the matches in
   * the requested profile when there are any, so the advice is about the
   * symbol the caller can actually use.
   */
  function wrongKind(qname, inRequested, all, expected) {
    const rows = inRequested.length > 0 ? inRequested : all;
    const kinds = [...new Set(rows.map((row) => row.kind))];
    const typeNames = [
      ...new Set(
        rows
          .filter((row) => row.type_symbol_id !== null)
          .map((row) => display(symbolById(row.type_symbol_id))),
      ),
    ];
    const calls = new Set();
    for (const k of kinds) {
      if (k === 'element') {
        for (const name of typeNames) calls.add(`type('${name}')`);
        calls.add(`children('${qname}')`);
      } else if (k === 'complexType') {
        calls.add(`type('${qname}')`);
        calls.add(`children('${qname}')`);
      } else if (k === 'group') {
        calls.add(`children('${qname}')`);
      } else if (k === 'attribute' || k === 'simpleType') {
        calls.add(`values('${qname}')`);
      } else if (k === 'attributeGroup') {
        calls.add(`attributes('${qname}')`);
      } else {
        calls.add(`element('${qname}')`);
      }
    }
    const typed =
      typeNames.length === 0
        ? ''
        : ` Its type ${typeNames.length === 1 ? 'is' : 'is one of'} ${typeNames.join(', ')}.`;
    return {
      found: false,
      reason: 'wrong_kind',
      message:
        `"${qname}" is ${kinds.map((k) => KIND_NOUNS[k] ?? k).join(' and ')}, not ${expected}.` +
        `${typed} Use ${[...calls].join(' or ')}.`,
      kinds,
    };
  }

  // Aliases are included because this list is advice for a caller who just
  // mistyped a prefix, and "the prefixes that work" is the useful set — a
  // spelling we accept but omit here reads as unsupported.
  const knownPrefixes = () =>
    [
      ...new Set(
        index.all.flatMap((v) => [
          ...v.namespaces.map((n) => n.prefix),
          ...v.aliasPrefixes.map((a) => a.prefix),
        ]),
      ),
    ]
      .filter(Boolean)
      .sort();

  /** Only symbols actually present in the requested profile. */
  const inProfile = (rows, profile) =>
    rows.filter((row) => symbolProfiles(row.id).includes(profile));

  /**
   * What an ambiguous answer says, which depends on why it is ambiguous.
   *
   * The two causes need opposite advice. A name matching several *vocabularies*
   * is the caller's to fix — qualifying it picks one. A name declared in
   * several places *within* a vocabulary cannot be fixed that way: `w:tblPr` is
   * genuinely two content models and which applies depends on the parent, so
   * the answer has to carry both and say where each holds.
   *
   * It lists the matched *names*, not the resolved types: `a:p, sml:p, w:p` is
   * what the caller can qualify with, `a:CT_TextParagraph` is not.
   */
  const ambiguityMessage = (qname, resolved, noun) =>
    resolved.ambiguity === 'vocabulary'
      ? `"${qname}" names ${resolved.names.length} unrelated symbols that share a local name: ` +
        `${resolved.names.join(', ')}. Qualify the name to pick one.`
      : `${qname} has ${resolved.variants.length} different ${noun} depending on where it appears.`;

  /**
   * One variant answers flat; several answer `ambiguous` with every variant.
   * The common case stays flat, and only a genuinely ambiguous name pays for
   * the extra nesting, visibly.
   */
  const variantAnswer = (qname, profile, variants, describe, message) =>
    variants.length === 1
      ? {query: qname, profile, found: true, ...describe(variants[0])}
      : {
          query: qname,
          profile,
          found: true,
          ambiguous: true,
          message,
          variants: variants.map(describe),
        };

  /** Which type a `resolveToType` variant is and where it applies. Mirrors `PLACEMENT`. */
  const placement = ({symbol, via, declaredIn}, truncated) => ({
    type: display(symbol),
    ...(via === null ? {} : {resolved_from: via}),
    ...(declaredIn.length === 0 ? {} : {applies_when_declared_in: declaredIn}),
    truncated,
  });

  // ----------------------------------------------------------------- tools --

  /** Canonical record for a name. */
  function element(qname, {profile = DEFAULT_PROFILE} = {}) {
    profileId(profile);
    const found = lookup(qname);
    const matches = inProfile(found.rows, profile);
    if (matches.length === 0) return {query: qname, profile, ...notFound(qname, found, profile)};
    return {
      query: qname,
      profile,
      found: true,
      count: matches.length,
      // More than one is normal, not an error: the same element name is
      // declared inside several types, and they can carry different types.
      symbols: matches.map((row) => describeSymbol(row, profile)),
    };
  }

  /** A complexType or simpleType: what it derives from and what shape it has. */
  function type(qname, {profile = DEFAULT_PROFILE} = {}) {
    const pid = profileId(profile);
    const kind = ['complexType', 'simpleType'];
    const found = lookup(qname, {kind});
    const matches = inProfile(found.rows, profile);
    if (matches.length === 0) {
      return {
        query: qname,
        profile,
        ...notFound(qname, found, profile, {kind, expected: 'a type'}),
      };
    }

    return {
      query: qname,
      profile,
      found: true,
      count: matches.length,
      types: matches.map((row) => {
        const base = baseOf(row.id, pid);
        const summary =
          row.kind === 'simpleType'
            ? {value_space: describeValueSpace(row.id, pid, 0)}
            : {
                content: contentSummary(row.id, pid),
                // The whole legal set, inherited and grouped attributes
                // included, not the ones this type happens to declare itself.
                attribute_count: attributeSet(row.id, pid).list.length,
              };
        return {
          ...describeSymbol(row, profile),
          derivation:
            base === undefined
              ? null
              : {
                  relation: base.relation,
                  content_model: base.content_model,
                  base: describeType(base.base_type_ref, base.base_symbol_id),
                },
          ...summary,
        };
      }),
    };
  }

  /** A one-line shape for `type`, so it does not have to embed the whole tree. */
  function contentSummary(symbolId, pid) {
    const compositors = handle.all(
      'SELECT kind FROM compositors WHERE parent_symbol_id = ? AND profile_id = ? ORDER BY order_index',
      symbolId,
      pid,
    );
    const children = childEdgeCount(symbolId, pid);
    const groups = handle.get(
      `SELECT COUNT(*) AS n FROM group_edges
        WHERE parent_symbol_id = ? AND profile_id = ? AND ref_kind = 'group'`,
      symbolId,
      pid,
    ).n;
    if (compositors.length === 0 && groups === 0) return 'empty';
    return {top: compositors.map((c) => c.kind), direct_children: children, group_refs: groups};
  }

  // ------------------------------------------------------------- children ---

  /**
   * Legal children, in schema order.
   *
   * The differentiator, so the output is both shapes at once: the **compositor
   * tree**, which is what actually answers "can I put this here, and where",
   * and a **flat ordered list** for the common case. A flat list alone loses
   * the choice/sequence distinction, which is most of the question.
   *
   * Two resolutions happen before anything is returned, and skipping either
   * produces a plausible wrong answer:
   *
   * - **Inheritance.** For an `extension`, the base's particle comes *first*,
   *   then the derived one. Every contributed node says which type it came
   *   from, so the agent can see why. A `restriction` replaces the base's
   *   particle rather than extending it, and is not prepended.
   * - **Group refs.** A type whose whole content is a `group ref` has zero
   *   `child_edges` — `CT_SolidColorFillProperties` is the standard example —
   *   so a query that reads only `child_edges` answers "accepts nothing" for a
   *   large part of DrawingML. Groups are expanded in place, carrying the
   *   *ref site's* cardinality, not the definition's.
   */
  function children(qname, {profile = DEFAULT_PROFILE, expandGroups = true} = {}) {
    const pid = profileId(profile);
    const resolved = resolveToType(qname, profile);
    if (resolved.found === false) return {query: qname, profile, ...resolved};

    const describe = (variant) => {
      const state = {seenGroups: new Set(), truncated: false};
      const tree = particlesOf(variant.symbol.id, pid, state, 0, expandGroups);
      return {...placement(variant, state.truncated), tree, order: flatten(tree)};
    };

    return variantAnswer(
      qname,
      profile,
      resolved.variants,
      describe,
      ambiguityMessage(qname, resolved, 'content models'),
    );
  }

  /**
   * An element resolves to its type; a type is already one.
   *
   * Returns **every** distinct type the name resolves to, because in this
   * corpus one element name genuinely has several. `w:tblPr` is `CT_TblPr`
   * inside `CT_Tbl` and `CT_TblPrBase` in three other places — a real
   * difference, and the second most common thing anyone asks about tables.
   *
   * Refusing to answer until the caller disambiguates would be correct and
   * useless; picking one silently would be wrong. So each variant is resolved
   * and labelled with where it applies, and the caller decides.
   */
  function resolveToType(qname, profile, {attributeGroups = false} = {}) {
    const found = lookup(qname);
    const matches = inProfile(found.rows, profile);
    if (matches.length === 0) return notFound(qname, found, profile);

    // A global type name is unique per vocabulary but not across them:
    // `CT_Shape` is declared in six, and they are unrelated types that happen
    // to share a name. Returning the first is the silent pick rule 3 forbids,
    // and it is the wrong one five times out of six.
    const typeKinds = ['complexType', 'group', ...(attributeGroups ? ['attributeGroup'] : [])];
    const asType = matches.filter((r) => typeKinds.includes(r.kind));
    if (asType.length > 0) {
      return {
        found: true,
        ambiguity: 'vocabulary',
        names: asType.map(display),
        variants: asType.map((symbol) => ({symbol, via: null, declaredIn: []})),
      };
    }

    // Only a complex type has content or attributes. A declaration typed by a
    // simple type resolved to that type answers an empty tree with
    // `found: true`, which reads as "nothing is allowed here", not "this holds
    // a value".
    const declarations = matches.filter(
      (r) => r.type_symbol_id !== null && symbolById(r.type_symbol_id).kind === 'complexType',
    );
    if (declarations.length === 0) {
      const group = matches.find((r) => r.kind === 'attributeGroup');
      const simple = matches.find((r) => r.kind === 'simpleType' || r.type_ref !== null);
      const external = matches.find((r) => externalSource(r.vocabulary) !== null);
      return {
        found: false,
        reason: 'no_content_model',
        message: group
          ? `${qname} is an attribute group: it has attributes but no element content. ` +
            `Use attributes('${qname}').`
          : simple
            ? `${qname} ${simple.kind === 'simpleType' ? 'is' : `has type ${displayRef(simple.type_ref)},`} ` +
              `a simple type with no element content or attributes. Use values('${qname}').`
            : external
              ? `${display(external)} is defined outside ECMA-376, and its type is not recorded here. ` +
                `Defined in: ${externalSource(external.vocabulary)}`
              : `${qname} declares no type, so it has no children in the schema.`,
      };
    }

    // Group the declarations by the type they point at, so the answer is one
    // entry per genuinely different content model rather than one per site.
    const byType = new Map();
    for (const row of declarations) {
      if (!byType.has(row.type_symbol_id)) byType.set(row.type_symbol_id, []);
      byType.get(row.type_symbol_id).push(row);
    }

    // Same-named elements in different vocabularies are unrelated — `p` is a:p,
    // sml:p and w:p — so the caller fixes it by qualifying, not by looking at
    // the parent. Only a name confined to one vocabulary varies by site.
    const elementNames = [...new Set(declarations.map(display))];
    const spansVocabularies = new Set(declarations.map((r) => r.vocabulary)).size > 1;

    return {
      found: true,
      ambiguity: spansVocabularies ? 'vocabulary' : 'declaration_site',
      names: elementNames,
      variants: [...byType.entries()].map(([typeSymbolId, sites]) => ({
        symbol: symbolById(typeSymbolId),
        via: `${display(sites[0])} -> ${displayRef(sites[0].type_ref)}`,
        declaredIn: sites.map((r) => declaredInName(r) ?? 'global'),
      })),
    };
  }

  /**
   * The particle tree of one type, with inheritance and groups resolved.
   *
   * `contributedBy` threads the originating type down through the recursion so
   * every node in the answer can say where it came from — the difference
   * between "these are the legal children" and "these are the legal children
   * *and here is why*".
   */
  /** @param {string | null} contributedBy the type that contributed these particles, if inherited */
  function particlesOf(symbolId, pid, state, depth, expandGroups, contributedBy = null) {
    if (depth > MAX_DEPTH) {
      state.truncated = true;
      return [];
    }
    const nodes = [];

    const base = baseOf(symbolId, pid);
    // Extension prepends the base particle; restriction replaces it. Getting
    // this backwards reorders the legal children of every derived type.
    if (base !== undefined && base.relation === 'extension' && base.base_symbol_id !== null) {
      const from = display(symbolById(base.base_symbol_id));
      nodes.push(...particlesOf(base.base_symbol_id, pid, state, depth + 1, expandGroups, from));
    }

    nodes.push(...topLevelParticles(symbolId, pid, state, depth, expandGroups, contributedBy));
    return nodes;
  }

  /**
   * The particles directly under a type or group definition, or inside one
   * compositor, merged into document order. Only a compositor holds element
   * edges; a definition's top level is compositors and group refs.
   *
   * @param {{parentSymbolId: number} | {compositorId: number}} parent
   */
  function particleRows(parent, pid) {
    const inCompositor = 'compositorId' in parent;
    const id = inCompositor ? parent.compositorId : parent.parentSymbolId;
    const tag = (kind) => (row) => ({...row, _kind: kind});
    const elements = inCompositor
      ? handle
          .all(
            `SELECT child_symbol_id, min_occurs, max_occurs, order_index,
                    is_wildcard, wildcard_namespace, wildcard_process_contents
               FROM child_edges WHERE compositor_id = ? AND profile_id = ? ORDER BY order_index`,
            id,
            pid,
          )
          .map(tag('child'))
      : [];
    const compositors = handle
      .all(
        `SELECT id, kind, min_occurs, max_occurs, order_index FROM compositors
          WHERE ${inCompositor ? 'parent_compositor_id' : 'parent_symbol_id'} = ? AND profile_id = ?
          ORDER BY order_index`,
        id,
        pid,
      )
      .map(tag('compositor'));
    const groups = handle
      .all(
        `SELECT id, group_symbol_id, min_occurs, max_occurs, order_index FROM group_edges
          WHERE ${inCompositor ? 'compositor_id = ?' : 'parent_symbol_id = ? AND compositor_id IS NULL'}
            AND profile_id = ? AND ref_kind = 'group'
          ORDER BY order_index`,
        id,
        pid,
      )
      .map(tag('group'));
    return [...elements, ...compositors, ...groups].sort((a, b) => a.order_index - b.order_index);
  }

  /** Compositors and group refs hanging directly off a definition, in document order. */
  function topLevelParticles(symbolId, pid, state, depth, expandGroups, contributedBy) {
    return particleRows({parentSymbolId: symbolId}, pid).map((entry) =>
      particleNode(entry, pid, state, depth, expandGroups, contributedBy),
    );
  }

  /** Elements, wildcards, nested compositors and group refs inside one compositor. */
  function compositorChildren(compositorId, pid, state, depth, expandGroups, contributedBy) {
    if (depth > MAX_DEPTH) {
      state.truncated = true;
      return [];
    }
    return particleRows({compositorId}, pid).map((entry) =>
      particleNode(entry, pid, state, depth + 1, expandGroups, contributedBy),
    );
  }

  const fromField = (contributedBy) => (contributedBy === null ? {} : {from: contributedBy});

  function particleNode(entry, pid, state, depth, expandGroups, contributedBy) {
    if (entry._kind === 'compositor') {
      return {
        kind: entry.kind,
        min: entry.min_occurs,
        max: entry.max_occurs,
        ...fromField(contributedBy),
        children: compositorChildren(entry.id, pid, state, depth, expandGroups, contributedBy),
      };
    }
    if (entry._kind === 'group') {
      return groupNode(entry, pid, state, depth, expandGroups, contributedBy);
    }
    if (entry.is_wildcard === 1) {
      return {
        kind: 'any',
        namespace: entry.wildcard_namespace,
        process_contents: entry.wildcard_process_contents,
        min: entry.min_occurs,
        max: entry.max_occurs,
        ...fromField(contributedBy),
      };
    }
    const child = symbolById(entry.child_symbol_id);
    return {
      kind: 'element',
      qname: display(child),
      type: displayRef(child.type_ref),
      min: entry.min_occurs,
      max: entry.max_occurs,
      ...fromField(contributedBy),
    };
  }

  /**
   * A group reference, expanded in place.
   *
   * The min/max reported are the **ref site's**: `<xsd:group ref="EG_X"
   * maxOccurs="unbounded"/>` says the group repeats here, which is not what the
   * group's own definition says.
   *
   * A group already open on this path is marked `recursive` rather than
   * expanded again. Measured on the built graph, ECMA-376 has 19
   * group-to-group references and **no cycles among them**, so this guard does
   * not currently fire — the recursion in OOXML runs through *types*
   * (CT_Tbl -> CT_Row -> CT_Cell -> block content), which this function does
   * not follow. It stays anyway: the failure it prevents is a hang rather than
   * a wrong answer, and one added group ref in a future edition is all it takes.
   */
  function groupNode(edge, pid, state, depth, expandGroups, contributedBy) {
    const group = symbolById(edge.group_symbol_id);
    /** @type {{kind: string, qname: string, min: number, max: number, from?: string, children?: any[]}} */
    const node = {
      kind: 'group',
      qname: display(group),
      min: edge.min_occurs,
      max: edge.max_occurs,
      ...fromField(contributedBy),
    };
    if (!expandGroups) return node;
    if (state.seenGroups.has(group.id)) return {...node, recursive: true};
    if (depth > MAX_DEPTH) {
      state.truncated = true;
      return {...node, truncated: true};
    }

    state.seenGroups.add(group.id);
    node.children = topLevelParticles(group.id, pid, state, depth + 1, expandGroups, contributedBy);
    state.seenGroups.delete(group.id);
    return node;
  }

  /** Every element the tree permits, in order, flattened for the common case. */
  function flatten(nodes, path = [], out = []) {
    const where = path.join(' > ') || 'top';
    for (const node of nodes) {
      if (node.kind === 'element') {
        out.push({
          qname: node.qname,
          type: node.type,
          min: node.min,
          max: node.max,
          in: where,
          ...(node.from === undefined ? {} : {from: node.from}),
        });
      } else if (node.kind === 'any') {
        out.push({
          wildcard: node.namespace,
          process_contents: node.process_contents,
          in: where,
        });
      } else if (node.children !== undefined) {
        const label = node.kind === 'group' ? `group ${node.qname}` : node.kind;
        flatten(node.children, [...path, label], out);
      }
    }
    return out;
  }

  // ----------------------------------------------------------- attributes ---

  /**
   * Attributes of a type, including inherited ones and attributeGroup
   * expansions.
   *
   * Everything is resolved: an `attributeGroup` ref is expanded to the
   * attributes it carries, and each attribute names where it came from. An
   * agent asked to add an attribute needs the whole legal set, not the set this
   * one type happens to declare directly.
   */
  function attributes(qname, {profile = DEFAULT_PROFILE} = {}) {
    const pid = profileId(profile);
    // An attributeGroup has no content model, but it does have attributes:
    // `w:AG_Password` is the whole answer to "what does document protection
    // take".
    const resolved = resolveToType(qname, profile, {attributeGroups: true});
    if (resolved.found === false) return {query: qname, profile, ...resolved};

    const describe = (variant) => {
      const {list, truncated} = attributeSet(variant.symbol.id, pid);
      return {...placement(variant, truncated), count: list.length, attributes: list};
    };

    return variantAnswer(
      qname,
      profile,
      resolved.variants,
      describe,
      ambiguityMessage(qname, resolved, 'types'),
    );
  }

  /** Every attribute one type or attributeGroup accepts, resolved and sorted by name. */
  function attributeSet(rootSymbolId, pid) {
    const collected = [];
    // Shared across the base-type recursion too, so a group referenced by
    // both a base and a derived type is expanded once, at the base. That is
    // safe because an attributeGroup carries no per-site variation in
    // ECMA-376; it would stop being safe if one ever did.
    const seenGroups = new Set();
    const state = {truncated: false};

    const collect = (symbolId, from, depth) => {
      // Recorded, never silent: a short list with no flag reads as the whole
      // legal set, and the caller would never add the missing attribute.
      if (depth > MAX_DEPTH) {
        state.truncated = true;
        return;
      }

      const base = baseOf(symbolId, pid);
      // Both extension and restriction inherit attributes — unlike particles,
      // where restriction replaces. A restriction may narrow an attribute's
      // use, and the derived declaration wins, which is why the base is
      // collected first and later duplicates override.
      if (base !== undefined && base.base_symbol_id !== null) {
        collect(base.base_symbol_id, display(symbolById(base.base_symbol_id)), depth + 1);
      }

      // A `ref` attribute declares nothing itself: its type is on the global
      // attribute it names, and so is its namespace. Read both through the
      // ref, or `r:id` comes back untyped and indistinguishable from `id`.
      const owner = symbolById(symbolId).vocabulary;
      for (const row of handle.all(
        `SELECT e.local_name, e.attr_use, e.is_qualified, e.default_value, e.fixed_value,
                COALESCE(e.type_ref, a.type_ref) AS type_ref,
                COALESCE(e.type_symbol_id, a.type_symbol_id) AS type_symbol_id,
                v.key AS ref_vocabulary
           FROM attr_edges e
           LEFT JOIN symbols a ON a.id = e.attr_symbol_id
           LEFT JOIN vocabularies v ON v.id = a.vocabulary_id
          WHERE e.symbol_id = ? AND e.profile_id = ? ORDER BY e.order_index`,
        symbolId,
        pid,
      )) {
        const qualified = row.is_qualified === 1;
        const vocabulary = row.ref_vocabulary ?? (qualified ? owner : null);
        collected.push({
          name: row.local_name,
          // The spelling a document uses. Absent on an unqualified attribute,
          // which is in no namespace and is written bare.
          ...(vocabulary === null ? {} : {qname: formatQName(vocabulary, row.local_name, index)}),
          qualified,
          use: row.attr_use,
          type: describeType(row.type_ref, row.type_symbol_id),
          ...(row.default_value === null ? {} : {default: row.default_value}),
          ...(row.fixed_value === null ? {} : {fixed: row.fixed_value}),
          ...(from === null ? {} : {from}),
        });
      }

      for (const row of handle.all(
        `SELECT group_symbol_id FROM group_edges
        WHERE parent_symbol_id = ? AND profile_id = ? AND ref_kind = 'attributeGroup'
        ORDER BY order_index`,
        symbolId,
        pid,
      )) {
        if (seenGroups.has(row.group_symbol_id)) continue;
        seenGroups.add(row.group_symbol_id);
        collect(row.group_symbol_id, display(symbolById(row.group_symbol_id)), depth + 1);
      }
    };

    collect(rootSymbolId, null, 0);

    // A derived type redeclaring an inherited attribute wins; it was
    // collected later, so the last write is the right one. Keyed on the
    // namespace too: `id` and `r:id` on a slide list entry are two
    // attributes, not one declared twice.
    const byIdentity = new Map();
    for (const attribute of collected) byIdentity.set(attribute.qname ?? attribute.name, attribute);
    return {
      list: [...byIdentity.values()].sort(
        (a, b) =>
          a.name.localeCompare(b.name, 'en') || (a.qname ?? '').localeCompare(b.qname ?? '', 'en'),
      ),
      truncated: state.truncated,
    };
  }

  // --------------------------------------------------------------- values ---

  /**
   * Every distinct simple type a name resolves to.
   *
   * `resolveToType`'s counterpart for the value-space tools, and the sharper
   * case of the same hazard: `ST_Direction` is `ltr|rtl` in wml, `horz|vert` in
   * pml and `norm|rev` in dml-diagram. Collapsing that to one is not a partial
   * answer, it is a wrong one that reads as authoritative.
   *
   * Deduplicated on the resolved *target*, so several declarations pointing at
   * one type stay a single answer rather than becoming false ambiguity.
   */
  function resolveToSimpleType(qname, profile) {
    const kind = ['simpleType', 'attribute', 'element'];
    const found = lookup(qname, {kind});
    const matches = inProfile(found.rows, profile);
    if (matches.length === 0) {
      return notFound(qname, found, profile, {
        kind,
        expected: 'a simple type',
      });
    }

    const pid = profileId(profile);
    const byKey = new Map();
    for (const row of matches) {
      const target = valueTarget(row, pid);
      const key = target.symbolId === null ? `ref:${target.typeRef}` : `id:${target.symbolId}`;
      if (!byKey.has(key)) byKey.set(key, {...target, sites: []});
      byKey.get(key).sites.push(declaredInName(row) ?? 'global');
    }
    const targets = [...byKey.values()];

    // `w:p` is an element, so it gets this far, but its type is element
    // content. Answering `unconstrained` would read as "any string is legal".
    if (targets.every((t) => t.complex)) {
      return wrongKind(qname, matches, matches, 'one with a simple value space');
    }
    // As in `resolveToType`: qualifying fixes a name shared across
    // vocabularies, but not one whose declarations differ by site, like sml
    // `t`, which is text in rich text and a tuple inside an MDX entry.
    const ambiguity =
      new Set(matches.map((r) => r.vocabulary)).size > 1 ? 'vocabulary' : 'declaration_site';
    return {found: true, ambiguity, targets};
  }

  /**
   * The simple type that bounds a declaration's text, or the complex type
   * that stands in its way.
   *
   * A complex type with simple content carries a value as well as
   * attributes: `x:f` is `CT_CellFormula`, which extends `ST_Formula`. Its
   * value space is the base's, so the chain is followed to it.
   *
   * @returns {{row: any, symbolId: number | null, typeRef: string | null, complex?: true, simpleContentOf?: string}}
   */
  function valueTarget(row, pid) {
    if (row.kind === 'simpleType') return {row, symbolId: row.id, typeRef: null};
    let symbolId = row.type_symbol_id;
    let typeRef = row.type_ref;
    let simpleContentOf;
    for (let depth = 0; symbolId !== null; depth++) {
      const symbol = symbolById(symbolId);
      if (symbol.kind === 'simpleType') break;
      const base = baseOf(symbolId, pid);
      if (base?.content_model !== 'simpleContent' || depth > MAX_DEPTH) {
        return {row, symbolId, typeRef, complex: true};
      }
      simpleContentOf ??= display(symbol);
      symbolId = base.base_symbol_id;
      typeRef = base.base_type_ref;
    }
    return {row, symbolId, typeRef, ...(simpleContentOf === undefined ? {} : {simpleContentOf})};
  }

  const targetName = ({symbolId, typeRef}) =>
    symbolId === null ? displayRef(typeRef) : display(symbolById(symbolId));

  /** Where a target's value space came from, when it was not the declared type. */
  const viaField = (target) =>
    target.simpleContentOf === undefined ? {} : {simple_content_of: target.simpleContentOf};

  /** A variant of an ambiguous name whose type is element content. */
  const complexVariant = (target, extra) => ({
    type: targetName(target),
    reason: 'not_a_simple_type',
    message:
      `${targetName(target)} has element content, so it has no simple value space. ` +
      `Use children('${targetName(target)}').`,
    ...extra,
  });

  /**
   * Every variant of a value-space answer, labelled with where it applies
   * when that is what tells the variants apart. Mirrors `variantAnswer`.
   */
  const valueAnswer = (qname, profile, resolved, describe) =>
    variantAnswer(
      qname,
      profile,
      resolved.targets,
      (target) => ({
        ...describe(target),
        ...(resolved.ambiguity === 'declaration_site' && resolved.targets.length > 1
          ? {applies_when_declared_in: target.sites}
          : {}),
      }),
      resolved.ambiguity === 'vocabulary'
        ? `"${qname}" resolves to ${resolved.targets.length} unrelated types that share a local ` +
            `name: ${resolved.targets.map(targetName).join(', ')}. Qualify the name to pick one.`
        : `${qname} has ${resolved.targets.length} different value spaces depending on where it appears.`,
    );

  /** Enumeration values only. Says so usefully when the type is not enumerated. */
  function enumValues(qname, {profile = DEFAULT_PROFILE} = {}) {
    const pid = profileId(profile);
    const resolved = resolveToSimpleType(qname, profile);
    if (resolved.found === false) return {query: qname, profile, ...resolved};

    const describe = (target) => {
      if (target.complex) return complexVariant(target, {enumerated: false, values: []});
      if (target.symbolId === null) {
        return {
          type: targetName(target),
          ...viaField(target),
          enumerated: false,
          reason: 'not_a_simple_type',
          message: `${display(target.row)} has no simple type to enumerate.`,
          values: [],
        };
      }
      const name = targetName(target);
      const values = enumValuesOf(target.symbolId, pid);
      // Not an error — most simple types are bounded by facets or unions rather
      // than enumerated, and `values` is the tool that answers those.
      if (values.length === 0) {
        return {
          type: name,
          ...viaField(target),
          enumerated: false,
          message: `${name} is not an enumerated type; use values() for its facets and union members.`,
          values: [],
        };
      }
      return {
        type: name,
        ...viaField(target),
        enumerated: true,
        count: values.length,
        values,
      };
    };

    return valueAnswer(qname, profile, resolved, describe);
  }

  /**
   * The whole legal value space of a simple type: base, facets, enumeration,
   * union members and list item type, resolved recursively.
   *
   * This is what `enum` cannot answer. `ST_TwipsMeasure` is a union,
   * `ST_Percentage` is a pattern, and the numeric family is bounded by
   * inclusive facets; an agent *writing* OOXML needs the bounds and the
   * pattern, not "it restricts xsd:string".
   */
  function values(qname, {profile = DEFAULT_PROFILE} = {}) {
    const pid = profileId(profile);
    const resolved = resolveToSimpleType(qname, profile);
    if (resolved.found === false) return {query: qname, profile, ...resolved};

    const describe = (target) => {
      if (target.complex) return complexVariant(target, {});
      if (target.symbolId === null) {
        if (target.typeRef === null) {
          const source = externalSource(target.row.vocabulary);
          return {
            type: null,
            message:
              source === null
                ? `${display(target.row)} declares no type, so it has no value space in the schema.`
                : `${display(target.row)} is defined outside ECMA-376, and its type is not ` +
                  `recorded here. Defined in: ${source}`,
            ...(source === null ? {} : {external_source: source}),
          };
        }
        const name = targetName(target);
        return {
          type: name,
          ...viaField(target),
          builtin: true,
          message:
            target.simpleContentOf === undefined
              ? `${display(target.row)} is typed ${name}, an XSD built-in; its value space is the XSD one.`
              : `${display(target.row)} holds ${name} text through ${target.simpleContentOf}, an XSD ` +
                'built-in; its value space is the XSD one.',
        };
      }
      return {
        type: targetName(target),
        ...viaField(target),
        ...describeValueSpace(target.symbolId, pid, 0),
      };
    };

    return valueAnswer(qname, profile, resolved, describe);
  }

  function describeValueSpace(symbolId, pid, depth) {
    if (depth > MAX_DEPTH) return {truncated: true};

    const inherited = baseOf(symbolId, pid);
    const base = inherited?.content_model === 'simpleType' ? inherited : undefined;
    const enumerated = enumValuesOf(symbolId, pid);
    const facets = handle.all(
      'SELECT facet, value FROM simple_type_facets WHERE symbol_id = ? AND profile_id = ? ORDER BY order_index',
      symbolId,
      pid,
    );
    const members = handle.all(
      `SELECT member_kind, member_type_ref, member_symbol_id, order_index FROM union_members
        WHERE symbol_id = ? AND profile_id = ? ORDER BY order_index`,
      symbolId,
      pid,
    );

    const space = {};
    if (base !== undefined) space.base = displayRef(base.base_type_ref);
    if (enumerated.length > 0) space.enumeration = enumerated;
    if (facets.length > 0) {
      space.facets = Object.fromEntries(facets.map((f) => [f.facet, f.value]));
    }
    if (members.length > 0) {
      space[members[0].member_kind === 'list' ? 'list_of' : 'one_of'] = members.map((member) => {
        if (member.member_symbol_id === null)
          return {type: displayRef(member.member_type_ref), builtin: true};
        const symbol = symbolById(member.member_symbol_id);
        return {
          // Anonymous members have no usable name — they are the inline
          // alternatives of a union — so they are described inline instead.
          ...(symbol.is_anonymous === 1 ? {inline: true} : {type: display(symbol)}),
          ...describeValueSpace(member.member_symbol_id, pid, depth + 1),
        };
      });
    }
    if (Object.keys(space).length === 0) space.unconstrained = true;
    return space;
  }

  // ------------------------------------------------------------ namespace ---

  /**
   * URI to vocabulary and back, in both directions, for both profiles.
   *
   * An alias prefix matches here too, and says so: `prefix` keeps reporting what
   * the schemas bind (NULL when they bind nothing), and `aliases` carries the
   * accepted spellings with the citation for each. Folding an alias into
   * `prefix` would make this tool claim the standard mandates a prefix it does
   * not, which is the claim the NULL exists to avoid.
   */
  function namespace(query, {profile = null} = {}) {
    const text = String(query ?? '').trim();
    const matches = [];
    for (const vocabulary of index.all) {
      const aliases = vocabulary.aliasPrefixes;
      const aliasHit = aliases.some((a) => a.prefix === text);
      for (const ns of vocabulary.namespaces) {
        if (profile !== null && ns.profile !== profile) continue;
        if (ns.uri === text || ns.prefix === text || vocabulary.key === text || aliasHit) {
          matches.push({
            vocabulary: vocabulary.key,
            uri: ns.uri,
            prefix: ns.prefix,
            profile: ns.profile,
            ...(aliases.length === 0 ? {} : {aliases}),
            ...externalNote(vocabulary.key),
          });
        }
      }
    }
    if (matches.length === 0) {
      return {
        query: text,
        found: false,
        reason: 'unknown_namespace',
        message: `no namespace, prefix or vocabulary matches "${text}".`,
        known_prefixes: knownPrefixes(),
      };
    }
    return {query: text, found: true, count: matches.length, namespaces: matches};
  }

  // --------------------------------------------------------------- search ---

  /**
   * Substring match on symbol names. **Not semantic, and it says so.**
   *
   * There are no embeddings here by design. That is fine for the real use — an
   * agent asking about OOXML usually already knows the qname and wants the
   * record — but the tool must not imply otherwise, and an empty result must
   * say "no name contains X" rather than returning nothing ambiguously.
   */
  /**
   * @param {string} text
   * @param {{profile?: string, kind?: string | string[] | null, limit?: number}} [options]
   */
  function search(text, {profile = DEFAULT_PROFILE, kind = null, limit = 40} = {}) {
    const pid = profileId(profile);
    const needle = String(text ?? '').trim();
    if (needle === '') {
      return {
        query: needle,
        profile,
        found: false,
        reason: 'empty_query',
        message: 'search needs a substring.',
      };
    }

    // `_` and `%` are LIKE wildcards, and `_` is in nearly every ECMA-376 name
    // (CT_*, ST_*, EG_*). Unescaped, `_Tbl` matched `wholeTbl`. The backslash
    // goes first so the escapes added after it are not escaped again.
    const pattern = needle.replace(/[\\%_]/g, (c) => `\\${c}`);
    const params = [pid, `%${pattern}%`];
    let kindClause = '';
    if (kind !== null) {
      const kinds = [kind].flat();
      kindClause = ` AND s.kind IN (${placeholders(kinds)})`;
      params.push(...kinds);
    }

    const rows = handle.all(
      `SELECT s.id, s.local_name, s.kind, s.parent_symbol_id, s.type_ref, v.key AS vocabulary
         FROM symbols s
         JOIN vocabularies v ON v.id = s.vocabulary_id
         JOIN symbol_profiles sp ON sp.symbol_id = s.id AND sp.profile_id = ?
        WHERE s.local_name LIKE ? ESCAPE '\\' COLLATE NOCASE AND s.is_anonymous = 0${kindClause}
        ORDER BY LENGTH(s.local_name), v.key, s.kind, s.local_name
        LIMIT ?`,
      ...params,
      limit + 1,
    );

    const truncated = rows.length > limit;
    const page = rows.slice(0, limit);
    return {
      query: needle,
      profile,
      match: 'substring, case-insensitive — this is a name search, not a semantic one',
      found: page.length > 0,
      ...(page.length === 0
        ? {message: `no symbol name contains "${needle}".`}
        : {
            count: page.length,
            truncated,
            results: page.map((row) => ({
              qname: display(row),
              kind: row.kind,
              vocabulary: row.vocabulary,
              ...(row.parent_symbol_id === 0 ? {} : {declared_in: declaredInName(row)}),
              ...(row.type_ref === null ? {} : {type: displayRef(row.type_ref)}),
            })),
          }),
    };
  }

  // -------------------------------------------------------- diff_profiles ---

  /**
   * What Transitional adds to Strict for one symbol.
   *
   * Falls out of the profile model for free, and it is a genuinely one-sided
   * comparison: Strict contains no symbol Transitional lacks, verified in the
   * ingest, so every difference is something Transitional adds back for legacy
   * compatibility.
   */
  function diffProfiles(qname) {
    const found = lookup(qname);
    const {rows} = found;
    if (rows.length === 0) {
      return {query: qname, ...notFound(qname, found, DEFAULT_PROFILE)};
    }

    return {
      query: qname,
      found: true,
      count: rows.length,
      symbols: rows.map((row) => {
        const present = symbolProfiles(row.id);
        const shaped = shapeSymbolOf(row);
        const perProfile = {};
        for (const key of present) {
          const pid = profileId(key);
          perProfile[key] = {
            namespace: namespaceOf(row.vocabulary, key)?.uri ?? null,
            children: shaped === null ? [] : childNames(shaped, pid),
            attributes:
              shaped === null ? [] : attributeSet(shaped, pid).list.map((a) => a.qname ?? a.name),
            enumeration: enumValuesOf(row.id, pid),
            union_members: handle
              .all(
                `SELECT member_type_ref FROM union_members
                  WHERE symbol_id = ? AND profile_id = ? ORDER BY order_index`,
                row.id,
                pid,
              )
              .map((m) => displayRef(m.member_type_ref)),
          };
        }

        const missing = PROFILE_KEYS.filter((key) => !present.includes(key));
        return {
          qname: display(row),
          kind: row.kind,
          in_profiles: present,
          ...(missing.length > 0 ? {absent_from: missing} : {}),
          differences: describeDifferences(perProfile, present),
          detail: perProfile,
        };
      }),
    };
  }

  /**
   * The symbol whose content and attributes describe `row`: a type, group or
   * attributeGroup itself, an element's or attribute's type, or null for a
   * name with no such shape.
   */
  const shapeSymbolOf = (row) => {
    if (['complexType', 'group', 'attributeGroup'].includes(row.kind)) return row.id;
    if (row.type_symbol_id === null) return null;
    return symbolById(row.type_symbol_id).kind === 'complexType' ? row.type_symbol_id : null;
  };

  /**
   * Every child a symbol permits, as a set of names, inheritance and groups
   * resolved. A raw edge count misses both: a DrawingML type whose content is
   * one group ref has no edges of its own, so a profile difference inside the
   * group never showed.
   */
  const childNames = (symbolId, pid) => {
    const state = {seenGroups: new Set(), truncated: false};
    const order = flatten(particlesOf(symbolId, pid, state, 0, true));
    return [...new Set(order.map((entry) => entry.qname ?? `any(${entry.wildcard})`))];
  };

  function describeDifferences(perProfile, present) {
    if (present.length < 2) return [`present only in ${present.join(', ')}`];
    const [a, b] = present;
    const notes = [];
    for (const field of ['children', 'attributes', 'enumeration', 'union_members']) {
      const onlyA = perProfile[a][field].filter((v) => !perProfile[b][field].includes(v));
      const onlyB = perProfile[b][field].filter((v) => !perProfile[a][field].includes(v));
      if (onlyA.length > 0) notes.push(`${field} only in ${a}: ${onlyA.join(', ')}`);
      if (onlyB.length > 0) notes.push(`${field} only in ${b}: ${onlyB.join(', ')}`);
    }
    if (perProfile[a].namespace !== perProfile[b].namespace) {
      notes.push('namespace URI differs (expected — the profiles alias the same vocabulary)');
    }
    // Only reachable with one URI for both profiles, which is the packaging
    // vocabularies: OPC was never split into Transitional and Strict.
    return notes.length === 0 ? ['identical, namespace URI included'] : notes;
  }

  return {
    element,
    type,
    children,
    attributes,
    enum: enumValues,
    values,
    namespace,
    search,
    diff_profiles: diffProfiles,
    // Shared with core/explain.mjs, which is a composition of these rather than
    // a second query layer.
    _internal: {handle, index, profileId, lookup, inProfile, display, symbolById, resolveToType},
    close: () => handle.close(),
  };
}
