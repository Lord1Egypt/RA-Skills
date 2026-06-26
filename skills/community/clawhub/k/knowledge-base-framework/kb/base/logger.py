#!/usr/bin/env python3
"""
KBLogger - Singleton für KB Logging

Konsistentes Format, konsistentes Level.
Verbesserungen gegenüber Original:
- Thread-Safe Initialization
- Colored Output Support (TTY Detection)
- Named Logger Cache
- Configurable Format
"""

import logging
import sys
import threading
from typing import Optional, Dict


# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for TTY output."""
    
    COLORS = {
        'DEBUG': Colors.GRAY,
        'INFO': Colors.GREEN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.MAGENTA,
    }
    
    def format(self, record):
        if sys.stderr.isatty() or sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, Colors.RESET)
            record.levelname = f"{color}{record.levelname}{Colors.RESET}"
        return super().format(record)


class KBLogger:
    """
    Singleton für KB Logging.
    
    Thread-safe implementation with colored output support.
    
    Usage:
        KBLogger.setup_logging()  # Once at app start
        log = KBLogger.get_logger("kb.sync")
        log.info("Hello world")
    """
    
    _initialized: bool = False
    _lock = threading.Lock()
    _default_level: int = logging.INFO
    _format_str: str = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    _date_format: str = '%Y-%m-%d %H:%M:%S'
    
    # Cache for logger instances
    _logger_cache: Dict[str, logging.Logger] = {}
    _cache_lock = threading.Lock()
    
    @classmethod
    def setup_logging(
        cls,
        level: int = logging.INFO,
        format_str: Optional[str] = None,
        date_format: Optional[str] = None,
        use_colors: bool = True
    ) -> None:
        """
        Initialize global logging configuration.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR)
            format_str: Custom format string
            date_format: Custom date format
            use_colors: Enable colored output for TTY
        """
        with cls._lock:
            if cls._initialized:
                return
            
            cls._default_level = level
            
            if format_str is not None:
                cls._format_str = format_str
            
            if date_format is not None:
                cls._date_format = date_format
            
            # Create formatter
            if use_colors and (sys.stderr.isatty() or sys.stdout.isatty()):
                formatter = ColoredFormatter(cls._format_str, datefmt=cls._date_format)
            else:
                formatter = logging.Formatter(cls._format_str, datefmt=cls._date_format)
            
            # Setup root handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            
            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(level)
            root_logger.handlers.clear()
            root_logger.addHandler(handler)
            
            cls._initialized = True
    
    @classmethod
    def get_logger(cls, name: str, level: Optional[int] = None) -> logging.Logger:
        """
        Get or create logger for specified name.
        
        Thread-safe with caching for performance.
        All cache operations are under _cache_lock to prevent race conditions.
        
        Args:
            name: Logger name (e.g., "kb.sync")
            level: Optional level override
            
        Returns:
            Configured logger instance
        """
        # Ensure logging is initialized
        if not cls._initialized:
            with cls._lock:
                if not cls._initialized:
                    cls.setup_logging()
        
        with cls._cache_lock:
            if name in cls._logger_cache:
                cached = cls._logger_cache[name]
                if level is not None:
                    cached.setLevel(level)
                return cached
            
            # Create new logger under lock to prevent duplicate creation
            logger = logging.getLogger(name)
            
            if level is not None:
                logger.setLevel(level)
            elif not logger.level:
                logger.setLevel(cls._default_level)
            
            # Avoid duplicate handlers and duplicate propagation
            if not logger.handlers:
                handler = logging.StreamHandler(sys.stdout)
                formatter = logging.Formatter(cls._format_str, datefmt=cls._date_format)
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.propagate = False
            
            # Cache the logger
            cls._logger_cache[name] = logger
            
            return logger
    
    @classmethod
    def set_level(cls, level: int) -> None:
        """Change default log level."""
        with cls._lock:
            cls._default_level = level
            logging.getLogger().setLevel(level)
    
    @classmethod
    def reset(cls) -> None:
        """Reset logger state (mainly for testing)."""
        with cls._lock:
            cls._initialized = False
            cls._logger_cache.clear()
            # Clear all handlers from root
            root = logging.getLogger()
            root.handlers.clear()


# Convenience function
def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Get KB logger instance."""
    return KBLogger.get_logger(name, level)
