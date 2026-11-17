# Installing `postking-cli`

## Install

Global install (preferred):

```
npm i -g postking-cli
```

## Ephemeral invocation (no global install)

If the global install fails with permission errors (common in sandboxed agent terminals), invoke via `npx` without installing:

```
npx -p postking-cli@latest pking --version
```

Use `npx -p postking-cli@latest pking <command>` for all subsequent calls when running ephemerally.

## Upgrade

To upgrade to the latest version:

```
npm i -g postking-cli@latest
```
