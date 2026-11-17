#!/usr/bin/env python3
"""
快速烟测脚本 - 王琦教授中医体质学术助手

快速验证核心功能是否正常工作。

Usage:
    python smoke_test.py
    python smoke_test.py --verbose
"""

import hashlib
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from chroma_compat import list_collection_names

# Keep smoke-test output clean: disable Chroma telemetry for this process.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "FALSE")

# Add scripts to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from runtime_paths import PROJECT_DIR, WORKSPACE_DIR, load_runtime_env, resolve_env_file


ENV_PATH, ENV_SOURCE, ENV_WARNING = resolve_env_file()
load_runtime_env()


class SmokeTest:
    """Quick smoke test runner"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []
    
    def test(self, name: str, func) -> bool:
        """Run a single test"""
        try:
            result = func()
            if result.get("status") == "pass":
                self.passed += 1
                status = "[PASS]"
            elif result.get("status") == "warn":
                self.warnings += 1
                status = "[WARN]"
            else:
                self.failed += 1
                status = "[FAIL]"
            
            message = result.get("message", "")
            details = result.get("details", {})
            self.results.append({
                "name": name,
                "status": result.get("status"),
                "message": message,
                "details": details
            })
            
            print(f"  {status} {name}: {message}")
            if self.verbose and details:
                for key, value in details.items():
                    print(f"         {key}: {value}")
            return result.get("status") != "fail"
        
        except Exception as e:
            self.failed += 1
            print(f"  [FAIL] {name}: {e}")
            self.results.append({
                "name": name,
                "status": "fail",
                "message": str(e),
                "details": {}
            })
            return False
    
    def summary(self) -> dict:
        """Print summary and return results"""
        total = self.passed + self.failed + self.warnings
        print()
        print("=" * 60)
        print(f"Summary: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        print("=" * 60)
        
        return {
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "total": total,
            "results": self.results
        }


# ===== Test Functions =====

def test_skill_file():
    """Test SKILL.md exists"""
    skill_path = PROJECT_DIR / "SKILL.md"
    if skill_path.exists():
        size = skill_path.stat().st_size
        return {
            "status": "pass",
            "message": f"Found ({size} bytes)",
            "details": {"path": str(skill_path)}
        }
    return {"status": "fail", "message": "SKILL.md not found"}


def test_env_file():
    """Test which env file is being used."""
    if ENV_PATH is not None:
        status = "pass" if ENV_WARNING is None else "warn"
        message = f"Loaded from {ENV_PATH}"
        if ENV_WARNING:
            message = f"{message} ({ENV_WARNING})"
        return {
            "status": status,
            "message": message,
            "details": {"source": ENV_SOURCE}
        }

    return {
        "status": "warn",
        "message": ENV_WARNING or ".env not found (may rely on shell environment)",
        "details": {"source": ENV_SOURCE}
    }


def _mask_env_value(value: str) -> str:
    if not value:
        return "NOT SET"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def test_chat_env():
    """Test chat model environment variables."""
    required = ["API_KEY", "BASE_URL"]
    missing = [v for v in required if not os.getenv(v)]

    if not missing:
        return {
            "status": "pass",
            "message": "Chat env ready",
            "details": {
                "API_KEY": _mask_env_value(os.getenv("API_KEY", "")),
                "BASE_URL": os.getenv("BASE_URL", ""),
                "MODEL_NAME": os.getenv("MODEL_NAME", "(default)")
            }
        }

    return {
        "status": "fail",
        "message": f"Missing: {', '.join(missing)}",
        "details": {"source": str(ENV_PATH) if ENV_PATH else "shell only"}
    }


def test_embedding_env():
    """Test embedding environment variables after fallback resolution."""
    resolved_api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
    resolved_base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
    resolved_model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")

    missing = []
    if not resolved_api_key:
        missing.append("EMBEDDING_API_KEY/API_KEY")
    if not resolved_base_url:
        missing.append("EMBEDDING_BASE_URL/BASE_URL")

    if not missing:
        return {
            "status": "pass",
            "message": "Embedding env ready",
            "details": {
                "EMBEDDING_MODEL": resolved_model,
                "EMBEDDING_BASE_URL": resolved_base_url,
                "EMBEDDING_API_KEY": _mask_env_value(resolved_api_key)
            }
        }

    return {
        "status": "fail",
        "message": f"Missing: {', '.join(missing)}",
        "details": {"source": str(ENV_PATH) if ENV_PATH else "shell only"}
    }


def test_knowledge_cards():
    """Test knowledge cards directory"""
    cards_path = PROJECT_DIR / "data" / "cards"
    if not cards_path.exists():
        return {"status": "fail", "message": "Cards directory not found"}
    
    # Count JSON files
    json_files = list(cards_path.rglob("*.json"))
    if len(json_files) >= 10:
        return {
            "status": "pass",
            "message": f"{len(json_files)} cards found",
            "details": {"path": str(cards_path)}
        }
    return {
        "status": "warn",
        "message": f"Only {len(json_files)} cards found",
        "details": {"path": str(cards_path)}
    }


def test_chroma_db():
    """Test whether ChromaDB is actually readable."""
    chroma_path = PROJECT_DIR / "chroma_db"
    if not chroma_path.exists():
        return {"status": "warn", "message": "ChromaDB not built (run build_local_index.py)"}

    files = list(chroma_path.glob("*"))
    if not files:
        return {"status": "warn", "message": "ChromaDB directory empty"}

    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        return {"status": "fail", "message": "chromadb not installed"}

    try:
        client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=Settings(anonymized_telemetry=False)
        )
        collections = client.list_collections()
        collection_names = list_collection_names(collections)

        if not collections:
            return {
                "status": "warn",
                "message": "Directory exists but no collections found",
                "details": {"path": str(chroma_path)}
            }

        if "wangqi_knowledge" in collection_names:
            collection = client.get_collection("wangqi_knowledge")
            count = collection.count()
            if count == 0:
                return {
                    "status": "warn",
                    "message": "wangqi_knowledge exists but is empty",
                    "details": {
                        "collections": ", ".join(collection_names),
                        "path": str(chroma_path)
                    }
                }
            return {
                "status": "pass",
                "message": f"wangqi_knowledge ready ({count} docs)",
                "details": {
                    "collections": ", ".join(collection_names),
                    "path": str(chroma_path)
                }
            }

        return {
            "status": "warn",
            "message": f"Collections found but wangqi_knowledge missing: {', '.join(collection_names)}",
            "details": {"path": str(chroma_path)}
        }
    except Exception as e:
        return {
            "status": "fail",
            "message": f"Unreadable: {str(e)[:120]}",
            "details": {"path": str(chroma_path)}
        }


def test_python_packages():
    """Test required Python packages"""
    missing = []
    
    try:
        import openai
    except ImportError:
        missing.append("openai")
    
    try:
        import chromadb
    except ImportError:
        missing.append("chromadb")
    
    try:
        import fitz  # PyMuPDF
    except ImportError:
        missing.append("pymupdf")
    
    if not missing:
        return {"status": "pass", "message": "All packages installed"}
    return {"status": "fail", "message": f"Missing: {', '.join(missing)}"}


def test_retrieve_script():
    """Test retrieve.py can be imported"""
    try:
        from retrieve import retrieve
        return {"status": "pass", "message": "Import successful"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}


def test_ask_script():
    """Test ask.py can be imported"""
    try:
        from ask import ask
        return {"status": "pass", "message": "Import successful"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}


def test_evals_file():
    """Test evals.json exists and is valid"""
    evals_path = PROJECT_DIR / "evals" / "evals.json"
    if not evals_path.exists():
        return {"status": "warn", "message": "evals.json not found"}
    
    try:
        with open(evals_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        count = len(data.get("evals", []))
        if count >= 10:
            return {
                "status": "pass",
                "message": f"{count} test cases",
                "details": {"path": str(evals_path)}
            }
        return {
            "status": "warn",
            "message": f"Only {count} test cases",
            "details": {"path": str(evals_path)}
        }
    except json.JSONDecodeError:
        return {"status": "fail", "message": "Invalid JSON"}


def test_skill_sync():
    """Test SKILL.md is synced to Claude Code skills directory.
    
    If not synced or content differs, automatically copy the file.
    """
    import shutil
    
    source = PROJECT_DIR / "SKILL.md"
    target = WORKSPACE_DIR / ".claude" / "skills" / "professor-wangqi" / "SKILL.md"
    
    if not source.exists():
        return {"status": "fail", "message": "Source SKILL.md not found"}
    
    # Ensure target directory exists
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if sync needed
    needs_sync = False
    reason = ""
    
    if not target.exists():
        needs_sync = True
        reason = "Target not found"
    else:
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        
        if source_hash != target_hash:
            needs_sync = True
            reason = "Content differs"
    
    if needs_sync:
        # Auto-sync: copy source to target
        try:
            shutil.copy2(source, target)
            return {
                "status": "pass",
                "message": f"Auto-synced ({reason})",
                "details": {"from": str(source), "to": str(target)}
            }
        except Exception as e:
            return {
                "status": "warn",
                "message": f"Auto-sync failed: {e}",
                "details": {"target": str(target)}
            }
    
    return {"status": "pass", "message": "Already synced"}


# ===== Main =====

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Quick smoke test")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Wang Qi Professor TCM Assistant - Smoke Test")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    tester = SmokeTest(verbose=args.verbose)
    
    # File tests
    print("[Files]")
    tester.test("SKILL.md", test_skill_file)
    tester.test("Knowledge cards", test_knowledge_cards)
    tester.test("ChromaDB", test_chroma_db)
    tester.test("Evals file", test_evals_file)
    print()
    
    # Environment tests
    print("[Environment]")
    tester.test("Env file", test_env_file)
    tester.test("Chat env", test_chat_env)
    tester.test("Embedding env", test_embedding_env)
    print()
    
    # Package tests
    print("[Packages]")
    tester.test("Python packages", test_python_packages)
    print()
    
    # Script tests
    print("[Scripts]")
    tester.test("retrieve.py", test_retrieve_script)
    tester.test("ask.py", test_ask_script)
    print()
    
    # Sync test
    print("[Claude Code]")
    tester.test("Skill sync", test_skill_sync)
    print()
    
    # Summary
    result = tester.summary()
    
    if args.json:
        print()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Exit code
    sys.exit(0 if result["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
