#!/usr/bin/env python3
"""
API 文档提取器 - 从源代码提取 API 信息并生成文档
支持 Python (FastAPI/Flask/Django)、JavaScript/TypeScript、Go
"""

import ast
import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class APIParam:
    name: str
    type: str = "string"
    required: bool = True
    location: str = "query"  # query/path/body/header
    description: str = ""


@dataclass
class APIEndpoint:
    method: str = "GET"
    path: str = ""
    name: str = ""
    description: str = ""
    params: list = field(default_factory=list)
    returns: str = ""
    return_example: str = ""
    errors: list = field(default_factory=list)
    examples: dict = field(default_factory=dict)
    source_file: str = ""
    line_number: int = 0


class PythonExtractor(ast.NodeVisitor):
    """从 Python 代码提取 API 文档信息"""

    def __init__(self, source_file: str = ""):
        self.endpoints: list[APIEndpoint] = []
        self.source_file = source_file
        self._route_decorators = {
            "get", "post", "put", "delete", "patch", "head", "options"
        }

    def visit_FunctionDef(self, node):
        self._process_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._process_function(node)
        self.generic_visit(node)

    def _process_function(self, node):
        """处理函数定义，提取路由和文档"""
        # 检查是否有路由装饰器
        route_info = self._extract_route_from_decorators(node.decorator_list)
        if not route_info:
            # 检查是否是传统的 API 函数命名
            for prefix in ("get_", "post_", "put_", "delete_", "patch_", "create_", "update_", "remove_", "fetch_", "list_"):
                if node.name.startswith(prefix):
                    route_info = {
                        "method": prefix.rstrip("_").upper().replace("CREATE", "POST").replace("UPDATE", "PUT").replace("REMOVE", "DELETE").replace("FETCH", "GET").replace("LIST", "GET"),
                        "path": f"/{node.name.replace('_', '-')}"
                    }
                    break

        if not route_info:
            return

        docstring = ast.get_docstring(node) or ""
        endpoint = APIEndpoint(
            method=route_info["method"],
            path=route_info["path"],
            name=node.name,
            description=self._parse_docstring_desc(docstring),
            params=self._extract_params(node, docstring),
            returns=self._extract_returns(node, docstring),
            errors=self._extract_errors(docstring),
            source_file=self.source_file,
            line_number=node.lineno,
        )
        self.endpoints.append(endpoint)

    def _extract_route_from_decorators(self, decorators) -> Optional[dict]:
        """从装饰器提取路由信息"""
        for dec in decorators:
            method = None
            path = None

            # @app.get("/path") 或 @router.post("/path")
            if isinstance(dec, ast.Call):
                func = dec.func
                if isinstance(func, ast.Attribute) and func.attr in self._route_decorators:
                    method = func.attr.upper()
                    if dec.args and isinstance(dec.args[0], ast.Constant):
                        path = dec.args[0].value

            # @app.route("/path", methods=["POST"])
            if isinstance(dec, ast.Call):
                func = dec.func
                if isinstance(func, ast.Attribute) and func.attr == "route":
                    if dec.args and isinstance(dec.args[0], ast.Constant):
                        path = dec.args[0].value
                    method = "GET"
                    for kw in dec.keywords:
                        if kw.arg == "methods" and isinstance(kw.value, ast.List):
                            for elt in kw.value.elts:
                                if isinstance(elt, ast.Constant):
                                    method = elt.value.upper()
                                    break

            if method and path:
                return {"method": method, "path": path}
        return None

    def _parse_docstring_desc(self, docstring: str) -> str:
        """提取 docstring 的描述部分"""
        if not docstring:
            return ""
        lines = docstring.strip().split("\n")
        desc_lines = []
        for line in lines:
            stripped = line.strip()
            # 遇到 Args/Returns/Raises 等节停止
            if stripped and stripped.rstrip(":") in ("Args", "Parameters", "Returns", "Raises", "Exceptions", "Note", "Examples"):
                break
            if re.match(r"^(Args|Parameters|Returns|Raises|Exceptions|Note|Examples)\s*:?\s*$", stripped):
                break
            desc_lines.append(line)
        return "\n".join(desc_lines).strip()

    def _extract_params(self, node, docstring: str) -> list:
        """从函数签名和 docstring 提取参数"""
        params = []
        # 跳过 self/cls
        args = node.args
        arg_list = [a.arg for a in args.args if a.arg not in ("self", "cls")]

        # 从 type hints 获取类型
        type_map = {}
        for a in args.args:
            if a.arg in ("self", "cls"):
                continue
            if a.annotation:
                type_map[a.arg] = ast.unparse(a.annotation)

        # 从 docstring 提取描述
        desc_map = self._parse_docstring_params(docstring)

        for arg_name in arg_list:
            param = APIParam(
                name=arg_name,
                type=type_map.get(arg_name, "string"),
                description=desc_map.get(arg_name, ""),
            )
            # 判断是否为 path 参数
            if "{" + arg_name + "}" in getattr(self, '_current_path', ""):
                param.location = "path"
            params.append(param)

        # 处理默认值
        defaults_offset = len(args.args) - len(args.defaults)
        for i, default in enumerate(args.defaults):
            idx = defaults_offset + i
            if idx < len(params):
                params[idx].required = False

        return params

    def _parse_docstring_params(self, docstring: str) -> dict:
        """解析 docstring 中的参数描述，支持 Google/NumPy/Sphinx 格式"""
        if not docstring:
            return {}
        desc_map = {}
        lines = docstring.split("\n")
        in_args = False

        for line in lines:
            stripped = line.strip()

            # Google 风格: Args:
            if re.match(r"^(Args|Parameters)\s*:?\s*$", stripped):
                in_args = True
                continue
            if re.match(r"^(Returns|Raises|Exceptions|Note|Examples)\s*:?\s*$", stripped):
                in_args = False
                continue

            if in_args:
                # Google 风格: param_name (type): description  或  param_name: description
                m = re.match(r"^\s*(\w+)\s*(?:\(([^)]*)\))?\s*:\s*(.*)", line)
                if m:
                    desc_map[m.group(1)] = m.group(3).strip()

                # Sphinx 风格: :param name: description
                m = re.match(r"^\s*:param\s+(\w+)\s*:\s*(.*)", line)
                if m:
                    desc_map[m.group(1)] = m.group(2).strip()

        return desc_map

    def _extract_returns(self, node, docstring: str) -> str:
        """提取返回类型"""
        if node.returns:
            return ast.unparse(node.returns)

        if not docstring:
            return ""
        lines = docstring.split("\n")
        in_returns = False
        for line in lines:
            stripped = line.strip()
            if re.match(r"^Returns?\s*:?\s*$", stripped):
                in_returns = True
                continue
            if in_returns:
                if re.match(r"^(Args|Parameters|Raises|Exceptions|Note|Examples)\s*:?\s*$", stripped):
                    break
                if stripped:
                    return stripped
        return ""

    def _extract_errors(self, docstring: str) -> list:
        """提取可能抛出的异常"""
        if not docstring:
            return []
        errors = []
        lines = docstring.split("\n")
        in_raises = False
        for line in lines:
            stripped = line.strip()
            if re.match(r"^(Raises|Exceptions)\s*:?\s*$", stripped):
                in_raises = True
                continue
            if in_raises:
                if re.match(r"^(Args|Parameters|Returns|Note|Examples)\s*:?\s*$", stripped):
                    break
                m = re.match(r"^\s*(\w+)\s*:\s*(.*)", line)
                if m:
                    errors.append({"type": m.group(1), "description": m.group(2).strip()})
        return errors


