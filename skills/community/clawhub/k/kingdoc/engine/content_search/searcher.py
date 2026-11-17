"""KingDoc 文档内容全文搜索引擎（v3.8.0 新增）"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from engine.hardware import get_recommended_settings


class ContentSearchEngine:
    """全文搜索引擎：文档内容搜索 + 结果高亮定位。"""

    def __init__(self, backend=None):
        self.backend = backend
        hw = get_recommended_settings()
        self._workers = hw.get("workers", 1)

    def search(self, query: str, file_id: str = "", limit: int = 20) -> Dict:
        if self.backend:
            try:
                result = self.backend.kdoc_file_search(query, limit)
                return {
                    "success": True, "query": query,
                    "results": result if isinstance(result, list) else [],
                    "total": len(result) if isinstance(result, list) else 0,
                    "mode": "api", "hint": "金山开放平台内容搜索 API。",
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        return self._local_search(query, file_id, limit)

    def search_in_document(self, file_id: str, query: str) -> Dict:
        if self.backend:
            try:
                content = self.backend.kdoc_file_content(file_id)
                text = content if isinstance(content, str) else str(content)
                matches = self._find_in_text(text, query)
                return {"success": True, "file_id": file_id, "matches": matches, "total": len(matches), "mode": "api"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        try:
            from pathlib import Path
            p = Path("output") / f"{file_id}.md"
            if p.exists():
                text = p.read_text(encoding="utf-8")
                matches = self._find_in_text(text, query)
                return {"success": True, "file_id": file_id, "matches": matches, "total": len(matches), "mode": "local_fallback"}
            return {"success": False, "file_id": file_id, "hint": f"文件不存在：{p}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _local_search(self, query: str, file_id: str = "", limit: int = 20) -> Dict:
        try:
            from pathlib import Path
            results = []
            output_dir = Path("output")
            if not output_dir.exists():
                return {"success": True, "query": query, "results": [], "total": 0, "mode": "local_fallback", "hint": "无本地文件"}
            files = list(output_dir.glob("*.md")) if not file_id else [output_dir / f"{file_id}.md"]
            for f in files:
                if not f.exists():
                    continue
                text = f.read_text(encoding="utf-8")
                matches = self._find_in_text(text, query)
                if matches:
                    results.append({"file_id": f.stem, "file_name": f.name, "matches": matches})
                if len(results) >= limit:
                    break
            return {"success": True, "query": query, "results": results, "total": len(results), "mode": "local_fallback", "hint": "本地降级搜索。"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _find_in_text(self, text: str, query: str, context_lines: int = 1) -> List[Dict]:
        matches = []
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                highlighted = line.replace(query, f"**{query}**")
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                matches.append({"line": i + 1, "text": line, "highlighted": highlighted, "context": "\n".join(lines[start:end])})
        return matches
