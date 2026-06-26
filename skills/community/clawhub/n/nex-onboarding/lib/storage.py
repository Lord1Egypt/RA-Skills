"""
Nex Onboarding - Storage & Database
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from .config import DB_PATH, DEFAULT_CHECKLIST, CATEGORIES


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # Templates table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            steps TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Onboardings table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS onboardings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_email TEXT,
            client_phone TEXT,
            template_id INTEGER NOT NULL,
            retainer_tier TEXT,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            status TEXT DEFAULT 'active',
            assigned_to TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (template_id) REFERENCES templates (id)
        )
    """
    )

    # Onboarding steps table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS onboarding_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            onboarding_id INTEGER NOT NULL,
            step_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            required INTEGER DEFAULT 1,
            status TEXT DEFAULT 'pending',
            completed_at TIMESTAMP,
            completed_by TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (onboarding_id) REFERENCES onboardings (id)
        )
    """
    )

    # Activity log table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS onboarding_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            onboarding_id INTEGER NOT NULL,
            step_id INTEGER,
            action TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (onboarding_id) REFERENCES onboardings (id),
            FOREIGN KEY (step_id) REFERENCES onboarding_steps (id)
        )
    """
    )

    # Create default template if it doesn't exist
    c.execute("SELECT id FROM templates WHERE name = ?", ("default",))
    if not c.fetchone():
        default_steps = json.dumps(DEFAULT_CHECKLIST)
        c.execute(
            "INSERT INTO templates (name, description, steps) VALUES (?, ?, ?)",
            ("default", "Default Nex AI onboarding checklist", default_steps),
        )

    conn.commit()
    conn.close()


def save_template(name: str, description: str, steps: List[Dict]) -> int:
    """Save a template. Returns template ID."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    steps_json = json.dumps(steps)
    c.execute(
        "INSERT OR REPLACE INTO templates (name, description, steps, updated_at) VALUES (?, ?, ?, ?)",
        (name, description, steps_json, datetime.now().isoformat()),
    )

    template_id = c.lastrowid
    conn.commit()
    conn.close()
    return template_id


def get_template(name: str) -> Optional[Dict]:
    """Get template by name."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("SELECT id, name, description, steps FROM templates WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "steps": json.loads(row[3]),
    }


def list_templates() -> List[Dict]:
    """List all templates."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("SELECT id, name, description FROM templates ORDER BY name")
    rows = c.fetchall()
    conn.close()

    return [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]


def start_onboarding(
    client_name: str,
    client_email: str = None,
    client_phone: str = None,
    template_name: str = "default",
    retainer_tier: str = None,
    assigned_to: str = None,
) -> int:
    """Start a new onboarding. Returns onboarding ID."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # Get template
    template = get_template(template_name)
    if not template:
        conn.close()
        raise ValueError(f"Template '{template_name}' not found")

    # Create onboarding
    c.execute(
        """
        INSERT INTO onboardings
        (client_name, client_email, client_phone, template_id, retainer_tier, assigned_to, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (client_name, client_email, client_phone, template["id"], retainer_tier, assigned_to, "active"),
    )

    onboarding_id = c.lastrowid

    # Create steps from template
    for step in template["steps"]:
        c.execute(
            """
            INSERT INTO onboarding_steps
            (onboarding_id, step_number, title, description, category, required, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                onboarding_id,
                step["step"],
                step["title"],
                step["description"],
                step["category"],
                1 if step["required"] else 0,
                "pending",
            ),
        )

    # Log action
    c.execute(
        "INSERT INTO onboarding_log (onboarding_id, action, message) VALUES (?, ?, ?)",
        (onboarding_id, "create", f"Onboarding started for {client_name}"),
    )

    conn.commit()
    conn.close()
    return onboarding_id


