---
name: senior-data-engineer
description: Design and build scalable data pipelines, ETL/ELT systems, and data infrastructure. Use when designing data architectures, choosing between batch and streaming, building pipelines with Airflow, dbt, Spark, or Kafka, implementing data quality frameworks, modeling dimensional or Data Vault schemas, or troubleshooting pipeline performance and data issues.
compatibility: Requires Python 3.8+ for scripts in scripts/.
---

# Senior Data Engineer

Production-grade data engineering: pipelines, modeling, quality, and DataOps.

## Activation

Use this skill when the user asks to:
- design a data pipeline (batch, streaming, or hybrid)
- choose between Lambda and Kappa architecture, or batch vs streaming
- build ETL/ELT with Airflow, Prefect, Dagster, dbt, or Spark
- implement data quality checks or data contracts
- model data (star schema, snowflake, SCD, Data Vault)
- optimize a slow Spark job, DAG, or warehouse query
- set up data observability, lineage, or incident response

## Workflow

1. **Classify** the request: `pipeline` | `model` | `quality` | `optimize` | `architecture`.
2. **Load the relevant reference**:
   - batch/streaming patterns, Lambda vs Kappa, CDC → `{baseDir}/references/data_pipeline_architecture.md`
   - dimensional modeling, SCD, dbt, Data Vault → `{baseDir}/references/data_modeling_patterns.md`
   - data testing, contracts, CI/CD, observability → `{baseDir}/references/dataops_best_practices.md`
   - end-to-end workflow walkthroughs → `{baseDir}/references/workflows.md`
   - slow queries, DAG failures, Spark tuning → `{baseDir}/references/troubleshooting.md`
3. **Run the appropriate script** when artifacts are provided:
   ```bash
   # Generate pipeline orchestration config (airflow | prefect | dagster)
   python {baseDir}/scripts/pipeline_orchestrator.py generate \
     --type airflow --source postgres --destination snowflake --schedule "0 5 * * *"

   # Validate data quality (freshness, completeness, uniqueness, schema)
   python {baseDir}/scripts/data_quality_validator.py validate \
     --input data/file.parquet --schema schemas/file.json \
     --checks freshness,completeness,uniqueness

   # Analyze and optimize ETL performance
   python {baseDir}/scripts/etl_performance_optimizer.py analyze \
     --query queries/aggregation.sql --engine spark --recommend
   ```
4. **Emit the artifact**: pipeline config, dbt model, schema DDL, quality rules, or architecture diagram.

## Output Contract

- Open with the pipeline classification and dominant bottleneck or design decision.
- Emit one primary artifact per response (DAG, dbt model, schema, quality config).
- For architecture decisions: state the trade-offs of each option before recommending.
- Declare data loss risk explicitly when a pipeline design cannot guarantee exactly-once semantics.
- Close with observability recommendation (what to monitor and at what threshold).

## Key Rules

- Default to **batch** unless sub-minute latency is a stated requirement.
- Default to **dbt + warehouse compute** for <1TB daily; recommend Spark only when justified by volume or complexity.
- Every pipeline must declare: idempotency strategy, error handling, and dead-letter queue approach.
- Data quality checks are non-optional — include them in every pipeline design.

## Guardrails

- Do not generate application-layer code (APIs, web services) — stay within data pipeline scope.
- Do not recommend streaming when batch satisfies the latency requirement; streaming adds operational cost.
- Flag missing idempotency as a HIGH issue; flag missing data quality checks as MEDIUM.
- For cross-engine migration refer to `migration-architect`.

## Self Check

Before emitting any artifact, verify:
- idempotency strategy is stated;
- error handling and retry logic are addressed;
- data quality checks are included or explicitly deferred with a reason;
- the chosen architecture (batch vs stream) matches the stated latency requirement.
