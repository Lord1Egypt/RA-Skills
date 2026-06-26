#!/usr/bin/env python3
"""
Session Healer for OpenClaw

Automatically detects and heals locked OpenClaw session files.

Usage:
    python healer.py check [--verbose]
    python healer.py heal [--force] [--dry-run]
    python healer.py unlock <session-id>
    python healer.py recover <session-id>
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LockInfo:
    """Information about a session lock."""
    
    lock_path: Path
    session_path: Path
    session_id: str
    pid: int
    is_alive: bool
    age_seconds: float
    agent_name: str


class SessionHealer:
    """Detects and heals locked OpenClaw sessions."""
    
    def __init__(self, openclaw_dir: Optional[str] = None):
        if openclaw_dir:
            self.openclaw_dir = Path(openclaw_dir)
        else:
            self.openclaw_dir = Path.home() / ".openclaw"
        
        self.agents_dir = self.openclaw_dir / "agents"
        self.logs = []
    
    def find_locks(self) -> List[LockInfo]:
        """Find all session lock files."""
        
        locks = []
        
        if not self.agents_dir.exists():
            return locks
        
        for agent_dir in self.agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            
            sessions_dir = agent_dir / "sessions"
            if not sessions_dir.exists():
                continue
            
            for lock_file in sessions_dir.glob("*.jsonl.lock"):
                lock_info = self._parse_lock(lock_file, agent_dir.name)
                if lock_info:
                    locks.append(lock_info)
        
        return locks
    
    def _parse_lock(self, lock_path: Path, agent_name: str) -> Optional[LockInfo]:
        """Parse a lock file and extract info."""
        
        try:
            # Get session ID from filename
            session_id = lock_path.stem.replace(".jsonl", "")
            
            # Get session file path
            session_path = lock_path.with_suffix("")  # Remove .lock
            
            # Read PID from lock file
            content = lock_path.read_text().strip()
            pid = None
            
            # Lock file might contain PID or just be empty
            # Try to extract PID from content or mtime
            if content:
                try:
                    data = json.loads(content)
                    pid = data.get("pid")
                except json.JSONDecodeError:
                    # Try parsing as plain number
                    try:
                        pid = int(content.split()[0])
                    except (ValueError, IndexError):
                        pass
            
            # If no PID in file, try to get from filename pattern or stat
            if pid is None:
                # Use stat to get creation time
                stat = lock_path.stat()
                mtime = stat.st_mtime
                age_seconds = time.time() - mtime
                
                # Create lock info without PID
                return LockInfo(
                    lock_path=lock_path,
                    session_path=session_path,
                    session_id=session_id,
                    pid=0,
                    is_alive=False,  # Assume stale if we can't find PID
                    age_seconds=age_seconds,
                    agent_name=agent_name
                )
            
            # Check if process is alive
            is_alive = self._is_process_alive(pid)
            
            # Get lock age
            stat = lock_path.stat()
            age_seconds = time.time() - stat.st_mtime
            
            return LockInfo(
                lock_path=lock_path,
                session_path=session_path,
                session_id=session_id,
                pid=pid,
                is_alive=is_alive,
                age_seconds=age_seconds,
                agent_name=agent_name
            )
        
        except Exception as e:
            self.logs.append(f"Error parsing lock {lock_path}: {e}")
            return None
    
    def _is_process_alive(self, pid: int) -> bool:
        """Check if a process is still running."""
        
        if pid <= 0:
            return False
        
        try:
            # Send signal 0 to check if process exists
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    
    def check(self, verbose: bool = False) -> List[LockInfo]:
        """Check for locked sessions and print status."""
        
        locks = self.find_locks()
        
        if not locks:
            print("No locked sessions found.")
            return locks
        
        print(f"Found {len(locks)} lock file(s):\n")
        
        for lock in locks:
            status = "ACTIVE" if lock.is_alive else "STALE"
            status_icon = "✓" if lock.is_alive else "✗"
            age_str = self._format_age(lock.age_seconds)
            
            print(f"  {status_icon} session: {lock.session_id}")
            
            if verbose:
                print(f"    Lock: {lock.lock_path}")
                print(f"    PID: {lock.pid} ({'ALIVE' if lock.is_alive else 'DEAD'})")
                print(f"    Agent: {lock.agent_name}")
                print(f"    Age: {age_str}")
            
            print(f"    Status: {status}")
            
            if verbose:
                print()
        
        return locks
    
    def heal(self, force: bool = False, dry_run: bool = False) -> Tuple[int, int]:
        """Clear stale locks. Returns (cleared, skipped)."""
        
        locks = self.find_locks()
        
        if not locks:
            print("No locked sessions found.")
            return 0, 0
        
        cleared = 0
        skipped = 0
        
        print(f"Processing {len(locks)} lock(s)...\n")
        
        for lock in locks:
            if lock.is_alive and not force:
                print(f"[SKIPPED] {lock.session_id} (PID {lock.pid} still alive)")
                skipped += 1
                continue
            
            if dry_run:
                print(f"[DRY-RUN] Would clear: {lock.session_id}")
                cleared += 1
                continue
            
            try:
                # Remove lock file
                lock.lock_path.unlink()
                print(f"[CLEARED] {lock.session_id} (PID {lock.pid} was {'dead' if not lock.is_alive else 'forced'})")
                cleared += 1
                
                # Log the action
                self._log_heal(lock)
                
            except Exception as e:
                print(f"[ERROR] Failed to clear {lock.session_id}: {e}")
                skipped += 1
        
        print(f"\nHealed {cleared} session(s). {skipped} skipped.")
        return cleared, skipped
    
    def unlock(self, session_id: str, dry_run: bool = False) -> bool:
        """Unlock a specific session by ID."""
        
        locks = self.find_locks()
        
        for lock in locks:
            if lock.session_id == session_id or lock.session_id.startswith(session_id):
                if dry_run:
                    print(f"[DRY-RUN] Would clear: {lock.lock_path}")
                    return True
                
                try:
                    lock.lock_path.unlink()
                    print(f"[CLEARED] {lock.session_id}")
                    self._log_heal(lock)
                    return True
                except Exception as e:
                    print(f"[ERROR] Failed to clear: {e}")
                    return False
        
        print(f"[NOT FOUND] No lock found for session: {session_id}")
        return False
    
    def recover(self, session_id: str, dry_run: bool = False) -> bool:
        """Attempt to recover a corrupted session file."""
        
        locks = self.find_locks()
        session_path = None
        
        for lock in locks:
            if lock.session_id == session_id or lock.session_id.startswith(session_id):
                session_path = lock.session_path
                break
        
        if not session_path:
            # Try to find session without lock
            for agent_dir in self.agents_dir.iterdir():
                if not agent_dir.is_dir():
                    continue
                sessions_dir = agent_dir / "sessions"
                if not sessions_dir.exists():
                    continue
                
                for session_file in sessions_dir.glob("*.jsonl"):
                    if session_id in session_file.name:
                        session_path = session_file
                        break
                
                if session_path:
                    break
        
        if not session_path:
            print(f"[NOT FOUND] No session file found for: {session_id}")
            return False
        
        if not session_path.exists():
            print(f"[NOT FOUND] Session file does not exist: {session_path}")
            return False
        
        # Create backup
        backup_path = session_path.with_suffix(f".{int(time.time())}.bak")
        
        if dry_run:
            print(f"[DRY-RUN] Would recover: {session_path}")
            print(f"[DRY-RUN] Would create backup: {backup_path}")
            return True
        
        try:
            # Create backup
            shutil.copy2(session_path, backup_path)
            print(f"[BACKUP] Created: {backup_path}")
            
            # Read and validate lines
            valid_lines = []
            corrupted_count = 0
            
            with open(session_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        json.loads(line)
                        valid_lines.append(line)
                    except json.JSONDecodeError as e:
                        print(f"[CORRUPT] Line {i}: {str(e)[:50]}...")
                        corrupted_count += 1
            
            if corrupted_count == 0:
                print(f"[OK] Session file is valid. No recovery needed.")
                backup_path.unlink()  # Remove unnecessary backup
                return True
            
            # Write recovered file
            with open(session_path, 'w') as f:
                for line in valid_lines:
                    f.write(line + '\n')
            
            print(f"[RECOVERED] Removed {corrupted_count} corrupted lines from {session_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Recovery failed: {e}")
            return False
    
    def _format_age(self, seconds: float) -> str:
        """Format age in human-readable form."""
        
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
        else:
            days = int(seconds / 86400)
            hours = int((seconds % 86400) / 3600)
            return f"{days} day{'s' if days != 1 else ''} {hours} hour{'s' if hours != 1 else ''}"
    
    def _log_heal(self, lock: LockInfo) -> None:
        """Log a heal action."""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "heal",
            "session_id": lock.session_id,
            "pid": lock.pid,
            "lock_path": str(lock.lock_path),
            "agent": lock.agent_name,
            "was_alive": lock.is_alive
        }
        
        log_file = self.openclaw_dir / "session-healer.log"
        
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception:
            pass  # Ignore logging errors


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Heal locked OpenClaw sessions")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # check command
    check_parser = subparsers.add_parser('check', help='Check for locked sessions')
    check_parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed info')
    
    # heal command
    heal_parser = subparsers.add_parser('heal', help='Clear stale locks')
    heal_parser.add_argument('--force', '-f', action='store_true', help='Clear all locks, even for alive processes')
    heal_parser.add_argument('--dry-run', action='store_true', help='Show what would be cleared')
    
    # unlock command
    unlock_parser = subparsers.add_parser('unlock', help='Unlock a specific session')
    unlock_parser.add_argument('session_id', help='Session ID to unlock')
    unlock_parser.add_argument('--dry-run', action='store_true', help='Show what would be cleared')
    
    # recover command
    recover_parser = subparsers.add_parser('recover', help='Recover a corrupted session')
    recover_parser.add_argument('session_id', help='Session ID to recover')
    recover_parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    
    # clear-all command (convenience)
    clear_parser = subparsers.add_parser('clear-all', help='Clear all stale locks (alias for heal)')
    clear_parser.add_argument('--dry-run', action='store_true', help='Show what would be cleared')
    
    args = parser.parse_args()
    
    healer = SessionHealer()
    
    if args.command == 'check':
        healer.check(verbose=args.verbose)
    
    elif args.command == 'heal':
        healer.heal(force=args.force, dry_run=args.dry_run)
    
    elif args.command == 'unlock':
        healer.unlock(args.session_id, dry_run=args.dry_run)
    
    elif args.command == 'recover':
        healer.recover(args.session_id, dry_run=args.dry_run)
    
    elif args.command == 'clear-all':
        healer.heal(force=False, dry_run=args.dry_run)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()