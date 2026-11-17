# Locale strategy

## Locale matrix

Build a matrix from the user's requested locales and the selected repository files. Locale identifiers are not limited to Chinese; use the user's requested language and the repository's established naming convention.

| Locale | Default path | Mirror path | Status |
| --- | --- | --- | --- |
| en | README.md | README.md | default |
| ja | README.md | README.ja.md | requested |
| fr | README.md | README.fr.md | requested |

Use standard locale forms such as en, ja, zh-CN, zh-Hant, fr-FR, or ar. Preserve an existing filename when it is already clear and linked. Do not rename every localized file merely to impose a new convention.

## Non-English README.md

README.md is the English default entry in the target state. When its current content is not English:

1. identify the current locale from the filename and content;
2. preserve the current content as README.<locale>.md;
3. check existing links and references to the original path;
4. create the English README.md from the preserved factual source;
5. add language-switch links for the confirmed locale set;
6. preview both the English entry and the preserved locale mirror.

Do not silently overwrite the only copy of a non-English README. If the locale cannot be identified with confidence, ask before creating a filename.

## More than two locales

Treat each requested locale as a peer mirror of the same factual document. Do not assume that zh-CN is the only non-English choice or that every repository needs the same locale set.

For every selected document:

- keep the same section responsibilities and factual range;
- retain code, commands, URLs, versions, and asset targets;
- make language-switch links point to all confirmed locale mirrors;
- use the target locale's natural wording without adding locale-specific claims;
- record an intentional divergence before changing structure, assets, or technical facts.

## Locale detection limits

Filename conventions are stronger evidence than a language guess. Content detection is an aid for finding a likely source locale, not proof of the user's desired target language. The agent must show the inferred locale and proposed path before renaming or creating a mirror.

## Language links

Use repository-relative links that resolve from the current document's directory. Keep the switch labels understandable in the current language. Check links in every selected locale when language navigation is part of scope. A document can be audited without adding language links when the user did not request navigation changes.
