#!/usr/bin/env python3
"""
Vibe Codebase Audit - Usage Examples
Demonstrates all available tools and features
"""

import asyncio
import sys
from pathlib import Path

# Add skill directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import tools
from vibe_audit_enhanced import (
    vibe_audit_enhanced,
    vibe_audit_incremental,
    vibe_audit_diff
)
from vibe_audit_tools import (
    vibe_audit_scan,
    vibe_audit_multi_model,
    vibe_audit_full
)

# ============================================================================
# Example 1: Agent-Native Audit (Recommended)
# ============================================================================

async def example_agent_native_audit():
    """
    Example 1: Use current agent's LLM for audit
    No API key required! Perfect for OpenCode/Hermes/OpenClaw users.
    """
    print("=" * 80)
    print("Example 1: Agent-Native Audit (No API Key Needed!)")
    print("=" * 80)
    
    result = await vibe_audit_enhanced(
        project_path=".",  # Current directory
        primary_provider="agent_llm",  # Use current agent's LLM
        enable_dependency_scan=True,  # Check dependencies
        enable_config_scan=True,  # Check configurations
        use_cache=True,  # Enable caching
        output_format="json"
    )
    
    # Print summary
    if 'summary' in result:
        print(f"\n📊 Risk Level: {result['summary'].get('risk_level', 'N/A')}")
        print(f"📊 Risk Score: {result['summary'].get('risk_score', 0)}/100")
        print(f"📊 Total Findings: {result['summary'].get('total_findings', 0)}")
    
    return result

# ============================================================================
# Example 2: Multi-Provider with Fallback
# ============================================================================

async def example_multi_provider():
    """
    Example 2: Use multiple providers with fallback
    If primary provider fails, automatically use fallback.
    """
    print("\n" + "=" * 80)
    print("Example 2: Multi-Provider Audit with Fallback")
    print("=" * 80)
    
    result = await vibe_audit_enhanced(
        project_path=".",
        primary_provider="openai",  # Try OpenAI first
        fallback_provider="claude",  # Fallback to Claude if OpenAI fails
        enable_dependency_scan=True,
        enable_config_scan=True,
        output_format="json"
    )
    
    print(f"Provider used: {result.get('provider_used', 'unknown')}")
    return result

# ============================================================================
# Example 3: Local Model with Ollama
# ============================================================================

async def example_ollama_local():
    """
    Example 3: Use local model via Ollama
    Free! No API costs. Runs completely locally.
    
    Prerequisites:
    1. Install Ollama: curl -fsSL https://ollama.com/install.sh | sh
    2. Pull model: ollama pull llama2
    """
    print("\n" + "=" * 80)
    print("Example 3: Local Model with Ollama (Free, No API)")
    print("=" * 80)
    
    result = await vibe_audit_enhanced(
        project_path=".",
        primary_provider="ollama",  # Use local model
        output_format="json"
    )
    
    return result

# ============================================================================
# Example 4: Incremental Audit (CI/CD)
# ============================================================================

def example_incremental_audit():
    """
    Example 4: Incremental audit - only check changed files
    Perfect for CI/CD pipelines and large projects.
    """
    print("\n" + "=" * 80)
    print("Example 4: Incremental Audit (Changed Files Only)")
    print("=" * 80)
    
    result = vibe_audit_incremental(
        project_path=".",
        base_branch="main",  # Compare with main branch
        compare_branch="HEAD"  # Current branch
    )
    
    if result['status'] == 'success':
        print(f"\n✅ Changed files detected: {len(result['changed_files'])}")
        for file in result['changed_files'][:10]:  # Show first 10
            print(f"  - {file}")
        
        if len(result['changed_files']) > 10:
            print(f"  ... and {len(result['changed_files']) - 10} more")
        
        print("\n💡 Tip: Run full audit on these specific files for detailed analysis")
    else:
        print(f"⚠️ {result.get('note', 'Unknown error')}")
    
    return result

# ============================================================================
# Example 5: Diff Audit (Compare Commits)
# ============================================================================

def example_diff_audit():
    """
    Example 5: Compare security between two commits
    Track security improvements over time.
    """
    print("\n" + "=" * 80)
    print("Example 5: Diff Audit (Compare Security Between Commits)")
    print("=" * 80)
    
    # Example: Compare current HEAD with previous commit
    result = vibe_audit_diff(
        project_path=".",
        base_commit="HEAD~1",  # Previous commit
        head_commit="HEAD"  # Current commit
    )
    
    print(f"\nBase: {result['base_commit']}")
    print(f"Head: {result['head_commit']}")
    print(f"Status: {result['status']}")
    
    return result

# ============================================================================
# Example 6: Legacy Tool - Quick Scan
# ============================================================================

def example_quick_scan():
    """
    Example 6: Quick local scan (legacy tool)
    Fast pattern-based scanning, no AI needed.
    """
    print("\n" + "=" * 80)
    print("Example 6: Quick Local Scan (Pattern-Based)")
    print("=" * 80)
    
    result = vibe_audit_scan(
        project_path=".",
        output_format="console",  # Console output
        severity_threshold=3  # Medium and above
    )
    
    return result

# ============================================================================
# Example 7: Legacy Tool - Multi-Model Consensus
# ============================================================================

