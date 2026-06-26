import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from notification_formatter import format_notification

def test_format_sdlc_start():
    res = format_notification("sdlc_start", {"prd_id": "PRD_081_test.md", "command": "python3 script.py"})
    assert res == "🚀 1. [prd-081] SDLC 启动\n💻 Command: `python3 script.py`"

def test_format_sdlc_resume():
    res = format_notification("sdlc_resume", {"prd_id": "PRD_081_test.md", "command": "python3 script.py"})
    assert res == "🚀 1. [prd-081] SDLC 恢复执行\n💻 Command: `python3 script.py`"

def test_format_auditor_start():
    res = format_notification("auditor_start", {"prd_id": "PRD_081_test.md", "command": "python3 spawn_auditor.py"})
    assert res == "🚀 [Auditor] 启动审批流程\n💻 Command: `python3 spawn_auditor.py`"

def test_format_slicing_start():
    res = format_notification("slicing_start", {"prd_id": "PRD_081_test.md"})
    assert res == "🔪 2. [prd-081] 切片中..."

def test_format_slicing_end():
    res = format_notification("slicing_end", {"prd_id": "PRD_081_test.md", "count": 5})
    assert res == "✅ 3. [prd-081] 切片结束，共生成 5 个切片"

def test_format_coder_start():
    res = format_notification("coder_start", {"pr_id": "PR_001_test.md"})
    assert res == "👨💻 4. [pr-001] Coder 运行中..."

def test_format_review_start():
    res = format_notification("review_start", {"pr_id": "PR_001_test.md"})
    assert res == "🧐 5. [pr-001] Coder 结束，Review 中..."

def test_format_review_result():
    res = format_notification("review_result", {"pr_id": "PR_001_test.md", "result": "LGTM"})
    assert res == "📝 6. [pr-001] Review 结果：LGTM"

def test_format_coder_start_microsliced():
    res = format_notification("coder_start", {"pr_id": "PR_003_1_Fix.md"})
    assert res == "👨💻 4. [pr-003-1] Coder 运行中..."

def test_format_coder_start_microsliced_complex():
    res = format_notification("coder_start", {"pr_id": "PR_003_1_2_Fix_Something.md"})
    assert res == "👨💻 4. [pr-003-1-2] Coder 运行中..."

def test_format_auditor_approved():
    res = format_notification("auditor_approved", {"prd_id": "PRD_123_Test.md"})
    assert res == "✅ [Auditor] PRD 审查通过 (APPROVED)。"

def test_format_auditor_rejected():
    res = format_notification("auditor_rejected", {"prd_id": "PRD_123_Test.md"})
    assert res == "❌ [Auditor] PRD 审查未通过 (REJECTED)，请根据反馈进行修改并重试。"

def test_format_uat_complete_pass():
    res = format_notification("uat_complete", {"prd_id": "PRD_123_Test.md", "status": "PASS"})
    assert res == "🎉 [prd-123] UAT Verification: Passed."

def test_format_uat_complete_fail():
    res = format_notification("uat_complete", {"prd_id": "PRD_123_Test.md", "status": "NEEDS_FIX"})
    assert res == "⚠️ [prd-123] UAT Verification: Missed (Needs Fix)."

def test_format_uat_error():
    res = format_notification("uat_error", {"prd_id": "PRD_123_Test.md"})
    assert res == "❌ [prd-123] UAT Verification Error: 测试报告解析失败或发生异常。"
