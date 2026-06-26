#!/usr/bin/env python3
"""
KB Full Audit – Vollständiger KB-Integritätscheck

Laufzeit: Sonntag 03:00 Uhr (via Cron)
Zweck: Gründliche Prüfung von DB und Library
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime
import csv
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from kb.framework.paths import get_default_db_path
    DB_PATH = str(get_default_db_path())
except ImportError:
    from kb.base.config import KBConfig
    DB_PATH = str(KBConfig.get_instance().db_path)

# Konfiguration - use KBConfig for portable paths
try:
    from kb.base.config import KBConfig
    _cfg = KBConfig.get_instance()
    LIBRARY_PATH = _cfg.library_path
    OUTPUT_DIR = _cfg.library_path / "audit"
except ImportError:
    from kb.framework.paths import get_default_library_path
    LIBRARY_PATH = get_default_library_path()
    OUTPUT_DIR = LIBRARY_PATH / "audit"
OUTPUT_ORPHANED = OUTPUT_DIR / "orphaned_entries.csv"
OUTPUT_PATHS = OUTPUT_DIR / "path_check.csv"
OUTPUT_REPORT = OUTPUT_DIR / "audit_report.md"
LOG_FILE = OUTPUT_DIR / "audit_log.md"

def log(message: str):
    """Loggt eine Nachricht"""
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}")

def init_output_dir():
    """Erstellt Output-Verzeichnis wenn nötig"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def check_db_integrity() -> dict:
    """Prüft DB-Integrität"""
    results = {
        'tables': [],
        'indexes': [],
        'foreign_keys': [],
        'issues': []
    }
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Tables prüfen
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    results['tables'] = [t[0] for t in tables]
    
    # Indizes prüfen
    indexes = conn.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL").fetchall()
    results['indexes'] = [f"{i[0]} on {i[1]}" for i in indexes]
    
    # PRAGMA foreign_keys prüfen
    fk_on = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    if not fk_on:
        results['issues'].append("WARN: Foreign Keys sind deaktiviert")
    
    conn.close()
    return results

def check_library_paths() -> list[dict]:
    """Prüft ob alle in KB referenzierten Pfade noch existieren"""
    issues = []
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Dateien mit Pfaden holen
    files = conn.execute("SELECT id, file_path, file_name FROM files WHERE file_path IS NOT NULL").fetchall()
    
    for file_id, file_path, original_name in files:
        if not Path(file_path).exists():
            issues.append({
                'id': file_id,
                'path': file_path,
                'name': original_name,
                'issue': 'FILE_NOT_FOUND'
            })
    
    conn.close()
    return issues

def find_orphaned_entries() -> list[dict]:
    """Findet KB-Einträge ohne zugehörige Datei"""
    orphaned = []
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Section-Einträge ohne file_id Referenz
    orphan_sections = conn.execute("""
        SELECT s.id, s.section_header, f.file_path
        FROM file_sections s
        LEFT JOIN files f ON s.file_id = f.id
        WHERE f.id IS NULL AND s.file_id IS NOT NULL
    """).fetchall()
    
    for section_id, header, path in orphan_sections:
        orphaned.append({
            'type': 'section',
            'id': section_id,
            'header': header[:50] if header else 'N/A',
            'path': path or 'N/A'
        })
    
    conn.close()
    return orphaned

def save_orphaned(orphaned: list[dict]):
    """Speichert verwaiste Einträge als CSV"""
    if not orphaned:
        log("Keine verwaisten Einträge gefunden")
        return
    
    with open(OUTPUT_ORPHANED, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['type', 'id', 'header', 'path'])
        writer.writeheader()
        writer.writerows(orphaned)
    log(f"Verwaiste Einträge: {len(orphaned)}")

def save_path_issues(issues: list[dict]):
    """Speichert Pfad-Probleme als CSV"""
    if not issues:
        log("Keine Pfad-Probleme gefunden")
        return
    
    with open(OUTPUT_PATHS, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'path', 'name', 'issue'])
        writer.writeheader()
        writer.writerows(issues)
    log(f"Pfad-Probleme: {len(issues)}")

def generate_report(db_info: dict, path_issues: list, orphaned: list) -> str:
    """Generiert Audit-Report für MC"""
    report = f"""# KB Audit Report

**Datum:** {datetime.now():%Y-%m-%d}  
**Uhrzeit:** {datetime.now():%H:%M:%S}

## Zusammenfassung

| Check | Ergebnis |
|-------|----------|
| DB-Integrität | {'✅ OK' if not db_info['issues'] else '⚠️ ' + str(len(db_info['issues']))} |
| Pfad-Check | {'✅ OK' if not path_issues else f'⚠️ {len(path_issues)} Probleme'} |
| Verwaiste Einträge | {'✅ OK' if not orphaned else f'⚠️ {len(orphaned)}'} |

## DB-Status

- Tabellen: {len(db_info['tables'])}
- Indizes: {len(db_info['indexes'])}
- Foreign Keys: {'Aktiv' if not db_info['issues'] else 'Inaktiv'}

### Issues
"""
    for issue in db_info['issues']:
        report += f"- {issue}\n"
    
    if path_issues:
        report += f"\n### Pfad-Probleme ({len(path_issues)})\n"
        for issue in path_issues[:10]:  # Max 10 anzeigen
            report += f"- `{issue['path']}`: {issue['issue']}\n"
        if len(path_issues) > 10:
            report += f"- ... und {len(path_issues) - 10} weitere (siehe {OUTPUT_PATHS})\n"
    
    if orphaned:
        report += f"\n### Verwaiste Einträge ({len(orphaned)})\n"
        for entry in orphaned[:10]:
            report += f"- [{entry['type']}] {entry['header']} ({entry['id']})\n"
        if len(orphaned) > 10:
            report += f"- ... und {len(orphaned) - 10} weitere (siehe {OUTPUT_ORPHANED})\n"
    
    report += f"\n---\n*Automatisch generiert am {datetime.now():%Y-%m-%d %H:%M:%S}*\n"
    return report

