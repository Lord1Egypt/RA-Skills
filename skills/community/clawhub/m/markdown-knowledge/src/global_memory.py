# Global Memory Module (placeholder)
# This module provides optional global memory functionality

class GlobalMemory:
    """Optional global memory for cross-session context."""
    
    def __init__(self):
        self.memory = {}
    
    def store(self, key, value):
        self.memory[key] = value
    
    def retrieve(self, key, default=None):
        return self.memory.get(key, default)
    
    def clear(self):
        self.memory.clear()
