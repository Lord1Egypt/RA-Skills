# Known Use Cases (KUC)

Total: **60**

## `KUC-101`
**Source**: `zavod/zavod/cli/etl.py`

Automates the extraction, transformation, and loading of data from external sources into the OpenSanctions data store with optional validation and data clearing.

## `KUC-103`
**Source**: `zavod/zavod/cli/wd_up.py`

Interactively reviews and applies Wikidata updates to OpenSanctions datasets, allowing manual curation of proposed entity matches.

## `KUC-104`
**Source**: `zavod/zavod/cli/util.py`

Loads dataset statements from the archive into a SQL database for querying and analysis, with configurable batch sizes.

## `KUC-106`
**Source**: `zavod/zavod/cli/dedupe.py`

Generates deduplication candidates by cross-referencing entities across datasets using configurable blocking strategies and matching algorithms.

## `KUC-107`
**Source**: `zavod/zavod/cli/archive.py`

Manages dataset versions in the archive, tracking publication history and maintaining version lineage for reproducibility.

## `KUC-108`
**Source**: `datasets/_analysis/ann_pep_positions/test_analyzer.py`

Analyzes politically exposed persons (PEP) positions to determine influence levels and occupancy status across government roles.

## `KUC-109`
**Source**: `datasets/ba/companies/test_crawler.py`

Cleans company names by removing patterns like 'dissolved', 'liquidated' and splitting full/short names for consistent entity representation.

## `KUC-110`
**Source**: `contrib/test_index.py`

Validates dataset index files to ensure proper structure, type assignments, and collection/source/external relationships.

## `KUC-111`
**Source**: `zavod/zavod/tests/test_entity.py`

Core functionality for creating, populating, and managing entity objects with schema validation and property management.

## `KUC-112`
**Source**: `zavod/zavod/tests/test_store.py`

Manages persistent storage and retrieval of entities with support for views, external data, and entity state tracking.

## `KUC-113`
**Source**: `zavod/zavod/tests/test_tune.py`

Optimizes and tunes extraction models (e.g., name extraction) by comparing results and validating performance.

## `KUC-114`
**Source**: `zavod/zavod/tests/test_archive.py`

Publishes dataset artifacts to the archive backend, managing file resources and version tracking for releases.

## `KUC-115`
**Source**: `zavod/zavod/tests/test_dataset.py`

Defines and manages dataset metadata including HTTP settings, naming rules, and schema configurations.

## `KUC-116`
**Source**: `zavod/zavod/tests/test_logs.py`

Redacts sensitive information from logs to protect confidential data while maintaining operational visibility.

## `KUC-117`
**Source**: `zavod/zavod/tests/test_assertions.py`

Defines and validates data quality assertions such as minimum entity counts, property value requirements, and schema constraints.

## `KUC-118`
**Source**: `zavod/zavod/tests/test_context.py`

Manages the crawling context including entity creation, ID generation, URL handling, and issue logging during data extraction.

## `KUC-119`
**Source**: `zavod/zavod/tests/test_validate.py`

Executes data validators that check for dangling references, self-references, empty entities, and assertion compliance.

## `KUC-120`
**Source**: `zavod/zavod/tests/test_publish.py`

Orchestrates the complete dataset publishing workflow including crawling, storage, export, and archive publication.

## `KUC-121`
**Source**: `zavod/zavod/tests/test_dedupe.py`

Resolves duplicate entities by managing resolver edges, making merge decisions, and handling cluster operations.

## `KUC-122`
**Source**: `zavod/zavod/tests/test_cli.py`

Executes CLI commands for crawling, exporting, validating, and managing datasets through the command-line interface.

## `KUC-123`
**Source**: `zavod/zavod/tests/tools/test_export_catalog.py`

Exports dataset catalog information including collection hierarchies and cross-references to index files.

## `KUC-124`
**Source**: `zavod/zavod/tests/tools/test_load_db.py`

Bulk loads dataset statements into a SQL database with batching support for efficient large-scale data ingestion.

## `KUC-125`
**Source**: `zavod/zavod/tests/tools/test_dump_file.py`

Dumps dataset entities with resolved canonical IDs to files, handling merged entities and deduplication state.

## `KUC-126`
**Source**: `zavod/zavod/tests/exporters/test_statistics.py`

Exports dataset statistics including entity counts, schema distributions, country coverage, and target counts.

## `KUC-127`
**Source**: `zavod/zavod/tests/exporters/test_delta.py`

Exports incremental changes between dataset versions, tracking additions, modifications, and deletions.

## `KUC-128`
**Source**: `zavod/zavod/tests/exporters/test_securities.py`

Exports securities/financial instrument data including ISINs, tickers, and company identifiers in standardized formats.

## `KUC-129`
**Source**: `zavod/zavod/tests/exporters/test_metadata.py`

Exports dataset metadata and catalog information to index files for discovery and resource listing.

## `KUC-130`
**Source**: `zavod/zavod/tests/exporters/test_exporters.py`

Exports entities in multiple formats including FollowTheMoney JSON, CSV, nested JSON, and Senzing formats.

## `KUC-131`
**Source**: `zavod/zavod/tests/exporters/test_nested.py`

Exports target entities with nested relationships in a hierarchical JSON format preserving entity associations.

