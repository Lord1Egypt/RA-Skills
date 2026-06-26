import time
import logging
import os
from datetime import datetime
from scripts.auth import auth_google

REFRESH_INTERVAL = 30 * 60  # ทุก 30 นาที
LOCK_FILE = 'refresh_service.lock'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class LockFile:
    def __init__(self, path):
        self.path = path
        self.locked = False

    def acquire(self):
        if os.path.exists(self.path):
            # Check if the lock is stale (process died)
            try:
                with open(self.path, 'r') as f:
                    pid = int(f.read())
                # If process is not running, remove stale lock
                if not self._pid_exists(pid):
                    os.remove(self.path)
                else:
                    return False
            except Exception:
                return False
        with open(self.path, 'w') as f:
            f.write(str(os.getpid()))
        self.locked = True
        return True

    def release(self):
        if self.locked and os.path.exists(self.path):
            try:
                os.remove(self.path)
            except Exception:
                pass
        self.locked = False

    def _pid_exists(self, pid):
        # Windows version
        import psutil
        return psutil.pid_exists(pid)

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("psutil not found. Please install with: pip install psutil")
        exit(1)

    lock = LockFile(LOCK_FILE)
    if not lock.acquire():
        logging.warning("Another refresh_service.py process is already running. Exiting.")
        exit(0)
    try:
        while True:
            try:
                creds = auth_google()  # refresh ถ้าจำเป็น
                logging.info(f"Token refreshed at {datetime.now()}")
            except Exception as e:
                logging.error(f"Refresh failed: {e}")
            time.sleep(REFRESH_INTERVAL)
    finally:
        lock.release()
