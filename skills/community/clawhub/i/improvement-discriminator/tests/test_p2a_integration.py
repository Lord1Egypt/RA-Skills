#!/usr/bin/env python3
"""
Skill Evaluator P2-a Integration Test

测试 P2-a 新增功能:
1. Hidden Tests 工程化 (数据源/可见性边界)
2. External Regression Hook
3. Human Review Receipt

运行方式:
    python3 tests/test_p2a_integration.py
    pytest tests/test_p2a_integration.py -v
"""

import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime

# 添加 interfaces 到 path
interfaces_dir = str(Path(__file__).parent.parent / "interfaces")
if interfaces_dir not in sys.path:
    sys.path.insert(0, interfaces_dir)


def test_hidden_tests_data_source():
    """测试隐藏测试数据源接口"""
    print("\n" + "=" * 60)
    print("Test 1: Hidden Tests Data Source")
    print("=" * 60)

    from hidden_tests import (
        HiddenTestSuite,
        DictHiddenTestDataSource,
        FileHiddenTestDataSource,
        TestVisibility,
        create_hidden_test,
        TestType,
    )

    # 测试 1: 字典数据源
    print("\n1.1 Testing DictHiddenTestDataSource...")
    
    demo_data = {
        "suite_id": "demo-suite-001",
        "tests": [
            {
                "metadata": {
                    "id": "test-001",
                    "type": "functional",
                    "category": "general",
                    "difficulty": 2,
                    "estimated_time_ms": 100.0,
                },
                "encrypted_input": "eyJ0YXNrIjogInRlc3QifQ==",  # {"task": "test"}
                "encrypted_expected": "eyJzdGF0dXMiOiAic3VjY2VzcyJ9",  # {"status": "success"}
                "encrypted_validator": "eyJ0eXBlIjogImV4YWN0In0=",  # {"type": "exact"}
                "salt": "c2FsdHkxMjM0NTY3OA==",  # salty12345678
                "visibility": "hidden",
            }
        ]
    }

    # 简单加密 (XOR with key)
    import base64
    import hashlib
    key = hashlib.sha256("demo_password_123".encode()).digest()
    
    def encrypt(data):
        json_data = json.dumps(data).encode()
        return base64.b64encode(bytes([b ^ key[i % len(key)] for i, b in enumerate(json_data)])).decode()
    
    demo_data["tests"][0]["encrypted_input"] = encrypt({"task": "test_001", "data": [1, 2, 3]})
    demo_data["tests"][0]["encrypted_expected"] = encrypt({"status": "success", "score": 0.9})
    demo_data["tests"][0]["encrypted_validator"] = encrypt({"type": "contains", "threshold": 0.8})

    import hashlib
    data_source = DictHiddenTestDataSource(demo_data, password="demo_password_123")
    
    suite = HiddenTestSuite(
        suite_id="test-suite",
        name="Test Suite",
        version="1.0.0",
    )
    
    loaded = suite.load_from_data_source(data_source, password="demo_password_123")
    assert loaded, "Should load from data source"
    assert len(suite._tests) > 0, "Should have loaded tests"
    
    print(f"✅ Loaded {len(suite._tests)} tests from dict data source")

    # 测试 2: 可见性边界
    print("\n1.2 Testing Visibility Boundary...")
    
    suite.set_visibility_boundary("evaluator")
    assert suite.is_visible_to("evaluator") == True
    assert suite.is_visible_to("proposer") == False
    
    suite.set_visibility_boundary("proposer")
    assert suite.is_visible_to("evaluator") == False
    assert suite.is_visible_to("proposer") == True
    
    suite.set_visibility_boundary("both")
    assert suite.is_visible_to("evaluator") == True
    assert suite.is_visible_to("proposer") == True
    
    print(f"✅ Visibility boundary working correctly")

    # 测试 3: 获取可见测试
    print("\n1.3 Testing Get Visible Tests...")
    
    suite.set_visibility_boundary("evaluator")
    evaluator_tests = suite.get_visible_tests("evaluator")
    proposer_tests = suite.get_visible_tests("proposer")
    
    assert len(evaluator_tests) > 0, "Evaluator should see tests"
    assert len(proposer_tests) == 0, "Proposer should not see tests"
    
    print(f"✅ Evaluator sees {len(evaluator_tests)} tests, proposer sees {len(proposer_tests)} tests")

    print("\n✅ Hidden Tests Data Source tests passed!")