## `KUC-132`
**Source**: `zavod/zavod/tests/exporters/test_senzing.py`

Exports entities in Senzing G2 format with standardized entity records for entity resolution systems.

## `KUC-133`
**Source**: `zavod/zavod/tests/exporters/test_maritime.py`

Exports maritime vessel data including IMO numbers, vessel types, and ownership information.

## `KUC-134`
**Source**: `zavod/zavod/tests/integration/test_edges.py`

Detects and manages entity relationships and edges in the knowledge graph for ownership and association tracking.

## `KUC-135`
**Source**: `zavod/zavod/tests/runtime/test_resources.py`

Manages dataset resources including downloaded files, checksums, and resource metadata tracking.

## `KUC-136`
**Source**: `zavod/zavod/tests/runtime/test_loader.py`

Dynamically loads dataset entry point functions for custom crawling and processing logic.

## `KUC-137`
**Source**: `zavod/zavod/tests/runtime/test_issues.py`

Logs and tracks issues encountered during crawling including warnings, errors, and entity-specific problems.

## `KUC-138`
**Source**: `zavod/zavod/tests/runtime/test_timestamps.py`

Indexes and tracks entity timestamps for first_seen, last_seen, and statement-level temporal tracking.

## `KUC-139`
**Source**: `zavod/zavod/tests/stateful/test_positions.py`

Categorizes political positions by occupancy status (current, former, unknown) and determines influence levels.

## `KUC-140`
**Source**: `zavod/zavod/tests/stateful/test_review.py`

Manages review workflows for human-in-the-loop data validation with source tracking and acceptance workflows.

## `KUC-141`
**Source**: `zavod/zavod/tests/enrich/test_local_enricher.py`

Enriches entities with additional data from local enrichment datasets based on configurable matching rules.

## `KUC-142`
**Source**: `zavod/zavod/tests/enrich/test_enrichment.py`

Enriches entities with data from external enricher services through matching and expansion operations.

## `KUC-143`
**Source**: `zavod/zavod/tests/extract/test_names.py`

Extracts and evaluates name components from unstructured text with feedback-based metric scoring.

## `KUC-144`
**Source**: `zavod/zavod/tests/extract/test_zyte_api.py`

Fetches HTML, JSON, and text content from websites using the Zyte API with browser rendering support.

## `KUC-145`
**Source**: `zavod/zavod/tests/helpers/test_identification.py`

Creates identification documents (passports, licenses) linked to entities with number validation.

## `KUC-146`
**Source**: `zavod/zavod/tests/helpers/test_xml.py`

Removes XML namespaces from parsed documents to simplify element selection and processing.

## `KUC-147`
**Source**: `zavod/zavod/tests/helpers/test_pdf.py`

Extracts tabular data from PDF documents with configurable page settings and border detection.

## `KUC-148`
**Source**: `zavod/zavod/tests/helpers/test_sanctions.py`

Creates sanction list entries linked to entities with program identification and authority information.

## `KUC-149`
**Source**: `zavod/zavod/tests/helpers/test_dates.py`

Parses and extracts dates from various formats with month replacement and date application utilities.

## `KUC-150`
**Source**: `zavod/zavod/tests/helpers/test_numbers.py`

Applies consistent number formatting to entity properties including unit suffixes and decimal handling.

## `KUC-151`
**Source**: `zavod/zavod/tests/helpers/test_securities.py`

Creates financial security entities with ISIN validation and country code extraction.

## `KUC-152`
**Source**: `zavod/zavod/tests/helpers/test_cryptos.py`

Extracts cryptocurrency wallet addresses (BTC, ETH, TRON) from unstructured text for blockchain analysis.

## `KUC-153`
**Source**: `zavod/zavod/tests/helpers/test_change.py`

Detects changes in files and URLs by comparing content against expected hashes.

## `KUC-154`
**Source**: `zavod/zavod/tests/helpers/test_html.py`

Extracts tabular data from HTML documents using XPath selectors with header detection.

## `KUC-155`
**Source**: `zavod/zavod/tests/helpers/test_addresses.py`

Creates standardized address entities from component parts with country code resolution.

## `KUC-156`
**Source**: `zavod/zavod/tests/helpers/test_text.py`

Processes unstructured text with multi-split delimiters, bracket removal, and empty value filtering.

## `KUC-157`
**Source**: `zavod/zavod/tests/helpers/test_positions.py`

Creates political position entities with topics, dates, and organizational affiliations.

## `KUC-158`
**Source**: `zavod/zavod/tests/helpers/test_excel.py`

Parses Excel files (.xls and .xlsx) with cell type detection and date conversion.

## `KUC-159`
**Source**: `zavod/zavod/tests/extract/names/test_clean.py`

Handles name components with language tagging and multi-value management for person names.

## `KUC-160`
**Source**: `zavod/zavod/tests/helpers/names/test_names.py`

Applies parsed names to entities with support for first/last names, aliases, and review workflow integration.

## `KUC-161`
**Source**: `zavod/zavod/tests/helpers/names/test_regularity.py`

Checks name regularity against configured rules including character filters, null word detection, and length validation.

## `KUC-162`
**Source**: `zavod/zavod/tests/helpers/names/test_derive_originals.py`

Maps extracted name values back to original source values when names contain multiple variants.
