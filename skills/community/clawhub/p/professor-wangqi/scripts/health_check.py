"""
健康检查脚本 - 王琦教授中医体质学术助手

快速诊断系统状态，检查所有依赖和配置。

Usage:
    python health_check.py
    python health_check.py --verbose
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

from runtime_paths import (
    DEFAULT_CARDS_DIR,
    DEFAULT_PERSIST_DIR,
    DEFAULT_SKILL_PATH,
    load_runtime_env,
    resolve_env_file,
)

# Load environment
ENV_PATH, ENV_SOURCE, ENV_WARNING = resolve_env_file()
load_runtime_env()


class HealthChecker:
    """System health checker"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name: str, func) -> bool:
        """Run a single check"""
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
    
    def summary(self) -> Dict:
        """Print summary and return results"""
        total = self.passed + self.failed + self.warnings
        print()
        print("=" * 60)
        print("Health Check Summary")
        print("=" * 60)
        print(f"  Total checks: {total}")
        print(f"  [PASS] Passed: {self.passed}")
        print(f"  [WARN] Warnings: {self.warnings}")
        print(f"  [FAIL] Failed: {self.failed}")
        
        if self.failed == 0:
            print()
            print("All critical checks passed!")
        else:
            print()
            print("Some checks failed. Please review the issues above.")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total": total,
            "passed": self.passed,
            "warnings": self.warnings,
            "failed": self.failed,
            "results": self.results
        }


def check_python_version() -> Dict:
    """Check Python version"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        return {"status": "pass", "message": f"Python {version_str}"}
    else:
        return {"status": "fail", "message": f"Python {version_str} (requires 3.8+)"}


def check_env_file() -> Dict:
    """Check .env file exists"""
    if ENV_PATH is not None:
        details = {"source": ENV_SOURCE}
        if ENV_WARNING:
            details["warning"] = ENV_WARNING
        return {"status": "pass", "message": str(ENV_PATH), "details": details}

    details = {"source": ENV_SOURCE}
    if ENV_WARNING:
        details["warning"] = ENV_WARNING
    return {"status": "fail", "message": "No .env file found", "details": details}


def check_env_variables() -> Dict:
    """Check required environment variables"""
    required = ["API_KEY", "BASE_URL", "MODEL_NAME"]
    missing = []
    present = []
    
    for var in required:
        value = os.getenv(var)
        if value:
            present.append(var)
        else:
            missing.append(var)
    
    if not missing:
        return {
            "status": "pass",
            "message": f"All {len(required)} variables set",
            "details": {v: os.getenv(v, "")[:20] + "..." for v in present}
        }
    else:
        return {
            "status": "fail",
            "message": f"Missing: {', '.join(missing)}",
            "details": {v: "NOT SET" for v in missing}
        }


def check_embedding_env() -> Dict:
    """Check embedding environment variables"""
    vars = ["EMBEDDING_MODEL", "EMBEDDING_BASE_URL", "EMBEDDING_API_KEY"]
    present = []
    missing = []
    
    for var in vars:
        if os.getenv(var):
            present.append(var)
        else:
            missing.append(var)
    
    if not missing:
        return {"status": "pass", "message": f"All {len(vars)} variables set"}
    else:
        return {"status": "warn", "message": f"Missing: {', '.join(missing)} (will use defaults)"}


def check_openai_package() -> Dict:
    """Check openai package"""
    try:
        import openai
        return {"status": "pass", "message": f"openai {openai.__version__}"}
    except ImportError:
        return {"status": "fail", "message": "openai not installed. Run: pip install openai"}


def check_chromadb_package() -> Dict:
    """Check chromadb package"""
    try:
        import chromadb
        return {"status": "pass", "message": f"chromadb {chromadb.__version__}"}
    except ImportError:
        return {"status": "fail", "message": "chromadb not installed. Run: pip install chromadb"}


def check_llm_connection() -> Dict:
    """Check LLM service connection"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("API_KEY")
        base_url = os.getenv("BASE_URL")
        
        if not api_key or not base_url:
            return {"status": "fail", "message": "API_KEY or BASE_URL not set"}
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Try to list models
        start = time.time()
        response = client.models.list()
        elapsed = time.time() - start
        
        models = [m.id for m in response.data]
        
        return {
            "status": "pass",
            "message": f"Connected ({elapsed:.2f}s)",
            "details": {"models": ", ".join(models[:3]) + ("..." if len(models) > 3 else "")}
        }
    except Exception as e:
        return {"status": "fail", "message": str(e)[:100]}


