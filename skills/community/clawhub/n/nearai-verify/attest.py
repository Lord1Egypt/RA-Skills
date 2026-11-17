#!/usr/bin/env python3
"""Attestation checks for NEAR AI Cloud endpoints (evidence level: ATTESTED).

Degrades on purpose. Every check that can run, runs; every check that cannot
says which package would enable it and how to get it. Missing dependencies are
reported as actionable findings, never as a crash.

Usage:
  attest.py --doctor            what each level needs and whether it is reachable
  attest.py                     attest the endpoint behind the primary model
  attest.py --endpoint HOST     attest a specific TEE host
  attest.py --install           create a private venv and install the extras
  attest.py --json              machine-readable
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import http.client
import json
import os
import re
import secrets
import socket
import ssl
import subprocess
import sys
import sysconfig
import urllib.request
from pathlib import Path
from typing import Any

CONFIG = Path(os.environ.get("OPENCLAW_CONFIG_PATH", Path.home() / ".openclaw" / "openclaw.json"))
VENV = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "nearai-verify" / "venv"
EXTRAS = ["cryptography>=46.0.0", "dcap-qvl>=0.3.9"]
NRAS_URL = "https://nras.attestation.nvidia.com/v3/attest/gpu"
OK, NO = "ok", "MISSING"
INTEL_QE_VENDOR_ID = bytes.fromhex("939a7233f79c4ca9940a0db3957f0607")
DCAP_QUOTE_HEADER_LEN = 48
QE_VENDOR_ID_OFFSET = 12


# ---------------------------------------------------------------- capabilities

def venv_python() -> Path | None:
    p = VENV / "bin" / "python"
    return p if p.exists() else None


def probe(mod: str) -> tuple[bool, str]:
    """Is `mod` importable here, or in our private venv?"""
    try:
        m = __import__(mod)
        return True, f"{getattr(m, '__version__', '?')} (current interpreter)"
    except ImportError:
        pass
    vp = venv_python()
    if vp:
        r = subprocess.run([str(vp), "-c", f"import {mod},sys;print(getattr({mod},'__version__','?'))"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return True, f"{r.stdout.strip()} (skill venv)"
    return False, ""


def externally_managed() -> bool:
    """PEP 668: pip refuses to touch this interpreter's site-packages."""
    stdlib = sysconfig.get_path("stdlib")
    return bool(stdlib) and (Path(stdlib) / "EXTERNALLY-MANAGED").exists()


def net_ok(host: str = "api.trustedservices.intel.com", port: int = 443) -> bool:
    try:
        socket.create_connection((host, port), timeout=8).close()
        return True
    except OSError:
        return False


def capabilities() -> dict:
    crypto_ok, crypto_v = probe("cryptography")
    qvl_ok, qvl_v = probe("dcap_qvl")
    return {
        "cryptography": {"ok": crypto_ok, "detail": crypto_v, "enables": "TLS key-binding check"},
        "dcap_qvl": {"ok": qvl_ok, "detail": qvl_v,
                     "enables": "Intel TDX quote + signer/nonce binding verification"},
        "intel_pcs": {"ok": net_ok(), "detail": "api.trustedservices.intel.com:443",
                      "enables": "Intel quote collateral download"},
        "nvidia_nras": {"ok": net_ok("nras.attestation.nvidia.com"),
                        "detail": "nras.attestation.nvidia.com:443",
                        "enables": "NVIDIA GPU attestation (no package needed)"},
    }


def install_hint() -> list[str]:
    """The command that will actually work here, not the textbook one."""
    if venv_python():
        return [f"{VENV}/bin/pip install " + " ".join(EXTRAS)]
    if sys.prefix != sys.base_prefix:
        return ["pip install " + " ".join(EXTRAS) + "   # active venv"]
    if externally_managed():
        return [
            "This Python is externally managed (PEP 668) - a plain 'pip install' will refuse.",
            f"Use a private venv instead:  python3 {Path(__file__).name} --install",
        ]
    return ["pip install --user " + " ".join(EXTRAS),
            f"or keep it self-contained:  python3 {Path(__file__).name} --install"]


