#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pg-copilot - PostgreSQL AI 助手
支持：自然语言查询、ERD、性能优化、分区管理、实时同步（支持 MySQL）
"""

import os
import sys
import json
import time
import re
from datetime import datetime

# Windows 编码设置
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import psycopg2
from psycopg2 import pool

# ============== 加密/解密 ==============
import base64

def encrypt_password(password):
    """简单加密密码（生产环境建议用密钥服务）"""
    if not password:
        return password
    encoded = base64.b64encode(password.encode('utf-8'))
    return encoded.decode('utf-8')

def decrypt_password(encrypted):
    """解密密码"""
    if not encrypted:
        return encrypted
    try:
        decoded = base64.b64decode(encrypted.encode('utf-8'))
        return decoded.decode('utf-8')
    except:
        return encrypted

def get_password_from_env(env_var, encrypted_password):
    """优先从环境变量获取密码"""
    import os
    env_password = os.environ.get(env_var)
    if env_password:
        return env_password
    return decrypt_password(encrypted_password)

# ============== 告警通知 ==============
def send_alert(webhook_url, message):
    """发送告警到 webhook"""
    if not webhook_url:
        return
    
    try:
        import urllib.request
        data = {'text': message}
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"告警发送失败: {e}")

# ============== 配置 ==============
if os.name == 'nt':
    CONFIG_DIR = os.path.join(os.environ.get('USERPROFILE', '~'), '.pg-copilot')
else:
    CONFIG_DIR = os.path.expanduser('~/.pg-copilot')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

# ============== 配置管理 ==============
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def configure_database(host, port, user, password, database, alias=None):
    config = load_config()
    conn_name = alias or host
    if 'connections' not in config:
        config['connections'] = {}
    config['connections'][conn_name] = {
        'host': host, 'port': port, 'user': user,
        'password': password, 'database': database,
        'last_updated': datetime.now().isoformat()
    }
    config['active_connection'] = conn_name
    save_config(config)
    return {'success': True, 'message': f'数据库 [{conn_name}] 配置已保存'}

def get_connection():
    config = load_config()
    active = config.get('active_connection')
    if not active:
        return psycopg2.connect(
            host=os.environ.get('PG_HOST', 'localhost'),
            port=int(os.environ.get('PG_PORT', 5432)),
            user=os.environ.get('PG_USER', 'postgres'),
            password=os.environ.get('PG_PASSWORD', ''),
            database=os.environ.get('PG_DATABASE', 'postgres'),
            client_encoding='UTF8'
        )
    conn_config = config.get('connections', {}).get(active)
    if not conn_config:
        raise Exception(f'未找到数据库配置: {active}')
    return psycopg2.connect(
        host=conn_config['host'], port=conn_config['port'],
        user=conn_config['user'], password=conn_config['password'],
        database=conn_config['database'], client_encoding='UTF8'
    )

# ============== MySQL 连接 ==============
def get_mysql_connection(config):
    try:
        import pymysql
        return pymysql.connect(
            host=config['host'], port=config['port'],
            user=config['user'], password=config['password'],
            database=config['database'], charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except ImportError:
        return None

# ============== 核心功能 ==============
def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT version(), current_database(), current_user')
        result = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        table_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {'success': True, 'version': result[0], 'database': result[1], 'user': result[2], 'table_count': table_count}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_schema():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        tables = [t[0] for t in cur.fetchall()]
        schema = {}
        for table in tables:
            cur.execute(f"SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position")
            columns = [{'name': c[0], 'type': c[1], 'nullable': c[2] == 'YES', 'default': c[3]} for c in cur.fetchall()]
            cur.execute(f"SELECT kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name WHERE tc.table_name = '{table}' AND tc.constraint_type = 'PRIMARY KEY'")
            primary_keys = [p[0] for p in cur.fetchall()]
            cur.execute(f"SELECT kcu.column_name, ccu.table_name, ccu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name WHERE tc.table_name = '{table}' AND tc.constraint_type = 'FOREIGN KEY'")
            foreign_keys = [{'column': f[0], 'references': f'{f[1]}.{f[2]}'} for f in cur.fetchall()]
            cur.execute(f"SELECT pg_size_pretty(pg_total_relation_size('{table}')), COALESCE(n_live_tup, 0) FROM pg_stat_user_tables WHERE relname = '{table}'")
            stats = cur.fetchone()
            schema[table] = {'columns': columns, 'primary_keys': primary_keys, 'foreign_keys': foreign_keys, 'size': stats[0] if stats else '0 B', 'row_count': stats[1] if stats else 0}
        return schema
    finally:
        cur.close()
        conn.close()

# ============== SQL 执行 ==============
DANGEROUS = ['DROP', 'TRUNCATE', 'GRANT', 'REVOKE', 'CREATE USER', 'DROP USER']

def is_dangerous(query):
    q = query.strip().upper()
    for op in DANGEROUS:
        if op in q:
            return True
    return ('DELETE' in q or 'UPDATE' in q) and 'WHERE' not in q

def execute_query(query, read_only=True):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if is_dangerous(query):
            return {'success': False, 'error': '危险操作被拦截'}
        q = query.strip().upper()
        if q.startswith('SELECT'):
            cur.execute(query)
            columns = [d[0] for d in cur.description]
            rows = cur.fetchall()
            truncated = len(rows) > 1000
            return {'success': True, 'type': 'SELECT', 'columns': columns, 'rows': rows[:1000] if truncated else rows, 'truncated': truncated}
        else:
            if read_only:
                return {'success': False, 'error': '只读模式'}
            cur.execute(query)
            conn.commit()
            return {'success': True, 'type': 'WRITE', 'row_count': cur.rowcount}
    except psycopg2.Error as e:
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        conn.close()

def explain_query(query):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) {query}")
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

# ============== LLM 调用 ==============
def call_llm(prompt, system_prompt=None):
    """
    调用 LLM 生成自然语言解释
    支持配置 API Key
    """
    import urllib.request
    import urllib.parse
    
    # 加载配置
    config = load_config()
    llm_config = config.get('llm', {})
    
    api_url = llm_config.get('api_url', os.environ.get('LLM_API_URL', ''))
    api_key = llm_config.get('api_key', os.environ.get('LLM_API_KEY', ''))
    model = llm_config.get('model', os.environ.get('LLM_MODEL', 'gpt-3.5-turbo'))
    
    if not api_url or not api_key:
        return None, "未配置 LLM API。请在配置中设置 api_url 和 api_key"
    
    try:
        # 构建请求
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        data = {
            'model': model,
            'messages': messages,
            'temperature': 0.7
        }
        
        req = urllib.request.Request(
            api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'], None
            
    except Exception as e:
        return None, str(e)

def llm_explain_sql(query, schema_info=None):
    """
    使用 LLM 解释 SQL 查询
    """
    # 构建提示词
    system_prompt = """你是一个数据库专家。你的任务是用用户易懂的中文解释 SQL 查询的含义。
    
