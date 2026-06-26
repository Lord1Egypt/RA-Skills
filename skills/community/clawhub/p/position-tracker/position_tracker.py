"""
Position Tracker — Self-Healing State Management
=================================================
Generalized position tracking with orphan detection, phantom cleanup,
and reconciliation against external APIs.

Production-tested position tracking, domain-agnostic.

Copyright © 2026 Shadow Rose
License: MIT
"""
import json
import os
import time
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable


class ExternalAPIAdapter(ABC):
    """Abstract interface for external position APIs.
    
    Implement this to connect Position Tracker to your exchange, broker,
    cloud provider, or any external system that holds positions.
    """
    
    @abstractmethod
    def get_all_positions(self) -> List[Dict[str, Any]]:
        """Fetch all positions from external API.
        
        Returns:
            List of dicts, each with at minimum:
                - "id" (str): Unique position identifier
                - "value" (float): Position value in your currency/units
                - Any additional fields you want to track
        
        Example:
            [
                {"id": "AAPL-123", "value": 1000.0, "status": "open"},
                {"id": "GOOGL-456", "value": 2500.0, "status": "open"},
            ]
        """
        pass
    
    @abstractmethod
    def close_position(self, position_id: str) -> bool:
        """Close a position on the external system.
        
        Args:
            position_id: Unique identifier of position to close
        
        Returns:
            True if successfully closed, False otherwise
        """
        pass


class PositionState:
    """State for a single tracked position."""
    
    def __init__(self, position_id: str, data: Optional[Dict] = None):
        self.id = position_id
        d = data or {}
        
        # State machine
        self.status = d.get("status", "WATCHING")  # WATCHING, IN, EXITED, SKIPPED
        self.first_seen = d.get("first_seen", datetime.now(timezone.utc).isoformat())
        
        # Value tracking
        self.entry_value = d.get("entry_value")
        self.current_value = d.get("current_value", 0.0)
        self.peak_value = d.get("peak_value", 0.0)
        
        # Timestamps
        self.entry_time = d.get("entry_time")
        self.exit_time = d.get("exit_time")
        self.skip_time = d.get("skip_time")
        
        # Metadata (user-defined)
        self.metadata = d.get("metadata", {})
        
        # Orphan cleanup flag (persisted to survive restarts)
        self._orphan_cleanup = d.get("_orphan_cleanup", False)
        
        # Action history
        self.last_action = d.get("last_action", {})
        self.action_count = d.get("action_count", 0)
    
    def to_dict(self) -> Dict:
        """Serialize to dict for persistence."""
        return {
            "id": self.id,
            "status": self.status,
            "first_seen": self.first_seen,
            "entry_value": self.entry_value,
            "current_value": self.current_value,
            "peak_value": self.peak_value,
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
            "skip_time": self.skip_time,
            "metadata": self.metadata,
            "_orphan_cleanup": self._orphan_cleanup,
            "last_action": self.last_action,
            "action_count": self.action_count,
        }