def get_onboarding(onboarding_id: int) -> Optional[Dict]:
    """Get onboarding with all steps."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute(
        """
        SELECT id, client_name, client_email, client_phone, template_id, retainer_tier,
               started_at, completed_at, status, assigned_to, notes
        FROM onboardings WHERE id = ?
        """,
        (onboarding_id,),
    )

    row = c.fetchone()
    if not row:
        conn.close()
        return None

    onboarding = {
        "id": row[0],
        "client_name": row[1],
        "client_email": row[2],
        "client_phone": row[3],
        "template_id": row[4],
        "retainer_tier": row[5],
        "started_at": row[6],
        "completed_at": row[7],
        "status": row[8],
        "assigned_to": row[9],
        "notes": row[10],
    }

    # Get steps
    c.execute(
        """
        SELECT id, step_number, title, description, category, required, status, completed_at, completed_by, notes
        FROM onboarding_steps WHERE onboarding_id = ? ORDER BY step_number
        """,
        (onboarding_id,),
    )

    steps = []
    for step_row in c.fetchall():
        steps.append(
            {
                "id": step_row[0],
                "step_number": step_row[1],
                "title": step_row[2],
                "description": step_row[3],
                "category": step_row[4],
                "required": bool(step_row[5]),
                "status": step_row[6],
                "completed_at": step_row[7],
                "completed_by": step_row[8],
                "notes": step_row[9],
            }
        )

    onboarding["steps"] = steps
    conn.close()
    return onboarding


def list_onboardings(status: Optional[str] = None, retainer_tier: Optional[str] = None) -> List[Dict]:
    """List onboardings with optional filtering."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    query = "SELECT id, client_name, retainer_tier, status, started_at FROM onboardings WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if retainer_tier:
        query += " AND retainer_tier = ?"
        params.append(retainer_tier)

    query += " ORDER BY started_at DESC"

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    return [
        {"id": row[0], "client_name": row[1], "retainer_tier": row[2], "status": row[3], "started_at": row[4]}
        for row in rows
    ]


def complete_step(onboarding_id: int, step_number: int, notes: str = None, completed_by: str = None) -> bool:
    """Mark a step as completed."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute(
        """
        UPDATE onboarding_steps
        SET status = ?, completed_at = ?, completed_by = ?, notes = ?
        WHERE onboarding_id = ? AND step_number = ?
        """,
        ("completed", datetime.now().isoformat(), completed_by, notes, onboarding_id, step_number),
    )

    affected = c.rowcount

    # Log action
    if affected > 0:
        c.execute(
            "SELECT id FROM onboarding_steps WHERE onboarding_id = ? AND step_number = ?",
            (onboarding_id, step_number),
        )
        step_id = c.fetchone()[0]

        c.execute(
            "INSERT INTO onboarding_log (onboarding_id, step_id, action, message) VALUES (?, ?, ?, ?)",
            (onboarding_id, step_id, "complete", f"Step {step_number} completed"),
        )

    conn.commit()
    conn.close()
    return affected > 0


def skip_step(onboarding_id: int, step_number: int, reason: str = None) -> bool:
    """Mark a step as skipped."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute(
        """
        UPDATE onboarding_steps
        SET status = ?, notes = ?
        WHERE onboarding_id = ? AND step_number = ?
        """,
        ("skipped", reason, onboarding_id, step_number),
    )

    affected = c.rowcount

    # Log action
    if affected > 0:
        c.execute(
            "SELECT id FROM onboarding_steps WHERE onboarding_id = ? AND step_number = ?",
            (onboarding_id, step_number),
        )
        step_id = c.fetchone()[0]

        c.execute(
            "INSERT INTO onboarding_log (onboarding_id, step_id, action, message) VALUES (?, ?, ?, ?)",
            (onboarding_id, step_id, "skip", f"Step {step_number} skipped: {reason}"),
        )

    conn.commit()
    conn.close()
    return affected > 0


def block_step(onboarding_id: int, step_number: int, reason: str = None) -> bool:
    """Mark a step as blocked."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute(
        """
        UPDATE onboarding_steps
        SET status = ?, notes = ?
        WHERE onboarding_id = ? AND step_number = ?
        """,
        ("blocked", reason, onboarding_id, step_number),
    )

    affected = c.rowcount

    # Log action
    if affected > 0:
        c.execute(
            "SELECT id FROM onboarding_steps WHERE onboarding_id = ? AND step_number = ?",
            (onboarding_id, step_number),
        )
        step_id = c.fetchone()[0]

        c.execute(
            "INSERT INTO onboarding_log (onboarding_id, step_id, action, message) VALUES (?, ?, ?, ?)",
            (onboarding_id, step_id, "block", f"Step {step_number} blocked: {reason}"),
        )

    conn.commit()
    conn.close()
    return affected > 0


def get_onboarding_progress(onboarding_id: int) -> Dict:
    """Get progress stats for an onboarding."""
    onboarding = get_onboarding(onboarding_id)
    if not onboarding:
        return {}

    steps = onboarding["steps"]
    total = len(steps)
    completed = len([s for s in steps if s["status"] == "completed"])
    required_total = len([s for s in steps if s["required"]])
    required_completed = len([s for s in steps if s["required"] and s["status"] == "completed"])
    blocked = [s for s in steps if s["status"] == "blocked"]
    pending = [s for s in steps if s["status"] == "pending"]

    percentage = int((completed / total * 100) if total > 0 else 0)

    return {
        "onboarding_id": onboarding_id,
        "client_name": onboarding["client_name"],
        "status": onboarding["status"],
        "percentage": percentage,
        "completed": completed,
        "total": total,
        "required_completed": required_completed,
        "required_total": required_total,
        "blocked_count": len(blocked),
        "pending_count": len(pending),
        "blocked": blocked,
        "pending": pending,
    }


def get_next_step(onboarding_id: int) -> Optional[Dict]:
    """Get the next pending step."""
    onboarding = get_onboarding(onboarding_id)
    if not onboarding:
        return None

    for step in onboarding["steps"]:
        if step["status"] == "pending":
            return step

    return None


def complete_onboarding(onboarding_id: int) -> bool:
    """Mark entire onboarding as completed."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute(
        "UPDATE onboardings SET status = ?, completed_at = ? WHERE id = ?",
        ("completed", datetime.now().isoformat(), onboarding_id),
    )

    affected = c.rowcount

    if affected > 0:
        c.execute(
            "INSERT INTO onboarding_log (onboarding_id, action, message) VALUES (?, ?, ?)",
            (onboarding_id, "complete", "Onboarding completed"),
        )

    conn.commit()
    conn.close()
    return affected > 0


