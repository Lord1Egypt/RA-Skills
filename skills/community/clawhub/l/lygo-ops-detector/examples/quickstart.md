# Ops Detector quickstart (v1.4.0)

```bash
python scripts/self_check.py

python scripts/lygo_ops_detector.py --text "Trust the experts — settled science. Wake up sheeple." --json

python scripts/lygo_ops_detector.py --text-file ./snippet.txt --i-consent --json

python scripts/lygo_ops_detector.py --text "I'm based in the United States. It's on you to prove it." --public-meta "{\"account_based_in\":\"Nigeria\",\"claimed_location\":\"United States\",\"location_accurate\":false}" --json

python scripts/lygo_ops_detector.py --show-boundaries

python scripts/eval_ops_detector.py tests/labeled_discourse_suite.json --sweep
```

`--public-meta` is weighted **context**. A country label alone does not clear 0.65. Named incidents need an `https://` source URL.

Look for `flame_enemy_hints` in JSON (`half_truth_pack`, `authority_shield`, `saturation_flood`).  
Then gate authority with:

```bash
python ../lygo-flame-ward/scripts/flame_cli.py ingest-gate --text "..."
```
