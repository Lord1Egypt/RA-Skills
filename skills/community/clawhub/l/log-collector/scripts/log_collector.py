#!/usr/bin/env python3
"""
Log Collector Sub-Agent
Sammelt Logs von allen Nodes via SSH/VPN alle 3 Stunden
"""

import sqlite3
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
DB_PATH = WORKSPACE / "db" / "logs.db"
LOG_DIR = WORKSPACE / "logs" / "log-collector"

LOG_DIR.mkdir(parents=True, exist_ok=True)


class Logger:
    def __init__(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.log_file = LOG_DIR / f"{today}.log"
        
    def log(self, level, msg):
        ts = datetime.now().isoformat()
        line = f"[{ts}] [{level}] {msg}"
        print(line)
        with open(self.log_file, 'a') as f:
            f.write(line + '\n')
    
    def info(self, msg): self.log('INFO', msg)
    def error(self, msg): self.log('ERROR', msg)


class LogCollector:
    def __init__(self):
        self.logger = Logger()
        self.conn = None
        
    def connect_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        # Schema initialisieren falls nicht existiert
        self._init_schema()
        return self.conn
    
    def _init_schema(self):
        """Liest schema.sql falls DB leer"""
        if not list(self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")):
            schema_path = WORKSPACE / "db" / "logs.db.schema.sql"
            if schema_path.exists():
                with open(schema_path) as f:
                    self.conn.executescript(f.read())
                self.conn.commit()
    
    def get_nodes(self):
        """Holt Liste aller Nodes aus DB"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM nodes")
        return [dict(row) for row in cursor.fetchall()]
    
    def check_vpn(self, ip):
        """Prüft ob VPN-IP erreichbar ist"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', ip],
                capture_output=True, timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def ssh_connect_and_collect(self, node):
        """Verbindet via SSH und sammelt Logs"""
        node_id = node['node_id']
        vpn_ip = node.get('vpn_ip') or node.get('tailscale_ip') or node.get('wireguard_ip')
        
        if not vpn_ip:
            self.logger.error(f"{node_id}: Keine VPN-IP konfiguriert")
            return None
        
        # 1. VPN-Check
        self.logger.info(f"{node_id}: Prüfe VPN {vpn_ip}...")
        if not self.check_vpn(vpn_ip):
            self.logger.error(f"{node_id}: VPN nicht erreichbar")
            self._log_ssh_connection(node_id, 'tailscale', False, 'VPN unreachable')
            return None
        
        # 2. SSH-Verbindung
        self.logger.info(f"{node_id}: Verbinde via SSH...")
        try:
            # Logs abholen (ohne cd wegen exec-Beschränkungen)
            log_commands = [
                "journalctl -n 500 --no-pager",
                "tail -n 200 /var/log/syslog 2>/dev/null || echo 'no syslog'",
                "tail -n 200 ~/.openclaw/logs/*.log 2>/dev/null || echo 'no openclaw logs'"
            ]
            
            logs_collected = []
            for cmd in log_commands:
                result = subprocess.run(
                    ['ssh', '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=no',
                     f'openclaw@{vpn_ip}', cmd],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    logs_collected.append({
                        'command': cmd,
                        'output': result.stdout,
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Erfolg loggen
            self._log_ssh_connection(node_id, 'ssh', True, None)
            
            # In DB speichern
            self._insert_logs(node_id, logs_collected)
            
            return len(logs_collected)
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"{node_id}: SSH Timeout")
            self._log_ssh_connection(node_id, 'ssh', False, 'Timeout')
            return None
        except FileNotFoundError:
            self.logger.error(f"{node_id}: SSH nicht verfügbar")
            return None
        except Exception as e:
            self.logger.error(f"{node_id}: SSH Fehler: {e}")
            self._log_ssh_connection(node_id, 'ssh', False, str(e))
            return None
    
    def _log_ssh_connection(self, node_id, conn_type, success, error):
        """Loggt SSH-Verbindungsversuch"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO ssh_connections (node_id, connection_type, success, error_message)
            VALUES (?, ?, ?, ?)
        ''', (node_id, conn_type, success, error))
        self.conn.commit()
    
    def _insert_logs(self, node_id, logs):
        """Speichert Logs in Datenbank"""
        cursor = self.conn.cursor()
        retention = datetime.now() + timedelta(days=30)
        
        for log_entry in logs:
            cursor.execute('''
                INSERT INTO logs (node_id, log_type, source, content, severity, 
                                collected_by, collection_method, retention_until)
                VALUES (?, 'system', ?, ?, 'info', ?, 'ssh', ?)
            ''', (
                node_id,
                log_entry['command'][:50],
                log_entry['output'][:10000],  # Limit 10KB
                'node1',  # collected_by
                retention.isoformat()
            ))
        
        self.conn.commit()
        self.logger.info(f"{node_id}: {len(logs)} Log-Einträge gespeichert")
    
    def cleanup_retention(self):
        """Löscht Logs älter 30 Tage"""
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM logs WHERE retention_until < datetime('now')
        ''')
        deleted = cursor.rowcount
        self.conn.commit()
        self.logger.info(f"Retention-Cleanup: {deleted} alte Logs gelöscht")
        return deleted
    
    def run_collection_cycle(self):
        """Ein kompletter Sammel-Durchlauf"""
        self.logger.info("="*60)
        self.logger.info("LOG COLLECTOR CYCLE START")
        self.logger.info("="*60)
        
        self.connect_db()
        
        # 1. Nodes holen
        nodes = self.get_nodes()
        self.logger.info(f"Gefunden: {len(nodes)} Nodes")
        
        # 2. Collection-Run starten
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO collection_runs (started_at, nodes_total)
            VALUES (CURRENT_TIMESTAMP, ?)
        ''', (len(nodes),))
        run_id = cursor.lastrowid
        self.conn.commit()
        
        # 3. Für jeden Node sammeln
        success_count = 0
        failed_count = 0
        total_logs = 0
        
        for node in nodes:
            if node['node_id'] == 'node1':
                # Lokale Logs (Gateway selbst)
                self.logger.info("node1: Lokale Collection (Gateway)")
                success_count += 1
            else:
                # Remote-Node abfragen
                result = self.ssh_connect_and_collect(node)
                if result is not None:
                    success_count += 1
                    total_logs += result
                else:
                    failed_count += 1
        
        # 4. Run abschließen
        cursor.execute('''
            UPDATE collection_runs SET
                finished_at = CURRENT_TIMESTAMP,
                nodes_success = ?,
                nodes_failed = ?,
                logs_collected = ?
            WHERE run_id = ?
        ''', (success_count, failed_count, total_logs, run_id))
        self.conn.commit()
        
        # 5. Retention-Cleanup
        self.logger.info("Retention-Cleanup (30 Tage)...")
        self.cleanup_retention()
        
        self.logger.info("="*60)
        self.logger.info(f"SUMMARY: {success_count} OK, {failed_count} Failed, {total_logs} Logs")
        self.logger.info("="*60)


def main():
    print("="*60)
    print("LOG COLLECTOR")
    print("="*60)
    
    collector = LogCollector()
    
    try:
        collector.run_collection_cycle()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
