# Contribute an agreed shared improvement

Read this after the user requests or agrees to a PIP improvement. The
[repository](https://github.com/WhiteKiwi/kiwi-design-system) owns its current
development instructions, package configuration, and
[release procedure](https://github.com/WhiteKiwi/kiwi-design-system/blob/main/docs/npm-release.md).
Read applicable repository instructions before editing.

## Start from the consumer's need

Record the installed PIP version, expected and current behavior, and a small
reproduction or use case. Check existing APIs, tokens, issues, and PRs. A useful
component, token, or shared composition can be proposed from one product; no
second consumer is required.

When scope is genuinely new, a proposal can be brief: “This screen needs X, which the current
API cannot express. Adding Y to PIP would solve it without a local fork. I propose
adding Y with an example and regression check, then applying it here.” Wait for
agreement only when that scope has not already been requested or approved.

Do not include product data fetching, business rules, or product-specific props
in a shared API merely to finish one screen. If the user wants the fix to remain
local, follow that scope and explain any temporary workaround's removal condition.

## Implement upstream first

Work in an authorized checkout of the design-system repository. Implement the
shared change there before consuming it in the app. Keep one coherent behavior
change, its documentation, and its checks together. Split larger work into
independently buildable changes, such as a needed token, a component family, and
consumer adoption; link dependent PRs.

| Change | Source to inspect |
| --- | --- |
| Tokens and theme roles | `packages/tokens/src/theme.css` and the design guidelines |
| UI behavior and styles | The appropriate family in `packages/ui/src`, `styles.css`, and public `index.ts` exports |
| API and state documentation | The package README, design contracts, and `apps/docs` specimens/inventory |
| Consumer adoption | App imports, dependencies, lockfile, and affected screens |

Use existing native semantics and tokens. For new primitives, inspect license,
dependencies, keyboard/focus behavior, motion, and fit with PIP. Add a regression
check for the demonstrated problem; a source-string assertion alone does not
validate the behavior. Keep the public catalog about components and standards,
not the agent workflow used to author them.

## Verify the package and the app

Use the Node and pnpm versions declared by the current repository. The workflow
at authoring time uses Node 24+ and pnpm 10.33.0. From its root:

```sh
pnpm install --frozen-lockfile
pnpm check
pnpm release:check
pnpm release:pack
```

These checks build and inspect packages without publishing. Inspect both themes
and relevant interaction states, keyboard flow, focus, reduced motion, and the
changed layout at 320px, 390px, and desktop. The automated contrast and static
rendering checks do not cover all browser behavior or complete app accessibility.

Read the current `dist/npm/release-plan.json` for the exact tarball filenames.
In a temporary branch or isolated consumer checkout, assign their real absolute
paths:

```sh
PIP_TOKENS_TGZ=/absolute/path/to/whitekiwi-tokens-VERSION.tgz
PIP_UI_TGZ=/absolute/path/to/whitekiwi-ui-VERSION.tgz
```

Run only the command for the consumer's existing package manager:

| Package manager | Command |
| --- | --- |
| pnpm | `pnpm add "$PIP_TOKENS_TGZ" "$PIP_UI_TGZ"` |
| Yarn | `yarn add "$PIP_TOKENS_TGZ" "$PIP_UI_TGZ"` |
| npm | `npm install "$PIP_TOKENS_TGZ" "$PIP_UI_TGZ"` |

Preserve the app's lockfile format; do not introduce another package manager.

Token-only apps install only tokens. Record the PIP source revision, tarball
version, consumer revision, and checks run. If consumer access is missing, provide
the reproduction and catalog results and mark actual app verification as pending.

## Review, release, and adoption

Use the consumer task as the completion boundary. After the authorized release,
replace the local implementation, remove obsolete style rules, and verify the
consumer against the published version. Record any remaining adoption as open
with a concrete next action rather than reporting the entire improvement done.

Describe the concrete problem, resulting behavior, public API/token impact,
validation, and consumer follow-up in the PR. Link the actual related PRs; do not
invent a tracking link. Contribution does not require pushing a release tag.

Both library versions move together when a release is authorized. A new `v*` tag
push triggers npm publication; never use it just to test CI. Use the current
release guide for preview and publication, and record publication separately from
merge. Once published, update the consumer's registry versions and lockfile,
verify the app, and remove the workaround and temporary tarball dependencies.
