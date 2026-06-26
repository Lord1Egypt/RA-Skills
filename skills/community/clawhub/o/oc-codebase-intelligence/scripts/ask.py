#!/usr/bin/env python3
"""
Natural Language Query Script

Answers questions about the codebase using indexed information.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CodebaseIndex:
    """Simple index of codebase information"""
    
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.files: Dict[str, Dict] = {}
        self.functions: Dict[str, List[str]] = {}
        self.classes: Dict[str, List[str]] = {}
        self._build_index()
    
    def _build_index(self):
        """Build index from source files"""
        for filepath in self.root.rglob('*'):
            if not filepath.is_file():
                continue
            
            # Skip ignored directories
            if any(part in {'.git', 'node_modules', '__pycache__', '.venv'}
                   for part in filepath.parts):
                continue
            
            ext = filepath.suffix.lower()
            if ext not in ['.py', '.js', '.ts', '.go', '.java', '.rb']:
                continue
            
            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                rel_path = str(filepath.relative_to(self.root))
                
                self.files[rel_path] = {
                    'path': rel_path,
                    'content': content,
                    'lines': len(content.split('\n'))
                }
                
                # Extract functions and classes based on language
                if ext == '.py':
                    self._index_python(content, rel_path)
                elif ext in ['.js', '.ts']:
                    self._index_js_ts(content, rel_path)
                elif ext == '.go':
                    self._index_go(content, rel_path)
                    
            except Exception:
                pass
    
    def _index_python(self, content: str, filepath: str):
        """Index Python file"""
        # Find function definitions
        for match in re.finditer(r'^def\s+(\w+)\s*\(', content, re.MULTILINE):
            func_name = match.group(1)
            if func_name not in self.functions:
                self.functions[func_name] = []
            self.functions[func_name].append(filepath)
        
        # Find class definitions
        for match in re.finditer(r'^class\s+(\w+)', content, re.MULTILINE):
            class_name = match.group(1)
            if class_name not in self.classes:
                self.classes[class_name] = []
            self.classes[class_name].append(filepath)
    
    def _index_js_ts(self, content: str, filepath: str):
        """Index JavaScript/TypeScript file"""
        # Find function definitions (various patterns)
        patterns = [
            r'function\s+(\w+)\s*\(',
            r'(\w+)\s*=\s*function\s*\(',
            r'(\w+)\s*:\s*function\s*\(',
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\(',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                if func_name and func_name not in ['if', 'for', 'while', 'switch']:
                    if func_name not in self.functions:
                        self.functions[func_name] = []
                    self.functions[func_name].append(filepath)
        
        # Find class definitions
        for match in re.finditer(r'class\s+(\w+)', content):
            class_name = match.group(1)
            if class_name not in self.classes:
                self.classes[class_name] = []
            self.classes[class_name].append(filepath)
    
    def _index_go(self, content: str, filepath: str):
        """Index Go file"""
        # Find function definitions
        for match in re.finditer(r'^func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(', content, re.MULTILINE):
            func_name = match.group(1)
            if func_name:
                if func_name not in self.functions:
                    self.functions[func_name] = []
                self.functions[func_name].append(filepath)
        
        # Find type definitions (structs/interfaces)
        for match in re.finditer(r'^type\s+(\w+)\s+(?:struct|interface)', content, re.MULTILINE):
            type_name = match.group(1)
            if type_name not in self.classes:
                self.classes[type_name] = []
            self.classes[type_name].append(filepath)
    
    def search(self, query: str, context_files: int = 10) -> List[Tuple[str, float]]:
        """Search for relevant files based on query"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        scores = []
        for filepath, info in self.files.items():
            score = 0.0
            content_lower = info['content'].lower()
            
            # Check if query terms appear in file
            for term in query_terms:
                if term in filepath.lower():
                    score += 10
                if term in content_lower:
                    score += 5
            
            # Boost for exact matches
            if query_lower in content_lower:
                score += 20
            
            if score > 0:
                scores.append((filepath, score))
        
        # Sort by score and return top results
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:context_files]
    
    def find_function(self, name: str) -> List[str]:
        """Find where a function is defined"""
        return self.functions.get(name, [])
    
    def find_class(self, name: str) -> List[str]:
        """Find where a class/type is defined"""
        return self.classes.get(name, [])


