---
name: jupyter-notebook-manager
version: 1.0.0
author: AI Skills Community
description: Complete Jupyter notebook management system with creation, execution, debugging, and analysis capabilities
tags:
  - jupyter
  - data-science
  - python
  - notebook
  - analysis
category: data-science
requires:
  - jupyter
  - nbformat
  - nbconvert
  - pandas
trigger_keywords:
  - jupyter
  - notebook
  - ipynb
  - data analysis
  - create notebook
  - run notebook
  - debug notebook
  - execute notebook
  - analyze data
---

# Jupyter Notebook Manager

Complete Jupyter notebook management system that enables Claude to create, execute, debug, analyze, and optimize Jupyter notebooks with deep integration of data science workflows.

## 🎯 When to Use This Skill

### Trigger Conditions

Use this skill when you encounter:

1. **User mentions Jupyter-related keywords**:
   - "create a Jupyter notebook"
   - "run this notebook"
   - "debug my .ipynb file"
   - "analyze notebook results"
   - "optimize my notebook"

2. **User requests data analysis workflows**:
   - "set up data analysis pipeline"
   - "perform data cleaning"
   - "visualize analysis results"
   - "generate analysis report"

3. **User provides .ipynb files**:
   - Detecting .ipynb file references
   - User uploads notebook files
   - Working directory contains notebooks

4. **User needs notebook operations**:
   - "convert notebook to Python script"
   - "extract code from notebook"
   - "merge multiple notebooks"
   - "generate notebook template"

## 🚀 Core Capabilities

### 1. Notebook Creation & Templates

**When**: User needs to create new notebooks for specific analysis tasks

**Capabilities**:
- Generate notebooks from scratch with proper structure
- Provide domain-specific templates (EDA, ML, visualization)
- Add markdown documentation and code cells
- Configure kernel and metadata
- Support custom templates

**Example**:
```python
# User: "Create a data analysis notebook for sales data"
# → Generates structured notebook with:
#   - Import cells (pandas, numpy, matplotlib)
#   - Data loading section
#   - EDA section with common analyses
#   - Visualization section
#   - Summary section
```

### 2. Notebook Execution & Monitoring

**When**: User needs to run notebooks and track execution

**Capabilities**:
- Execute notebooks programmatically
- Monitor execution progress
- Capture outputs and errors
- Handle long-running cells
- Support parameterized execution

**Example**:
```python
# User: "Run analysis.ipynb with dataset=sales_2024.csv"
# → Executes notebook with parameters
# → Shows real-time progress
# → Captures all outputs
# → Reports execution time and status
```

### 3. Debugging & Error Analysis

**When**: Notebook execution fails or produces unexpected results

**Capabilities**:
- Identify error cells and stack traces
- Analyze variable states at error points
- Suggest fixes for common issues
- Detect dependency problems
- Check data quality issues

**Example**:
```python
# User: "My notebook fails at cell 5"
# → Analyzes error traceback
# → Checks variable values before error
# → Identifies root cause (e.g., missing column)
# → Suggests fix with corrected code
```

### 4. Variable Inspection & State Analysis

**When**: User needs to understand notebook state and variables

**Capabilities**:
- Extract all variables and their types
- Show dataframe summaries
- Visualize data distributions
- Track variable flow across cells
- Detect unused variables

**Example**:
```python
# User: "What variables are defined in this notebook?"
# → Lists all variables with types
# → Shows dataframe shapes and dtypes
# → Displays memory usage
# → Highlights key variables
```

### 5. Code Quality & Optimization

**When**: User wants to improve notebook code

**Capabilities**:
- Detect code smells and anti-patterns
- Suggest performance improvements
- Identify redundant computations
- Recommend vectorization
- Check PEP 8 compliance

**Example**:
```python
# User: "Optimize my data processing notebook"
# → Identifies slow loops that can be vectorized
# → Suggests caching for expensive operations
# → Recommends better pandas operations
# → Provides optimized code snippets
```

### 6. Notebook Conversion & Export

**When**: User needs different formats or want to modularize code

**Capabilities**:
- Convert notebook to Python script
- Export to HTML/PDF/Markdown
- Extract functions for reuse
- Generate documentation
- Create clean code modules

**Example**:
```python
# User: "Convert my notebook to a Python module"
# → Extracts all function definitions
# → Creates proper module structure
# → Adds docstrings
# → Generates import-ready .py file
```

### 7. Results Visualization & Reporting

**When**: User needs to present or summarize notebook results

