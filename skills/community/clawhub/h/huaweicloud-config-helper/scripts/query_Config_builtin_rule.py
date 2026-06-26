import json
import argparse
import requests

from tools import list_built_in_policy_definitions

requests.packages.urllib3.disable_warnings()


def query_Config_builtin_rule(keyword="obs", limit=20):
    if not limit:
        limit = 20
    config_rules = list_built_in_policy_definitions()
    config_rules = [item for item in config_rules.get("value") if (not keyword) or (keyword in item.get("keywords"))]
    config_rules = config_rules[:int(limit)]
    if len(config_rules) == 1:
        config_rules = config_rules[0]
    return config_rules


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Config服务预置合规规则查询")
    parser.add_argument("--keyword", help="云服务关键词")
    parser.add_argument("--limit", help="返回数量")
    args = parser.parse_args()

    result = query_Config_builtin_rule(
        keyword=args.keyword,
        limit=args.limit
    )
    # 输出结果
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(output_json)