def save_report(report: str):
    """Speichert Report"""
    with open(OUTPUT_REPORT, 'w') as f:
        f.write(report)
    log(f"Report gespeichert: {OUTPUT_REPORT}")

def update_log(path_count: int, orphan_count: int):
    """Aktualisiert das Audit-Log"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n## {datetime.now():%Y-%m-%d} (Full Audit)\n")
        f.write(f"- Pfad-Probleme: {path_count}\n")
        f.write(f"- Verwaiste Einträge: {orphan_count}\n")

# Neue Funktionen (vor main() definiert)
def check_null_file_paths(conn):
    """Findet file_sections mit NULL file_path."""
    cursor = conn.execute(
        "SELECT COUNT(*) FROM file_sections WHERE file_path IS NULL OR file_path = ''"
    )
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"⚠️  {count} sections with NULL file_path")
    return count

def check_embeddings_table(conn):
    """Prüft ob embeddings Tabelle existiert und Daten hat."""
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'"
    )
    if not cursor.fetchone():
        print("❌ embeddings table missing")
        return False
    
    cursor = conn.execute("SELECT COUNT(*) FROM embeddings")
    count = cursor.fetchone()[0]
    print(f"✅ embeddings table: {count} entries")
    return True

def check_chroma_sqlite_sync(conn, chroma_path):
    """Vergleicht ChromaDB mit SQLite."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from kb.framework.chroma_integration import get_chroma
    
    try:
        chroma = get_chroma(chroma_path=chroma_path)
        chroma_count = chroma.sections_collection.count()
        
        cursor = conn.execute("SELECT COUNT(*) FROM file_sections WHERE file_path IS NOT NULL")
        sqlite_count = cursor.fetchone()[0]
        
        if chroma_count != sqlite_count:
            print(f"⚠️  Sync issue: SQLite={sqlite_count}, ChromaDB={chroma_count}")
        else:
            print(f"✅ Sync OK: {sqlite_count} entries")
        return chroma_count == sqlite_count
    except Exception as e:
        print(f"❌ ChromaDB check failed: {e}")
        return False

def main():
    log("Start: KB Full Audit")
    init_output_dir()
    
    # Connection für erweiterte Checks
    conn = sqlite3.connect(str(DB_PATH))
    
    # DB-Integrität
    log("Prüfe DB-Integrität...")
    db_info = check_db_integrity()
    log(f"  Tabellen: {len(db_info['tables'])}, Indizes: {len(db_info['indexes'])}")
    
    # Pfad-Check
    log("Prüfe Library-Pfade...")
    path_issues = check_library_paths()
    
    # Neue erweiterte Checks
    log("Prüfe NULL file_paths...")
    null_paths = check_null_file_paths(conn)
    
    log("Prüfe embeddings Tabelle...")
    check_embeddings_table(conn)
    
    log("Prüfe ChromaDB/SQLite Sync...")
    chroma_path = str(DB_PATH).replace('/library/biblio.db', '/chroma_db')
    check_chroma_sqlite_sync(conn, chroma_path)
    
    conn.close()
    
    # Verwaiste Einträge
    log("Suche verwaiste Einträge...")
    orphaned = find_orphaned_entries()
    
    # Speichern
    save_path_issues(path_issues)
    save_orphaned(orphaned)
    
    # Report
    report = generate_report(db_info, path_issues, orphaned)
    save_report(report)
    
    # Log
    update_log(len(path_issues), len(orphaned))
    
    log("Fertig: KB Full Audit")

if __name__ == "__main__":
    main()

# =============================================================================
# FK-CLEANUP (TÄGLICH IM AUDIT)
# =============================================================================

def cleanup_orphaned_fk():
    """Löscht verwaiste FK-Einträge - läuft täglich im Audit."""
    conn = _get_connection()
    
    # Orphan section_keywords (keyword_id existiert nicht)
    deleted = conn.execute("""
        DELETE FROM section_keywords
        WHERE keyword_id NOT IN (SELECT id FROM keywords)
    """).rowcount
    
    # Orphan section_keywords (section_id existiert nicht)
    deleted += conn.execute("""
        DELETE FROM section_keywords
        WHERE section_id NOT IN (SELECT id FROM file_sections)
    """).rowcount
    
    conn.commit()
    logger.info(f"FK-Cleanup: {deleted} verwaiste Einträge gelöscht")
    return deleted