class PositionTracker:
    """Self-healing position tracker with orphan detection."""
    
    def __init__(
        self,
        api_adapter: ExternalAPIAdapter,
        state_dir: str = "./state",
        state_file: str = "positions.json",
        min_position_value: float = 5.0,
        max_positions: int = 100,
        skip_cleanup_seconds: int = 3600,
        exited_cleanup_seconds: int = 1800,
        enable_auto_reconcile: bool = False,
        reconcile_interval: int = 300,
        alert_callback: Optional[Callable] = None,
    ):
        """Initialize position tracker.
        
        Args:
            api_adapter: Implementation of ExternalAPIAdapter for your system
            state_dir: Directory for state persistence
            state_file: Filename for state (within state_dir)
            min_position_value: Dust threshold — ignore positions below this value
            max_positions: Safety cap on concurrent IN positions
            skip_cleanup_seconds: Remove SKIPPED positions after this timeout
            exited_cleanup_seconds: Remove EXITED positions after this timeout
            enable_auto_reconcile: Auto-fix orphans/phantoms during reconcile
            reconcile_interval: Seconds between auto-reconciliation (if enabled)
            alert_callback: Function(message: str) called for alerts
        """
        self.api = api_adapter
        self.state_dir = state_dir
        self.state_file = os.path.join(state_dir, state_file)
        self.min_position_value = min_position_value
        self.max_positions = max_positions
        self.skip_cleanup_seconds = skip_cleanup_seconds
        self.exited_cleanup_seconds = exited_cleanup_seconds
        self.enable_auto_reconcile = enable_auto_reconcile
        self.reconcile_interval = reconcile_interval
        self.alert_callback = alert_callback or self._default_alert
        
        # State
        self.positions: Dict[str, PositionState] = {}
        self._last_reconcile = 0
        
        # Create state directory
        os.makedirs(state_dir, exist_ok=True)
        
        # Load existing state
        self._load()
        
        self._log(f"Position Tracker initialized: {len(self.positions)} positions loaded")
    
    def _log(self, message: str):
        """Internal logging (override for custom logger)."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} [PositionTracker] {message}")
    
    def _default_alert(self, message: str):
        """Default alert handler (just logs)."""
        self._log(f"ALERT: {message}")
    
    def _load(self):
        """Load state from disk."""
        if not os.path.exists(self.state_file):
            return
        
        try:
            with open(self.state_file, "r") as f:
                data = json.load(f)
            
            for pos_id, pos_data in data.items():
                self.positions[pos_id] = PositionState(pos_id, pos_data)
            
            self._log(f"Loaded state for {len(self.positions)} positions")
        except Exception as e:
            self._log(f"Failed to load state: {e}")
            self.positions = {}
    
    def save(self):
        """Persist state to disk (atomic write with fsync)."""
        data = {pos_id: pos.to_dict() for pos_id, pos in self.positions.items()}
        tmp = self.state_file + ".tmp"
        
        try:
            with open(tmp, "w") as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self.state_file)
        except Exception as e:
            self._log(f"Failed to save state: {e}")
    
    def track(self, position_id: str, metadata: Optional[Dict] = None) -> PositionState:
        """Start tracking a new position.
        
        Args:
            position_id: Unique identifier for this position
            metadata: Optional metadata dict to store
        
        Returns:
            PositionState object for the tracked position
        """
        if position_id not in self.positions:
            pos = PositionState(position_id)
            if metadata:
                pos.metadata = metadata
            self.positions[position_id] = pos
            self._log(f"Now tracking: {position_id}")
            self.save()
        return self.positions[position_id]
    
    def get(self, position_id: str) -> Optional[PositionState]:
        """Get position state by ID.
        
        Returns:
            PositionState or None if not tracked
        """
        return self.positions.get(position_id)
    
    def update(self, position_id: str, action: str, value: float = 0.0) -> Optional[PositionState]:
        """Update position state based on action.
        
        Args:
            position_id: Position to update
            action: One of "ENTER", "EXIT", "HOLD", "MONITOR", "SKIP"
            value: Current position value
        
        Returns:
            Updated PositionState or None if position not tracked
        """
        pos = self.positions.get(position_id)
        if not pos:
            self._log(f"Warning: update called on untracked position {position_id}")
            return None
        
        now = time.time()
        pos.last_action = {"action": action, "value": value, "time": now}
        pos.action_count += 1
        pos.current_value = value
        pos.peak_value = max(pos.peak_value, value)
        
        if action == "ENTER":
            pos.status = "IN"
            pos.entry_value = value
            pos.entry_time = datetime.now(timezone.utc).isoformat()
            self._log(f"ENTER: {position_id} @ {value}")
        
        elif action == "EXIT":
            pos.status = "EXITED"
            pos.exit_time = now
            self._log(f"EXIT: {position_id} @ {value}")
        
        elif action == "HOLD":
            # Stay in current status
            pass
        
        elif action == "MONITOR":
            # Stay in WATCHING
            pass
        
        elif action == "SKIP":
            pos.status = "SKIPPED"
            pos.skip_time = now
            self._log(f"SKIP: {position_id}")
        
        self.save()
        return pos
    
    def get_in_positions(self) -> List[str]:
        """Get all position IDs currently IN."""
        return [pos_id for pos_id, pos in self.positions.items() if pos.status == "IN"]
    
    def get_active_positions(self) -> List[str]:
        """Get all positions that need monitoring (WATCHING or IN)."""
        return [pos_id for pos_id, pos in self.positions.items() 
                if pos.status in ("WATCHING", "IN")]
    
    def cleanup(self):
        """Remove stale SKIPPED and EXITED positions."""
        now = time.time()
        to_remove = []
        
        for pos_id, pos in self.positions.items():
            if pos.status == "SKIPPED" and pos.skip_time:
                if now - pos.skip_time > self.skip_cleanup_seconds:
                    to_remove.append(pos_id)
            
            elif pos.status == "EXITED" and pos.exit_time:
                if now - pos.exit_time > self.exited_cleanup_seconds:
                    to_remove.append(pos_id)
        
        for pos_id in to_remove:
            del self.positions[pos_id]
        
        if to_remove:
            self._log(f"Cleaned up {len(to_remove)} stale positions")
            self.save()
    
    def detect_orphans(self) -> List[Dict[str, Any]]:
        """Detect positions on external API that aren't in local state.
        
        Returns:
            List of orphan position dicts from API
        """
        try:
            external_positions = self.api.get_all_positions()
        except Exception as e:
            self._log(f"Failed to fetch external positions: {e}")
            return []
        
        orphans = []
        for ext_pos in external_positions:
            pos_id = ext_pos.get("id")
            value = ext_pos.get("value", 0.0)
            
            # Filter dust
            if value < self.min_position_value:
                continue
            
            # Check if tracked locally
            if pos_id not in self.positions:
                orphans.append(ext_pos)
        
        if orphans:
            self._log(f"Detected {len(orphans)} orphans: {[o['id'] for o in orphans]}")
        
        return orphans
    
    def cleanup_orphans(self, orphans: List[Dict], auto_close: bool = False) -> List[str]:
        """Handle orphaned positions.
        
        Args:
            orphans: List of orphan dicts from detect_orphans()
            auto_close: If True, close orphans via API adapter
        
        Returns:
            List of position IDs that were cleaned up
        """
        cleaned = []
        
        for orphan in orphans:
            pos_id = orphan["id"]
            value = orphan.get("value", 0.0)
            
            if auto_close:
                try:
                    success = self.api.close_position(pos_id)
                    if success:
                        self._log(f"Auto-closed orphan: {pos_id} (value={value})")
                        cleaned.append(pos_id)
                    else:
                        self._log(f"Failed to close orphan: {pos_id}")
                except Exception as e:
                    self._log(f"Error closing orphan {pos_id}: {e}")
            else:
                # Track as orphan cleanup (flag for later analysis)
                pos = self.track(pos_id, metadata={"orphan": True, "value": value})
                pos._orphan_cleanup = True
                pos.status = "IN"  # Mark as IN so it gets handled
                self._log(f"Tracked orphan for cleanup: {pos_id} (value={value})")
                cleaned.append(pos_id)
        
        if cleaned:
            self.save()
        
        return cleaned
    
    def reconcile(self) -> Dict[str, Any]:
        """Reconcile local state against external API.
        
        Returns:
            Reconciliation report dict with keys:
                - orphans: List of orphan position dicts
                - phantoms: List of phantom position IDs (local but not external)
                - corrected: List of position IDs that were auto-corrected
                - errors: List of error messages
        """
        report = {
            "orphans": [],
            "phantoms": [],
            "corrected": [],
            "errors": [],
        }
        
        # Get external positions
        try:
            external_positions = self.api.get_all_positions()
        except Exception as e:
            report["errors"].append(f"API fetch failed: {e}")
            return report
        
        # Build external ID set
        external_ids = {pos["id"] for pos in external_positions}
        
        # Detect orphans (external but not local)
        for ext_pos in external_positions:
            pos_id = ext_pos["id"]
            value = ext_pos.get("value", 0.0)
            
            if value < self.min_position_value:
                continue  # Skip dust
            
            if pos_id not in self.positions:
                report["orphans"].append(ext_pos)
        
        # Detect phantoms (local IN but not external)
        for pos_id, pos in self.positions.items():
            if pos.status == "IN" and pos_id not in external_ids:
                report["phantoms"].append(pos_id)
        
        # Auto-correct if enabled
        if self.enable_auto_reconcile:
            # Cleanup orphans
            if report["orphans"]:
                cleaned = self.cleanup_orphans(report["orphans"], auto_close=False)
                report["corrected"].extend(cleaned)
            
            # Remove phantoms
            for phantom_id in report["phantoms"]:
                pos = self.positions.get(phantom_id)
                if pos:
                    pos.status = "EXITED"
                    pos.exit_time = time.time()
                    self._log(f"Auto-corrected phantom: {phantom_id} (marked EXITED)")
                    report["corrected"].append(phantom_id)
            
            if report["corrected"]:
                self.save()
        
        # Log results
        if report["orphans"] or report["phantoms"]:
            self._log(f"Reconciliation: {len(report['orphans'])} orphans, "
                      f"{len(report['phantoms'])} phantoms, "
                      f"{len(report['corrected'])} auto-corrected")
        
        # Update reconcile timestamp
        self._last_reconcile = time.time()
        
        return report
    
    def get_stats(self) -> Dict[str, Any]:
        """Get summary statistics.
        
        Returns:
            Dict with counts by status and other metrics
        """
        by_status = {}
        for pos in self.positions.values():
            by_status[pos.status] = by_status.get(pos.status, 0) + 1
        
        return {
            "total_positions": len(self.positions),
            "by_status": by_status,
            "in_positions": len(self.get_in_positions()),
            "last_reconcile": self._last_reconcile,
        }


# ─── Mock Adapter for Testing ───────────────────────────────────────

class MockAPIAdapter(ExternalAPIAdapter):
    """Mock API adapter for testing."""
    
    def __init__(self):
        self._positions = {}
    
    def add_position(self, position_id: str, value: float, **metadata):
        """Add a mock position."""
        self._positions[position_id] = {"id": position_id, "value": value, **metadata}
    
    def remove_position(self, position_id: str):
        """Remove a mock position."""
        self._positions.pop(position_id, None)
    
    def get_all_positions(self) -> List[Dict[str, Any]]:
        """Return all mock positions."""
        return list(self._positions.values())
    
    def close_position(self, position_id: str) -> bool:
        """Close a mock position."""
        if position_id in self._positions:
            self._positions.pop(position_id)
            return True
        return False