**Capabilities**:
- Generate executive summaries
- Create result dashboards
- Extract key findings
- Compile visualizations
- Format output reports

**Example**:
```python
# User: "Summarize the results from my analysis notebook"
# → Extracts all plots and tables
# → Identifies key metrics and insights
# → Generates markdown report
# → Includes data quality notes
```

### 8. Collaborative Features

**When**: Multiple users work on notebooks

**Capabilities**:
- Compare notebook versions
- Merge notebook changes
- Generate diff reports
- Track cell modifications
- Resolve conflicts

**Example**:
```python
# User: "Compare my notebook with the previous version"
# → Shows cell-by-cell differences
# → Highlights output changes
# → Identifies new/deleted cells
# → Suggests conflict resolution
```

## 🛠️ Tool Integration

### Core Tools

1. **nbformat** - Notebook file I/O and manipulation
2. **nbconvert** - Format conversion and execution
3. **papermill** - Parameterized execution
4. **nbdime** - Notebook diffing and merging
5. **pandas** - Data manipulation and analysis
6. **matplotlib/seaborn** - Visualization
7. **jupyter_client** - Kernel management

### Script Integration

The skill includes these utility scripts:

- `scripts/notebook_creator.py` - Template-based notebook generation
- `scripts/notebook_executor.py` - Robust notebook execution
- `scripts/notebook_debugger.py` - Error analysis and debugging
- `scripts/notebook_analyzer.py` - Code quality and optimization
- `scripts/notebook_converter.py` - Format conversion utilities
- `scripts/notebook_reporter.py` - Results extraction and reporting

## 📋 Workflow Examples

### Workflow 1: Create and Run Analysis

```markdown
User: "Create a sales analysis notebook and run it with Q4_sales.csv"

Step 1: Generate Template
→ Call notebook_creator.py with "sales-analysis" template
→ Customize for Q4 data

Step 2: Configure Parameters
→ Set data_file = "Q4_sales.csv"
→ Set analysis_type = "quarterly"

Step 3: Execute Notebook
→ Call notebook_executor.py
→ Monitor progress (show cell N/M)

Step 4: Report Results
→ Extract key metrics
→ Show visualizations
→ Summarize findings
```

### Workflow 2: Debug Failed Notebook

```markdown
User: "My notebook analysis.ipynb crashes at cell 10"

Step 1: Identify Error
→ Parse notebook with nbformat
→ Find cell 10 and error traceback

Step 2: Analyze Context
→ Check variables in cells 1-9
→ Identify dataframe state before error

Step 3: Diagnose Issue
→ Analyze error message
→ Check for common issues (missing columns, type errors, etc.)

Step 4: Suggest Fix
→ Provide corrected code
→ Explain root cause
→ Offer prevention tips
```

### Workflow 3: Optimize Slow Notebook

```markdown
User: "This notebook takes 10 minutes to run, can you optimize it?"

Step 1: Profile Execution
→ Run with timing enabled
→ Identify slow cells

Step 2: Analyze Code
→ Detect inefficient patterns
→ Find opportunities for vectorization

Step 3: Suggest Improvements
→ Show optimized code versions
→ Estimate speed improvements

Step 4: Validate
→ Test optimized notebook
→ Verify outputs match original
```

## 🎓 Best Practices

### Notebook Structure

1. **Start with imports and configuration**
   - Group all imports at top
   - Set display options early
   - Configure logging

2. **Use markdown for documentation**
   - Section headers with ##
   - Explain analysis steps
   - Document assumptions

3. **Modular code cells**
   - One logical operation per cell
   - Avoid overly long cells
   - Keep cell outputs manageable

4. **Clear variable naming**
   - Use descriptive names
   - Follow naming conventions
   - Avoid single-letter variables (except i, j, k)

### Code Quality

1. **Avoid loops when vectorization possible**
   ```python
   # Bad
   for i in range(len(df)):
       df.loc[i, 'new_col'] = df.loc[i, 'a'] + df.loc[i, 'b']
   
   # Good
   df['new_col'] = df['a'] + df['b']
   ```

2. **Cache expensive computations**
   ```python
   # Check if already computed
   if not os.path.exists('cached_result.pkl'):
       result = expensive_computation()
       result.to_pickle('cached_result.pkl')
   else:
       result = pd.read_pickle('cached_result.pkl')
   ```

