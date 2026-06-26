#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JVM + MySQL Metrics Collector
Pushes metrics to Prometheus Pushgateway.
Configure via environment variables (see below).
"""

import os
import time
import socket
import psutil
import subprocess
import requests
import re
import logging
import sys
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# ==============   Env Config   =================
# PUSHGATEWAY       # Pushgateway URL, e.g. http://pushgateway:9091
# PUSH_INTERVAL     # Push interval in seconds (default: 60)
# MYSQL_USER        # MySQL username
# MYSQL_PASSWORD    # MySQL password
# MYSQL_HOST        # MySQL host (default: 127.0.0.1)
# MYSQL_PORT        # MySQL port (default: 3306)
# GAME_ROOT_DIR     # Game server root path, e.g. /data/game
# GAME_PROCESS_NAME # Java process cmdline match string, e.g. com.example.game.main
# AGENT_LOG_FILE    # Log file path (default: /var/log/game_monitor/agent.log)
# HISTO_INTERVAL    # Class histogram collection interval in seconds (default: 600)

PUSHGATEWAY = os.environ.get("PUSHGATEWAY", "")
PUSH_INTERVAL = int(os.environ.get("PUSH_INTERVAL", "60"))

MYSQL_USER = os.environ.get("MYSQL_USER", "")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))

GAME_ROOT = os.environ.get("GAME_ROOT_DIR", "/data/game")
GAME_PROCESS_NAME = os.environ.get("GAME_PROCESS_NAME", "java")

LOG_FILE = os.environ.get("AGENT_LOG_FILE", "/var/log/game_monitor/agent.log")
HISTO_INTERVAL = int(os.environ.get("HISTO_INTERVAL", "600"))

HOSTNAME = socket.gethostname()

# ==============   Logging   =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# ================= Metrics   =================
jvm_registry = CollectorRegistry()

heap_used = Gauge("heap_used_bytes", "", ["hostname", "game_dir"], registry=jvm_registry)
heap_committed = Gauge("heap_committed_bytes", "", ["hostname", "game_dir"], registry=jvm_registry)
young_used = Gauge("young_used_bytes", "", ["hostname", "game_dir"], registry=jvm_registry)
young_max = Gauge("young_max_bytes", "", ["hostname", "game_dir"], registry=jvm_registry)
old_used = Gauge("old_used_bytes", "", ["hostname", "game_dir"], registry=jvm_registry)
old_max = Gauge("old_max_bytes", "", ["hostname", "game_dir"], registry=jvm_registry)

gc_time = Gauge("gc_time_seconds", "", ["hostname", "game_dir"], registry=jvm_registry)
gc_count = Gauge("gc_count", "", ["hostname", "game_dir"], registry=jvm_registry)
threads = Gauge("threads_live", "", ["hostname", "game_dir"], registry=jvm_registry)

jvm_up = Gauge("jvm_up", "", ["hostname", "game_dir"], registry=jvm_registry)
jvm_start_time = Gauge("jvm_start_time_seconds", "", ["hostname", "game_dir"], registry=jvm_registry)

jvm_class_bytes = Gauge(
    "jvm_class_bytes", "Top class memory usage",
    ["hostname", "game_dir", "class"], registry=jvm_registry
)

jvm_class_instance_count = Gauge(
    "jvm_class_instance_count", "Top class instances count",
    ["hostname", "game_dir", "class"], registry=jvm_registry
)

# MySQL
mysql_registry = CollectorRegistry()
mysql_up = Gauge("mysql_up", "", ["hostname"], registry=mysql_registry)
mysql_rss = Gauge("mysql_process_resident_memory_bytes", "", ["hostname"], registry=mysql_registry)
buffer_used = Gauge("innodb_buffer_pool_bytes_data", "", ["hostname"], registry=mysql_registry)
buffer_total = Gauge("innodb_buffer_pool_bytes_total", "", ["hostname"], registry=mysql_registry)

# ================= GC Cache   =================
last_gc_time = {}
last_gc_count = {}

# ================= Histogram Throttle   =================
last_histo_time = {}
last_histo_global = 0


# ================= Main Server Detection   =================
def is_main_server(cmd, game_dir):
    """Detect main server by JVM heap size in cmdline."""
    if "_game_s" not in game_dir:
        return False
    if "test" in game_dir or "dev" in game_dir:
        return False

    m = re.search(r"-Xmx(\d+)([mMgG])", cmd)
    if not m:
        return False

    size = int(m.group(1))
    unit = m.group(2).lower()
    if unit == "g":
        size *= 1024

    return size >= 2048


# ================= JVM Scan   =================
def get_jvms():
    jvms = {}
    for p in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmdline = p.info["cmdline"]
            if not cmdline:
                continue

            cmd_str = " ".join(cmdline)
            if GAME_PROCESS_NAME not in cmd_str:
                continue

            for arg in cmdline:
                if arg.startswith(GAME_ROOT):
                    parts = arg.split("/")
                    if len(parts) > 4:
                        game_dir = parts[4]
                        jvms[game_dir] = p.info["pid"]
                        break
        except Exception:
            pass
    return jvms


# ================= JCMD Histogram Collection   =================
def collect_class_histo(game_dir, pid):
    try:
        out = subprocess.check_output(
            ["jcmd", str(pid), "GC.class_histogram"],
            stderr=subprocess.DEVNULL, timeout=15
        ).decode(errors="ignore")

        count = 0
        for line in out.splitlines():
            line = line.strip()
            if not line or "class name" in line or line.startswith("total"):
                continue

            m = re.match(r"^\d+:\s+(\d+)\s+(\d+)\s+(.+)$", line)
            if not m:
                continue

            instances = int(m.group(1))
            bytes_ = int(m.group(2))
            clazz = m.group(3)

            if len(clazz) > 80:
                clazz = clazz[:80]

            jvm_class_instance_count.labels(HOSTNAME, game_dir, clazz).set(instances)
            jvm_class_bytes.labels(HOSTNAME, game_dir, clazz).set(bytes_)

            count += 1
            if count >= 50:
                break

        logging.info(f"jcmd collected class histo for {game_dir}")

    except Exception as e:
        logging.exception(f"jcmd failed for {game_dir}: {e}")


# ================= JVM Metrics Collection   =================
def collect_jvm(game_dir, pid):
    key = f"{HOSTNAME}_{game_dir}"

    try:
        out = subprocess.check_output(["jstat", "-gc", str(pid)]).decode().splitlines()[-1].split()

        # Memory
        s0u, s1u, eu = float(out[2]), float(out[3]), float(out[5])
        young = (s0u + s1u + eu) * 1024
        young_cap = (float(out[0]) + float(out[1]) + float(out[4])) * 1024

        old = float(out[7]) * 1024
        old_cap = float(out[6]) * 1024

        heap = young + old
        heap_committed_cap = young_cap + old_cap

        # GC
        gc_total_time = float(out[14]) + float(out[15])
        ygc = float(out[12])
        fgc = float(out[13])
        gc_total_count = ygc + fgc

        # Delta
        gc_delta = 0
        if key in last_gc_time:
            gc_delta = max(0, gc_total_time - last_gc_time[key])
        last_gc_time[key] = gc_total_time

        count_delta = 0
        if key in last_gc_count:
            count_delta = max(0, gc_total_count - last_gc_count[key])
        last_gc_count[key] = gc_total_count

        # Threads
        t = psutil.Process(pid).num_threads()
        start = psutil.Process(pid).create_time()

        # Set metrics
        young_used.labels(HOSTNAME, game_dir).set(young)
        young_max.labels(HOSTNAME, game_dir).set(young_cap)
        old_used.labels(HOSTNAME, game_dir).set(old)
        old_max.labels(HOSTNAME, game_dir).set(old_cap)
        heap_used.labels(HOSTNAME, game_dir).set(heap)
        heap_committed.labels(HOSTNAME, game_dir).set(heap_committed_cap)
        gc_time.labels(HOSTNAME, game_dir).set(gc_delta)
        gc_count.labels(HOSTNAME, game_dir).set(count_delta)
        threads.labels(HOSTNAME, game_dir).set(t)
        jvm_up.labels(HOSTNAME, game_dir).set(1)
        jvm_start_time.labels(HOSTNAME, game_dir).set(start)

        logging.info(f"JVM collected for {game_dir} (pid={pid})")

        # Throttled class histogram
        global last_histo_global
        now = time.time()
        if key not in last_histo_time or now - last_histo_time[key] > HISTO_INTERVAL:
            if now - last_histo_global > 30:
                collect_class_histo(game_dir, pid)
                last_histo_time[key] = now
                last_histo_global = now

    except Exception as e:
        logging.exception(f"JVM collection failed for {game_dir}: {e}")


# ================= MySQL Collection   =================
def collect_mysql():
    if not MYSQL_USER or not MYSQL_PASSWORD:
        logging.warning("MySQL credentials not configured, skipping MySQL collection")
        return

    try:
        import pymysql
        conn = pymysql.connect(
            host=MYSQL_HOST, user=MYSQL_USER,
            password=MYSQL_PASSWORD, port=MYSQL_PORT
        )
        cur = conn.cursor()

        cur.execute("show global status like 'Innodb_buffer_pool_bytes_data'")
        row = cur.fetchone()
        if row:
            buffer_used.labels(HOSTNAME).set(int(row[1]))

        cur.execute("show variables like 'innodb_buffer_pool_size'")
        row = cur.fetchone()
        if row:
            buffer_total.labels(HOSTNAME).set(int(row[1]))

        conn.close()

        mysql_up.labels(HOSTNAME).set(1)
        for p in psutil.process_iter(["name", "memory_info"]):
            if p.info["name"] and "mysql" in p.info["name"].lower():
                mysql_rss.labels(HOSTNAME).set(p.info["memory_info"].rss)

        logging.info(f"MySQL metrics collected for {HOSTNAME}")

    except Exception as e:
        mysql_up.labels(HOSTNAME).set(0)
        logging.exception(f"MySQL collection failed for {HOSTNAME}: {e}")


# ================= Push =================
def push_metrics():
    if not PUSHGATEWAY:
        logging.error("PUSHGATEWAY environment variable is not set")
        return

    push_to_gateway(
        PUSHGATEWAY, job="game_jvm",
        grouping_key={"instance": HOSTNAME}, registry=jvm_registry)
    push_to_gateway(
        PUSHGATEWAY, job="game_mysql",
        grouping_key={"instance": HOSTNAME}, registry=mysql_registry)


# ================= Main Loop   =================
def main():
    logging.info(f"Agent starting, hostname={HOSTNAME}, game_root={GAME_ROOT}")
    if not PUSHGATEWAY:
        logging.error("PUSHGATEWAY env not set, exiting")
        sys.exit(1)

    old = set()

    while True:
        try:
            current = get_jvms()

            # Mark all previously known as down
            for g in old:
                jvm_up.labels(HOSTNAME, g).set(0)

            for g, pid in current.items():
                collect_jvm(g, pid)

            collect_mysql()
            old = set(current.keys())

            push_metrics()

        except Exception as e:
            logging.exception(f"Main loop error: {e}")

        time.sleep(PUSH_INTERVAL)


if __name__ == "__main__":
    main()
