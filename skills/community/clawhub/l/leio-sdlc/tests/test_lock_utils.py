import sys
import os
import unittest
import tempfile
import shutil
import multiprocessing
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from lock_utils import WorkspaceLock, WorkspaceLockException

def hold_lock_worker(workspace_dir, event):
    lock = WorkspaceLock(workspace_dir)
    lock.acquire()
    event.set()
    time.sleep(2)
    lock.release()

class TestWorkspaceLock(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_acquire_and_release(self):
        lock = WorkspaceLock(self.test_dir)
        lock.acquire()
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, '.sdlc_run.lock')))
        lock.release()
        
        lock2 = WorkspaceLock(self.test_dir)
        lock2.acquire()
        lock2.release()

    def test_concurrent_lock_fails(self):
        event = multiprocessing.Event()
        p = multiprocessing.Process(target=hold_lock_worker, args=(self.test_dir, event))
        p.start()
        
        event.wait(timeout=5)
        
        lock = WorkspaceLock(self.test_dir)
        with self.assertRaises(WorkspaceLockException):
            lock.acquire()
            
        p.join()

    def test_context_manager(self):
        with WorkspaceLock(self.test_dir):
            lock2 = WorkspaceLock(self.test_dir)
            with self.assertRaises(WorkspaceLockException):
                lock2.acquire()

if __name__ == '__main__':
    unittest.main()
