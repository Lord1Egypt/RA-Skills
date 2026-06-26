#!/usr/bin/env python3
"""
OpenClaw 工具链配置专家系统
THE TOOLCHAIN EXPERT - 专业的工具集成与API接入

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

功能：
1. 内置工具使用指南
2. 第三方 API 接入
3. 自定义工具开发
4. 工具链编排技巧
5. 工具配置模板
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# =============================================================================
# 内置工具库
# =============================================================================

class BuiltInTools:
    """OpenClaw 内置工具库"""

    # 搜索工具
    SEARCH_TOOLS = {
        "google_search": {
            "name": "Google 搜索",
            "description": "使用 Google 搜索获取信息",
            "category": "search",
            "parameters": {
                "query": {"type": "string", "required": True, "description": "搜索关键词"},
                "num_results": {"type": "integer", "default": 10, "description": "返回结果数量"}
            },
            "output": {"type": "array", "description": "搜索结果列表"},
            "example": {
                "input": {"query": "OpenClaw AI agent", "num_results": 5},
                "output": [{"title": "...", "url": "...", "snippet": "..."}]
            }
        },
        "bing_search": {
            "name": "Bing 搜索",
            "description": "使用 Bing 搜索获取信息",
            "category": "search",
            "parameters": {
                "query": {"type": "string", "required": True}
            }
        },
        "ddg_search": {
            "name": "DuckDuckGo 搜索",
            "description": "使用 DuckDuckGo 搜索（无需 API Key）",
            "category": "search",
            "parameters": {
                "query": {"type": "string", "required": True},
                "max_results": {"type": "integer", "default": 10}
            }
        }
    }

    # 网络工具
    WEB_TOOLS = {
        "web_fetch": {
            "name": "网页抓取",
            "description": "抓取网页内容",
            "category": "web",
            "parameters": {
                "url": {"type": "string", "required": True, "description": "网页 URL"},
                "selector": {"type": "string", "description": "CSS 选择器"}
            },
            "output": {"type": "string", "description": "网页内容"}
        },
        "web_screenshot": {
            "name": "网页截图",
            "description": "对网页进行截图",
            "category": "web",
            "parameters": {
                "url": {"type": "string", "required": True},
                "width": {"type": "integer", "default": 1920},
                "height": {"type": "integer", "default": 1080}
            }
        }
    }

    # 计算工具
    CALCULATOR_TOOLS = {
        "calculator": {
            "name": "计算器",
            "description": "执行数学计算",
            "category": "utility",
            "parameters": {
                "expression": {"type": "string", "required": True, "description": "数学表达式"},
                "precision": {"type": "integer", "default": 2, "description": "小数精度"}
            },
            "output": {"type": "number", "description": "计算结果"}
        },
        "code_interpreter": {
            "name": "代码执行器",
            "description": "执行 Python/JS 代码",
            "category": "utility",
            "parameters": {
                "language": {"type": "string", "enum": ["python", "javascript"], "required": True},
                "code": {"type": "string", "required": True},
                "timeout": {"type": "integer", "default": 30}
            },
            "output": {"type": "object", "description": "执行结果"}
        }
    }

    # 数据工具
    DATA_TOOLS = {
        "json_parser": {
            "name": "JSON 解析",
            "description": "解析和操作 JSON 数据",
            "category": "data",
            "parameters": {
                "data": {"type": "string", "required": True},
                "operation": {"type": "string", "enum": ["parse", "get", "set", "transform"]},
                "path": {"type": "string", "description": "JSONPath"}
            }
        },
        "csv_processor": {
            "name": "CSV 处理",
            "description": "处理 CSV 数据",
            "category": "data",
            "parameters": {
                "data": {"type": "string", "required": True},
                "operation": {"type": "string", "enum": ["read", "write", "filter", "aggregate"]},
                "options": {"type": "object"}
            }
        }
    }

    # 文件工具
    FILE_TOOLS = {
        "file_read": {
            "name": "读取文件",
            "description": "读取本地文件内容",
            "category": "file",
            "parameters": {
                "path": {"type": "string", "required": True},
                "encoding": {"type": "string", "default": "utf-8"}
            }
        },
        "file_write": {
            "name": "写入文件",
            "description": "写入内容到文件",
            "category": "file",
            "parameters": {
                "path": {"type": "string", "required": True},
                "content": {"type": "string", "required": True},
                "append": {"type": "boolean", "default": False}
            }
        }
    }

    @classmethod
    def get_all_tools(cls) -> Dict:
        """获取所有内置工具"""
        all_tools = {}
        for category in [cls.SEARCH_TOOLS, cls.WEB_TOOLS, cls.CALCULATOR_TOOLS, 
                        cls.DATA_TOOLS, cls.FILE_TOOLS]:
            all_tools.update(category)
        return all_tools

    @classmethod
    def get_tools_by_category(cls, category: str) -> Dict:
        """按分类获取工具"""
        category_map = {
            "search": cls.SEARCH_TOOLS,
            "web": cls.WEB_TOOLS,
            "utility": cls.CALCULATOR_TOOLS,
            "data": cls.DATA_TOOLS,
            "file": cls.FILE_TOOLS
        }
        return category_map.get(category, {})


# =============================================================================
# API 接入模板
# =============================================================================

class APITemplates:
    """API 接入模板库"""

    # REST API 通用模板
    REST_API_TEMPLATE = """
{
  "type": "tool",
  "name": "{tool_name}",
  "description": "{description}",
  "provider": "custom_api",
  "config": {{
    "base_url": "{base_url}",
    "auth": {{
      "type": "{auth_type}",  // none / api_key / bearer / basic / oauth
      "key": "{api_key}",
      "prefix": "{token_prefix}"
    }},
    "endpoints": {{
      "{endpoint_name}": {{
        "method": "{method}",  // GET / POST / PUT / DELETE
        "path": "{path}",
        "parameters": {{
{parameters}
        }},
        "headers": {{}},
        "body_template": {body_template}
      }}
    }},
    "response_mapping": {{
      "result_path": "{result_path}",
      "error_path": "{error_path}"
    }}
  }}
}}
"""

    # 常用 API 配置模板
    COMMON_APIS = {
        "weather": {
            "name": "天气查询",
            "base_url": "https://api.weather.example.com",
            "auth_type": "api_key",
            "auth_key": "X-API-Key",
            "endpoints": {
                "current": {
                    "method": "GET",
                    "path": "/v1/current",
                    "params": ["city", "lang"]
                }
            }
        },
        "translate": {
            "name": "翻译服务",
            "base_url": "https://api.translate.example.com",
            "auth_type": "api_key",
            "auth_key": "Authorization",
            "auth_prefix": "Bearer",
            "endpoints": {
                "translate": {
                    "method": "POST",
                    "path": "/v1/translate",
                    "body": {
                        "text": "{{text}}",
                        "source_lang": "{{source}}",
                        "target_lang": "{{target}}"
                    }
                }
            }
        },
        "email": {
            "name": "邮件发送",
            "base_url": "https://api.email.example.com",
            "auth_type": "api_key",
            "auth_key": "X-API-Key",
            "endpoints": {
                "send": {
                    "method": "POST",
                    "path": "/v1/send",
                    "body": {
                        "to": "{{to}}",
                        "subject": "{{subject}}",
                        "body": "{{body}}"
                    }
                }
            }
        },
        "sms": {
            "name": "短信发送",
            "base_url": "https://api.sms.example.com",
            "auth_type": "basic",
            "endpoints": {
                "send": {
                    "method": "POST",
                    "path": "/v1/send",
                    "body": {
                        "phone": "{{phone}}",
                        "message": "{{message}}"
                    }
                }
            }
        }
    }


# =============================================================================
# 自定义工具开发模板
# =============================================================================

class CustomToolTemplates:
    """自定义工具开发模板"""

    # Python 工具模板
    PYTHON_TOOL_TEMPLATE = '''
"""自定义工具: {tool_name}"""

from typing import Dict, Any, Optional
from openclaw import BaseTool, ToolParameter


class {ToolClassName}(BaseTool):
    """{tool_description}"""
    
    name = "{tool_name}"
    description = "{tool_description}"
    category = "{category}"
    
    parameters = [
        ToolParameter(
            name="{param_name}",
            type="string",
            description="{param_description}",
            required={required}
        )
    ]
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具逻辑
        
        Args:
            params: 包含所有输入参数的字典
            
        Returns:
            包含执行结果的字典
        """
        # 获取参数
        {param_name} = params.get("{param_name}")
        
        try:
            # 工具逻辑
            result = self._do_something({param_name})
            
            return {{
                "success": True,
                "result": result
            }}
        except Exception as e:
            return {{
                "success": False,
                "error": str(e)
            }}
    
    def _do_something(self, input_value) -> Any:
        """核心业务逻辑"""
        # TODO: 实现具体逻辑
        pass


