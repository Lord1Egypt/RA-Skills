/**
 * Resolve a validator diagnostic against the schema graph.
 *
 * This is the tool the incumbent cannot ship, because it needs a local graph to
 * answer "and what *would* have been legal here". It is also the loop agents
 * are actually stuck in: a validator says a child is unexpected, and the next
 * question is always "then what may go there, and in what order".
 *
 * ## What it consumes, and why so little
 *
 * Four fields of `ooxml-validate`'s JSON diagnostic:
 *
 *     { id: "Sch_UndeclaredAttribute", type: "Schema",
 *       description: "The 'bogus' attribute is not declared.",
 *       partUri: "/ppt/slides/slide1.xml", xpath: "/p:sld[1]" }
 *
 * Element identity and position come from `xpath`. The violated constraint
 * comes from `id`, a finite Open XML SDK enum. Only the quoted names inside
 * `description` need text handling, and that is a bounded regex per id rather
 * than a grammar.
 *
 * A diagnostic pasted as text is read into the same four fields by
 * `parseDiagnosticText`, so the text form adds an input shape and nothing else.
 *
 * Reading exactly four fields is the deliberate mitigation for a **cross-repo
 * contract**: `ooxml-validate` is pre-1.0 and does not freeze its report shape,
 * so anything outside those four moving is a non-event here. Do not widen this
 * to consume the whole report — `AGENTS.md` says so, and this is the code that
 * paragraph is about.
 *
 * ## What it is not
 *
 * It **consumes** validator output, it does not produce it. No validation
 * happens here, nothing is imported from `ooxml-validate`, and nothing needs it
 * installed — consuming a data shape is not a dependency. The boundary in
 * `AGENTS.md` holds.
 */

import {DEFAULT_PROFILE} from './graph.mjs';

/** The quoted name in an SDK message about an element or an attribute. */
const ELEMENT_NAME = /element '([^']+)'/;
const ATTRIBUTE_NAME = /attribute '([^']+)'/;

/**
 * Diagnostic classes this resolves, and how to read each one.
 *
 * An explicit allowlist, not a `Sch_*` prefix match: the prefix covers plenty
 * of ids that are not about structure, and pretending to resolve one of those
 * would produce a confident answer to a question we did not understand.
 *
 * `extract` pulls the quoted names out of `description`. The Open XML SDK
 * phrases these consistently, but the regexes are anchored loosely on purpose —
 * a missed capture degrades to "here is what is legal here", which is still the
 * useful half.
 *
 * `summary` therefore takes `name` as `string | null` and **every template must
 * handle null**, because a missed capture is a normal outcome rather than an
 * edge case. Substituting a placeholder into the quoted slot is not an option:
 * `The 'it' attribute is not allowed on x:sheet` reads as a real attribute
 * called `it`, which is a confident answer to a question we did not understand.
 * The nameless phrasing also has to match what `resolveLegal` returns — without
 * a name it cannot narrow to one attribute's value space, so those two ids
 * promise the attribute list instead.
 */
