"""GPG (OpenPGP) detached-signature verification for iterate release artifacts.

Every iterate release publishes, next to each artifact, a detached
ASCII-armored signature (``*.asc``) made with the project signing key. The
public key is PINNED here and must stay identical in three places:

  * ``iterate_cli/signing.py``                       (this file — CLI updater)
  * ``scripts/install.py``                           (standalone installer)
  * ``npm-installer/lib/installer.js``               (``ITERATE_SIGNING_PUBLIC_KEY``)

plus the ``GPG_PRIVATE_KEY`` repository secret used by
``.github/workflows/release.yml`` to sign the release artifacts.
``tests/test_release_meta.py`` asserts the copies stay in sync, and the
release workflow refuses to publish artifacts signed by any other key.

Signature verification is MANDATORY by default: a missing or non-verifying
signature aborts an install/update (SHA256 alone cannot defend against a
release channel that is compromised at the source, since the checksum file
travels in the same release as the tarball). The ONLY escape hatch is the
environment variable ``ITERATE_ALLOW_UNSIGNED`` (for hosts without a ``gpg``
binary), which downgrades the failure to a loud warning.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Final

__all__ = [
    "ALLOW_UNSIGNED_ENV",
    "ITERATE_SIGNING_PUBLIC_KEY",
    "SIGNING_KEY_FINGERPRINT",
    "allow_unsigned",
    "enforce_signature_policy",
    "verify_detached_signature",
]

#: Opt-out for hosts with no ``gpg`` binary. Only explicit truthy values
#: (``1``/``true``/``yes``, case-insensitive) disable the mandatory-signature
#: policy; ``0``/``false``/``no``/blank all keep it in force. It is deliberately
#: an ENVIRONMENT variable (not a config file / flag) so it cannot be enabled by
#: a hand-edited project config and shows up in the invoking environment for
#: audit.
ALLOW_UNSIGNED_ENV: Final[str] = "ITERATE_ALLOW_UNSIGNED"

#: Values that explicitly opt OUT of signature enforcement. MUST stay identical
#: to ``scripts/install.py`` ``_ALLOW_UNSIGNED_TRUE_VALUES`` and
#: ``npm-installer/lib/installer.js`` ``ALLOW_UNSIGNED_TRUTHY`` — all three
#: paths must agree on what "unsigned is allowed" means, or one installer would
#: silently accept what another refused (see tests/test_signing.py).
ALLOW_UNSIGNED_TRUE_VALUES: Final[frozenset[str]] = frozenset({"1", "true", "yes"})

#: Fingerprint of the pinned signing key (GPG_PRIVATE_KEY in CI). Printed in
#: diagnostics so an operator can see WHICH key was expected.
SIGNING_KEY_FINGERPRINT: Final[str] = "0929EA31DF4F7429F63FC53189D88B1D043A1298"

#: ASCII-armored public key of the release signer. Kept byte-identical with the
#: copies in scripts/install.py and npm-installer/lib/installer.js.
ITERATE_SIGNING_PUBLIC_KEY: Final[str] = """-----BEGIN PGP PUBLIC KEY BLOCK-----

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
YVXa4IEQs7aBxKO+n+T2AvUYiKQ=
=DYXk
-----END PGP PUBLIC KEY BLOCK-----"""

_VERIFY_TIMEOUT_SECONDS: Final[int] = 30


def allow_unsigned() -> bool:
    """True when the operator explicitly opted out of signature enforcement.

    Requires an explicit truthy value (``1`` / ``true`` / ``yes``,
    case-insensitive). A bare truthiness test treated every non-empty value as
    an opt-out, so the intuitive ``ITERATE_ALLOW_UNSIGNED=0`` ("keep signatures
    mandatory") silently DISABLED signature enforcement — the exact opposite of
    the operator's intent, and a silent downgrade of the authenticity gate.
    """
    value = os.environ.get(ALLOW_UNSIGNED_ENV, "").strip().lower()
    return value in ALLOW_UNSIGNED_TRUE_VALUES


def enforce_signature_policy(
    artifact_path: Path | str,
    signature_path: Path | str | None,
    *,
    allow_unsigned_override: bool | None = None,
    gpg_bin: str = "gpg",
) -> tuple[bool, str]:
    """Apply the MANDATORY release-signature policy.

    Args:
        artifact_path: The downloaded artifact (the release tarball).
        signature_path: The downloaded ``.asc`` signature, or ``None`` when the
            release did not publish one.
        allow_unsigned_override: Defaults to ``allow_unsigned()``; injectable
            for tests.
        gpg_bin: gpg executable name/path.

    Returns:
        ``(ok, detail)``. ``ok=False`` means the caller MUST abort the
        install/update.

    Policy:
        * signature VERIFIED → proceed (this is the only clean success).
        * signature MISSING → abort, unless ``ITERATE_ALLOW_UNSIGNED`` is set.
        * gpg UNAVAILABLE → abort, unless ``ITERATE_ALLOW_UNSIGNED`` is set.
        * signature INVALID → **always** abort. The override exists for hosts
          without a ``gpg`` binary, never to wave through a bad signature
          (that is exactly the tampering/key-substitution case).
    """
    override = allow_unsigned() if allow_unsigned_override is None else allow_unsigned_override

    if signature_path is None:
        if override:
            return True, (
                f"UNSIGNED release accepted because {ALLOW_UNSIGNED_ENV} is set "
                "(SHA256 integrity only)"
            )
        return False, (
            "release is UNSIGNED: it publishes no .asc signature, so authenticity "
            "cannot be verified. Refusing to proceed (SHA256SUMS travels in the "
            f"same release and is not an independent anchor). Set "
            f"{ALLOW_UNSIGNED_ENV}=1 only if you accept an unauthenticated install."
        )

    status, detail = verify_detached_signature(
        artifact_path, signature_path, gpg_bin=gpg_bin
    )
    if status == "verified":
        return True, detail
    if status == "invalid":
        return False, (
            f"GPG signature verification FAILED ({detail}). Refusing to proceed: "
            "the artifact is not signed by the pinned iterate signing key "
            f"({SIGNING_KEY_FINGERPRINT}). This is either tampering or a key "
            f"rotation that this version does not know about — {ALLOW_UNSIGNED_ENV} "
            "does NOT bypass a bad signature."
        )
    # status == "unavailable"
    if override:
        return True, (
            f"signature NOT verified ({detail}) but accepted because "
            f"{ALLOW_UNSIGNED_ENV} is set (SHA256 integrity only)"
        )
    return False, (
        f"cannot verify the release signature ({detail}). Install GnuPG (``gpg``) "
        f"and retry, or set {ALLOW_UNSIGNED_ENV}=1 to accept an unauthenticated "
        "install."
    )


def _list_key_fingerprints(gpg: str, home: Path, timeout: int) -> list[str]:
    """Return every fingerprint (primary + subkeys) in ``home``'s keyring.

    Used to establish WHICH key a signature must have been made by: the verify
    step compares gpg's ``VALIDSIG`` fingerprint against this set, so passing
    gpg's exit code alone is never enough.
    """
    listing = subprocess.run(
        [gpg, "--homedir", str(home), "--batch", "--with-colons", "--list-keys"],
        capture_output=True, text=True, timeout=timeout, check=False,
    )
    if listing.returncode != 0:
        return []
    fingerprints: list[str] = []
    for line in listing.stdout.splitlines():
        if not line.startswith("fpr:"):
            continue
        fields = line.split(":")
        if len(fields) > 9 and fields[9]:
            fingerprints.append(fields[9].upper())
    return fingerprints


def _validsig_fingerprints(status_output: str) -> list[str]:
    """Extract the fingerprints gpg reported as ``VALIDSIG`` in ``--status-fd``.

    A status line looks like ``[GNUPG:] VALIDSIG <fpr> <date> …``; the
    fingerprint is the token right after the ``VALIDSIG`` keyword.
    """
    fingerprints: list[str] = []
    for line in status_output.splitlines():
        if not line.startswith("[GNUPG:] VALIDSIG "):
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[2]:
            fingerprints.append(parts[2].upper())
    return fingerprints


def _kill_gpg_agent(gpg: str, home: Path, timeout: int) -> None:
    """Best-effort ``gpgconf --kill gpg-agent`` for the throwaway homedir.

    gpg may leave an agent running with the imported key cached; killing it
    ensures no stale agent (pinning an old/cached key) outlives the
    verification. This is cleanup, never part of the security decision, so it
    swallows every error and never raises.
    """
    gpgconf = shutil.which("gpgconf")
    if not gpgconf and os.sep in gpg:
        candidate = str(Path(gpg).with_name("gpgconf"))
        if os.path.exists(candidate):
            gpgconf = candidate
    if not gpgconf:
        return
    with contextlib.suppress(Exception):
        subprocess.run(
            [gpgconf, "--homedir", str(home), "--kill", "gpg-agent"],
            capture_output=True, text=True, timeout=timeout, check=False,
        )


def verify_detached_signature(
    artifact_path: Path | str,
    signature_path: Path | str,
    *,
    public_key: str = ITERATE_SIGNING_PUBLIC_KEY,
    gpg_bin: str = "gpg",
    timeout: int = _VERIFY_TIMEOUT_SECONDS,
) -> tuple[str, str]:
    """Verify ``artifact_path`` against ``signature_path`` with the pinned key.

    Returns:
        ``(status, detail)`` where ``status`` is one of:

        * ``"verified"``    — gpg is present and the signature is VALID *and*
          gpg's ``VALIDSIG`` fingerprint belongs to the pinned key.
        * ``"invalid"``     — gpg is present but the signature did not verify
          (wrong key, tampered artifact, or tampered signature), or it verified
          under a fingerprint that is not the pinned key.
        * ``"unavailable"`` — no gpg binary, or the pinned key could not be
          imported into the throwaway keyring.

    The check runs in an isolated temporary ``GNUPGHOME``, so the invoking
    user's own keyring and gpg-agent are never read or modified.
    """
    gpg = gpg_bin if os.sep in gpg_bin else shutil.which(gpg_bin)
    if not gpg:
        return "unavailable", "gpg binary not found on PATH"

    # The keyring MUST live under a SHORT path: gpg derives its agent socket as
    # ``<GNUPGHOME>/S.gpg-agent``, and a deep TMPDIR (macOS ``/var/folders/…``,
    # or a pytest tmp_path) pushes it past the ~104-char unix-socket limit —
    # gpg then reports "can't connect to the gpg-agent: File name too long" and
    # every operation fails. ``mkdtemp`` (mode 0700) with a short prefix and no
    # extra nesting keeps the socket path short.
    try:
        with tempfile.TemporaryDirectory(prefix="ig-") as tmp:
            home = Path(tmp)
            key_path = home / "pub.asc"
            key_path.write_text(public_key, encoding="utf-8")
            # No --no-autostart: gpg may start a PRIVATE agent inside this
            # throwaway homedir (the user's own keyring/agent is never touched).
            imported = subprocess.run(
                [
                    gpg, "--homedir", str(home), "--batch", "--yes", "--quiet",
                    "--import", str(key_path),
                ],
                capture_output=True, text=True, timeout=timeout, check=False,
            )
            if imported.returncode != 0:
                detail = (imported.stderr or imported.stdout).strip().splitlines()
                return "unavailable", (
                    "could not import the pinned public key"
                    + (f": {detail[-1][:160]}" if detail else "")
                )
            pinned_fingerprints = _list_key_fingerprints(gpg, home, timeout)
            if not pinned_fingerprints:
                return "unavailable", "could not read the pinned key fingerprint"
            try:
                # --no-auto-key-retrieve: never let gpg fetch a signer's key
                # over the network behind our back — the only key that may
                # verify here is the one we just imported.
                verified = subprocess.run(
                    [
                        gpg, "--homedir", str(home), "--batch",
                        "--no-auto-key-retrieve",
                        "--status-fd", "1", "--verify", str(signature_path),
                        str(artifact_path),
                    ],
                    capture_output=True, text=True, timeout=timeout, check=False,
                )
            finally:
                _kill_gpg_agent(gpg, home, timeout)
    except subprocess.TimeoutExpired as exc:
        # A hung gpg is not a missing dependency: reporting it as
        # "unavailable" let ITERATE_ALLOW_UNSIGNED bypass verification
        # entirely. Fail closed; only a genuinely absent/unlaunchable gpg may
        # take the explicit unsigned escape hatch.
        return "invalid", (
            f"gpg timed out while verifying (treated as invalid): {exc}. "
            "Retry, or inspect the gpg agent/keyring."
        )
    except OSError as exc:
        return "unavailable", f"gpg could not run: {exc}"

    signer_fingerprints = _validsig_fingerprints(verified.stdout)
    if (
        verified.returncode == 0
        and signer_fingerprints
        and any(fpr in pinned_fingerprints for fpr in signer_fingerprints)
    ):
        return (
            "verified",
            f"signature matches the pinned key ({pinned_fingerprints[0]})",
        )
    detail_lines = [ln for ln in verified.stderr.strip().splitlines() if ln.strip()]
    return "invalid", (detail_lines[-1][:200] if detail_lines else "gpg reported a bad signature")
