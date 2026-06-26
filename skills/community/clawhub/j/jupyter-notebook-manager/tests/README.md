# Jupyter Notebook Manager - Test Suite

This directory contains comprehensive test cases for the jupyter-notebook-manager skill.

## Test Structure

```
tests/
├── README.md (this file)
├── test_creator.py          # Unit tests for notebook_creator.py
├── test_executor.py          # Unit tests for notebook_executor.py
├── test_integration.py       # Integration tests
├── test_scenarios/           # Real-world scenario tests
│   ├── scenario_01_eda.md
│   ├── scenario_02_ml.md
│   ├── scenario_03_debug.md
│   └── scenario_04_optimize.md
└── fixtures/                 # Test data and notebooks
    ├── sample_data.csv
    ├── simple_notebook.ipynb
    ├── error_notebook.ipynb
    └── large_notebook.ipynb
```

## Test Categories

### 1. Unit Tests

**Purpose**: Test individual functions and methods

- `test_creator.py`: Notebook creation logic
  - Template loading
  - Cell generation
  - Metadata handling
  - Custom cell injection

- `test_executor.py`: Notebook execution logic
  - Execution flow
  - Parameter injection
  - Error capture
  - Output extraction

### 2. Integration Tests

**Purpose**: Test end-to-end workflows

- `test_integration.py`:
  - Create → Execute workflow
  - Execute → Analyze workflow
  - Multi-step operations

### 3. Scenario Tests

**Purpose**: Test real-world use cases

- **Scenario 1: Exploratory Data Analysis**
  - User provides CSV file
  - Create EDA notebook
  - Execute and analyze results
  - Validate output quality

- **Scenario 2: Machine Learning Pipeline**
  - User requests ML model training
  - Create ML notebook
  - Execute with different parameters
  - Compare model performances

- **Scenario 3: Debugging Failed Notebook**
  - User reports notebook error
  - Identify error cell
  - Analyze error cause
  - Suggest fix

- **Scenario 4: Notebook Optimization**
  - User complains about slow execution
  - Profile notebook performance
  - Identify bottlenecks
  - Provide optimized version

## Test Data

### Sample Datasets

1. **sample_data.csv** - Clean dataset for testing
   - 1000 rows, 10 columns
   - Mix of numeric and categorical
   - No missing values
   - Known patterns for validation

2. **messy_data.csv** - Dirty dataset for cleaning tests
   - Missing values (20%)
   - Duplicates (5%)
   - Outliers
   - Type inconsistencies

3. **large_data.csv** - Performance testing
   - 100,000 rows
   - Memory stress test
   - Optimization opportunities

### Test Notebooks

1. **simple_notebook.ipynb** - Basic operations
   - Simple calculations
   - Quick execution (<5s)
   - All cells succeed

2. **error_notebook.ipynb** - Error scenarios
   - Cell 5 has KeyError
   - Cell 8 has TypeError
   - Tests error handling

3. **long_running_notebook.ipynb** - Timeout testing
   - Has sleep(60) call
   - Tests timeout handling

4. **large_notebook.ipynb** - Scale testing
   - 100+ cells
   - Large outputs
   - Tests memory handling

## Running Tests

### Quick Test

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_creator.py -v

# Run with coverage
python -m pytest tests/ --cov=scripts --cov-report=html
```

### Scenario Tests

```bash
# Run scenario 1: EDA
python tests/run_scenario.py --scenario eda

# Run scenario 2: ML
python tests/run_scenario.py --scenario ml

# Run all scenarios
python tests/run_scenario.py --all
```

## Test Coverage Goals

- **Code Coverage**: >80%
- **Branch Coverage**: >70%
- **Scenario Coverage**: 100% of documented use cases

## Expected Test Results

### Success Criteria

✅ All unit tests pass  
✅ All integration tests pass  
✅ At least 4 scenario tests pass  
✅ No critical bugs found  
✅ Performance within acceptable range (<10s for simple notebooks)  

### Known Issues

- ⚠️ Timeout tests may be flaky on slow machines
- ⚠️ Large notebook tests require >2GB RAM
- ⚠️ Some matplotlib tests may fail in headless environments

## Test Maintenance

### Adding New Tests

1. Identify the feature/bug to test
2. Create test case in appropriate file
3. Add test data if needed
4. Document expected behavior
5. Update this README

### Updating Tests

When modifying scripts, update corresponding tests:

```python
# Before: Old behavior
assert result == expected_old

# After: New behavior  
assert result == expected_new
```

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/test.yml
name: Test Jupyter Notebook Manager
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ -v --cov=scripts
```

## Troubleshooting

### Common Test Failures

**Issue**: ImportError for nbformat
```bash
# Solution
pip install nbformat nbconvert jupyter
```

**Issue**: Timeout in executor tests
```bash
# Solution: Increase timeout
pytest tests/test_executor.py --timeout=300
```

**Issue**: Display issues in viz tests
```bash
# Solution: Use headless backend
export MPLBACKEND=Agg
pytest tests/
```

## Test Metrics

Track these metrics over time:

- Test execution time
- Coverage percentage
- Number of flaky tests
- Bug detection rate

---

**Last Updated**: 2026-04-16  
**Maintained By**: AI Skills Community
