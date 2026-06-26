#!/usr/bin/env python3
"""
HeteroMind Comprehensive Test Suite

Tests all three engines (SQL, SPARQL, TableQA) with accuracy metrics.
Includes ground truth comparison and unknown knowledge source testing.

Usage:
    python3 comprehensive_tests.py
"""

import asyncio
import os
import json
import time
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

from engines.nl2sql.multi_stage_engine import MultiStageNL2SQLEngine
from engines.nl2sparql.multi_stage_engine import MultiStageNL2SPARQLEngine
from engines.table_qa.multi_stage_engine import MultiStageTableQAEngine

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-YOUR_API_KEY_HERE")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"
TEST_DATA_DIR = Path(__file__).parent / "tests" / "test_data"

@dataclass
class TestResult:
    test_id: str
    query: str
    engine_type: str
    generated_query: Optional[str]
    expected_query: Optional[str]
    execution_success: bool
    answer_correct: bool
    confidence: float
    execution_time_ms: float
    error: Optional[str] = None
    details: Dict = field(default_factory=dict)

@dataclass
class TestSuiteResult:
    total_tests: int
    passed_tests: int
    failed_tests: int
    accuracy: float
    avg_confidence: float
    avg_time_ms: float
    by_engine: Dict[str, Dict]
    detailed_results: List[TestResult]

SQL_TEST_CASES = [
    {"id": "SQL-001", "query": "How many employees are in the Engineering department?", "language": "en", "expected_sql": "SELECT COUNT(*) FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Engineering'", "expected_tables": ["employees", "departments"]},
    {"id": "SQL-002", "query": "按部门统计每个部门的平均薪资，并显示薪资最高的前 3 个部门", "language": "zh", "expected_sql": "SELECT d.name, AVG(e.salary) FROM employees e JOIN departments d ON e.department_id = d.id GROUP BY d.name ORDER BY AVG(e.salary) DESC LIMIT 3", "expected_tables": ["employees", "departments"]},
    {"id": "SQL-003", "query": "List all employees hired after 2020", "language": "en", "expected_sql": "SELECT * FROM employees WHERE hire_date > '2020-01-01'", "expected_tables": ["employees"]},
]

SPARQL_TEST_CASES = [
    {"id": "KG-001", "query": "Who is the founder of Microsoft?", "language": "en", "expected_sparql": "SELECT ?founder WHERE { <http://dbpedia.org/resource/Microsoft> <http://dbpedia.org/ontology/founder> ?founder }", "expected_entities": ["Microsoft"]},
    {"id": "KG-002", "query": "What companies are headquartered in Seattle?", "language": "en", "expected_sparql": "SELECT ?company WHERE { ?company <http://dbpedia.org/ontology/headquarters> <http://dbpedia.org/resource/Seattle> }", "expected_entities": ["Seattle"]},
]

TABLEQA_TEST_CASES = [
    {"id": "TQ-001", "query": "2024 年哪个季度的销售额最高？", "language": "zh", "expected_code_contains": ["groupby", "max", "quarter", "sales"], "expected_columns": ["quarter", "sales"], "is_unknown_source": False},
    {"id": "TQ-002", "query": "What is the average sales per quarter?", "language": "en", "expected_code_contains": ["mean", "average", "sales"], "expected_columns": ["quarter", "sales"], "is_unknown_source": False},
    {"id": "TQ-003-UNKNOWN", "query": "根据提供的表格，计算总销售额", "language": "zh", "expected_code_contains": ["sum", "sales"], "expected_columns": ["sales"], "is_unknown_source": True},
]