def cmd_install() -> int:
    print(f"Creating venv at {VENV}")
    VENV.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "-m", "venv", str(VENV)])
    if r.returncode:
        print("  venv creation failed - is python3-venv installed?")
        return 1
    print(f"Installing {' '.join(EXTRAS)}")
    r = subprocess.run([str(VENV / "bin" / "pip"), "install", "-q", *EXTRAS])
    if r.returncode:
        print("  install failed - see pip output above")
        return 1
    print("Done. Re-run --doctor to confirm.")
    return 0


# ------------------------------------------------------------------- reporting

def cmd_doctor(as_json: bool) -> int:
    caps = capabilities()
    missing = [k for k, v in caps.items() if not v["ok"]]

    if as_json:
        print(json.dumps({"capabilities": caps, "install": install_hint()}, indent=2))
        return 0

    print("Verification levels\n")
    print("  [1] CLAIMED    ready")
    print("      Proves : nothing. Reads local config + gateway logs.")
    print("      Needs  : python3 stdlib only")
    print("      Run    : python3 check.py\n")

    done = sum(1 for v in caps.values() if v["ok"])
    state = "ready" if done == len(caps) else f"partial - {done}/{len(caps)} checks available"
    print(f"  [2] ATTESTED   {state}")
    print("      Proves : this endpoint is genuine TEE hardware, right now.")
    for i, (name, v) in enumerate(caps.items()):
        label = "Needs  :" if i == 0 else "        "
        mark = OK if v["ok"] else NO
        print(f"      {label} {name:<14} {mark:<8} {v['detail'] or v['enables']}")
    print("      Run    : python3 attest.py")
    if missing:
        print("\n      To enable the missing checks:")
        for line in install_hint():
            print(f"        {line}")
    print()

    print("  [3] PROVEN     not available")
    print("      Proves : this specific message was signed inside that TEE.")
    print("      Needs  : an OpenClaw provider plugin (createStreamFn) - not built yet.")
    print("               A skill cannot see raw request/response bytes.")
    print()
    print("  Stdlib check: response nonce echo.")
    print("  Verified quote report_data binding requires dcap-qvl.")
    return 0


# ----------------------------------------------------------------- attestation

def primary_endpoint() -> tuple[str, str]:
    """(host, model) for the configured primary model."""
    if not CONFIG.exists():
        sys.exit(f"No OpenClaw config at {CONFIG}")
    cfg = json.loads(CONFIG.read_text())
    ref = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
    provider, _, bare = ref.partition("/")
    pcfg = cfg.get("models", {}).get("providers", {}).get(provider, {})
    base = pcfg.get("baseUrl")
    for e in pcfg.get("models", []):
        if e.get("id") == bare and e.get("baseUrl"):
            base = e["baseUrl"]
            break
    if not base:
        sys.exit(f"Primary model '{ref}' has no configured baseUrl - nothing to attest.")
    host = re.sub(r"^https?://", "", base).split("/")[0]
    if not host.endswith(".completions.near.ai"):
        sys.exit(f"Primary model '{ref}' is not on a NEAR direct-completions endpoint ({host}).\n"
                 f"Attestation only applies to *.completions.near.ai. Run check.py first.")
    return host, bare


