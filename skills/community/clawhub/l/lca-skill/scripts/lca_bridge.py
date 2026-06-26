#!/usr/bin/env python3
"""
lca_bridge.py — CLI bridge between OpenClaw and openLCA IPC server.

Usage:
    python3 lca_bridge.py <command> [args...]

All output is JSON to stdout. Errors return {"error": "message"}.
Connects to localhost on the port specified by OPENLCA_IPC_PORT (default 8080).
"""

import json
import os
import sys

try:
    import olca_ipc as ipc
    import olca_schema as o
except ImportError:
    print(json.dumps({"error": "olca-ipc not installed. Run: pip install olca-ipc"}))
    sys.exit(1)


def get_client():
    port = int(os.environ.get("OPENLCA_IPC_PORT", "8080"))
    return ipc.Client(port)


def out(data):
    print(json.dumps(data, indent=2, default=str))


def cmd_ping():
    try:
        client = get_client()
        # Try to list something small to verify connection
        client.get_descriptors(o.Flow)
        out({"status": "connected", "port": int(os.environ.get("OPENLCA_IPC_PORT", "8080"))})
    except Exception as e:
        out({"error": f"Cannot connect to openLCA IPC server: {e}"})


def cmd_list_processes(search=None):
    client = get_client()
    descriptors = client.get_descriptors(o.Process)
    processes = [{"id": d.id, "name": d.name} for d in descriptors]
    if search:
        search_lower = search.lower()
        processes = [p for p in processes if search_lower in p["name"].lower()]
    out({"count": len(processes), "processes": processes[:100]})


def cmd_list_flows(search=None):
    client = get_client()
    descriptors = client.get_descriptors(o.Flow)
    flows = [{"id": d.id, "name": d.name} for d in descriptors]
    if search:
        search_lower = search.lower()
        flows = [f for f in flows if search_lower in f["name"].lower()]
    out({"count": len(flows), "flows": flows[:100]})


def cmd_list_impact_methods():
    client = get_client()
    descriptors = client.get_descriptors(o.ImpactMethod)
    methods = [{"id": d.id, "name": d.name} for d in descriptors]
    out({"count": len(methods), "methods": methods})


def cmd_list_impact_categories(method_id):
    client = get_client()
    method = client.get(o.ImpactMethod, method_id)
    if not method:
        out({"error": f"Impact method {method_id} not found"})
        return
    categories = []
    if method.impact_categories:
        for cat in method.impact_categories:
            categories.append({"id": cat.id, "name": cat.name})
    out({"method": method.name, "count": len(categories), "categories": categories})


def cmd_get_process(process_id):
    client = get_client()
    process = client.get(o.Process, process_id)
    if not process:
        out({"error": f"Process {process_id} not found"})
        return
    exchanges = []
    if process.exchanges:
        for ex in process.exchanges:
            exchanges.append({
                "flow": ex.flow.name if ex.flow else None,
                "amount": ex.amount,
                "unit": ex.unit.name if ex.unit else None,
                "is_input": ex.is_input,
                "is_quantitative_reference": ex.is_quantitative_reference,
            })
    out({
        "id": process.id,
        "name": process.name,
        "description": process.description,
        "process_type": str(process.process_type) if process.process_type else None,
        "exchanges": exchanges,
    })


def cmd_create_product_system(process_id):
    client = get_client()
    config = o.LinkingConfig(
        prefer_unit_processes=True,
        provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
    )
    system = client.create_product_system(process_id, config)
    if not system:
        out({"error": f"Failed to create product system for process {process_id}"})
        return
    out({
        "id": system.id,
        "name": system.name,
        "description": system.description,
    })


def cmd_calculate(system_id, method_id):
    client = get_client()
    setup = o.CalculationSetup(
        target=o.Ref(ref_type=o.RefType.ProductSystem, id=system_id),
        impact_method=o.Ref(id=method_id),
    )
    result = client.calculate(setup)
    if not result:
        out({"error": "Calculation failed"})
        return

    impacts = []
    for impact in result.get_total_impacts():
        impacts.append({
            "category": impact.impact_category.name if impact.impact_category else None,
            "value": impact.amount,
            "unit": impact.impact_category.ref_unit if impact.impact_category else None,
        })

    result_id = result.uid if hasattr(result, 'uid') else id(result)
    out({
        "result_id": str(result_id),
        "system_id": system_id,
        "method_id": method_id,
        "impacts": impacts,
    })


def cmd_get_contributions(result_id, category_id):
    out({
        "info": "Contribution analysis requires an active result handle. "
                "Run 'calculate' first and use the result object directly. "
                "This is a placeholder for the full implementation.",
        "result_id": result_id,
        "category_id": category_id,
    })


COMMANDS = {
    "ping": (cmd_ping, 0, 0),
    "list_processes": (cmd_list_processes, 0, 1),
    "list_flows": (cmd_list_flows, 0, 1),
    "list_impact_methods": (cmd_list_impact_methods, 0, 0),
    "list_impact_categories": (cmd_list_impact_categories, 1, 1),
    "get_process": (cmd_get_process, 1, 1),
    "create_product_system": (cmd_create_product_system, 1, 1),
    "calculate": (cmd_calculate, 2, 2),
    "get_result": (cmd_calculate, 2, 2),  # alias
    "get_contributions": (cmd_get_contributions, 2, 2),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        out({
            "usage": "python3 lca_bridge.py <command> [args...]",
            "commands": list(COMMANDS.keys()),
        })
        sys.exit(0)

    cmd_name = sys.argv[1]
    args = sys.argv[2:]

    if cmd_name not in COMMANDS:
        out({"error": f"Unknown command: {cmd_name}", "available": list(COMMANDS.keys())})
        sys.exit(1)

    fn, min_args, max_args = COMMANDS[cmd_name]
    if len(args) < min_args or len(args) > max_args:
        out({"error": f"'{cmd_name}' expects {min_args}-{max_args} args, got {len(args)}"})
        sys.exit(1)

    try:
        fn(*args)
    except Exception as e:
        out({"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
