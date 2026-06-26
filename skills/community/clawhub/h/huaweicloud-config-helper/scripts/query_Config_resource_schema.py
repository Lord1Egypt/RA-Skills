import json
import argparse
import requests

from tools import list_schema

requests.packages.urllib3.disable_warnings()


def query_Config_resource_schema(resource_type="obs") -> str:
    """
    获取指定资源类型的schema
    :resource_type: 资源类型
    """
    schemas1 = list_schema()
    marker = schemas1.get("page_info", {}).get("next_marker", "")
    schemas2 = list_schema(marker)

    schemas = schemas1.get("value", []) + schemas2.get("value", [])
    schemas = [item for item in schemas if resource_type in item.get("type")]
    if len(schemas) == 1:
        schemas = schemas[0]
    return schemas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Config资源Schema查询")
    parser.add_argument("--resource_type", help="资源类型")
    args = parser.parse_args()

    result = query_Config_resource_schema(
        resource_type=args.resource_type,
    )
    # 输出结果
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(output_json)
