# HeteroMind Comprehensive Test Report

**Generated:** 2026-04-12 17:42:50
**Model:** deepseek-chat

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | 8 |
| Passed | 8 ✅ |
| Failed | 0 ❌ |
| **Overall Accuracy** | **100.0%** |
| Avg Confidence | 0.64 |
| Avg Response Time | 25246ms |

## Results by Engine

| Engine | Tests | Passed | Accuracy | Avg Confidence | Avg Time |
|--------|-------|--------|----------|----------------|----------|
| SQL | 3 | 3 | 100.0% | 0.60 | 21421ms |
| SPARQL | 2 | 2 | 100.0% | 0.72 | 37752ms |
| TableQA | 3 | 3 | 100.0% | 0.62 | 20735ms |

## Detailed Results

### SQL-001 - ✅ PASS

**Query:** How many employees are in the Engineering department?

**Engine:** SQL

**Confidence:** 0.60

**Execution Time:** 25618ms

**Generated Query:**
```
SELECT COUNT(*) 
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE d.name = 'Engineering';
```

### SQL-002 - ✅ PASS

**Query:** 按部门统计每个部门的平均薪资，并显示薪资最高的前 3 个部门

**Engine:** SQL

**Confidence:** 0.60

**Execution Time:** 22919ms

**Generated Query:**
```
SELECT 
    d.name AS department_name,
    AVG(e.salary) AS average_salary
FROM 
    departments d
JOIN 
    employees e ON d.id = e.department_id
GROUP BY 
    d.id, d.name
ORDER BY 
    average_salary DESC
LIMIT 3;
```

### SQL-003 - ✅ PASS

**Query:** List all employees hired after 2020

**Engine:** SQL

**Confidence:** 0.60

**Execution Time:** 15727ms

**Generated Query:**
```
SELECT * FROM employees WHERE hire_date > '2020-12-31';
```

### KG-001 - ✅ PASS

**Query:** Who is the founder of Microsoft?

**Engine:** SPARQL

**Confidence:** 0.60

**Execution Time:** 27886ms

**Generated Query:**
```
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?founder WHERE {
    dbr:Microsoft dbo:founder ?founder .
}
```

### KG-002 - ✅ PASS

**Query:** What companies are headquartered in Seattle?

**Engine:** SPARQL

**Confidence:** 0.85

**Execution Time:** 47618ms

**Generated Query:**
```
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?company ?companyLabel WHERE {
  ?company rdf:type dbo:Company ;
           dbo:headquarter dbr:Seattle ;
           rdfs:label ?companyLabel .
  FILTER(LANG(?companyLabel) = "en")
}
```

### TQ-001 - ✅ PASS

**Query:** 2024 年哪个季度的销售额最高？

**Engine:** TableQA

**Confidence:** 0.50

**Execution Time:** 25327ms

**Generated Query:**
```
import pandas as pd

# Filter data for year 2024
df_2024 = df[df['year'] == 2024]

# Group by quarter and calculate total sales per quarter
quarterly_sales = df_2024.groupby('quarter')['sales'].sum().reset_index()

# Find the quarter with the maximum sales
max_sales_quarter = quarterly_sales.loc[quarterly_sales['sales'].idxmax()]

print(max_sales_quarter['quarter'])
```

### TQ-002 - ✅ PASS

**Query:** What is the average sales per quarter?

**Engine:** TableQA

**Confidence:** 0.85

**Execution Time:** 23538ms

**Generated Query:**
```
import pandas as pd

# Calculate average sales per quarter
result = df.groupby('quarter')['sales'].mean().reset_index()
result.columns = ['quarter', 'average_sales']
print(result)
```

### TQ-003-UNKNOWN [UNKNOWN SOURCE] - ✅ PASS

**Query:** 根据提供的表格，计算总销售额

**Engine:** TableQA

**Confidence:** 0.50

**Execution Time:** 13339ms

**Generated Query:**
```
total_sales = df['sales'].sum()
print(total_sales)
```

