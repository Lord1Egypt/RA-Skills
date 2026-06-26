#!/usr/bin/env python3
"""SSL certificate checker — check expiry, issuer, and chain for one or more domains.

Usage:
    check_ssl.py <domain> [<domain> ...] [--warn-days N] [--json] [--port PORT]
    check_ssl.py --help

Examples:
    check_ssl.py example.com
    check_ssl.py example.com google.com --warn-days 30
    check_ssl.py internal.host --port 8443 --json
"""

import argparse
import json
import socket
import ssl
import sys
from datetime import datetime, timezone


def check_certificate(domain: str, port: int = 443, timeout: int = 10) -> dict:
    """Fetch SSL certificate info for a domain."""
    result = {
        "domain": domain,
        "port": port,
        "status": "ok",
        "error": None,
        "subject": None,
        "issuer": None,
        "not_before": None,
        "not_after": None,
        "days_remaining": None,
        "serial": None,
        "san": [],
        "protocol": None,
    }

    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                result["protocol"] = ssock.version()

                # Subject
                subject = dict(x[0] for x in cert.get("subject", ()))
                result["subject"] = subject.get("commonName", "N/A")

                # Issuer
                issuer = dict(x[0] for x in cert.get("issuer", ()))
                result["issuer"] = issuer.get("organizationName", issuer.get("commonName", "N/A"))

                # Dates
                not_before = cert.get("notBefore")
                not_after = cert.get("notAfter")

                if not_before:
                    nb = datetime.strptime(not_before, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                    result["not_before"] = nb.isoformat()

                if not_after:
                    na = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                    result["not_after"] = na.isoformat()
                    now = datetime.now(timezone.utc)
                    delta = na - now
                    result["days_remaining"] = delta.days

                    if delta.days < 0:
                        result["status"] = "expired"
                    elif delta.days == 0:
                        result["status"] = "expires_today"

                # Serial
                result["serial"] = cert.get("serialNumber", "N/A")

                # SAN
                san_entries = cert.get("subjectAltName", ())
                result["san"] = [entry[1] for entry in san_entries if entry[0] == "DNS"]

    except ssl.SSLCertVerificationError as e:
        result["status"] = "verification_failed"
        result["error"] = str(e)
    except ssl.SSLError as e:
        result["status"] = "ssl_error"
        result["error"] = str(e)
    except socket.timeout:
        result["status"] = "timeout"
        result["error"] = f"Connection timed out after {timeout}s"
    except socket.gaierror as e:
        result["status"] = "dns_error"
        result["error"] = f"DNS resolution failed: {e}"
    except ConnectionRefusedError:
        result["status"] = "connection_refused"
        result["error"] = f"Connection refused on port {port}"
    except OSError as e:
        result["status"] = "connection_error"
        result["error"] = str(e)

    return result


def status_icon(status: str, days: int | None, warn_days: int) -> str:
    """Return a status indicator."""
    if status == "expired":
        return "[EXPIRED]"
    if status == "expires_today":
        return "[EXPIRING]"
    if status not in ("ok",):
        return "[FAIL]"
    if days is not None and days <= warn_days:
        return "[WARN]"
    return "[OK]"


def print_report(results: list[dict], warn_days: int) -> None:
    """Print a human-readable report."""
    print(f"\n{'='*65}")
    print(f"  SSL CERTIFICATE CHECK — {len(results)} domain(s)")
    print(f"{'='*65}")

    for r in results:
        icon = status_icon(r["status"], r["days_remaining"], warn_days)
        print(f"\n  {icon} {r['domain']}:{r['port']}")

        if r["error"]:
            print(f"    Error: {r['error']}")
            continue

        print(f"    Subject:   {r['subject']}")
        print(f"    Issuer:    {r['issuer']}")
        print(f"    Protocol:  {r['protocol']}")
        print(f"    Valid:     {r['not_before']} → {r['not_after']}")

        days = r["days_remaining"]
        if days is not None:
            if days < 0:
                print(f"    Expiry:    EXPIRED {abs(days)} days ago")
            elif days == 0:
                print(f"    Expiry:    EXPIRES TODAY")
            elif days <= warn_days:
                print(f"    Expiry:    {days} days remaining (below {warn_days}-day threshold)")
            else:
                print(f"    Expiry:    {days} days remaining")

        if r["san"]:
            san_display = r["san"][:5]
            extra = len(r["san"]) - 5
            san_str = ", ".join(san_display)
            if extra > 0:
                san_str += f" (+{extra} more)"
            print(f"    SANs:      {san_str}")

    # Summary
    ok = sum(1 for r in results if r["status"] == "ok" and (r["days_remaining"] is None or r["days_remaining"] > warn_days))
    warn = sum(1 for r in results if r["status"] == "ok" and r["days_remaining"] is not None and 0 < r["days_remaining"] <= warn_days)
    fail = sum(1 for r in results if r["status"] not in ("ok",))
    expired = sum(1 for r in results if r["status"] in ("expired", "expires_today"))

    print(f"\n  SUMMARY: {ok} ok, {warn} warning, {expired} expired, {fail} failed")
    print(f"{'='*65}\n")

    # Exit code
    if expired > 0 or fail > 0:
        sys.exit(2)
    elif warn > 0:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Check SSL certificate expiry, issuer, and chain for one or more domains.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s example.com\n"
               "  %(prog)s example.com google.com --warn-days 30\n"
               "  %(prog)s internal.host --port 8443 --json\n",
    )
    parser.add_argument("domains", nargs="+", help="Domain(s) to check")
    parser.add_argument("--warn-days", type=int, default=14, help="Warning threshold in days (default: 14)")
    parser.add_argument("--port", type=int, default=443, help="Port to connect to (default: 443)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--timeout", type=int, default=10, help="Connection timeout in seconds (default: 10)")

    args = parser.parse_args()

    results = []
    for domain in args.domains:
        # Strip protocol prefix if provided
        domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
        r = check_certificate(domain, port=args.port, timeout=args.timeout)
        results.append(r)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results, args.warn_days)


if __name__ == "__main__":
    main()
