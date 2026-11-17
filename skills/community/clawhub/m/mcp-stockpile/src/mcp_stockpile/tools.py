"""
Tool definitions and execution handlers for Stockpile MCP Server.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional
from .client import StockpileClient

# Complete MCP Tool Definitions
TOOLS_METADATA: List[Dict[str, Any]] = [
    {
        "name": "set_store_message_receiver",
        "description": "Configure where inbound buyer inquiries, store contact messages, and notices for your store are routed (email or webhook). Prevents inquiries routing to platform admin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {
                    "type": "string",
                    "description": "The ID or slug of your store"
                },
                "message_receiver_email": {
                    "type": "string",
                    "description": "Email address where inquiries and messages sent to this store should be delivered"
                },
                "webhook_url": {
                    "type": "string",
                    "description": "Optional webhook endpoint to stream incoming messages directly into your agent runtime"
                },
                "notes": {
                    "type": "string",
                    "description": "Routing notes or agent instructions"
                }
            },
            "required": ["store_id", "message_receiver_email"]
        }
    },
    {
        "name": "get_store_message_receiver",
        "description": "Retrieve the current message receiver and fallback routing settings for a store.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {
                    "type": "string",
                    "description": "The ID or slug of your store"
                }
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "list_my_stores",
        "description": "List all stores owned by or accessible to this agent account.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_store_inventory",
        "description": "List active and listed items in a store with pricing, quantity, and status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {
                    "type": "string",
                    "description": "The ID or slug of the store"
                }
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "add_store_item",
        "description": "Add a new scouted item with price, curator note, and delivery guarantee to your store. Always specify source_url so the merchant can review supplier information.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Target store ID or slug"},
                "name": {"type": "string", "description": "Product title"},
                "description": {"type": "string", "description": "Physical product description"},
                "price": {"type": "number", "description": "Resale price on Stockpile Market in USD"},
                "curator_note": {"type": "string", "description": "Why the agent curated this piece"},
                "source_url": {"type": "string", "description": "Reference source or supplier URL"},
                "source_price": {"type": "number", "description": "Original cost before markup"},
                "image_url": {"type": "string", "description": "Product photograph URL"},
                "quantity": {"type": "integer", "description": "Available stock quantity", "default": 1},
                "delivery_sla_days": {"type": "integer", "description": "Guaranteed delivery days (e.g. 4)"}
            },
            "required": ["store_id", "name", "description", "price", "curator_note"]
        }
    },
    {
        "name": "update_store_item",
        "description": "Update an existing item's price, quantity, description, or curator note in your store.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Store ID or slug"},
                "item_id": {"type": "string", "description": "Item ID to update"},
                "name": {"type": "string", "description": "Updated product name"},
                "description": {"type": "string", "description": "Updated description"},
                "price": {"type": "number", "description": "Updated price in USD"},
                "quantity": {"type": "integer", "description": "Available stock quantity"},
                "curator_note": {"type": "string", "description": "Updated curator rationale"},
                "is_active": {"type": "boolean", "description": "Active status in marketplace"}
            },
            "required": ["store_id", "item_id"]
        }
    },
    {
        "name": "delete_store_item",
        "description": "Remove or unlist an item from your store.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Store ID or slug"},
                "item_id": {"type": "string", "description": "Item ID to delete"}
            },
            "required": ["store_id", "item_id"]
        }
    },
    {
        "name": "get_bulletin_board",
        "description": "Read notes, announcements, and restocking alerts pinned to the store's physical-style bulletin board.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Store ID or slug"}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "post_bulletin_note",
        "description": "Pin a new note, announcement, or restocking alert to the store bulletin board.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Store ID or slug"},
                "title": {"type": "string", "description": "Note title"},
                "message": {"type": "string", "description": "Note content"},
                "note_color": {"type": "string", "description": "yellow, kraft, green, blue, pink, or purple", "default": "yellow"},
                "is_pinned": {"type": "boolean", "description": "Pin note to the top", "default": False}
            },
            "required": ["store_id", "message"]
        }
    },
    {
        "name": "delete_bulletin_note",
        "description": "Remove an unpinned note from the store bulletin board.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Store ID or slug"},
                "note_id": {"type": "string", "description": "Bulletin note ID to remove"}
            },
            "required": ["store_id", "note_id"]
        }
    },
    {
        "name": "get_pending_orders",
        "description": "List paid customer orders awaiting shipping and fulfillment for your store.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Optional store ID filter"}
            }
        }
    },
    {
        "name": "fulfill_order",
        "description": "Submit carrier and tracking number once an order has been paid and shipped. Releases escrow payout.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "ID of the paid order to fulfill"},
                "tracking_number": {"type": "string", "description": "Physical shipping carrier tracking number"},
                "carrier": {"type": "string", "description": "Shipping carrier (USPS, UPS, FedEx, DHL, etc.)"},
                "fulfillment_type": {"type": "string", "description": "direct_shipping or digital_code", "default": "direct_shipping"},
                "notes": {"type": "string", "description": "Optional fulfillment or packaging notes"}
            },
            "required": ["order_id", "tracking_number"]
        }
    },
    {
        "name": "get_store_automation_credits",
        "description": "Inspect current automation credit balance, weekly allowance (7 for standard, 21 for AI Co-Manager), and next Sunday 00:01 UTC refill time for a store.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "The ID or slug of your store"}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "run_inventory_sweep",
        "description": "Perform an automated inventory maintenance sweep (audits dead supplier links, restocks scouted finds if low, optimizes stale pricing). Consumes 1 Auto-Credit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "The ID or slug of your store"},
                "min_inventory_target": {"type": "integer", "description": "Minimum active inventory target", "default": 4},
                "items_to_scout": {"type": "integer", "description": "Items to scout if restocking", "default": 2}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "run_pricing_audit",
        "description": "Run an AI pricing audit to generate competitive pricing recommendations for store inventory. Consumes 1 Auto-Credit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "The ID or slug of your store"},
                "strategy": {"type": "string", "description": "Pricing strategy: balanced, aggressive, conservative", "default": "balanced"}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "scout_store_items",
        "description": "Scout fresh commercial products from the web tailored to store niche. Consumes 1 Auto-Credit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Target store ID"},
                "count": {"type": "integer", "description": "Number of items to scout (1-8)", "default": 3},
                "theme_or_query": {"type": "string", "description": "Optional theme or category"}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "audit_source_urls",
        "description": "Check all active external supplier/source links in a store and automatically unlist 404 or dead items. Consumes 1 Auto-Credit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "The ID or slug of your store"}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "get_store_limits",
        "description": "Inspect store catalog capacity (standard 50 items vs Large Store 500 items) and account store limit (standard 5 vs Store Fleet 50 stores).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Optional store ID to check catalog limits"}
            }
        }
    },
    {
        "name": "checkout_large_store_tier",
        "description": "Prepare Stripe checkout payment intent to upgrade a store catalog from 50 to 500 items ($19.99/mo Large Store Pass).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "The ID or slug of the store to upgrade"}
            },
            "required": ["store_id"]
        }
    },
    {
        "name": "checkout_store_fleet_tier",
        "description": "Prepare Stripe checkout payment intent to upgrade account store limit from 5 to 50 storefronts ($19.99/mo Store Fleet Pass).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "evaluate_item_collectibility",
        "description": "Appraise item rarity score (1-100), collectible tier, collector desirability, and estimated secondary valuation across comics, rare books, toys, vintage tech, cars, artwork, garage finds, artisan crafts, and digital assets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "item_name": {"type": "string", "description": "Title, edition, or model of the item"},
                "category": {"type": "string", "description": "Category (e.g. comics, rare books, toys, electronics, collectible cars, artwork, garage finds, artisan goods, digital assets)"},
                "condition": {"type": "string", "description": "Condition grade (e.g. Mint, Near Mint, Vintage Patina, Sealed, Artist Proof)"},
                "provenance_notes": {"type": "string", "description": "Edition details, publisher, artist, year, or authenticity markings"}
            },
            "required": ["item_name"]
        }
    },
    {
        "name": "inventory_collection_batch",
        "description": "Batch inventory and list a collection, estate haul, or curated lot directly to a Stockpile storefront catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store_id": {"type": "string", "description": "Target store ID or slug"},
                "items": {
                    "type": "array",
                    "description": "List of collection items to add to inventory",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "price": {"type": "number"},
                            "curator_note": {"type": "string"},
                            "image_url": {"type": "string"},
                            "quantity": {"type": "integer", "default": 1},
                            "delivery_sla_days": {"type": "integer", "default": 4},
                            "rarity_tier": {"type": "string"}
                        },
                        "required": ["name", "description", "price"]
                    }
                }
            },
            "required": ["store_id", "items"]
        }
    },
    {
        "name": "search_collection_matches",
        "description": "Search marketplace catalog to help collectors find missing set pieces, track comparative valuations, or verify market availability.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (e.g. 'Illustrated Dune 1978', 'Analog synthesizer')"},
                "category": {"type": "string", "description": "Optional category filter"}
            },
            "required": ["query"]
        }
    }
]


def execute_tool(
    name: str,
    arguments: Dict[str, Any],
    client: StockpileClient,
    api_key_override: Optional[str] = None,
    jwt_token_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute an MCP tool against the Stockpile API."""
    kwargs = {"api_key_override": api_key_override, "jwt_token_override": jwt_token_override}

    if name == "set_store_message_receiver":
        store_id = arguments["store_id"]
        payload = {
            "message_receiver_email": arguments["message_receiver_email"],
            "webhook_url": arguments.get("webhook_url"),
            "notes": arguments.get("notes"),
        }
        res = client.request(f"v1/agent/stores/{store_id}/message-receiver", method="PUT", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "get_store_message_receiver":
        store_id = arguments["store_id"]
        res = client.request(f"v1/agent/stores/{store_id}/message-receiver", method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "list_my_stores":
        res = client.request("stores", method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "get_store_inventory":
        store_id = arguments["store_id"]
        res = client.request(f"stores/{store_id}/items", method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "add_store_item":
        store_id = arguments["store_id"]
        payload = {
            "name": arguments["name"],
            "description": arguments["description"],
            "price": arguments["price"],
            "curator_note": arguments["curator_note"],
            "source_url": arguments.get("source_url"),
            "source_price": arguments.get("source_price"),
            "image_url": arguments.get("image_url"),
            "quantity": int(arguments.get("quantity", 1)),
            "delivery_sla_days": arguments.get("delivery_sla_days", 4),
        }
        res = client.request(f"v1/agent/stores/{store_id}/items", method="POST", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "update_store_item":
        store_id = arguments["store_id"]
        item_id = arguments["item_id"]
        payload = {k: v for k, v in arguments.items() if k not in ("store_id", "item_id") and v is not None}
        res = client.request(f"v1/agent/stores/{store_id}/items/{item_id}", method="PUT", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "delete_store_item":
        store_id = arguments["store_id"]
        item_id = arguments["item_id"]
        res = client.request(f"v1/agent/stores/{store_id}/items/{item_id}", method="DELETE", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "get_bulletin_board":
        store_id = arguments["store_id"]
        res = client.request(f"v1/agent/stores/{store_id}/bulletin-board", method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "post_bulletin_note":
        store_id = arguments["store_id"]
        payload = {
            "title": arguments.get("title"),
            "message": arguments["message"],
            "note_color": arguments.get("note_color", "yellow"),
            "is_pinned": arguments.get("is_pinned", False),
        }
        res = client.request(f"v1/agent/stores/{store_id}/bulletin-board", method="POST", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "delete_bulletin_note":
        store_id = arguments["store_id"]
        note_id = arguments["note_id"]
        res = client.request(f"v1/agent/stores/{store_id}/bulletin-board/{note_id}", method="DELETE", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "get_pending_orders":
        store_id = arguments.get("store_id")
        endpoint = f"v1/agent/orders/pending?store_id={store_id}" if store_id else "v1/agent/orders/pending"
        res = client.request(endpoint, method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "fulfill_order":
        order_id = arguments["order_id"]
        payload = {
            "fulfillment_type": arguments.get("fulfillment_type", "direct_shipping"),
            "carrier": arguments.get("carrier"),
            "tracking_number": arguments.get("tracking_number"),
            "notes": arguments.get("notes"),
        }
        res = client.request(f"v1/agent/orders/{order_id}/fulfill", method="POST", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "get_store_automation_credits":
        store_id = arguments["store_id"]
        res = client.request(f"v1/agent/stores/{store_id}/credits", method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "run_inventory_sweep":
        store_id = arguments["store_id"]
        payload = {
            "min_inventory_target": arguments.get("min_inventory_target", 4),
            "items_to_scout": arguments.get("items_to_scout", 2),
            "audit_sources": True,
            "dynamic_pricing": True,
            "auto_restock_if_low": True,
        }
        res = client.request(f"v1/agent/stores/{store_id}/maintenance", method="POST", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "run_pricing_audit":
        store_id = arguments["store_id"]
        payload = {
            "strategy": arguments.get("strategy", "balanced"),
            "target_margin_percent": 22.0,
        }
        res = client.request(f"v1/agent/stores/{store_id}/pricing-audit", method="POST", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "scout_store_items":
        store_id = arguments["store_id"]
        payload = {
            "count": int(arguments.get("count", 3)),
            "theme_or_query": arguments.get("theme_or_query"),
        }
        res = client.request(f"v1/agent/stores/{store_id}/scout", method="POST", payload=payload, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "audit_source_urls":
        store_id = arguments["store_id"]
        res = client.request(f"v1/agent/stores/{store_id}/audit-sources", method="POST", payload={}, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "get_store_limits":
        store_id = arguments.get("store_id")
        result: Dict[str, Any] = {}
        if store_id:
            res_store = client.request(f"v1/agent/stores/{store_id}/tier", method="GET", **kwargs)
            result["store_tier"] = res_store
        res_acct = client.request("v1/agent/account/tier", method="GET", **kwargs)
        result["account_tier"] = res_acct
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

    elif name == "checkout_large_store_tier":
        store_id = arguments["store_id"]
        res = client.request(f"v1/agent/stores/{store_id}/large-store/checkout", method="POST", payload={"price": 19.99}, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "checkout_store_fleet_tier":
        res = client.request("v1/agent/account/store-fleet/checkout", method="POST", payload={"price": 19.99}, **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    elif name == "evaluate_item_collectibility":
        item_name = arguments.get("item_name", "")
        category = arguments.get("category", "General Collectibles")
        condition = arguments.get("condition", "Good")
        provenance = arguments.get("provenance_notes", "")

        full_text = f"{item_name} {category} {provenance}".lower()
        is_grail = any(k in full_text for k in ["grail", "first edition", "1st edition", "prototype", "museum", "signed", "original pressing", "artist proof"])
        is_rare = any(k in full_text for k in ["rare", "limited edition", "limited to", "scarce", "out of print", "archival", "discontinued", "numbered", "deadstock"])
        is_collectible = any(k in full_text for k in ["vintage", "retro", "estate", "artisan", "handcrafted", "collectible", "custom", "japanese import", "mint condition", "die-cast", "comic", "cartridge"])

        if is_grail:
            tier = "Grail / Museum Grade"
            score = 96
            appeal = "Ultra-high; blue-chip collector status"
            rec_markup = "40% - 75%"
            notes = "Exceptional rarity. Verify physical hallmarks, edition numbers, and publication imprint. High secondary market liquidity."
        elif is_rare:
            tier = "Scarce Collector Find"
            score = 84
            appeal = "High; sought after by niche specialists"
            rec_markup = "28% - 45%"
            notes = "Limited physical supply. Desirable among community collectors and completionists."
        elif is_collectible:
            tier = "Curated Collectible"
            score = 70
            appeal = "Moderate-High; reliable enthusiast demand"
            rec_markup = "20% - 32%"
            notes = "Authentic period aesthetic or artisan build. Strong storefront centerpiece."
        else:
            tier = "Specialty Curated"
            score = 52
            appeal = "Standard commercial enthusiast appeal"
            rec_markup = "18% - 25%"
            notes = "Quality merchandise suitable for everyday buyers."

        result = {
            "item_name": item_name,
            "category": category,
            "condition": condition,
            "rarity_tier": tier,
            "rarity_score": score,
            "collector_appeal": appeal,
            "recommended_markup": rec_markup,
            "curator_appraisal_note": notes,
            "escrow_recommended": score >= 70,
        }
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

    elif name == "inventory_collection_batch":
        store_id = arguments["store_id"]
        items = arguments.get("items", [])
        created_items = []
        errors = []
        for it in items:
            try:
                res = client.request(f"v1/agent/stores/{store_id}/items", method="POST", payload=it, **kwargs)
                created_items.append(res)
            except Exception as e:
                errors.append({"item_name": it.get("name"), "error": str(e)})
        return {"content": [{"type": "text", "text": json.dumps({"store_id": store_id, "success_count": len(created_items), "created_items": created_items, "errors": errors}, indent=2)}]}

    elif name == "search_collection_matches":
        query = arguments.get("query", "")
        import urllib.parse
        encoded = urllib.parse.quote(query)
        res = client.request(f"items?search={encoded}", method="GET", **kwargs)
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

    else:
        raise ValueError(f"Unknown tool: {name}")
