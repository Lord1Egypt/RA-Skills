#!/usr/bin/env python3
"""
Simple logging utility for Health Coach.
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional


class Logger:
    """Simple file logger."""
    
    def __init__(self, username: str, log_dir: Optional[str] = None):
        self.username = username
        
        if log_dir is None:
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(skill_dir, 'logs')
        
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Log file: logs/<username>_YYYYMMDD.log
        today = datetime.now().strftime('%Y%m%d')
        self.log_file = os.path.join(log_dir, f"{username}_{today}.log")
    
    def _write(self, level: str, message: str, **kwargs):
        """Write log entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        entry.update(kwargs)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._write('INFO', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._write('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._write('ERROR', message, **kwargs)
    
    def scan_result(self, product: str, action: str, barcode: Optional[str] = None, **kwargs):
        """Log OCR scan result."""
        self._write('SCAN', f"Scanned: {product}", 
                   product=product, action=action, barcode=barcode, **kwargs)


def get_logger(username: str) -> Logger:
    """Get logger instance for user."""
    return Logger(username)


if __name__ == '__main__':
    # Test
    logger = get_logger('test')
    logger.info("Test message", module="test")
    logger.scan_result("薯片", "added_new", barcode="1234567890")
    print(f"Log written to: {logger.log_file}")
