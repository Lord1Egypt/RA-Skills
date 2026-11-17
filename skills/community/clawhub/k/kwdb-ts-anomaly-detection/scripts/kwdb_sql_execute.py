import sys
import json
from datetime import datetime, date
from kwdb_connection import create_kwdb_connection, close_kwdb_connection
from psycopg2 import Error

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

def show_usage():
    print("使用方法：")
    print("  带密码：python kwdb_sql_client.py <host> <port> <username> <password> <sql语句> [输出文件]")
    print("  无密码：python kwdb_sql_client.py <host> <port> <username> \"\" <sql语句> [输出文件]")
    print("示例：")
    print("  python kwdb_sql_client.py 127.0.0.1 54321 admin 123456 \"select version();\"")
    print("  python kwdb_sql_client.py 127.0.0.1 54321 root \"\" \"create table test(id int);\"")
    print("  python kwdb_sql_client.py 127.0.0.1 54321 admin 123456 \"select * from t;\" /tmp/result.json")

def execute_sql_once(host, port, user, password, sql, output_file=None):
    conn = None
    cursor = None
    try:
        conn = create_kwdb_connection(host, port, user, password)
        cursor = conn.cursor()
        cursor.execute(sql)

        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            if output_file:
                result = {
                    "columns": columns,
                    "rows": [list(row) for row in rows]
                }
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
                print(f"结果已保存到: {output_file}")
            else:
                col_width = 20  # 每列固定宽度，统一对齐
                # 1. 打印表头
                header = "".join(f"{col:<{col_width}}" for col in columns)
                print(header)
                print("-" * len(header))  # 自动生成分隔线
                # 2. 循环打印所有行（自动适配任意列数）
                for row in rows:
                    row_str = "".join(f"{str(item) if item is not None else '':<{col_width}}" for item in row)
                    print(row_str)
        else:
            conn.commit()
            print(f"执行成功！影响行数：{cursor.rowcount}")

    except Error as e:
        print(f"执行失败：{str(e)}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"错误：{str(e)}")
    finally:
        close_kwdb_connection(conn, cursor)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        show_usage()
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    sql = sys.argv[5]
    output_file = sys.argv[6] if len(sys.argv) > 6 else None

    execute_sql_once(host, port, user, password, sql, output_file)