def fetch_report_and_cert(host: str, nonce: str) -> tuple[dict, bytes]:
    """Report and served certificate over ONE TLS connection.

    A domain can be load-balanced across several CVMs. Fetching the report on
    one connection and the certificate on another can hit different backends and
    produce a false SPKI mismatch, so both must come from the same socket.

    CA verification is skipped deliberately: a TEE generates its own TLS key and
    it need not be CA-signed. Trust comes from the hardware quote plus the SPKI
    binding, not from a certificate authority.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = http.client.HTTPSConnection(host, 443, context=ctx, timeout=90)
    try:
        conn.connect()
        der = conn.sock.getpeercert(binary_form=True)
        conn.request("GET", f"/v1/attestation/report?signing_algo=ecdsa"
                            f"&nonce={nonce}&include_tls_fingerprint=true",
                     headers={"accept": "application/json"})
        return json.loads(conn.getresponse().read()), der
    finally:
        conn.close()


def spki_fingerprint(cert_der: bytes) -> str | None:
    """SHA256 of the certificate's SubjectPublicKeyInfo. Needs `cryptography`.

    Hashing only the public key info keeps the value stable across certificate
    renewals that reuse the same key.
    """
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        return None
    spki = x509.load_der_x509_certificate(cert_der).public_key().public_bytes(
        serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return hashlib.sha256(spki).hexdigest()


def extract_verified_report_data(result: Any) -> str | None:
    """Extract TD report_data from dcap-qvl's cryptographically verified result."""
    try:
        payload = json.loads(result.to_json())
    except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
        return None

    report = payload.get("report")
    if not isinstance(report, dict):
        return None

    # dcap-qvl serializes quote report variants as, for example,
    # {"report": {"TD10": {"report_data": "..."}}}. Accept the field-name
    # spelling used by older releases without searching outside the verified
    # quote report, where an untrusted lookalike field could exist.
    candidates = [report, *(v for v in report.values() if isinstance(v, dict))]
    for candidate in candidates:
        for key in ("report_data", "reportdata"):
            value = candidate.get(key)
            if isinstance(value, str):
                return value.removeprefix("0x").lower()
    return None


def appraise_verified_tcb_statuses(result: Any) -> tuple[bool | None, str]:
    """Require passing aggregate, platform, and QE statuses from verified output."""
    try:
        payload = json.loads(result.to_json())
    except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
        return None, "dcap-qvl result did not expose verified TCB statuses"

    statuses: dict[str, str] = {}
    overall = payload.get("status")
    if isinstance(overall, str):
        statuses["overall"] = overall
    for label, key in (("platform", "platform_status"), ("QE", "qe_status")):
        value = payload.get(key)
        if isinstance(value, dict) and isinstance(value.get("status"), str):
            statuses[label] = value["status"]

    missing = [label for label in ("overall", "platform", "QE") if label not in statuses]
    if missing:
        return None, f"verified result missing {', '.join(missing)} TCB status"

    failed = [f"{label}={status}" for label, status in statuses.items()
              if status.lower() not in ("uptodate", "ok")]
    detail = ", ".join(f"{label} {status}" for label, status in statuses.items())
    if failed:
        return False, "TCB policy rejected " + ", ".join(failed)
    return True, detail


def verify_intel_qe_vendor_id(quote: bytes) -> tuple[bool, str]:
    """Enforce Intel's QE Vendor ID until dcap-qvl validates it upstream."""
    if len(quote) < DCAP_QUOTE_HEADER_LEN:
        return False, "DCAP quote is shorter than its 48-byte header"
    actual = quote[QE_VENDOR_ID_OFFSET:QE_VENDOR_ID_OFFSET + len(INTEL_QE_VENDOR_ID)]
    if not secrets.compare_digest(actual, INTEL_QE_VENDOR_ID):
        return False, f"unexpected QE Vendor ID {actual.hex()}"
    return True, "Intel QE Vendor ID"


def _decode_hex(value: object, name: str, expected_bytes: int) -> bytes:
    if not isinstance(value, str):
        raise ValueError(f"{name} is missing")
    raw = value.removeprefix("0x")
    if len(raw) != expected_bytes * 2 or not re.fullmatch(r"[0-9a-fA-F]+", raw):
        raise ValueError(f"{name} must be exactly {expected_bytes} bytes of hex")
    return bytes.fromhex(raw)


