# HeteroMind Test Suite

## Overview

This test suite validates the HeteroMind heterogeneous knowledge QA system across:
- **Multiple Languages**: Chinese (中文), English
- **Multiple Knowledge Sources**: SQL, SPARQL/KG, Table/CSV
- **Unknown Source Handling**: Tests panics with unspecified knowledge sources

## Test Cases Summary

| ID | Language | Source | Description |
|----|----------|--------|-------------|
| SQL-001 | English | SQL | Count employees in department |
| SQL-002 | Chinese | SQL | GROUP BY + AVG + ORDER BY + LIMIT |
| SQL-003 | English | SQL | Filter by date |
| KG-001 | English | SPARQL | Entity lookup (founder) |
| KG-002 | English | SPARQL | Entity lookup (headquarters) |
| TQ-001 | Chinese | Table | Find max sales by quarter |
| TQ-002 | English | Table | Calculate average |
| TQ-003-UNKNOWN | Chinese | Table | Unknown source test |

## Running Tests

### Prerequisites

```bash
pip install pandas openpyxl aiohttp
```

### Run All Tests (Recommended)

```bash
cd ~/Documents/openclaw/workspace/HeteroMind
python3 comprehensive_tests.py
```

This will:
- Test all 3 engines (SQL, SPARQL, TableQA)
- Run 8 test cases total
- Generate detailed reports:
  - `tests/comprehensive_test_results.json` - JSON format results
  - `tests/comprehensive_test_report.md` - Markdown format report

## Test Data

Located in `tests/test_data/`:

| File | Description |
|------|-------------|
| `company_db_schema.json` | SQL database schema |
| `sales_quarterly.csv` | Sample sales data (32 rows) |
| `kg_ontology.json` | Knowledge graph ontology |

## Evaluation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Source Detection Accuracy | >90% | Correctly identifies knowledge source |
| Query Generation | >95% | Generates syntactically correct query |
| Execution Success | >90% | Query executes without error |
| Answer Accuracy | >80% | Answer matches expected result |

## Adding New Test Cases

Edit `comprehensive_tests.py` and add to the appropriate test case list:

```python
SQL_TEST_CASES = [
    {
        "id": "SQL-004",
        "query": "Your new query",
        "language": "en",
        "expected_sql": "Expected SQL pattern",
        "expected_tables": ["table1", "table2"],
    },
]
```

## Troubleshooting

### Test Fails with "No module named 'engines'"
```bash
# Ensure you're running from the HeteroMind directory
cd ~/Documents/openclaw/workspace/HeteroMind
```

### LLM Tests Fail Without API Key
```bash
# The test uses DeepSeek API by default
# Check DEEPSEEK_API_KEY in comprehensive_tests.py
```

## Contact

For questions or issues, please open a GitHub issue.