const DIAGNOSTICS = {
  Sch_UndeclaredAttribute: {
    finding: 'undeclared_attribute',
    answer: 'attributes',
    extract: /'([^']+)' attribute is not declared/,
    summary: (name, position) =>
      name === null
        ? `An attribute given on ${position} is not allowed there. Its legal attributes are listed below.`
        : `The '${name}' attribute is not allowed on ${position}. Its legal attributes are listed below.`,
  },
  Sch_MissRequiredAttribute: {
    finding: 'missing_required_attribute',
    answer: 'attributes',
    extract: /'([^']+)' attribute is required/,
    summary: (name, position) =>
      name === null
        ? `${position} is missing a required attribute. Every attribute it accepts is listed below, with its use.`
        : `${position} requires the '${name}' attribute. Every attribute it accepts is listed below, with its use.`,
  },
  Sch_AttributeValueDataTypeDetailed: {
    finding: 'invalid_attribute_value',
    answer: 'attribute_values',
    extract: ATTRIBUTE_NAME,
    summary: (name, position) =>
      name === null
        ? `An attribute value on ${position} is outside the value space of its type. Which attribute could not be read from the diagnostic, so every attribute it accepts is listed below, with its type.`
        : `The value given for '${name}' on ${position} is outside its type's value space, shown below.`,
  },
  Sch_InvalidAttributeValue: {
    finding: 'invalid_attribute_value',
    answer: 'attribute_values',
    extract: ATTRIBUTE_NAME,
    summary: (name, position) =>
      name === null
        ? `An attribute value on ${position} is not legal. Which attribute could not be read from the diagnostic, so every attribute it accepts is listed below, with its type.`
        : `The value given for '${name}' on ${position} is not legal. Its value space is shown below.`,
  },
  Sch_UnexpectedElementContentExpectingComplex: {
    finding: 'unexpected_child',
    answer: 'children',
    extract: ELEMENT_NAME,
    summary: (name, position) =>
      name === null
        ? `Something inside ${position} is not legal at that position. The legal content model is below, in order.`
        : `'${name}' is not legal inside ${position} at that position. The legal content model is below, in order.`,
  },
  Sch_UnexpectedElementQNameOrText: {
    finding: 'unexpected_child',
    answer: 'children',
    extract: ELEMENT_NAME,
    summary: (name, position) =>
      name === null
        ? `${position} does not accept the content found there. The legal content model is below, in order.`
        : `${position} does not accept '${name}' there. The legal content model is below, in order.`,
  },
  Sch_IncompleteContentExpectingComplex: {
    finding: 'incomplete_content',
    answer: 'children',
    extract: ELEMENT_NAME,
    summary: (_name, position) =>
      `${position} is missing required content. The content model below shows what is required and in what order.`,
  },
  Sch_EmptyContentExpectingComplex: {
    finding: 'incomplete_content',
    answer: 'children',
    extract: ELEMENT_NAME,
    summary: (_name, position) =>
      `${position} is empty but its content model requires children, listed below.`,
  },
};

/** The Open XML SDK ids this understands, for documentation and tests. */
export const SUPPORTED_DIAGNOSTIC_IDS = Object.keys(DIAGNOSTICS).sort();

/**
 * The most ancestor steps an xpath is walked through. Each step is a full
 * `children()` resolution, and the xpath comes from another program's report,
 * so an unbounded walk would let one diagnostic hold a single-threaded server
 * for as long as its path is long. No real OOXML part nests anywhere near this
 * deep.
 */
export const MAX_PATH_STEPS = 64;

/**
 * The last element step of an XPath, and the trail that led to it.
 *
 * `/p:sld[1]/p:cSld[1]/p:spTree[1]` -> `p:spTree`, with the ancestors kept so
 * the answer can say where it is. Positional predicates are dropped: they
 * identify *which* sibling, which the schema has no opinion about. Beyond
 * `MAX_PATH_STEPS` the leading steps are dropped and `truncated` says so: the
 * trail no longer starts at the document root.
 */
export function parseDiagnosticXPath(xpath) {
  const text = String(xpath ?? '').trim();
  if (text === '') return {steps: [], element: null, truncated: false};
  const all = text
    .split('/')
    .filter((step) => step !== '')
    .map((step) => step.replace(/\[[^\]]*\]/g, '').trim())
    .filter((step) => step !== '' && !step.startsWith('@'));
  // Kept from the end: the last steps are the ones that disambiguate.
  const steps = all.length <= MAX_PATH_STEPS ? all : all.slice(-MAX_PATH_STEPS);
  return {
    steps,
    element: steps.length === 0 ? null : steps[steps.length - 1],
    truncated: steps.length < all.length,
  };
}

/**
 * A diagnostic pasted as text — a log line, a terminal message — read into the
 * same four fields the JSON form carries.
 *
 * The text has no grammar, so this recovers what it can and leaves the rest
 * out: a `Sch_*` id, the longest run of `/prefix:name[n]` steps as the xpath,
 * and a `.xml` part URI. The whole text stays the `description`, because the
 * per-id regexes already find quoted names inside a longer message. Nothing
 * here throws: an unrecovered id or position degrades through
 * `explainDiagnostic` exactly as a structured diagnostic missing them would.
 *
 * @param {string} text
 * @returns {{id?: string, description: string, partUri?: string, xpath?: string}}
 */
