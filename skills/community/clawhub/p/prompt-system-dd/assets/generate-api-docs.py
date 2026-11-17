#!/usr/bin/env python3
"""
generate-api-docs.py — 从源码自动生成 API 文档
用法：
    python generate-api-docs.py <包名> <输出目录>
示例：
    python generate-api-docs.py docs/references

原理：
    以代码为唯一真相源，通过 import + inspect 反射提取
    类、函数、枚举、Pydantic 模型的签名和 docstring，
    生成 Markdown 格式 API 文档。
"""
import enum
import importlib
import inspect
import pkgutil
import sys
from pathlib import Path
from typing import Any


def _indent(text: str, spaces: int = 2) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.split("\n"))


def _format_default(value: Any) -> str:
    if value is inspect.Parameter.empty:
        return ""
    if isinstance(value, str):
        return f' = {value!r}'
    return f" = {value!r}"


def _format_signature(func: Any) -> str:
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return "(签名不可获取)"
    parts = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        annotation = ""
        if param.annotation != inspect.Parameter.empty:
            ann = param.annotation
            ann_str = str(ann)
            if hasattr(ann, "__origin__"):
                ann_str = str(ann).replace("typing.", "")
            annotation = f": {ann_str}"
        default = _format_default(param.default)
        parts.append(f"{name}{annotation}{default}")
    return_annotation = ""
    if sig.return_annotation != inspect.Signature.empty:
        ret = sig.return_annotation
        ret_str = str(ret).replace("typing.", "")
        return_annotation = f" -> {ret_str}"
    return f"({', '.join(parts)}){return_annotation}"


def _extract_class(obj: type) -> list[str]:
    lines = [f"### `{obj.__name__}`", ""]
    doc = inspect.getdoc(obj)
    if doc:
        lines.append(f"*{doc.strip()}*")
        lines.append("")

    # 构造方法
    try:
        sig = inspect.signature(obj.__init__)
        params = [p for p in sig.parameters.values() if p.name != "self"]
        param_parts = []
        for p in params:
            ann = f": {p.annotation}" if p.annotation != inspect.Parameter.empty else ""
            dft = _format_default(p.default)
            param_parts.append(f"{p.name}{ann}{dft}")
        return_type = ""
        if sig.return_annotation != inspect.Signature.empty:
            return_type = f" -> {sig.return_annotation}"
        lines.append(f"- 构造: `{obj.__name__}({', '.join(param_parts)}){return_type}`")
    except (ValueError, TypeError):
        lines.append(f"- 构造: `{obj.__name__}(...)`")

    # 公开方法
    methods = [
        m for m in dir(obj)
        if not m.startswith("_") and callable(getattr(obj, m, None))
    ]
    if methods:
        lines.append("- 方法:")
        for m in methods:
            method = getattr(obj, m)
            try:
                sig = inspect.signature(method)
                params = [p for p in sig.parameters.values() if p.name != "self"]
                param_parts = []
                for p in params:
                    ann = f": {p.annotation}" if p.annotation != inspect.Parameter.empty else ""
                    dft = _format_default(p.default)
                    param_parts.append(f"{p.name}{ann}{dft}")
                ret = ""
                if sig.return_annotation != inspect.Signature.empty:
                    ret = f" -> {sig.return_annotation}"
                lines.append(f"  - `{m}({', '.join(param_parts)}){ret}`")
            except (ValueError, TypeError):
                lines.append(f"  - `{m}(...)`")
    lines.append("")
    return lines


def _extract_enum(obj: type[enum.Enum]) -> list[str]:
    lines = [f"### `{obj.__name__}`", ""]
    doc = inspect.getdoc(obj)
    if doc:
        lines.append(f"*{doc.strip()}*")
        lines.append("")
    members = [(m.name, m.value) for m in obj]
    lines.append(f"成员：{'，'.join(f'`{name} = {value!r}`' for name, value in members)}")
    lines.append("")
    return lines


def _extract_function(obj) -> list[str]:
    lines = [f"### `{obj.__name__}`", ""]
    doc = inspect.getdoc(obj)
    if doc:
        lines.append(f"*{doc.strip()}*")
        lines.append("")
    lines.append(f"- 签名: `{obj.__name__}{_format_signature(obj)}`")
    lines.append("")
    return lines


