#!/usr/bin/env python3
"""LMDB vs hipool vs SQLite 性能对比基准测试"""
import lmdb
import sqlite3
import time
import random
import string
import subprocess
import os
import sys

N = 50000
VAL_SIZES = [32, 256, 1024, 4096]
ENTRIES_PER_BATCH = 50000

def rand_str(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def ns():
    return time.time_ns()

# ========== LMDB Benchmark ==========
def bench_lmdb():
    print(f"\n{'='*60}")
    print(f"  LMDB Benchmark (n={N})")
    print(f"{'='*60}")
    
    for val_size in VAL_SIZES:
        env_path = f"/tmp/bench_lmdb_{val_size}"
        os.system(f"rm -rf {env_path}")
        
        env = lmdb.open(env_path, map_size=104857600, metasync=False, sync=False)  # 100MB, no fsync
        samples_set = []
        samples_get = []
        
        # Pre-generate keys/values
        keys = [rand_str(16) for _ in range(N)]
        vals = [rand_str(val_size) for _ in range(N)]
        
        # SET benchmark
        for i in range(N):
            with env.begin(write=True) as txn:
                k = keys[i].encode()
                v = vals[i].encode()
                t0 = ns()
                txn.put(k, v)
                samples_set.append(ns() - t0)
        
        # GET benchmark
        for i in range(N):
            with env.begin() as txn:
                k = keys[i].encode()
                t0 = ns()
                txn.get(k)
                samples_get.append(ns() - t0)
        
        env.close()
        
        def report(samples, label):
            samples.sort()
            n = len(samples)
            p50 = samples[int(n*0.50)]
            p90 = samples[int(n*0.90)]
            p99 = samples[int(n*0.99)]
            p999 = samples[int(n*0.999)]
            avg = sum(samples) / n
            print(f"  {label:15s} val={val_size:<5}B  n={n:<6}  avg={avg:<8.0f}ns  p50={p50:<6}  p90={p90:<6}  p99={p99:<6}  p999={p999:<6}")
        
        report(samples_set, "LMDB SET")
        report(samples_get, "LMDB GET")
        
        os.system(f"rm -rf {env_path}")

# ========== SQLite Benchmark ==========
def bench_sqlite():
    print(f"\n{'='*60}")
    print(f"  SQLite Benchmark (n={N})")
    print(f"{'='*60}")
    
    for val_size in VAL_SIZES:
        db_path = f"/tmp/bench_sqlite_{val_size}.db"
        os.system(f"rm -f {db_path}")
        
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA synchronous=OFF")
        conn.execute("PRAGMA journal_mode=MEMORY")
        conn.execute("CREATE TABLE IF NOT EXISTS mem (key TEXT PRIMARY KEY, value TEXT)")
        
        # Prepared statement
        c = conn.cursor()
        samples_set = []
        samples_get = []
        
        keys = [rand_str(16) for _ in range(N)]
        vals = [rand_str(val_size) for _ in range(N)]
        
        # SET benchmark (reuse prepared statement)
        for i in range(N):
            t0 = ns()
            c.execute("INSERT OR REPLACE INTO mem VALUES (?,?)", (keys[i], vals[i]))
            samples_set.append(ns() - t0)
        conn.commit()
        
        # GET benchmark
        for i in range(N):
            t0 = ns()
            c.execute("SELECT value FROM mem WHERE key=?", (keys[i],))
            conn.fetchone() if hasattr(conn, 'fetchone') else c.fetchone()
            samples_get.append(ns() - t0)
        
        conn.close()
        
        def report(samples, label):
            samples.sort()
            n = len(samples)
            p50 = samples[int(n*0.50)]
            p90 = samples[int(n*0.90)]
            p99 = samples[int(n*0.99)]
            p999 = samples[int(n*0.999)]
            avg = sum(samples) / n
            print(f"  {label:15s} val={val_size:<5}B  n={n:<6}  avg={avg:<8.0f}ns  p50={p50:<6}  p90={p90:<6}  p99={p99:<6}  p999={p999:<6}")
        
        report(samples_set, "SQLite SET")
        report(samples_get, "SQLite GET")
        
        os.system(f"rm -f {db_path}")

def bench_redis():
    """用 redis-benchmark 工具"""
    print(f"\n{'='*60}")
    print(f"  Redis Benchmark (via redis-benchmark)")
    print(f"{'='*60}")
    
    # Check if redis is running
    result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != "PONG":
        print("  Redis not running. Starting...")
        subprocess.run(["redis-server", "--daemonize", "yes"], capture_output=True)
        time.sleep(1)
    
    for val_size in VAL_SIZES:
        print(f"  Value size: {val_size}B")
        # Use redis-benchmark
        for mode, cmd in [("SET", "SET"), ("GET", "GET")]:
            result = subprocess.run(
                ["redis-benchmark", "-n", str(N), "-d", str(val_size), 
                 "-t", cmd, "--csv"],
                capture_output=True, text=True, timeout=120
            )
            output = result.stdout + result.stderr
            # Parse: find the relevant line
            for line in output.split('\n'):
                if cmd in line and 'ms' in line:
                    print(f"    {mode:15s} {line.strip()}")

def parse_hipool_results():
    """Parse the hipool microbenchmark output if available"""
    print(f"\n{'='*60}")
    print(f"  hipool (from bench_micro binary)")
    print(f"{'='*60}")
    print(f"  (Run ./bench_micro separately for full data)")
    
if __name__ == "__main__":
    print("=" * 60)
    print("  Cross-Platform Memory Benchmark Suite")
    print("  Platform: AMD EPYC 7K62")
    print(f"  N={N}, value sizes: {VAL_SIZES}")
    print("=" * 60)
    
    bench_lmdb()
    bench_sqlite()
    bench_redis()
    
    print(f"\n{'='*60}")
    print("  All done.")
    print(f"{'='*60}")
