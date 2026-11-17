"""Focused request-body validation for Fulfillment Inbound operations.

The gateway still treats Amazon's OpenAPI model as the source of truth.  These
checks catch the high-value, deterministic mistakes that would otherwise spend
one billable request (missing keys, wrong container types, and documented list
limits) without trying to duplicate every nested Amazon schema.
"""

from __future__ import annotations

from typing import Any, Callable


class ValidationError(ValueError):
    """Raised when a request cannot satisfy the documented API contract."""


def _object(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{field} must be an object")
    return value


def _array(
    value: Any,
    field: str,
    *,
    minimum: int = 0,
    maximum: int | None = None,
) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{field} must be an array")
    if len(value) < minimum:
        raise ValidationError(f"{field} must contain at least {minimum} item(s)")
    if maximum is not None and len(value) > maximum:
        raise ValidationError(f"{field} must contain at most {maximum} item(s)")
    return value


def _required(obj: dict[str, Any], field: str, parent: str) -> Any:
    if field not in obj or obj[field] is None:
        raise ValidationError(f"Missing required field: {parent}.{field}")
    if isinstance(obj[field], str) and not obj[field].strip():
        raise ValidationError(f"{parent}.{field} must not be blank")
    return obj[field]


def _string_length(value: Any, field: str, minimum: int, maximum: int) -> None:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    size = len(value)
    if size < minimum or size > maximum:
        raise ValidationError(f"{field} length must be between {minimum} and {maximum}")


def _integer_range(value: Any, field: str, minimum: int, maximum: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{field} must be an integer")
    if value < minimum or value > maximum:
        raise ValidationError(f"{field} must be between {minimum} and {maximum}")


def _validate_item(item: Any, field: str) -> None:
    obj = _object(item, field)
    for required in ("labelOwner", "msku", "prepOwner", "quantity"):
        _required(obj, required, field)
    _string_length(obj["msku"], f"{field}.msku", 1, 255)
    _integer_range(obj["quantity"], f"{field}.quantity", 1, 500_000)


def _validate_address(value: Any, field: str) -> None:
    address = _object(value, field)
    limits = {
        "addressLine1": (1, 180),
        "city": (1, 30),
        "countryCode": (2, 2),
        "name": (1, 50),
        "phoneNumber": (1, 20),
        "postalCode": (1, 32),
    }
    for name, (minimum, maximum) in limits.items():
        _string_length(_required(address, name, field), f"{field}.{name}", minimum, maximum)
    if not all("A" <= char <= "Z" for char in address["countryCode"]):
        raise ValidationError(f"{field}.countryCode must be a two-letter uppercase country code")


def create_inbound_plan(request: dict[str, Any]) -> None:
    destinations = _array(
        request["destinationMarketplaces"],
        "requestBody.destinationMarketplaces",
        minimum=1,
        maximum=1,
    )
    _string_length(destinations[0], "requestBody.destinationMarketplaces[0]", 1, 20)
    items = _array(request["items"], "requestBody.items", minimum=1, maximum=2000)
    for index, item in enumerate(items):
        _validate_item(item, f"requestBody.items[{index}]")
    _validate_address(request["sourceAddress"], "requestBody.sourceAddress")
    if "name" in request:
        _string_length(request["name"], "requestBody.name", 1, 40)


def update_inbound_plan_name(request: dict[str, Any]) -> None:
    _string_length(request["name"], "requestBody.name", 1, 40)


def update_shipment_name(request: dict[str, Any]) -> None:
    _string_length(request["name"], "requestBody.name", 1, 100)


def shipment_source_address(request: dict[str, Any]) -> None:
    _validate_address(request["address"], "requestBody.address")


def set_packing_information(request: dict[str, Any]) -> None:
    groups = _array(
        request["packageGroupings"],
        "requestBody.packageGroupings",
        minimum=1,
    )
    for index, value in enumerate(groups):
        field = f"requestBody.packageGroupings[{index}]"
        group = _object(value, field)
        boxes = _array(_required(group, "boxes", field), f"{field}.boxes", minimum=1, maximum=5000)
        identifiers = [group.get("packingGroupId"), group.get("shipmentId")]
        if sum(value is not None and str(value).strip() != "" for value in identifiers) != 1:
            raise ValidationError(f"{field} must include exactly one of packingGroupId or shipmentId")
        for box_index, box_value in enumerate(boxes):
            box_field = f"{field}.boxes[{box_index}]"
            box = _object(box_value, box_field)
            for required in ("contentInformationSource", "dimensions", "quantity", "weight"):
                _required(box, required, box_field)
            _integer_range(box["quantity"], f"{box_field}.quantity", 1, 10_000)


def shipment_content_update(request: dict[str, Any]) -> None:
    boxes = _array(request["boxes"], "requestBody.boxes", minimum=1, maximum=5000)
    items = _array(request["items"], "requestBody.items", minimum=1, maximum=2000)
    for index, box in enumerate(boxes):
        _object(box, f"requestBody.boxes[{index}]")
    for index, item in enumerate(items):
        _validate_item(item, f"requestBody.items[{index}]")


def tracking_details(request: dict[str, Any]) -> None:
    details = _object(request["trackingDetails"], "requestBody.trackingDetails")
    ltl = details.get("ltlTrackingDetail")
    spd = details.get("spdTrackingDetail")
    if ltl is None and spd is None:
        raise ValidationError(
            "requestBody.trackingDetails must include ltlTrackingDetail or spdTrackingDetail"
        )
    if ltl is not None and spd is not None:
        raise ValidationError(
            "requestBody.trackingDetails must not include both ltlTrackingDetail and spdTrackingDetail"
        )
    if ltl is not None:
        ltl_obj = _object(ltl, "requestBody.trackingDetails.ltlTrackingDetail")
        bills = _array(
            _required(ltl_obj, "freightBillNumber", "requestBody.trackingDetails.ltlTrackingDetail"),
            "requestBody.trackingDetails.ltlTrackingDetail.freightBillNumber",
            minimum=1,
            maximum=1,
        )
        _string_length(
            bills[0],
            "requestBody.trackingDetails.ltlTrackingDetail.freightBillNumber[0]",
            1,
            64,
        )
    if spd is not None:
        spd_obj = _object(spd, "requestBody.trackingDetails.spdTrackingDetail")
        _array(
            _required(spd_obj, "spdTrackingItems", "requestBody.trackingDetails.spdTrackingDetail"),
            "requestBody.trackingDetails.spdTrackingDetail.spdTrackingItems",
        )


def transportation_configurations(request: dict[str, Any]) -> None:
    configurations = _array(
        request["shipmentTransportationConfigurations"],
        "requestBody.shipmentTransportationConfigurations",
        minimum=1,
    )
    for index, value in enumerate(configurations):
        field = f"requestBody.shipmentTransportationConfigurations[{index}]"
        configuration = _object(value, field)
        _required(configuration, "shipmentId", field)
        _object(_required(configuration, "readyToShipWindow", field), f"{field}.readyToShipWindow")


def transportation_selections(request: dict[str, Any]) -> None:
    selections = _array(
        request["transportationSelections"],
        "requestBody.transportationSelections",
        minimum=1,
    )
    for index, value in enumerate(selections):
        field = f"requestBody.transportationSelections[{index}]"
        selection = _object(value, field)
        _required(selection, "shipmentId", field)
        _required(selection, "transportationOptionId", field)


def marketplace_item_labels(request: dict[str, Any]) -> None:
    quantities = _array(
        request["mskuQuantities"],
        "requestBody.mskuQuantities",
        minimum=1,
        maximum=100,
    )
    for index, value in enumerate(quantities):
        field = f"requestBody.mskuQuantities[{index}]"
        item = _object(value, field)
        _string_length(_required(item, "msku", field), f"{field}.msku", 1, 255)
        _integer_range(_required(item, "quantity", field), f"{field}.quantity", 1, 10_000)


def prep_details(request: dict[str, Any]) -> None:
    details = _array(
        request["mskuPrepDetails"],
        "requestBody.mskuPrepDetails",
        minimum=1,
        maximum=100,
    )
    for index, value in enumerate(details):
        field = f"requestBody.mskuPrepDetails[{index}]"
        item = _object(value, field)
        _string_length(_required(item, "msku", field), f"{field}.msku", 1, 255)
        _required(item, "prepCategory", field)
        _array(_required(item, "prepTypes", field), f"{field}.prepTypes")


VALIDATORS: dict[str, Callable[[dict[str, Any]], None]] = {
    "create_inbound_plan": create_inbound_plan,
    "marketplace_item_labels": marketplace_item_labels,
    "prep_details": prep_details,
    "set_packing_information": set_packing_information,
    "shipment_content_update": shipment_content_update,
    "shipment_source_address": shipment_source_address,
    "tracking_details": tracking_details,
    "transportation_configurations": transportation_configurations,
    "transportation_selections": transportation_selections,
    "update_inbound_plan_name": update_inbound_plan_name,
    "update_shipment_name": update_shipment_name,
}


def validate_request_body(validator_name: str | None, request: dict[str, Any]) -> None:
    if not validator_name:
        return
    try:
        validator = VALIDATORS[validator_name]
    except KeyError as exc:  # fail fast for a broken local registry
        raise RuntimeError(f"Unknown request-body validator: {validator_name}") from exc
    validator(request)
