# Muse approval scope

The cloud save directory defaults to `/home/hatch/workspace/image-gen` with the legacy browser
profile and `/home/hatch/workspace/imagegen-swarm` otherwise. `IMAGE_GEN_MUSE_REMOTE_DIR` accepts an
absolute directory below `/home/hatch/` with characters `[A-Za-z0-9_./-]` and no `..`.
Create the cloud directory first on a new environment or handle the directory creation
approval manually; the script always refuses directory-creation cards.

Default and `IMAGE_GEN_MUSE_APPROVAL=legacy` evaluate old-style text cards. The button must
be exactly `Allow once`. The card must contain at least one path, and every parsed path
must match this run's exact output PNG after cloud-home expansion and canonicalization.
Parent traversal, other paths, directory creation, command keywords and shell
metacharacters cause refusal. A rejected decoded request cannot use the text policy.
The script records the detail text of each clicked card in `approved`.

`IMAGE_GEN_MUSE_APPROVAL=strict` requires a decoded `save_image` with one literal path for the
exact output. The current extractor leaves `request` null, so strict mode refuses live text cards.
Refusals report `approval_refused`. A stalled turn with no approvable card or completed reply
reports `approval_card_timeout` after 75 seconds. A completed reply without the output reports
`no_image`.

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
Its `request` is always null. The exact-file fallback is tested with old-style fixtures.
In a live test on 2026-11-17, three Muse generations completed without showing an approval card.

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
whitespace, quotes or shell syntax, matching the trusted `remote`. The structured policy does not consult detail text. Synthetic normalized requests test the policy and
wait loop; they do not demonstrate that a live Muse card can be decoded or clicked.

Before enabling a live decoder, capture a real approval card without credentials
and add a sanitized fixture. Derive selectors or a strict whole-card grammar from
that evidence. Account for the entire request and every argument; a tool title,
summary, or selected subset of a compound request is insufficient. Missing,
unknown or additional fields and layout changes must still fail closed. Do not
populate `request` by keyword matching, guessing data attributes or parsing an
unverified JSON/code block. Keep the output JSON shape and `approved` detail-string
list; record a detail only after that card is clicked.
