"""Operation registry for Amazon Fulfillment Inbound SP-API.

The registry is intentionally declarative: public entry scripts select one
operation by ID, while the shared runner owns validation and request building.
Paths and wire parameter names follow Amazon's official v2024-03-20 and v0
OpenAPI models.
"""

from __future__ import annotations

from typing import Any


V2024_PATH_PARAM_RULES: dict[str, dict[str, Any]] = {
    "contentUpdatePreviewId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "deliveryWindowOptionId": {"minLength": 36, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "inboundPlanId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "operationId": {"minLength": 36, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "packingGroupId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "packingOptionId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "placementOptionId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "shipmentId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
    "slotId": {"minLength": 38, "maxLength": 38, "pattern": r"^[a-zA-Z0-9-]*$"},
}


def query(
    name: str,
    *,
    wire: str | None = None,
    required: bool = False,
    kind: str = "string",
    enum: tuple[str, ...] = (),
    minimum: int | None = None,
    maximum: int | None = None,
    min_items: int | None = None,
    max_items: int | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | None = None,
    value_format: str | None = None,
    collection: str = "single",
) -> dict[str, Any]:
    return {
        "name": name,
        "wire": wire or name,
        "required": required,
        "kind": kind,
        "enum": enum,
        "minimum": minimum,
        "maximum": maximum,
        "minItems": min_items,
        "maxItems": max_items,
        "minLength": min_length,
        "maxLength": max_length,
        "pattern": pattern,
        "format": value_format,
        "collection": collection,
    }


def body(*required_keys: str, allow_empty: bool = False, validator: str | None = None) -> dict[str, Any]:
    return {
        "required": True,
        "requiredKeys": required_keys,
        "allowEmpty": allow_empty,
        "validator": validator,
    }


def operation(
    operation_id: str,
    method: str,
    path: str,
    *,
    path_params: tuple[str, ...] = (),
    query_params: tuple[dict[str, Any], ...] = (),
    request_body: dict[str, Any] | None = None,
    success: tuple[int, ...] = (200,),
    result_key: str = "result",
    execution: str = "sync",
    risk: str = "read",
    version: str = "2024-03-20",
) -> dict[str, Any]:
    return {
        "operationId": operation_id,
        "script": camel_to_snake(operation_id) + ".py",
        "version": version,
        "method": method,
        "path": path,
        "pathParams": path_params,
        "pathParamRules": {
            name: V2024_PATH_PARAM_RULES[name]
            for name in path_params
            if version == "2024-03-20" and name in V2024_PATH_PARAM_RULES
        },
        "queryParams": query_params,
        "requestBody": request_body,
        "successStatuses": success,
        "resultKey": result_key,
        "execution": execution,
        "risk": risk,
    }


def camel_to_snake(value: str) -> str:
    out: list[str] = []
    for index, char in enumerate(value):
        if char.isupper() and index:
            out.append("_")
        out.append(char.lower())
    return "".join(out)


def paging(maximum: int) -> tuple[dict[str, Any], ...]:
    return (
        query("pageSize", kind="integer", minimum=1, maximum=maximum),
        query("paginationToken", min_length=0, max_length=1024),
    )


PLAN = "inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}"
SHIPMENT = PLAN + "/shipments/{shipmentId}"


OPERATION_SPECS: dict[str, dict[str, Any]] = {}


def register(spec: dict[str, Any]) -> None:
    operation_id = spec["operationId"]
    if operation_id in OPERATION_SPECS:
        raise ValueError(f"Duplicate operationId: {operation_id}")
    OPERATION_SPECS[operation_id] = spec


# Inbound plans
register(operation(
    "listInboundPlans", "GET", "inbound/fba/2024-03-20/inboundPlans",
    query_params=paging(30) + (
        query("status", enum=("ACTIVE", "VOIDED", "SHIPPED")),
        query("sortBy", enum=("LAST_UPDATED_TIME", "CREATION_TIME")),
        query("sortOrder", enum=("ASC", "DESC")),
    ), result_key="inboundPlans",
))
register(operation(
    "createInboundPlan", "POST", "inbound/fba/2024-03-20/inboundPlans",
    request_body=body("destinationMarketplaces", "items", "sourceAddress", validator="create_inbound_plan"),
    success=(202,), result_key="inboundPlanCreation", execution="async", risk="write",
))
register(operation(
    "getInboundPlan", "GET", PLAN, path_params=("inboundPlanId",), result_key="inboundPlan",
))
register(operation(
    "listInboundPlanBoxes", "GET", PLAN + "/boxes", path_params=("inboundPlanId",),
    query_params=paging(1000), result_key="boxes",
))
register(operation(
    "cancelInboundPlan", "PUT", PLAN + "/cancellation", path_params=("inboundPlanId",),
    success=(202,), result_key="operation", execution="async", risk="commit",
))
register(operation(
    "listInboundPlanItems", "GET", PLAN + "/items", path_params=("inboundPlanId",),
    query_params=paging(1000), result_key="items",
))
register(operation(
    "updateInboundPlanName", "PUT", PLAN + "/name", path_params=("inboundPlanId",),
    request_body=body("name", validator="update_inbound_plan_name"), success=(204,),
    result_key="nameUpdate", risk="write",
))

# Packing
register(operation(
    "listPackingGroupBoxes", "GET", PLAN + "/packingGroups/{packingGroupId}/boxes",
    path_params=("inboundPlanId", "packingGroupId"), query_params=paging(100), result_key="boxes",
))
register(operation(
    "listPackingGroupItems", "GET", PLAN + "/packingGroups/{packingGroupId}/items",
    path_params=("inboundPlanId", "packingGroupId"), query_params=paging(100), result_key="items",
))
register(operation(
    "setPackingInformation", "POST", PLAN + "/packingInformation", path_params=("inboundPlanId",),
    request_body=body("packageGroupings", validator="set_packing_information"), success=(202,),
    result_key="operation", execution="async", risk="write",
))
register(operation(
    "listPackingOptions", "GET", PLAN + "/packingOptions", path_params=("inboundPlanId",),
    query_params=paging(20), result_key="packingOptions",
))
register(operation(
    "generatePackingOptions", "POST", PLAN + "/packingOptions", path_params=("inboundPlanId",),
    success=(202,), result_key="operation", execution="async", risk="generate",
))
register(operation(
    "confirmPackingOption", "POST", PLAN + "/packingOptions/{packingOptionId}/confirmation",
    path_params=("inboundPlanId", "packingOptionId"), success=(202,), result_key="operation",
    execution="async", risk="commit",
))
register(operation(
    "listInboundPlanPallets", "GET", PLAN + "/pallets", path_params=("inboundPlanId",),
    query_params=paging(1000), result_key="pallets",
))

# Placement
register(operation(
    "listPlacementOptions", "GET", PLAN + "/placementOptions", path_params=("inboundPlanId",),
    query_params=paging(20), result_key="placementOptions",
))
register(operation(
    "generatePlacementOptions", "POST", PLAN + "/placementOptions", path_params=("inboundPlanId",),
    request_body=body(allow_empty=True), success=(202,), result_key="operation",
    execution="async", risk="generate",
))
register(operation(
    "confirmPlacementOption", "POST", PLAN + "/placementOptions/{placementOptionId}/confirmation",
    path_params=("inboundPlanId", "placementOptionId"), success=(202,), result_key="operation",
    execution="async", risk="commit",
))

# Shipments and shipment content updates
register(operation(
    "getShipment", "GET", SHIPMENT, path_params=("inboundPlanId", "shipmentId"), result_key="shipment",
))
register(operation(
    "listShipmentBoxes", "GET", SHIPMENT + "/boxes", path_params=("inboundPlanId", "shipmentId"),
    query_params=paging(1000), result_key="boxes",
))
register(operation(
    "listShipmentContentUpdatePreviews", "GET", SHIPMENT + "/contentUpdatePreviews",
    path_params=("inboundPlanId", "shipmentId"), query_params=paging(20), result_key="contentUpdatePreviews",
))
register(operation(
    "generateShipmentContentUpdatePreviews", "POST", SHIPMENT + "/contentUpdatePreviews",
    path_params=("inboundPlanId", "shipmentId"),
    request_body=body("boxes", "items", validator="shipment_content_update"), success=(202,),
    result_key="operation", execution="async", risk="generate",
))
register(operation(
    "getShipmentContentUpdatePreview", "GET", SHIPMENT + "/contentUpdatePreviews/{contentUpdatePreviewId}",
    path_params=("inboundPlanId", "shipmentId", "contentUpdatePreviewId"), result_key="contentUpdatePreview",
))
register(operation(
    "confirmShipmentContentUpdatePreview", "POST",
    SHIPMENT + "/contentUpdatePreviews/{contentUpdatePreviewId}/confirmation",
    path_params=("inboundPlanId", "shipmentId", "contentUpdatePreviewId"), success=(202,),
    result_key="operation", execution="async", risk="commit",
))
register(operation(
    "getDeliveryChallanDocument", "GET", SHIPMENT + "/deliveryChallanDocument",
    path_params=("inboundPlanId", "shipmentId"), result_key="deliveryChallanDocument",
))
register(operation(
    "listDeliveryWindowOptions", "GET", SHIPMENT + "/deliveryWindowOptions",
    path_params=("inboundPlanId", "shipmentId"), query_params=paging(100), result_key="deliveryWindowOptions",
))
register(operation(
    "generateDeliveryWindowOptions", "POST", SHIPMENT + "/deliveryWindowOptions",
    path_params=("inboundPlanId", "shipmentId"), success=(202,), result_key="operation",
    execution="async", risk="generate",
))
register(operation(
    "confirmDeliveryWindowOptions", "POST",
    SHIPMENT + "/deliveryWindowOptions/{deliveryWindowOptionId}/confirmation",
    path_params=("inboundPlanId", "shipmentId", "deliveryWindowOptionId"), success=(202,),
    result_key="operation", execution="async", risk="commit",
))
register(operation(
    "listShipmentItems", "GET", SHIPMENT + "/items", path_params=("inboundPlanId", "shipmentId"),
    query_params=paging(1000), result_key="items",
))
register(operation(
    "updateShipmentName", "PUT", SHIPMENT + "/name", path_params=("inboundPlanId", "shipmentId"),
    request_body=body("name", validator="update_shipment_name"), success=(204,),
    result_key="nameUpdate", risk="write",
))
register(operation(
    "listShipmentPallets", "GET", SHIPMENT + "/pallets", path_params=("inboundPlanId", "shipmentId"),
    query_params=paging(1000), result_key="pallets",
))
register(operation(
    "cancelSelfShipAppointment", "PUT", SHIPMENT + "/selfShipAppointmentCancellation",
    path_params=("inboundPlanId", "shipmentId"), request_body=body(allow_empty=True), success=(202,),
    result_key="operation", execution="async", risk="commit",
))
register(operation(
    "getSelfShipAppointmentSlots", "GET", SHIPMENT + "/selfShipAppointmentSlots",
    path_params=("inboundPlanId", "shipmentId"), query_params=paging(100), result_key="selfShipAppointmentSlots",
))
register(operation(
    "generateSelfShipAppointmentSlots", "POST", SHIPMENT + "/selfShipAppointmentSlots",
    path_params=("inboundPlanId", "shipmentId"), request_body=body(allow_empty=True), success=(201,),
    result_key="operation", execution="async", risk="generate",
))
register(operation(
    "scheduleSelfShipAppointment", "POST", SHIPMENT + "/selfShipAppointmentSlots/{slotId}/schedule",
    path_params=("inboundPlanId", "shipmentId", "slotId"), request_body=body(allow_empty=True), success=(200,),
    result_key="appointment", risk="commit",
))
register(operation(
    "updateShipmentSourceAddress", "PUT", SHIPMENT + "/sourceAddress",
    path_params=("inboundPlanId", "shipmentId"),
    request_body=body("address", validator="shipment_source_address"), success=(202,),
    result_key="operation", execution="async", risk="write",
))
register(operation(
    "updateShipmentTrackingDetails", "PUT", SHIPMENT + "/trackingDetails",
    path_params=("inboundPlanId", "shipmentId"),
    request_body=body("trackingDetails", validator="tracking_details"), success=(202,),
    result_key="operation", execution="async", risk="write",
))

# Transportation
register(operation(
    "listTransportationOptions", "GET", PLAN + "/transportationOptions", path_params=("inboundPlanId",),
    query_params=paging(20) + (
        query("placementOptionId", min_length=38, max_length=38, pattern=r"^[a-zA-Z0-9-]*$"),
        query("shipmentId", min_length=38, max_length=38, pattern=r"^[a-zA-Z0-9-]*$"),
    ),
    result_key="transportationOptions",
))
register(operation(
    "generateTransportationOptions", "POST", PLAN + "/transportationOptions",
    path_params=("inboundPlanId",),
    request_body=body("placementOptionId", "shipmentTransportationConfigurations", validator="transportation_configurations"),
    success=(202,), result_key="operation", execution="async", risk="generate",
))
register(operation(
    "confirmTransportationOptions", "POST", PLAN + "/transportationOptions/confirmation",
    path_params=("inboundPlanId",),
    request_body=body("transportationSelections", validator="transportation_selections"), success=(202,),
    result_key="operation", execution="async", risk="commit",
))

# Prep, compliance, and marketplace item labels
register(operation(
    "listItemComplianceDetails", "GET", "inbound/fba/2024-03-20/items/compliance",
    query_params=(
        query("mskus", required=True, kind="list", min_items=1, max_items=100,
              min_length=1, max_length=255, collection="multi"),
        query("marketplaceId", required=True, min_length=1, max_length=20),
    ), result_key="complianceDetails",
))
register(operation(
    "updateItemComplianceDetails", "PUT", "inbound/fba/2024-03-20/items/compliance",
    query_params=(query("marketplaceId", required=True, min_length=1, max_length=20),),
    request_body=body("msku", "taxDetails"), success=(202,), result_key="operation",
    execution="async", risk="write",
))
register(operation(
    "createMarketplaceItemLabels", "POST", "inbound/fba/2024-03-20/items/labels",
    request_body=body("labelType", "marketplaceId", "mskuQuantities", validator="marketplace_item_labels"),
    success=(200,), result_key="marketplaceItemLabels", risk="generate",
))
register(operation(
    "listPrepDetails", "GET", "inbound/fba/2024-03-20/items/prepDetails",
    query_params=(
        query("marketplaceId", required=True, min_length=1, max_length=20),
        query("mskus", required=True, kind="list", min_items=1, max_items=100,
              min_length=1, max_length=255, collection="multi"),
    ), result_key="prepDetails",
))
register(operation(
    "setPrepDetails", "POST", "inbound/fba/2024-03-20/items/prepDetails",
    request_body=body("marketplaceId", "mskuPrepDetails", validator="prep_details"), success=(202,),
    result_key="operation", execution="async", risk="write",
))

# Asynchronous operation status
register(operation(
    "getInboundOperationStatus", "GET", "inbound/fba/2024-03-20/operations/{operationId}",
    path_params=("operationId",), result_key="operationStatus",
))

# Retained v0 read/document operations. CLI field names are lower camel case;
# wire names preserve Amazon's legacy PascalCase contract.
register(operation(
    "getPrepInstructions", "GET", "fba/inbound/v0/prepInstructions",
    query_params=(
        query("shipToCountryCode", wire="ShipToCountryCode", required=True,
              min_length=2, max_length=2, pattern=r"^[A-Z]{2}$"),
        query("sellerSKUList", wire="SellerSKUList", kind="list", max_items=50, collection="csv"),
        query("asinList", wire="ASINList", kind="list", max_items=50, collection="csv"),
    ), result_key="prepInstructions", version="v0",
))
register(operation(
    "getLabels", "GET", "fba/inbound/v0/shipments/{shipmentId}/labels", path_params=("shipmentId",),
    query_params=(
        query("pageType", wire="PageType", required=True, enum=(
            "PackageLabel_Letter_2", "PackageLabel_Letter_4", "PackageLabel_Letter_6",
            "PackageLabel_Letter_6_CarrierLeft", "PackageLabel_A4_2", "PackageLabel_A4_4",
            "PackageLabel_Plain_Paper", "PackageLabel_Plain_Paper_CarrierBottom",
            "PackageLabel_Thermal", "PackageLabel_Thermal_Unified", "PackageLabel_Thermal_NonPCP",
            "PackageLabel_Thermal_No_Carrier_Rotation",
        )),
        query("labelType", wire="LabelType", required=True, enum=("BARCODE_2D", "UNIQUE", "PALLET")),
        query("numberOfPackages", wire="NumberOfPackages", kind="integer"),
        query("packageLabelsToPrint", wire="PackageLabelsToPrint", kind="list", collection="csv"),
        query("numberOfPallets", wire="NumberOfPallets", kind="integer"),
        query("pageSize", wire="PageSize", kind="integer", maximum=1000),
        query("pageStartIndex", wire="PageStartIndex", kind="integer"),
    ), result_key="labels", version="v0",
))
register(operation(
    "getBillOfLading", "GET", "fba/inbound/v0/shipments/{shipmentId}/billOfLading",
    path_params=("shipmentId",), result_key="billOfLading", version="v0",
))
register(operation(
    "getShipments", "GET", "fba/inbound/v0/shipments",
    query_params=(
        query("shipmentStatusList", wire="ShipmentStatusList", kind="list", collection="csv", enum=(
            "WORKING", "READY_TO_SHIP", "SHIPPED", "RECEIVING", "CANCELLED", "DELETED",
            "CLOSED", "ERROR", "IN_TRANSIT", "DELIVERED", "CHECKED_IN",
        )),
        query("shipmentIdList", wire="ShipmentIdList", kind="list", max_items=999, collection="csv"),
        query("lastUpdatedAfter", wire="LastUpdatedAfter", value_format="date-time"),
        query("lastUpdatedBefore", wire="LastUpdatedBefore", value_format="date-time"),
        query("queryType", wire="QueryType", required=True, enum=("SHIPMENT", "DATE_RANGE", "NEXT_TOKEN")),
        query("nextToken", wire="NextToken"),
        query("marketplaceId", wire="MarketplaceId", required=True),
    ), result_key="shipments", version="v0",
))
register(operation(
    "getShipmentItemsByShipmentId", "GET", "fba/inbound/v0/shipments/{shipmentId}/items",
    path_params=("shipmentId",), query_params=(query("marketplaceId", wire="MarketplaceId"),),
    result_key="shipmentItems", version="v0",
))
register(operation(
    "getShipmentItems", "GET", "fba/inbound/v0/shipmentItems",
    query_params=(
        query("lastUpdatedAfter", wire="LastUpdatedAfter", value_format="date-time"),
        query("lastUpdatedBefore", wire="LastUpdatedBefore", value_format="date-time"),
        query("queryType", wire="QueryType", required=True, enum=("DATE_RANGE", "NEXT_TOKEN")),
        query("nextToken", wire="NextToken"),
        query("marketplaceId", wire="MarketplaceId", required=True),
    ), result_key="shipmentItems", version="v0",
))


if len(OPERATION_SPECS) != 51:  # fail fast if the registry is edited incorrectly
    raise RuntimeError(f"Expected 51 Fulfillment Inbound operations, got {len(OPERATION_SPECS)}")


COMMIT_OPERATIONS = frozenset(
    operation_id for operation_id, spec in OPERATION_SPECS.items() if spec["risk"] == "commit"
)
ASYNC_OPERATIONS = frozenset(
    operation_id for operation_id, spec in OPERATION_SPECS.items() if spec["execution"] == "async"
)
