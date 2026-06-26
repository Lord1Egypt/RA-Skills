#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCode PR Review Wrapper
讓 OpenClaw 方便地派送 PR review 任務給 OpenCode

用法：
    python opencode_review.py --repo jlin53882/Minecraft-translate --pr 374
    python opencode_review.py --repo jlin53882/Minecraft-translate --pr 374 --model minimax/MiniMax-M2.7 --reasoning high
    python opencode_review.py --diff "path/to/diff.txt"
    python opencode_review.py --local "C:\\repo" --branch feature/xxx
"""

import argparse
import json
import sys
import os
from pathlib import Path

DEFAULT_BASE_URL = "http://127.0.0.1:4096"


def get_gh_diff(repo: str, pr_num: int) -> str:
    import subprocess
    try:
        result = subprocess.run(
            ["gh", "pr", "diff", "--repo", repo, str(pr_num)],
            capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            return result.stdout
        return f"[gh error] {result.stderr}"
    except FileNotFoundError:
        return "[ERROR] gh CLI 未安裝"
    except Exception as e:
        return f"[ERROR] {e}"


def get_local_diff(repo_path: str, branch: str) -> str:
    import subprocess
    try:
        result = subprocess.run(
            ["git", "diff", "main...", branch or "HEAD"],
            capture_output=True, text=True, timeout=30,
            cwd=repo_path, encoding="utf-8", errors="replace"
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"[ERROR] {e}"


def call_opencode_review(
    diff_content: str,
    repo: str = "",
    pr_num: int = None,
    model: str = "minimax/MiniMax-M2.7",
    reasoning: str = "medium",
    base_url: str = DEFAULT_BASE_URL,
    auto_start: bool = True,
) -> dict:
    """
    呼叫 OpenCode 進行 PR review（自動處理 Server 未運行的情況）
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from opencode_client import OpenCodeClient

    if not diff_content.strip():
        return {"ok": False, "error": "diff 內容為空"}

    client = OpenCodeClient(base_url=base_url, auto_start=auto_start)

    # 完整 Code Review Prompt（11 面向 + 結構化輸出）
    project_context = """**專案背景**：
- Minecraft 翻譯工具（Flet UI + translation_tool CLI）
- 主要技術：Python（Flet 0.82）、JAR parsing（ftb_snbt_lib）
- 翻譯格式：lang item、kubejs、ftb_quests 等
"""
    prompt = f"""你是一位資深軟體工程師，專責執行嚴謹的程式碼審查。請用繁體中文輸出。

{project_context}

請對以下 diff 依序完成 11 個面向的審查：

### 1. 正確性（Correctness）
邏輯是否有明顯 bug 或邊界條件未處理？非同步/並發是否有 race condition？錯誤處理是否完整？

### 2. 邏輯性（Logic & Design）
整體解題思路是否符合需求意圖？流程控制是否合理？是否有「繞路解法」？

### 3. 可讀性（Readability）
命名是否清晰？是否有過度巢狀？關鍵邏輯是否有注釋？程式碼風格是否與專案慣例一致？

### 4. 可維護性（Maintainability）
是否符合 SRP？是否有重複程式碼？硬編碼的魔法數字是否應提取為常數？

### 5. 效能（Performance）
是否有 N+1、不必要的重複計算？資料結構選擇是否合適？是否有記憶體洩漏風險？

### 6. 安全性（Security）
是否有 XSS（Flet WebView）、路徑 injection、敏感資訊洩漏？外部輸入是否有驗證？

### 7. 可觀測性（Observability）
是否有足夠的 logging？log level 是否合適？錯誤訊息是否足夠明確？

### 8. 向後相容性（Backward Compatibility）
是否破壞現有 API 合約或資料格式？是否有 breaking change？

### 9. 相依性與授權（Dependencies & Licensing）
新增套件是否有授權風險？是否有已知 CVE？

### 10. 參考來源與歸屬（Attribution）
程式碼是否來自外部開源專案需要標注來源？AI 生成片段是否已人工驗證？

### 11. 測試覆蓋（Testability）
是否有對應的單元測試或整合測試？是否涵蓋邊界條件？

=== Git Diff ===
{diff_content[:50000]}

### ✅ 優點
（列出值得保留的設計）

### 🔴 必須修正（Blocking）
- [面向] 問題描述
  建議修改：...

### 🟡 建議改善（Non-blocking）
- [面向] 問題描述
  建議修改：...

### 💡 可選優化（Optional）

### 📝 總結
整體評估：...
結論：Approve ✅ / Request Changes 🔄 / Needs Discussion 💬"""


    try:
        session = client.create_session(title=f"PR Review {pr_num or ''} - {repo}")
        session_id = session["id"]
    except Exception as e:
        return {"ok": False, "error": f"建立 session 失敗: {e}"}

    try:
        response = client.send_message(
            session_id=session_id,
            prompt=prompt,
            model=model,
            reasoning=reasoning,
        )
        review_text = client.extract_text(response)
    except RuntimeError as e:
        return {"ok": False, "error": str(e), "session_id": session_id}
    except Exception as e:
        return {"ok": False, "error": f"傳送訊息失敗: {e}", "session_id": session_id}

    return {
        "ok": True,
        "session_id": session_id,
        "review": review_text,
        "model": model,
        "reasoning": reasoning,
    }


def main():
    parser = argparse.ArgumentParser(description="OpenCode PR Review Wrapper")
    parser.add_argument("--repo", help="GitHub repo（格式：owner/name）")
    parser.add_argument("--pr", type=int, help="PR 編號")
    parser.add_argument("--diff", help="直接提供 diff 檔案路徑")
    parser.add_argument("--local", help="本機 repo 路徑")
    parser.add_argument("--branch", help="本機 branch 名稱")
    parser.add_argument("--model", default="minimax/MiniMax-M2.7", help="模型")
    parser.add_argument("--reasoning", default="medium",
                        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
                        help="思考深度")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--json", action="store_true", help="輸出 JSON 格式")
    parser.add_argument("--auto-start", dest="auto_start", action="store_true", default=True)
    parser.add_argument("--no-auto-start", dest="auto_start", action="store_false")

    args = parser.parse_args()

    # 取得 diff
    if args.diff:
        diff_path = Path(args.diff)
        if diff_path.exists():
            diff_content = diff_path.read_text(encoding="utf-8", errors="replace")
        else:
            diff_content = args.diff
    elif args.repo and args.pr:
        diff_content = get_gh_diff(args.repo, args.pr)
    elif args.local and args.branch:
        diff_content = get_local_diff(args.local, args.branch)
    else:
        print("[ERROR] 請提供 --diff、--repo+--pr、或 --local+--branch")
        sys.exit(1)

    if diff_content.startswith("[ERROR]"):
        print(diff_content)
        sys.exit(1)

    result = call_opencode_review(
        diff_content=diff_content,
        repo=args.repo or "",
        pr_num=args.pr,
        model=args.model,
        reasoning=args.reasoning,
        base_url=args.base_url,
        auto_start=args.auto_start,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result["ok"]:
            print(f"[ERROR] {result.get('error', '未知錯誤')}")
            sys.exit(1)
        print(f"[Model] {result['model']} | [Session] {result['session_id']}")
        print("=" * 60)
        print(result["review"])


if __name__ == "__main__":
    main()