def extract_from_python(filepath: str) -> list[APIEndpoint]:
    """从 Python 文件提取 API 端点"""
    with open(filepath) as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    extractor = PythonExtractor(source_file=filepath)
    extractor.visit(tree)

    # 尝试从路由装饰器推断 path 参数
    for ep in extractor.endpoints:
        for param in ep.params:
            if "{" + param.name + "}" in ep.path:
                param.location = "path"

    return extractor.endpoints


def extract_from_javascript(filepath: str) -> list[APIEndpoint]:
    """从 JavaScript/TypeScript 文件提取 API 端点"""
    with open(filepath) as f:
        source = f.read()

    endpoints = []

    # Express/Koa/Hono 路由: app.get('/path', ...) / router.post('/path', ...)
    route_pattern = re.compile(
        r"(?:app|router|route)\s*\.\s*(get|post|put|delete|patch|head|options)\s*\(\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE,
    )
    for match in route_pattern.finditer(source):
        method = match.group(1).upper()
        path = match.group(2)

        # 提取附近的 JSDoc 注释
        start = max(0, match.start() - 500)
        preceding = source[start:match.start()]
        docstring = extract_jsdoc(preceding)

        endpoint = APIEndpoint(
            method=method,
            path=path,
            name=docstring.get("summary", path),
            description=docstring.get("description", ""),
            params=docstring.get("params", []),
            returns=docstring.get("returns", ""),
            errors=docstring.get("errors", []),
            source_file=filepath,
        )
        endpoints.append(endpoint)

    # JSDoc @api 注释
    api_pattern = re.compile(
        r"/\*\*\s*(.*?)\*/\s*\n\s*(?:async\s+)?(?:function|const|let|var)\s+(\w+)",
        re.DOTALL,
    )
    for match in api_pattern.finditer(source):
        jsdoc = match.group(1)
        func_name = match.group(2)
        docstring = extract_jsdoc(jsdoc)
        if docstring.get("api") or docstring.get("route"):
            route = docstring.get("route", f"/{func_name.replace('_', '-')}")
            method = docstring.get("method", docstring.get("api", "GET").upper())
            endpoint = APIEndpoint(
                method=method,
                path=route,
                name=func_name,
                description=docstring.get("description", ""),
                params=docstring.get("params", []),
                returns=docstring.get("returns", ""),
                source_file=filepath,
            )
            endpoints.append(endpoint)

    return endpoints


