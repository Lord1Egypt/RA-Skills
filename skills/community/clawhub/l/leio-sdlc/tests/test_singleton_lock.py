import unittest
import os
from utils.singleton_lock import acquire_lock, ConcurrentExecutionError

class TestSingletonLock(unittest.TestCase):
    def test_acquire_lock_success(self):
        lock_file = ".test_success.lock"
        fd = acquire_lock(lock_file)
        self.assertIsNotNone(fd)
        # Cleanup
        os.close(fd)
        if os.path.exists(lock_file):
            os.remove(lock_file)

    def test_acquire_lock_failure(self):
        lock_file = ".test_failure.lock"
        # Acquire first lock
        fd1 = acquire_lock(lock_file)
        
        # Attempt second lock should fail
        with self.assertRaises(ConcurrentExecutionError):
            acquire_lock(lock_file)
            
        # Cleanup
        os.close(fd1)
        if os.path.exists(lock_file):
            os.remove(lock_file)

if __name__ == '__main__':
    unittest.main()
