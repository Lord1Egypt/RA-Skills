#!/usr/bin/env python3
"""
check_certs.py — Check SSL certificate expiration for all HTTPS services.

For each HTTPS service in services.json:
  - Connects via ssl module to the host
  - Extracts certificate expiry date
  - Flags certs expiring within 30 days (or custom threshold)

Outputs JSON with days_remaining, expires_at, warning flags.

Usage:
    python3 check_certs.py --config assets/services.json
    python3 check_certs.py --config assets/services.json --output /tmp/certs.json
    python3 check_certs.py --config assets/services.json --warn-days 60
"""

import argparse
import json
import os
import socket
import ssl
import sys
from datetime import datetime, timezone


DEFAULT_WARN_DAYS = 30
DEFAULT_TIMEOUT = 10


def load_config(config_path: str) -> dict:
    """Load and validate the services config file."""
    if not os.path.exists(config_path):
        print(f"ERROR: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in config: {e}", file=sys.stderr)
            sys.exit(1)


def parse_cert_date(date_str: str) -> datetime:
    """
    Parse an SSL certificate date string.
    Format: 'Jan  1 00:00:00 2025 GMT' or 'Jan 01 00:00:00 2025 GMT'
    """
    date_str = date_str.strip()
    for fmt in ("%b %d %H:%M:%S %Y %Z", "%b  %d %H:%M:%S %Y %Z"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse cert date: {date_str!r}")


def check_cert(host: str, port: int = 443, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """
    Connect to host:port via TLS and inspect the certificate.
    Returns dict with expiry info or error.
    """
    result = {
        "host": host,
        "port": port,
        "checked": False,
        "valid": None,
        "expires_at": None,
        "days_remaining": None,
        "subject": None,
        "issuer": None,
        "error": None,
    }

    ctx = ssl.create_default_context()
    try:
        conn = ctx.wrap_socket(
            socket.create_connection((host, port), timeout=timeout),
            server_hostname=host,
        )
        cert = conn.getpeercert()
        conn.close()

        not_after = cert.get("notAfter")
        if not not_after:
            result["error"] = "Certificate has no notAfter field"
            return result

        expiry = parse_cert_date(not_after)
        now = datetime.now(timezone.utc)
        days_remaining = (expiry - now).days

        # Extract subject CN
        subject_dict = dict(x[0] for x in cert.get("subject", []))
        issuer_dict = dict(x[0] for x in cert.get("issuer", []))

        result.update(
            {
                "checked": True,
                "valid": cert.get("notBefore") is not None,
                "expires_at": expiry.isoformat(),
                "days_remaining": days_remaining,
                "subject": subject_dict.get("commonName", host),
                "issuer": issuer_dict.get("organizationName", "Unknown"),
            }
        )

    except ssl.SSLCertVerificationError as e:
        result["error"] = f"SSL verification failed: {e.reason}"
    except ssl.SSLError as e:
        result["error"] = f"SSL error: {e}"
    except (socket.timeout, TimeoutError):
        result["error"] = f"Connection timed out after {timeout}s"
    except ConnectionRefusedError:
        result["error"] = "Connection refused"
    except socket.gaierror as e:
        result["error"] = f"DNS resolution failed: {e}"
    except OSError as e:
        result["error"] = f"Network error: {e}"
    except Exception as e:
        result["error"] = str(e)

    return result


def extract_https_services(config: dict) -> list[dict]:
    """Return only HTTPS services from the config."""
    return [
        svc
        for svc in config.get("services", [])
        if svc.get("url", "").startswith("https://")
    ]


def parse_host_port(url: str) -> tuple[str, int]:
    """Extract host and port from a URL. Default port 443."""
    # Strip scheme
    rest = url.split("://", 1)[-1]
    # Strip path
    host_port = rest.split("/")[0]
    if ":" in host_port:
        host, port_str = host_port.rsplit(":", 1)
        return host, int(port_str)
    return host_port, 443


def main():
    parser = argparse.ArgumentParser(
        description="Check SSL certificate expiration for HTTPS services."
    )
    parser.add_argument(
        "--config",
        default="assets/services.json",
        help="Path to services.json config (default: assets/services.json)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write JSON output to this file (default: stdout)",
    )
    parser.add_argument(
        "--warn-days",
        type=int,
        default=DEFAULT_WARN_DAYS,
        help=f"Days before expiry to flag as warning (default: {DEFAULT_WARN_DAYS})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Connection timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress to stderr",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    https_services = extract_https_services(config)

    if not https_services:
        print("No HTTPS services found in config.", file=sys.stderr)

    now = datetime.now(timezone.utc).isoformat()
    cert_results = []

    for svc in https_services:
        name = svc.get("name", svc.get("url", "?"))
        host, port = parse_host_port(svc["url"])

        if args.verbose:
            print(f"Checking cert: {name} ({host}:{port})...", file=sys.stderr)

        cert = check_cert(host, port, args.timeout)
        cert["service_name"] = name
        cert["url"] = svc["url"]

        # Set warning/critical flags
        if cert["days_remaining"] is not None:
            cert["expiring_soon"] = cert["days_remaining"] <= args.warn_days
            cert["expired"] = cert["days_remaining"] < 0
        else:
            cert["expiring_soon"] = False
            cert["expired"] = False

        cert_results.append(cert)

        if args.verbose:
            if cert["error"]:
                print(f"  ✗ {name}: {cert['error']}", file=sys.stderr)
            elif cert["expired"]:
                print(f"  ✗ {name}: EXPIRED ({cert['days_remaining']}d)", file=sys.stderr)
            elif cert["expiring_soon"]:
                print(
                    f"  ⚠ {name}: expires in {cert['days_remaining']}d",
                    file=sys.stderr,
                )
            else:
                print(
                    f"  ✓ {name}: valid, {cert['days_remaining']}d remaining",
                    file=sys.stderr,
                )

    summary = {
        "checked_at": now,
        "warn_days": args.warn_days,
        "total_checked": len(cert_results),
        "warnings": sum(
            1 for c in cert_results if c.get("expiring_soon") or c.get("expired")
        ),
        "errors": sum(1 for c in cert_results if c.get("error")),
        "certs": cert_results,
    }

    output_json = json.dumps(summary, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        if args.verbose:
            print(f"\nResults written to: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
