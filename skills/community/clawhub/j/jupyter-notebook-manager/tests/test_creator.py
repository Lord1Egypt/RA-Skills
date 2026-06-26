"""
Unit tests for notebook_creator.py
Tests notebook creation from various templates.
"""

import pytest
import json
from pathlib import Path
import sys
import tempfile
import shutil

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from notebook_creator import NotebookCreator


class TestNotebookCreator:
    """Test cases for NotebookCreator class."""
    
    @pytest.fixture
    def creator(self):
        """Create NotebookCreator instance."""
        return NotebookCreator()
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)
    
    def test_creator_initialization(self, creator):
        """Test creator initializes with templates."""
        assert creator is not None
        assert isinstance(creator.templates, dict)
        assert len(creator.templates) > 0
    
    def test_available_templates(self, creator):
        """Test all expected templates are available."""
        expected_templates = [
            "exploratory-data-analysis",
            "machine-learning-training",
            "data-cleaning",
            "time-series-analysis",
            "statistical-testing",
            "visualization-dashboard",
            "blank",
        ]
        
        for template in expected_templates:
            assert template in creator.templates, f"Template {template} not found"
    
    def test_create_blank_notebook(self, creator, temp_dir):
        """Test creating blank notebook."""
        output_path = temp_dir / "blank.ipynb"
        
        result = creator.create_notebook(
            template="blank",
            output_path=str(output_path),
            title="Test Blank Notebook"
        )
        
        assert result.exists()
        assert result == output_path
        
        # Verify notebook structure
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        assert "cells" in notebook
        assert "metadata" in notebook
        assert "nbformat" in notebook
        assert notebook["nbformat"] == 4
        assert len(notebook["cells"]) >= 2  # At least title + import cell
    
    def test_create_eda_notebook(self, creator, temp_dir):
        """Test creating EDA notebook."""
        output_path = temp_dir / "eda.ipynb"
        
        result = creator.create_notebook(
            template="exploratory-data-analysis",
            output_path=str(output_path),
            title="Sales Data Analysis",
            data_file="sales.csv"
        )
        
        assert result.exists()
        
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        # Check cells
        cells = notebook["cells"]
        assert len(cells) > 10  # EDA template has many cells
        
        # Check for key sections
        markdown_cells = [c for c in cells if c["cell_type"] == "markdown"]
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        
        assert len(markdown_cells) >= 5  # Section headers
        assert len(code_cells) >= 5  # Analysis code
        
        # Check data file is referenced
        notebook_str = json.dumps(notebook)
        assert "sales.csv" in notebook_str
    
    def test_create_ml_notebook(self, creator, temp_dir):
        """Test creating ML notebook."""
        output_path = temp_dir / "ml.ipynb"
        
        result = creator.create_notebook(
            template="machine-learning-training",
            output_path=str(output_path),
            title="Customer Churn Prediction",
            data_file="customers.csv",
            target_column="churn"
        )
        
        assert result.exists()
        
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        notebook_str = json.dumps(notebook)
        assert "churn" in notebook_str
        assert "customers.csv" in notebook_str
        assert "sklearn" in notebook_str
    
    def test_create_with_custom_cells(self, creator, temp_dir):
        """Test adding custom cells to notebook."""
        output_path = temp_dir / "custom.ipynb"
        
        custom_cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Custom Section\n"]
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": ["# Custom code\nprint('Hello')\n"],
                "execution_count": None,
                "outputs": []
            }
        ]
        
        result = creator.create_notebook(
            template="blank",
            output_path=str(output_path),
            custom_cells=custom_cells
        )
        
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        # Check custom cells were added
        cells = notebook["cells"]
        assert len(cells) >= 4  # Original + 2 custom
        assert any("Custom Section" in str(c.get("source", [])) for c in cells)
    
    def test_invalid_template(self, creator, temp_dir):
        """Test creating notebook with invalid template."""
        output_path = temp_dir / "invalid.ipynb"
        
        with pytest.raises(ValueError, match="Unknown template"):
            creator.create_notebook(
                template="non-existent-template",
                output_path=str(output_path)
            )
    
    def test_cell_creation(self, creator):
        """Test _create_cell method."""
        # Markdown cell
        md_cell = creator._create_cell("markdown", ["# Title\n", "Content\n"])
        assert md_cell["cell_type"] == "markdown"
        assert md_cell["source"] == ["# Title\n", "Content\n"]
        
        # Code cell
        code_cell = creator._create_cell("code", ["print('hello')\n"])
        assert code_cell["cell_type"] == "code"
        assert code_cell["execution_count"] is None
        assert "outputs" in code_cell
        
        # String input (auto-split)
        cell = creator._create_cell("markdown", "Line 1\nLine 2")
        assert isinstance(cell["source"], list)
        assert len(cell["source"]) == 2
    
    def test_metadata_inclusion(self, creator, temp_dir):
        """Test notebook metadata is properly set."""
        output_path = temp_dir / "metadata.ipynb"
        
        result = creator.create_notebook(
            template="blank",
            output_path=str(output_path),
            title="Metadata Test"
        )
        
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        metadata = notebook["metadata"]
        
        # Check required metadata
        assert "kernelspec" in metadata
        assert "language_info" in metadata
        assert "created_by" in metadata
        assert "created_at" in metadata
        assert "template_used" in metadata
        
        assert metadata["created_by"] == "jupyter-notebook-manager"
        assert metadata["template_used"] == "blank"
    
    def test_output_directory_creation(self, creator, temp_dir):
        """Test output directory is created if it doesn't exist."""
        nested_path = temp_dir / "a" / "b" / "c" / "notebook.ipynb"
        
        result = creator.create_notebook(
            template="blank",
            output_path=str(nested_path)
        )
        
        assert result.exists()
        assert result.parent.exists()
    
    def test_notebook_format_version(self, creator, temp_dir):
        """Test notebook uses correct format version."""
        output_path = temp_dir / "version.ipynb"
        
        result = creator.create_notebook(
            template="blank",
            output_path=str(output_path)
        )
        
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        assert notebook["nbformat"] == 4
        assert notebook["nbformat_minor"] >= 0
    
    def test_eda_template_structure(self, creator):
        """Test EDA template has correct structure."""
        cells = creator._template_eda(
            title="Test EDA",
            data_file="test.csv"
        )
        
        # Check sections are present
        section_titles = []
        for cell in cells:
            if cell["cell_type"] == "markdown":
                source = "".join(cell["source"])
                if source.startswith("##"):
                    section_titles.append(source)
        
        # Should have multiple analysis sections
        assert len(section_titles) >= 5
        
        # Check for key analysis steps
        notebook_text = json.dumps(cells)
        assert "import" in notebook_text.lower()
        assert "missing" in notebook_text.lower() or "null" in notebook_text.lower()
        assert "correlation" in notebook_text.lower() or "corr" in notebook_text.lower()
    
    def test_ml_template_structure(self, creator):
        """Test ML template has correct structure."""
        cells = creator._template_ml(
            title="Test ML",
            data_file="train.csv",
            target_column="target"
        )
        
        notebook_text = json.dumps(cells)
        
        # Check for ML-specific content
        assert "sklearn" in notebook_text
        assert "train_test_split" in notebook_text
        assert "target" in notebook_text
        
        # Check sections
        markdown_cells = [c for c in cells if c["cell_type"] == "markdown"]
        assert len(markdown_cells) >= 3  # Multiple sections
    
    def test_notebook_is_valid_json(self, creator, temp_dir):
        """Test created notebook is valid JSON."""
        output_path = temp_dir / "valid_json.ipynb"
        
        creator.create_notebook(
            template="exploratory-data-analysis",
            output_path=str(output_path)
        )
        
        # Try to load it back
        try:
            with open(output_path, 'r') as f:
                notebook = json.load(f)
            assert isinstance(notebook, dict)
        except json.JSONDecodeError:
            pytest.fail("Created notebook is not valid JSON")
    
    def test_special_characters_in_title(self, creator, temp_dir):
        """Test notebook creation with special characters."""
        output_path = temp_dir / "special.ipynb"
        
        # Title with special characters
        result = creator.create_notebook(
            template="blank",
            output_path=str(output_path),
            title="Test: Data Analysis (2024) - Part 1"
        )
        
        assert result.exists()
        
        with open(result, 'r') as f:
            notebook = json.load(f)
        
        # Check title is preserved
        first_cell = notebook["cells"][0]
        source = "".join(first_cell["source"])
        assert "Test: Data Analysis (2024) - Part 1" in source


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