export function parseDiagnosticText(text) {
  const description = String(text ?? '').trim();
  const id = /\bSch_[A-Za-z]+\b/.exec(description)?.[0];
  // Not preceded by a word or URL character: the namespace URI in
  // `'http://…/2006/main:bogus'` must not read as a one-step path.
  const xpath = [
    ...description.matchAll(/(?<![\w./:-])(?:\/@?[A-Za-z_][\w.-]*:[A-Za-z_][\w.-]*(?:\[\d+\])?)+/g),
  ]
    .map((match) => match[0])
    .sort((a, b) => b.length - a.length)[0];
  const partUri = /(?<![\w:/])\/[\w.-]+(?:\/[\w.-]+)*\.xml\b/.exec(description)?.[0];
  return {
    ...(id === undefined ? {} : {id}),
    description,
    ...(partUri === undefined ? {} : {partUri}),
    ...(xpath === undefined ? {} : {xpath}),
  };
}

/**
 * @param {{id?: string, description?: string, partUri?: string, xpath?: string}} diagnostic
 */
export function explainDiagnostic(graph, diagnostic, {profile = DEFAULT_PROFILE} = {}) {
  const id = diagnostic?.id ?? null;
  const description = diagnostic?.description ?? '';
  const {steps, element, truncated} = parseDiagnosticXPath(diagnostic?.xpath);

  const base = {
    diagnostic: {
      id,
      part: diagnostic?.partUri ?? null,
      xpath: diagnostic?.xpath ?? null,
      description: description === '' ? null : description,
    },
    profile,
    position: {path: steps, element, truncated},
  };

  if (element === null) {
    return {
      ...base,
      resolved: false,
      reason: 'no_position',
      message:
        'The diagnostic carries no xpath, so there is no position to resolve. ' +
        'Pass the `xpath` field from the validator report.',
    };
  }

  const known = id !== null && Object.hasOwn(DIAGNOSTICS, id);
  const spec = known ? DIAGNOSTICS[id] : null;
  const named = spec?.extract.exec(description)?.[1] ?? null;

  // An unrecognised id is not an error. Answering "I do not resolve this class,
  // but here is what is legal at that position" is this part's own
  // absent-is-not-prohibited rule applied to `explain` itself: it degrades into
  // a useful answer rather than a dead end.
  const answer = spec?.answer ?? 'children';
  const legal = resolveLegal(graph, answer, element, named, profile, steps);

  return {
    ...base,
    resolved: known,
    ...(known
      ? {
          finding: {kind: spec.finding, ...(named === null ? {} : {name: named})},
          message: spec.summary(named, element),
        }
      : {
          reason: id === null ? 'no_id' : 'unrecognised_id',
          message:
            `${id === null ? 'No diagnostic id was given' : `"${id}" is not a diagnostic class this resolves`}` +
            `, so the finding is not interpreted. What the schema allows at ${element} is below.` +
            (id === null ? '' : ` Recognised ids: ${SUPPORTED_DIAGNOSTIC_IDS.join(', ')}.`),
        }),
    legal,
  };
}

/** `w:firstLine` and `firstLine` name the same attribute; the schema stores the local part. */
const localPart = (name) => (name === null ? null : name.slice(name.indexOf(':') + 1));

/**
 * Narrow an ambiguous name using the ancestor chain the xpath already gave us.
 *
 * This is where `explain` beats calling `children` directly. `w:pPr` has three
 * content models in wml depending on where it is declared, so `children('w:pPr')`
 * has to return all three. But a diagnostic says
 * `/w:document/w:body/w:p/w:pPr` — and a `pPr` inside a `w:p` is `CT_PPr`, no
 * ambiguity at all. Walking the path down from the root resolves it.
 *
 * Returns the winning variant, or null when the walk cannot decide, in which
 * case the caller falls back to reporting every variant rather than guessing.
 */