# 注册工具
tool = {ToolClassName}()
'''

    # JavaScript 工具模板
    JAVASCRIPT_TOOL_TEMPLATE = '''
/**
 * 自定义工具: {tool_name}
 */

class {ToolClassName} {{
    static get name() {{ return "{tool_name}"; }}
    static get description() {{ return "{tool_description}"; }}
    static get category() {{ return "{category}"; }}
    
    static get parameters() {{
        return [
            {{
                name: "{param_name}",
                type: "string",
                description: "{param_description}",
                required: {required}
            }}
        ];
    }}
    
    static async execute(params) {{
        const {{ {param_name} }} = params;
        
        try {{
            const result = await this._doSomething({param_name});
            return {{
                success: true,
                result: result
            }};
        }} catch (error) {{
            return {{
                success: false,
                error: error.message
            }};
        }}
    }}
    
    static async _doSomething(input) {{
        // TODO: 实现具体逻辑
    }}
}}

module.exports = {ToolClassName};
'''

    # API 工具模板（无需代码）
    API_TOOL_TEMPLATE = '''
{
  "type": "tool",
  "name": "{tool_name}",
  "description": "{description}",
  "category": "{category}",
  
  "api": {{
    "base_url": "{base_url}",
    "method": "{method}",
    "path": "{path}",
    "headers": {{
      "Authorization": "Bearer {api_key}",
      "Content-Type": "application/json"
    }},
    "parameters": {{
      "param1": "{{param1}}",
      "param2": "{{param2}}"
    }}
  }},
  
  "input_schema": {{
    "param1": {{"type": "string", "required": true}},
    "param2": {{"type": "integer", "required": false}}
  }},
  
  "output_schema": {{
    "result": {{"type": "string"}},
    "status": {{"type": "string"}}
  }},
  
  "error_handling": {{
    "retry": {{"enabled": true, "max_attempts": 3}},
    "timeout": 30
  }}
}
'''


# =============================================================================
# 工具链编排专家
# =============================================================================

class ToolChainExpert:
    """
    工具链编排专家
    
    提供专业级的工具集成和编排服务
    """

    def __init__(self):
        self.builtin_tools = BuiltInTools()
        self.api_templates = APITemplates()
        self.custom_templates = CustomToolTemplates()

    def get_builtin_tools(self, category: str = None) -> Dict:
        """获取内置工具"""
        if category:
            return self.builtin_tools.get_tools_by_category(category)
        return self.builtin_tools.get_all_tools()

    def create_api_tool(
        self,
        tool_name: str,
        base_url: str,
        api_key: str,
        endpoints: List[Dict],
        auth_type: str = "api_key"
    ) -> Dict:
        """
        创建 API 工具配置
        
        Args:
            tool_name: 工具名称
            base_url: API 基础 URL
            api_key: API 密钥
            endpoints: 端点配置列表
            auth_type: 认证类型
        """
        tool_config = {
            "type": "tool",
            "name": tool_name,
            "provider": "custom_api",
            "config": {
                "base_url": base_url,
                "auth": {
                    "type": auth_type,
                    "key": api_key
                },
                "endpoints": {},
                "error_handling": {
                    "retry": {"enabled": True, "max_attempts": 3},
                    "timeout": 30
                }
            }
        }
        
        for endpoint in endpoints:
            endpoint_name = endpoint.get("name")
            tool_config["config"]["endpoints"][endpoint_name] = {
                "method": endpoint.get("method", "GET"),
                "path": endpoint.get("path"),
                "parameters": endpoint.get("parameters", {}),
                "body_template": endpoint.get("body", {}),
                "response_mapping": endpoint.get("response_mapping", {})
            }
        
        return tool_config

    def create_custom_tool(
        self,
        tool_name: str,
        description: str,
        language: str = "python",
        **kwargs
    ) -> str:
        """
        生成自定义工具代码
        
        Args:
            tool_name: 工具名称
            description: 工具描述
            language: 编程语言
            **kwargs: 其他参数
        """
        class_name = ''.join(word.capitalize() for word in tool_name.split('_'))
        
        if language == "python":
            template = self.custom_templates.PYTHON_TOOL_TEMPLATE
        elif language == "javascript":
            template = self.custom_templates.JAVASCRIPT_TOOL_TEMPLATE
        elif language == "api":
            template = self.custom_templates.API_TOOL_TEMPLATE
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        code = template.format(
            tool_name=tool_name,
            tool_description=description,
            ToolClassName=class_name,
            category=kwargs.get("category", "custom"),
            param_name=kwargs.get("param_name", "input"),
            param_description=kwargs.get("param_description", "输入参数"),
            required=kwargs.get("required", True)
        )
        
        return code

    def design_tool_chain(
        self,
        tasks: List[Dict],
        chain_type: str = "sequential"
    ) -> Dict:
        """
        设计工具链
        
        Args:
            tasks: 任务列表
            chain_type: 链类型 (sequential/parallel/conditional)
        """
        if chain_type == "sequential":
            return self._sequential_chain(tasks)
        elif chain_type == "parallel":
            return self._parallel_chain(tasks)
        elif chain_type == "conditional":
            return self._conditional_chain(tasks)
        else:
            raise ValueError(f"Unknown chain type: {chain_type}")

    def _sequential_chain(self, tasks: List[Dict]) -> Dict:
        """顺序链"""
        nodes = [{"id": "start", "type": "input"}]
        edges = []
        
        for i, task in enumerate(tasks):
            node_id = f"task_{i}"
            nodes.append({
                "id": node_id,
                "type": "tool",
                "config": task
            })
            edges.append({
                "from": "start" if i == 0 else f"task_{i-1}",
                "to": node_id
            })
        
        nodes.append({"id": "end", "type": "output"})
        edges.append({"from": f"task_{len(tasks)-1}", "to": "end"})
        
        return {
            "chain_type": "sequential",
            "nodes": nodes,
            "edges": edges
        }

    def _parallel_chain(self, tasks: List[Dict]) -> Dict:
        """并行链"""
        nodes = [
            {"id": "start", "type": "input"},
            {"id": "dispatch", "type": "parallel"},
            {"id": "merge", "type": "merge"},
            {"id": "end", "type": "output"}
        ]
        edges = [
            {"from": "start", "to": "dispatch"}
        ]
        
        for i, task in enumerate(tasks):
            nodes.append({
                "id": f"task_{i}",
                "type": "tool",
                "config": task
            })
            edges.append({"from": "dispatch", "to": f"task_{i}"})
            edges.append({"from": f"task_{i}", "to": "merge"})
        
        edges.append({"from": "merge", "to": "end"})
        
        return {
            "chain_type": "parallel",
            "nodes": nodes,
            "edges": edges
        }

    def _conditional_chain(self, tasks: List[Dict]) -> Dict:
        """条件链"""
        nodes = [
            {"id": "start", "type": "input"},
            {"id": "condition", "type": "condition"},
            {"id": "end", "type": "output"}
        ]
        edges = [
            {"from": "start", "to": "condition"}
        ]
        
        branches = {"true": [], "false": []}
        for i, task in enumerate(tasks):
            node_id = f"task_{i}"
            branch = task.get("condition", "true")
            
            nodes.append({
                "id": node_id,
                "type": "tool",
                "config": task
            })
            branches[branch].append(node_id)
            
            edges.append({
                "from": "condition",
                "to": node_id,
                "condition": branch
            })
        
        for branch_nodes in branches.values():
            for node_id in branch_nodes:
                edges.append({"from": node_id, "to": "end"})
        
        return {
            "chain_type": "conditional",
            "nodes": nodes,
            "edges": edges
        }

    def generate_tool_config(
        self,
        provider: str,
        api_key: str = None
    ) -> Dict:
        """
        生成第三方 API 工具配置
        
        Args:
            provider: API 提供商
            api_key: API 密钥
        """
        templates = {
            "openweathermap": {
                "name": "OpenWeatherMap",
                "base_url": "https://api.openweathermap.org/data/2.5",
                "auth_type": "api_key",
                "auth_key": "appid",
                "endpoints": [
                    {"name": "current", "method": "GET", "path": "/weather",
                     "params": ["q", "units", "lang"]},
                    {"name": "forecast", "method": "GET", "path": "/forecast",
                     "params": ["q", "units", "cnt"]}
                ]
            },
            "openai": {
                "name": "OpenAI API",
                "base_url": "https://api.openai.com/v1",
                "auth_type": "bearer",
                "auth_prefix": "Bearer",
                "auth_key": api_key,
                "endpoints": [
                    {"name": "chat", "method": "POST", "path": "/chat/completions",
                     "body": {"model": "gpt-4o", "messages": "{{messages}}",
                              "temperature": "{{temperature}}"}}
                ]
            },
            "stripe": {
                "name": "Stripe支付",
                "base_url": "https://api.stripe.com/v1",
                "auth_type": "bearer",
                "auth_prefix": "Bearer",
                "auth_key": api_key,
                "endpoints": [
                    {"name": "charge", "method": "POST", "path": "/charges",
                     "body": {"amount": "{{amount}}", "currency": "{{currency}}",
                              "source": "{{source}}"}}
                ]
            },
            "twilio": {
                "name": "Twilio短信",
                "base_url": "https://api.twilio.com/2010-04-01",
                "auth_type": "basic",
                "auth_key": api_key,
                "endpoints": [
                    {"name": "send_sms", "method": "POST",
                     "path": "/Accounts/{account_sid}/Messages.json",
                     "body": {"To": "{{to}}", "From": "{{from}}", "Body": "{{body}}"}}
                ]
            }
        }
        
        template = templates.get(provider)
        if not template:
            raise ValueError(f"Unknown provider: {provider}")
        
        return self.create_api_tool(
            tool_name=template["name"],
            base_url=template["base_url"],
            api_key=template.get("auth_key", api_key or ""),
            auth_type=template["auth_type"],
            endpoints=template["endpoints"]
        )


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 工具链配置专家系统 v5.0"
    )

    # 列出工具
    parser.add_argument("--list-tools", action="store_true", help="列出内置工具")
    parser.add_argument("--category", help="按分类筛选工具")

    # 创建 API 工具
    parser.add_argument("--create-api-tool", help="创建 API 工具")
    parser.add_argument("--base-url", help="API 基础 URL")
    parser.add_argument("--api-key", help="API 密钥")
    parser.add_argument("--endpoints", help="端点配置 (JSON)")

    # 创建自定义工具
    parser.add_argument("--create-custom-tool", help="创建自定义工具")
    parser.add_argument("--language", choices=["python", "javascript", "api"],
                       default="python", help="编程语言")
    parser.add_argument("--output", "-o", help="输出文件路径")

    # 设计工具链
    parser.add_argument("--design-chain", help="设计工具链")
    parser.add_argument("--chain-type", choices=["sequential", "parallel", "conditional"],
                       default="sequential", help="链类型")
    parser.add_argument("--tasks", help="任务列表 (JSON)")

    # 生成配置
    parser.add_argument("--generate-config", help="生成第三方 API 配置")
    parser.add_argument("--provider", help="API 提供商")

    args = parser.parse_args()

    expert = ToolChainExpert()

    if args.list_tools:
        tools = expert.get_builtin_tools(args.category)
        print(json.dumps(tools, indent=2, ensure_ascii=False))

    elif args.create_api_tool:
        endpoints = json.loads(args.endpoints or "[]")
        tool = expert.create_api_tool(
            tool_name=args.create_api_tool,
            base_url=args.base_url,
            api_key=args.api_key,
            endpoints=endpoints
        )
        print(json.dumps(tool, indent=2, ensure_ascii=False))

    elif args.create_custom_tool:
        code = expert.create_custom_tool(
            tool_name=args.create_custom_tool,
            description="Custom tool",
            language=args.language
        )
        
        if args.output:
            Path(args.output).write_text(code)
            print(f"工具代码已保存: {args.output}")
        else:
            print(code)

    elif args.design_chain:
        tasks = json.loads(args.tasks or "[]")
        chain = expert.design_tool_chain(
            tasks=tasks,
            chain_type=args.chain_type
        )
        print(json.dumps(chain, indent=2, ensure_ascii=False))

    elif args.generate_config:
        config = expert.generate_tool_config(
            provider=args.generate_config,
            api_key=args.api_key
        )
        print(json.dumps(config, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