def check_embedding_service() -> Dict:
    """Check embedding service"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        
        if not api_key or not base_url:
            return {"status": "fail", "message": "Embedding credentials not set"}
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        start = time.time()
        response = client.embeddings.create(model=model, input=["test"])
        elapsed = time.time() - start
        
        dim = len(response.data[0].embedding)
        
        return {
            "status": "pass",
            "message": f"Working ({elapsed:.2f}s, {dim}D)",
            "details": {"model": model}
        }
    except Exception as e:
        return {"status": "fail", "message": str(e)[:100]}


def check_chroma_db() -> Dict:
    """Check ChromaDB status"""
    try:
        import chromadb
        
        persist_dir = DEFAULT_PERSIST_DIR
        
        if not Path(persist_dir).exists():
            return {"status": "warn", "message": f"Directory not found: {persist_dir}"}
        
        client = chromadb.PersistentClient(path=persist_dir)
        collections = client.list_collections()
        
        if not collections:
            return {"status": "warn", "message": "No collections found. Run: python build_local_index.py"}
        
        # Get document count
        collection = client.get_collection("wangqi_knowledge")
        count = collection.count()

        if count == 0:
            return {
                "status": "warn",
                "message": f"{len(collections)} collection(s), but wangqi_knowledge is empty",
                "details": {"persist_dir": persist_dir}
            }
        
        return {
            "status": "pass",
            "message": f"{len(collections)} collection(s), {count} documents",
            "details": {"persist_dir": persist_dir}
        }
    except Exception as e:
        return {"status": "fail", "message": str(e)[:100]}


def check_knowledge_cards() -> Dict:
    """Check knowledge cards"""
    cards_dir = Path(DEFAULT_CARDS_DIR)
    
    if not cards_dir.exists():
        return {"status": "warn", "message": f"Directory not found: {cards_dir}"}
    
    # Count cards
    paper_cards = list((cards_dir / "papers").glob("*.json")) if (cards_dir / "papers").exists() else []
    exp_cards = list((cards_dir / "experiences").glob("*.json")) if (cards_dir / "experiences").exists() else []
    
    total = len(paper_cards) + len(exp_cards)
    
    if total == 0:
        return {"status": "warn", "message": "No knowledge cards found. Run: python extract_knowledge_cards.py"}
    
    return {
        "status": "pass",
        "message": f"{total} cards ({len(paper_cards)} papers, {len(exp_cards)} experiences)",
        "details": {"path": str(cards_dir)}
    }


def check_skill_file() -> Dict:
    """Check SKILL.md exists"""
    skill_path = Path(DEFAULT_SKILL_PATH)
    
    if skill_path.exists():
        size = skill_path.stat().st_size
        return {"status": "pass", "message": f"{size} bytes"}
    else:
        return {"status": "fail", "message": f"File not found: {skill_path}"}


def check_test_query() -> Dict:
    """Run a test query"""
    try:
        import chromadb
        from openai import OpenAI
        
        # Get embedding
        api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        start = time.time()
        response = client.embeddings.create(model=model, input=["test query"])
        embedding = response.data[0].embedding
        embed_time = time.time() - start
        
        # Query ChromaDB
        persist_dir = DEFAULT_PERSIST_DIR
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        collection = chroma_client.get_collection("wangqi_knowledge")
        
        start = time.time()
        results = collection.query(query_embeddings=[embedding], n_results=3)
        query_time = time.time() - start
        
        return {
            "status": "pass",
            "message": f"Embed: {embed_time:.2f}s, Query: {query_time:.2f}s",
            "details": {"results": len(results["documents"][0])}
        }
    except Exception as e:
        return {"status": "fail", "message": str(e)[:100]}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Health check for Wang Qi Professor TCM Assistant")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Wang Qi Professor TCM Assistant - Health Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    checker = HealthChecker(verbose=args.verbose)
    
    # System checks
    print("[System]")
    checker.check("Python version", check_python_version)
    checker.check("Environment file", check_env_file)
    checker.check("Environment variables", check_env_variables)
    checker.check("Embedding env vars", check_embedding_env)
    print()
    
    # Package checks
    print("[Packages]")
    checker.check("openai package", check_openai_package)
    checker.check("chromadb package", check_chromadb_package)
    print()
    
    # Service checks
    print("[Services]")
    checker.check("LLM service", check_llm_connection)
    checker.check("Embedding service", check_embedding_service)
    print()
    
    # Data checks
    print("[Data]")
    checker.check("ChromaDB", check_chroma_db)
    checker.check("Knowledge cards", check_knowledge_cards)
    checker.check("SKILL.md", check_skill_file)
    print()
    
    # Functional check
    print("[Functional]")
    checker.check("Test query", check_test_query)
    print()
    
    # Summary
    result = checker.summary()
    
    if args.json:
        print()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Exit with error code if any checks failed
    sys.exit(0 if checker.failed == 0 else 1)


if __name__ == "__main__":
    main()
