#!/usr/bin/env python3
"""
mysql-slow-query-analyzer CLI 入口
提供 explain-json / explain-text / slowlog / index-advice / rewrite / analyze 命令
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mysql_slow_query_analyzer import (
    parse_explain_json,
    parse_explain_text,
    parse_slow_query_log,
    generate_index_suggestions,
    generate_rewrite_suggestions,
    analyze_slow_query,
    _format_report,
)


def main():
    if len(sys.argv) < 2:
        print("mysql-slow-query-analyzer - MySQL 慢查询分析与优化")
        print("")
        print("用法:")
        print("  mysql-slow-query-analyzer explain-json <JSON>   解析 EXPLAIN JSON")
        print("  mysql-slow-query-analyzer explain-text <TEXT>   解析 EXPLAIN 文本格式")
        print("  mysql-slow-query-analyzer slowlog <LOG>         分析慢查询日志")
        print("  mysql-slow-query-analyzer index-advice <SQL>    生成索引建议")
        print("  mysql-slow-query-analyzer rewrite <SQL>         生成重写建议")
        print("  mysql-slow-query-analyzer analyze <SQL>         完整分析")
        print("  mysql-slow-query-analyzer help                  显示帮助")
        print("")
        print("示例:")
        print('  mysql-slow-query-analyzer analyze "SELECT * FROM orders WHERE status=1"')
        print('  mysql-slow-query-analyzer index-advice "SELECT * FROM users WHERE email=\'a@b.com\'"')
        print('  mysql-slow-query-analyzer slowlog "# Query_time: 5.0 ..."')
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "help":
        print(__doc__ if __doc__ else "mysql-slow-query-analyzer - MySQL 慢查询分析与优化")
        sys.exit(0)

    if len(sys.argv) >= 3:
        args = " ".join(sys.argv[2:])
    else:
        print(f"❌ 命令 '{cmd}' 需要参数")
        print(f"   用法: mysql-slow-query-analyzer {cmd} <参数>")
        sys.exit(1)

    if cmd == "explain-json":
        result = parse_explain_json(args)
        print(_format_report({"explain_result": result}))

    elif cmd == "explain-text":
        result = parse_explain_text(args)
        print(_format_report({"explain_result": result}))

    elif cmd == "slowlog":
        result = parse_slow_query_log(args)
        print(_format_report({"log_info": result}))

    elif cmd == "index-advice":
        result = generate_index_suggestions(args)
        if result:
            print("💡 索引建议:")
            for s in result:
                print(f"  {s}")
        else:
            print("✅ 未发现需要额外索引的列（已有适当索引或无需索引）")

    elif cmd == "rewrite":
        result = generate_rewrite_suggestions(args)
        if result:
            print("🔧 重写建议:")
            for s in result:
                print(f"  {s}")
        else:
            print("✅ SQL 结构良好，暂无需重写")

    elif cmd == "analyze":
        result = analyze_slow_query(args)
        print(_format_report(result))

    else:
        print(f"❌ 未知命令: {cmd}")
        print("   可用命令: explain-json, explain-text, slowlog, index-advice, rewrite, analyze, help")
        sys.exit(1)


if __name__ == "__main__":
    main()