def extract_jsdoc(jsdoc_text: str) -> dict:
    """解析 JSDoc 注释"""
    result = {}
    lines = jsdoc_text.replace("*", "").split("\n")

    desc_lines = []
    params = []
    for line in lines:
        line = line.strip().lstrip("/")
        if line.startswith("@summary"):
            result["summary"] = line.replace("@summary", "").strip()
        elif line.startswith("@description"):
            result["description"] = line.replace("@description", "").strip()
        elif line.startswith("@api") or line.startswith("@route"):
            parts = line.split()
            if len(parts) >= 2:
                if parts[0] == "@api":
                    result["api"] = parts[1].upper()
                elif parts[0] == "@route":
                    result["route"] = parts[1]
                    if len(parts) >= 3:
                        result["method"] = parts[2].strip("[]").upper()
        elif line.startswith("@param"):
            m = re.match(r"@param\s+\{(\w+)\}\s+(\w+)\s*-?\s*(.*)", line)
            if m:
                params.append(APIParam(name=m.group(2), type=m.group(1), description=m.group(3)))
        elif line.startswith("@returns") or line.startswith("@return"):
            m = re.match(r"@returns?\s+\{(\w+)\}\s*(.*)", line)
            if m:
                result["returns"] = f"{m.group(1)}: {m.group(2)}"
        elif line.startswith("@throws"):
            m = re.match(r"@throws\s+\{(\w+)\}\s*(.*)", line)
            if m:
                if "errors" not in result:
                    result["errors"] = []
                result["errors"].append({"type": m.group(1), "description": m.group(2)})
        elif line and not line.startswith("@"):
            desc_lines.append(line)

    if params:
        result["params"] = params
    if desc_lines and "description" not in result:
        result["description"] = " ".join(desc_lines).strip()

    return result


