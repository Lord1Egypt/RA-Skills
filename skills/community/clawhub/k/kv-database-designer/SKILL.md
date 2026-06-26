---
name: database-designer
description: Design, analyze, optimize and evolve database schemas. Use when the user asks to design schemas from scratch, choose between SQL and NoSQL engines, analyze or fix an existing schema (normalization, naming, constraints), plan index strategy, generate migration scripts, or interpret EXPLAIN plans.
compatibility: Requires Python 3.8+ for scripts in scripts/.
---

# Database Designer

Convert a design request or existing schema into a structured, validated, production-ready artifact.

## Activation

Use this skill when the user asks to:
- design or review a database schema (DDL, ERD, Prisma, JSON Schema)
- choose a database engine or decide SQL vs NoSQL
- analyze normalization, constraints, naming or data types
- plan an indexing strategy or diagnose slow queries
- generate migration scripts with rollback
- interpret an EXPLAIN plan or diagnose N+1 patterns

## Workflow

1. **Classify** the request: `design` | `analyze` | `index` | `migrate` | `query` | `select-engine`.
2. **Load the relevant reference** for that mode:
   - `design` / `analyze` → `{baseDir}/references/database-design-reference.md`
   - normalization questions → `{baseDir}/references/normalization_guide.md`
   - indexing / EXPLAIN → `{baseDir}/references/index_strategy_patterns.md`
   - engine selection → `{baseDir}/references/database_selection_decision_tree.md`
3. **Run the appropriate script** when the user provides a schema or queries:
   ```bash
   # Analyze schema for issues (normalization, constraints, naming, types)
   python {baseDir}/scripts/schema_analyzer.py --schema=<ddl_file>

   # Suggest index improvements for a query workload
   python {baseDir}/scripts/index_optimizer.py --schema=<ddl_file> --queries=<queries_file>

   # Generate up/down migration scripts
   python {baseDir}/scripts/migration_generator.py --before=<old_schema> --after=<new_schema>
   ```
4. **Formalize the design**: objects, relationships, constraints, normalization level, primary/foreign keys.
5. **Emit the artifact**: DDL, Mermaid ERD, Prisma schema, or JSON Schema — one format unless the user asks for multiple.
6. **Declare trade-offs**: note any denormalization choices, missing constraints, or engine-specific limitations.

## Output Contract

- Open with the dominant design decision or issue found.
- Emit one primary artifact (DDL, ERD, or schema) per response.
- Annotate non-obvious choices (e.g. why a partial index, why a surrogate key).
- Declare `Information Loss` when the target format cannot express a constraint (e.g. CHECK logic in Prisma).
- Close with indexing recommendations and next migration step if applicable.

## Key Rules

- Default to **PostgreSQL** unless the user specifies another engine or the decision tree points elsewhere.
- Default to **3NF** for new schemas; document any intentional deviation and the reason.
- Every generated migration must include a `down` script.
- For destructive changes (DROP COLUMN with data), always recommend a logical backup first.
- Do not generate application-layer connection pool code unless explicitly asked — reference the patterns instead.

## Guardrails

- Do not skip normalization analysis when designing from scratch.
- Do not recommend over-indexing — flag indexes that may hurt write throughput.
- Flag N+1 patterns but do not generate ORM-specific code unless the user's stack is known.
- Stay within schema, index, migration and query scope; for large-scale cross-engine migrations refer to `migration-architect`.

## Self Check

Before emitting any artifact, verify:
- all foreign keys are declared;
- primary key strategy is explicit (surrogate vs natural);
- normalization level is stated and intentional deviations justified;
- migration script has a `down` counterpart;
- no inline example code duplicates what a reference file already covers.
