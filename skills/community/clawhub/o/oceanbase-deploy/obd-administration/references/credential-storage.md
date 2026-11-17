# OBD Stored-Credential Encryption

Use this workflow for the OBD-local password-encryption state and encryption passkey (EPK). In the inspected implementation, EPK is a controller-wide verification passphrase whose digest is stored; it is not the AES key used to encrypt deployment credentials. That AES key is derived from deployment identity. Re-verify this model against the installed build. EPK protection does not prove that secrets in YAML, URIs, shell history, process arguments, traces, backups, or external services are protected.

## Scope and Custody Gate

1. Record the controller, user, `OBD_HOME`, OBD version/build, encryption state, metadata owner and permissions, registered deployments, and OBD processes that can read or write credentials.
2. Read the installed `obd pwd` help and version-matched implementation or documentation. Determine which stored fields/files are migrated, where encryption metadata resides, and what interruption does to plaintext and ciphertext.
3. Define EPK generation, custody, recovery, and access control before enabling encryption. Store the verification passphrase separately from metadata with least privilege; do not describe it as the deployment credential-encryption key.
4. Inspect how the current build accepts the EPK and current passkey. If only command arguments or positional values are available, disclose process-list and shell-history exposure and require an approved secure local procedure. Do not invent a protected input channel.
5. Back up only the required metadata with permissions that protect its credentials. Never put an EPK or decrypted credential in Skill text, chat, traces, or reports.

Enabling/disabling stored-password encryption and changing the EPK are distinct credential-control mutations. Determine which operation rewrites deployment metadata and which only changes the EPK verifier, then show the exact transition, plaintext exposure, and interruption boundary before authorization. Do not claim that `set-epk` rotates or re-encrypts stored deployment credentials when the installed implementation only replaces the verifier.

## Enable, Disable, or Rotate

Use only the installed syntax, such as the supported forms of `obd pwd encrypt` and `obd pwd set-epk`, without literal passkeys in reusable commands.

- **Enable:** verify all intended stored credentials remain usable after migration and that no unexpected plaintext copy was created.
- **Disable:** explain the loss of at-rest protection and verify resulting file permissions and documented migration artifacts.
- **Change EPK:** require a recoverably escrowed new verification passphrase and the supported proof of the current passphrase. Verify the new EPK gate and representative stored credentials separately; success of one does not prove the other was migrated.

Never add a force option automatically. A forced EPK replacement is a manual incident-recovery action, not credential re-encryption. If the installed command requests an operating-system credential, obtain it through a protected local input path, keep it out of chat and reusable command text, disclose any process/history/trace exposure, and execute only after the user authorizes the exact recovery action.

## Acceptance and Recovery

Verify EPK state, stored-password encryption state, metadata permissions, absence of unexpected plaintext artifacts, and successful credential use through a read-only operation that exercises loading without printing the secret. Record only redacted evidence.

On interruption during an encryption migration or on decryption failure, freeze OBD mutations that depend on stored credentials. Preserve encrypted metadata, verifier/encryption-state evidence, OBD identity, and the completed stage. Do not disable encryption, force-reset the EPK, clear metadata, or recreate deployments as a generic repair. A force-reset EPK does not repair ciphertext whose deployment-derived key or metadata is wrong.

## Sources

- Official OBD V4.6.0 Command Guide `obd pwd` command group.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `core.py` `encrypt_manager`, `check_encryption_passkey`, and `set_encryption_passkey`; `_deploy.py` `change_deploy_config_password` in the exact inspected checkout.
