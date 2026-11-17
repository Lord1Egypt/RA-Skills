import psycopg2
from psycopg2 import OperationalError


def create_kwdb_connection(host, port, user, password, database="postgres"):
    """
    根据传入的参数动态创建 KWDB 连接
    :return: 连接对象
    """
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            options="-c search_path=public"
        )
        return conn
    except OperationalError as e:
        raise Exception(f"连接失败: {str(e)}")


def close_kwdb_connection(conn, cursor):
    """安全关闭游标和连接"""
    if cursor:
        cursor.close()
    if conn:
        conn.close()