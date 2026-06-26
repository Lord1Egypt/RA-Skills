#!/usr/bin/env python3
"""
Jupyter Notebook Creator
Creates Jupyter notebooks from templates with customization.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Notebook format version
NBFORMAT_VERSION = 4
NBFORMAT_MINOR = 5


class NotebookCreator:
    """Create Jupyter notebooks with various templates."""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, callable]:
        """Load predefined notebook templates."""
        return {
            "exploratory-data-analysis": self._template_eda,
            "machine-learning-training": self._template_ml,
            "data-cleaning": self._template_cleaning,
            "time-series-analysis": self._template_timeseries,
            "statistical-testing": self._template_stats,
            "visualization-dashboard": self._template_viz,
            "blank": self._template_blank,
        }
    
    def create_notebook(
        self,
        template: str = "blank",
        output_path: str = "notebook.ipynb",
        title: str = "Untitled",
        author: str = "Data Scientist",
        data_file: Optional[str] = None,
        target_column: Optional[str] = None,
        custom_cells: Optional[List[Dict]] = None,
    ) -> Path:
        """
        Create a Jupyter notebook from template.
        
        Args:
            template: Template name
            output_path: Output file path
            title: Notebook title
            author: Author name
            data_file: Path to data file (if applicable)
            target_column: Target variable name (for ML)
            custom_cells: Additional cells to include
        
        Returns:
            Path to created notebook
        """
        # Get template
        if template not in self.templates:
            raise ValueError(f"Unknown template: {template}. Available: {list(self.templates.keys())}")
        
        template_func = self.templates[template]
        cells = template_func(
            title=title,
            author=author,
            data_file=data_file,
            target_column=target_column
        )
        
        # Add custom cells if provided
        if custom_cells:
            cells.extend(custom_cells)
        
        # Create notebook structure
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.9.0"
                },
                "toc": {
                    "base_numbering": 1,
                    "nav_menu": {},
                    "number_sections": True,
                    "sideBar": True,
                    "skip_h1_title": False,
                    "title_cell": "Table of Contents",
                    "title_sidebar": "Contents",
                    "toc_cell": False,
                    "toc_position": {},
                    "toc_section_display": True,
                    "toc_window_display": False
                },
                "created_by": "jupyter-notebook-manager",
                "created_at": datetime.now().isoformat(),
                "template_used": template,
            },
            "nbformat": NBFORMAT_VERSION,
            "nbformat_minor": NBFORMAT_MINOR
        }
        
        # Write to file
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created notebook: {output}")
        print(f"   Template: {template}")
        print(f"   Cells: {len(cells)}")
        
        return output
    
    # Template definitions
    
    def _create_cell(self, cell_type: str, source: List[str] or str, **kwargs) -> Dict:
        """Create a notebook cell."""
        if isinstance(source, str):
            source = source.split('\n')
        
        cell = {
            "cell_type": cell_type,
            "metadata": kwargs.get("metadata", {}),
            "source": source
        }
        
        if cell_type == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        
        return cell
    
    def _template_blank(self, **kwargs) -> List[Dict]:
        """Blank notebook with minimal structure."""
        title = kwargs.get('title', 'Untitled Notebook')
        author = kwargs.get('author', 'Data Scientist')
        
        return [
            self._create_cell("markdown", [
                f"# {title}\n",
                "\n",
                f"**Author**: {author}  \n",
                f"**Created**: {datetime.now().strftime('%Y-%m-%d')}  \n",
                "\n",
                "## Overview\n",
                "\n",
                "Brief description of this notebook's purpose.\n",
            ]),
            self._create_cell("code", ["# Import libraries\n"]),
        ]
    
    def _template_eda(self, **kwargs) -> List[Dict]:
        """Exploratory Data Analysis template."""
        title = kwargs.get('title', 'Exploratory Data Analysis')
        author = kwargs.get('author', 'Data Scientist')
        data_file = kwargs.get('data_file', 'data.csv')
        
        cells = [
            # Header
            self._create_cell("markdown", [
                f"# {title}\n",
                "\n",
                f"**Author**: {author}  \n",
                f"**Created**: {datetime.now().strftime('%Y-%m-%d')}  \n",
                f"**Data**: `{data_file}`  \n",
                "\n",
                "## Objective\n",
                "\n",
                "Perform comprehensive exploratory data analysis to understand:\n",
                "- Data structure and types\n",
                "- Distributions and patterns\n",
                "- Missing values and outliers\n",
                "- Relationships between variables\n",
            ]),
            
            # Imports
            self._create_cell("markdown", ["## 1. Setup and Imports\n"]),
            self._create_cell("code", [
                "# Core libraries\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from pathlib import Path\n",
                "import warnings\n",
                "\n",
                "# Configuration\n",
                "warnings.filterwarnings('ignore')\n",
                "pd.set_option('display.max_columns', None)\n",
                "pd.set_option('display.max_rows', 100)\n",
                "plt.style.use('seaborn-v0_8-darkgrid')\n",
                "sns.set_palette('husl')\n",
                "\n",
                "# Display settings\n",
                "%matplotlib inline\n",
                "%config InlineBackend.figure_format = 'retina'\n",
            ]),
            
            # Load data
            self._create_cell("markdown", ["## 2. Load Data\n"]),
            self._create_cell("code", [
                "# Load dataset\n",
                f"data_path = '{data_file}'\n",
                "df = pd.read_csv(data_path)\n",
                "\n",
                "print(f\"✅ Loaded {len(df):,} rows and {len(df.columns)} columns\")\n",
                "df.head()\n",
            ]),
            
            # Data overview
            self._create_cell("markdown", ["## 3. Data Overview\n"]),
            self._create_cell("code", [
                "# Basic information\n",
                "print(\"📊 Dataset Shape:\", df.shape)\n",
                "print(\"\\n📋 Column Names:\")\n",
                "print(df.columns.tolist())\n",
                "print(\"\\n🔢 Data Types:\")\n",
                "print(df.dtypes)\n",
                "print(\"\\n💾 Memory Usage:\")\n",
                "print(f\"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\")\n",
            ]),
            
            self._create_cell("code", [
                "# Statistical summary\n",
                "df.describe(include='all').T\n",
            ]),
            
            # Missing values
            self._create_cell("markdown", ["## 4. Missing Values Analysis\n"]),
            self._create_cell("code", [
                "# Missing values count\n",
                "missing = df.isnull().sum()\n",
                "missing_pct = (missing / len(df)) * 100\n",
                "missing_df = pd.DataFrame({\n",
                "    'Missing Count': missing,\n",
                "    'Percentage': missing_pct\n",
                "}).sort_values('Missing Count', ascending=False)\n",
                "\n",
                "print(\"🔍 Missing Values:\")\n",
                "print(missing_df[missing_df['Missing Count'] > 0])\n",
                "\n",
                "# Visualize\n",
                "if missing.sum() > 0:\n",
                "    plt.figure(figsize=(10, 6))\n",
                "    missing[missing > 0].plot(kind='barh')\n",
                "    plt.xlabel('Missing Count')\n",
                "    plt.title('Missing Values by Column')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
            ]),
            
            # Duplicates
            self._create_cell("markdown", ["## 5. Duplicate Analysis\n"]),
            self._create_cell("code", [
                "# Check duplicates\n",
                "duplicates = df.duplicated().sum()\n",
                "print(f\"🔄 Duplicate rows: {duplicates} ({duplicates/len(df)*100:.2f}%)\")\n",
                "\n",
                "if duplicates > 0:\n",
                "    print(\"\\n📌 Sample duplicate rows:\")\n",
                "    display(df[df.duplicated(keep=False)].head(10))\n",
            ]),
            
            # Distributions
            self._create_cell("markdown", ["## 6. Distribution Analysis\n"]),
            self._create_cell("code", [
                "# Numeric columns\n",
                "numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()\n",
                "print(f\"📈 Numeric columns ({len(numeric_cols)}): {numeric_cols}\")\n",
                "\n",
                "# Plot distributions\n",
                "if len(numeric_cols) > 0:\n",
                "    n_cols = min(4, len(numeric_cols))\n",
                "    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols\n",
                "    \n",
                "    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, n_rows*4))\n",
                "    axes = axes.flatten() if n_rows > 1 else [axes]\n",
                "    \n",
                "    for idx, col in enumerate(numeric_cols[:len(axes)]):\n",
                "        df[col].hist(bins=50, ax=axes[idx], edgecolor='black')\n",
                "        axes[idx].set_title(f'Distribution of {col}')\n",
                "        axes[idx].set_xlabel(col)\n",
                "        axes[idx].set_ylabel('Frequency')\n",
                "    \n",
                "    # Hide unused subplots\n",
                "    for idx in range(len(numeric_cols), len(axes)):\n",
                "        axes[idx].axis('off')\n",
                "    \n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
            ]),
            
            # Categorical analysis
            self._create_cell("markdown", ["## 7. Categorical Analysis\n"]),
            self._create_cell("code", [
                "# Categorical columns\n",
                "cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()\n",
                "print(f\"📝 Categorical columns ({len(cat_cols)}): {cat_cols}\")\n",
                "\n",
                "# Value counts for categorical columns\n",
                "for col in cat_cols[:5]:  # Show first 5\n",
                "    print(f\"\\n{'='*60}\")\n",
                "    print(f\"Column: {col}\")\n",
                "    print(f\"Unique values: {df[col].nunique()}\")\n",
                "    print(\"\\nTop 10 values:\")\n",
                "    print(df[col].value_counts().head(10))\n",
            ]),
            
            # Correlation analysis
            self._create_cell("markdown", ["## 8. Correlation Analysis\n"]),
            self._create_cell("code", [
                "# Correlation matrix\n",
                "if len(numeric_cols) > 1:\n",
                "    plt.figure(figsize=(12, 10))\n",
                "    corr_matrix = df[numeric_cols].corr()\n",
                "    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',\n",
                "                center=0, square=True, linewidths=1)\n",
                "    plt.title('Correlation Heatmap')\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "    \n",
                "    # High correlations\n",
                "    print(\"\\n🔗 High correlations (|r| > 0.7):\")\n",
                "    high_corr = []\n",
                "    for i in range(len(corr_matrix.columns)):\n",
                "        for j in range(i+1, len(corr_matrix.columns)):\n",
                "            if abs(corr_matrix.iloc[i, j]) > 0.7:\n",
                "                high_corr.append((\n",
                "                    corr_matrix.columns[i],\n",
                "                    corr_matrix.columns[j],\n",
                "                    corr_matrix.iloc[i, j]\n",
                "                ))\n",
                "    \n",
                "    if high_corr:\n",
                "        for col1, col2, corr in high_corr:\n",
                "            print(f\"  {col1} ↔ {col2}: {corr:.3f}\")\n",
                "    else:\n",
                "        print(\"  No high correlations found.\")\n",
            ]),
            
            # Outliers
            self._create_cell("markdown", ["## 9. Outlier Detection\n"]),
            self._create_cell("code", [
                "# Box plots for numeric columns\n",
                "if len(numeric_cols) > 0:\n",
                "    n_cols = min(4, len(numeric_cols))\n",
                "    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols\n",
                "    \n",
                "    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, n_rows*4))\n",
                "    axes = axes.flatten() if n_rows > 1 else [axes]\n",
                "    \n",
                "    for idx, col in enumerate(numeric_cols[:len(axes)]):\n",
                "        df.boxplot(column=col, ax=axes[idx])\n",
                "        axes[idx].set_title(f'Box Plot: {col}')\n",
                "    \n",
                "    # Hide unused subplots\n",
                "    for idx in range(len(numeric_cols), len(axes)):\n",
                "        axes[idx].axis('off')\n",
                "    \n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "# IQR method for outlier detection\n",
                "print(\"\\n📊 Outlier counts (IQR method):\")\n",
                "for col in numeric_cols:\n",
                "    Q1 = df[col].quantile(0.25)\n",
                "    Q3 = df[col].quantile(0.75)\n",
                "    IQR = Q3 - Q1\n",
                "    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()\n",
                "    if outliers > 0:\n",
                "        print(f\"  {col}: {outliers} outliers ({outliers/len(df)*100:.2f}%)\")\n",
            ]),
            
            # Summary
            self._create_cell("markdown", ["## 10. Key Findings\n"]),
            self._create_cell("markdown", [
                "### Summary\n",
                "\n",
                "Write your key findings here:\n",
                "\n",
                "1. **Data Quality**:\n",
                "   - \n",
                "\n",
                "2. **Distributions**:\n",
                "   - \n",
                "\n",
                "3. **Relationships**:\n",
                "   - \n",
                "\n",
                "4. **Anomalies**:\n",
                "   - \n",
                "\n",
                "### Next Steps\n",
                "\n",
                "1. \n",
                "2. \n",
                "3. \n",
            ]),
        ]
        
        return cells
    
    def _template_ml(self, **kwargs) -> List[Dict]:
        """Machine Learning template."""
        title = kwargs.get('title', 'Machine Learning Model Training')
        data_file = kwargs.get('data_file', 'data.csv')
        target = kwargs.get('target_column', 'target')
        
        cells = [
            self._create_cell("markdown", [
                f"# {title}\n",
                "\n",
                "## Objective\n",
                "\n",
                f"Train and evaluate machine learning models to predict `{target}`.\n",
            ]),
            
            self._create_cell("code", [
                "# Imports\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from sklearn.model_selection import train_test_split, cross_val_score\n",
                "from sklearn.preprocessing import StandardScaler, LabelEncoder\n",
                "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n",
                "from sklearn.linear_model import LogisticRegression\n",
                "from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score\n",
                "import warnings\n",
                "warnings.filterwarnings('ignore')\n",
            ]),
            
            self._create_cell("markdown", ["## 1. Load and Prepare Data\n"]),
            self._create_cell("code", [
                f"# Load data\n",
                f"df = pd.read_csv('{data_file}')\n",
                f"target_col = '{target}'\n",
                "\n",
                "print(f\"Dataset shape: {df.shape}\")\n",
                "print(f\"Target distribution:\\n{df[target_col].value_counts()}\")\n",
            ]),
            
            self._create_cell("markdown", ["## 2. Feature Engineering\n"]),
            self._create_cell("code", [
                "# TODO: Add feature engineering steps\n",
                "# Example: encoding, scaling, feature creation\n",
            ]),
            
            self._create_cell("markdown", ["## 3. Train-Test Split\n"]),
            self._create_cell("code", [
                "# Split data\n",
                f"X = df.drop(columns=[target_col])\n",
                f"y = df[target_col]\n",
                "\n",
                "X_train, X_test, y_train, y_test = train_test_split(\n",
                "    X, y, test_size=0.2, random_state=42, stratify=y\n",
                ")\n",
                "\n",
                "print(f\"Training set: {X_train.shape}\")\n",
                "print(f\"Test set: {X_test.shape}\")\n",
            ]),
            
            self._create_cell("markdown", ["## 4. Model Training\n"]),
            self._create_cell("code", [
                "# Train models\n",
                "models = {\n",
                "    'Logistic Regression': LogisticRegression(max_iter=1000),\n",
                "    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),\n",
                "    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)\n",
                "}\n",
                "\n",
                "results = {}\n",
                "for name, model in models.items():\n",
                "    model.fit(X_train, y_train)\n",
                "    train_score = model.score(X_train, y_train)\n",
                "    test_score = model.score(X_test, y_test)\n",
                "    results[name] = {'train': train_score, 'test': test_score}\n",
                "    print(f\"{name}: Train={train_score:.4f}, Test={test_score:.4f}\")\n",
            ]),
            
            self._create_cell("markdown", ["## 5. Model Evaluation\n"]),
            self._create_cell("code", [
                "# Evaluate best model\n",
                "# TODO: Select best model and evaluate in detail\n",
            ]),
        ]
        
        return cells
    
    def _template_cleaning(self, **kwargs) -> List[Dict]:
        """Data cleaning template."""
        title = kwargs.get('title', 'Data Cleaning')
        data_file = kwargs.get('data_file', 'data.csv')
        
        cells = [
            self._create_cell("markdown", [f"# {title}\n"]),
            self._create_cell("code", ["import pandas as pd\nimport numpy as np\n"]),
            self._create_cell("code", [f"df = pd.read_csv('{data_file}')\ndf.head()\n"]),
            self._create_cell("markdown", ["## 1. Handle Missing Values\n"]),
            self._create_cell("code", ["# TODO: Handle missing values\n"]),
            self._create_cell("markdown", ["## 2. Remove Duplicates\n"]),
            self._create_cell("code", ["# TODO: Remove duplicates\n"]),
            self._create_cell("markdown", ["## 3. Fix Data Types\n"]),
            self._create_cell("code", ["# TODO: Convert data types\n"]),
            self._create_cell("markdown", ["## 4. Handle Outliers\n"]),
            self._create_cell("code", ["# TODO: Treat outliers\n"]),
            self._create_cell("markdown", ["## 5. Save Cleaned Data\n"]),
            self._create_cell("code", ["# df.to_csv('cleaned_data.csv', index=False)\n"]),
        ]
        
        return cells
    
    def _template_timeseries(self, **kwargs) -> List[Dict]:
        """Time series analysis template."""
        return [
            self._create_cell("markdown", ["# Time Series Analysis\n"]),
            self._create_cell("code", ["import pandas as pd\nimport numpy as np\nfrom statsmodels.tsa.seasonal import seasonal_decompose\n"]),
        ]
    
    def _template_stats(self, **kwargs) -> List[Dict]:
        """Statistical testing template."""
        return [
            self._create_cell("markdown", ["# Statistical Testing\n"]),
            self._create_cell("code", ["import pandas as pd\nimport numpy as np\nfrom scipy import stats\n"]),
        ]
    
    def _template_viz(self, **kwargs) -> List[Dict]:
        """Visualization dashboard template."""
        return [
            self._create_cell("markdown", ["# Visualization Dashboard\n"]),
            self._create_cell("code", ["import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n"]),
        ]


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(description="Create Jupyter notebooks from templates")
    parser.add_argument("--template", default="blank", help="Template name")
    parser.add_argument("--output", default="notebook.ipynb", help="Output path")
    parser.add_argument("--title", default="Untitled", help="Notebook title")
    parser.add_argument("--author", default="Data Scientist", help="Author name")
    parser.add_argument("--data-file", help="Data file path")
    parser.add_argument("--target-column", help="Target variable (for ML)")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    
    args = parser.parse_args()
    
    creator = NotebookCreator()
    
    if args.list_templates:
        print("Available templates:")
        for name in creator.templates.keys():
            print(f"  - {name}")
        return
    
    creator.create_notebook(
        template=args.template,
        output_path=args.output,
        title=args.title,
        author=args.author,
        data_file=args.data_file,
        target_column=args.target_column,
    )


if __name__ == "__main__":
    main()
