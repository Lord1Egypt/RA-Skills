# Action contract

index: files:[relative paths] OR directory; tags optional string list; prune:true removes missing documents from this selected directory index only. Supports UTF-8 TXT/MD/HTML/CSV/JSON, 8MiB per file and 32MiB per batch. search: query, optional tag and limit1..50. list: indexed metadata. remove: id from list; source remains. export: index manifest. Search returns lexical ranking, chunk citations and indexCurrent based on current source hashes. It is not embedding-based semantic search. HTML scripts/styles are excluded. Samples are fictional.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.