async def example_multi_model_consensus():
    """
    Example 7: Multi-model consensus audit (legacy tool)
    Uses Claude, GPT-4, and Gemini for independent review.
    
    Requires OpenRouter API key.
    """
    print("\n" + "=" * 80)
    print("Example 7: Multi-Model AI Consensus (Legacy)")
    print("=" * 80)
    
    import os
    if not os.environ.get('OPENROUTER_API_KEY'):
        print("⚠️ OPENROUTER_API_KEY not set - skipping this example")
        print("Set it with: export OPENROUTER_API_KEY='your_key'")
        return None
    
    result = vibe_audit_multi_model(
        project_path=".",
        models=["claude", "gpt4"],  # Use only Claude and GPT-4
        consensus_mode="conservative",  # Use highest risk score
        output_format="json"
    )
    
    return result

# ============================================================================
# Example 8: Complete Workflow
# ============================================================================

async def example_complete_workflow():
    """
    Example 8: Complete security workflow
    Automated scan + dependency check + config check + AI audit.
    """
    print("\n" + "=" * 80)
    print("Example 8: Complete Security Workflow")
    print("=" * 80)
    
    result = vibe_audit_full(
        project_path=".",
        auto_fix_suggestions=True,
        output_format="markdown"
    )
    
    return result

# ============================================================================
# Example 9: Custom Configuration
# ============================================================================

async def example_custom_config():
    """
    Example 9: Use custom configuration file
    """
    print("\n" + "=" * 80)
    print("Example 9: Custom Configuration")
    print("=" * 80)
    
    from vibe_audit_enhanced import AuditConfig, EnhancedAuditor
    
    # Create custom config
    config = AuditConfig(
        primary_provider="agent_llm",
        cache_enabled=True,
        parallel_workers=8,  # More parallel workers
        max_file_size=5_000_000  # 5MB limit
    )
    
    # Create auditor with custom config
    auditor = EnhancedAuditor(config)
    
    # Run audit
    result = await auditor.audit_project(
        project_path=".",
        enable_dependency_scan=True,
        enable_config_scan=True
    )
    
    return result

# ============================================================================
# Example 10: Caching Demo
# ============================================================================

async def example_caching():
    """
    Example 10: Demonstrate caching mechanism
    """
    print("\n" + "=" * 80)
    print("Example 10: Caching Demonstration")
    print("=" * 80)
    
    from vibe_audit_enhanced import AuditCache
    import time
    
    # Create cache
    cache = AuditCache(cache_dir=".vibe-audit-cache", expire_days=7)
    
    # First run (cache miss)
    print("\n📊 First run (no cache)...")
    start_time = time.time()
    result1 = await vibe_audit_enhanced(
        project_path=".",
        primary_provider="agent_llm",
        use_cache=True
    )
    time1 = time.time() - start_time
    print(f"Time: {time1:.2f}s")
    
    # Second run (cache hit)
    print("\n📊 Second run (with cache)...")
    start_time = time.time()
    result2 = await vibe_audit_enhanced(
        project_path=".",
        primary_provider="agent_llm",
        use_cache=True
    )
    time2 = time.time() - start_time
    print(f"Time: {time2:.2f}s")
    
    print(f"\n⚡ Speed improvement: {(time1 - time2) / time1 * 100:.1f}%")
    
    return result2

# ============================================================================
# Main Runner
# ============================================================================

async def run_all_examples():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("🔒 VIBE CODEBASE AUDIT - USAGE EXAMPLES")
    print("=" * 80)
    
    examples = [
        ("Agent-Native Audit (Recommended)", example_agent_native_audit, True),
        ("Multi-Provider with Fallback", example_multi_provider, True),
        ("Local Model with Ollama", example_ollama_local, True),
        ("Incremental Audit", example_incremental_audit, False),
        ("Diff Audit", example_diff_audit, False),
        ("Quick Scan (Legacy)", example_quick_scan, False),
        ("Multi-Model Consensus (Legacy)", example_multi_model_consensus, True),
        ("Complete Workflow", example_complete_workflow, True),
        ("Custom Configuration", example_custom_config, True),
        ("Caching Demo", example_caching, True),
    ]
    
    for name, func, is_async in examples:
        print(f"\n{'='*80}")
        print(f"Running: {name}")
        print(f"{'='*80}")
        
        try:
            if is_async:
                await func()
            else:
                func()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        input("\nPress Enter to continue to next example...")
    
    print("\n" + "=" * 80)
    print("✅ All examples completed!")
    print("=" * 80)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Vibe Audit Examples")
    parser.add_argument("--all", action="store_true", help="Run all examples")
    parser.add_argument("--example", type=int, choices=range(1, 11),
                       help="Run specific example (1-10)")
    
    args = parser.parse_args()
    
    if args.all:
        asyncio.run(run_all_examples())
    elif args.example:
        examples = {
            1: example_agent_native_audit,
            2: example_multi_provider,
            3: example_ollama_local,
            4: example_incremental_audit,
            5: example_diff_audit,
            6: example_quick_scan,
            7: example_multi_model_consensus,
            8: example_complete_workflow,
            9: example_custom_config,
            10: example_caching,
        }
        
        func = examples[args.example]
        if args.example in [4, 5, 6]:  # Sync functions
            func()
        else:  # Async functions
            asyncio.run(func())
    else:
        print("Usage:")
        print("  python examples.py --all           # Run all examples")
        print("  python examples.py --example 1     # Run example 1")
        print("\nExamples:")
        print("  1 - Agent-Native Audit (Recommended)")
        print("  2 - Multi-Provider with Fallback")
        print("  3 - Local Model with Ollama")
        print("  4 - Incremental Audit")
        print("  5 - Diff Audit")
        print("  6 - Quick Scan (Legacy)")
        print("  7 - Multi-Model Consensus (Legacy)")
        print("  8 - Complete Workflow")
        print("  9 - Custom Configuration")
        print(" 10 - Caching Demo")
