"""
Nex Deliverables - Storage & Database
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

SQLite database management for clients, deliverables, milestones, and status updates.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from config import DB_PATH, DATA_DIR, DATE_FORMAT, DATETIME_FORMAT, DEFAULT_SLA_DAYS, STATUSES


def _get_conn():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with schema"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = _get_conn()
    cursor = conn.cursor()

    # Clients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            contact_name TEXT,
            email TEXT,
            phone TEXT,
            retainer_amount REAL,
            retainer_tier TEXT,
            contract_start TEXT,
            contract_end TEXT,
            status TEXT DEFAULT 'active',
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Deliverables table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deliverables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'planned',
            priority TEXT DEFAULT 'normal',
            assigned_to TEXT,
            deadline TEXT,
            started_at TEXT,
            delivered_at TEXT,
            approved_at TEXT,
            estimated_hours REAL,
            actual_hours REAL,
            notes TEXT,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    # Milestones table (for tracking sub-tasks within deliverables)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deliverable_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            completed_at TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (deliverable_id) REFERENCES deliverables(id)
        )
    """)

    # Status updates history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deliverable_id INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            message TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (deliverable_id) REFERENCES deliverables(id)
        )
    """)

    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_deliverables_client ON deliverables(client_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_deliverables_status ON deliverables(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_deliverables_deadline ON deliverables(deadline)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_milestones_deliverable ON milestones(deliverable_id)")

    conn.commit()
    conn.close()


def save_client(name: str, contact_name: Optional[str] = None, email: Optional[str] = None,
                phone: Optional[str] = None, retainer_amount: Optional[float] = None,
                retainer_tier: Optional[str] = None, contract_start: Optional[str] = None,
                contract_end: Optional[str] = None, status: str = "active",
                notes: Optional[str] = None) -> int:
    """Save a new client or update existing"""
    conn = _get_conn()
    cursor = conn.cursor()
    now = datetime.now().strftime(DATETIME_FORMAT)

    try:
        cursor.execute("""
            INSERT INTO clients (name, contact_name, email, phone, retainer_amount,
                               retainer_tier, contract_start, contract_end, status, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, contact_name, email, phone, retainer_amount, retainer_tier,
              contract_start, contract_end, status, notes, now))
        conn.commit()
        client_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Client exists, update instead
        cursor.execute("""
            UPDATE clients SET contact_name=?, email=?, phone=?, retainer_amount=?,
                            retainer_tier=?, contract_start=?, contract_end=?, status=?, notes=?
            WHERE name=?
        """, (contact_name, email, phone, retainer_amount, retainer_tier,
              contract_start, contract_end, status, notes, name))
        conn.commit()
        cursor.execute("SELECT id FROM clients WHERE name=?", (name,))
        client_id = cursor.fetchone()[0]

    conn.close()
    return client_id


def get_client(client_id: int) -> Optional[Dict[str, Any]]:
    """Get client details by ID"""
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_client_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get client by name"""
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def list_clients(status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """List all clients, optionally filtered by status"""
    conn = _get_conn()
    cursor = conn.cursor()

    if status:
        cursor.execute("SELECT * FROM clients WHERE status=? ORDER BY name LIMIT ?",
                      (status, limit))
    else:
        cursor.execute("SELECT * FROM clients ORDER BY name LIMIT ?", (limit,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_deliverable(client_id: int, title: str, type: str, deadline: Optional[str] = None,
                    description: Optional[str] = None, status: str = "planned",
                    priority: str = "normal", assigned_to: Optional[str] = None,
                    estimated_hours: Optional[float] = None, notes: Optional[str] = None,
                    tags: Optional[str] = None) -> int:
    """Save a new deliverable"""
    conn = _get_conn()
    cursor = conn.cursor()
    now = datetime.now().strftime(DATETIME_FORMAT)

    # Calculate deadline from SLA if not provided
    if not deadline and type in DEFAULT_SLA_DAYS:
        from datetime import timedelta
        days = DEFAULT_SLA_DAYS[type]
        deadline = (datetime.now() + timedelta(days=days)).strftime(DATE_FORMAT)

    cursor.execute("""
        INSERT INTO deliverables
        (client_id, title, type, deadline, description, status, priority,
         assigned_to, estimated_hours, notes, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (client_id, title, type, deadline, description, status, priority,
          assigned_to, estimated_hours, notes, tags, now, now))

    conn.commit()
    deliverable_id = cursor.lastrowid
    conn.close()
    return deliverable_id