3. **Handle errors gracefully**
   ```python
   try:
       df = pd.read_csv('data.csv')
   except FileNotFoundError:
       print("⚠️ Data file not found, using sample data")
       df = generate_sample_data()
   ```

### Performance Tips

1. **Use appropriate data types**
   - Convert to categorical for low-cardinality strings
   - Use int32 instead of int64 when possible
   - Leverage datetime types

2. **Process data in chunks for large files**
   ```python
   chunks = pd.read_csv('large_file.csv', chunksize=10000)
   result = pd.concat([process(chunk) for chunk in chunks])
   ```

3. **Leverage pandas built-in functions**
   - Use `query()` for filtering
   - Use `eval()` for expressions
   - Use `pipe()` for chaining

## 🔍 Error Patterns and Solutions

### Common Issues

| Error Pattern | Cause | Solution |
|--------------|-------|----------|
| `KeyError: 'column_name'` | Column doesn't exist | Check `df.columns`, verify spelling |
| `SettingWithCopyWarning` | Chained assignment | Use `.loc[]` or `.copy()` |
| `MemoryError` | Dataset too large | Process in chunks or use dask |
| `ModuleNotFoundError` | Missing package | Add to requirements, install in kernel |
| `KernelDead` | Out of memory or crash | Restart kernel, reduce data size |

### Debugging Checklist

```python
# 1. Check data loading
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Dtypes:\n{df.dtypes}")

# 2. Check for missing values
print(f"Missing values:\n{df.isnull().sum()}")

# 3. Check data types
print(f"Object columns: {df.select_dtypes('object').columns.tolist()}")

# 4. Check memory usage
print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# 5. Check for duplicates
print(f"Duplicates: {df.duplicated().sum()}")
```

## 📊 Template Library

### Available Templates

1. **exploratory-data-analysis** - Comprehensive EDA workflow
2. **machine-learning-training** - ML model development pipeline
3. **time-series-analysis** - Time series forecasting
4. **data-cleaning** - Data quality and cleaning
5. **statistical-testing** - Hypothesis testing and statistics
6. **visualization-dashboard** - Interactive visualizations
7. **data-pipeline** - ETL and data transformation
8. **report-generation** - Automated reporting

### Template Usage

```bash
# Create notebook from template
python scripts/notebook_creator.py \
  --template exploratory-data-analysis \
  --output eda_analysis.ipynb \
  --data-file sales_data.csv \
  --target-column revenue
```

## 🔗 Integration Points

### With Other Skills

- **pandas-data-wrangler**: Data manipulation operations
- **matplotlib-plotter**: Advanced visualizations
- **ml-model-trainer**: Model training and evaluation
- **data-pipeline-builder**: ETL workflows

### With External Tools

- **Jupyter Lab/Notebook**: Interactive development
- **VS Code**: Notebook editing and debugging
- **Papermill**: Batch execution and parameterization
- **nbconvert**: Publishing and sharing
- **git**: Version control (with nbstripout)

## 🎯 Success Criteria

A successful skill invocation should:

✅ Understand user's notebook-related intent  
✅ Select appropriate operation (create/run/debug/optimize)  
✅ Execute operation with proper error handling  
✅ Provide clear progress updates  
✅ Return actionable results or insights  
✅ Offer next steps or improvements  
✅ Handle edge cases gracefully  

## 📚 Resources

### Documentation Links

- [Jupyter Documentation](https://jupyter.org/documentation)
- [nbformat Specification](https://nbformat.readthedocs.io/)
- [nbconvert Guide](https://nbconvert.readthedocs.io/)
- [Papermill Documentation](https://papermill.readthedocs.io/)

### Example Notebooks

See `examples/` directory for:
- Sample analysis notebooks
- Template demonstrations
- Use case tutorials
- Best practice examples

## 🚨 Limitations

1. **Kernel Management**: Cannot directly interact with running kernels (use scripts)
2. **Interactive Widgets**: Limited support for ipywidgets
3. **Long-Running**: Very long computations (>10 min) may timeout
4. **GPU Operations**: No direct GPU kernel access
5. **Large Files**: Memory constraints for very large notebooks (>100MB)

## 📝 Notes

- Always validate notebook structure before execution
- Use timeouts to prevent hanging on infinite loops
- Sanitize user inputs in parameterized execution
- Consider notebook size when extracting outputs
- Test scripts with various notebook formats
- Maintain compatibility with Jupyter 4.x and 5.x formats

---

**Version**: 1.0.0  
**Last Updated**: 2026-04-16  
**Maintainer**: AI Skills Community
