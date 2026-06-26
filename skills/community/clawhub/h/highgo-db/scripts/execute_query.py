import sys
import os
import json
import argparse
import tempfile
import shutil

def execute_query(dsn, sql, driver_path=None):
    # If no driver_path provided, look in the skill's assets/driver/psycopg2
    if driver_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        driver_path = os.path.join(script_dir, "..", "assets", "driver", "psycopg2")
    
    if not os.path.exists(driver_path):
        return {"status": "error", "message": "Driver not found at {}".format(driver_path)}

    # Manual temporary directory for Python 2.7 compatibility
    tmp_dir = tempfile.mkdtemp()
    try:
        target_path = os.path.join(tmp_dir, "psycopg2")
        if not os.path.exists(target_path):
            os.symlink(os.path.abspath(driver_path), target_path)
        
        # Add the driver path to LD_LIBRARY_PATH for the .so libraries
        env = os.environ.copy()
        driver_abs_path = os.path.abspath(driver_path)
        if "LD_LIBRARY_PATH" in env:
            os.environ["LD_LIBRARY_PATH"] = "{}:{}".format(driver_abs_path, env['LD_LIBRARY_PATH'])
        else:
            os.environ["LD_LIBRARY_PATH"] = driver_abs_path
        
        # Add the temp directory to sys.path
        sys.path.insert(0, tmp_dir)
        
        try:
            import psycopg2
            from psycopg2 import extras
            
            conn = psycopg2.connect(dsn)
            # Use DictCursor to get results with column names
            cur = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            # Execute multiple statements if necessary
            cur.execute(sql)
            
            results = None
            if cur.description:
                results = cur.fetchall()
            
            conn.commit()
            cur.close()
            conn.close()
            
            return {"status": "success", "results": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    finally:
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute SQL on HighGo DB using built-in psycopg2")
    parser.add_argument("--dsn", required=True, help="Connection DSN")
    parser.add_argument("--sql", required=True, help="SQL query or path to SQL file")
    parser.add_argument("--driver", required=False, help="Path to psycopg2 directory (optional, uses built-in if omitted)")
    
    args = parser.parse_args()
    
    sql_content = args.sql
    if os.path.exists(args.sql):
        with open(args.sql, "r") as f:
            sql_content = f.read()
            
    result = execute_query(args.dsn, sql_content, args.driver)
    print(json.dumps(result))
