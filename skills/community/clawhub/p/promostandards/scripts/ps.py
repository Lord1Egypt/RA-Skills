#!/usr/bin/env python3
"""PromoStandards skill entrypoint.

    ps.py <action> < payload.json

Every action takes a `config` (path to a supplier config file) or an inline
`configJson` object, plus action-specific fields.

    echo '{"config":"sanmar.json","productId":"PC61"}' | ps.py get-inventory

Authentication is always environmental: the config carries `${ENV_VAR}`
references that are resolved from this process's environment at load time.
Credentials are never passed on stdin — on a delegated (agent-to-agent)
turn the platform injects the calling agent's shared credentials into this
process's environment before the script runs, and the agent composing the
payload above is deliberately never shown their values. See the
"Delegated turns" section of SKILL.md.

Actions:
    capabilities        what this supplier can do (no network)
    get-inventory       stock levels, per-warehouse where the version allows
    get-inventory-filters
    get-product         normalized product + parts
    get-products-modified
    get-closeout
    get-fob-points
    get-pricing         configured pricing (resolves a FOB point if needed)
    get-decoration-locations
    preview-po          render PO XML without sending (dry run)
    send-po             submit a PO; test endpoint unless allowProduction
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import emit, fail, fail_from, read_stdin_json, require  # noqa: E402
from client import PromoStandardsClient  # noqa: E402
from config import SupplierConfig  # noqa: E402
from errors import PromoStandardsError  # noqa: E402


def _client(payload: dict) -> PromoStandardsClient:
    if payload.get("configJson"):
        config = SupplierConfig.from_dict(payload["configJson"])
    elif payload.get("config"):
        config = SupplierConfig.load(payload["config"])
    else:
        fail("bad_input", "provide 'config' (path) or 'configJson' (object)")

    # No credential handling here by design: identity arrives in the
    # environment (see the module docstring), which SupplierConfig already
    # resolved above. A 'credentials' object on stdin is rejected rather
    # than honoured — on a delegated turn the only party able to put one
    # there is a model that should never have seen the values.
    if payload.get("credentials"):
        fail("bad_input",
             "credentials are not accepted on stdin; they are read from the "
             "environment via the config's '${ENV_VAR}' references. On a "
             "delegated turn the runtime injects them for you.")

    return PromoStandardsClient(
        config,
        timeout=int(payload.get("timeout") or 60),
        use_test=bool(payload.get("useTest")),
    )


def action_capabilities(payload: dict) -> None:
    emit(_client(payload).capabilities())


def action_get_inventory(payload: dict) -> None:
    (product_id,) = require(payload, "productId")
    result = _client(payload).get_inventory(
        product_id,
        part_ids=payload.get("partIds"),
        colors=payload.get("colors"),
        sizes=payload.get("sizes"),
    )
    emit(result.to_dict())


def action_get_inventory_filters(payload: dict) -> None:
    (product_id,) = require(payload, "productId")
    emit(_client(payload).get_inventory_filters(product_id))


def action_get_product(payload: dict) -> None:
    (product_id,) = require(payload, "productId")
    result = _client(payload).get_product(
        product_id,
        part_id=payload.get("partId"),
        color=payload.get("color"),
        country=payload.get("country") or "US",
        language=payload.get("language") or "EN",
    )
    emit(result.to_dict())


def action_get_products_modified(payload: dict) -> None:
    (since,) = require(payload, "since")
    emit(_client(payload).get_products_modified_since(since))


def action_get_closeout(payload: dict) -> None:
    emit(_client(payload).get_closeout_products())


def action_get_fob_points(payload: dict) -> None:
    emit({"fob_points": _client(payload).get_fob_points(
        payload.get("productId"))})


def action_get_pricing(payload: dict) -> None:
    (product_id,) = require(payload, "productId")
    grids = _client(payload).get_pricing(
        product_id,
        fob_id=payload.get("fobId"),
        currency=payload.get("currency") or "USD",
        price_type=payload.get("priceType") or "Net",
        part_id=payload.get("partId"),
    )
    emit({"price_grids": [g.to_dict() for g in grids]})


def action_get_decoration_locations(payload: dict) -> None:
    (product_id,) = require(payload, "productId")
    locations = _client(payload).get_decoration_locations(product_id)
    emit({"locations": [loc.to_dict() for loc in locations]})


def action_preview_po(payload: dict) -> None:
    (po,) = require(payload, "po")
    emit({"xml": _client(payload).preview_purchase_order(po)})


def action_send_po(payload: dict) -> None:
    (po,) = require(payload, "po")
    allow_production = bool(payload.get("allowProduction"))
    result = _client(payload).send_purchase_order(
        po, allow_production=allow_production
    )
    emit(result.to_dict())


ACTIONS = {
    "capabilities": action_capabilities,
    "get-inventory": action_get_inventory,
    "get-inventory-filters": action_get_inventory_filters,
    "get-product": action_get_product,
    "get-products-modified": action_get_products_modified,
    "get-closeout": action_get_closeout,
    "get-fob-points": action_get_fob_points,
    "get-pricing": action_get_pricing,
    "get-decoration-locations": action_get_decoration_locations,
    "preview-po": action_preview_po,
    "send-po": action_send_po,
}


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    action = ACTIONS.get(argv[1])
    if action is None:
        fail("unknown_action",
             f"unknown action '{argv[1]}'; expected one of "
             f"{', '.join(sorted(ACTIONS))}")
    payload = read_stdin_json()
    try:
        action(payload)
    except PromoStandardsError as exc:
        # escalation_required exits 3 so a caller can branch on it directly.
        fail_from(exc, exit_code=3 if exc.kind == "escalation_required" else 1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
