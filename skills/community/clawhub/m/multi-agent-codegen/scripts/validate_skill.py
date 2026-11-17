#!/usr/bin/env python3
"""
multi-agent-codegen 健康检查 + dry-run 测试
============================================

验证维度：
1. 文件结构（所有关键文件存在）
2. 依赖完整性（venv + requirements）
3. 代码 import 可用性
4. 关键配置（API Key、open_id、通知开关）
5. dry-run 测试（mock LLM + 关闭飞书通知，跑完整流水线）
6. Verify Agent 验证产物（独立脚本能跑）

用法：
    .venv/bin/python scripts/validate_skill.py [--no-notify] [--skip-demo]
"""
from __future__ import annotations

import os
import sys
import json
import importlib.util
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENV_DIR = SKILL_DIR / ".venv"


class HealthCheck:
    """健康检查执行器"""
    def __init__(self):
        self.results = []  # (level, name, passed, message)

    def add(self, name: str, passed: bool, message: str = ""):
        self.results.append((name, passed, message))
        emoji = "✅" if passed else "❌"
        print(f"{emoji} {name}: {message}")

    def summary(self):
        total = len(self.results)
        passed = sum(1 for _, p, _ in self.results if p)
        print("\n" + "=" * 60)
        print(f"📊 总览: {passed}/{total} 通过")
        if passed == total:
            print("🏆 全部通过 — 技能健康！")
        else:
            print(f"⚠️ {total - passed} 项失败 — 需要修复")
        print("=" * 60)
        return passed == total


def check_file_structure() -> bool:
    """1. 文件结构检查"""
    print("\n━━━ [1/8] 文件结构检查 ━━━━━")
    required = {
        "SKILL.md": SKILL_DIR / "SKILL.md",
        "skill.json": SKILL_DIR / "skill.json",
        "_meta.json": SKILL_DIR / "_meta.json",
        "requirements.txt": SKILL_DIR / "requirements.txt",
        "scripts/multi_codegen.py": SCRIPTS_DIR / "multi_codegen.py",
        "scripts/verify_agent.py": SCRIPTS_DIR / "verify_agent.py",
        "scripts/cli.sh": SCRIPTS_DIR / "cli.sh",
        "scripts/validate_skill.py": SCRIPTS_DIR / "validate_skill.py",
        ".venv/bin/python": VENV_DIR / "bin" / "python",
        ".clawhub/origin.json": SKILL_DIR / ".clawhub" / "origin.json",
    }
    ok = True
    for name, path in required.items():
        if path.exists():
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} 缺失: {path}")
            ok = False
    return ok


def check_version_consistency() -> bool:
    """2. 版本号一致性检查（v3.1 新增）

    skill.json 版本号 必须 == SKILL.md 里 "版本:" 字段
    """
    print("\n━━━ [2/8] 版本号一致性 ━━━━")
    import re

    # 读 skill.json 版本
    try:
        skill_json = json.loads((SKILL_DIR / "skill.json").read_text())
        json_ver = skill_json.get("version", "?")
    except Exception as e:
        print(f"  ❌ skill.json 读失败: {e}")
        return False

    # 读 SKILL.md 顶部 + 底部 版本
    skill_md = (SKILL_DIR / "SKILL.md").read_text()
    # 顶部: "> **4 Agent 软件工程协作流水线 v3.1.0**" - 只取第一个（避免被中间的 v3.0/v3.1 干扰）
    md_top_match = re.search(r"^>.*?v(\d+(?:\.\d+)+)\*\*", skill_md, re.MULTILINE)
    # 底部: *版本: v3.1.0* (斜体)
    md_bottom_match = re.search(r"\*?版本[::]\s*v?([\d.]+)", skill_md)
    md_top = md_top_match.group(1) if md_top_match else None
    md_bottom = md_bottom_match.group(1) if md_bottom_match else None

    ok = True
    print(f"  📋 skill.json: v{json_ver}")
    print(f"  📋 SKILL.md 顶部: v{md_top}")
    print(f"  📋 SKILL.md 底部 '版本:': v{md_bottom}")

    if json_ver == md_top == md_bottom:
        print(f"  ✅ 版本号完全一致")
    else:
        print(f"  ❌ 版本号不一致")
        ok = False

    return ok