function narrowByPath(result, steps, graph, profile) {
  if (result.ambiguous !== true || steps.length < 2) return null;
  const parent = steps[steps.length - 2];

  // Which type does the parent step resolve to? Walk from the root so that an
  // ambiguous ancestor does not silently pick the wrong branch either. Each
  // step's content model is carried to the next, which finds its child in it.
  /** @type {any} */
  let current = null;
  for (const [i, step] of steps.slice(0, -1).entries()) {
    current =
      i === 0 ? graph.children(step, {profile}) : childModelOf(current, step, graph, profile);
    if (current === null || current.found !== true || current.ambiguous === true) return null;
  }
  if (current === null) return null;

  const declaringType = current.type;
  const match = result.variants.find((variant) =>
    (variant.applies_when_declared_in ?? []).includes(declaringType),
  );
  return match === undefined ? null : {...match, narrowed_by: `${parent} is ${declaringType}`};
}

/** The content model of `childName` as declared inside the `parent` content model. */
function childModelOf(parent, childName, graph, profile) {
  const child = parent.order.find((entry) => entry.qname === childName);
  if (child === undefined || child.type === undefined) return null;
  return graph.children(child.type, {profile});
}

/**
 * A `children` or `attributes` answer at a position, narrowed by the ancestor
 * chain where it can be.
 *
 * Attributes need it as much as content models do: `pageSetup` is
 * `CT_PageSetup` on a worksheet and `CT_CsPageSetup` on a chartsheet, with
 * *different attribute sets*, so answering from whichever variant sorted first
 * is a confidently wrong answer about a real spreadsheet. The diagnostic's
 * xpath says `/x:worksheet/…`, which settles it.
 *
 * @param {'children' | 'attributes'} tool
 */
function narrowedAt(graph, tool, element, profile, steps) {
  const result = graph[tool](element, {profile});
  const narrowed = narrowByPath(result, steps, graph, profile);
  if (narrowed === null) return result;
  return {query: result.query, profile: result.profile, found: true, ...narrowed};
}

/** Compose the existing tools rather than querying again — one query layer, not two. */
function resolveLegal(graph, answer, element, named, profile, steps = []) {
  if (answer === 'attributes') {
    return {kind: 'attributes', ...narrowedAt(graph, 'attributes', element, profile, steps)};
  }
  if (answer === 'attribute_values') {
    const attributes = narrowedAt(graph, 'attributes', element, profile, steps);
    if (attributes.found === true && named !== null) {
      // Narrow to the attribute the diagnostic actually named, and resolve its
      // type's value space — the bounds and pattern are the answer, not the
      // type's name.
      const lists = attributes.variants ?? [attributes];
      const wanted = localPart(named);
      let sharedName = false;
      for (const list of lists) {
        // The validator writes a qualified attribute prefixed (`w:firstLine`,
        // `r:id`) and an unqualified one bare (`id`), which is exactly the
        // attribute's `qname ?? name`. Falling back to the local part keeps a
        // differently-prefixed spelling working, but only when the local part
        // names one attribute: `id` and `r:id` share it on a slide list entry.
        const candidates = list.attributes.filter((a) => a.name === wanted);
        const match =
          candidates.find((a) => (a.qname ?? a.name) === named) ??
          (candidates.length === 1 ? candidates[0] : undefined);
        if (match === undefined && candidates.length > 1) sharedName = true;
        if (match !== undefined && match.type !== null && match.type.builtin === false) {
          return {
            kind: 'attribute_values',
            attribute: match,
            on: list.type,
            values: graph.values(match.type.qname, {profile}),
          };
        }
        if (match !== undefined) {
          return {kind: 'attribute_values', attribute: match, on: list.type, values: null};
        }
      }
      return {
        kind: 'attributes',
        note: sharedName
          ? `${element} has more than one attribute named '${wanted}', and '${named}' does not pick one. Each is listed below with its qname.`
          : `${element} has no attribute named '${named}' at all — check the name before the value.`,
        ...attributes,
      };
    }
    return {kind: 'attributes', ...attributes};
  }

  return {kind: 'children', ...narrowedAt(graph, 'children', element, profile, steps)};
}