def _generate_reference(package_name: str) -> str:
    pkg = importlib.import_module(package_name)
    lines = [
        f"# {package_name} API 参考文档（自动生成）",
        "",
        "> **本文档由 `generate-api-docs.py` 自动生成，以代码为唯一真相源**，"
        "人工修改会被下次生成覆盖。",
        "> 若需更新 API 描述，请修改代码 docstring 后重新生成。",
        "",
        "---",
        "",
    ]

    module_paths = []

    def scan_module(mod, prefix: str):
        if not hasattr(mod, "__all__"):
            return
        for name in mod.__all__:
            obj = getattr(mod, name, None)
            if obj is None:
                continue
            full_path = f"{prefix}.{name}" if prefix else name
            module_paths.append((full_path, obj))

    scan_module(pkg, "")

    # 扫描子包和子模块
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__, prefix=f"{package_name}."):
        try:
            submodule = importlib.import_module(name)
            scan_module(submodule, name)
        except ImportError:
            pass

    # 按模块分组
    from collections import OrderedDict
    grouped: dict[str, list[tuple[str, Any]]] = OrderedDict()
    for full_path, obj in module_paths:
        parts = full_path.split(".")
        module_key = ".".join(parts[:-1]) if len(parts) > 1 else "root"
        grouped.setdefault(module_key, []).append((parts[-1], obj))

    for module_name, items in grouped.items():
        lines.append(f"## `{module_name}`")
        lines.append("")
        for name, obj in sorted(items, key=lambda x: x[0]):
            if isinstance(obj, type) and issubclass(obj, enum.Enum):
                lines.extend(_extract_enum(obj))
            elif isinstance(obj, type):
                lines.extend(_extract_class(obj))
            elif callable(obj):
                lines.extend(_extract_function(obj))
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _generate_class_index(package_name: str) -> str:
    pkg = importlib.import_module(package_name)
    lines = [
        f"# {package_name} 类名速查表（自动生成）",
        "",
        "> **本文档由 `generate-api-docs.py` 自动生成**，以代码为唯一真相源。",
        "> 列出全部可导入类、枚举与函数及其真实所在模块。",
        "",
        "## 导出符号总表",
        "",
        "| 符号 | 类型 | 真实模块 | 职责/说明 |",
        "|------|------|----------|-----------|",
    ]

    seen = set()

    def collect(obj, prefix=""):
        if obj in seen or not inspect.ismodule(obj):
            return
        seen.add(obj)
        if hasattr(obj, "__all__"):
            for name in obj.__all__:
                member = getattr(obj, name, None)
                if member is None:
                    continue
                mod = inspect.getmodule(member)
                mod_path = f"{mod.__name__}" if mod else "unknown"
                doc = ""
                if hasattr(member, "__doc__") and member.__doc__:
                    doc = str(member.__doc__).strip().split("\n")[0][:60]
                elif inspect.isclass(member):
                    doc = member.__name__
                else:
                    doc = "-"
                if inspect.isclass(member) and issubclass(member, enum.Enum):
                    sym_type = "枚举"
                elif inspect.isclass(member):
                    sym_type = "类"
                elif inspect.isfunction(member) or inspect.ismethod(member):
                    sym_type = "函数"
                elif isinstance(member, (int, float, str, bool, type(None))):
                    sym_type = "常量"
                else:
                    sym_type = "-"
                lines.append(f"| `{name}` | {sym_type} | `{mod_path}` | {doc} |")
        if prefix and hasattr(obj, "__path__"):
            for finder, name, ispkg in pkgutil.iter_modules(obj.__path__, prefix=prefix + "."):
                try:
                    submod = importlib.import_module(name)
                    collect(submod, name)
                except ImportError:
                    pass

    collect(pkg, package_name)
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python generate-api-docs.py <输出目录>")
        sys.exit(1)
    output_dir = Path(sys.argv[1])
    output_dir.mkdir(parents=True, exist_ok=True)

    # 确保项目根目录在 sys.path 中
    cwd = Path.cwd()
    if str(cwd) not in sys.path:
        sys.path.insert(0, str(cwd))

    # 生成前先确保 scripts 包可导入
    importlib.invalidate_caches()

    ref_doc = _generate_reference("scripts")
    (output_dir / "api_reference.md").write_text(ref_doc, encoding="utf-8")

    index_doc = _generate_class_index("scripts")
    (output_dir / "api_class_reference.md").write_text(index_doc, encoding="utf-8")

    print(f"[OK] 已生成 api_reference.md ({len(ref_doc)} 字符)")
    print(f"[OK] 已生成 api_class_reference.md ({len(index_doc)} 字符)")


if __name__ == "__main__":
    main()
    
