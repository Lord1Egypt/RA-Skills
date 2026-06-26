"""
Nex Domains - Storage & Database
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
Domain portfolio database management
"""
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

from config import DATA_DIR, DB_PATH, LOG_PATH

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database with all required tables."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Domains table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE NOT NULL,
            registrar TEXT NOT NULL,
            registration_date TEXT,
            expiry_date TEXT,
            auto_renew BOOLEAN DEFAULT 0,
            nameservers TEXT,
            ssl_expiry TEXT,
            ssl_issuer TEXT,
            dns_provider TEXT,
            hosting_provider TEXT,
            client TEXT,
            monthly_cost REAL,
            status TEXT DEFAULT 'active',
            tags TEXT,
            notes TEXT,
            last_checked TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

    # DNS records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_id INTEGER NOT NULL,
            record_type TEXT NOT NULL,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            ttl INTEGER,
            proxied BOOLEAN DEFAULT 0,
            priority INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (domain_id) REFERENCES domains(id) ON DELETE CASCADE
        )
    ''')

    # Domain checks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domain_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_id INTEGER NOT NULL,
            check_type TEXT NOT NULL,
            status TEXT NOT NULL,
            details TEXT,
            checked_at TEXT NOT NULL,
            FOREIGN KEY (domain_id) REFERENCES domains(id) ON DELETE CASCADE
        )
    ''')

    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain ON domains(domain)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_registrar ON domains(registrar)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_client ON domains(client)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON domains(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_expiry ON domains(expiry_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain_id ON dns_records(domain_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_check_domain ON domain_checks(domain_id)')

    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {DB_PATH}")


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_domain(domain: str, registrar: str, client: str = None, auto_renew: bool = False,
                monthly_cost: float = None, status: str = "active", notes: str = None) -> int:
    """Save a new domain or update existing."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    try:
        cursor.execute(
            '''INSERT INTO domains
            (domain, registrar, client, auto_renew, monthly_cost, status, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (domain, registrar, client, auto_renew, monthly_cost, status, notes, now, now)
        )
        conn.commit()
        domain_id = cursor.lastrowid
        logger.info(f"Domain saved: {domain} (ID: {domain_id})")
        return domain_id
    except sqlite3.IntegrityError:
        logger.warning(f"Domain already exists: {domain}")
        return get_domain(domain)['id']
    finally:
        conn.close()


def get_domain(domain: str) -> Optional[Dict]:
    """Get a domain by name."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM domains WHERE domain = ?', (domain,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def get_domain_by_id(domain_id: int) -> Optional[Dict]:
    """Get a domain by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM domains WHERE id = ?', (domain_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def list_domains(registrar: str = None, client: str = None, expiring_within: int = None,
                 status: str = None) -> List[Dict]:
    """List domains with optional filters."""
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM domains WHERE 1=1'
    params = []

    if registrar:
        query += ' AND registrar = ?'
        params.append(registrar)

    if client:
        query += ' AND client = ?'
        params.append(client)

    if status:
        query += ' AND status = ?'
        params.append(status)

    if expiring_within:
        query += ' AND expiry_date IS NOT NULL AND date(expiry_date) <= date(?, "+{} days")'.format(expiring_within)
        params.append(datetime.utcnow().isoformat()[:10])

    query += ' ORDER BY domain'

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def update_domain(domain_id: int, **kwargs) -> bool:
    """Update domain fields."""
    conn = get_connection()
    cursor = conn.cursor()

    # Whitelist allowed fields
    allowed_fields = [
        'registrar', 'registration_date', 'expiry_date', 'auto_renew',
        'nameservers', 'ssl_expiry', 'ssl_issuer', 'dns_provider',
        'hosting_provider', 'client', 'monthly_cost', 'status', 'tags', 'notes'
    ]

    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    if not updates:
        conn.close()
        return False

    updates['updated_at'] = datetime.utcnow().isoformat()

    set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
    values = list(updates.values()) + [domain_id]

    cursor.execute(f'UPDATE domains SET {set_clause} WHERE id = ?', values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected > 0:
        logger.info(f"Domain {domain_id} updated")

    return affected > 0


def delete_domain(domain_id: int) -> bool:
    """Delete a domain and all related data."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM domains WHERE id = ?', (domain_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()

    if affected > 0:
        logger.info(f"Domain {domain_id} deleted")

    return affected > 0


def save_dns_records(domain_id: int, records: List[Dict]) -> int:
    """Save DNS records for a domain."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    # Delete existing records
    cursor.execute('DELETE FROM dns_records WHERE domain_id = ?', (domain_id,))

    # Insert new records
    count = 0
    for record in records:
        cursor.execute('''
            INSERT INTO dns_records
            (domain_id, record_type, name, content, ttl, proxied, priority, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            domain_id,
            record.get('type', ''),
            record.get('name', ''),
            record.get('content', ''),
            record.get('ttl'),
            record.get('proxied', False),
            record.get('priority'),
            now,
            now
        ))
        count += 1

    conn.commit()
    conn.close()
    logger.info(f"Saved {count} DNS records for domain {domain_id}")
    return count


def get_dns_records(domain_id: int, record_type: str = None) -> List[Dict]:
    """Get DNS records for a domain."""
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM dns_records WHERE domain_id = ?'
    params = [domain_id]

    if record_type:
        query += ' AND record_type = ?'
        params.append(record_type)

    query += ' ORDER BY record_type, name'

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_expiring_domains(days: int = 90) -> List[Dict]:
    """Get domains expiring within N days."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM domains
        WHERE expiry_date IS NOT NULL
        AND date(expiry_date) <= date('now', ?)
        AND status != 'expired'
        ORDER BY expiry_date
    ''', (f'+{days} days',))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_expiring_ssl(days: int = 30) -> List[Dict]:
    """Get domains with SSL certs expiring within N days."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM domains
        WHERE ssl_expiry IS NOT NULL
        AND date(ssl_expiry) <= date('now', ?)
        ORDER BY ssl_expiry
    ''', (f'+{days} days',))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_domain_stats() -> Dict[str, Any]:
    """Get portfolio statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total domains
    cursor.execute('SELECT COUNT(*) as count FROM domains')
    total = cursor.fetchone()['count']

    # By registrar
    cursor.execute('''
        SELECT registrar, COUNT(*) as count FROM domains
        GROUP BY registrar ORDER BY count DESC
    ''')
    by_registrar = {row['registrar']: row['count'] for row in cursor.fetchall()}

    # By status
    cursor.execute('''
        SELECT status, COUNT(*) as count FROM domains
        GROUP BY status ORDER BY count DESC
    ''')
    by_status = {row['status']: row['count'] for row in cursor.fetchall()}

    # By client
    cursor.execute('''
        SELECT client, COUNT(*) as count FROM domains
        WHERE client IS NOT NULL
        GROUP BY client ORDER BY count DESC
    ''')
    by_client = {row['client']: row['count'] for row in cursor.fetchall()}

    # Total monthly cost
    cursor.execute('SELECT SUM(monthly_cost) as total FROM domains WHERE monthly_cost IS NOT NULL')
    total_cost = cursor.fetchone()['total'] or 0

    # Expiring soon
    cursor.execute('''
        SELECT COUNT(*) as count FROM domains
        WHERE expiry_date IS NOT NULL
        AND date(expiry_date) <= date('now', '+90 days')
        AND status != 'expired'
    ''')
    expiring_soon = cursor.fetchone()['count']

    conn.close()

    return {
        'total_domains': total,
        'by_registrar': by_registrar,
        'by_status': by_status,
        'by_client': by_client,
        'total_monthly_cost': total_cost,
        'expiring_soon_90d': expiring_soon,
    }


def search_domains(query: str) -> List[Dict]:
    """Search domains by name, client, or tags."""
    conn = get_connection()
    cursor = conn.cursor()

    search_term = f'%{query}%'
    cursor.execute('''
        SELECT * FROM domains
        WHERE domain LIKE ? OR client LIKE ? OR tags LIKE ? OR notes LIKE ?
        ORDER BY domain
    ''', (search_term, search_term, search_term, search_term))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def export_domains(format: str = 'csv') -> str:
    """Export domains to CSV or JSON."""
    domains = list_domains()

    if format == 'json':
        return json.dumps(domains, indent=2, default=str)

    elif format == 'csv':
        import csv
        from io import StringIO

        output = StringIO()
        if not domains:
            return "No domains to export"

        fieldnames = list(domains[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(domains)

        return output.getvalue()

    return ""


def save_check_result(domain_id: int, check_type: str, status: str, details: Dict) -> int:
    """Save domain check result."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    cursor.execute('''
        INSERT INTO domain_checks
        (domain_id, check_type, status, details, checked_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (domain_id, check_type, status, json.dumps(details, default=str), now))

    conn.commit()
    check_id = cursor.lastrowid
    conn.close()

    logger.info(f"Check result saved: {domain_id} - {check_type} - {status}")
    return check_id


def get_check_history(domain_id: int, check_type: str = None, limit: int = 20) -> List[Dict]:
    """Get domain check history."""
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM domain_checks WHERE domain_id = ?'
    params = [domain_id]

    if check_type:
        query += ' AND check_type = ?'
        params.append(check_type)

    query += ' ORDER BY checked_at DESC LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        r = dict(row)
        if r['details']:
            r['details'] = json.loads(r['details'])
        result.append(r)

    return result
