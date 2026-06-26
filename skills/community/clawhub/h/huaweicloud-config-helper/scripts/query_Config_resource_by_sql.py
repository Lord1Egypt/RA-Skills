import argparse
import requests

from tools import query_Config_resource_by_sql

requests.packages.urllib3.disable_warnings()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="按照条件查询资源")
    parser.add_argument("--sql", help="查询的sql语句")
    args = parser.parse_args()

    result = query_Config_resource_by_sql(sql=args.sql)
    # 输出结果
    print(result)