def test_external_regression_hook():
    """测试外部回归结果接入"""
    print("\n" + "=" * 60)
    print("Test 2: External Regression Hook")
    print("=" * 60)

    from external_regression import (
        ExternalRegressionHook,
        RegressionSourceType,
        create_regression_result,
    )

    # 测试 1: 从字典加载
    print("\n2.1 Testing load from dict...")
    
    hook = ExternalRegressionHook()
    
    demo_data = {
        "suite_id": "regression-001",
        "suite_name": "Demo Regression",
        "tests": [
            {"test_id": "test-001", "test_name": "Test A", "status": "passed", "score": 1.0},
            {"test_id": "test-002", "test_name": "Test B", "status": "passed", "score": 0.9},
            {"test_id": "test-003", "test_name": "Test C", "status": "failed", "score": 0.3},
        ]
    }
    
    result = hook.load_from_dict(demo_data)
    assert result.total_tests == 3, "Should have 3 tests"
    assert result.passed == 2, "Should have 2 passed"
    assert result.failed == 1, "Should have 1 failed"
    
    print(f"✅ Loaded {result.total_tests} tests from dict")

    # 测试 2: 从 JSON 文件加载
    print("\n2.2 Testing load from JSON file...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(demo_data, f)
        json_path = f.name
    
    try:
        hook2 = ExternalRegressionHook()
        result2 = hook2.load_from_file(json_path, adapter_type="json")
        assert result2.total_tests == 3, "Should load from file"
        print(f"✅ Loaded {result2.total_tests} tests from JSON file")
    finally:
        Path(json_path).unlink()

    # 测试 3: 归一化评分
    print("\n2.3 Testing normalized score...")
    
    score = hook.get_normalized_score()
    assert 0.0 <= score <= 1.0, "Score should be in valid range"
    print(f"✅ Normalized score: {score:.4f}")

    # 测试 4: 合并到基础评分
    print("\n2.4 Testing merge into base score...")
    
    base_score = 0.85
    final_score = hook.merge_into_score(base_score, regression_weight=0.2)
    expected = base_score * 0.8 + score * 0.2
    assert abs(final_score - expected) < 0.001, f"Should merge correctly: {final_score} vs {expected}"
    print(f"✅ Merged score: {base_score:.4f} -> {final_score:.4f} (regression weight=0.2)")

    # 测试 5: 导出报告
    print("\n2.5 Testing export report...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        report_path = f.name
    
    try:
        hook.export_report(report_path, format="json")
        assert Path(report_path).exists(), "Report should be created"
        
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        assert "summary" in report_data, "Report should have summary"
        assert "suites" in report_data, "Report should have suites"
        
        print(f"✅ Exported report to {report_path}")
    finally:
        Path(report_path).unlink()

    print("\n✅ External Regression Hook tests passed!")


def test_human_review_receipt():
    """测试人工审查回执"""
    print("\n" + "=" * 60)
    print("Test 3: Human Review Receipt")
    print("=" * 60)

    from human_review import (
        HumanReviewManager,
        HumanReviewReceipt,
        ReviewDecision,
        ReviewSeverity,
        create_review_finding,
    )

    # 测试 1: 创建审查回执
    print("\n3.1 Testing create receipt...")
    
    manager = HumanReviewManager()
    
    receipt = manager.create_receipt(
        skill_name="test-skill",
        skill_version="1.0.0",
        reviewer_id="reviewer-001",
        reviewer_name="Test Reviewer",
        decision=ReviewDecision.APPROVED,
        confidence=0.9,
        comments="Looks good, ready for production",
        final_score=0.88,
    )
    
    assert receipt.receipt_id.startswith("review-"), "Should have valid receipt ID"
    assert receipt.decision == ReviewDecision.APPROVED
    assert receipt.confidence == 0.9
    assert receipt.final_score == 0.88
    # Signature is computed on save, not on create
    
    print(f"✅ Created receipt: {receipt.receipt_id}")

    # 测试 2: 添加发现的问题
    print("\n3.2 Testing add findings...")
    
    finding = create_review_finding(
        category="performance",
        severity=ReviewSeverity.MINOR,
        title="Response time slightly high",
        description="Some edge cases take >1s",
        recommendation="Optimize caching strategy",
    )
    
    receipt.add_finding(finding)
    assert len(receipt.findings) == 1, "Should have 1 finding"
    
    print(f"✅ Added {len(receipt.findings)} finding(s)")

    # 测试 3: 保存和加载
    print("\n3.3 Testing save and load...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        receipt_path = f.name
    
    try:
        saved_path = receipt.save(receipt_path)
        assert Path(saved_path).exists(), "File should be created"
        
        loaded_receipt = HumanReviewReceipt.load(receipt_path)
        assert loaded_receipt.receipt_id == receipt.receipt_id
        assert loaded_receipt.decision == receipt.decision
        assert len(loaded_receipt.findings) == len(receipt.findings)
        # Signature is recomputed on load, so just verify it exists
        assert loaded_receipt.signature, "Signature should exist"
        
        print(f"✅ Saved and loaded receipt successfully")
    finally:
        Path(receipt_path).unlink()

    # 测试 4: 合并到基础评分
    print("\n3.4 Testing merge into base score...")
    
    base_score = 0.85
    final_score = manager.merge_scores(base_score, review_weight=0.3)
    
    # 由于是 APPROVED，分数应该接近 base_score 或略高
    assert 0.0 <= final_score <= 1.0, "Final score should be valid"
    print(f"✅ Merged score: {base_score:.4f} -> {final_score:.4f} (review weight=0.3)")

    # 测试 5: 导出报告
    print("\n3.5 Testing export report...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        report_path = f.name
    
    try:
        manager.export_report(report_path, format="markdown")
        assert Path(report_path).exists(), "Report should be created"
        
        content = Path(report_path).read_text()
        assert "Human Review Report" in content, "Should have title"
        assert "Test Reviewer" in content, "Should have reviewer name"
        
        print(f"✅ Exported markdown report to {report_path}")
    finally:
        Path(report_path).unlink()

    print("\n✅ Human Review Receipt tests passed!")


def test_critic_v2_p2a_integration():
    """测试 Critic V2 与 P2-a 组件的整合"""
    print("\n" + "=" * 60)
    print("Test 4: Critic V2 P2-a Integration")
    print("=" * 60)

    from critic_engine import CriticEngineV2, CriticConfig
    from human_review import ReviewDecision

    # 创建配置 (包含 P2-a 权重)
    config = CriticConfig(
        enable_frozen_benchmark=True,
        enable_hidden_tests=True,
        enable_assertions=True,
        enable_external_regression=True,
        enable_human_review=True,
        benchmark_weight=0.35,
        hidden_test_weight=0.25,
        assertion_weight=0.20,
        regression_weight=0.10,
        human_review_weight=0.10,
        verbose=False,
    )

    # 验证权重和为 1.0
    total = (
        config.benchmark_weight +
        config.hidden_test_weight +
        config.assertion_weight +
        config.regression_weight +
        config.human_review_weight
    )
    assert abs(total - 1.0) < 0.001, f"Weights should sum to 1.0, got {total}"
    print(f"✅ Config weights sum to 1.0: {total:.2f}")

    # 创建引擎
    engine = CriticEngineV2(config)

    # 加载标准组件
    engine.load_benchmark_suite()
    engine.load_hidden_tests(password="DEMO_ONLY_NOT_FOR_PRODUCTION")
    engine.load_standard_assertions()

    print(f"✅ Loaded standard components")

    # 加载外部回归结果
    regression_data = {
        "suite_id": "integration-test-regression",
        "suite_name": "Integration Test",
        "tests": [
            {"test_id": "reg-001", "test_name": "Regression A", "status": "passed", "score": 0.95},
            {"test_id": "reg-002", "test_name": "Regression B", "status": "passed", "score": 0.88},
        ]
    }
    engine.load_external_regression(data=regression_data)
    print(f"✅ Loaded external regression")

    # 创建人工审查回执
    receipt = engine.create_human_review_receipt(
        skill_name="integration-test-skill",
        skill_version="1.0.0",
        reviewer_id="auto-reviewer",
        reviewer_name="Automated Reviewer",
        decision=ReviewDecision.APPROVED,
        confidence=0.85,
        final_score=0.87,
    )
    print(f"✅ Created human review receipt")

    # 运行评估
    score = engine.evaluate()

    # 验证结果
    assert score.overall >= 0.0, "Overall score should be non-negative"
    assert score.overall <= 1.0, "Overall score should be <= 1.0"
    assert hasattr(score, 'regression_score'), "Score should have regression_score (P2-a)"
    assert hasattr(score, 'human_review_score'), "Score should have human_review_score (P2-a)"
    assert hasattr(score, 'regression_details'), "Score should have regression_details (P2-a)"
    assert hasattr(score, 'human_review_details'), "Score should have human_review_details (P2-a)"

    print(f"\n✅ Critic V2 P2-a evaluation completed")
    print(f"   Overall: {score.overall:.4f}")
    print(f"   Benchmark: {score.benchmark_score:.4f}")
    print(f"   Hidden: {score.hidden_test_score:.4f}")
    print(f"   Assertion: {score.assertion_score:.4f}")
    print(f"   Regression: {score.regression_score:.4f} (P2-a)")
    print(f"   Human Review: {score.human_review_score:.4f} (P2-a)")
    print(f"   Level: {score.level}")

    # 验证报告生成
    report = engine.generate_report("/tmp/test_critic_v2_p2a_report.md")
    assert "P2" in report or "P2-a" in report or "regression" in report.lower(), "Report should mention P2-a"
    print(f"✅ Report generated successfully")

    print("\n✅ Critic V2 P2-a Integration tests passed!")


def run_all_tests():
    """运行所有 P2-a 集成测试"""
    print("=" * 60)
    print("Skill Evaluator P2-a Integration Tests")
    print("=" * 60)

    tests = [
        ("Hidden Tests Data Source", test_hidden_tests_data_source),
        ("External Regression Hook", test_external_regression_hook),
        ("Human Review Receipt", test_human_review_receipt),
        ("Critic V2 P2-a Integration", test_critic_v2_p2a_integration),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n❌ {name} FAILED: {e}")
            import traceback
            traceback.print_exc()

    # 汇总结果
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)

    for name, passed, error in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if error:
            print(f"       Error: {error}")

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 All P2-a integration tests passed!")
        return True
    else:
        print(f"\n⚠️ {total_count - passed_count} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
