#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=1.27.0",
#   "certifi>=2025.11.12",
# ]
# ///
"""Local Shopify Admin MCP server exposed over stdio."""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.request
from typing import Any

import certifi
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("shopify")

_SHOP = os.environ.get("MAVERICK_SHOPIFY_MCP_SHOP", "").strip().lower()
_API_VERSION = os.environ.get("MAVERICK_SHOPIFY_MCP_API_VERSION", "2026-04").strip() or "2026-04"
_ACCESS_TOKEN_ENV = "MAVERICK_SHOPIFY_MCP_ACCESS_TOKEN"

_PRODUCT_FIELDS = """
id
title
handle
descriptionHtml
vendor
productType
status
tags
totalInventory
createdAt
updatedAt
onlineStoreUrl
variants(first: 10) {
  nodes {
    id
    title
    sku
    price
    inventoryQuantity
  }
}
"""

_ORDER_FIELDS = """
id
name
createdAt
updatedAt
displayFinancialStatus
displayFulfillmentStatus
email
phone
totalPriceSet {
  shopMoney {
    amount
    currencyCode
  }
}
customer {
  id
  displayName
  email
}
lineItems(first: 10) {
  nodes {
    name
    quantity
    sku
    variantTitle
    product {
      id
      title
    }
  }
}
"""


def _bearer_token(ctx: Context) -> str:
    _ = ctx
    token = os.environ.get(_ACCESS_TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(f"{_ACCESS_TOKEN_ENV} is required")
    return token


def _bounded_limit(limit: int, *, default: int = 20, maximum: int = 100) -> int:
    try:
        value = int(limit or default)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, maximum))


def _graphql_url() -> str:
    if not _SHOP:
        raise RuntimeError("MAVERICK_SHOPIFY_MCP_SHOP is required")
    return f"https://{_SHOP}/admin/api/{_API_VERSION}/graphql.json"


def _normalize_gid(resource: str, value: str) -> str:
    candidate = str(value or "").strip()
    if candidate.startswith("gid://shopify/"):
        return candidate
    if candidate.isdigit():
        return f"gid://shopify/{resource}/{candidate}"
    return candidate


def _compact_input(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None and value != ""}


