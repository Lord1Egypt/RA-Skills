#!/usr/bin/env python3
"""
Test fixtures for kb.llm package tests.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import Generator, Optional

# Pre-initialize logger to avoid deadlock on first import
from kb.base.logger import KBLogger
KBLogger.setup_logging()

from kb.biblio.config import LLMConfig


# --- Fixtures ---


@pytest.fixture(scope="function")
def llm_config(tmp_path) -> LLMConfig:
    """Create a test LLM config with validation skipped."""
    from unittest.mock import MagicMock
    
    LLMConfig.reset()
    
    # Create a mock KB config with tmp_path
    mock_kb_config = MagicMock()
    mock_kb_config.base_path = tmp_path
    
    with patch('kb.biblio.config.get_config', return_value=mock_kb_config):
        config = LLMConfig(
            model="gemma4:e2b",
            ollama_url="http://localhost:11434",
            timeout=30,
            temperature=0.7,
            skip_validation=True
        )
        return config


@pytest.fixture
def mock_ollama_response():
    """Mock Ollama API response."""
    return {
        "model": "gemma4:e2b",
        "response": "Mocked LLM response text",
        "done": True,
        "total_duration": 1234567890,
        "eval_count": 50,
    }


@pytest.fixture
def mock_ollama_stream_response(mock_ollama_response):
    """Mock Ollama streaming response chunks."""
    chunks = []
    text = mock_ollama_response["response"]
    for i, char in enumerate(text):
        chunks.append({
            "response": char,
            "done": i == len(text) - 1,
            "total_duration": mock_ollama_response["total_duration"],
        })
    return chunks


@pytest.fixture
def ollama_engine(llm_config):
    """Create OllamaEngine instance with mocked config."""
    from kb.biblio.engine.ollama_engine import OllamaEngine
    
    OllamaEngine.reset()
    engine = OllamaEngine(config=llm_config)
    return engine


@pytest.fixture
def temp_llm_dirs(tmp_path) -> dict:
    """Create temporary LLM directory structure."""
    base = tmp_path / "library" / "llm"
    dirs = {
        "base": base,
        "essences": base / "essences",
        "reports": base / "reports",
        "reports_daily": base / "reports" / "daily",
        "reports_weekly": base / "reports" / "weekly",
        "reports_monthly": base / "reports" / "monthly",
        "graph": base / "graph",
        "incoming": base / "incoming",
    }
    
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    
    return dirs


@pytest.fixture
def sample_pdf(tmp_path) -> Path:
    """Create a sample PDF file for testing."""
    pdf = tmp_path / "test_document.pdf"
    pdf.write_text("Sample PDF content for testing", encoding="utf-8")
    return pdf


@pytest.fixture
def sample_markdown(tmp_path) -> Path:
    """Create a sample markdown file for testing."""
    md = tmp_path / "test_document.md"
    md.write_text("# Test Document\n\nThis is test content.", encoding="utf-8")
    return md


@pytest.fixture
def sample_text(tmp_path) -> Path:
    """Create a sample text file for testing."""
    txt = tmp_path / "test_document.txt"
    txt.write_text("Sample text content for testing", encoding="utf-8")
    return txt


@pytest.fixture
def mock_llm_content_manager(llm_config, temp_llm_dirs):
    """Create a mocked LLMContentManager with temp directories."""
    from kb.biblio.content_manager import LLMContentManager
    
    with patch.object(LLMConfig, 'get_instance', return_value=llm_config) as mock_config:
        manager = LLMContentManager(llm_config=llm_config)
        # Override paths to use temp dirs
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        yield manager


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# --- Mock Utilities ---


class MockOllamaEngine:
    """Mock OllamaEngine for testing without actual Ollama server."""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self._config = config or llm_config()
        self._call_count = 0
    
    def generate(self, prompt: str, **kwargs) -> "LLMResponse":
        """Mock generate that returns canned response."""
        from kb.biblio.engine.base import LLMResponse, LLMProvider
        
        self._call_count += 1
        
        return LLMResponse(
            content=f"Mocked response to: {prompt[:50]}...",
            model=self._config.model,
            provider=LLMProvider.OLLAMA,
            done=True,
            total_duration=1000000000,
            tokens=len(prompt) // 4,
        )
    
    async def generate_async(self, prompt: str, **kwargs) -> "LLMResponse":
        """Mock async generate."""
        return self.generate(prompt, **kwargs)
    
    def is_available(self) -> bool:
        """Mock availability check."""
        return True
    
    def get_model_name(self) -> str:
        """Mock model name."""
        return self._config.model
    
    def get_provider(self) -> "LLMProvider":
        """Mock provider."""
        from kb.biblio.engine.base import LLMProvider
        return LLMProvider.OLLAMA
    
    @property
    def supports_streaming(self) -> bool:
        return True
    
    @property
    def supports_async(self) -> bool:
        return True


@pytest.fixture
def mock_engine():
    """Provide a MockOllamaEngine instance."""
    return MockOllamaEngine()


# --- Async Test Helper ---


@pytest.fixture
async def async_manager(llm_config, temp_llm_dirs):
    """Create actual LLMContentManager with temp dirs for async tests."""
    from kb.biblio.content_manager import LLMContentManager
    
    manager = LLMContentManager(llm_config=llm_config)
    # Override paths
    manager._llm_config._essences_path = temp_llm_dirs["essences"]
    manager._llm_config._reports_path = temp_llm_dirs["reports"]
    manager._llm_config._graph_path = temp_llm_dirs["graph"]
    manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
    
    return manager


# --- TransformersEngine Fixtures ---


@pytest.fixture
def mock_torch():
    """Mock fuer torch.cuda mit typischen CUDA-Operationen."""
    mock = MagicMock()
    mock.__version__ = "2.2.0"
    mock.cuda.is_available.return_value = True
    mock.cuda.is_bf16_supported.return_value = False
    mock.cuda.device_count.return_value = 1
    mock.cuda.empty_cache = MagicMock()
    mock.cuda.OutOfMemoryError = type("OutOfMemoryError", (RuntimeError,), {})
    mock.cuda.get_device_name.return_value = "Mock GPU"
    mock.cuda.memory_allocated.return_value = 0
    mock.cuda.memory_reserved.return_value = 0
    mock.cuda.get_device_properties.return_value = MagicMock(total_memory=8 * (1024 ** 3))
    mock.float16 = "float16"
    mock.float32 = "float32"
    mock.bfloat16 = "bfloat16"
    mock.device = MagicMock(return_value=MagicMock(type="cuda"))
    mock.inference_mode = MagicMock(return_value=MagicMock(__enter__=Mock(), __exit__=Mock(return_value=False)))
    # For generate() OOM handling
    mock.no_grad = MagicMock(return_value=MagicMock(__enter__=Mock(), __exit__=Mock(return_value=False)))
    return mock


@pytest.fixture
def mock_transformers():
    """Mock fuer transformers.AutoModel und zugehoerige Klassen."""
    mock = MagicMock()
    mock.__version__ = "4.40.0"
    mock.AutoModelForCausalLM = MagicMock()
    mock.AutoTokenizer = MagicMock()
    mock.TextIteratorStreamer = MagicMock()
    mock.BitsAndBytesConfig = MagicMock()
    return mock


@pytest.fixture
def hf_config():
    """LLMConfig mit HuggingFace-Settings."""
    LLMConfig.reset()
    config = LLMConfig(
        model_source="huggingface",
        hf_model_name="google/gemma-2-2b-it",
        hf_device="auto",
        hf_quantization=None,
        hf_torch_dtype="auto",
        skip_validation=True,
    )
    return config


@pytest.fixture
def transformers_engine(hf_config, mock_torch, mock_transformers):
    """TransformersEngine-Instanz mit Mock-Dependencies."""
    from kb.biblio.engine.transformers_engine import TransformersEngine
    TransformersEngine.reset()  # Reset singleton before each test
    engine = TransformersEngine(config=hf_config)
    return engine


# --- Import for type hints ---
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from kb.biblio.engine.base import LLMResponse
    from kb.biblio.config import LLMConfig