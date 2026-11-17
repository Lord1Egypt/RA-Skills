"""KingDoc 模板市场引擎

设计：
- 模板 git 仓库管理（clone/pull）
- 模板索引（名称/类别/变量/描述）
- 变量替换生成文档
- 异步操作 + 硬件自适应

v3.6.0 新增功能：降低文档创建门槛，行业模板库一键复用。
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional

from engine.hardware import get_recommended_settings

# 默认模板仓库（可配置）
DEFAULT_TEMPLATE_REPO = "https://github.com/fyniujin/kingdoc-templates.git"
LOCAL_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates"

# 模板变量正则
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")


class Template:
    """单个模板"""

    def __init__(self, name: str, category: str, description: str,
                 file_path: Path, variables: List[str]):
        self.name = name
        self.category = category
        self.description = description
        self.file_path = file_path
        self.variables = variables

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "variables": self.variables,
        }


class TemplateMarket:
    """模板市场引擎"""

    def __init__(self, repo_url: str = "", local_dir: str = ""):
        hw = get_recommended_settings()
        self._workers = hw["workers"]

        self.repo_url = repo_url or DEFAULT_TEMPLATE_REPO
        self.local_dir = Path(local_dir) if local_dir else LOCAL_TEMPLATE_DIR
        self._templates: Dict[str, Template] = {}
        self._last_refresh = 0
        self._refresh_interval = 3600  # 1 小时内不重复刷新

    def refresh(self, force: bool = False) -> Dict:
        """刷新模板仓库。

        force: 强制刷新，忽略缓存间隔
        """
        now = time.time()
        if not force and now - self._last_refresh < self._refresh_interval:
            return {"status": "skipped", "reason": "缓存未过期", "templates": len(self._templates)}

        # 确保本地目录存在
        self.local_dir.mkdir(parents=True, exist_ok=True)

        try:
            # 检查是否已 clone
            git_dir = self.local_dir / ".git"
            if git_dir.exists():
                # 已有仓库，pull 更新
                result = self._run_git(["pull"], cwd=self.local_dir)
            else:
                # 全新 clone
                result = self._run_git(["clone", self.repo_url, str(self.local_dir)])

            if result.returncode != 0:
                # git 失败，检查是否已有本地模板
                if not any(self.local_dir.iterdir()):
                    return {"status": "error", "error": result.stderr, "templates": 0}
                # 有本地模板，继续索引
                pass

            # 索引模板
            self._index_templates()
            self._last_refresh = now

            return {
                "status": "success",
                "templates": len(self._templates),
                "categories": len(set(t.category for t in self._templates.values())),
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "templates": len(self._templates)}

    def list_templates(self, category: str = "") -> List[Dict]:
        """列出所有可用模板。"""
        if not self._templates:
            self.refresh()

        templates = list(self._templates.values())
        if category:
            templates = [t for t in templates if t.category == category]

        return [t.to_dict() for t in templates]

    def search_templates(self, keyword: str) -> List[Dict]:
        """搜索模板。"""
        if not self._templates:
            self.refresh()

        keyword_lower = keyword.lower()
        results = []
        for t in self._templates.values():
            if (keyword_lower in t.name.lower() or
                keyword_lower in t.description.lower() or
                keyword_lower in t.category.lower()):
                results.append(t.to_dict())
        return results

    def get_template(self, name: str) -> Optional[Template]:
        """获取单个模板。"""
        return self._templates.get(name)

    def use_template(self, name: str, variables: Dict[str, str] = None) -> Dict:
        """使用模板（变量替换）。

        Args:
            name: 模板名称
            variables: 变量字典，如 {"title": "周报", "author": "张三"}

        Returns:
            {"content": "替换后的内容", "file_path": "保存路径", "variables_used": [...]}
        """
        if not self._templates:
            self.refresh()

        template = self._templates.get(name)
        if not template:
            return {"error": f"模板不存在: {name}"}

        try:
            content = template.file_path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"读取模板失败: {e}"}

        # 变量替换
        used_vars = []
        missing_vars = []

        def replace_var(match):
            var_name = match.group(1)
            if variables and var_name in variables:
                used_vars.append(var_name)
                return variables[var_name]
            missing_vars.append(var_name)
            return match.group(0)

        result = VAR_PATTERN.sub(replace_var, content)

        # 保存生成的文档
        output_dir = Path(__file__).resolve().parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{name}_{int(time.time())}.md"
        try:
            output_path.write_text(result, encoding="utf-8")
        except Exception as e:
            return {"error": f"保存失败: {e}", "content": result}

        return {
            "content": result,
            "file_path": str(output_path),
            "template": name,
            "variables_used": used_vars,
            "variables_missing": missing_vars,
        }

    def _index_templates(self):
        """索引本地模板文件。"""
        self._templates.clear()

        if not self.local_dir.exists():
            return

        for md_file in self.local_dir.rglob("*.md"):
            # 跳过 README 和隐藏文件
            if md_file.name.startswith(".") or md_file.name.upper() == "README.MD":
                continue

            try:
                content = md_file.read_text(encoding="utf-8")
            except:
                continue

            # 解析 frontmatter（简单的 key: value）
            name = md_file.stem
            category = "通用"
            description = ""

            # 尝试从 frontmatter 提取元数据
            if content.startswith("---"):
                try:
                    _, fm, _ = content.split("---", 2)
                    for line in fm.splitlines():
                        if line.startswith("name:"):
                            name = line.split(":", 1)[1].strip()
                        elif line.startswith("category:"):
                            category = line.split(":", 1)[1].strip()
                        elif line.startswith("description:"):
                            description = line.split(":", 1)[1].strip()
                except:
                    pass

            # 提取变量
            variables = list(set(VAR_PATTERN.findall(content)))

            template = Template(
                name=name,
                category=category,
                description=description,
                file_path=md_file,
                variables=variables,
            )
            self._templates[name] = template

    def _run_git(self, args: List[str], cwd: Path = None) -> subprocess.CompletedProcess:
        """运行 git 命令。"""
        cmd = ["git"] + args
        try:
            return subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(cmd, returncode=1, stdout="", stderr="git 操作超时")
        except FileNotFoundError:
            return subprocess.CompletedProcess(cmd, returncode=1, stdout="", stderr="git 未安装")
        except Exception as e:
            return subprocess.CompletedProcess(cmd, returncode=1, stdout="", stderr=str(e))


# 全局单例
_market: Optional[TemplateMarket] = None


def get_market() -> TemplateMarket:
    """获取模板市场单例"""
    global _market
    if _market is None:
        _market = TemplateMarket()
    return _market


# 便捷函数
def refresh_templates(force: bool = False) -> Dict:
    return get_market().refresh(force)


def list_templates(category: str = "") -> List[Dict]:
    return get_market().list_templates(category)


def search_templates(keyword: str) -> List[Dict]:
    return get_market().search_templates(keyword)


def use_template(name: str, variables: Dict[str, str] = None) -> Dict:
    return get_market().use_template(name, variables)