def pause_onboarding(onboarding_id: int) -> bool:
    """Pause an onboarding."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("UPDATE onboardings SET status = ? WHERE id = ?", ("paused", onboarding_id))

    affected = c.rowcount

    if affected > 0:
        c.execute(
            "INSERT INTO onboarding_log (onboarding_id, action, message) VALUES (?, ?, ?)",
            (onboarding_id, "pause", "Onboarding paused"),
        )

    conn.commit()
    conn.close()
    return affected > 0


def get_onboarding_stats() -> Dict:
    """Get overall statistics."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # Total counts
    c.execute("SELECT COUNT(*) FROM onboardings")
    total_onboardings = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM onboardings WHERE status = 'completed'")
    completed_onboardings = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM onboardings WHERE status = 'active'")
    active_onboardings = c.fetchone()[0]

    # Steps stats
    c.execute("SELECT COUNT(*) FROM onboarding_steps")
    total_steps = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM onboarding_steps WHERE status = 'completed'")
    completed_steps = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM onboarding_steps WHERE status = 'blocked'")
    blocked_steps = c.fetchone()[0]

    # Find bottlenecks (most blocked steps)
    c.execute(
        """
        SELECT step_number, title, COUNT(*) as blocked_count
        FROM onboarding_steps WHERE status = 'blocked'
        GROUP BY step_number, title
        ORDER BY blocked_count DESC LIMIT 5
        """
    )
    bottlenecks = [{"step": row[0], "title": row[1], "blocked_count": row[2]} for row in c.fetchall()]

    conn.close()

    return {
        "total_onboardings": total_onboardings,
        "completed_onboardings": completed_onboardings,
        "active_onboardings": active_onboardings,
        "completion_rate": int(
            (completed_onboardings / total_onboardings * 100) if total_onboardings > 0 else 0
        ),
        "total_steps": total_steps,
        "completed_steps": completed_steps,
        "blocked_steps": blocked_steps,
        "step_completion_rate": int((completed_steps / total_steps * 100) if total_steps > 0 else 0),
        "bottlenecks": bottlenecks,
    }


def export_onboarding(onboarding_id: int, format: str = "json") -> str:
    """Export onboarding as JSON or CSV."""
    onboarding = get_onboarding(onboarding_id)
    if not onboarding:
        return ""

    if format == "json":
        return json.dumps(onboarding, indent=2, default=str)

    elif format == "csv":
        lines = []
        lines.append(
            f"Client,Status,Progress,Started,Completed,Assigned To,Retainer Tier"
        )
        lines.append(
            f"{onboarding['client_name']},{onboarding['status']},"
            f"{len([s for s in onboarding['steps'] if s['status'] == 'completed'])}/{len(onboarding['steps'])},"
            f"{onboarding['started_at']},{onboarding['completed_at']},{onboarding['assigned_to']},"
            f"{onboarding['retainer_tier']}"
        )
        lines.append("")
        lines.append("Step,Title,Category,Required,Status,Notes,Completed At")

        for step in onboarding["steps"]:
            lines.append(
                f"{step['step_number']},{step['title']},{step['category']},"
                f"{step['required']},{step['status']},{step['notes']},{step['completed_at']}"
            )

        return "\n".join(lines)

    return ""
