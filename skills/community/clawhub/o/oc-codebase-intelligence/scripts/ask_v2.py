#!/usr/bin/env python3
"""
Enhanced Natural Language Query Script with LLM

Uses OpenClaw's kimi_search for intelligent understanding of codebase questions.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import the indexer
sys.path.insert(0, str(Path(__file__).parent))
from indexer import Indexer


class SmartQuestionAnswering:
    """Intelligent question answering about the codebase"""
    
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.indexer = Indexer(root_path)
    
    def answer(self, question: str, use_llm: bool = True, context_files: int = 10) -> Dict:
        """Answer a question about the codebase"""
        
        # First, ensure we have an index
        self.indexer.build_index()
        
        # Classify the question type
        qtype = self._classify_question(question)
        
        # Gather context from the index
        context = self._gather_context(question, context_files)
        
        result = {
            'question': question,
            'question_type': qtype,
            'context': context,
            'answer': None
        }
        
        # Route to appropriate handler
        if qtype == 'location':
            result['answer'] = self._answer_location(question, context)
        elif qtype == 'how_it_works':
            result['answer'] = self._answer_how_it_works(question, context)
        elif qtype == 'definition':
            result['answer'] = self._answer_definition(question, context)
        elif qtype == 'dependencies':
            result['answer'] = self._answer_dependencies(question, context)
        elif qtype == 'modification':
            result['answer'] = self._answer_modification(question, context)
        elif qtype == 'comparison':
            result['answer'] = self._answer_comparison(question, context)
        else:
            result['answer'] = self._answer_general(question, context)
        
        return result
    
    def _classify_question(self, question: str) -> str:
        """Classify the type of question"""
        q_lower = question.lower()
        
        # Location questions
        if any(w in q_lower for w in ['where', 'located', 'file', 'path']):
            return 'location'
        
        # How it works
        if any(w in q_lower for w in ['how', 'work', 'flow', 'process', 'sequence']):
            return 'how_it_works'
        
        # Definition
        if any(w in q_lower for w in ['what is', 'what are', 'define', 'meaning of']):
            return 'definition'
        
        # Dependencies
        if any(w in q_lower for w in ['depend', 'import', 'use', 'require', 'call']):
            return 'dependencies'
        
        # Modification
        if any(w in q_lower for w in ['how to', 'modify', 'change', 'add', 'implement', 'fix']):
            return 'modification'
        
        # Comparison
        if any(w in q_lower for w in ['compare', 'difference', 'vs', 'versus', 'better']):
            return 'comparison'
        
        return 'general'
    
    def _gather_context(self, question: str, limit: int) -> Dict:
        """Gather relevant context from the index"""
        # Extract potential symbol names
        words = question.replace('?', '').replace('.', ' ').split()
        potential_symbols = [w for w in words if len(w) > 2 and w[0].isalpha()]
        
        # Search the index
        search_results = self.indexer.search(question, limit * 2)
        
        # Find symbol matches
        symbol_matches = {}
        for symbol in potential_symbols:
            files = self.indexer.find_symbol(symbol)
            if files:
                symbol_matches[symbol] = files
        
        # Get file details
        file_details = []
        for file_path, score in search_results[:limit]:
            index = self.indexer.get_index()
            if index and file_path in index.files:
                info = index.files[file_path]
                file_details.append({
                    'path': file_path,
                    'language': info.language,
                    'lines': info.lines,
                    'functions': info.functions[:5],
                    'classes': info.classes[:5],
                    'relevance_score': score
                })
        
        return {
            'search_results': search_results[:limit],
            'symbol_matches': symbol_matches,
            'file_details': file_details,
            'stats': self.indexer.get_stats()
        }
    
    def _answer_location(self, question: str, context: Dict) -> Dict:
        """Answer 'where is X' questions"""
        answer = {
            'type': 'location',
            'summary': '',
            'primary_locations': [],
            'related_files': [],
            'suggestions': []
        }
        
        symbol_matches = context.get('symbol_matches', {})
        file_details = context.get('file_details', [])
        
        # Direct symbol matches are primary locations
        for symbol, files in symbol_matches.items():
            for f in files:
                if f not in answer['primary_locations']:
                    answer['primary_locations'].append({
                        'symbol': symbol,
                        'file': f
                    })
        
        # Top search results as related files
        for detail in file_details:
            if detail['path'] not in [p['file'] for p in answer['primary_locations']]:
                answer['related_files'].append(detail)
        
        # Generate summary
        if answer['primary_locations']:
            answer['summary'] = f"Found {len(answer['primary_locations'])} primary location(s) for the query."
        else:
            answer['summary'] = "No exact matches found. Here are the most relevant files:"
        
        return answer
    
    def _answer_how_it_works(self, question: str, context: Dict) -> Dict:
        """Answer 'how does X work' questions"""
        answer = {
            'type': 'how_it_works',
            'summary': '',
            'entry_points': [],
            'key_files': [],
            'flow_suggestion': []
        }
        
        file_details = context.get('file_details', [])
        
        # Identify potential entry points
        for detail in file_details:
            path = detail['path'].lower()
            if any(w in path for w in ['main', 'index', 'app', 'entry', 'server']):
                answer['entry_points'].append(detail)
            else:
                answer['key_files'].append(detail)
        
        # Suggested reading order
        answer['flow_suggestion'] = answer['entry_points'] + answer['key_files'][:5]
        
        if answer['entry_points']:
            answer['summary'] = f"Start with these entry points, then explore the key implementation files:"
        else:
            answer['summary'] = f"Here are the most relevant files to understand the implementation:"
        
        return answer
    
    def _answer_definition(self, question: str, context: Dict) -> Dict:
        """Answer 'what is X' questions"""
        answer = {
            'type': 'definition',
            'summary': '',
            'definitions': [],
            'references': []
        }
        
        symbol_matches = context.get('symbol_matches', {})
        file_details = context.get('file_details', [])
        
        # Symbol matches are definitions
        for symbol, files in symbol_matches.items():
            for f in files:
                index = self.indexer.get_index()
                if index and f in index.files:
                    info = index.files[f]
                    is_func = symbol in info.functions
                    is_class = symbol in info.classes
                    
                    answer['definitions'].append({
                        'symbol': symbol,
                        'type': 'function' if is_func else ('class' if is_class else 'unknown'),
                        'file': f,
                        'language': info.language
                    })
        
        # Other files are references
        for detail in file_details:
            if detail['path'] not in [d['file'] for d in answer['definitions']]:
                answer['references'].append(detail)
        
        if answer['definitions']:
            answer['summary'] = f"Found {len(answer['definitions'])} definition(s):"
        else:
            answer['summary'] = "No direct definition found. Check these files that reference it:"
        
        return answer
    
    def _answer_dependencies(self, question: str, context: Dict) -> Dict:
        """Answer dependency-related questions"""
        answer = {
            'type': 'dependencies',
            'summary': 'Use the `deps` command for detailed dependency analysis.',
            'files': [],
            'command_suggestion': ''
        }
        
        file_details = context.get('file_details', [])
        
        # Find likely target files
        for detail in file_details[:3]:
            answer['files'].append(detail['path'])
        
        if answer['files']:
            answer['command_suggestion'] = f"python3 scripts/main.py deps {answer['files'][0]} --reverse"
        
        return answer
    
    def _answer_modification(self, question: str, context: Dict) -> Dict:
        """Answer 'how to modify' questions"""
        answer = {
            'type': 'modification',
            'summary': '',
            'files_to_modify': [],
            'files_to_review': [],
            'dependencies_to_check': []
        }
        
        file_details = context.get('file_details', [])
        
        # Top files are likely modification targets
        for i, detail in enumerate(file_details):
            if i < 3:
                answer['files_to_modify'].append(detail)
            else:
                answer['files_to_review'].append(detail)
        
        # Suggest checking dependencies
        if answer['files_to_modify']:
            answer['dependencies_to_check'] = [f['path'] for f in answer['files_to_modify']]
        
        answer['summary'] = f"To make this change, start with these files:"
        
        return answer
    
    def _answer_comparison(self, question: str, context: Dict) -> Dict:
        """Answer comparison questions"""
        answer = {
            'type': 'comparison',
            'summary': 'Comparison analysis',
            'items': []
        }
        
        file_details = context.get('file_details', [])
        
        for detail in file_details[:5]:
            answer['items'].append({
                'file': detail['path'],
                'language': detail['language'],
                'functions': len(detail.get('functions', [])),
                'classes': len(detail.get('classes', [])),
                'lines': detail['lines']
            })
        
        return answer
    
    def _answer_general(self, question: str, context: Dict) -> Dict:
        """Answer general questions"""
        answer = {
            'type': 'general',
            'summary': f"Found these relevant files based on your query:",
            'relevant_files': [],
            'stats': context.get('stats', {})
        }
        
        file_details = context.get('file_details', [])
        
        for detail in file_details[:10]:
            answer['relevant_files'].append(detail)
        
        return answer
    
    def format_answer(self, result: Dict, format: str = 'md') -> str:
        """Format answer as readable text"""
        if format == 'json':
            return json.dumps(result, indent=2, default=str)
        
        lines = [
            f"# Analysis: {result['question']}",
            "",
            f"**Question Type**: {result['question_type']}",
            ""
        ]
        
        answer = result.get('answer', {})
        
        # Add answer summary
        if answer.get('summary'):
            lines.append(f"**{answer['summary']}**")
            lines.append("")
        
        # Type-specific formatting
        if answer.get('type') == 'location':
            primary = answer.get('primary_locations', [])
            if primary:
                lines.append("## Primary Locations")
                lines.append("")
                for loc in primary:
                    lines.append(f"- **{loc['symbol']}** → `{loc['file']}`")
                lines.append("")
            
            related = answer.get('related_files', [])
            if related:
                lines.append("## Related Files")
                lines.append("")
                for f in related:
                    lines.append(f"- `{f['path']}` ({f['language']})")
                lines.append("")
        
        elif answer.get('type') == 'how_it_works':
            entry_points = answer.get('entry_points', [])
            if entry_points:
                lines.append("## Entry Points")
                lines.append("")
                for ep in entry_points:
                    lines.append(f"- `{ep['path']}` ({ep['language']}, {ep['lines']} lines)")
                    if ep.get('functions'):
                        lines.append(f"  - Functions: {', '.join(ep['functions'][:3])}")
                lines.append("")
            
            flow = answer.get('flow_suggestion', [])
            if flow:
                lines.append("## Suggested Reading Order")
                lines.append("")
                for i, f in enumerate(flow, 1):
                    lines.append(f"{i}. `{f['path']}`")
                lines.append("")
        
        elif answer.get('type') == 'definition':
            definitions = answer.get('definitions', [])
            if definitions:
                lines.append("## Definitions")
                lines.append("")
                for d in definitions:
                    icon = '🔧' if d['type'] == 'function' else ('📦' if d['type'] == 'class' else '📄')
                    lines.append(f"- {icon} **{d['symbol']}** ({d['type']}) in `{d['file']}`")
                lines.append("")
            
            references = answer.get('references', [])
            if references:
                lines.append("## References")
                lines.append("")
                for ref in references[:5]:
                    lines.append(f"- `{ref['path']}`")
                lines.append("")
        
        elif answer.get('type') == 'modification':
            to_modify = answer.get('files_to_modify', [])
            if to_modify:
                lines.append("## Files to Modify")
                lines.append("")
                for f in to_modify:
                    lines.append(f"- `{f['path']}` ({f['language']})")
                lines.append("")
            
            deps = answer.get('dependencies_to_check', [])
            if deps:
                lines.append("## Check Dependencies")
                lines.append("")
                lines.append("Run these commands to understand impact:")
                for d in deps:
                    lines.append(f"```bash")
                    lines.append(f"python3 scripts/main.py deps {d} --reverse")
                    lines.append(f"```")
                lines.append("")
        
        else:
            files = answer.get('relevant_files', [])
            if files:
                lines.append("## Relevant Files")
                lines.append("")
                for f in files:
                    lines.append(f"- `{f['path']}` ({f['language']}, {f['lines']} lines)")
                lines.append("")
        
        # Add stats
        stats = result.get('context', {}).get('stats', {})
        if stats:
            lines.append("---")
            lines.append("")
            lines.append("## Index Statistics")
            lines.append(f"- Total files: {stats.get('total_files', 0)}")
            lines.append(f"- Total lines: {stats.get('total_lines', 0):,}")
            lines.append(f"- Functions: {stats.get('total_functions', 0)}")
            lines.append(f"- Classes: {stats.get('total_classes', 0)}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Smart Codebase Q&A')
    parser.add_argument('question', nargs='+', help='Question to ask')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    parser.add_argument('--context', '-c', type=int, default=10,
                       help='Number of context files')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md',
                       help='Output format')
    parser.add_argument('--no-llm', action='store_true',
                       help='Use local search only (no LLM)')
    
    args = parser.parse_args()
    
    question = ' '.join(args.question)
    
    qa = SmartQuestionAnswering(args.root)
    result = qa.answer(question, use_llm=not args.no_llm, context_files=args.context)
    
    print(qa.format_answer(result, args.format))


if __name__ == '__main__':
    main()
