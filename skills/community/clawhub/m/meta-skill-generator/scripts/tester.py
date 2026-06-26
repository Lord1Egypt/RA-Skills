"""
技能测试器 - 安全沙盒执行
"""

import os
import sys
import time
import json
import traceback
import tempfile
import subprocess
import signal
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class TestCase:
    """测试用例"""
    name: str
    inputs: Dict[str, Any]
    expected: Any
    timeout: int = 5


@dataclass
class TestResult:
    """测试结果"""
    case_name: str
    success: bool
    output: Any
    error: Optional[str]
    execution_time: float
    traceback: Optional[str] = None


class SimpleTester:
    """简单本地测试器（不用 Docker）"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def test_skill(self, code: str, test_cases: List[TestCase]) -> List[TestResult]:
        """在本地环境测试技能"""
        results = []
        
        for case in test_cases:
            result = self._run_single_test(code, case)
            results.append(result)
        
        return results
    
    def _run_single_test(self, code: str, test_case: TestCase) -> TestResult:
        """运行单个测试"""
        start_time = time.time()
        
        # 创建隔离命名空间
        namespace = {
            '__name__': '__test__',
            '__builtins__': __builtins__,
        }
        
        try:
            # 编译代码
            compiled = compile(code, '<skill>', 'exec')
            
            # 执行代码
            exec(compiled, namespace)
            
            # 查找技能类
            skill_class = None
            for name, obj in namespace.items():
                if isinstance(obj, type) and hasattr(obj, 'execute'):
                    skill_class = obj
                    break
            
            if not skill_class:
                return TestResult(
                    case_name=test_case.name,
                    success=False,
                    output=None,
                    error="未找到技能类",
                    execution_time=time.time() - start_time
                )
            
            # 实例化并执行
            skill = skill_class()
            
            # 验证输入
            if hasattr(skill, 'validate_input'):
                if not skill.validate_input(test_case.inputs):
                    return TestResult(
                        case_name=test_case.name,
                        success=False,
                        output=None,
                        error="输入验证失败",
                        execution_time=time.time() - start_time
                    )
            
            # 执行（带超时）
            output = self._execute_with_timeout(
                skill.execute,
                test_case.inputs,
                test_case.timeout or self.timeout
            )
            
            execution_time = time.time() - start_time
            
            # 检查结果
            success = output.get('success', False) if isinstance(output, dict) else True
            
            return TestResult(
                case_name=test_case.name,
                success=success,
                output=output,
                error=None,
                execution_time=execution_time
            )
            
        except subprocess.TimeoutExpired:
            return TestResult(
                case_name=test_case.name,
                success=False,
                output=None,
                error="执行超时",
                execution_time=self.timeout
            )
            
        except Exception as e:
            return TestResult(
                case_name=test_case.name,
                success=False,
                output=None,
                error=str(e),
                traceback=traceback.format_exc(),
                execution_time=time.time() - start_time
            )
    
    def _execute_with_timeout(self, func, args, timeout: int):
        """带超时执行"""
        import threading
        
        result = {}
        exception = [None]
        
        def target():
            try:
                result['value'] = func(**args)
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            raise subprocess.TimeoutExpired("func", timeout)
        
        if exception[0]:
            raise exception[0]
        
        return result.get('value', {})


class DockerTester:
    """Docker 沙盒测试器"""
    
    def __init__(
        self,
        image: str = "python:3.11-slim",
        timeout: int = 10,
        memory_limit: str = "256m",
        cpu_limit: float = 0.5
    ):
        self.image = image
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.client = None
    
    def _get_client(self):
        """获取 Docker 客户端"""
        try:
            import docker
            if not self.client:
                self.client = docker.from_env()
            return self.client
        except ImportError:
            print("⚠️ Docker SDK 未安装，回退到简单测试器")
            return None
        except Exception as e:
            print(f"⚠️ Docker 连接失败: {e}，回退到简单测试器")
            return None
    
    def test_skill(self, code: str, test_cases: List[TestCase]) -> List[TestResult]:
        """在 Docker 容器中测试"""
        client = self._get_client()
        
        if not client:
            # 回退到简单测试器
            tester = SimpleTester(self.timeout)
            return tester.test_skill(code, test_cases)
        
        # 构建测试代码
        test_code = self._build_test_code(code, test_cases)
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(test_code)
            test_file = f.name
        
        try:
            # 拉取镜像（如需要）
            try:
                client.images.get(self.image)
            except:
                print(f"📦 拉取镜像: {self.image}")
                client.images.pull(self.image)
            
            # 运行容器
            container = client.containers.run(
                self.image,
                detach=True,
                mem_limit=self.memory_limit,
                cpu_period=100000,
                cpu_quota=int(100000 * self.cpu_limit),
                security_opt=["no-new-privileges:true"],
                tmpfs={"/tmp": "size=50m,uid=1000"},
                read_only=True,
                network_disabled=True,
            )
            
            try:
                # 上传测试文件
                with open(test_file, 'rb') as f:
                    container.put_archive("/tmp", {"test_runner.py": f.read()})
                
                # 执行测试
                result = container.exec_run(
                    "python /tmp/test_runner.py",
                    stream=False,
                    demux=False,
                    socket=True
                )
                
                # 解析输出
                output = result.output.decode('utf-8')
                
                # 尝试解析 JSON
                try:
                    # 提取 JSON 部分
                    json_start = output.find('```json')
                    json_end = output.rfind('```')
                    
                    if json_start >= 0 and json_end > json_start:
                        json_str = output[json_start+7:json_end]
                        results_data = json.loads(json_str)
                        return self._parse_results(results_data, test_cases)
                except:
                    pass
                
                # 回退：创建简单结果
                return [
                    TestResult(
                        case_name=tc.name,
                        success="error" not in output.lower(),
                        output=output,
                        error=None if "error" not in output.lower() else output[:200],
                        execution_time=1.0
                    )
                    for tc in test_cases
                ]
                
            finally:
                container.remove(force=True)
                
        finally:
            os.unlink(test_file)
    
    def _build_test_code(self, skill_code: str, test_cases: List[TestCase]) -> str:
        """构建测试代码"""
        test_cases_json = json.dumps([
            {
                "name": tc.name,
                "inputs": tc.inputs,
                "expected": str(tc.expected)
            }
            for tc in test_cases
        ])
        
        return f'''
import sys
import json
import traceback

# 技能代码
{skill_code}

# 测试用例
test_cases = {test_cases_json}

results = []

for tc in test_cases:
    result = {{"case_name": tc["name"]}}
    
    try:
        # 查找技能类
        skill_class = None
        for name in dir():
            obj = eval(name) if name in locals() else None
            if isinstance(obj, type) and hasattr(obj, "execute"):
                skill_class = obj
                break
        
        if not skill_class:
            result["success"] = False
            result["error"] = "No skill class found"
        else:
            skill = skill_class()
            output = skill.execute(**tc["inputs"])
            result["success"] = output.get("success", True)
            result["output"] = str(output)
            
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
    
    results.append(result)

print("```json")
print(json.dumps(results, indent=2))
print("```")
'''
    
    def _parse_results(self, data: List[Dict], test_cases: List[TestCase]) -> List[TestResult]:
        """解析测试结果"""
        results = []
        
        for tc, res in zip(test_cases, data):
            results.append(TestResult(
                case_name=res.get('case_name', tc.name),
                success=res.get('success', False),
                output=res.get('output'),
                error=res.get('error'),
                execution_time=1.0,
                traceback=res.get('traceback')
            ))
        
        return results


def create_tester(use_docker: bool = True, **kwargs) -> Any:
    """创建测试器实例"""
    if use_docker:
        return DockerTester(**kwargs)
    else:
        return SimpleTester(**kwargs)


if __name__ == "__main__":
    # 测试
    code = '''
class TestSkill:
    def execute(self, name="World"):
        return {"success": True, "result": f"Hello, {name}!"}
    
    def validate_input(self, inputs):
        return True
    
    def handle_error(self, error):
        return {"success": False, "error": str(error)}
'''
    
    tester = SimpleTester()
    results = tester.test_skill(code, [
        TestCase("test1", {"name": "Alice"}, "Hello, Alice!"),
        TestCase("test2", {"name": "Bob"}, "Hello, Bob!")
    ])
    
    for r in results:
        print(f"{r.case_name}: {'✅' if r.success else '❌'} - {r.error or r.output}")
