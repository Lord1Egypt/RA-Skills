#!/usr/bin/env python3
"""
Agent Memory Optimizer - Analyzer v1.0.0
Scans agent memory files, detects duplicates, stale info, and structural issues.
Author: Peru 🇵🇪
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

VERSION = "1.0.0"
STALE_DAYS = 30  # entries older than this are flagged

class MemoryAnalyzer:
    def __init__(self, workspace_path, verbose=False):
        self.workspace = Path(workspace_path)
        self.verbose = verbose
        self.files = {}          # path -> content
        self.entries = []        # all extracted entries
        self.headings = []       # heading structure
        self.issues = {
            'critical': [],
            'warning': [],
            'suggestion': []
        }
        self.stats = {
            'files_scanned': 0,
            'total_entries': 0,
            'total_bytes': 0,
            'duplicates': 0,
            'stale_entries': 0,
            'missing_indexes': 0,
            'structure_issues': 0,
        }

    def discover_files(self):
        """Find all memory-related markdown files."""
        patterns = [
            self.workspace / 'MEMORY.md',
            self.workspace / 'memory' / '*.md',
            self.workspace / 'TOOLS.md',
            self.workspace / 'AGENTS.md',
        ]
        
        found = []
        
        # Direct files
        for p in [self.workspace / 'MEMORY.md', self.workspace / 'TOOLS.md', self.workspace / 'AGENTS.md']:
            if p.exists():
                found.append(p)
        
        # Memory directory
        memory_dir = self.workspace / 'memory'
        if memory_dir.exists():
            found.extend(sorted(memory_dir.glob('*.md')))
        
        return found

    def load_files(self):
        """Load and parse all found files."""
        files = self.discover_files()
        for f in files:
            try:
                content = f.read_text(encoding='utf-8', errors='replace')
                self.files[str(f)] = content
                self.stats['files_scanned'] += 1
                self.stats['total_bytes'] += len(content.encode('utf-8'))
            except Exception as e:
                self.issues['warning'].append(f"Could not read {f}: {e}")
        
        if self.verbose:
            print(f"  Loaded {len(self.files)} files ({self.stats['total_bytes'] / 1024:.1f} KB)")

    def extract_entries(self):
        """Extract individual entries from all files."""
        for filepath, content in self.files.items():
            lines = content.split('\n')
            current_heading = ""
            current_entry = []
            entry_line = 0
            
            for i, line in enumerate(lines):
                # Track headings
                heading_match = re.match(r'^(#{1,6})\s+(.+)', line)
                if heading_match:
                    level = len(heading_match.group(1))
                    title = heading_match.group(2).strip()
                    self.headings.append({
                        'file': filepath,
                        'line': i + 1,
                        'level': level,
                        'title': title
                    })
                    current_heading = title
                
                # Extract list items as entries
                list_match = re.match(r'^[\s]*[-*+]\s+(.+)', line)
                if list_match:
                    entry_text = list_match.group(1).strip()
                    if len(entry_text) > 10:  # Skip trivial entries
                        self.entries.append({
                            'text': entry_text,
                            'file': filepath,
                            'line': i + 1,
                            'heading': current_heading,
                            'type': 'list_item'
                        })
                
                # Extract paragraph blocks (non-heading, non-list, non-empty)
                elif line.strip() and not heading_match and not line.strip().startswith(('```', '|', '---', '===')):
                    if len(line.strip()) > 20:
                        self.entries.append({
                            'text': line.strip(),
                            'file': filepath,
                            'line': i + 1,
                            'heading': current_heading,
                            'type': 'paragraph'
                        })
            
        self.stats['total_entries'] = len(self.entries)
        if self.verbose:
            print(f"  Extracted {len(self.entries)} entries")

    def detect_duplicates(self, threshold=0.80):
        """Find duplicate entries using fuzzy matching."""
        duplicates = []
        seen_pairs = set()
        
        # Group entries by first few words for efficiency
        buckets = defaultdict(list)
        for i, entry in enumerate(self.entries):
            # Use first 3 significant words as bucket key
            words = re.findall(r'\b\w{3,}\b', entry['text'].lower())
            if words:
                key = ' '.join(words[:3])
                buckets[key].append(i)
        
        # Compare within similar buckets
        for key, indices in buckets.items():
            if len(indices) < 2:
                continue
            for a in range(len(indices)):
                for b in range(a + 1, len(indices)):
                    i, j = indices[a], indices[b]
                    pair_key = (min(i, j), max(i, j))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)
                    
                    e1, e2 = self.entries[i], self.entries[j]
                    # Skip if from same file and same line
                    if e1['file'] == e2['file'] and abs(e1['line'] - e2['line']) <= 1:
                        continue
                    
                    ratio = SequenceMatcher(None, e1['text'].lower(), e2['text'].lower()).ratio()
                    if ratio >= threshold:
                        duplicates.append({
                            'entry1': e1,
                            'entry2': e2,
                            'similarity': round(ratio * 100, 1)
                        })
        
        # Also do a broader sweep for very similar entries across all
        all_texts = [(i, e['text'].lower()) for i, e in enumerate(self.entries)]
        for i in range(len(all_texts)):
            for j in range(i + 1, min(i + 50, len(all_texts))):  # Limit comparisons
                pair_key = (i, j)
                if pair_key in seen_pairs:
                    continue
                
                t1, t2 = all_texts[i][1], all_texts[j][1]
                if abs(len(t1) - len(t2)) > max(len(t1), len(t2)) * 0.5:
                    continue  # Skip if lengths too different
                
                ratio = SequenceMatcher(None, t1, t2).ratio()
                if ratio >= threshold:
                    e1 = self.entries[all_texts[i][0]]
                    e2 = self.entries[all_texts[j][0]]
                    if e1['file'] == e2['file'] and abs(e1['line'] - e2['line']) <= 1:
                        continue
                    duplicates.append({
                        'entry1': e1,
                        'entry2': e2,
                        'similarity': round(ratio * 100, 1)
                    })
                    seen_pairs.add(pair_key)
        
        self.stats['duplicates'] = len(duplicates)
        
        if duplicates:
            self.issues['critical'].append({
                'type': 'duplicates',
                'message': f'{len(duplicates)} duplicate entries found',
                'details': duplicates[:20]  # Top 20
            })
        
        return duplicates

    def detect_stale(self):
        """Find entries with outdated dates or metrics."""
        stale = []
        now = datetime.now()
        cutoff = now - timedelta(days=STALE_DAYS)
        
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',           # 2025-01-15
            r'(\d{1,2}/\d{1,2}/\d{4})',       # 1/15/2025
            r'(\w+ \d{1,2},?\s*\d{4})',        # January 15, 2025
        ]
        
        for entry in self.entries:
            for pattern in date_patterns:
                matches = re.findall(pattern, entry['text'])
                for match in matches:
                    try:
                        # Try parsing different formats
                        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%B %d, %Y', '%B %d %Y']:
                            try:
                                d = datetime.strptime(match.strip().rstrip(','), fmt)
                                if d < cutoff:
                                    stale.append({
                                        'entry': entry,
                                        'date_found': match,
                                        'age_days': (now - d).days
                                    })
                                break
                            except ValueError:
                                continue
                    except:
                        pass
        
        # Also check for "current", "now", "today" in daily files
        for filepath, content in self.files.items():
            if '/memory/' in filepath:
                filename = os.path.basename(filepath)
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
                if date_match:
                    try:
                        file_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                        if file_date < cutoff:
                            # Check if this file has "current" or "active" references
                            if re.search(r'\b(current|active|ongoing|in progress|TODO)\b', content, re.I):
                                stale.append({
                                    'entry': {
                                        'text': f'File {filename} contains "current/active" references but is {(now - file_date).days} days old',
                                        'file': filepath,
                                        'line': 0,
                                        'heading': '',
                                        'type': 'file'
                                    },
                                    'date_found': date_match.group(1),
                                    'age_days': (now - file_date).days
                                })
                    except:
                        pass
        
        self.stats['stale_entries'] = len(stale)
        
        if stale:
            severity = 'critical' if len(stale) > 10 else 'warning'
            self.issues[severity].append({
                'type': 'stale',
                'message': f'{len(stale)} stale entries with outdated dates',
                'details': stale[:15]
            })
        
        return stale

    def check_structure(self):
        """Check heading hierarchy and structure."""
        issues = []
        
        for filepath, content in self.files.items():
            filename = os.path.basename(filepath)
            lines = content.split('\n')
            
            # Check heading hierarchy
            prev_level = 0
            for h in [h for h in self.headings if h['file'] == filepath]:
                if h['level'] > prev_level + 1 and prev_level > 0:
                    issues.append({
                        'file': filepath,
                        'line': h['line'],
                        'message': f'Heading level jumps from {prev_level} to {h["level"]}: "{h["title"]}"'
                    })
                prev_level = h['level']
            
            # Check for very long files without headings
            if len(lines) > 50 and not any(h['file'] == filepath for h in self.headings):
                issues.append({
                    'file': filepath,
                    'line': 1,
                    'message': f'{filename} has {len(lines)} lines but no headings — consider adding structure'
                })
            
            # Check for very long sections
            current_heading_line = 0
            for h in [h for h in self.headings if h['file'] == filepath]:
                if h['line'] - current_heading_line > 100:
                    issues.append({
                        'file': filepath,
                        'line': current_heading_line,
                        'message': f'Very long section ({h["line"] - current_heading_line} lines) before "{h["title"]}" — consider splitting'
                    })
                current_heading_line = h['line']
            
            # Check for empty sections
            for i, h in enumerate([h for h in self.headings if h['file'] == filepath]):
                next_headings = [h2 for h2 in self.headings if h2['file'] == filepath and h2['line'] > h['line']]
                if next_headings:
                    next_line = next_headings[0]['line']
                    section_content = '\n'.join(lines[h['line']:next_line-1]).strip()
                    if not section_content:
                        issues.append({
                            'file': filepath,
                            'line': h['line'],
                            'message': f'Empty section: "{h["title"]}"'
                        })
            
            # Check for broken internal links
            link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
            for i, line in enumerate(lines):
                for match in link_pattern.finditer(line):
                    link_text, link_target = match.groups()
                    if link_target.startswith(('#', 'http', 'mailto')):
                        continue
                    # Check if local file exists
                    target_path = Path(filepath).parent / link_target
                    if not target_path.exists():
                        issues.append({
                            'file': filepath,
                            'line': i + 1,
                            'message': f'Broken link: [{link_text}]({link_target})'
                        })
        
        self.stats['structure_issues'] = len(issues)
        
        if issues:
            self.issues['warning' if len(issues) < 5 else 'critical'].append({
                'type': 'structure',
                'message': f'{len(issues)} structural issues found',
                'details': issues[:15]
            })
        
        return issues

    def check_missing_indexes(self):
        """Check if large files are missing table of contents / indexes."""
        missing = []
        
        for filepath, content in self.files.items():
            filename = os.path.basename(filepath)
            file_headings = [h for h in self.headings if h['file'] == filepath]
            lines = content.split('\n')
            
            # Large file with many headings but no TOC
            if len(file_headings) > 5 and len(lines) > 80:
                has_toc = bool(re.search(r'(table of contents|toc|## index|## contents)', content, re.I))
                if not has_toc:
                    missing.append({
                        'file': filepath,
                        'headings': len(file_headings),
                        'lines': len(lines),
                        'message': f'{filename} has {len(file_headings)} sections and {len(lines)} lines — consider adding a table of contents'
                    })
        
        self.stats['missing_indexes'] = len(missing)
        
        if missing:
            self.issues['suggestion'].append({
                'type': 'missing_index',
                'message': f'{len(missing)} files would benefit from an index/TOC',
                'details': missing
            })
        
        return missing

    def calculate_score(self):
        """Calculate memory efficiency score (0-100)."""
        score = 100
        
        # Deductions
        score -= min(30, self.stats['duplicates'] * 3)        # -3 per duplicate, max -30
        score -= min(20, self.stats['stale_entries'] * 2)      # -2 per stale, max -20
        score -= min(15, self.stats['structure_issues'] * 3)   # -3 per issue, max -15
        score -= min(10, self.stats['missing_indexes'] * 5)    # -5 per missing index, max -10
        
        # Bonuses
        if self.stats['files_scanned'] > 0:
            # Bonus for having organized memory directory
            if (self.workspace / 'memory').exists():
                score += 5
            # Bonus for having MEMORY.md
            if (self.workspace / 'MEMORY.md').exists():
                score += 5
        
        return max(0, min(100, score))

    def analyze(self):
        """Run full analysis."""
        print(f"🧠 Agent Memory Optimizer v{VERSION}")
        print(f"Scanning workspace: {self.workspace}")
        
        self.load_files()
        
        if not self.files:
            print("No memory files found!")
            return None
        
        print(f"Found {self.stats['files_scanned']} memory files ({self.stats['total_bytes'] / 1024:.1f} KB total)")
        print("Analyzing...\n")
        
        self.extract_entries()
        self.detect_duplicates()
        self.detect_stale()
        self.check_structure()
        self.check_missing_indexes()
        
        score = self.calculate_score()
        
        # Print summary
        if score >= 80:
            emoji = "✅"
        elif score >= 60:
            emoji = "⚠️"
        else:
            emoji = "🔴"
        
        print(f"Memory Efficiency Score: {score}/100 {emoji}\n")
        print("Issues found:")
        print(f"  🔴 Critical: {len(self.issues['critical'])}")
        print(f"  🟡 Warning: {len(self.issues['warning'])}")
        print(f"  🟢 Suggestion: {len(self.issues['suggestion'])}")
        
        return {
            'score': score,
            'stats': self.stats,
            'issues': self.issues
        }

    def generate_report(self, result, output_format='markdown'):
        """Generate the full report."""
        if output_format == 'json':
            return json.dumps(result, indent=2, default=str)
        
        score = result['score']
        stats = result['stats']
        issues = result['issues']
        
        lines = []
        lines.append(f'# 🧠 Memory Optimization Report')
        lines.append(f'Workspace: {self.workspace}')
        lines.append(f'Analyzed: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}')
        lines.append('')
        lines.append(f'## Memory Efficiency Score: {score}/100')
        lines.append('')
        lines.append('### Summary')
        lines.append(f'- Files scanned: {stats["files_scanned"]}')
        lines.append(f'- Total size: {stats["total_bytes"] / 1024:.1f} KB')
        lines.append(f'- Total entries: {stats["total_entries"]}')
        lines.append(f'- Duplicates found: {stats["duplicates"]}')
        lines.append(f'- Stale entries: {stats["stale_entries"]}')
        lines.append(f'- Missing indexes: {stats["missing_indexes"]}')
        lines.append(f'- Structure issues: {stats["structure_issues"]}')
        lines.append('')
        
        if issues['critical']:
            lines.append('## 🔴 Critical Issues')
            lines.append('')
            for i, issue in enumerate(issues['critical'], 1):
                lines.append(f'{i}. **{issue["message"]}**')
                if 'details' in issue:
                    for detail in issue['details'][:10]:
                        if issue['type'] == 'duplicates':
                            e1 = detail['entry1']
                            e2 = detail['entry2']
                            sim = detail['similarity']
                            lines.append(f'   - `{e1["text"][:60]}...` ({os.path.basename(e1["file"])}:{e1["line"]})')
                            lines.append(f'     ↔ `{e2["text"][:60]}...` ({os.path.basename(e2["file"])}:{e2["line"]}) [{sim}% similar]')
                        elif issue['type'] == 'stale':
                            e = detail['entry']
                            lines.append(f'   - `{e["text"][:80]}` ({detail["age_days"]} days old)')
                        elif issue['type'] == 'structure':
                            lines.append(f'   - {detail["message"]} ({os.path.basename(detail["file"])}:{detail["line"]})')
                lines.append('')
        
        if issues['warning']:
            lines.append('## 🟡 Warnings')
            lines.append('')
            for i, issue in enumerate(issues['warning'], 1):
                lines.append(f'{i}. **{issue["message"]}**')
                if 'details' in issue:
                    for detail in issue['details'][:8]:
                        if issue['type'] == 'duplicates':
                            e1 = detail['entry1']
                            e2 = detail['entry2']
                            lines.append(f'   - `{e1["text"][:60]}` ↔ `{e2["text"][:60]}` [{detail["similarity"]}%]')
                        elif issue['type'] == 'stale':
                            e = detail['entry']
                            lines.append(f'   - `{e["text"][:80]}` ({detail["age_days"]}d old)')
                        elif issue['type'] == 'structure':
                            lines.append(f'   - {detail["message"]}')
                lines.append('')
        
        if issues['suggestion']:
            lines.append('## 🟢 Suggestions')
            lines.append('')
            for i, issue in enumerate(issues['suggestion'], 1):
                lines.append(f'{i}. **{issue["message"]}**')
                if 'details' in issue:
                    for detail in issue['details'][:5]:
                        if isinstance(detail, dict) and 'message' in detail:
                            lines.append(f'   - {detail["message"]}')
                lines.append('')
        
        # Recommended actions
        lines.append('## Recommended Actions')
        lines.append('')
        if stats['duplicates'] > 0:
            est_savings = stats['duplicates'] * 0.2  # rough estimate
            lines.append(f'- [ ] Remove {stats["duplicates"]} duplicate entries (saves ~{est_savings:.1f} KB)')
        if stats['stale_entries'] > 0:
            lines.append(f'- [ ] Archive {stats["stale_entries"]} stale entries')
        if stats['missing_indexes'] > 0:
            lines.append(f'- [ ] Add index/TOC to {stats["missing_indexes"]} large files')
        if stats['structure_issues'] > 0:
            lines.append(f'- [ ] Fix {stats["structure_issues"]} structural issues')
        if stats['duplicates'] == 0 and stats['stale_entries'] == 0 and stats['structure_issues'] == 0:
            lines.append('✅ No critical actions needed — memory is well-organized!')
        lines.append('')
        lines.append('---')
        lines.append(f'*Generated by Agent Memory Optimizer v{VERSION} | Peru 🇵🇪*')
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=f'Agent Memory Optimizer - Analyzer v{VERSION}')
    parser.add_argument('--path', default='.', help='Workspace directory to analyze')
    parser.add_argument('--output', help='Save report to file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    workspace = Path(args.path).resolve()
    if not workspace.exists():
        print(f"Error: workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)
    
    analyzer = MemoryAnalyzer(workspace, verbose=args.verbose)
    result = analyzer.analyze()
    
    if result is None:
        sys.exit(1)
    
    fmt = 'json' if args.json else 'markdown'
    report = analyzer.generate_report(result, fmt)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")
        print(f"Run `python3 optimize.py --apply` to fix issues.")
    else:
        print(f"\n{'=' * 60}")
        print(report)


if __name__ == '__main__':
    main()
