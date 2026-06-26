#!/usr/bin/env python3
"""
Codebase Intelligence - Main Analysis Script

Analyzes project structure, identifies modules, and generates comprehensive reports.
"""

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import fnmatch


@dataclass
class FileInfo:
    """Information about a source file"""
    path: Path
    language: str
    lines: int
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ModuleInfo:
    """Information about a module/directory"""
    name: str
    path: Path
    files: List[FileInfo] = field(default_factory=list)
    submodules: List['ModuleInfo'] = field(default_factory=list)
    total_lines: int = 0
    languages: Set[str] = field(default_factory=set)


class LanguageDetector:
    """Detects programming language from file extension"""
    
    EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript (React)',
        '.tsx': 'TypeScript (React)',
        '.go': 'Go',
        '.rs': 'Rust',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.cs': 'C#',
        '.swift': 'Swift',
        '.m': 'Objective-C',
        '.r': 'R',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.zsh': 'Zsh',
        '.ps1': 'PowerShell',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        '.vue': 'Vue',
        '.svelte': 'Svelte',
        '.json': 'JSON',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.toml': 'TOML',
        '.xml': 'XML',
        '.md': 'Markdown',
        '.rst': 'reStructuredText',
    }
    
    @classmethod
    def detect(cls, filepath: Path) -> Optional[str]:
        """Detect language from file path"""
        ext = filepath.suffix.lower()
        return cls.EXTENSIONS.get(ext)
    
    @classmethod
    def is_source_file(cls, filepath: Path) -> bool:
        """Check if file is a source code file"""
        return cls.detect(filepath) is not None


