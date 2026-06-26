#!/usr/bin/env python3
"""
Kiwi Voice Utilities

Logging, crash protection, and common utilities for Kiwi Voice Service.
"""

import os
import sys
import time
import traceback
import threading
from datetime import datetime
from typing import Optional, Callable

# Global lock for stdout to prevent garbled output in multi-threaded environment
_stdout_lock = threading.Lock()


def kiwi_log(tag: str, message: str, level: str = "INFO"):
    """
    Log a message with timestamp and tag.
    
    Format: [HH:MM:SS.mmm] [LEVEL] [TAG] message
    
    Args:
        tag: Component tag (e.g., "MIC", "WHISPER", "TTS")
        message: Log message
        level: Log level (DEBUG, INFO, WARN, ERROR)
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    # Format: [14:08:25.342] [INFO] [MIC] Speech started
    log_line = f"[{timestamp}] [{level}] [{tag}] {message}"
    
    with _stdout_lock:
        print(log_line, flush=True)


def kiwi_log_progress(tag: str, current: int, total: int, message: str = ""):
    """
    Log progress with timestamp.
    
    Args:
        tag: Component tag
        current: Current progress value
        total: Total progress value
        message: Additional message
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    percent = (current / total * 100) if total > 0 else 0
    bar_len = int(percent / 2)
    bar = "█" * bar_len + "░" * (50 - bar_len)
    
    log_line = f"[{timestamp}] [{tag}] |{bar}| {percent:.1f}% {message}"
    
    with _stdout_lock:
        print(log_line, flush=True)


def log_crash(exc_type, exc_value, exc_traceback):
    """
    Log crash information to file for debugging.
    
    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    from kiwi import LOGS_DIR
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    crash_file = os.path.join(LOGS_DIR, f"kiwi_crash_{timestamp}.log")

    try:
        with open(crash_file, 'w', encoding='utf-8') as f:
            f.write(f"Kiwi Voice Crash Log\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Exception Type: {exc_type.__name__}\n")
            f.write(f"Exception Value: {exc_value}\n")
            f.write(f"\nTraceback:\n")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
            f.write(f"\n\nThread Information:\n")
            for thread in threading.enumerate():
                f.write(f"  - {thread.name} (daemon={thread.daemon})\n")
        
        kiwi_log("CRASH", f"Crash log saved to {crash_file}", level="ERROR")
    except Exception as e:
        print(f"[CRITICAL] Failed to write crash log: {e}", file=sys.stderr)


def setup_crash_protection():
    """
    Setup global crash protection for the application.
    
    This should be called once at the start of the application.
    """
    def custom_excepthook(exc_type, exc_value, exc_traceback):
        log_crash(exc_type, exc_value, exc_traceback)
        # Call the original excepthook to still print to stderr
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = custom_excepthook
    kiwi_log("INIT", "Crash protection enabled")


def thread_safe_loop(thread_name: str, loop_func: Callable, stop_event, retry_delay: float = 1.0):
    """
    Run a loop function with crash protection and auto-retry.
    
    Args:
        thread_name: Name of the thread for logging
        loop_func: Function to run in the loop (should check stop_event)
        stop_event: threading.Event to signal stop
        retry_delay: Delay in seconds before retry after crash
    """
    kiwi_log(thread_name, f"Thread started")
    
    while not stop_event.is_set():
        try:
            loop_func()
        except Exception as e:
            kiwi_log(thread_name, f"Thread crashed: {e}", level="ERROR")
            kiwi_log(thread_name, f"Traceback: {traceback.format_exc()}", level="DEBUG")
            kiwi_log(thread_name, f"Restarting in {retry_delay}s...")
            time.sleep(retry_delay)
    
    kiwi_log(thread_name, f"Thread stopped")


# Backward compatibility: keep old function names for existing code
def log(tag: str, message: str, level: str = "INFO"):
    """Alias for kiwi_log for backward compatibility."""
    kiwi_log(tag, message, level)


if __name__ == "__main__":
    # Test the logging
    setup_crash_protection()
    kiwi_log("TEST", "This is a test message")
    kiwi_log("TEST", "This is a warning", level="WARN")
    kiwi_log("TEST", "This is an error", level="ERROR")
    
    # Test progress logging
    for i in range(0, 101, 10):
        kiwi_log_progress("TEST", i, 100, f"Processing...")
        time.sleep(0.1)
    
    print("\nTest complete!")
