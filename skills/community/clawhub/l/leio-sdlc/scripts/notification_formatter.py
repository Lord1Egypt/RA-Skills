def format_notification(event_type: str, context: dict) -> str:
    prd_id = context.get('prd_id', 'unknown')
    pr_id = context.get('pr_id', 'unknown')
    
    # Optional prefix extracted from PRD filename, assuming format "PRD_123_Name.md"
    prd_match = prd_id
    if prd_id.lower().startswith("prd"):
        parts = prd_id.split('_')
        if len(parts) >= 2:
            prd_match = f"prd-{parts[1]}"
            
    import re
    pr_match = pr_id
    # Extract PR prefix (case-insensitive) followed by underscores and digits/underscores
    match = re.search(r'^(?i:pr_)([\d_]+)', pr_id)
    if match:
        # Align regex comment with PRD-1063 for clarity
        extracted = match.group(1).rstrip('_')
        pr_match = f"pr-{extracted.replace('_', '-')}"

    if event_type == "sdlc_resume":
        cmd = context.get("command", "unknown")
        return f"🚀 1. [{prd_match}] SDLC 恢复执行\n💻 Command: `{cmd}`"
    elif event_type == "sdlc_start":
        cmd = context.get("command", "unknown")
        return f"🚀 1. [{prd_match}] SDLC 启动\n💻 Command: `{cmd}`"
    elif event_type == "auditor_start":
        cmd = context.get("command", "unknown")
        return f"🚀 [Auditor] 启动审批流程\n💻 Command: `{cmd}`"
    elif event_type == "slicing_start":
        return f"🔪 2. [{prd_match}] 切片中..."
    elif event_type == "slicing_end":
        count = context.get('count', 0)
        return f"✅ 3. [{prd_match}] 切片结束，共生成 {count} 个切片"
    elif event_type == "pr_switch":
        branch = context.get('branch', 'unknown')
        return f"🔄 [{pr_match}] 切换分支：{branch}"
    elif event_type == "coder_start":
        return f"👨💻 4. [{pr_match}] Coder 运行中..."
    elif event_type == "review_start":
        return f"🧐 5. [{pr_match}] Coder 结束，Review 中..."
    elif event_type == "review_result":
        result = context.get('result', 'N/A')
        return f"📝 6. [{pr_match}] Review 结果：{result}"
    elif event_type == "all_done":
        return f"🎉 [{prd_match}] SDLC 完成：所有 PR 执行完毕"
    elif event_type == "dead_end":
        return f"🛑 [{pr_match}] PR 需要人工介入"
    elif event_type == "sdlc_handshake":
        return f"🤝 [SDLC Engine] Initial Handshake successful. Channel linked."
    elif event_type == "coder_spawned":
        return f"Calling Coder for [{pr_match}]..."
    elif event_type == "reviewer_spawned":
        return f"Coder submitted changes. Reviewer is now auditing..."
    elif event_type == "review_rejected":
        summary = context.get('summary', 'No reason provided')
        return f"❌ Reviewer rejected changes. Reason: {summary}. Retrying..."
    elif event_type == "pr_merged":
        return f"✅ [{pr_match}] successfully merged to master."
    elif event_type == "github_sync_start":
        return f"Synchronizing code to GitHub..."
    elif event_type == "github_sync_complete":
        return f"GitHub sync complete."
    elif event_type == "github_sync_failed":
        err = context.get('error', 'unknown error')
        return f"⚠️ GitHub sync failed: {err}"
    elif event_type == "auditor_approved":
        return f"✅ [Auditor] PRD 审查通过 (APPROVED)。"
    elif event_type == "auditor_rejected":
        return f"❌ [Auditor] PRD 审查未通过 (REJECTED)，请根据反馈进行修改并重试。"
    elif event_type == "uat_complete":
        status = context.get('status', 'UNKNOWN')
        if status == "PASS":
            return f"🎉 [{prd_match}] UAT Verification: Passed."
        else:
            return f"⚠️ [{prd_match}] UAT Verification: Missed (Needs Fix)."
    elif event_type == "uat_error":
        return f"❌ [{prd_match}] UAT Verification Error: 测试报告解析失败或发生异常。"
    
    return f"🤖 [SDLC Engine] 未知事件: {event_type}"