class CodebaseAnalyzer:
    """Main codebase analyzer"""
    
    DEFAULT_IGNORE = [
        '.git', '.svn', '.hg',
        'node_modules', 'vendor', '__pycache__',
        '.venv', 'venv', 'env',
        'dist', 'build', 'target',
        '*.min.js', '*.min.css',
        '.DS_Store', 'Thumbs.db',
    ]
    
    def __init__(self, root_path: str, ignore_patterns: Optional[List[str]] = None):
        self.root = Path(root_path).resolve()
        self.ignore_patterns = ignore_patterns or self.DEFAULT_IGNORE
        self.files: List[FileInfo] = []
        self.modules: Dict[str, ModuleInfo] = {}
        self.stats = {
            'total_files': 0,
            'total_lines': 0,
            'languages': {},
        }
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        rel_path = path.relative_to(self.root)
        
        for pattern in self.ignore_patterns:
            # Check if any part of the path matches
            for part in rel_path.parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
            # Check full path match
            if fnmatch.fnmatch(str(rel_path), pattern):
                return True
        
        return False
    
    def analyze_file(self, filepath: Path) -> Optional[FileInfo]:
        """Analyze a single file"""
        language = LanguageDetector.detect(filepath)
        if not language:
            return None
        
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            lines = len(content.split('\n'))
            
            # Detect imports based on language
            imports = self._extract_imports(content, language)
            
            return FileInfo(
                path=filepath,
                language=language,
                lines=lines,
                imports=imports
            )
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return None
    
    def _extract_imports(self, content: str, language: str) -> List[str]:
        """Extract import statements from file content"""
        imports = []
        
        if language == 'Python':
            # Simple regex-free import detection
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    # Extract module name
                    if line.startswith('import '):
                        mod = line[7:].split()[0].split('.')[0]
                    else:  # from X import Y
                        parts = line[5:].split(' import')
                        if parts:
                            mod = parts[0].strip().split('.')[0]
                        else:
                            continue
                    
                    # Filter out stdlib
                    if mod and not self._is_stdlib(mod, 'Python'):
                        imports.append(mod)
        
        elif language in ['JavaScript', 'TypeScript']:
            for line in content.split('\n'):
                line = line.strip()
                if 'require(' in line or 'import ' in line:
                    # Extract package name
                    if 'from ' in line:
                        parts = line.split('from ')
                        if len(parts) > 1:
                            pkg = parts[1].strip().strip('"\';')
                            if pkg and not pkg.startswith('.'):
                                imports.append(pkg.split('/')[0])
                    elif 'require(' in line:
                        start = line.find('require(') + 8
                        end = line.find(')', start)
                        if end > start:
                            pkg = line[start:end].strip('"\'')
                            if pkg and not pkg.startswith('.'):
                                imports.append(pkg.split('/')[0])
        
        return list(set(imports))
    
    def _is_stdlib(self, module: str, language: str) -> bool:
        """Check if module is standard library"""
        if language == 'Python':
            stdlib_modules = {
                'os', 'sys', 'json', 're', 'collections', 'itertools',
                'functools', 'datetime', 'pathlib', 'typing', 'argparse',
                'subprocess', 'tempfile', 'shutil', 'glob', 'fnmatch',
                'hashlib', 'base64', 'urllib', 'http', 'socket', 'asyncio',
                'unittest', 'pytest', 'logging', 'warnings', 'traceback',
                'inspect', 'types', 'abc', 'copy', 'pickle', 'csv',
                'xml', 'html', 'email', 'uuid', 'random', 'string',
                'math', 'statistics', 'decimal', 'fractions', 'numbers',
                'datetime', 'time', 'calendar', 'zoneinfo',
            }
            return module in stdlib_modules
        return False
    
    def analyze(self, max_files: int = 1000) -> 'CodebaseAnalyzer':
        """Analyze the entire codebase"""
        print(f"Analyzing codebase at: {self.root}")
        
        file_count = 0
        for filepath in self.root.rglob('*'):
            if not filepath.is_file():
                continue
            
            if self.should_ignore(filepath):
                continue
            
            file_info = self.analyze_file(filepath)
            if file_info:
                self.files.append(file_info)
                self.stats['total_files'] += 1
                self.stats['total_lines'] += file_info.lines
                
                lang = file_info.language
                if lang not in self.stats['languages']:
                    self.stats['languages'][lang] = {'files': 0, 'lines': 0}
                self.stats['languages'][lang]['files'] += 1
                self.stats['languages'][lang]['lines'] += file_info.lines
                
                file_count += 1
                if file_count >= max_files:
                    print(f"Reached max files limit ({max_files})")
                    break
        
        self._build_module_tree()
        
        print(f"Analyzed {len(self.files)} files")
        return self
    
    def _build_module_tree(self):
        """Build module tree from files"""
        for file_info in self.files:
            rel_path = file_info.path.relative_to(self.root)
            
            # Build module hierarchy
            current_path = self.root
            for part in rel_path.parts[:-1]:  # Exclude filename
                current_path = current_path / part
                module_name = str(current_path.relative_to(self.root))
                
                if module_name not in self.modules:
                    self.modules[module_name] = ModuleInfo(
                        name=part,
                        path=current_path
                    )
                
                self.modules[module_name].files.append(file_info)
                self.modules[module_name].total_lines += file_info.lines
                self.modules[module_name].languages.add(file_info.language)
    
    def generate_report(self, format: str = 'md') -> str:
        """Generate analysis report"""
        if format == 'json':
            return self._generate_json_report()
        else:
            return self._generate_markdown_report()
    
    def _generate_markdown_report(self) -> str:
        """Generate Markdown report"""
        lines = [
            "# Codebase Analysis Report",
            "",
            f"**Root Directory**: `{self.root}`",
            f"**Generated**: {__import__('datetime').datetime.now().isoformat()}",
            "",
            "## Overview",
            "",
            f"- **Total Files**: {self.stats['total_files']}",
            f"- **Total Lines**: {self.stats['total_lines']:,}",
            f"- **Languages**: {len(self.stats['languages'])}",
            f"- **Modules**: {len(self.modules)}",
            "",
            "## Languages",
            "",
            "| Language | Files | Lines | Percentage |",
            "|----------|-------|-------|------------|",
        ]
        
        # Sort languages by lines
        sorted_langs = sorted(
            self.stats['languages'].items(),
            key=lambda x: x[1]['lines'],
            reverse=True
        )
        
        total_lines = self.stats['total_lines'] or 1
        for lang, data in sorted_langs:
            pct = (data['lines'] / total_lines) * 100
            lines.append(f"| {lang} | {data['files']} | {data['lines']:,} | {pct:.1f}% |")
        
        lines.extend([
            "",
            "## Module Structure",
            "",
            "```",
        ])
        
        # Build tree representation
        tree_lines = self._build_tree(self.root, "")
        lines.extend(tree_lines)
        
        lines.extend([
            "```",
            "",
            "## Entry Points",
            "",
        ])
        
        # Try to find entry points
        entry_points = self._find_entry_points()
        if entry_points:
            for ep in entry_points:
                rel = Path(ep).relative_to(self.root)
                lines.append(f"- `{rel}`")
        else:
            lines.append("No obvious entry points found.")
        
        lines.extend([
            "",
            "## External Dependencies",
            "",
        ])
        
        # Collect all external dependencies
        all_deps: Dict[str, int] = {}
        for file_info in self.files:
            for dep in file_info.imports:
                all_deps[dep] = all_deps.get(dep, 0) + 1
        
        if all_deps:
            sorted_deps = sorted(all_deps.items(), key=lambda x: x[1], reverse=True)
            lines.append("| Dependency | Import Count |")
            lines.append("|------------|--------------|")
            for dep, count in sorted_deps[:20]:  # Top 20
                lines.append(f"| {dep} | {count} |")
        else:
            lines.append("No external dependencies detected.")
        
        return "\n".join(lines)
    
    def _build_tree(self, path: Path, prefix: str) -> List[str]:
        """Build ASCII tree representation"""
        lines = []
        
        # Get immediate children
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
        except:
            return lines
        
        # Filter items
        items = [item for item in items if not self.should_ignore(item)]
        
        # Limit display
        if len(items) > 20:
            items = items[:20]
            show_more = True
        else:
            show_more = False
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1 and not show_more
            connector = "└── " if is_last else "├── "
            
            rel = item.relative_to(self.root)
            
            if item.is_dir():
                lines.append(f"{prefix}{connector}{item.name}/")
                extension = "    " if is_last else "│   "
                lines.extend(self._build_tree(item, prefix + extension))
            else:
                # Show file with language icon
                lang = LanguageDetector.detect(item)
                icon = self._get_file_icon(lang)
                lines.append(f"{prefix}{connector}{icon} {item.name}")
        
        if show_more:
            lines.append(f"{prefix}└── ... ({len(items) - 20} more items)")
        
        return lines
    
    def _get_file_icon(self, language: Optional[str]) -> str:
        """Get icon for file type"""
        icons = {
            'Python': '🐍',
            'JavaScript': '📜',
            'TypeScript': '📘',
            'Go': '🐹',
            'Rust': '🦀',
            'Java': '☕',
            'C': '🔧',
            'C++': '⚙️',
        }
        return icons.get(language or '', '📄')
    
    def _find_entry_points(self) -> List[str]:
        """Try to find entry points"""
        entry_points = []
        
        # Common entry point patterns
        patterns = [
            'main.py', 'main.js', 'index.js', 'index.ts',
            'app.py', 'app.js', 'server.js', 'server.ts',
            '__main__.py', 'manage.py', 'setup.py',
            'Cargo.toml', 'package.json', 'go.mod',
        ]
        
        for pattern in patterns:
            for file_info in self.files:
                if file_info.path.name == pattern:
                    entry_points.append(str(file_info.path))
        
        return entry_points[:10]  # Limit results
    
    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        data = {
            'root': str(self.root),
            'stats': self.stats,
            'modules': {
                name: {
                    'path': str(m.path),
                    'files': len(m.files),
                    'lines': m.total_lines,
                    'languages': list(m.languages)
                }
                for name, m in self.modules.items()
            },
            'files': [
                {
                    'path': str(f.path.relative_to(self.root)),
                    'language': f.language,
                    'lines': f.lines,
                    'imports': f.imports
                }
                for f in self.files[:100]  # Limit for JSON
            ]
        }
        return json.dumps(data, indent=2)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Codebase Intelligence Analyzer')
    parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md',
                        help='Output format')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--max-files', type=int, default=1000,
                        help='Maximum files to analyze')
    
    args = parser.parse_args()
    
    analyzer = CodebaseAnalyzer(args.path)
    analyzer.analyze(max_files=args.max_files)
    report = analyzer.generate_report(format=args.format)
    
    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
