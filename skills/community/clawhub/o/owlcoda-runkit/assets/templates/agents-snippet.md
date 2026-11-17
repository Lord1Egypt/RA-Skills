## OwlCoda RunKit

- Treat `.owlcoda/runkit/` as this project's execution truth, not as product source.
- Keep one active lease per write scope and never include `.owlcoda/runkit/**` in owned source paths.
- Do not repeat commands already covered by a valid receipt.
- Require stage verification before accepting an execution.
- RunKit configuration does not authorize Git, release, credentials, destructive actions, or foreign-project writes.
