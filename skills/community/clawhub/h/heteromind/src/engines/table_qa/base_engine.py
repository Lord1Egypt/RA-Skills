"""
HeteroMind - TableQA Base Engine

Base class for Table QA engines.
"""

from ..base import BaseEngine

class BaseTableQAEngine(BaseEngine):
    """
    Base class for Table QA engines.
    
    Provides common utilities for table-based question answering.
    """
    
    def __init__(self, config: dict):
        """
        Initialize Table QA engine.
        
        Args:
            config: Configuration dict
        """
        super().__init__(config)
        self.table_path = config.get("table_path")
        self.supported_formats = config.get("supported_formats", ["csv", "xlsx"])
