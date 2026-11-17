# Document parity

## What parity means

Parity means that selected locales serve the same reader need and cover the same factual range. It does not mean word-for-word translation or identical sentence length.

Review these roles in every selected mirror when they exist in the source:

- project identity and plain-language value;
- proof, examples, screenshots, and outputs;
- feature and mechanism explanation;
- installation and first-success path;
- compatibility, limitations, privacy, and security statements;
- documentation navigation, contribution guidance, contact information, and license.

If a role is absent from one locale, determine whether it is intentionally absent or was lost during translation. Restore lost necessary content before acceptance.

## Preserve technical material

Keep the following equivalent unless the user explicitly requests a technical change:

- fenced code blocks and their commands;
- package names, paths, URLs, anchors, version numbers, and product names;
- image and asset targets;
- configuration keys, API names, identifiers, and command-line flags;
- examples that demonstrate the same successful path.

Translate explanatory prose and comments only when that does not alter the executable example. Do not translate identifiers into a different command or path.

## Preserve factual content

Do not invent or silently remove:

- feature claims, supported environments, limitations, or compatibility notes;
- screenshots, outputs, contact links, product links, or license links;
- attribution or author information that exists in the selected source;
- warnings, prerequisites, privacy statements, or security boundaries.

The Skill maintains parity; it does not decide whether a fact is suitable for public release. Route that separate judgment to the user's chosen repository-publication Skill.

## Structural checks

Use the audit script for facts that can be checked deterministically:

- selected locale files exist inside the repository;
- heading-level sequences are aligned;
- fenced-code counts and language markers are aligned;
- local link and image targets exist;
- non-locale content link targets are aligned;
- requested locale-switch links are present.

Use manual review for:

- translation quality and naturalness;
- whether every feature statement still has the same meaning;
- whether prose has accidentally changed a limitation or promise;
- locale-specific image text, screenshots, dates, units, and examples.

A passing structural audit is necessary evidence, not a semantic translation certificate.
