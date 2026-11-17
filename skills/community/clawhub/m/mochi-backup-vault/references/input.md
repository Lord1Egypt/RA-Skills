# Action contract

snapshot:id unique,directory workspace-relative,exclude optional glob list. 10000 files,64MiB/file,256MiB/snapshot. Vault must stay outside selected source directory. Immutable content blobs are deduplicated by SHA256; every source is rechecked after capture. list; verify:id; compare:left/right snapshot IDs; restore:id,destination new workspace directory; export:id outputs manifest. There is no retention deletion or in-place restore. A live database or continually changing file needs its own application-consistent backup. Snapshot storage is local and private, not encrypted cloud storage.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
