# AI-DFE — Whitepaper

**Package:** AI-DFE — AI-Driven Data Fabric
**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

---

## The problem with scattered output

A mature AI-* family produces an enormous amount of valuable, structured thinking — initiation packages, architecture decisions, backlogs, design systems, risk registers, compliance state. But it lives as human-readable markdown spread across per-project role folders. That is exactly right for the humans who edit it, and exactly wrong for anything that needs the data programmatically.

The moment you want a dashboard, a portfolio roll-up, or a "what's the status of project X?" answer, you hit the same wall: the consumer has to know where every file lives and how to parse it. Each new consumer re-implements that knowledge, and every change to a package's output layout silently breaks them.

## The data-fabric idea

A data fabric is a layer that sits between producers and consumers and owns the data lifecycle end to end: it knows where raw data lives, it shapes it into what consumers need, and it serves it from one place. Producers keep producing in their own way. Consumers stop caring where anything lives — they ask the fabric.

AI-DFE applies that idea to the family. It owns one folder, `{family}-ws/data/`, and is its sole writer. Everything else only reads.

## Three contracts, two layers

DFE is built on three contracts:

1. **The package contract** — each package ships a `SOURCE_MAP.md` (where its raw data lives) and a `{pkg}-data.schema.json` (the shape DFE produces for it). The package is the authority on its own data.
2. **The consumer contract** — each consumer drops a DEMAND file declaring what it needs. It never reaches into source files.
3. **The registry contract** — `REGISTRY.json` is the one path every consumer knows. Read the registry, get your file's path, read clean JSON.

And two layers of transformation:

- **Layer 1 (gather):** scattered sources → one faithful `{pkg}-data.json` per package.
- **Layer 2 (shape):** per-package JSON → consumer-tailored outputs. Consumer views are always assembled from Layer 1, never from raw sources again — so there is exactly one place each fact is extracted.

## Why an engine, not a script

DFE is a continuous adaptive engine, not a one-shot generator, because the data layer is never "done." Projects advance, packages re-run, and consumers come and go. DFE uses a discover-once, monitor-continuously pattern: it pays the cost of understanding a package's interface once, caches it, then rides cheap timestamp checks until something actually changes.

## Peers, not hierarchy: FLO and DFE

The family already has a nervous system — AI-FLO, the router. DFE is its complement. FLO decides *what happens next*; DFE decides *where data lands and what shape it takes*. They never collide: FLO writes only routing metadata, DFE writes only the data surface. DFE even reads FLO's own state to publish `flo-data.json`, exactly as it reads every other package. Two engines, two territories, one coherent system.

## Governance without hooks

DFE governs by architecture, not enforcement machinery. Because it is the sole writer of `data/`, the data surface is trustworthy by construction. A schema sits behind every file. A report-only agent (`DFA__`) audits conformance, freshness, and registry consistency on demand. A family-level integrity invariant lets the workspace's governance scanner confirm that every data file has both a schema and a manifest entry. No IDE hooks required.

## The result

Install DFE and the family stops being a pile of folders and becomes a queryable data surface. Build a dashboard against `REGISTRY.json` once and it keeps working as projects evolve. Ask for portfolio status and there is one component that knows. *Fabric it.*