def _graphql(access_token: str, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    request = urllib.request.Request(
        _graphql_url(),
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
        method="POST",
    )
    context = ssl.create_default_context(cafile=certifi.where())
    try:
        with urllib.request.urlopen(request, timeout=30, context=context) as response:
            raw = response.read().decode("utf-8")
            parsed = json.loads(raw) if raw else {}
            return parsed if isinstance(parsed, dict) else {"data": parsed}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            details = json.loads(raw)
        except ValueError:
            details = {"message": raw[:500]}
        return {"errors": [{"message": "Shopify Admin API HTTP error", "status": exc.code, "details": details}]}
    except urllib.error.URLError as exc:
        return {"errors": [{"message": "Shopify Admin API connection error", "details": str(exc)}]}


@mcp.tool()
def admin_graphql(ctx: Context, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a Shopify Admin GraphQL query or mutation against the connected store."""
    return _graphql(_bearer_token(ctx), query, variables)


@mcp.tool()
def get_shop(ctx: Context) -> dict[str, Any]:
    """Get basic Shopify store information."""
    return _graphql(
        _bearer_token(ctx),
        """
        query GetShop {
          shop {
            id
            name
            email
            myshopifyDomain
            currencyCode
            timezoneAbbreviation
            primaryDomain {
              host
              url
            }
            plan {
              displayName
              partnerDevelopment
            }
          }
        }
        """,
    )


@mcp.tool()
def list_products(ctx: Context, query: str = "", limit: int = 20) -> dict[str, Any]:
    """List or search Shopify products."""
    return _graphql(
        _bearer_token(ctx),
        f"""
        query ListProducts($first: Int!, $query: String) {{
          products(first: $first, query: $query, sortKey: UPDATED_AT, reverse: true) {{
            nodes {{
              {_PRODUCT_FIELDS}
            }}
          }}
        }}
        """,
        {"first": _bounded_limit(limit), "query": query or None},
    )


@mcp.tool()
def get_product(ctx: Context, product_id: str) -> dict[str, Any]:
    """Get details for one Shopify product by GraphQL gid or numeric product id."""
    return _graphql(
        _bearer_token(ctx),
        f"""
        query GetProduct($id: ID!) {{
          node(id: $id) {{
            ... on Product {{
              {_PRODUCT_FIELDS}
            }}
          }}
        }}
        """,
        {"id": _normalize_gid("Product", product_id)},
    )


@mcp.tool()
def create_product(
    ctx: Context,
    title: str,
    description_html: str = "",
    vendor: str = "",
    product_type: str = "",
    status: str = "DRAFT",
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Create a Shopify product."""
    product = _compact_input(
        {
            "title": title,
            "descriptionHtml": description_html,
            "vendor": vendor,
            "productType": product_type,
            "status": status.strip().upper() or "DRAFT",
            "tags": tags or None,
        }
    )
    return _graphql(
        _bearer_token(ctx),
        f"""
        mutation CreateProduct($product: ProductCreateInput!) {{
          productCreate(product: $product) {{
            product {{
              {_PRODUCT_FIELDS}
            }}
            userErrors {{
              field
              message
            }}
          }}
        }}
        """,
        {"product": product},
    )


@mcp.tool()
def update_product(
    ctx: Context,
    product_id: str,
    title: str = "",
    description_html: str = "",
    vendor: str = "",
    product_type: str = "",
    status: str = "",
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """Update Shopify product fields."""
    product = _compact_input(
        {
            "id": _normalize_gid("Product", product_id),
            "title": title,
            "descriptionHtml": description_html,
            "vendor": vendor,
            "productType": product_type,
            "status": status.strip().upper() if status else "",
            "tags": tags,
        }
    )
    return _graphql(
        _bearer_token(ctx),
        f"""
        mutation UpdateProduct($product: ProductUpdateInput!) {{
          productUpdate(product: $product) {{
            product {{
              {_PRODUCT_FIELDS}
            }}
            userErrors {{
              field
              message
            }}
          }}
        }}
        """,
        {"product": product},
    )


@mcp.tool()
def list_orders(ctx: Context, query: str = "", limit: int = 20) -> dict[str, Any]:
    """List or search Shopify orders."""
    return _graphql(
        _bearer_token(ctx),
        f"""
        query ListOrders($first: Int!, $query: String) {{
          orders(first: $first, query: $query, sortKey: CREATED_AT, reverse: true) {{
            nodes {{
              {_ORDER_FIELDS}
            }}
          }}
        }}
        """,
        {"first": _bounded_limit(limit), "query": query or None},
    )


@mcp.tool()
def get_order(ctx: Context, order_id: str) -> dict[str, Any]:
    """Get details for one Shopify order by GraphQL gid or numeric order id."""
    return _graphql(
        _bearer_token(ctx),
        f"""
        query GetOrder($id: ID!) {{
          node(id: $id) {{
            ... on Order {{
              {_ORDER_FIELDS}
            }}
          }}
        }}
        """,
        {"id": _normalize_gid("Order", order_id)},
    )


@mcp.tool()
def list_customers(ctx: Context, query: str = "", limit: int = 20) -> dict[str, Any]:
    """List or search Shopify customers."""
    return _graphql(
        _bearer_token(ctx),
        """
        query ListCustomers($first: Int!, $query: String) {
          customers(first: $first, query: $query, sortKey: UPDATED_AT, reverse: true) {
            nodes {
              id
              displayName
              firstName
              lastName
              email
              phone
              createdAt
              updatedAt
              numberOfOrders
              tags
              amountSpent {
                amount
                currencyCode
              }
            }
          }
        }
        """,
        {"first": _bounded_limit(limit), "query": query or None},
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
