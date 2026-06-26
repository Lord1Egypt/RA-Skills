#!/usr/bin/env python3
"""
Create a simple Lens metric visualization via Saved Objects API.
Usage: python3 create_lens_metric.py [kibana-url] [title] [data-view-id] [source-field]
"""

import json
import sys
import urllib.request
import uuid

DEFAULT_KIBANA = "http://192.168.99.43"

def create_lens_metric(kibana_url, title, data_view_id, source_field, operation="count"):
    """Create a simple Lens metric visualization."""
    
    # Generate UUIDs
    layer_id = str(uuid.uuid4())
    accessor_id = str(uuid.uuid4())
    
    # Build the Lens state
    state = {
        "datasourceStates": {
            "formBased": {
                "layers": {
                    layer_id: {
                        "columns": {
                            accessor_id: {
                                "label": title,
                                "dataType": "number",
                                "operationType": operation,
                                "sourceField": source_field,
                                "isBucketed": False,
                                "scale": "ratio",
                                "params": {"emptyAsNull": True}
                            }
                        },
                        "columnOrder": [accessor_id],
                        "incompleteColumns": {}
                    }
                }
            },
            "indexpattern": {"layers": {}},
            "textBased": {"layers": {}}
        },
        "visualization": {
            "layerId": layer_id,
            "layerType": "data",
            "metricAccessor": accessor_id
        }
    }
    
    # Build the attributes
    attributes = {
        "title": title,
        "description": "",
        "state": json.dumps(state),
        " visualizationType": "lnsMetric"
    }
    
    # Build the saved object
    obj = {
        "type": "lens",
        "attributes": attributes,
        "references": [
            {
                "id": data_view_id,
                "name": f"indexpattern-datasource-layer-{layer_id}",
                "type": "index-pattern"
            }
        ]
    }
    
    # Create the lens
    url = f"{kibana_url}/api/saved_objects/lens"
    
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"kbn-xsrf": "true", "Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode())
            return {"success": True, "id": result.get("id"), "type": result.get("type")}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        try:
            error_json = json.loads(error_body)
            return {"success": False, "error": error_json.get("message", error_body)}
        except:
            return {"success": False, "error": error_body}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    args = sys.argv[1:]
    
    if len(args) < 4:
        print("Usage: python3 create_lens_metric.py <kibana-url> <title> <data-view-id> <source-field> [operation]")
        print(f"Example: python3 create_lens_metric.py {DEFAULT_KIBANA} 'Total Hosts' b58d25c5-c05c-47be-a6cb-4073ef478a8f 'hostid.keyword' count")
        sys.exit(1)
    
    kibana_url = args[0]
    title = args[1]
    data_view_id = args[2]
    source_field = args[3]
    operation = args[4] if len(args) > 4 else "count"
    
    print(f"Creating Lens metric:")
    print(f"  Title: {title}")
    print(f"  Data View ID: {data_view_id}")
    print(f"  Source Field: {source_field}")
    print(f"  Operation: {operation}")
    print("-" * 50)
    
    result = create_lens_metric(kibana_url, title, data_view_id, source_field, operation)
    
    if result["success"]:
        print(f"✅ Lens created!")
        print(f"   ID: {result['id']}")
        print(f"   Type: {result['type']}")
    else:
        print(f"❌ Failed: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()