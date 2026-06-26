import fcntl
import os

class WorkspaceLockException(Exception):
    pass

class WorkspaceLock:
    def __init__(self, workspace_dir):
        self.lock_file = os.path.join(workspace_dir, '.sdlc_run.lock')
        self.fd = None

    def acquire(self):
        self.fd = open(self.lock_file, 'w')
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (BlockingIOError, IOError):
            self.fd.close()
            self.fd = None
            raise WorkspaceLockException("Could not acquire lock.")
        return self

    def release(self):
        if self.fd:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
            except Exception:
                pass
            self.fd.close()
            self.fd = None

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
