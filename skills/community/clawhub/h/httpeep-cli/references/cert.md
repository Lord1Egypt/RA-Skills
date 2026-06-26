<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/cert.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Certificate

HTTPeep intercepts HTTPS traffic by acting as a man-in-the-middle proxy using its own root CA certificate. The `cert` subcommand lets you check the status of that certificate, install it into the OS trust store, or export it for manual installation.

## cert status

Show the current state of the root CA certificate.

```bash
httpeep-cli cert status
```

Example output:

```text
Root CA:      exists
OS Trust:     trusted ✓
Expires:      2028-04-13 (in 730 days)
Fingerprint:  SHA256:abc123...
```

The output tells you whether the CA exists, whether the OS trusts it, when it expires, and its SHA256 fingerprint for verification.

## cert install

Install the root CA certificate and register it with the OS trust store. This enables HTTPS decryption for all traffic through the proxy.

```bash
httpeep-cli cert install
```

> **Note:**
> After installing the certificate, verify it is trusted by running `httpeep-cli cert status` and checking that `OS Trust` shows `trusted ✓`. If it does not, restart your browser or application — some apps cache the trust store at startup.

## cert uninstall

Remove the root CA certificate from the system trust store.

```bash
httpeep-cli cert uninstall
```

## cert export

Export the root CA certificate to a file for manual distribution or inspection.

```bash
httpeep-cli cert export --output ./httpeep-ca.crt
```

| Flag | Description |
|---|---|
| `--output <path>` / `-o <path>` | Destination file path |