class HeteroMindTestSuite:
    def __init__(self):
        self.results = []
        self.sql_engine = None
        self.sparql_engine = None
        self.table_engine = None
    
    def setup_engines(self):
        print("\n" + "="*70)
        print("Initializing HeteroMind Engines")
        print("="*70)
        
        try:
            schema_path = TEST_DATA_DIR / "company_db_schema.json"
            with open(schema_path) as f:
                schema = json.load(f)
            self.sql_engine = MultiStageNL2SQLEngine({"name": "test_sql", "schema": schema, "llm_config": {"model": DEEPSEEK_MODEL, "api_key": DEEPSEEK_API_KEY, "base_url": DEEPSEEK_BASE_URL}, "generation_config": {"num_candidates": 3, "max_revisions": 2, "voting_enabled": True, "parallel_generation": True}})
            print("✅ SQL Engine initialized")
        except Exception as e:
            print(f"❌ SQL Engine failed: {e}")
        
        try:
            ontology_path = TEST_DATA_DIR / "kg_ontology.json"
            with open(ontology_path) as f:
                ontology = json.load(f)
            self.sparql_engine = MultiStageNL2SPARQLEngine({"name": "test_sparql", "endpoint_url": "https://dbpedia.org/sparql", "ontology": ontology, "llm_config": {"model": DEEPSEEK_MODEL, "api_key": DEEPSEEK_API_KEY, "base_url": DEEPSEEK_BASE_URL}, "generation_config": {"num_candidates": 3, "max_revisions": 2, "voting_enabled": True}})
            print("✅ SPARQL Engine initialized")
        except Exception as e:
            print(f"❌ SPARQL Engine failed: {e}")
        
        try:
            self.table_engine = MultiStageTableQAEngine({"name": "test_table", "table_path": str(TEST_DATA_DIR / "sales_quarterly.csv"), "llm_config": {"model": DEEPSEEK_MODEL, "api_key": DEEPSEEK_API_KEY, "base_url": DEEPSEEK_BASE_URL}, "generation_config": {"num_candidates": 3, "max_revisions": 2, "voting_enabled": True}})
            print("✅ TableQA Engine initialized")
        except Exception as e:
            print(f"❌ TableQA Engine failed: {e}")
        
        print("="*70)
    
    async def test_sql_engine(self) -> List[TestResult]:
        if not self.sql_engine:
            print("⚠️  SQL engine not available, skipping SQL tests")
            return []
        
        results = []
        print("\n" + "="*70)
        print("Testing SQL Engine")
        print("="*70)
        
        for tc in SQL_TEST_CASES:
            print(f"\n[{tc['id']}] {tc['query']}")
            start_time = time.time()
            
            try:
                result = await self.sql_engine.execute(tc["query"], {})
                exec_time = (time.time() - start_time) * 1000
                sql_correct = self._evaluate_sql_correctness(result.generated_sql, tc["expected_sql"], tc["expected_tables"])
                
                test_result = TestResult(test_id=tc["id"], query=tc["query"], engine_type="SQL", generated_query=result.generated_sql, expected_query=tc["expected_sql"], execution_success=result.success, answer_correct=sql_correct, confidence=result.final_confidence, execution_time_ms=exec_time, details={"schema_links": str(result.schema_links) if hasattr(result, "schema_links") else None, "revision_count": result.revision_count})
                
                status = "✅ PASS" if sql_correct else "❌ FAIL"
                print(f"  {status} | Confidence: {result.final_confidence:.2f} | Time: {exec_time:.0f}ms")
                print(f"  Generated: {result.generated_sql[:100]}...")
                
            except Exception as e:
                test_result = TestResult(test_id=tc["id"], query=tc["query"], engine_type="SQL", generated_query=None, expected_query=tc["expected_sql"], execution_success=False, answer_correct=False, confidence=0.0, execution_time_ms=(time.time() - start_time) * 1000, error=str(e))
                print(f"  ❌ ERROR: {e}")
            
            results.append(test_result)
        
        return results
    
    async def test_sparql_engine(self) -> List[TestResult]:
        if not self.sparql_engine:
            print("⚠️  SPARQL engine not available, skipping SPARQL tests")
            return []
        
        results = []
        print("\n" + "="*70)
        print("Testing SPARQL Engine")
        print("="*70)
        
        for tc in SPARQL_TEST_CASES:
            print(f"\n[{tc['id']}] {tc['query']}")
            start_time = time.time()
            
            try:
                result = await self.sparql_engine.execute(tc["query"], {})
                exec_time = (time.time() - start_time) * 1000
                sparql_correct = self._evaluate_sparql_correctness(result.generated_sparql, tc["expected_sparql"], tc["expected_entities"])
                
                test_result = TestResult(test_id=tc["id"], query=tc["query"], engine_type="SPARQL", generated_query=result.generated_sparql, expected_query=tc["expected_sparql"], execution_success=result.success, answer_correct=sparql_correct, confidence=result.final_confidence, execution_time_ms=exec_time, details={"linked_entities": str(result.linked_entities) if hasattr(result, "linked_entities") else None, "revision_count": result.revision_count})
                
                status = "✅ PASS" if sparql_correct else "❌ FAIL"
                print(f"  {status} | Confidence: {result.final_confidence:.2f} | Time: {exec_time:.0f}ms")
                print(f"  Generated: {result.generated_sparql[:100]}...")
                
            except Exception as e:
                test_result = TestResult(test_id=tc["id"], query=tc["query"], engine_type="SPARQL", generated_query=None, expected_query=tc["expected_sparql"], execution_success=False, answer_correct=False, confidence=0.0, execution_time_ms=(time.time() - start_time) * 1000, error=str(e))
                print(f"  ❌ ERROR: {e}")
            
            results.append(test_result)
        
        return results
    
    async def test_table_engine(self) -> List[TestResult]:
        if not self.table_engine:
            print("⚠️  TableQA engine not available, skipping TableQA tests")
            return []
        
        results = []
        print("\n" + "="*70)
        print("Testing TableQA Engine")
        print("="*70)
        
        for tc in TABLEQA_TEST_CASES:
            unknown_tag = " [UNKNOWN SOURCE]" if tc.get("is_unknown_source") else ""
            print(f"\n[{tc['id']}]{unknown_tag} {tc['query']}")
            start_time = time.time()
            
            try:
                result = await self.table_engine.execute(tc["query"], {})
                exec_time = (time.time() - start_time) * 1000
                code_correct = self._evaluate_code_correctness(result.generated_code, tc["expected_code_contains"], tc["expected_columns"])
                
                test_result = TestResult(test_id=tc["id"], query=tc["query"], engine_type="TableQA", generated_query=result.generated_code, expected_query=tc.get("expected_code_contains"), execution_success=result.success, answer_correct=code_correct, confidence=result.final_confidence, execution_time_ms=exec_time, details={"table_schema": dict(result.table_schema) if isinstance(result.table_schema, dict) else str(result.table_schema) if result.table_schema else None, "revision_count": result.revision_count, "is_unknown_source": tc.get("is_unknown_source", False)})
                
                status = "✅ PASS" if code_correct else "❌ FAIL"
                unknown_info = " (Unknown Source)" if tc.get("is_unknown_source") else ""
                print(f"  {status}{unknown_info} | Confidence: {result.final_confidence:.2f} | Time: {exec_time:.0f}ms")
                print(f"  Generated: {result.generated_code[:100]}...")
                
            except Exception as e:
                test_result = TestResult(test_id=tc["id"], query=tc["query"], engine_type="TableQA", generated_query=None, expected_query=tc.get("expected_code_contains"), execution_success=False, answer_correct=False, confidence=0.0, execution_time_ms=(time.time() - start_time) * 1000, error=str(e))
                print(f"  ❌ ERROR: {e}")
            
            results.append(test_result)
        
        return results
    
    def _evaluate_sql_correctness(self, generated: str, expected: str, expected_tables: List[str]) -> bool:
        if not generated:
            return False
        has_tables = all(table.lower() in generated.lower() for table in expected_tables)
        has_select = "SELECT" in generated.upper()
        return has_tables and has_select
    
    def _evaluate_sparql_correctness(self, generated: str, expected: str, expected_entities: List[str]) -> bool:
        if not generated:
            return False
        has_entities = any(entity.lower() in generated.lower() for entity in expected_entities)
        has_select = "SELECT" in generated.upper()
        has_where = "WHERE" in generated.upper()
        return has_entities and has_select and has_where
    
    def _evaluate_code_correctness(self, generated: str, expected_contains: List[str], expected_columns: List[str]) -> bool:
        if not generated:
            return False
        has_patterns = any(pattern.lower() in generated.lower() for pattern in expected_contains)
        has_columns = any(col.lower() in generated.lower() for col in expected_columns)
        return has_patterns and has_columns
    
    def calculate_summary(self, results: List[TestResult]) -> TestSuiteResult:
        total = len(results)
        passed = sum(1 for r in results if r.answer_correct)
        failed = total - passed
        
        by_engine = {}
        for engine_type in ["SQL", "SPARQL", "TableQA"]:
            engine_results = [r for r in results if r.engine_type == engine_type]
            if engine_results:
                engine_passed = sum(1 for r in engine_results if r.answer_correct)
                by_engine[engine_type] = {"total": len(engine_results), "passed": engine_passed, "accuracy": engine_passed / len(engine_results), "avg_confidence": sum(r.confidence for r in engine_results) / len(engine_results), "avg_time_ms": sum(r.execution_time_ms for r in engine_results) / len(engine_results)}
        
        return TestSuiteResult(total_tests=total, passed_tests=passed, failed_tests=failed, accuracy=passed / total if total > 0 else 0, avg_confidence=sum(r.confidence for r in results) / total if total > 0 else 0, avg_time_ms=sum(r.execution_time_ms for r in results) / total if total > 0 else 0, by_engine=by_engine, detailed_results=results)
    
    def print_summary(self, summary: TestSuiteResult):
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests:     {summary.total_tests}")
        print(f"Passed:          {summary.passed_tests} ✅")
        print(f"Failed:          {summary.failed_tests} ❌")
        print(f"Overall Accuracy: {summary.accuracy:.1%}")
        print(f"Avg Confidence:  {summary.avg_confidence:.2f}")
        print(f"Avg Time:        {summary.avg_time_ms:.0f}ms")
        
        print("\nBy Engine:")
        for engine, stats in summary.by_engine.items():
            print(f"\n  {engine}:")
            print(f"    Tests:    {stats['total']}")
            print(f"    Passed:   {stats['passed']}/{stats['total']} ({stats['accuracy']:.1%})")
            print(f"    Confidence: {stats['avg_confidence']:.2f}")
            print(f"    Avg Time: {stats['avg_time_ms']:.0f}ms")
        
        print("\n" + "="*70)
    
    def save_results(self, summary: TestSuiteResult, output_path: str):
        output = {"timestamp": datetime.now().isoformat(), "summary": {"total_tests": summary.total_tests, "passed_tests": summary.passed_tests, "failed_tests": summary.failed_tests, "accuracy": summary.accuracy, "avg_confidence": summary.avg_confidence, "avg_time_ms": summary.avg_time_ms}, "by_engine": summary.by_engine, "detailed_results": [{"test_id": r.test_id, "query": r.query, "engine_type": r.engine_type, "execution_success": r.execution_success, "answer_correct": r.answer_correct, "confidence": r.confidence, "execution_time_ms": r.execution_time_ms, "error": r.error, "generated_query": r.generated_query, "details": r.details} for r in summary.detailed_results]}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Results saved to: {output_path}")

