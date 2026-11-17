# Muse approval scope

`scripts/muse-image.py` must not infer permissions from approval descriptions.
Its policy permits only the label `Allow once`, exactly one image-save operation,
and exactly one literal path equal to this run's `remote` output after the existing
`canonical_output_path` normalization (`~`/`~hatch`, `.`/`..`, existing symlinks).
Different filenames or directories, escaping traversal, extra paths or arguments,
compound operations, command separators or substitutions, reads and network access
are refused. Directory creation is no longer an exception: the prompt expressly
forbids it, and no captured run establishes that it is required.

## Evidence checked on 2026-11-17

- The existing extractor and comments establish Allow/Deny buttons and an ancestor
  containing the description. They do not establish a separate tool name, path or
  argument element, request data attribute, code block, or complete card grammar.
- Local saved `batch-results.json` files under `.image-gen-work` include Muse
  attempts, but no `approved` payloads. The saved Muse upload fixtures checked on
  this machine contain composer and user-message DOM, not approval cards.
- A prior session record says the auto-click path never encountered a real
  approval card after implementation. The previous tests' `write file ...` and
  `mkdir ...` strings are synthetic policy examples, not captured Muse requests.
- Read-only searches of likely output/log locations and local session logs found
  no captured approval request that could establish an operation/path layout or
  a strict whole-card grammar. Some large document-directory searches timed out;
  this is not proof that no sample exists anywhere on the machine.

No verified live card decoder is therefore enabled. `APPROVALS` returns the
observed button label, containing `detail`, and `controls` (actual button labels).
Its `request` is always null. Every live approval card stops the job through the
existing RuntimeError path with an explicit "shape was not recognized ... was not
clicked" error. This includes legitimate save requests. Jobs without approval
cards continue; prompting, uploads, downloads, renaming and timeouts are unchanged.

## Internal policy representation

`scoped_save_approval(approval, remote)` accepts an internal normalized request,
not an asserted Muse wire format:

```json
{
  "label": "Allow once",
  "detail": "diagnostic text only",
  "request": {
    "operation": "save_image",
    "paths": ["/home/hatch/workspace/imagegen-swarm/img-example.png"]
  }
}
```

The request must have exactly those two fields. The operation must be
`save_image`; the path list must contain one nonempty literal path, with no
whitespace, quotes or shell syntax, matching the trusted `remote`. Detail text
never supplies permission. Synthetic normalized requests test the policy and
wait loop; they do not demonstrate live Muse auto-approval support.

Before enabling a live decoder, capture a real approval card without credentials
and add a sanitized fixture. Derive selectors or a strict whole-card grammar from
that evidence. Account for the entire request and every argument; a tool title,
summary, or selected subset of a compound request is insufficient. Missing,
unknown or additional fields and layout changes must still fail closed. Do not
populate `request` by keyword matching, guessing data attributes or parsing an
unverified JSON/code block. Keep the output JSON shape and `approved` detail-string
list; record a detail only after that card is clicked.
