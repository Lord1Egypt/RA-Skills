import argparse
import json
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path


def runtime_dir(base_dir):
    path = Path(base_dir) / ".runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path(base_dir):
    return runtime_dir(base_dir) / "job-tracker.db"


def get_connection(base_dir):
    connection = sqlite3.connect(db_path(base_dir))
    connection.row_factory = sqlite3.Row
    ensure_schema(connection)
    return connection


def ensure_schema(connection):
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            applied_on TEXT,
            deadline TEXT,
            next_follow_up TEXT,
            priority TEXT,
            source TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            linkedin TEXT,
            role TEXT,
            notes TEXT,
            FOREIGN KEY(application_id) REFERENCES applications(id)
        );
        CREATE TABLE IF NOT EXISTS follow_ups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            due_on TEXT NOT NULL,
            channel TEXT DEFAULT 'unknown',
            status TEXT DEFAULT 'pending',
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(application_id) REFERENCES applications(id)
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(application_id) REFERENCES applications(id)
        );
        """
    )
    connection.commit()


def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def add_application(args):
    timestamp = now_iso()
    with get_connection(args.base_dir) as connection:
        cursor = connection.execute(
            """
            INSERT INTO applications
                (company, role, status, applied_on, deadline, next_follow_up, priority, source, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                args.company,
                args.role,
                args.status,
                args.applied_on,
                args.deadline,
                args.next_follow_up,
                args.priority,
                args.source,
                args.notes,
                timestamp,
                timestamp,
            ),
        )
        application_id = cursor.lastrowid
        if args.contact_name:
            connection.execute(
                """
                INSERT INTO contacts (application_id, name, email, linkedin, role, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    application_id,
                    args.contact_name,
                    args.contact_email,
                    args.contact_linkedin,
                    args.contact_role,
                    args.contact_notes,
                ),
            )
        if args.next_follow_up:
            connection.execute(
                """
                INSERT INTO follow_ups (application_id, due_on, channel, status, note, created_at)
                VALUES (?, ?, ?, 'pending', ?, ?)
                """,
                (application_id, args.next_follow_up, args.follow_up_channel, args.notes, timestamp),
            )
        if args.notes:
            connection.execute(
                "INSERT INTO notes (application_id, note, created_at) VALUES (?, ?, ?)",
                (application_id, args.notes, timestamp),
            )
        connection.commit()
        row = connection.execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()
        print(json.dumps({"application": row_to_dict(row)}, indent=2))


def update_application(args):
    updates = []
    values = []
    for field in ["status", "deadline", "next_follow_up", "priority", "source"]:
        value = getattr(args, field)
        if value is not None:
            updates.append(f"{field} = ?")
            values.append(value)
    if args.note is not None:
        updates.append("notes = ?")
        values.append(args.note)
    updates.append("updated_at = ?")
    values.append(now_iso())
    values.append(args.id)

    with get_connection(args.base_dir) as connection:
        connection.execute(
            f"UPDATE applications SET {', '.join(updates)} WHERE id = ?",
            values,
        )
        if args.note:
            connection.execute(
                "INSERT INTO notes (application_id, note, created_at) VALUES (?, ?, ?)",
                (args.id, args.note, now_iso()),
            )
        if args.next_follow_up:
            connection.execute(
                """
                INSERT INTO follow_ups (application_id, due_on, channel, status, note, created_at)
                VALUES (?, ?, ?, 'pending', ?, ?)
                """,
                (args.id, args.next_follow_up, args.follow_up_channel, args.note, now_iso()),
            )
        connection.commit()
        row = connection.execute("SELECT * FROM applications WHERE id = ?", (args.id,)).fetchone()
        print(json.dumps({"application": row_to_dict(row)}, indent=2))


def list_applications(args):
    query = "SELECT * FROM applications"
    values = []
    clauses = []
    if args.status:
        clauses.append("status = ?")
        values.append(args.status)
    if args.priority:
        clauses.append("priority = ?")
        values.append(args.priority)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY COALESCE(next_follow_up, deadline, applied_on, created_at) ASC LIMIT ?"
    values.append(args.limit)
    with get_connection(args.base_dir) as connection:
        rows = connection.execute(query, values).fetchall()
        print(json.dumps({"applications": [row_to_dict(row) for row in rows]}, indent=2))


def due_applications(args):
    start = date.fromisoformat(args.on) if args.on else date.today()
    end = start + timedelta(days=args.window)
    with get_connection(args.base_dir) as connection:
        rows = connection.execute(
            """
            SELECT id, company, role, status, next_follow_up, deadline
            FROM applications
            WHERE next_follow_up IS NOT NULL
              AND next_follow_up >= ?
              AND next_follow_up <= ?
            ORDER BY next_follow_up ASC
            """,
            (start.isoformat(), end.isoformat()),
        ).fetchall()
        print(
            json.dumps(
                {
                    "window": {"start": start.isoformat(), "end": end.isoformat()},
                    "applications": [row_to_dict(row) for row in rows],
                },
                indent=2,
            )
        )


def summary(args):
    with get_connection(args.base_dir) as connection:
        by_status = connection.execute(
            "SELECT status, COUNT(*) AS total FROM applications GROUP BY status ORDER BY total DESC, status ASC"
        ).fetchall()
        due_next_week = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM applications
            WHERE next_follow_up IS NOT NULL
              AND next_follow_up <= ?
            """,
            ((date.today() + timedelta(days=7)).isoformat(),),
        ).fetchone()
        total = connection.execute("SELECT COUNT(*) AS total FROM applications").fetchone()
        print(
            json.dumps(
                {
                    "totalApplications": total["total"],
                    "followUpsDueWithin7Days": due_next_week["total"],
                    "byStatus": [row_to_dict(row) for row in by_status],
                },
                indent=2,
            )
        )


def build_parser():
    parser = argparse.ArgumentParser(description="Track job applications in SQLite.")
    parser.add_argument("--base-dir", default=Path(__file__).resolve().parents[1], help="Skill directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--status", default="applied")
    add_parser.add_argument("--applied-on")
    add_parser.add_argument("--deadline")
    add_parser.add_argument("--next-follow-up")
    add_parser.add_argument("--follow-up-channel", default="email")
    add_parser.add_argument("--priority", default="medium")
    add_parser.add_argument("--source", default="unknown")
    add_parser.add_argument("--notes")
    add_parser.add_argument("--contact-name")
    add_parser.add_argument("--contact-email")
    add_parser.add_argument("--contact-linkedin")
    add_parser.add_argument("--contact-role")
    add_parser.add_argument("--contact-notes")
    add_parser.set_defaults(handler=add_application)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True, type=int)
    update_parser.add_argument("--status")
    update_parser.add_argument("--deadline")
    update_parser.add_argument("--next-follow-up")
    update_parser.add_argument("--follow-up-channel", default="email")
    update_parser.add_argument("--priority")
    update_parser.add_argument("--source")
    update_parser.add_argument("--note")
    update_parser.set_defaults(handler=update_application)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status")
    list_parser.add_argument("--priority")
    list_parser.add_argument("--limit", type=int, default=50)
    list_parser.set_defaults(handler=list_applications)

    due_parser = subparsers.add_parser("due")
    due_parser.add_argument("--on")
    due_parser.add_argument("--window", type=int, default=7)
    due_parser.set_defaults(handler=due_applications)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.set_defaults(handler=summary)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