def get_deliverable(deliverable_id: int) -> Optional[Dict[str, Any]]:
    """Get deliverable details"""
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deliverables WHERE id=?", (deliverable_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def list_deliverables(client_id: Optional[int] = None, status: Optional[str] = None,
                     type: Optional[str] = None, overdue: bool = False,
                     priority: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """List deliverables with multiple filter options"""
    conn = _get_conn()
    cursor = conn.cursor()

    query = "SELECT * FROM deliverables WHERE 1=1"
    params = []

    if client_id:
        query += " AND client_id=?"
        params.append(client_id)

    if status:
        query += " AND status=?"
        params.append(status)

    if type:
        query += " AND type=?"
        params.append(type)

    if priority:
        query += " AND priority=?"
        params.append(priority)

    if overdue:
        now = datetime.now().strftime(DATE_FORMAT)
        query += " AND deadline < ? AND status NOT IN ('delivered', 'approved')"
        params.append(now)

    query += " ORDER BY deadline ASC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_deliverable_status(deliverable_id: int, new_status: str, message: Optional[str] = None) -> bool:
    """Update deliverable status and log the change"""
    if new_status not in STATUSES:
        return False

    conn = _get_conn()
    cursor = conn.cursor()
    now = datetime.now().strftime(DATETIME_FORMAT)

    # Get current status
    cursor.execute("SELECT status FROM deliverables WHERE id=?", (deliverable_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    old_status = row[0]

    # Update deliverable
    cursor.execute("""
        UPDATE deliverables
        SET status=?, updated_at=?
        WHERE id=?
    """, (new_status, now, deliverable_id))

    # Log status change
    cursor.execute("""
        INSERT INTO status_updates (deliverable_id, old_status, new_status, message, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (deliverable_id, old_status, new_status, message, now))

    # Update timestamp fields for certain statuses
    if new_status == "in_progress":
        cursor.execute("UPDATE deliverables SET started_at=? WHERE id=?", (now, deliverable_id))
    elif new_status == "delivered":
        cursor.execute("UPDATE deliverables SET delivered_at=? WHERE id=?", (now, deliverable_id))
    elif new_status == "approved":
        cursor.execute("UPDATE deliverables SET approved_at=? WHERE id=?", (now, deliverable_id))

    conn.commit()
    conn.close()
    return True


def search_deliverables(query: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Full-text search deliverables by title, description, notes"""
    conn = _get_conn()
    cursor = conn.cursor()

    search_term = f"%{query}%"
    cursor.execute("""
        SELECT * FROM deliverables
        WHERE title LIKE ? OR description LIKE ? OR notes LIKE ?
        ORDER BY created_at DESC LIMIT ?
    """, (search_term, search_term, search_term, limit))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_client_summary(client_id: int) -> Dict[str, Any]:
    """Get summary of deliverables for a client"""
    conn = _get_conn()
    cursor = conn.cursor()

    # Count by status
    summary = {
        "client_id": client_id,
        "total": 0,
        "by_status": {},
        "overdue": 0,
        "in_progress": 0,
        "delivered": 0,
        "approved": 0,
    }

    for status in STATUSES:
        cursor.execute(
            "SELECT COUNT(*) FROM deliverables WHERE client_id=? AND status=?",
            (client_id, status)
        )
        count = cursor.fetchone()[0]
        summary["by_status"][status] = count
        summary["total"] += count

    # Count overdue
    now = datetime.now().strftime(DATE_FORMAT)
    cursor.execute("""
        SELECT COUNT(*) FROM deliverables
        WHERE client_id=? AND deadline < ? AND status NOT IN ('delivered', 'approved')
    """, (client_id, now))
    summary["overdue"] = cursor.fetchone()[0]

    conn.close()
    return summary


def get_overdue_deliverables(limit: int = 100) -> List[Dict[str, Any]]:
    """Get all overdue deliverables across all clients"""
    conn = _get_conn()
    cursor = conn.cursor()

    now = datetime.now().strftime(DATE_FORMAT)
    cursor.execute("""
        SELECT d.*, c.name as client_name
        FROM deliverables d
        JOIN clients c ON d.client_id = c.id
        WHERE d.deadline < ? AND d.status NOT IN ('delivered', 'approved')
        ORDER BY d.deadline ASC LIMIT ?
    """, (now, limit))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_workload_summary() -> Dict[str, Any]:
    """Get workload summary across all clients"""
    conn = _get_conn()
    cursor = conn.cursor()

    summary = {
        "total_deliverables": 0,
        "by_status": {},
        "by_priority": {},
        "by_type": {},
        "overdue": 0,
        "clients_active": 0,
    }

    # Total and by status
    cursor.execute("SELECT COUNT(*) FROM deliverables")
    summary["total_deliverables"] = cursor.fetchone()[0]

    for status in STATUSES:
        cursor.execute("SELECT COUNT(*) FROM deliverables WHERE status=?", (status,))
        summary["by_status"][status] = cursor.fetchone()[0]

    # By priority
    cursor.execute("""
        SELECT priority, COUNT(*) as count
        FROM deliverables
        WHERE status NOT IN ('delivered', 'approved')
        GROUP BY priority
    """)
    for row in cursor.fetchall():
        summary["by_priority"][row[0]] = row[1]

    # By type
    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM deliverables
        GROUP BY type
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        summary["by_type"][row[0]] = row[1]

    # Overdue count
    now = datetime.now().strftime(DATE_FORMAT)
    cursor.execute("""
        SELECT COUNT(*) FROM deliverables
        WHERE deadline < ? AND status NOT IN ('delivered', 'approved')
    """, (now,))
    summary["overdue"] = cursor.fetchone()[0]

    # Active clients
    cursor.execute("SELECT COUNT(*) FROM clients WHERE status='active'")
    summary["clients_active"] = cursor.fetchone()[0]

    conn.close()
    return summary


def generate_status_email(client_id: int) -> str:
    """Generate a professional status update email for a client"""
    client = get_client(client_id)
    if not client:
        return ""

    summary = get_client_summary(client_id)

    # Get deliverables by status
    open_items = list_deliverables(client_id=client_id, status="in_progress")
    delivered = list_deliverables(client_id=client_id, status="delivered")
    overdue = list_deliverables(client_id=client_id, overdue=True)

    email = f"""Subject: {client['name']} - Deliverable Status Update

Dear {client.get('contact_name', 'Client')},

Thank you for your partnership. Here is the current status of your deliverables:

OPEN DELIVERABLES:
{len(open_items)} items in progress
"""

    if open_items:
        for d in open_items:
            deadline = d['deadline'] or "No deadline set"
            email += f"\n  - {d['title']} (Type: {d['type']}, Deadline: {deadline})"
    else:
        email += "\n  None"

    email += f"\n\nRECENTLY DELIVERED:\n{len(delivered)} items delivered"

    if delivered:
        for d in delivered[:5]:  # Show last 5
            email += f"\n  - {d['title']}"
    else:
        email += "\n  None"

    if overdue:
        email += f"\n\nOVERDUE ITEMS:\n{len(overdue)} items overdue\n"
        for d in overdue:
            email += f"\n  - {d['title']} (was due {d['deadline']})"

    email += """

If you have any questions about these items, please don't hesitate to reach out.

Best regards,

---
Nex Deliverables by Nex AI | nex-ai.be
"""

    return email


def export_deliverables(format: str = "csv", client_id: Optional[int] = None) -> str:
    """Export deliverables to CSV or JSON format"""
    deliverables = list_deliverables(client_id=client_id, limit=10000)

    if format == "csv":
        import csv
        from io import StringIO

        output = StringIO()
        if deliverables:
            fieldnames = list(deliverables[0].keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(deliverables)

        return output.getvalue()

    elif format == "json":
        import json
        return json.dumps(deliverables, indent=2, default=str)

    return ""


def get_status_history(deliverable_id: int) -> List[Dict[str, Any]]:
    """Get status change history for a deliverable"""
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM status_updates
        WHERE deliverable_id=?
        ORDER BY created_at DESC
    """, (deliverable_id,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_milestone(deliverable_id: int, title: str) -> int:
    """Add a milestone to a deliverable"""
    conn = _get_conn()
    cursor = conn.cursor()
    now = datetime.now().strftime(DATETIME_FORMAT)

    cursor.execute("""
        INSERT INTO milestones (deliverable_id, title, created_at)
        VALUES (?, ?, ?)
    """, (deliverable_id, title, now))

    conn.commit()
    milestone_id = cursor.lastrowid
    conn.close()
    return milestone_id


def complete_milestone(milestone_id: int) -> bool:
    """Mark a milestone as complete"""
    conn = _get_conn()
    cursor = conn.cursor()
    now = datetime.now().strftime(DATETIME_FORMAT)

    cursor.execute("""
        UPDATE milestones
        SET completed=1, completed_at=?
        WHERE id=?
    """, (now, milestone_id))

    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success


def get_milestones(deliverable_id: int) -> List[Dict[str, Any]]:
    """Get milestones for a deliverable"""
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM milestones
        WHERE deliverable_id=?
        ORDER BY created_at ASC
    """, (deliverable_id,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
