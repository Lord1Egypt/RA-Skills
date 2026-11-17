---
name: ooxml-lookup
description: >-
  Use when writing, editing or debugging the XML inside a .docx, .xlsx or .pptx
  and you need to know what the OOXML schema allows: which children an element
  takes and in what order, its attributes, their legal values, or what a
  schema validation error means.
---

# ooxml-lookup

One CLI over a local SQLite copy of the ECMA-376 schema. No network, no
install. Run it from the skill directory:

```bash
node scripts/ooxml.mjs <command> <name> [--profile strict] [--compact]
```

Every command prints JSON on stdout and nothing else.

## Commands

| Command | Answers |
| --- | --- |
| `element <name>` | What a name is: kind, type, namespace, where it is declared |
| `type <name>` | A complexType or simpleType: derivation and shape |
| `children <name>` | What may go inside, in order, with cardinality |
| `attributes <name>` | Attributes, with inherited ones and attributeGroups expanded |
| `enum <name>` | Enumeration values of a simple type |
| `values <name>` | The whole value space: facets, patterns, unions |
| `namespace <uri\|prefix>` | Namespace URI to prefix, or prefix to vocabulary |
| `search <substring>` | Symbols whose name contains the substring |
| `diff <name>` | How Transitional and Strict differ for one symbol |
| `explain <json\|text>` | What was legal where a validation error points |
| `sql <select>` | Read-only SQL against the graph |

`min`/`max` of `-1` means unbounded.

## The usual loop

Start from the element, then ask about its type.

```bash
node scripts/ooxml.mjs element w:ind          # -> type w:CT_Ind
node scripts/ooxml.mjs attributes w:CT_Ind    # firstLine is s:ST_TwipsMeasure
node scripts/ooxml.mjs values s:ST_TwipsMeasure
```

The last one returns a union of an unsigned integer and a pattern
`[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)`. So `w:firstLine="720"` (twips) and
`w:firstLine="0.5in"` are both legal.

`children` returns the content model twice. `order` is a flat list in schema
order and answers "what goes here". `tree` keeps the nested
sequence/choice/all structure. Read `tree` when it matters whether two children
are alternatives or both allowed.

## Explaining a validation error

Pass one diagnostic as JSON. The fields read are `id`, `description`, `partUri`
and `xpath`.

```bash
node scripts/ooxml.mjs explain '{"id":"Sch_UndeclaredAttribute",
  "description":"The '\''bogus'\'' attribute is not declared.",
  "xpath":"/w:document[1]/w:body[1]/w:p[1]/w:pPr[1]/w:ind[1]"}'
```

A whole report works too, and the first diagnostic is used. Pasted text also
works:

```bash
node scripts/ooxml.mjs explain "Sch_UndeclaredAttribute: The 'bogus' attribute
  is not declared. at /w:document[1]/w:body[1]/w:p[1]/w:pPr[1]/w:ind[1]"
```

Include the xpath whenever you have it. Without it there is no position to
answer for, and with it the ancestors pick the right content model when a name
has several.

## Things that will bite you

- **Check the profile.** Answers default to Transitional, which is what Word,
  Excel and PowerPoint write. If the document declares
  `purl.oclc.org/ooxml/...` namespaces, pass `--profile strict`.
- **Check for `variants` before reading a result.** A bare or shared name comes
  back with `ambiguous:true` and one variant per meaning. `ST_Direction` is
  `ltr|rtl` in wml and `horz|vert` in pml. `w:tblPr` has different types
  depending on the parent, and each variant carries `applies_when_declared_in`.
  Qualify names (`s:ST_Percentage`, not `ST_Percentage`) to avoid most of this.
- **An empty answer is often correct.** `attributes w:CT_Tbl` returns
  `found:true, count:0` because wml puts table properties in child elements.
- **`search` matches substrings of names.** `search tblBorders` works. `search
  "table border"` does not.

## Names

Write a name however you have it: `w:tblPr`, `wml:tblPr`,
`{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblPr`, or bare
`tblPr`. Prefixes are the conventional ones (`w`, `a`, `p`, `s`, `m`, `r`, `v`,
`x`, `c`, `xdr`, `wp` and so on). Answers come back in canonical spelling, so
`element x:worksheet` replies `sml:worksheet`.

Package parts:

- `[Content_Types].xml` and `.rels` have no prefix. Use the bare name (`Types`,
  `Relationship`) or the vocabulary key (`opc-contentTypes:Override`).
- `cp:coreProperties` resolves directly. Its `dc:` and `dcterms:` children
  answer with `type:null` and an `external_source`, because Dublin Core is
  defined outside ECMA-376. Read `null` as "not recorded here".

## Direct SQL

Use the subcommands where they fit. They resolve inheritance and expand group
references, and a raw query does neither. When they do not fit:

```bash
node scripts/ooxml.mjs sql "SELECT local_name FROM symbols
  WHERE kind='complexType' AND local_name LIKE 'CT_Tbl%'"
```

Tables: `profiles`, `vocabularies`, `namespaces`, `prefix_aliases`, `symbols`,
`symbol_profiles`, `compositors`, `child_edges`, `group_edges`, `attr_edges`,
`inheritance_edges`, `enums`, `simple_type_facets`, `union_members`.

- `symbols` is keyed on vocabulary and has no profile column. Every edge table
  has one.
- `symbols.parent_symbol_id` is `0` for a global declaration, not NULL.
- Results cap at `--limit` rows (default and max 200). `truncated:true` means
  page with `LIMIT … OFFSET …`.
