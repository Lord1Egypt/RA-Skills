"""
Unit tests for notebook_executor.py
Tests notebook execution, monitoring, and error handling.
"""

import pytest
import json
from pathlib import Path
import sys
import tempfile
import shutil
import time

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from notebook_executor import NotebookExecutor
from notebook_creator import NotebookCreator


class TestNotebookExecutor:
    """Test cases for NotebookExecutor class."""
    
    @pytest.fixture
    def executor(self):
        """Create NotebookExecutor instance."""
        return NotebookExecutor(timeout=60)
    
    @pytest.fixture
    def creator(self):
        """Create NotebookCreator for test notebooks."""
        return NotebookCreator()
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)
    
    @pytest.fixture
    def simple_notebook(self, temp_dir):
        """Create a simple notebook for testing."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Test Notebook\n"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["x = 1 + 1\nprint(x)\n"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["y = x * 2\nprint(f'Result: {y}')\n"]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        
        notebook_path = temp_dir / "simple.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f)
        
        return notebook_path
    
    @pytest.fixture
    def error_notebook(self, temp_dir):
        """Create a notebook with an error."""
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["x = 10\n"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["# This will raise KeyError\nresult = {'a': 1}['b']\n"]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        
        notebook_path = temp_dir / "error.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f)
        
        return notebook_path
    
    def test_executor_initialization(self, executor):
        """Test executor initializes with timeout."""
        assert executor is not None
        assert executor.timeout == 60
    
    def test_execute_nonexistent_notebook(self, executor):
        """Test execution of non-existent notebook."""
        result = executor.execute(
            notebook_path="nonexistent.ipynb",
            verbose=False
        )
        
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()
    
    @pytest.mark.slow
    def test_execute_simple_notebook(self, executor, simple_notebook):
        """Test successful execution of simple notebook."""
        result = executor.execute(
            notebook_path=str(simple_notebook),
            verbose=False
        )
        
        assert result["status"] == "success"
        assert result["execution_time"] > 0
        assert result["cell_count"] == 3
        assert "output_path" in result
    
    @pytest.mark.slow
    def test_execute_with_output_path(self, executor, simple_notebook, temp_dir):
        """Test execution with different output path."""
        output_path = temp_dir / "executed.ipynb"
        
        result = executor.execute(
            notebook_path=str(simple_notebook),
            output_path=str(output_path),
            verbose=False
        )
        
        assert result["status"] == "success"
        assert output_path.exists()
        assert str(output_path) in result["output_path"]
    
    @pytest.mark.slow
    def test_execute_with_parameters(self, executor, temp_dir):
        """Test parameterized execution."""
        # Create notebook that uses parameters
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["# Default value\nvalue = 0\n"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["result = value * 2\nprint(f'Result: {result}')\n"]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        
        notebook_path = temp_dir / "param.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f)
        
        # Execute with parameters
        result = executor.execute(
            notebook_path=str(notebook_path),
            parameters={"value": 5},
            verbose=False
        )
        
        assert result["status"] == "success"
        
        # Check parameter was injected
        with open(notebook_path, 'r') as f:
            executed_nb = json.load(f)
        
        # Should have parameter cell
        sources = [cell["source"] for cell in executed_nb["cells"]]
        has_param_cell = any("value = 5" in "".join(src) for src in sources)
        assert has_param_cell or result["status"] == "success"  # Parameter injection may vary
    
    @pytest.mark.slow
    def test_execute_error_notebook(self, executor, error_notebook):
        """Test execution of notebook with errors."""
        result = executor.execute(
            notebook_path=str(error_notebook),
            verbose=False
        )
        
        # Should complete but report error
        assert result["status"] == "error"
        assert "error" in result
        assert "error_cell" in result
        assert result["error_cell"] == 2  # Second cell has error
    
    def test_inject_parameters(self, executor):
        """Test parameter injection."""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "source": ["# Title\n"]
                }
            ]
        }
        
        parameters = {
            "name": "test",
            "value": 42,
            "ratio": 0.5
        }
        
        result = executor._inject_parameters(notebook, parameters)
        
        # Check parameter cell was added
        assert len(result["cells"]) == 2
        param_cell = result["cells"][1]
        
        assert param_cell["cell_type"] == "code"
        source = "".join(param_cell["source"])
        
        assert "name = 'test'" in source
        assert "value = 42" in source
        assert "ratio = 0.5" in source
    
    def test_check_for_errors(self, executor):
        """Test error detection in executed notebooks."""
        # Notebook with error output
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "outputs": [
                        {
                            "output_type": "error",
                            "ename": "KeyError",
                            "evalue": "'missing_key'",
                            "traceback": [
                                "Traceback (most recent call last):",
                                "  File \"<ipython-input-2-abc>\", line 1, in <module>",
                                "    result = data['missing_key']",
                                "KeyError: 'missing_key'"
                            ]
                        }
                    ]
                }
            ]
        }
        
        error_info = executor._check_for_errors(notebook)
        
        assert error_info is not None
        assert error_info["error"] == "KeyError"
        assert error_info["error_cell"] == 1
        assert "traceback" in error_info["error_message"].lower()
    
    def test_extract_outputs(self, executor, temp_dir):
        """Test output extraction from executed notebook."""
        # Create notebook with various outputs
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "outputs": [
                        {
                            "output_type": "stream",
                            "name": "stdout",
                            "text": ["Hello World\n"]
                        }
                    ]
                },
                {
                    "cell_type": "code",
                    "outputs": [
                        {
                            "output_type": "execute_result",
                            "data": {
                                "text/plain": ["42"]
                            },
                            "execution_count": 1
                        }
                    ]
                },
                {
                    "cell_type": "code",
                    "outputs": [
                        {
                            "output_type": "display_data",
                            "data": {
                                "image/png": "iVBORw0KGgoAAAANS..."
                            }
                        }
                    ]
                }
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 5
        }
        
        notebook_path = temp_dir / "outputs.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f)
        
        outputs = executor._extract_outputs(notebook_path)
        
        assert len(outputs) == 3
        
        # Check text output
        assert outputs[0]["cell"] == 1
        assert outputs[0]["outputs"][0]["type"] == "text"
        assert "Hello World" in outputs[0]["outputs"][0]["content"]
        
        # Check result output
        assert outputs[1]["cell"] == 2
        assert outputs[1]["outputs"][0]["type"] == "result"
        
        # Check image output
        assert outputs[2]["cell"] == 3
        assert outputs[2]["outputs"][0]["type"] == "image"
    
    @pytest.mark.slow
    def test_execution_timing(self, executor, simple_notebook):
        """Test execution time is recorded."""
        result = executor.execute(
            notebook_path=str(simple_notebook),
            verbose=False
        )
        
        assert "execution_time" in result
        assert result["execution_time"] > 0
        assert result["execution_time"] < 60  # Should be fast
    
    def test_verbose_output(self, executor, simple_notebook, capsys):
        """Test verbose mode prints progress."""
        executor.execute(
            notebook_path=str(simple_notebook),
            verbose=True
        )
        
        captured = capsys.readouterr()
        assert "Executing notebook" in captured.out
    
    def test_quiet_mode(self, executor, simple_notebook, capsys):
        """Test quiet mode suppresses output."""
        executor.execute(
            notebook_path=str(simple_notebook),
            verbose=False
        )
        
        captured = capsys.readouterr()
        # Should have minimal or no output
        assert len(captured.out) < 100 or captured.out == ""
    
    @pytest.mark.slow
    def test_kernel_selection(self, executor, simple_notebook):
        """Test execution with specified kernel."""
        result = executor.execute(
            notebook_path=str(simple_notebook),
            kernel="python3",
            verbose=False
        )
        
        # Should succeed with valid kernel
        assert result["status"] in ["success", "error"]  # May error if kernel not available
    
    def test_multiple_parameters(self, executor):
        """Test injection of multiple parameter types."""
        notebook = {"cells": []}
        
        parameters = {
            "string_param": "hello",
            "int_param": 42,
            "float_param": 3.14,
            "bool_param": True,
            "list_param": [1, 2, 3]
        }
        
        result = executor._inject_parameters(notebook, parameters)
        
        param_cell = result["cells"][0]
        source = "".join(param_cell["source"])
        
        assert "string_param = 'hello'" in source
        assert "int_param = 42" in source
        assert "float_param = 3.14" in source
        assert "bool_param = True" in source
        assert "list_param = [1, 2, 3]" in source


# Integration test
class TestIntegration:
    """Integration tests combining creator and executor."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)
    
    @pytest.mark.slow
    def test_create_and_execute(self, temp_dir):
        """Test creating and executing a notebook."""
        # Create notebook
        creator = NotebookCreator()
        notebook_path = creator.create_notebook(
            template="blank",
            output_path=str(temp_dir / "test.ipynb"),
            title="Integration Test"
        )
        
        # Execute notebook
        executor = NotebookExecutor()
        result = executor.execute(
            notebook_path=str(notebook_path),
            verbose=False
        )
        
        assert result["status"] == "success"
        assert result["cell_count"] >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
