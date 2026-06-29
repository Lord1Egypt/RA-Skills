# Reality Gap Checklist

Use this checklist to find claim-vs-system mismatches.

## Docs vs Runtime

- README describes a feature that has no entrypoint.
- CLI help lists a flag that is parsed but ignored.
- Environment variable is documented but never loaded.
- Example command succeeds while silently doing nothing.
- Error path degrades to success without telling the user.

## Runtime vs Deployment

- Local behavior differs from production routing.
- Production bypasses a safeguard present in source.
- Deployment config points at an old build command or stale output directory.
- Public site or registry package omits claimed files.

## Tests vs Claims

- Tests mock the behavior used as proof.
- Unit tests pass but do not exercise public behavior.
- CI skips the relevant test path.
- Snapshot or fixture proves old output rather than current runtime.

## Release And Install

- Package metadata points to missing files.
- Installer assumes undeclared prerequisites.
- Release notes claim artifacts that are not shipped.
- Version, tag, changelog, package, and live registry disagree.

## Intentional Exceptions

Before filing a finding, check for ADRs, feature gates, role boundaries,
environment-specific behavior, or explicit deprecation notes.