def extract_from_go(filepath: str) -> list[APIEndpoint]:
    """从 Go 文件提取 API 端点 (gin/echo/swag 注释)"""
    with open(filepath) as f:
        source = f.read()

    endpoints = []

    # 提取 swag/gin 注释块
    comment_block_pattern = re.compile(
        r"((?://.*\n)+)\s*func\s+\w+",
        re.MULTILINE,
    )
    for match in comment_block_pattern.finditer(source):
        block = match.group(1)
        if "@Summary" not in block and "@Router" not in block:
            continue

        endpoint = APIEndpoint(source_file=filepath)
        for line in block.split("\n"):
            line = line.strip().lstrip("/").strip()
            if line.startswith("@Summary"):
                endpoint.description = line.replace("@Summary", "").strip().strip('"')
            elif line.startswith("@Router"):
                m = re.match(r'@Router\s+([^\s]+)\s+\[(\w+)\]', line)
                if m:
                    endpoint.path = m.group(1)
                    endpoint.method = m.group(2).upper()
            elif line.startswith("@Param"):
                m = re.match(r'@Param\s+(\w+)\s+(\w+)\s+(\w+)\s+(?:true|false)\s+"([^"]*)"', line)
                if m:
                    endpoint.params.append(APIParam(
                        name=m.group(1),
                        location=m.group(2),
                        type=m.group(3),
                        required="true" in line,
                        description=m.group(4),
                    ))
            elif line.startswith("@Success"):
                m = re.match(r'@Success\s+\d+\s+\{object\}\s+(\S+)', line)
                if m:
                    endpoint.returns = m.group(1)
            elif line.startswith("@Failure"):
                m = re.match(r'@Failure\s+(\d+)\s+\{object\}\s+(\S+)\s+"([^"]*)"', line)
                if m:
                    endpoint.errors.append({"code": m.group(1), "type": m.group(2), "description": m.group(3)})

        if endpoint.path:
            endpoints.append(endpoint)

    return endpoints


def detect_language(filepath: str) -> str:
    """根据文件扩展名检测语言"""
    ext = Path(filepath).suffix.lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "javascript",
        ".tsx": "javascript",
        ".go": "go",
    }.get(ext, "unknown")


def extract_file(filepath: str, lang: str = None) -> list[APIEndpoint]:
    """提取单个文件的 API 端点"""
    if not lang or lang == "auto":
        lang = detect_language(filepath)

    if lang == "python":
        return extract_from_python(filepath)
    elif lang in ("javascript", "js"):
        return extract_from_javascript(filepath)
    elif lang == "go":
        return extract_from_go(filepath)
    return []


def extract_directory(dirpath: str, lang: str = None) -> list[APIEndpoint]:
    """递归提取目录中所有文件的 API 端点"""
    endpoints = []
    extensions = {
        "python": [".py"],
        "javascript": [".js", ".jsx", ".ts", ".tsx"],
        "go": [".go"],
    }
    if lang == "auto" or not lang:
        all_exts = sum(extensions.values(), [])
    else:
        all_exts = extensions.get(lang, [])

    skip_dirs = {"node_modules", ".git", "__pycache__", "venv", ".venv", "vendor", "dist", "build"}

    for root, dirs, files in os.walk(dirpath):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if any(f.endswith(ext) for ext in all_exts):
                filepath = os.path.join(root, f)
                endpoints.extend(extract_file(filepath, lang))

    return endpoints


