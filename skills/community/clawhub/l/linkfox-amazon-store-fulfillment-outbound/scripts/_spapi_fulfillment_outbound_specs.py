"""Operation registry for Amazon Fulfillment Outbound SP-API v2026-07-04."""

from __future__ import annotations

from typing import Any


PATH_PARAM_RULES: dict[str, dict[str, Any]] = {
    "orderId": {"minLength": 1, "maxLength": 40, "pattern": r"^.*$"},
}


def query(
    name: str,
    *,
    required: bool = False,
    enum: tuple[str, ...] = (),
    min_length: int | None = None,
    max_length: int | None = None,
    value_format: str | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "wire": name,
        "required": required,
        "kind": "string",
        "enum": enum,
        "minimum": None,
        "maximum": None,
        "minItems": None,
        "maxItems": None,
        "minLength": min_length,
        "maxLength": max_length,
        "pattern": None,
        "format": value_format,
        "collection": "single",
    }


def body(*required_keys: str, allow_empty: bool = False, validator: str | None = None) -> dict[str, Any]:
    return {
        "required": True,
        "requiredKeys": required_keys,
        "allowEmpty": allow_empty,
        "validator": validator,
    }


def camel_to_snake(value: str) -> str:
    output: list[str] = []
    for index, character in enumerate(value):
        if character.isupper() and index:
            output.append("_")
        output.append(character.lower())
    return "".join(output)


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
    environment: str = "production",
    version: str = "2026-07-04",
    supports_fulfillment_service_id: bool = True,
) -> dict[str, Any]:
    return {
        "operationId": operation_id,
        "script": camel_to_snake(operation_id) + ".py",
        "version": version,
        "method": method,
        "path": path,
        "pathParams": path_params,
        "pathParamRules": {
            name: PATH_PARAM_RULES[name] for name in path_params if name in PATH_PARAM_RULES
        },
        "queryParams": query_params,
        "requestBody": request_body,
        "successStatuses": success,
        "resultKey": result_key,
        "execution": execution,
        "risk": risk,
        "environment": environment,
        "supportsFulfillmentServiceId": supports_fulfillment_service_id,
    }


ROOT = "fulfillment/outbound/2026-07-04"
ORDER = ROOT + "/orders/{orderId}"


OPERATION_SPECS: dict[str, dict[str, Any]] = {
    "getOrderPreview": operation(
        "getOrderPreview",
        "POST",
        ROOT + "/previews",
        request_body=body("lineItems", "destination", validator="order_preview"),
        result_key="orderPreview",
        risk="generate",
    ),
    "getOffers": operation(
        "getOffers",
        "POST",
        ROOT + "/offers",
        request_body=body("items", "origin", validator="offers"),
        result_key="offers",
        risk="generate",
    ),
    "createOrder": operation(
        "createOrder",
        "POST",
        ROOT + "/orders",
        request_body=body("orderId", "lineItems", "destination", validator="create_order"),
        success=(200, 202),
        result_key="orderCreation",
        execution="async-possible",
        risk="commit",
    ),
    "listOrders": operation(
        "listOrders",
        "GET",
        ROOT + "/orders",
        query_params=(
            query("updatedAfter", value_format="date-time"),
            query("pageToken"),
            query("shipments", enum=("INCLUDE", "EXCLUDE")),
        ),
        result_key="orders",
    ),
    "getOrder": operation(
        "getOrder",
        "GET",
        ORDER,
        path_params=("orderId",),
        query_params=(query("shipments", enum=("INCLUDE", "EXCLUDE")),),
        result_key="order",
    ),
    "updateOrder": operation(
        "updateOrder",
        "PUT",
        ORDER,
        path_params=("orderId",),
        request_body=body(allow_empty=True, validator="update_order"),
        success=(202,),
        result_key="orderUpdate",
        execution="async",
        risk="commit",
    ),
    "cancelOrder": operation(
        "cancelOrder",
        "PUT",
        ORDER + "/cancel",
        path_params=("orderId",),
        success=(202,),
        result_key="orderCancellation",
        execution="async",
        risk="commit",
    ),
    "updateOrderStatus": operation(
        "updateOrderStatus",
        "PUT",
        ORDER + "/status",
        path_params=("orderId",),
        request_body=body("status", validator="order_status"),
        success=(204,),
        result_key="statusUpdate",
        risk="sandbox-write",
        environment="sandbox",
    ),
    "updatePackage": operation(
        "updatePackage",
        "PUT",
        ORDER + "/packages/{packageId}",
        path_params=("orderId", "packageId"),
        request_body=body("status", validator="package_update"),
        success=(204,),
        result_key="packageUpdate",
        risk="sandbox-write",
        environment="sandbox",
    ),
    "getInvoiceHeaders": operation(
        "getInvoiceHeaders",
        "GET",
        "finances/invoices/2026-06-25/invoices",
        query_params=(
            query("marketplaceId", required=True),
            query("nextToken"),
            query("fromIssueDate", value_format="date-time"),
            query("toIssueDate", value_format="date-time"),
            query("invoicesModifiedAfter", value_format="date-time"),
        ),
        result_key="invoiceHeaders",
        version="2026-06-25",
        supports_fulfillment_service_id=False,
    ),
}


COMMIT_OPERATIONS = tuple(
    operation_id for operation_id, spec in OPERATION_SPECS.items() if spec["risk"] == "commit"
)
SANDBOX_OPERATIONS = tuple(
    operation_id for operation_id, spec in OPERATION_SPECS.items() if spec["environment"] == "sandbox"
)