def verify_report_data_binding(
    report_data_hex: str,
    attestation: dict,
    request_nonce: str,
) -> tuple[bool, str]:
    """Prove the verified TDX quote binds this signer and fresh request nonce."""
    try:
        report_data = _decode_hex(report_data_hex, "verified quote report_data", 64)
        nonce = _decode_hex(request_nonce, "request nonce", 32)
        algo = str(attestation.get("signing_algo", "ecdsa")).lower()
        if algo == "ecdsa":
            signing_address = _decode_hex(attestation.get("signing_address"),
                                          "ECDSA signing address", 20)
        elif algo == "ed25519":
            signing_address = _decode_hex(attestation.get("signing_address"),
                                          "Ed25519 signing address", 32)
        else:
            raise ValueError(f"unsupported signing algorithm: {algo}")

        fingerprint_value = attestation.get("tls_cert_fingerprint")
        if fingerprint_value is not None:
            fingerprint = _decode_hex(fingerprint_value, "TLS certificate fingerprint", 32)
            expected_signer = hashlib.sha256(signing_address + fingerprint).digest()
            signer_label = "signer + TLS fingerprint"
        else:
            expected_signer = signing_address.ljust(32, b"\x00")
            signer_label = "signer"
    except ValueError as e:
        return False, str(e)

    signer_ok = secrets.compare_digest(report_data[:32], expected_signer)
    nonce_ok = secrets.compare_digest(report_data[32:], nonce)
    if signer_ok and nonce_ok:
        return True, f"verified quote binds {signer_label} and fresh nonce"

    failed = []
    if not signer_ok:
        failed.append(f"{signer_label} mismatch")
    if not nonce_ok:
        failed.append("nonce mismatch (possible replay)")
    return False, ", ".join(failed)


def verify_quote(quote_hex: str) -> tuple[bool | None, str, str | None]:
    """(passed, detail, verified report_data). None = could not run."""
    try:
        import asyncio
        import dcap_qvl
    except ImportError:
        return None, "dcap-qvl not installed", None
    try:
        quote = bytes.fromhex(quote_hex)
        vendor_ok, vendor_detail = verify_intel_qe_vendor_id(quote)
        if not vendor_ok:
            return False, vendor_detail, None

        r = asyncio.run(dcap_qvl.get_collateral_and_verify(quote))
        status_ok, status_detail = appraise_verified_tcb_statuses(r)
        report_data = extract_verified_report_data(r)
        if status_ok is None:
            return None, status_detail, report_data
        return status_ok, f"{vendor_detail}; {status_detail}", report_data
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"[:160], None


def nvidia_verdict_passed(verdict: object) -> bool:
    """Accept only explicit NVIDIA pass values; truthiness is not a verdict."""
    if verdict is True:
        return True
    if isinstance(verdict, str):
        return verdict.strip().lower() in ("pass", "passed", "true")
    return False


