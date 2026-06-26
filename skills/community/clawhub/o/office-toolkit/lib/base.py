"""
Base classes and interfaces for document processing
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class DocumentProcessor(ABC):
    """Base class for document processors"""
    
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self._validate_path()
    
    def _validate_path(self):
        """Validate file path"""
        if not isinstance(self.file_path, Path):
            self.file_path = Path(self.file_path)
    
    @abstractmethod
    def read(self) -> str:
        """Read document content"""
        pass
    
    @abstractmethod
    def write(self, content: Any, output_path: Optional[Union[str, Path]] = None):
        """Write document content"""
        pass


class DocumentConverter(ABC):
    """Base class for document converters"""
    
    @abstractmethod
    def convert(self, input_path: Union[str, Path], output_path: Union[str, Path]):
        """Convert document format"""
        pass