def generate_markdown(endpoints: list[APIEndpoint], chinese: bool = True, title: str = "API 文档") -> str:
    """生成 Markdown 格式文档"""
    if chinese:
        lines = [
            f"# {title}",
            "",
            f"**文档版本**：v1.0 | **接口数量**：{len(endpoints)}",
            "",
            "---",
            "",
        ]
    else:
        lines = [
            f"# {title}",
            "",
            f"**Version**: v1.0 | **Endpoints**: {len(endpoints)}",
            "",
            "---",
            "",
        ]

    for i, ep in enumerate(endpoints, 1):
        if chinese:
            lines.append(f"### {i}. {ep.method} `{ep.path}`")
            lines.append("")
            if ep.description:
                lines.append(f"**接口说明**：{ep.description}")
                lines.append("")
            if ep.source_file:
                lines.append(f"**源文件**：`{ep.source_file}:{ep.line_number}`")
                lines.append("")

            if ep.params:
                lines.append("**请求参数**")
                lines.append("")
                lines.append("| 参数名 | 位置 | 类型 | 必填 | 说明 |")
                lines.append("|--------|------|------|------|------|")
                for p in ep.params:
                    req = "是" if p.required else "否"
                    lines.append(f"| {p.name} | {p.location} | {p.type} | {req} | {p.description} |")
                lines.append("")

            if ep.returns:
                lines.append(f"**返回类型**：`{ep.returns}`")
                lines.append("")

            if ep.errors:
                lines.append("**错误码**")
                lines.append("")
                lines.append("| 错误码 | 类型 | 说明 |")
                lines.append("|--------|------|------|")
                for e in ep.errors:
                    code = e.get("code", "")
                    etype = e.get("type", e.get("error", ""))
                    desc = e.get("description", "")
                    lines.append(f"| {code} | {etype} | {desc} |")
                lines.append("")
        else:
            lines.append(f"### {i}. {ep.method} `{ep.path}`")
            lines.append("")
            if ep.description:
                lines.append(f"**Description**: {ep.description}")
                lines.append("")
            if ep.params:
                lines.append("**Parameters**")
                lines.append("")
                lines.append("| Name | Location | Type | Required | Description |")
                lines.append("|------|----------|------|----------|-------------|")
                for p in ep.params:
                    req = "Yes" if p.required else "No"
                    lines.append(f"| {p.name} | {p.location} | {p.type} | {req} | {p.description} |")
                lines.append("")
            if ep.returns:
                lines.append(f"**Returns**: `{ep.returns}`")
                lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_openapi(endpoints: list[APIEndpoint], title: str = "API", version: str = "1.0.0") -> str:
    """生成 OpenAPI 3.0 规范 (YAML 格式)"""
    import yaml

    paths = {}
    for ep in endpoints:
        if ep.path not in paths:
            paths[ep.path] = {}

        operation = {
            "summary": ep.description or ep.name,
            "operationId": ep.name,
            "responses": {
                "200": {
                    "description": "Successful response",
                }
            },
        }

        if ep.params:
            parameters = []
            request_body_props = {}
            for p in ep.params:
                if p.location in ("path", "query", "header"):
                    parameters.append({
                        "name": p.name,
                        "in": p.location,
                        "required": p.required,
                        "schema": {"type": p.type},
                        "description": p.description,
                    })
                elif p.location == "body":
                    request_body_props[p.name] = {
                        "type": p.type,
                        "description": p.description,
                    }
            if parameters:
                operation["parameters"] = parameters
            if request_body_props:
                operation["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": request_body_props,
                            }
                        }
                    },
                }

        if ep.errors:
            for e in ep.errors:
                code = str(e.get("code", "400"))
                operation["responses"][code] = {
                    "description": e.get("description", ""),
                }

        paths[ep.path][ep.method.lower()] = operation

    spec = {
        "openapi": "3.0.3",
        "info": {"title": title, "version": version},
        "paths": paths,
    }

    return yaml.dump(spec, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="从源代码提取 API 文档")
    parser.add_argument("source", help="源文件或目录路径")
    parser.add_argument("--lang", default="auto", choices=["auto", "python", "js", "javascript", "go"],
                        help="代码语言（默认自动检测）")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json", "openapi"],
                        help="输出格式（默认 markdown）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--title", default="API 文档", help="文档标题")
    parser.add_argument("--chinese", action="store_true", default=True, help="使用中文模板（默认）")
    parser.add_argument("--english", action="store_true", help="使用英文模板")

    args = parser.parse_args()
    lang = "javascript" if args.lang == "js" else args.lang
    chinese = not args.english

    # 提取端点
    source = args.source
    if os.path.isfile(source):
        endpoints = extract_file(source, lang)
    elif os.path.isdir(source):
        endpoints = extract_directory(source, lang)
    else:
        print(f"错误：找不到 {source}", file=sys.stderr)
        sys.exit(1)

    if not endpoints:
        print("未找到 API 端点定义", file=sys.stderr)
        sys.exit(0)

    # 生成输出
    if args.format == "markdown":
        output = generate_markdown(endpoints, chinese=chinese, title=args.title)
    elif args.format == "openapi":
        try:
            output = generate_openapi(endpoints, title=args.title)
        except ImportError:
            print("错误：生成 OpenAPI 格式需要 PyYAML，请运行 pip install pyyaml", file=sys.stderr)
            sys.exit(1)
    else:
        output = json.dumps([asdict(ep) for ep in endpoints], ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"文档已生成：{args.output}（{len(endpoints)} 个端点）", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