class QuestionAnswering:
    """Answers questions about the codebase"""
    
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.index = CodebaseIndex(root_path)
    
    def answer(self, question: str, context_files: int = 10) -> Dict:
        """Answer a question about the codebase"""
        question_lower = question.lower()
        
        # Determine question type
        if any(word in question_lower for word in ['where', 'file', 'location']):
            return self._answer_location(question, context_files)
        elif any(word in question_lower for word in ['how', 'work', 'flow']):
            return self._answer_flow(question, context_files)
        elif any(word in question_lower for word in ['what', 'define', 'meaning']):
            return self._answer_definition(question, context_files)
        elif any(word in question_lower for word in ['depend', 'import', 'use']):
            return self._answer_dependencies(question, context_files)
        elif any(word in question_lower for word in ['modify', 'change', 'add', 'implement']):
            return self._answer_modification(question, context_files)
        else:
            return self._answer_general(question, context_files)
    
    def _answer_location(self, question: str, context_files: int) -> Dict:
        """Answer 'where is X' questions"""
        # Extract entity name
        words = question.lower().replace('?', '').split()
        entity = None
        
        for i, word in enumerate(words):
            if word in ['is', 'are', 'the', 'function', 'class', 'module']:
                if i + 1 < len(words):
                    entity = words[i + 1].strip('?')
                    break
        
        if not entity:
            # Use last significant word
            for word in reversed(words):
                if word not in ['where', 'is', 'are', 'the', 'in', 'located']:
                    entity = word.strip('?')
                    break
        
        results = {
            'question_type': 'location',
            'entity': entity,
            'function_locations': self.index.find_function(entity) if entity else [],
            'class_locations': self.index.find_class(entity) if entity else [],
            'related_files': []
        }
        
        # Search for related files
        if entity:
            related = self.index.search(entity, context_files)
            results['related_files'] = [f[0] for f in related]
        
        return results
    
    def _answer_flow(self, question: str, context_files: int) -> Dict:
        """Answer 'how does X work' questions"""
        # Extract process/flow name
        words = question.lower().replace('?', '').split()
        process = None
        
        for word in reversed(words):
            if word not in ['how', 'does', 'work', 'the', 'function', 'method', 'class']:
                process = word.strip('?')
                break
        
        # Find relevant files
        related = self.index.search(process or question, context_files)
        
        return {
            'question_type': 'flow',
            'process': process,
            'relevant_files': [f[0] for f in related],
            'suggested_reading': related[:3] if related else []
        }
    
    def _answer_definition(self, question: str, context_files: int) -> Dict:
        """Answer 'what is X' questions"""
        # Extract term
        words = question.lower().replace('?', '').split()
        term = None
        
        for i, word in enumerate(words):
            if word in ['is', 'are'] and i + 1 < len(words):
                # Combine remaining words
                term = ' '.join(words[i + 1:]).strip('?')
                break
        
        if not term:
            term = words[-1].strip('?') if words else None
        
        results = {
            'question_type': 'definition',
            'term': term,
            'function_locations': self.index.find_function(term.split()[0]) if term else [],
            'class_locations': self.index.find_class(term.split()[0]) if term else [],
            'related_files': []
        }
        
        if term:
            related = self.index.search(term, context_files)
            results['related_files'] = [f[0] for f in related]
        
        return results
    
    def _answer_dependencies(self, question: str, context_files: int) -> Dict:
        """Answer dependency-related questions"""
        # This would integrate with deps.py in real implementation
        return {
            'question_type': 'dependencies',
            'message': 'Use @codebase-intelligence deps <file> for detailed dependency analysis',
            'relevant_files': []
        }
    
    def _answer_modification(self, question: str, context_files: int) -> Dict:
        """Answer 'how to modify' questions"""
        related = self.index.search(question, context_files)
        
        # Identify what needs to be modified
        words = question.lower().split()
        target = None
        for word in reversed(words):
            if word not in ['how', 'to', 'modify', 'change', 'add', 'implement', 'the', 'a']:
                target = word.strip('?')
                break
        
        return {
            'question_type': 'modification',
            'target': target,
            'relevant_files': [f[0] for f in related],
            'suggestion': f"Look at these files to understand how to modify {target}:" if target else "Examine these files:"
        }
    
    def _answer_general(self, question: str, context_files: int) -> Dict:
        """Answer general questions"""
        related = self.index.search(question, context_files)
        
        return {
            'question_type': 'general',
            'relevant_files': [f[0] for f in related],
            'indexed_functions': len(self.index.functions),
            'indexed_classes': len(self.index.classes),
            'total_files': len(self.index.files)
        }
    
    def format_answer(self, result: Dict, format: str = 'md') -> str:
        """Format answer as text"""
        if format == 'json':
            return json.dumps(result, indent=2)
        
        lines = [
            "# Question Analysis",
            "",
            f"**Question Type**: {result.get('question_type', 'unknown')}",
            "",
        ]
        
        qtype = result.get('question_type')
        
        if qtype == 'location':
            entity = result.get('entity')
            lines.append(f"**Looking for**: `{entity}`")
            lines.append("")
            
            func_locs = result.get('function_locations', [])
            if func_locs:
                lines.append("## Function Definitions")
                for loc in func_locs:
                    lines.append(f"- `{loc}`")
                lines.append("")
            
            class_locs = result.get('class_locations', [])
            if class_locs:
                lines.append("## Class/Type Definitions")
                for loc in class_locs:
                    lines.append(f"- `{loc}`")
                lines.append("")
            
            related = result.get('related_files', [])
            if related:
                lines.append("## Related Files")
                for f in related[:10]:
                    lines.append(f"- `{f}`")
                lines.append("")
        
        elif qtype == 'flow':
            process = result.get('process')
            if process:
                lines.append(f"**Process**: {process}")
                lines.append("")
            
            relevant = result.get('relevant_files', [])
            if relevant:
                lines.append("## Files to Examine")
                for f in relevant[:10]:
                    lines.append(f"- `{f}`")
                lines.append("")
                
                lines.append("## Suggested Reading Order")
                for i, (f, score) in enumerate(result.get('suggested_reading', []), 1):
                    lines.append(f"{i}. `{f}` (relevance: {score:.1f})")
                lines.append("")
        
        elif qtype == 'definition':
            term = result.get('term')
            if term:
                lines.append(f"**Term**: {term}")
                lines.append("")
            
            func_locs = result.get('function_locations', [])
            class_locs = result.get('class_locations', [])
            
            if func_locs:
                lines.append("## Defined as Function")
                for loc in func_locs:
                    lines.append(f"- `{loc}`")
                lines.append("")
            
            if class_locs:
                lines.append("## Defined as Class/Type")
                for loc in class_locs:
                    lines.append(f"- `{loc}`")
                lines.append("")
            
            related = result.get('related_files', [])
            if related:
                lines.append("## Files Containing References")
                for f in related[:10]:
                    lines.append(f"- `{f}`")
                lines.append("")
        
        elif qtype == 'modification':
            target = result.get('target')
            suggestion = result.get('suggestion', '')
            
            lines.append(f"**{suggestion}**")
            lines.append("")
            
            relevant = result.get('relevant_files', [])
            if relevant:
                for f in relevant[:10]:
                    lines.append(f"- `{f}`")
                lines.append("")
        
        else:  # general
            lines.append("## Search Results")
            lines.append("")
            
            relevant = result.get('relevant_files', [])
            if relevant:
                for f in relevant[:10]:
                    lines.append(f"- `{f}`")
            else:
                lines.append("No specific matches found. Try a more specific query.")
            
            lines.append("")
            lines.append("## Index Statistics")
            lines.append(f"- Total files indexed: {result.get('total_files', 0)}")
            lines.append(f"- Functions found: {result.get('indexed_functions', 0)}")
            lines.append(f"- Classes found: {result.get('indexed_classes', 0)}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Codebase Q&A')
    parser.add_argument('question', nargs='+', help='Question to ask')
    parser.add_argument('--root', '-r', default='.', help='Project root directory')
    parser.add_argument('--context', '-c', type=int, default=10,
                        help='Number of context files')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md',
                        help='Output format')
    
    args = parser.parse_args()
    
    question = ' '.join(args.question)
    print(f"Analyzing: {question}")
    print("Indexing codebase...")
    
    qa = QuestionAnswering(args.root)
    result = qa.answer(question, args.context)
    
    print(qa.format_answer(result, args.format))


if __name__ == '__main__':
    main()
