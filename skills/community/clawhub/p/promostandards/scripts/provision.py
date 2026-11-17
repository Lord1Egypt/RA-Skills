"""Provisioning: company code -> validated config + capability list.

Adding a PromoStandards supplier is meant to be a data-entry operation, and
this is the data entry. Given a registry company code it emits a ready
config file plus the capability array a drive-thru listing consumes.

Credentials are never written into the output. The generated config carries
`${ENV_VAR}` references, with names derived from the supplier code so two
suppliers cannot collide.

One config serves both deployments, because both authenticate the same way:
a single-tenant host exports those vars at boot, and on a delegated
agent-to-agent turn the platform injects the calling agent's shared
credentials under the same names, for that turn only. There is deliberately
no credential-free variant — a config with no `credentials` block has no env
var to resolve, so a delegated turn has nowhere to land and every call
fails.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

import config as config_module
import registry
from config import SupplierConfig
from errors import PromoStandardsError


def env_var_name(supplier: str, suffix: str) -> str:
    """Derive a stable env var name, e.g. 'SanMar' -> PS_SANMAR_ID."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", supplier).strip("_").upper()
    return f"PS_{slug}_{suffix}"


def build_config(company_code: str, *, dump_path: str | None = None,
                 services: list[str] | None = None) -> dict:
    """Generate a supplier config from the registry.

    Only services with a working adapter are written into `services`;
    everything else the supplier publishes is reported separately so the
    gap is visible rather than silently dropped.

    The credentials block is always written, and always as `${ENV_VAR}`
    references — it carries no identity of its own, so the same file is
    safe to commit and safe to share between callers.
    """
    capabilities = registry.capabilities_for(company_code, path=dump_path)
    if not capabilities:
        raise PromoStandardsError(
            f"company '{company_code}' publishes no endpoints in the registry"
        )

    code, _ = registry.find_company(registry.load_dump(dump_path), company_code)
    chosen = registry.best_endpoints(capabilities)

    wanted = {s.upper() for s in services} if services else None
    service_map = {}
    skipped = []
    for service, capability in sorted(chosen.items()):
        if wanted and service not in wanted:
            continue
        if not capability.supported:
            skipped.append({
                "service": service,
                "version": capability.version,
                "reason": "no adapter for this version",
            })
            continue
        entry = {"url": capability.url, "wsVersion": capability.version}
        if capability.test_url:
            entry["testUrl"] = capability.test_url
        if capability.status:
            entry["status"] = capability.status
        service_map[service] = entry

    config: dict = {
        "supplier": code,
        "credentials": {
            "id": "${" + env_var_name(code, "ID") + "}",
            "password": "${" + env_var_name(code, "PASSWORD") + "}",
        },
    }
    return {
        **config,
        "services": service_map,
        "_capabilities": registry.summarize(capabilities),
        "_skipped": skipped,
    }


def validate(config_dict: dict) -> dict:
    """Load the generated config and report what it can actually do.

    Runs the same parsing path the client uses, so a config that validates
    here is one the client will accept — including the credential check,
    which reports whether the env vars are present without printing them.
    """
    findings = []
    try:
        loaded = SupplierConfig.from_dict(config_dict)
    except PromoStandardsError as exc:
        return {"valid": False, "errors": [exc.as_dict()]}

    if not loaded.credential_id:
        env = loaded.credential_env.get("id")
        findings.append(
            f"credential env var {env} is not set — expected when "
            "provisioning, since a delegated turn supplies it at call time; "
            "a single-tenant host must export it"
            if env else
            "no 'credentials' block — nothing can authenticate this config, "
            "and a delegated turn has no env var to land in"
        )
    if not loaded.services:
        findings.append("no drivable services: nothing to provision")

    for service in sorted(loaded.services):
        endpoint = loaded.services[service]
        if endpoint.test_url_is_production:
            findings.append(
                f"{service} registers a test endpoint identical to its "
                "production URL — this supplier has no test environment"
                + (". Test PO submissions will be REFUSED rather than sent "
                   "to production; every accepted PO is a real order"
                   if service == "PO" else "")
            )
        elif service == "PO" and not endpoint.has_test_endpoint:
            findings.append(
                "PO has no registered test endpoint; test submissions will "
                "be refused rather than sent to production"
            )
        if endpoint.status and endpoint.status.lower() == "deprecated":
            findings.append(f"{service} endpoint is marked Deprecated")

    return {
        "valid": True,
        "config": loaded.describe(),
        "warnings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("company_code",
                        help="registry company code, e.g. SanMar")
    parser.add_argument("-o", "--output",
                        help="write the config here (default: stdout)")
    parser.add_argument("--bundle", metavar="NAME", nargs="?", const="",
                        help="write into the skill's assets/suppliers/ as "
                             "NAME.json (default: the company code, "
                             "lower-cased) so it ships with the skill and "
                             "survives a workspace reset. Commit the result")
    parser.add_argument("-d", "--dump", help="path to the registry dump")
    parser.add_argument("-s", "--service", action="append",
                        help="limit to these services (repeatable)")
    parser.add_argument("--validate", action="store_true",
                        help="also validate and report warnings")
    args = parser.parse_args(argv)

    try:
        config_dict = build_config(args.company_code, dump_path=args.dump,
                                   services=args.service)
    except PromoStandardsError as exc:
        print(json.dumps({"error": exc.as_dict()}), file=sys.stderr)
        return 2

    report = {"config": config_dict}
    if args.validate:
        report["validation"] = validate(config_dict)

    destination = args.output
    if args.bundle is not None:
        name = re.sub(r"[^a-z0-9]+", "",
                      (args.bundle or config_dict["supplier"]).lower())
        if not name:
            print(json.dumps({"error": {
                "type": "bad_input",
                "message": f"--bundle name '{args.bundle}' has no usable "
                           "characters",
            }}), file=sys.stderr)
            return 2
        os.makedirs(config_module.BUNDLED_SUPPLIER_DIR, exist_ok=True)
        destination = os.path.join(config_module.BUNDLED_SUPPLIER_DIR,
                                   f"{name}.json")

    text = json.dumps(config_dict, indent=2)
    if destination:
        with open(destination, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print(f"wrote {destination}", file=sys.stderr)
        if args.bundle is not None:
            print(f"reference it as {{\"config\": \"{name}\"}} — commit the "
                  "file so it ships with the skill", file=sys.stderr)
        if args.validate:
            print(json.dumps(report["validation"], indent=2))
    else:
        print(json.dumps(report if args.validate else config_dict, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