def check_dependencies() -> bool:
    """2. 依赖完整性"""
    print("\n━━━ [3/8] 依赖完整性 ━━━━━")
    venv_py = VENV_DIR / "bin" / "python"
    if not venv_py.exists():
        print(f"  ❌ venv 不存在: {venv_py}")
        return False

    required_pkgs = ["langgraph", "langchain_anthropic", "anthropic"]
    try:
        import importlib.util
        import subprocess
        # 注意包名映射（pip 名 vs import 名）
        pkg_to_import = {
            "langgraph": "langgraph",
            "langchain_anthropic": "langchain_anthropic",  # import 用下划线
            "anthropic": "anthropic",
        }
        ok = True
        for pkg in required_pkgs:
            import_name = pkg_to_import.get(pkg, pkg)
            spec = importlib.util.find_spec(import_name)
            if spec is None:
                print(f"  ❌ {pkg}: 未安装")
                ok = False
                continue
            # 用 pip show 拿版本
            r = subprocess.run(
                [str(venv_py), "-m", "pip", "show", import_name],
                capture_output=True, text=True,
            )
            ver = "?"
            for line in r.stdout.splitlines():
                if line.startswith("Version:"):
                    ver = line.split(":", 1)[1].strip()
            print(f"  ✅ {pkg}: {ver}")
        return ok
    except Exception as e:
        print(f"  ❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_imports() -> bool:
    """3. 代码 import 可用性"""
    print("\n━━━ [4/8] 代码 import ━━━━━")
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import multi_codegen
        print(f"  ✅ multi_codegen 导入成功")
        print(f"     - PlanAgent: {multi_codegen.PlanAgent.__name__}")
        print(f"     - WriteAgent: {multi_codegen.WriteAgent.__name__}")
        print(f"     - TestAgent: {multi_codegen.TestAgent.__name__}")
        print(f"     - RefineAgent: {multi_codegen.RefineAgent.__name__}")
        print(f"     - Pipeline: {multi_codegen.Pipeline.__name__}")
        print(f"     - NOTIFY_ENABLED: {multi_codegen.NOTIFY_ENABLED}")
        print(f"     - FEISHU_USER_OPEN_ID: {multi_codegen.FEISHU_USER_OPEN_ID}")

        import verify_agent
        print(f"  ✅ verify_agent 导入成功")
        print(f"     - VerifyAgent: {verify_agent.VerifyAgent.__name__}")
        print(f"     - DEFAULT_MIN_CHARS: {verify_agent.VerifyAgent.DEFAULT_MIN_CHARS}")

        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_l4_verify_integration() -> bool:
    """5. L4 Verify Agent 是否接入主流水线（v3.1 + v3.2 + v3.3）

    v3.1: Write Verify
    v3.2: SyntaxError hard fail retry
    v3.3: Test Verify 接入
    """
    print("\n━━━ [5/8] L4 Verify Agent 接入检查 (v3.1+v3.2+v3.3) ━━━━")
    sys.path.insert(0, str(SCRIPTS_DIR))
    import multi_codegen
    import inspect

    ok = True

    # ===== v3.1 检查 =====

    # 检查 1: Pipeline 有 _run_verify_step 方法
    if hasattr(multi_codegen.Pipeline, "_run_verify_step"):
        print(f"  ✅ Pipeline._run_verify_step 方法存在")
    else:
        print(f"  ❌ Pipeline 缺 _run_verify_step 方法（未接入 L4 Verify）")
        ok = False

    # 检查 2: Pipeline.__init__ 有 enable_verify 参数
    sig = inspect.signature(multi_codegen.Pipeline.__init__)
    if "enable_verify" in sig.parameters and "max_verify_retries" in sig.parameters:
        print(f"  ✅ Pipeline.__init__ 支持 enable_verify + max_verify_retries")
    else:
        print(f"  ❌ Pipeline.__init__ 缺参数")
        ok = False

    # 检查 3: State TypedDict 有 verify_feedback 字段
    state_keys = multi_codegen.State.__annotations__.keys()
    if "verify_feedback" in state_keys and "verify_retry_count" in state_keys:
        print(f"  ✅ State 有 verify_feedback + verify_retry_count 字段")
    else:
        print(f"  ❌ State 缺 verify 字段")
        ok = False

    # 检查 4: notify_verify_done 函数存在
    if hasattr(multi_codegen, "notify_verify_done"):
        print(f"  ✅ notify_verify_done 函数存在")
    else:
        print(f"  ❌ 缺 notify_verify_done 通知函数")
        ok = False

    # 检查 5: WriteAgent.run() 调用了 verify_feedback
    write_src = inspect.getsource(multi_codegen.WriteAgent.run)
    if "verify_feedback" in write_src:
        print(f"  ✅ WriteAgent.run() 注入了 verify_feedback")
    else:
        print(f"  ❌ WriteAgent.run() 未注入 verify_feedback")
        ok = False

    # ===== v3.2 检查 =====

    # 检查 6: Pipeline 有 _classify_failure 方法（hard/soft 分类）
    if hasattr(multi_codegen.Pipeline, "_classify_failure"):
        print(f"  ✅ Pipeline._classify_failure 方法存在 (v3.2 hard/soft 分类)")
    else:
        print(f"  ❌ Pipeline 缺 _classify_failure 方法（v3.2 未实施）")
        ok = False

    # 检查 7: max_hard_retries 参数存在且默认 5
    if "max_hard_retries" in sig.parameters:
        default = sig.parameters["max_hard_retries"].default
        if default == 5:
            print(f"  ✅ Pipeline.__init__ 有 max_hard_retries={default} (v3.2)")
        else:
            print(f"  ⚠️ max_hard_retries 默认值是 {default}，推荐 5")
    else:
        print(f"  ❌ Pipeline.__init__ 缺 max_hard_retries 参数")
        ok = False

    # 检查 8: max_verify_retries 默认值应该是 3（v3.2: 2→3）
    if sig.parameters["max_verify_retries"].default == 3:
        print(f"  ✅ max_verify_retries 默认值 = 3 (v3.2: 2→3)")
    else:
        default = sig.parameters["max_verify_retries"].default
        print(f"  ⚠️ max_verify_retries 默认值是 {default}，v3.2 推荐 3")
        ok = False

    # 检查 9: State 有 syntax_retry_count 字段
    if "syntax_retry_count" in state_keys:
        print(f"  ✅ State.syntax_retry_count 字段存在 (v3.2 hard fail 独立计数)")
    else:
        print(f"  ❌ State 缺 syntax_retry_count 字段（v3.2 未实施）")
        ok = False

    # 检查 10: _run_verify_step 返回 tuple[bool, str]
    verify_src = inspect.getsource(multi_codegen.Pipeline._run_verify_step)
    if "tuple[bool, str]" in verify_src or 'return True, "' in verify_src or 'return False, "' in verify_src:
        print(f"  ✅ _run_verify_step 返回 tuple[bool, str] (v3.2 设计)")
    else:
        print(f"  ❌ _run_verify_step 未升级到 tuple 返回")
        ok = False

    # ===== v3.3 检查 =====

    # 检查 11: Pipeline 有 _run_test_verify_step 方法
    if hasattr(multi_codegen.Pipeline, "_run_test_verify_step"):
        print(f"  ✅ Pipeline._run_test_verify_step 方法存在 (v3.3 新增)")
    else:
        print(f"  ❌ Pipeline 缺 _run_test_verify_step 方法（v3.3 未实施）")
        ok = False

    # 检查 12: max_test_verify_retries 参数存在且默认 3
    if "max_test_verify_retries" in sig.parameters:
        default = sig.parameters["max_test_verify_retries"].default
        if default == 3:
            print(f"  ✅ Pipeline.__init__ 有 max_test_verify_retries={default} (v3.3)")
        else:
            print(f"  ⚠️ max_test_verify_retries 默认值是 {default}，v3.3 推荐 3")
    else:
        print(f"  ❌ Pipeline.__init__ 缺 max_test_verify_retries 参数")
        ok = False

    # 检查 13: State 有 verify_test_feedback + test_verify_retry_count + test_syntax_retry_count
    v33_fields = ["verify_test_feedback", "test_verify_retry_count", "test_syntax_retry_count"]
    missing_fields = [f for f in v33_fields if f not in state_keys]
    if not missing_fields:
        print(f"  ✅ State 有 v3.3 字段 ({len(v33_fields)} 个: verify_test_feedback/test_verify_retry_count/test_syntax_retry_count)")
    else:
        print(f"  ❌ State 缺 v3.3 字段: {missing_fields}")
        ok = False

    # 检查 14: notify_test_verify_done 函数存在
    if hasattr(multi_codegen, "notify_test_verify_done"):
        print(f"  ✅ notify_test_verify_done 函数存在 (v3.3 新增)")
    else:
        print(f"  ❌ 缺 notify_test_verify_done 通知函数")
        ok = False

    # 检查 15: TestAgent.run() 调用了 verify_test_feedback
    test_src = inspect.getsource(multi_codegen.TestAgent.run)
    if "verify_test_feedback" in test_src:
        print(f"  ✅ TestAgent.run() 注入了 verify_test_feedback (v3.3)")
    else:
        print(f"  ❌ TestAgent.run() 未注入 verify_test_feedback")
        ok = False

    return ok


def check_config() -> bool:
    """4. 配置检查"""
    print("\n━━━ [6/8] 配置检查 ━━━━━")
    api_key = os.environ.get("EM_API_KEY") or os.environ.get("MINIMAX_API_KEY")
    print(f"  {'✅' if api_key else '❌'} API Key (EM_API_KEY/MINIMAX_API_KEY): {'已设置' if api_key else '未设置'}")

    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if not config_path.exists():
        print(f"  ❌ openclaw.json 不存在: {config_path}")
        return False
    try:
        with open(config_path) as f:
            cfg = json.load(f)
        feishu_cfg = cfg.get("channels", {}).get("feishu", {})
        codebot = feishu_cfg.get("accounts", {}).get("codebot", {})
        app_id = codebot.get("appId")
        app_secret = codebot.get("appSecret")
        print(f"  {'✅' if app_id else '❌'} 飞书 appId: {'已配置' if app_id else '缺失'}")
        print(f"  {'✅' if app_secret else '❌'} 飞书 appSecret: {'已配置' if app_secret else '缺失'}")
        return bool(api_key and app_id and app_secret)
    except Exception as e:
        print(f"  ❌ 配置读取失败: {e}")
        return False


def check_dry_run() -> bool:
    """5. dry-run 测试：用 Mock LLM + 关闭通知跑完整流水线"""
    print("\n━━━ [7/8] dry-run (Mock LLM + 关闭通知) ━━━━━")
    sys.path.insert(0, str(SCRIPTS_DIR))
    import multi_codegen

    # 关闭飞书通知
    original_notify = multi_codegen.NOTIFY_ENABLED
    multi_codegen.NOTIFY_ENABLED = False

    # Mock LLM
    class MockLLM:
        def invoke(self, prompt):
            # 根据 prompt 判断返回什么内容
            if "Plan Agent" in prompt or "架构设计" in prompt:
                return type("Resp", (), {"content": _mock_plan()})()
            elif "Write Agent" in prompt or "完整可运行" in prompt:
                return type("Resp", (), {"content": _mock_code()})()
            elif "Test Agent" in prompt or "pytest 测试" in prompt:
                return type("Resp", (), {"content": _mock_tests()})()
            else:
                # Refine
                return type("Resp", (), {"content": _mock_refine()})()

    try:
        agents = [
            multi_codegen.PlanAgent(),
            multi_codegen.WriteAgent(),
            multi_codegen.TestAgent(),
            multi_codegen.RefineAgent(),
        ]
        pipeline = multi_codegen.Pipeline(agents, max_retries=1, threshold=70)
        mock_llm = MockLLM()
        result = pipeline.run("做个命令行 todo 工具", mock_llm, "/tmp/dryrun_output")
        print(f"  ✅ Pipeline 完成（mock 模式）")
        print(f"     - plan: {len(result['plan'])} 字")
        print(f"     - code: {len(result['code'])} 字")
        print(f"     - tests: {len(result['tests'])} 字")
        print(f"     - refine: {len(result['refine_feedback'])} 字")
        print(f"     - 评分: {result['quality_score']}/100")
        print(f"     - 迭代: {result['retry_count']} 次")
        return True
    except Exception as e:
        print(f"  ❌ Pipeline 失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        multi_codegen.NOTIFY_ENABLED = original_notify


def check_verify_agent() -> bool:
    """6. Verify Agent 独立测试"""
    print("\n━━━ [8/8] Verify Agent 独立运行 ━━━━")
    sys.path.insert(0, str(SCRIPTS_DIR))
    from verify_agent import VerifyAgent, verify_file

    all_pass = True

    # 测试 1: 完整代码应通过（必须有足够 keyword density > 0.1）
    # 关键: keyword_density = (class+def+import+from) / 非空行
    # 必须用足够多的 def/class 而不是 # 注释行填充
    full_code = '''#!/usr/bin/env python3
"""Demo module for verification."""
import os
import sys
import json
from pathlib import Path

class Demo:
    """Demo class."""
    def __init__(self, name):
        """Initialize with name."""
        self.name = name

    def run(self):
        """Run demo."""
        return f"Hello, {self.name}!"

    def transform(self, data):
        """Transform data."""
        return [d * 2 for d in data]

class Helper:
    """Helper class for demo."""
    def __init__(self):
        self.items = []

    def add(self, item):
        """Add item."""
        self.items.append(item)

    def get_all(self):
        """Get all items."""
        return list(self.items)

def parse_input(text):
    """Parse user input."""
    return text.strip().lower()

def format_output(data):
    """Format output."""
    return json.dumps(data, ensure_ascii=False)

def main():
    """Main entry."""
    d = Demo("world")
    h = Helper()
    h.add({"id": 1, "value": d.name})
    print(d.run())
    print(format_output(h.get_all()))
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    # 用更多 def 补足到 3000 字（保密度）
    pad = []
    i = 0
    while len(full_code) + sum(len(p) for p in pad) < 3200:
        pad.append(f"def utility_{i}():\n    \"\"\"Utility function {i}.\"\"\"\n    import math\n    return math.sqrt({i})\n\n")
        i += 1
    full_code += "".join(pad)
    agent = VerifyAgent(min_chars=3000)
    r = agent.verify(full_code, "code.py")
    test1_pass = r.passed
    all_pass = all_pass and test1_pass
    print(f"  {'✅' if test1_pass else '❌'} 完整代码通过验证（实际 {r.metrics['actual_chars']} 字, 密度 {r.metrics['keyword_density']}）")
    if not test1_pass:
        print(f"     失败原因: {r.failures}")

    # 测试 2: 太短的代码应失败
    short_code = "def foo(): pass\n"
    r = agent.verify(short_code, "code.py")
    test2_pass = not r.passed
    all_pass = all_pass and test2_pass
    print(f"  {'✅' if test2_pass else '❌'} 太短代码被拒（检测到 {len(r.failures)} 个问题）")

    # 测试 3: 占位符应失败
    placeholder_code = '''#!/usr/bin/env python3
"""Module with TODO."""
import os
# TODO: implement this
class Foo:
    def __init__(self):
        pass
def main():
    pass
if __name__ == "__main__":
    main()
'''
    placeholder_code += "\n# " + ("padding\n" * 250)
    r = agent.verify(placeholder_code, "code.py")
    test3_pass = not r.passed
    all_pass = all_pass and test3_pass
    print(f"  {'✅' if test3_pass else '❌'} 占位符代码被拒（检测到 {len(r.failures)} 个问题）")
    if r.failures:
        print(f"     失败原因示例: {r.failures[0][:80]}...")

    return all_pass


def _mock_plan() -> str:
    """Mock plan 输出"""
    return """# Todo CLI 架构设计

## 数据模型
- TodoStore 类: items (list), next_id (int)
- Item: id, title, done

## 核心接口
- add_item(title): str (返回 id)
- list_items() -> list
- complete_item(id) -> bool
- delete_item(id) -> bool

## 测试要点
1. 添加 + 列出
2. 完成 + 列表过滤
3. 边界 (空 list, 无效 id)
"""

def _mock_code() -> str:
    """Mock code 输出（满足 verify agent 3000 字硬下限 + 关键词密度 > 0.1）

    验证: 关键字密度 = (class+def+import+from) / 非空行
    要让密度 > 0.1，需要更多 def/class，而不是注释行。
    """
    # 用更多 def 来增加密度
    extras = []
    for i in range(8):
        extras.append(f"""
def helper_{i}(data):
    \"\"\"Helper function {i}.\"\"\"
    import json as _json_{i}
    return _json_{i}.dumps(data)

class Util_{i}:
    \"\"\"Utility class {i}.\"\"\"
    def __init__(self):
        self.value = {i}

    def transform(self, data):
        \"\"\"Transform data.\"\"\"
        return [d * 2 for d in data]

    def validate(self, item):
        \"\"\"Validate item.\"\"\"
        return bool(item)
""")
    base = '''#!/usr/bin/env python3
"""Todo CLI - simple todo list tool."""
import argparse
import json
from pathlib import Path

class TodoStore:
    """Stores todos in memory with persistence to JSON."""
    def __init__(self, path=None):
        self.path = path or Path.home() / ".todo.json"
        self.next_id = 1
        self.items = []
        self.load()

    def load(self):
        if self.path.exists():
            data = json.loads(self.path.read_text())
            self.items = data.get("items", [])
            self.next_id = data.get("next_id", 1)

    def save(self):
        data = {"items": self.items, "next_id": self.next_id}
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def add_item(self, title):
        item = {"id": self.next_id, "title": title, "done": False}
        self.items.append(item)
        self.next_id += 1
        self.save()
        return item["id"]

    def list_items(self, show_done=True):
        if show_done:
            return self.items
        return [i for i in self.items if not i["done"]]

    def complete_item(self, item_id):
        for item in self.items:
            if item["id"] == item_id:
                item["done"] = True
                self.save()
                return True
        return False

    def delete_item(self, item_id):
        before = len(self.items)
        self.items = [i for i in self.items if i["id"] != item_id]
        if len(self.items) < before:
            self.save()
            return True
        return False

    def count_pending(self):
        return len([i for i in self.items if not i["done"]])

    def clear_all(self):
        self.items = []
        self.save()

    def find_by_id(self, item_id):
        for item in self.items:
            if item["id"] == item_id:
                return item
        return None
''' + "".join(extras) + '''
def main():
    parser = argparse.ArgumentParser(description="Simple Todo CLI")
    parser.add_argument("--storage", help="Path to JSON storage")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new todo")
    add_p.add_argument("title", help="Todo title")

    list_p = subparsers.add_parser("list", help="List todos")
    list_p.add_argument("--all", action="store_true", help="Show all")

    done_p = subparsers.add_parser("done", help="Mark as done")
    done_p.add_argument("id", type=int)

    del_p = subparsers.add_parser("delete", help="Delete a todo")
    del_p.add_argument("id", type=int)

    args = parser.parse_args()
    store = TodoStore(args.storage)

    if args.command == "add":
        new_id = store.add_item(args.title)
        print(f"Added #{new_id}: {args.title}")
    elif args.command == "list":
        for item in store.list_items(show_done=args.all):
            mark = "X" if item["done"] else " "
            print(f"  [{mark}] #{item['id']} {item['title']}")
    elif args.command == "done":
        ok = store.complete_item(args.id)
        print("Done" if ok else "Not found")
    elif args.command == "delete":
        ok = store.delete_item(args.id)
        print("Deleted" if ok else "Not found")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
'''
    # 确保长度 >= 3000 字
    while len(base) < 3200:
        base += "\n# Module doc\n"
    return f"```python\n{base}\n```"


def _mock_tests() -> str:
    """Mock tests 输出"""
    base = '''#!/usr/bin/env python3
"""Pytest tests for TodoStore."""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from code import TodoStore

@pytest.fixture
def store(tmp_path):
    return TodoStore(path=tmp_path / "todo.json")

def test_add_item(store):
    new_id = store.add_item("Buy milk")
    assert new_id == 1
    assert len(store.items) == 1

def test_list_items(store):
    store.add_item("A")
    store.add_item("B")
    items = store.list_items()
    assert len(items) == 2

def test_complete_item(store):
    store.add_item("A")
    store.complete_item(1)
    assert store.items[0]["done"] is True

def test_delete_item(store):
    store.add_item("A")
    ok = store.delete_item(1)
    assert ok
    assert len(store.items) == 0

def test_complete_nonexistent(store):
    assert store.complete_item(999) is False

def test_delete_nonexistent(store):
    assert store.delete_item(999) is False

def test_persistence(tmp_path):
    p = tmp_path / "todo.json"
    s1 = TodoStore(path=p)
    s1.add_item("Persistent")
    s2 = TodoStore(path=p)
    assert len(s2.items) == 1

def test_list_done_filter(store):
    store.add_item("A")
    store.complete_item(1)
    pending = store.list_items(show_done=False)
    assert len(pending) == 0
'''
    while len(base) < 5200:
        base += "\n# extra docstring\n"
    return f"```python\n{base}\n```"


def _mock_refine() -> str:
    """Mock refine 输出"""
    return """严重问题：
- critical: 无
- major: 无
- minor: 命名一致性可改进

评分：85
理由：代码完整，测试覆盖度好，单文件实现。

意见：
1. 建议 add_item 返回详细的对象而非只 id
2. list_items 默认应 hide done
3. 缺一个 --clear 命令清空所有
4. error handling 可更细
5. docstring 可补充参数说明"""


def main():
    print("🐛 multi-agent-codegen 健康检查")
    print("=" * 60)
    print(f"📍 技能目录: {SKILL_DIR}")
    print(f"📍 venv: {VENV_DIR}")
    print()

    hc = HealthCheck()
    hc.add("文件结构", check_file_structure())
    hc.add("版本号一致性 (v3.1)", check_version_consistency())
    hc.add("依赖完整性", check_dependencies())
    hc.add("代码 import", check_imports())
    hc.add("L4 Verify 接入 (v3.1)", check_l4_verify_integration())
    hc.add("配置检查", check_config())
    hc.add("dry-run 流水线", check_dry_run())
    hc.add("Verify Agent", check_verify_agent())

    all_passed = hc.summary()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()