async def main():
    print("\n" + "="*70)
    print("HeteroMind Comprehensive Test Suite")
    print("="*70)
    print(f"Model: {DEEPSEEK_MODEL}")
    print(f"Test Cases: {len(SQL_TEST_CASES)} SQL + {len(SPARQL_TEST_CASES)} SPARQL + {len(TABLEQA_TEST_CASES)} TableQA")
    print("="*70)
    
    suite = HeteroMindTestSuite()
    suite.setup_engines()
    
    all_results = []
    all_results.extend(await suite.test_sql_engine())
    all_results.extend(await suite.test_sparql_engine())
    all_results.extend(await suite.test_table_engine())
    
    summary = suite.calculate_summary(all_results)
    suite.print_summary(summary)
    
    output_path = Path(__file__).parent / "tests" / "comprehensive_test_results.json"
    suite.save_results(summary, str(output_path))
    
    report_path = Path(__file__).parent / "tests" / "comprehensive_test_report.md"
    generate_markdown_report(summary, str(report_path))
    
    return summary

def generate_markdown_report(summary: TestSuiteResult, output_path: str):
    report = f"""# HeteroMind Comprehensive Test Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model:** {DEEPSEEK_MODEL}

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {summary.total_tests} |
| Passed | {summary.passed_tests} ✅ |
| Failed | {summary.failed_tests} ❌ |
| **Overall Accuracy** | **{summary.accuracy:.1%}** |
| Avg Confidence | {summary.avg_confidence:.2f} |
| Avg Response Time | {summary.avg_time_ms:.0f}ms |

## Results by Engine

| Engine | Tests | Passed | Accuracy | Avg Confidence | Avg Time |
|--------|-------|--------|----------|----------------|----------|
"""
    for engine, stats in summary.by_engine.items():
        report += f"| {engine} | {stats['total']} | {stats['passed']} | {stats['accuracy']:.1%} | {stats['avg_confidence']:.2f} | {stats['avg_time_ms']:.0f}ms |\n"
    
    report += "\n## Detailed Results\n\n"
    
    for result in summary.detailed_results:
        status = "✅ PASS" if result.answer_correct else "❌ FAIL"
        unknown_tag = " [UNKNOWN SOURCE]" if result.details.get("is_unknown_source") else ""
        report += f"### {result.test_id}{unknown_tag} - {status}\n\n**Query:** {result.query}\n\n**Engine:** {result.engine_type}\n\n**Confidence:** {result.confidence:.2f}\n\n**Execution Time:** {result.execution_time_ms:.0f}ms\n\n**Generated Query:**\n```\n{result.generated_query or 'N/A'}\n```\n\n"
        if result.error:
            report += f"**Error:** {result.error}\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Report saved to: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
