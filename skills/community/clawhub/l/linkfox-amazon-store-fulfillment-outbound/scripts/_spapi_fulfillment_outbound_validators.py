"""Focused request validators for Fulfillment Outbound v2026-07-04."""

from __future__ import annotations

import re
from typing import Any, Callable


class ValidationError(ValueError):
    """Raised before a malformed or unsupported request reaches the gateway."""


def _object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{field} must be an object")
    return value


def _array(value: Any, field: str, *, minimum: int = 1) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValidationError(f"{field} must contain at least {minimum} item(s)")
    return value


def _required(obj: dict[str, Any], field: str, parent: str) -> Any:
    if field not in obj or obj[field] is None:
        raise ValidationError(f"Missing required field: {parent}.{field}")
    if isinstance(obj[field], str) and not obj[field].strip():
        raise ValidationError(f"{parent}.{field} must not be blank")
    return obj[field]


def _country_code(value: Any, field: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"[A-Z]{2}", value) is None:
        raise ValidationError(f"{field} must be a two-letter uppercase country code")


def _product_identifier(value: Any, field: str) -> None:
    product = _object(value, field)
    amazon_sku = _required(product, "amazonSku", field)
    if not isinstance(amazon_sku, str):
        raise ValidationError(f"{field}.amazonSku must be a string")


def _amount(value: Any, field: str) -> None:
    amount = _object(value, field)
    decimal_value = _required(amount, "value", field)
    if not isinstance(decimal_value, str):
        raise ValidationError(f"{field}.value must be a string decimal")
    if "unit" in amount and amount["unit"] != "EACHES":
        raise ValidationError(f"{field}.unit must be EACHES when supplied")


def _address(value: Any, field: str) -> None:
    address = _object(value, field)
    for required in ("addressLine1", "countryCode", "name", "postalCode"):
        _required(address, required, field)
    _country_code(address["countryCode"], f"{field}.countryCode")


def _origin(value: Any, field: str) -> None:
    origin = _object(value, field)
    _country_code(_required(origin, "countryCode", field), f"{field}.countryCode")


def _preview_line_items(values: Any) -> None:
    for index, value in enumerate(_array(values, "requestBody.lineItems")):
        field = f"requestBody.lineItems[{index}]"
        item = _object(value, field)
        product = _object(_required(item, "product", field), f"{field}.product")
        _product_identifier(
            _required(product, "productIdentifier", f"{field}.product"),
            f"{field}.product.productIdentifier",
        )
        _amount(_required(item, "amount", field), f"{field}.amount")


def order_preview(request: dict[str, Any]) -> None:
    destination = _object(request["destination"], "requestBody.destination")
    _address(
        _required(destination, "deliveryAddress", "requestBody.destination"),
        "requestBody.destination.deliveryAddress",
    )
    _preview_line_items(request["lineItems"])
    if "origin" in request:
        _origin(request["origin"], "requestBody.origin")


def offers(request: dict[str, Any]) -> None:
    _origin(request["origin"], "requestBody.origin")
    for index, value in enumerate(_array(request["items"], "requestBody.items")):
        field = f"requestBody.items[{index}]"
        item = _object(value, field)
        _product_identifier(
            _required(item, "productIdentifier", field),
            f"{field}.productIdentifier",
        )


def create_order(request: dict[str, Any]) -> None:
    order_id = request["orderId"]
    if not isinstance(order_id, str) or not order_id.strip():
        raise ValidationError("requestBody.orderId must be a non-empty string")
    destination = _object(request["destination"], "requestBody.destination")
    _address(
        _required(destination, "deliveryAddress", "requestBody.destination"),
        "requestBody.destination.deliveryAddress",
    )
    seen: set[str] = set()
    for index, value in enumerate(_array(request["lineItems"], "requestBody.lineItems")):
        field = f"requestBody.lineItems[{index}]"
        item = _object(value, field)
        line_item_id = _required(item, "lineItemId", field)
        if not isinstance(line_item_id, str) or not line_item_id.strip():
            raise ValidationError(f"{field}.lineItemId must be a non-empty string")
        if line_item_id in seen:
            raise ValidationError(f"{field}.lineItemId must be unique within the order")
        seen.add(line_item_id)
        product = _object(_required(item, "product", field), f"{field}.product")
        _product_identifier(
            _required(product, "productIdentifier", f"{field}.product"),
            f"{field}.product.productIdentifier",
        )
        _amount(_required(item, "amount", field), f"{field}.amount")


def update_order(request: dict[str, Any]) -> None:
    configuration = request.get("fulfillmentConfiguration")
    if configuration is None:
        return
    configuration = _object(configuration, "requestBody.fulfillmentConfiguration")
    if "action" in configuration and configuration["action"] not in {"SHIP", "HOLD"}:
        raise ValidationError("requestBody.fulfillmentConfiguration.action must be SHIP or HOLD")


def order_status(request: dict[str, Any]) -> None:
    allowed = {"PROCESSING", "COMPLETE", "COMPLETE_PARTIAL", "CANCELLED", "UNFULFILLABLE", "INVALID"}
    if request["status"] not in allowed:
        raise ValidationError("requestBody.status must be a documented Fulfillment Outbound order status")


def package_update(request: dict[str, Any]) -> None:
    allowed = {"PROCESSING", "IN_TRANSIT", "DELAYED", "OUT_FOR_DELIVERY", "DELIVERED", "UNDELIVERABLE", "EXPIRED"}
    if request["status"] not in allowed:
        raise ValidationError("requestBody.status must be a documented package status")
    tracking = request.get("tracking")
    if tracking is not None:
        tracking = _object(tracking, "requestBody.tracking")
        carrier = tracking.get("carrier")
        if carrier is not None:
            carrier = _object(carrier, "requestBody.tracking.carrier")
            _required(carrier, "carrierCode", "requestBody.tracking.carrier")


VALIDATORS: dict[str, Callable[[dict[str, Any]], None]] = {
    "create_order": create_order,
    "offers": offers,
    "order_preview": order_preview,
    "order_status": order_status,
    "package_update": package_update,
    "update_order": update_order,
}


def validate_request_body(validator_name: str | None, request: dict[str, Any]) -> None:
    if not validator_name:
        return
    try:
        validator = VALIDATORS[validator_name]
    except KeyError as exc:
        raise RuntimeError(f"Unknown request-body validator: {validator_name}") from exc
    validator(request)
