import json
import argparse
import requests

from tools import query_Config_resource_by_sql

requests.packages.urllib3.disable_warnings()


def query_Config_resource_summary_by_sql(provider, resource_type, region_id):
    select_statement = "SELECT provider, type,region_id, count(1) AS cnt FROM resources "
    where_statement = ""
    if provider:
        where_statement += f" AND provider = '{provider}'"
    if resource_type:
        where_statement += f" AND type = '{resource_type}'"
    if region_id:
        where_statement += f" AND region_id = '{region_id}'"
    if where_statement:
        where_statement = "WHERE " + where_statement[5:]

    group_statement = " GROUP BY provider,type,region_id"
    sql = select_statement + where_statement + group_statement
    return query_Config_resource_by_sql(sql).get("results", [])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Config资源概要")
    parser.add_argument("--provider", help="只查询指定云服务")
    parser.add_argument("--region_id", help="只查询指定region")
    args = parser.parse_args()

    provider = args.provider
    if provider and "." in provider:
        resource_provider, resource_type = provider.split(".")[0], provider.split(".")[1]
    else:
        resource_provider, resource_type = provider, ""
    result = query_Config_resource_summary_by_sql(resource_provider, resource_type, args.region_id)
    # 输出结果
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(output_json)
