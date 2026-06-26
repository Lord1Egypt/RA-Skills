#!/usr/bin/env python3
"""
BaseCommand - Abstract Base Class für alle KB Commands

Jeder Command muss:
- `name` definieren (CLI command name)
- `add_arguments()` implementieren (argparse Konfiguration)
- `_execute()` implementieren (Hauptlogik)

Verbesserungen gegenüber Original:
- Besseres Error Handling
- Graceful Degradation bei fehlender DB
- Progress Reporting
- Command-specific Logging Setup
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import argparse
import logging
import sys
import traceback

from kb.base.config import KBConfig
from kb.base.logger import KBLogger
from kb.base.db import KBConnection, KBConnectionError


class CommandError(Exception):
    """Base exception for command errors."""
    pass


class ValidationError(CommandError):
    """Validation failed."""
    pass


class ExecutionError(CommandError):
    """Execution failed."""
    pass


class BaseCommand(ABC):
    """
    Abstract Base Class für alle KB Commands.
    
    Jeder Command muss:
    - `name` definieren (CLI command name)
    - `add_arguments()` implementieren (argparse Konfiguration)
    - `_execute()` implementieren (Hauptlogik)
    
    Geerbte Funktionalität:
    - validate() mit Basis-Checks
    - cleanup() für Aufräumen
    - get_config() / get_logger() / get_db()
    
    Usage:
        @register_command
        class MyCommand(BaseCommand):
            name = "mycmd"
            help = "My command description"
            
            def add_arguments(self, parser: argparse.ArgumentParser) -> None:
                parser.add_argument('--verbose', '-v', action='store_true')
            
            def _execute(self) -> int:
                log = self.get_logger()
                log.info("Doing work...")
                return 0
    """
    
    name: str = "base"
    help: str = "Base command (should not be instantiated)"
    
    # Default exit codes
    EXIT_SUCCESS = 0
    EXIT_VALIDATION_ERROR = 1
    EXIT_EXECUTION_ERROR = 2
    EXIT_CLEANUP_ERROR = 3
    
    def __init__(self):
        self._config: Optional[KBConfig] = None
        self._logger: Optional[logging.Logger] = None
        self._args: Optional[argparse.Namespace] = None
        self._exit_code: int = self.EXIT_SUCCESS
    
    # --- Subclass Interface (must implement) ---
    
    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Fügt Commands-spezifische Argumente hinzu.
        
        Override in subclass to add command-specific arguments.
        """
        pass
    
    @abstractmethod
    def _execute(self) -> int:
        """
        Hauptlogik des Commands.
        
        Override in subclass. Return 0 for success, non-zero for error.
        """
        pass
    
    # --- Validation Hook (optional override) ---
    
    def validate(self, args: argparse.Namespace) -> bool:
        """
        Validiert Argumente vor Ausführung.
        
        Default: Checks DB connectivity.
        Subclasses can override for additional checks.
        
        Raises:
            ValidationError: If validation fails critically
        """
        try:
            config = self.get_config()
            db_path = config.db_path
            
            if not db_path.exists():
                self.get_logger().warning(f"Database not found: {db_path}")
                # Don't fail - DB might be created later
                return True
            
            with self.get_db() as conn:
                conn.execute("SELECT 1")
            
            return True
            
        except KBConnectionError as e:
            self.get_logger().error(f"Database validation failed: {e}")
            return False
        except Exception as e:
            self.get_logger().error(f"Validation error: {e}")
            if self.get_logger().isEnabledFor(logging.DEBUG):
                traceback.print_exc()
            return False
    
    # --- Cleanup Hook (optional override) ---
    
    def cleanup(self) -> None:
        """
        Aufräumen nach Ausführung.
        
        Override in subclass if cleanup is needed.
        Called even if _execute() raises an exception.
        """
        pass
    
    # --- Execution Pipeline ---
    
    def run(self, args: argparse.Namespace) -> int:
        """
        Führt den Command aus.
        
        Pipeline: setup -> validate -> _execute -> cleanup
        
        Returns:
            Exit code (0 = success, non-zero = error)
        """
        self._args = args
        
        # Setup logging for this command
        self._setup_command_logging()
        
        log = self.get_logger()
        log.debug(f"Starting command: {self.name}")
        
        # Validation phase
        if not self._run_validation(args):
            return self.EXIT_VALIDATION_ERROR
        
        # Execution phase
        try:
            self._exit_code = self._execute()
            return self._exit_code
        except KeyboardInterrupt:
            log.warning("Interrupted by user")
            return 130  # Standard Ctrl+C exit code
        except Exception as e:
            log.error(f"Execution failed: {e}")
            if log.isEnabledFor(logging.DEBUG):
                traceback.print_exc()
            return self.EXIT_EXECUTION_ERROR
        finally:
            self._run_cleanup()
    
    def _run_validation(self, args: argparse.Namespace) -> bool:
        """Run validation with error handling."""
        try:
            return self.validate(args)
        except ValidationError as e:
            self.get_logger().error(f"Validation error: {e}")
            return False
        except Exception as e:
            self.get_logger().error(f"Unexpected validation error: {e}")
            return False
    
    def _run_cleanup(self) -> None:
        """Run cleanup with error handling."""
        try:
            self.cleanup()
        except Exception as e:
            log = self.get_logger()
            log.error(f"Cleanup error: {e}")
    
    def _setup_command_logging(self) -> None:
        """Setup logging context for this command."""
        # Logger is created lazily on first get_logger() call
    
    # --- Shared Resources ---
    
    def get_config(self) -> KBConfig:
        """Gibt KBConfig Singleton zurück."""
        if self._config is None:
            self._config = KBConfig.get_instance()
        return self._config
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Gibt Logger für diesen Command zurück.
        
        Args:
            name: Optional logger name suffix. Defaults to "kb.{command_name}"
        """
        if self._logger is None:
            logger_name = name or f"kb.{self.name}"
            self._logger = KBLogger.get_logger(logger_name)
        return self._logger
    
    def get_db(self) -> KBConnection:
        """Gibt DB Connection Context Manager zurück."""
        return KBConnection(self.get_config().db_path)
    
    # --- Helper Methods ---
    
    def log_section(self, title: str, char: str = "=", width: int = 50) -> None:
        """Log a section header."""
        line = char * width
        self.get_logger().info(line)
        self.get_logger().info(title)
        self.get_logger().info(line)
    
    def log_progress(self, current: int, total: int, prefix: str = "Progress") -> None:
        """Log progress update."""
        pct = (current / total * 100) if total > 0 else 0
        self.get_logger().info(f"{prefix}: {current}/{total} ({pct:.1f}%)")
    
    def require_db(self) -> KBConnection:
        """
        Get DB connection, failing fast if unavailable.
        
        Raises:
            ValidationError: If database is not accessible
        """
        config = self.get_config()
        if not config.db_path.exists():
            raise ValidationError(f"Database not found: {config.db_path}")
        
        try:
            conn = self.get_db()
            # Test connection
            conn.execute("SELECT 1")
            return conn
        except KBConnectionError as e:
            raise ValidationError(f"Cannot connect to database: {e}")
    
    def print_error(self, message: str) -> None:
        """Print error to stderr."""
        print(f"ERROR: {message}", file=sys.stderr)
    
    def print_warning(self, message: str) -> None:
        """Print warning to stderr."""
        print(f"WARNING: {message}", file=sys.stderr)


def format_error(e: Exception, include_traceback: bool = False) -> str:
    """Format exception as user-friendly string."""
    if include_traceback:
        return f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
    return f"{type(e).__name__}: {e}"