def verify_gpu(nvidia_payload: str, nonce: str) -> tuple[bool | None, str]:
    """Submit GPU evidence to NVIDIA's attestation service. (passed, detail).

    Intel TDX covers the CPU and the confidential VM. This covers the GPU that
    actually holds the weights and activations, so both are needed.
    """
    if not nvidia_payload:
        return None, "no nvidia_payload in report"
    try:
        payload = json.loads(nvidia_payload)
    except Exception:
        return False, "nvidia_payload is not valid JSON"

    if payload.get("nonce", "").lower() != nonce.lower():
        return False, "GPU evidence nonce does not match our nonce - possible replay"

    try:
        req = urllib.request.Request(NRAS_URL, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        body = json.loads(urllib.request.urlopen(req, timeout=90).read())
        claims_b64 = body[0][1].split(".")[1]
        claims_b64 += "=" * ((4 - len(claims_b64) % 4) % 4)
        claims = json.loads(base64.urlsafe_b64decode(claims_b64))
    except Exception as e:
        return None, f"NVIDIA NRAS unreachable ({type(e).__name__}) - cannot verify GPU"

    verdict = claims.get("x-nvidia-overall-att-result")
    gpus = len(claims.get("submods", {}))
    arch = payload.get("arch", "?")
    passed = nvidia_verdict_passed(verdict)
    return passed, (f"{arch}, {gpus} GPU(s) attested by NVIDIA"
                    if passed else f"NVIDIA verdict did not pass: {verdict!r}")


def cmd_attest(as_json: bool, endpoint: str | None) -> int:
    host, model = (endpoint, "(explicit endpoint)") if endpoint else primary_endpoint()
    nonce = secrets.token_hex(32)  # fresh every run; a cached attestation is a replayed one

    try:
        rep, cert_der = fetch_report_and_cert(host, nonce)
    except Exception as e:
        print(f"Could not fetch attestation from {host}: {type(e).__name__}: {e}")
        return 2

    checks: list[tuple[str, bool | None, str]] = []

    echoed = rep.get("request_nonce")
    checks.append(("nonce freshness", echoed == nonce,
                   "echoed our nonce" if echoed == nonce else f"expected {nonce[:12]}…, got {str(echoed)[:12]}…"))

    reported_fp = rep.get("tls_cert_fingerprint")
    live_fp = spki_fingerprint(cert_der)
    if live_fp is None:
        checks.append(("TLS key binding", None,
                       "needs `cryptography` - without it nothing ties this connection "
                       "to the quote; see --doctor"))
    else:
        checks.append(("TLS key binding", live_fp == reported_fp,
                       "our TLS session terminates inside the attested TEE" if live_fp == reported_fp
                       else "served key does not match the attested one"))

    q_ok, q_detail, verified_report_data = verify_quote(rep.get("intel_quote", ""))
    checks.append(("Intel TDX quote", q_ok, q_detail if q_ok is not None else q_detail + " - see --doctor"))
    if q_ok is True and verified_report_data is not None:
        binding_ok, binding_detail = verify_report_data_binding(
            verified_report_data, rep, nonce)
        checks.append(("signer + nonce binding", binding_ok, binding_detail))
    elif q_ok is True:
        checks.append(("signer + nonce binding", None,
                       "dcap-qvl verified the quote but did not expose TD report_data"))
    elif q_ok is False:
        checks.append(("signer + nonce binding", False,
                       "cannot trust report_data because the Intel quote did not verify"))
    else:
        checks.append(("signer + nonce binding", None,
                       "needs a verified Intel quote - see --doctor"))

    g_ok, g_detail = verify_gpu(rep.get("nvidia_payload", ""), nonce)
    checks.append(("NVIDIA GPU attestation", g_ok, g_detail))

    ran = [c for c in checks if c[1] is not None]
    failed = [c for c in ran if c[1] is False]
    skipped = [c for c in checks if c[1] is None]
    level = "ATTESTED" if not failed and not skipped else ("FAILED" if failed else "CLAIMED")

    if as_json:
        print(json.dumps({
            "level": level.lower(), "endpoint": host, "model": rep.get("model_name", model),
            "signing_address": rep.get("signing_address"),
            "checks": [{"name": n, "result": r, "detail": d} for n, r, d in checks],
        }, indent=2))
        return 0 if level == "ATTESTED" else 1

    print(f"NEAR AI attestation - level: {level}\n")
    print(f"  endpoint : {host}")
    print(f"  model    : {rep.get('model_name', model)}")
    print(f"  TEE stack: {rep.get('info', {}).get('app_name', '?')}")
    print(f"  signer   : {rep.get('signing_address', '?')}\n")
    for name, res, detail in checks:
        mark = {True: "PASS", False: "FAIL", None: "SKIP"}[res]
        print(f"  [{mark}] {name:<23} {detail}")

    print()
    if failed:
        print("  ATTESTATION FAILED. Do not treat this endpoint as private.")
    elif skipped:
        print(f"  {len(skipped)} check(s) skipped, so this is not a full attestation.")
        print("  Level stays CLAIMED. Run --doctor for the one-line fix.")
    else:
        print("  Endpoint proved it is genuine TEE hardware (CPU and GPU) and terminates")
        print("  our TLS session.")
        print("  This says nothing about any individual message - that needs level 3.")
    return 0 if level == "ATTESTED" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Attest a NEAR AI Cloud TEE endpoint.")
    ap.add_argument("--doctor", action="store_true", help="what each level needs and whether it is reachable")
    ap.add_argument("--install", action="store_true", help="create a private venv and install the extras")
    ap.add_argument("--endpoint", help="attest a specific *.completions.near.ai host")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()
    if a.install:
        return cmd_install()
    if a.doctor:
        return cmd_doctor(a.json)
    return cmd_attest(a.json, a.endpoint)


if __name__ == "__main__":
    sys.exit(main())
