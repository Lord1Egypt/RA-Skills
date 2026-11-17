# Input contract

artifacts: name, version, sha256 and testStatus. Passing requires semantic-version-shaped versions,64 lowercase hex digits and testStatus=passed.

## Operational scope

Manifest fields do not prove a file or test is genuine. Verify files, signatures, installation and public downloads separately. Never equate a submitted marketplace version with public availability.

## Fictional example

```json
{
  "artifacts": [
    {
      "name": "demo",
      "version": "1.0.0",
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "testStatus": "passed"
    }
  ]
}
```

## Results

The helper returns `ok`, a task-specific `result`, a report path and an artifact list with byte counts and SHA-256. `ok=true` means this local transformation completed; use the explicit result fields for remaining work. Source files are not overwritten. Python3.10+ is required; IANA timezone support needs timezone data on the operating system or the Python tzdata package.
