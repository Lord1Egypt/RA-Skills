import fcntl
import os

class ConcurrentExecutionError(Exception):
    pass

def acquire_lock(lock_file_path=".sdlc_run.lock"):
    try:
        fd = os.open(lock_file_path, os.O_CREAT | os.O_RDWR)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except BlockingIOError:
        raise ConcurrentExecutionError(f"Cannot acquire lock on {lock_file_path}")