请遵循以下格式：
1. 用一句话说明查询的目的
2. 解释查询涉及哪些表
3. 说明查询条件是什么
4. 解释结果如何排序或分组
5. 如果是统计查询，给出统计维度和指标

注意：用通俗易懂的语言，不要使用太多技术术语。"""
    
    prompt = f"""请解释以下 SQL 查询的含义：

```sql
{query}
```

"""
    
    if schema_info:
        prompt += f"涉及的表结构：\n{schema_info}\n"
    
    prompt += "\请用中文解释这个查询的含义："
    
    return call_llm(prompt, system_prompt)

def llm_suggest_queries(user_question, schema_info):
    """
    根据用户问题推荐 SQL 查询
    """
    system_prompt = """你是一个数据库专家。根据用户的问题，生成对应的 SQL 查询。
    
规则：
1. 只生成 SELECT 查询
2. 使用标准的 PostgreSQL 语法
3. 表名和字段名使用实际名称
4. 如果用户问题不明确，给出最可能的解释"""
    
    prompt = f"""用户的原始问题：{user_question}

数据库表结构：
{schema_info}

请生成对应的 SQL 查询语句，只需要返回 SQL 代码，不需要其他解释。"""
    
    return call_llm(prompt, system_prompt)

# ============== SQL 转自然语言 ==============
def sql_to_natural(query):
    """
    将 SQL 查询结果转换为自然语言解释
    优先使用 LLM，其次使用简单解析
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 执行查询获取数据
        cur.execute(query)
        columns = [d[0] for d in cur.description]
        rows = cur.fetchall()
        row_count = len(rows)
        
        # 尝试获取表结构信息
        schema_info = None
        table_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
        if table_match:
            table_name = table_match.group(1)
            try:
                cur.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}' 
                    ORDER BY ordinal_position 
                    LIMIT 10
                """)
                cols = cur.fetchall()
                if cols:
                    schema_info = f"表 {table_name}: " + ", ".join([f"{c[0]}({c[1]})" for c in cols])
            except:
                pass
        
        # 尝试使用 LLM 解释
        llm_result, llm_error = llm_explain_sql(query, schema_info)
        
        if llm_result:
            return {
                'success': True,
                'query': query,
                'row_count': row_count,
                'columns': columns,
                'data': rows[:10] if rows else [],
                'explanation': llm_result,
                'type': 'llm'  # 标记为 LLM 生成
            }
        
        # LLM 不可用，使用简单解析
        result = {
            'success': True,
            'query': query,
            'query_type': detect_query_type(query),
            'columns': columns,
            'row_count': row_count,
            'summary': generate_summary(columns, rows, query),
            'data': rows[:10] if rows else [],
            'type': 'simple',  # 标记为简单解析
            'llm_error': llm_error
        }
        
        if rows:
            result['analysis'] = analyze_data(columns, rows)
        
        return result
        
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        conn.close()

def detect_query_type(query):
    """检测查询类型"""
    q = query.strip().upper()
    if 'SELECT' in q:
        if 'COUNT' in q:
            return 'count'
        elif 'SUM' in q or 'AVG' in q or 'MAX' in q or 'MIN' in q:
            return 'aggregate'
        elif 'JOIN' in q:
            return 'join'
        elif 'GROUP BY' in q:
            return 'group'
        elif 'ORDER BY' in q:
            return 'sorted'
        else:
            return 'select'
    return 'other'

def generate_summary(columns, rows, query):
    """生成查询摘要"""
    q = query.strip().upper()
    row_count = len(rows)
    
    # 提取关键信息
    table_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
    table_name = table_match.group(1) if table_match else '表'
    
    summary_parts = []
    
    # 修正 COUNT 查询的 summary
    if 'COUNT' in q:
        # 检查是否是 COUNT(*)
        if 'COUNT(*)' in q or 'COUNT(1)' in q:
            return f"查询结果：共 {row_count} 条记录"
        # 检查是否有 SUM 等聚合
        if 'SUM' in q or 'AVG' in q:
            pass  # 继续下面逻辑
        else:
            return f"查询结果：共 {row_count} 条记录"
    
    elif 'SUM' in q:
        col = columns[0] if columns else '总计'
        total = sum(r[0] for r in rows) if rows else 0
        return f"查询结果：共 {row_count} 条记录，{col} 总计为 {total}"
    
    elif 'AVG' in q:
        col = columns[0] if columns else '平均'
        avg = sum(r[0] for r in rows) / row_count if rows else 0
        return f"查询结果：共 {row_count} 条记录，{col} 平均为 {avg:.2f}"
    
    elif 'MAX' in q:
        col = columns[0] if columns else '最大'
        max_val = max(r[0] for r in rows) if rows else 0
        return f"查询结果：{col} 最大值为 {max_val}"
    
    elif 'MIN' in q:
        col = columns[0] if columns else '最小'
        min_val = min(r[0] for r in rows) if rows else 0
        return f"查询结果：{col} 最小值为 {min_val}"
    
    elif 'JOIN' in q:
        return f"查询结果：从多个表关联查询获得 {row_count} 条记录"
    
    elif 'GROUP BY' in q:
        return f"查询结果：按分组统计，共 {row_count} 个分组"
    
    else:
        return f"查询结果：从 {table_name} 查询到 {row_count} 条记录"

def analyze_data(columns, rows):
    """分析数据特征"""
    if not rows or not columns:
        return {}
    
    analysis = {}
    
    # 检查第一列（通常是分组/分类列）
    first_col = columns[0]
    
    # 数值列统计
    numeric_cols = []
    for i, col in enumerate(columns):
        if rows and isinstance(rows[0][i], (int, float)):
            numeric_cols.append(i)
    
    if numeric_cols:
        # 找出有意义的数值列（不是ID、排名等）
        stats = {}
        for i in numeric_cols:
            col_name = columns[i].lower()
            if any(x in col_name for x in ['amount', 'price', 'total', 'count', 'num', 'qty']):
                values = [r[i] for r in rows if r[i] is not None]
                if values:
                    stats[columns[i]] = {
                        'sum': sum(values),
                        'avg': sum(values) / len(values),
                        'min': min(values),
                        'max': max(values)
                    }
        if stats:
            analysis['statistics'] = stats
    
    # 检查时间列
    time_cols = [i for i, c in enumerate(columns) if 'time' in c.lower() or 'date' in c.lower() or 'at' in c.lower()]
    if time_cols and rows:
        analysis['time_range'] = {
            'earliest': str(rows[-1][time_cols[0]]) if rows else None,
            'latest': str(rows[0][time_cols[0]]) if rows else None
        }
    
    return analysis

# ============== 同步功能 ==============
def sync_init():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 配置表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS _sync_config (
                id SERIAL PRIMARY KEY,
                source_table VARCHAR(255) NOT NULL UNIQUE,
                target_host VARCHAR(255) NOT NULL,
                target_port INTEGER DEFAULT 5432,
                target_user VARCHAR(255) NOT NULL,
                target_password VARCHAR(255) NOT NULL,
                target_database VARCHAR(255) NOT NULL,
                target_table VARCHAR(255),
                target_type VARCHAR(20) DEFAULT 'postgresql',
                sync_mode VARCHAR(20) DEFAULT 'realtime',
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # 变更队列表（按月分区）- 主键包含分区键
        cur.execute("DROP TABLE IF EXISTS _sync_changes CASCADE")
        cur.execute("""
            CREATE TABLE _sync_changes (
                id BIGSERIAL,
                table_name VARCHAR(255) NOT NULL,
                operation VARCHAR(10) NOT NULL,
                record_id INTEGER NOT NULL,
                old_data JSONB,
                new_data JSONB,
                synced BOOLEAN DEFAULT FALSE,
                retry_count INTEGER DEFAULT 0,
                last_error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id, created_at)
            ) PARTITION BY RANGE (created_at)
        """)
        
        # 创建月度分区
        now = datetime.now()
        for i in range(6):  # 创建未来6个月的分区
            month = now.month + i
            year = now.year
            while month > 12:
                month -= 12
                year += 1
            start = f"{year}-{month:02d}-01"
            if month == 12:
                end = f"{year+1}-01-01"
            else:
                end = f"{year}-{month+1:02d}-01"
            
            partition_name = f"_sync_changes_{year}_{month:02d}"
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {partition_name} 
                PARTITION OF _sync_changes 
                FOR VALUES FROM ('{start}') TO ('{end}')
            """)
        
        # 同步日志表（按月分区）- 主键包含分区键
        cur.execute("DROP TABLE IF EXISTS _sync_log CASCADE")
        cur.execute("""
            CREATE TABLE _sync_log (
                id SERIAL,
                table_name VARCHAR(255) NOT NULL,
                operation VARCHAR(20) NOT NULL,
                record_id INTEGER,
                target_db VARCHAR(255),
                status VARCHAR(20) NOT NULL,
                error_message TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id, created_at)
            ) PARTITION BY RANGE (created_at)
        """)
        
        # 创建月度分区
        for i in range(6):
            month = now.month + i
            year = now.year
            while month > 12:
                month -= 12
                year += 1
            start = f"{year}-{month:02d}-01"
            if month == 12:
                end = f"{year+1}-01-01"
            else:
                end = f"{year}-{month+1:02d}-01"
            
            partition_name = f"_sync_log_{year}_{month:02d}"
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {partition_name} 
                PARTITION OF _sync_log 
                FOR VALUES FROM ('{start}') TO ('{end}')
            """)
        # 同步配置表添加重试和告警字段
        cur.execute("""
            ALTER TABLE _sync_config 
            ADD COLUMN IF NOT EXISTS max_retries INTEGER DEFAULT 3,
            ADD COLUMN IF NOT EXISTS webhook_url TEXT,
            ADD COLUMN IF NOT EXISTS sync_batch_size INTEGER DEFAULT 100,
            ADD COLUMN IF NOT EXISTS sync_interval INTEGER DEFAULT 5
        """)
        conn.commit()
        cur.execute("SELECT source_table FROM _sync_config WHERE enabled = TRUE")
        tables = [r[0] for r in cur.fetchall()]
        for table in tables:
            create_trigger(cur, table)
        conn.commit()
        return {'success': True, 'message': f'同步表已创建，已配置 {len(tables)} 个任务'}
    finally:
        cur.close()
        conn.close()

def create_trigger(cur, table):
    func_name = f"sync_{table}"
    cur.execute(f"""
        CREATE OR REPLACE FUNCTION {func_name}() RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                INSERT INTO _sync_changes (table_name, operation, record_id, new_data)
                VALUES ('{table}', 'INSERT', NEW.id, to_jsonb(NEW));
            ELSIF TG_OP = 'UPDATE' THEN
                INSERT INTO _sync_changes (table_name, operation, record_id, old_data, new_data)
                VALUES ('{table}', 'UPDATE', NEW.id, to_jsonb(OLD), to_jsonb(NEW));
            ELSIF TG_OP = 'DELETE' THEN
                INSERT INTO _sync_changes (table_name, operation, record_id, old_data)
                VALUES ('{table}', 'DELETE', OLD.id, to_jsonb(OLD));
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql
    """)
    cur.execute(f"DROP TRIGGER IF EXISTS sync_trg ON {table}")
    cur.execute(f"CREATE TRIGGER sync_trg AFTER INSERT OR UPDATE OR DELETE ON {table} FOR EACH ROW EXECUTE FUNCTION {func_name}()")

def sync_add_task(source_table, target_host, target_port, target_user, target_password, target_database, target_table, target_type='postgresql', max_retries=3, webhook_url='', batch_size=100):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 加密密码存储
        encrypted_password = encrypt_password(target_password)
        
        cur.execute("""
            INSERT INTO _sync_config 
                (source_table, target_host, target_port, target_user, target_password, target_database, target_table, target_type, max_retries, webhook_url, sync_batch_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_table) DO UPDATE SET
                target_host = EXCLUDED.target_host, 
                target_table = EXCLUDED.target_table, 
                target_type = EXCLUDED.target_type,
                max_retries = EXCLUDED.max_retries,
                webhook_url = EXCLUDED.webhook_url,
                sync_batch_size = EXCLUDED.sync_batch_size
            RETURNING id
        """, (source_table, target_host, target_port, target_user, encrypted_password, target_database, target_table, target_type, max_retries, webhook_url, batch_size))
        
        create_trigger(cur, source_table)
        conn.commit()
        
        return {'success': True, 'message': f'同步任务已添加: {source_table} -> {target_type}:{target_host}/{target_database}\n重试次数: {max_retries}\n告警Webhook: {"已配置" if webhook_url else "未配置"}'}
    finally:
        cur.close()
        conn.close()

def sync_status():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT source_table, target_host, target_database, target_table, target_type, sync_mode, enabled FROM _sync_config")
        tasks = [{'source_table': r[0], 'target': f"{r[1]}/{r[2]}.{r[3]}", 'type': r[4], 'mode': r[5], 'enabled': r[6]} for r in cur.fetchall()]
        cur.execute("SELECT table_name, COUNT(*) as total, COUNT(CASE WHEN synced THEN 1 END) as synced, COUNT(CASE WHEN NOT synced THEN 1 END) as pending FROM _sync_changes GROUP BY table_name")
        stats = {r[0]: {'total': r[1], 'synced': r[2], 'pending': r[3]} for r in cur.fetchall()}
        cur.execute("SELECT table_name, operation, record_id, target_db, status, created_at FROM _sync_log ORDER BY created_at DESC LIMIT 20")
        logs = [{'table': r[0], 'operation': r[1], 'record_id': r[2], 'target': r[3], 'status': r[4], 'time': str(r[5])} for r in cur.fetchall()]
        return {'tasks': tasks, 'stats': stats, 'logs': logs}
    finally:
        cur.close()
        conn.close()

def sync_process():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, table_name, operation, record_id, new_data, old_data FROM _sync_changes WHERE synced = FALSE ORDER BY created_at LIMIT 100")
        changes = cur.fetchall()
        if not changes:
            return {'success': True, 'message': '没有待同步的变更'}
        
        synced_count = 0
        failed_count = 0
        
        for change in changes:
            change_id, table_name, operation, record_id, new_data, old_data = change
            
            # 获取配置（包括重试次数和 webhook）
            cur.execute("""
                SELECT target_host, target_port, target_user, target_password, target_database, 
                       target_table, target_type, max_retries, webhook_url, sync_batch_size
                FROM _sync_config 
                WHERE source_table = %s AND enabled = TRUE
            """, (table_name,))
            config = cur.fetchone()
            
            if not config:
                continue
            
            # 获取密码（优先环境变量）
            env_var = f"PG_SYNC_{table_name.upper()}_PASSWORD"
            password = get_password_from_env(env_var, config[3])
            
            max_retries = config[7] if config[7] else 3
            webhook_url = config[8]
            
            # 重试机制
            success = False
            last_error = None
            
            for retry in range(max_retries + 1):
                try:
                    if config[6] == 'mysql':
                        mysql_conn = get_mysql_connection({
                            'host': config[0], 'port': config[1], 
                            'user': config[2], 'password': password, 'database': config[4]
                        })
                        if not mysql_conn:
                            raise Exception('pymysql 未安装')
                        mysql_cur = mysql_conn.cursor()
                        target_table = config[5] or table_name
                        
                        if operation == 'INSERT':
                            cols = [k for k in new_data.keys() if k != 'id']
                            vals = [new_data[k] for k in cols]
                            if cols:
                                # 获取冲突策略
                                strategy = get_conflict_strategy(table_name)
                                on_conflict = strategy['on_conflict']
                                
                                if on_conflict == 'ignore':
                                    # 忽略冲突
                                    sql = f"INSERT IGNORE INTO {target_table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(vals))})"
                                elif on_conflict == 'update':
                                    # 更新冲突（使用 ON DUPLICATE KEY UPDATE）
                                    set_clause = ', '.join([f"{c}=VALUES({c})" for c in cols])
                                    sql = f"INSERT INTO {target_table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(vals))}) ON DUPLICATE KEY UPDATE {set_clause}"
                                else:
                                    sql = f"INSERT INTO {target_table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(vals))})"
                                
                                mysql_cur.execute(sql, vals)
                        elif operation == 'UPDATE':
                            cols = [f"{k}=%s" for k in new_data.keys() if k != 'id']
                            vals = [new_data[k] for k in new_data.keys() if k != 'id'] + [record_id]
                            sql = f"UPDATE {target_table} SET {','.join(cols)} WHERE id=%s"
                            mysql_cur.execute(sql, vals)
                        elif operation == 'DELETE':
                            mysql_cur.execute(f"DELETE FROM {target_table} WHERE id=%s", (record_id,))
                        
                        mysql_conn.commit()
                        mysql_cur.close()
                        mysql_conn.close()
                    else:
                        target_conn = psycopg2.connect(
                            host=config[0], port=config[1], user=config[2], 
                            password=password, database=config[4], client_encoding='UTF8'
                        )
                        target_cur = target_conn.cursor()
                        target_table = config[5] or table_name
                        
                        if operation == 'INSERT':
                            cols = list(new_data.keys())
                            vals = list(new_data.values())
                            
                            # 获取冲突策略
                            strategy = get_conflict_strategy(table_name)
                            on_conflict = strategy['on_conflict']
                            
                            if on_conflict == 'ignore':
                                sql = f"INSERT INTO {target_table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(vals))})"
                            elif on_conflict == 'update':
                                set_clause = ', '.join([f"{c}=EXCLUDED.{c}" for c in cols])
                                sql = f"INSERT INTO {target_table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(vals))}) ON CONFLICT (id) DO UPDATE SET {set_clause}"
                            else:
                                sql = f"INSERT INTO {target_table} ({','.join(cols)}) VALUES ({','.join(['%s']*len(vals))})"
                            
                            target_cur.execute(sql, vals)
                        elif operation == 'UPDATE':
                            cols = [f"{k}=%s" for k in new_data.keys()]
                            vals = list(new_data.values()) + [record_id]
                            sql = f"UPDATE {target_table} SET {','.join(cols)} WHERE id=%s"
                            target_cur.execute(sql, vals)
                        elif operation == 'DELETE':
                            sql = f"DELETE FROM {target_table} WHERE id=%s"
                            target_cur.execute(sql, (record_id,))
                        
                        target_conn.commit()
                        target_cur.close()
                        target_conn.close()
                    
                    success = True
                    break
                    
                except Exception as e:
                    last_error = str(e)
                    if retry < max_retries:
                        time.sleep(1 * (retry + 1))  # 递增延迟
                    continue
            
            if success:
                # 标记已同步
                cur.execute("UPDATE _sync_changes SET synced = TRUE WHERE id = %s", (change_id,))
                cur.execute("""
                    INSERT INTO _sync_log (table_name, operation, record_id, target_db, status)
                    VALUES (%s, %s, %s, %s, 'success')
                """, (table_name, operation, record_id, f"{config[6]} {config[0]}"))
                synced_count += 1
            else:
                # 更新重试次数
                cur.execute("""
                    UPDATE _sync_changes 
                    SET retry_count = retry_count + 1, last_error = %s 
                    WHERE id = %s
                """, (last_error, change_id))
                
                # 记录失败日志
                cur.execute("""
                    INSERT INTO _sync_log (table_name, operation, record_id, target_db, status, error_message, retry_count)
                    VALUES (%s, %s, %s, %s, 'failed', %s, %s)
                """, (table_name, operation, record_id, f"{config[6]} {config[0]}", last_error, max_retries))
                
                failed_count += 1
                
                # 发送告警
                if webhook_url:
                    alert_msg = f"⚠️ 同步失败告警\n表: {table_name}\n操作: {operation}\n记录ID: {record_id}\n错误: {last_error}\n已重试 {max_retries} 次"
                    send_alert(webhook_url, alert_msg)
        
        conn.commit()
        return {'success': True, 'synced': synced_count, 'failed': failed_count}
    finally:
        cur.close()
        conn.close()

def sync_watch(interval=5):
    print(f"启动实时同步监听 (间隔 {interval} 秒)... 按 Ctrl+C 停止")
    while True:
        try:
            result = sync_process()
            if result.get('synced', 0) > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 已同步 {result['synced']} 条变更")
        except Exception as e:
            print(f"错误: {e}")
        time.sleep(interval)

# ============== 清理功能 ==============

# ============== 同步校验 ==============
def sync_verify(table_name, sample_size=10):
    """
    校验同步数据一致性
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # 获取同步配置
        cur.execute("""
            SELECT target_host, target_port, target_user, target_password, 
                   target_database, target_table, target_type
            FROM _sync_config 
            WHERE source_table = %s AND enabled = TRUE
        """, (table_name,))
        
        config = cur.fetchone()
        if not config:
            return {'success': False, 'error': '未找到同步配置'}
        
        # 获取密码
        env_var = f"PG_SYNC_{table_name.upper()}_PASSWORD"
        password = get_password_from_env(env_var, config[3])
        
        # 连接目标数据库
        if config[6] == 'mysql':
            mysql_conn = get_mysql_connection({
                'host': config[0], 'port': config[1],
                'user': config[2], 'password': password, 'database': config[4]
            })
            if not mysql_conn:
                return {'success': False, 'error': 'MySQL 连接失败'}
            mysql_cur = mysql_conn.cursor()
            target_table = config[5] or table_name
            
            # 随机抽样校验
            mysql_cur.execute(f"SELECT * FROM {target_table} ORDER BY RAND() LIMIT {sample_size}")
            target_rows = mysql_cur.fetchall()
            target_cols = [desc[0] for desc in mysql_cur.description]
            
            mysql_cur.close()
            mysql_conn.close()
        else:
            target_conn = psycopg2.connect(
                host=config[0], port=config[1], user=config[2],
                password=password, database=config[4], client_encoding='UTF8'
            )
            target_cur = target_conn.cursor()
            target_table = config[5] or table_name
            
            target_cur.execute(f"SELECT * FROM {target_table} ORDER BY RANDOM() LIMIT {sample_size}")
            target_rows = target_cur.fetchall()
            target_cols = [desc[0] for desc in target_cur.description]
            
            target_cur.close()
            target_conn.close()
        
        # 获取源数据对比
        cur.execute(f"SELECT * FROM {table_name} ORDER BY id LIMIT {sample_size}")
        source_rows = cur.fetchall()
        
        # 简单比对（转换 datetime 为字符串）
        def convert_row(row):
            return tuple(str(v) if isinstance(v, datetime) else v for v in row)
        
        match_count = 0
        mismatches = []
        
        for i, (src, tgt) in enumerate(zip(source_rows, target_rows)):
            src_conv = convert_row(src)
            tgt_conv = convert_row(tgt)
            if src_conv == tgt_conv:
                match_count += 1
            else:
                mismatches.append({'source': src_conv, 'target': tgt_conv, 'index': i})
        
        return {
            'success': True,
            'table': table_name,
            'sample_size': sample_size,
            'matched': match_count,
            'mismatched': len(mismatches),
            'match_rate': f"{match_count/sample_size*100:.1f}%" if sample_size > 0 else "0%",
            'details': mismatches[:5]
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        conn.close()

# ============== 冲突处理 ==============
def get_conflict_strategy(table_name):
    """获取表的冲突处理策略"""
    config = load_config()
    sync_config = config.get('sync_strategies', {}).get(table_name, {})
    return {
        'on_conflict': sync_config.get('on_conflict', 'update'),  # update/ignore/error
        'id_conflict': sync_config.get('id_conflict', 'update')   # update/ignore/error
    }

def set_conflict_strategy(table_name, on_conflict='update', id_conflict='update'):
    """设置冲突处理策略"""
    config = load_config()
    if 'sync_strategies' not in config:
        config['sync_strategies'] = {}
    config['sync_strategies'][table_name] = {
        'on_conflict': on_conflict,
        'id_conflict': id_conflict
    }
    save_config(config)
    return {'success': True, 'strategy': {'on_conflict': on_conflict, 'id_conflict': id_conflict}}
def sync_cleanup(days=90):
    """
    清理旧的同步记录
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # 删除旧的已同步记录
        cur.execute("""
            DELETE FROM _sync_changes 
            WHERE synced = TRUE 
            AND created_at < NOW() - INTERVAL '%s days'
        """, (days,))
        deleted_changes = cur.rowcount
        
        # 删除旧的日志记录
        cur.execute("""
            DELETE FROM _sync_log 
            WHERE created_at < NOW() - INTERVAL '%s days'
        """, (days,))
        deleted_logs = cur.rowcount
        
        conn.commit()
        return {'success': True, 'deleted_changes': deleted_changes, 'deleted_logs': deleted_logs}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        conn.close()
def create_partition(table_name, partition_type, partition_key, partitions):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if partition_type == 'range':
            cur.execute(f"CREATE TABLE {table_name}_partitioned (LIKE {table_name} INCLUDING ALL) PARTITION BY RANGE ({partition_key})")
            for p in partitions:
                cur.execute(f"CREATE TABLE {p['name']} PARTITION OF {table_name}_partitioned FOR VALUES FROM ('{p['start']}') TO ('{p['end']}')")
            return {'success': True, 'message': '范围分区创建成功'}
        elif partition_type == 'list':
            cur.execute(f"CREATE TABLE {table_name}_partitioned (LIKE {table_name} INCLUDING ALL) PARTITION BY LIST ({partition_key})")
            for p in partitions:
                cur.execute(f"CREATE TABLE {p['name']} PARTITION OF {table_name}_partitioned FOR VALUES IN ({p['values']})")
            return {'success': True, 'message': '列表分区创建成功'}
        elif partition_type == 'hash':
            cur.execute(f"CREATE TABLE {table_name}_partitioned (LIKE {table_name} INCLUDING ALL) PARTITION BY HASH ({partition_key})")
            for i in range(partitions):
                cur.execute(f"CREATE TABLE {table_name}_p{i} PARTITION OF {table_name}_partitioned FOR VALUES WITH (MODULUS {partitions}, REMAINDER {i})")
            return {'success': True, 'message': '哈希分区创建成功'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        cur.close()
        conn.close()

# ============== CLI ==============
def main():
    if len(sys.argv) < 2:
        print("""
pg-copilot - PostgreSQL AI 助手 (支持 MySQL 同步)

Commands:
  config <host> <port> <user> <pwd> <db> [alias]     配置数据库
  test                                          测试连接
  schema                                        获取 Schema
  execute <sql>                                 执行 SQL
  explain <sql>                                 性能分析
  sync-init                                     初始化同步表（带重试、告警、分区）
  sync-add <table> <host> <port> <user> <pwd> <db> <target> [type] [retries] [webhook]  添加同步任务
  sync-status                                   同步状态
  sync-process                                  处理同步（含重试）
  sync-watch                                    监听同步
  sync-cleanup [days]                           清理旧记录（默认90天）
  sync-verify <table> [samples]                 校验同步数据一致性
  conflict-strategy <table> <update|ignore|error>  设置冲突处理策略
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'config' and len(sys.argv) >= 7:
        result = configure_database(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7] if len(sys.argv) > 7 else None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == 'config-llm' and len(sys.argv) >= 4:
        # config-llm <api_url> <api_key> [model]
        config = load_config()
        if 'llm' not in config:
            config['llm'] = {}
        config['llm']['api_url'] = sys.argv[2]
        config['llm']['api_key'] = sys.argv[3]
        config['llm']['model'] = sys.argv[4] if len(sys.argv) > 4 else 'gpt-3.5-turbo'
        save_config(config)
        print(json.dumps({'success': True, 'message': 'LLM 配置已保存'}, ensure_ascii=False, indent=2))
    elif cmd == 'test':
        print(json.dumps(test_connection(), ensure_ascii=False, indent=2))
    elif cmd == 'schema':
        print(json.dumps(get_schema(), ensure_ascii=False, indent=2))
    elif cmd == 'execute' and len(sys.argv) >= 3:
        print(json.dumps(execute_query(' '.join(sys.argv[2:])), ensure_ascii=False, indent=2))
    elif cmd == 'explain' and len(sys.argv) >= 3:
        for line in explain_query(' '.join(sys.argv[2:])):
            print(line)
    
    elif cmd == 'narrate' and len(sys.argv) >= 3:
        print(json.dumps(sql_to_natural(' '.join(sys.argv[2:])), ensure_ascii=False, indent=2))
    elif cmd == 'sync-init':
        print(json.dumps(sync_init(), ensure_ascii=False, indent=2))
    elif cmd == 'sync-add' and len(sys.argv) >= 9:
        target_type = sys.argv[9] if len(sys.argv) > 9 else 'postgresql'
        max_retries = int(sys.argv[10]) if len(sys.argv) > 10 else 3
        webhook_url = sys.argv[11] if len(sys.argv) > 11 else ''
        batch_size = int(sys.argv[12]) if len(sys.argv) > 12 else 100
        
        result = sync_add_task(
            sys.argv[2], sys.argv[3], int(sys.argv[4]), 
            sys.argv[5], sys.argv[6], sys.argv[7], 
            sys.argv[8], target_type, max_retries, webhook_url, batch_size
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == 'sync-status':
        print(json.dumps(sync_status(), ensure_ascii=False, indent=2))
    elif cmd == 'sync-process':
        print(json.dumps(sync_process(), ensure_ascii=False, indent=2))
    elif cmd == 'sync-watch':
        sync_watch()
    
    elif cmd == 'sync-cleanup':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        print(json.dumps(sync_cleanup(days), ensure_ascii=False, indent=2))
    
    elif cmd == 'sync-verify':
        table = sys.argv[2] if len(sys.argv) > 2 else None
        if not table:
            print("Usage: pg_copilot.py sync-verify <table> [sample_size]")
            sys.exit(1)
        sample_size = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        print(json.dumps(sync_verify(table, sample_size), ensure_ascii=False, indent=2))
    
    elif cmd == 'conflict-strategy':
        table = sys.argv[2] if len(sys.argv) > 2 else None
        strategy = sys.argv[3] if len(sys.argv) > 3 else 'update'
        if not table or strategy not in ['update', 'ignore', 'error']:
            print("Usage: pg_copilot.py conflict-strategy <table> <update|ignore|error>")
            sys.exit(1)
        print(json.dumps(set_conflict_strategy(table, strategy, strategy), ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
