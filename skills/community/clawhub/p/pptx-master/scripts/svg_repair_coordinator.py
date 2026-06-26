#!/usr/bin/env python3
"""
PPT Master - SVG Repair Coordinator

Coordinates automatic repair of problematic SVG files, especially blank pages.

Usage:
    python3 scripts/svg_repair_coordinator.py <project_path> --check
    
This tool works with svg_content_checker.py to:
    1. Identify blank/low-content pages
    2. Attempt to regenerate them
    3. Apply fallback strategies if regeneration fails
"""

import sys
import json
import shutil
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Import content checker
try:
    from svg_content_checker import SVGContentChecker
except ImportError:
    print("[ERROR] Cannot import svg_content_checker.py")
    sys.exit(1)


class SVGRepairCoordinator:
    """Coordinates SVG repair operations"""
    
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.svg_output = self.project_path / 'svg_output'
        self.design_spec = None
        self.source_content = None
        self.retry_count: Dict[str, int] = {}
        self.repair_log: List[Dict] = []
    
    def load_context(self) -> bool:
        """Load design spec and source content for regeneration"""
        # Load design spec
        design_spec_file = self.project_path / 'design-spec.md'
        if not design_spec_file.exists():
            design_spec_file = self.project_path / 'design_spec.md'
        
        if design_spec_file.exists():
            self.design_spec = design_spec_file.read_text(encoding='utf-8')
        else:
            print("[WARN] 未找到设计规范文件")
            self.design_spec = None
        
        # Load source content
        sources_dir = self.project_path / 'sources'
        if sources_dir.exists():
            md_files = list(sources_dir.glob('*.md'))
            if md_files:
                self.source_content = md_files[0].read_text(encoding='utf-8')
                print(f"[INFO] 已加载源内容: {md_files[0].name}")
        
        return self.design_spec is not None or self.source_content is not None
    
    def check_and_repair(self) -> Dict:
        """
        Main workflow: check SVGs and repair issues
        
        Returns:
            Summary of check and repair operations
        """
        print("\n" + "=" * 80)
        print("[PHASE 1] 内容完整性检查")
        print("=" * 80)
        
        # Run content checker
        checker = SVGContentChecker()
        checker.load_design_spec(self.project_path)
        checker.check_directory(self.project_path)
        
        # Get issues
        blank_pages = checker.get_blank_pages()
        issues = checker.get_issues()
        
        result = {
            'project': str(self.project_path),
            'timestamp': datetime.now().isoformat(),
            'check_summary': checker.summary,
            'blank_pages': [r['file'] for r in blank_pages],
            'issues': [r['file'] for r in issues],
            'repairs': []
        }
        
        # Print summary
        checker.print_summary()
        
        if not blank_pages:
            print("\n✅ 未发现空白页，无需修复")
            return result
        
        # Phase 2: Repair
        print("\n" + "=" * 80)
        print(f"[PHASE 2] 自动修复（发现 {len(blank_pages)} 个空白页）")
        print("=" * 80)
        
        # Load context for regeneration
        self.load_context()
        
        for blank_page in blank_pages:
            svg_file = self.svg_output / blank_page['file']
            repair_result = self.repair_file(svg_file, blank_page)
            result['repairs'].append(repair_result)
        
        # Phase 3: Re-check
        print("\n" + "=" * 80)
        print("[PHASE 3] 二次审核")
        print("=" * 80)
        
        checker2 = SVGContentChecker()
        checker2.load_design_spec(self.project_path)
        checker2.check_directory(self.project_path)
        checker2.print_summary()
        
        result['final_summary'] = checker2.summary
        
        return result
    
    def repair_file(self, svg_file: Path, issue_info: Dict) -> Dict:
        """
        Repair a single SVG file
        
        Args:
            svg_file: Path to SVG file
            issue_info: Issue information from checker
            
        Returns:
            Repair result
        """
        file_name = svg_file.name
        
        print(f"\n[REPAIR] 修复: {file_name}")
        print(f"  问题: {', '.join(issue_info.get('errors', ['空白页']))}")
        
        # Check retry count
        if self.retry_count.get(file_name, 0) >= self.MAX_RETRIES:
            print(f"  ⚠️ 重试次数已达上限，使用回退策略")
            return self._fallback_strategy(svg_file, issue_info)
        
        # Attempt repair strategies
        strategies = [
            ('regenerate', self._regenerate_page),
            ('enhance', self._enhance_content),
        ]
        
        for strategy_name, strategy_func in strategies:
            self.retry_count[file_name] = self.retry_count.get(file_name, 0) + 1
            
            print(f"  尝试策略: {strategy_name} (第 {self.retry_count[file_name]} 次)")
            
            success, message = strategy_func(svg_file, issue_info)
            
            if success:
                print(f"  ✅ 修复成功: {message}")
                return {
                    'file': file_name,
                    'status': 'repaired',
                    'strategy': strategy_name,
                    'message': message,
                    'attempts': self.retry_count[file_name]
                }
            else:
                print(f"  ❌ 策略失败: {message}")
        
        # All strategies failed, use fallback
        print(f"  ⚠️ 所有策略失败，使用回退策略")
        return self._fallback_strategy(svg_file, issue_info)
    
    def _regenerate_page(self, svg_file: Path, issue_info: Dict) -> Tuple[bool, str]:
        """
        Regenerate the page using LLM
        
        This extracts the page context and generates new SVG content.
        In multi-turn conversation, the agent has access to design_spec and sources.
        """
        if not self.design_spec:
            return False, "缺少设计规范"
        
        if not self.source_content:
            return False, "缺少源内容"
        
        # Extract page index from filename (e.g., "05_content.svg" -> 4)
        file_name = svg_file.name
        page_match = re.match(r'(\d+)_', file_name)
        if page_match:
            page_index = int(page_match.group(1)) - 1  # 0-based index
        else:
            page_index = 0
        
        # Extract page structure from design_spec
        page_structure = self._extract_page_structure(page_index)
        
        if not page_structure:
            return False, f"无法从设计规范中提取第 {page_index + 1} 页的结构"
        
        # Generate regeneration prompt
        prompt = self._build_regeneration_prompt(page_index, page_structure)
        
        # Save prompt for manual review or LLM call
        prompt_file = self.project_path / f'.repair_prompt_{file_name}.md'
        prompt_file.write_text(prompt, encoding='utf-8')
        
        # In a real implementation, this would call the LLM
        # For now, we return the prompt for manual execution
        return False, f"已生成重新生成提示词: {prompt_file.name}，请在当前会话中执行"
    
    def _extract_page_structure(self, page_index: int) -> Optional[Dict]:
        """Extract page structure from design_spec"""
        if not self.design_spec:
            return None
        
        # Parse design_spec to find page structure
        lines = self.design_spec.split('\n')
        page_lines = []
        capturing = False
        
        for line in lines:
            # Detect page markers
            page_marker = re.match(r'(?:Page|Slide|第)\s*(\d+)', line, re.IGNORECASE)
            if page_marker:
                detected_page = int(page_marker.group(1)) - 1
                if detected_page == page_index:
                    capturing = True
                elif capturing:
                    break  # Stop at next page
            
            if capturing:
                page_lines.append(line)
        
        if page_lines:
            return {
                'page_index': page_index,
                'content': '\n'.join(page_lines),
                'line_count': len(page_lines)
            }
        
        # Fallback: estimate page content from overall structure
        return {
            'page_index': page_index,
            'content': f'第 {page_index + 1} 页内容',
            'estimated': True
        }
    
    def _build_regeneration_prompt(self, page_index: int, page_structure: Dict) -> str:
        """Build prompt for page regeneration"""
        
        # Get source content snippet
        source_snippet = self.source_content[:3000] if self.source_content else ""
        
        prompt = f"""# SVG 页面重新生成任务

## 任务说明
请重新生成 PPT 第 {page_index + 1} 页的 SVG 内容。

## 问题说明
该页面被检测为空白页或内容缺失，需要重新生成。

## 设计规范（来自 design_spec.md）
```markdown
{self.design_spec[:2000]}
```

## 页面结构（第 {page_index + 1} 页）
```markdown
{page_structure.get('content', '未找到页面结构')}
```

## 源内容摘要
```markdown
{source_snippet}
```

## 生成要求
1. **画布尺寸**: 1280x720 (标准 16:9)
2. **内容要求**: 
   - 至少 3 个文本元素（<text>）
   - 至少 1 个图形元素（<rect>, <circle>, <path> 等）
   - 内容密度 > 30%
3. **风格要求**: 遵循设计规范中的颜色方案和字体
4. **输出格式**: 完整的 SVG 代码，以 <?xml version="1.0" encoding="UTF-8"?> 开头

## 输出
请直接输出 SVG 代码，不要包含其他解释。
"""
        
        return prompt
    
    def _enhance_content(self, svg_file: Path, issue_info: Dict) -> Tuple[bool, str]:
        """
        Try to enhance existing content
        
        This works for pages that have some content but are flagged as low-quality.
        """
        try:
            content = svg_file.read_text(encoding='utf-8')
            
            # Check if this is actually a blank page or just low content
            if issue_info.get('is_blank'):
                return False, "确认为空白页，无法增强"
            
            # For low-content pages, we could try to add more content
            # This is a placeholder for content enhancement logic
            return False, "内容增强功能待实现"
            
        except Exception as e:
            return False, f"读取文件失败: {e}"
    
    def _fallback_strategy(self, svg_file: Path, issue_info: Dict) -> Dict:
        """
        Apply fallback strategy when repair fails
        
        Options:
        1. Create a placeholder page
        2. Remove the page from the presentation
        3. Mark for manual review
        """
        file_name = svg_file.name
        
        # Create placeholder SVG
        placeholder_svg = self._create_placeholder_svg(svg_file, issue_info)
        
        # Backup original file
        backup_file = svg_file.with_suffix('.svg.bak')
        if svg_file.exists():
            shutil.copy(svg_file, backup_file)
        
        # Write placeholder
        svg_file.write_text(placeholder_svg, encoding='utf-8')
        
        print(f"  📝 已创建占位符页面")
        
        return {
            'file': file_name,
            'status': 'fallback',
            'strategy': 'placeholder',
            'message': '已创建占位符，请手动修复',
            'backup': str(backup_file),
            'attempts': self.retry_count.get(file_name, 0)
        }
    
    def _create_placeholder_svg(self, svg_file: Path, issue_info: Dict) -> str:
        """Create a placeholder SVG for problematic pages"""
        
        # Try to get viewBox from original file
        viewbox = "0 0 1280 720"
        try:
            content = svg_file.read_text(encoding='utf-8')
            import re
            match = re.search(r'viewBox="([^"]+)"', content)
            if match:
                viewbox = match.group(1)
        except:
            pass
        
        # Create placeholder
        placeholder = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">
  <!-- Placeholder page - content generation failed -->
  <rect width="100%" height="100%" fill="#F5F5F5"/>
  
  <!-- Warning banner -->
  <rect x="340" y="280" width="600" height="160" rx="8" fill="#FFF3CD" stroke="#FFC107" stroke-width="2"/>
  
  <!-- Warning icon -->
  <text x="640" y="330" text-anchor="middle" font-family="Arial, sans-serif" font-size="48" fill="#856404">⚠️</text>
  
  <!-- Warning message -->
  <text x="640" y="380" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#856404">
    <tspan x="640" dy="0">内容生成失败</tspan>
  </text>
  <text x="640" y="410" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="#856404">
    <tspan x="640" dy="0">请手动修复此页面: {svg_file.name}</tspan>
  </text>
  
  <!-- Timestamp -->
  <text x="640" y="700" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#999999">
    <tspan>Generated by SVG Repair Coordinator - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</tspan>
  </text>
</svg>'''
        
        return placeholder
    
    def export_repair_log(self, output_file: str = 'repair_log.json'):
        """Export repair log"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.repair_log, f, ensure_ascii=False, indent=2)
        print(f"\n[LOG] 修复日志已导出: {output_file}")


def main() -> None:
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("PPT Master - SVG 修复协调器\n")
        print("用法:")
        print("  python3 scripts/svg_repair_coordinator.py <project_path>")
        print("  python3 scripts/svg_repair_coordinator.py <project_path> --check-only")
        print("\n选项:")
        print("  --check-only    仅检查，不执行修复")
        print("  --export-log    导出修复日志")
        sys.exit(0)
    
    project_path = Path(sys.argv[1])
    
    if not project_path.exists():
        print(f"[ERROR] 项目目录不存在: {project_path}")
        sys.exit(1)
    
    # Create coordinator
    coordinator = SVGRepairCoordinator(project_path)
    
    # Parse options
    check_only = '--check-only' in sys.argv
    
    if check_only:
        # Only run content checker
        print("\n[CHECK ONLY MODE] 仅执行检查")
        checker = SVGContentChecker()
        checker.load_design_spec(project_path)
        checker.check_directory(project_path)
        checker.print_summary()
        
        if checker.summary['blank_pages'] > 0:
            sys.exit(2)
        sys.exit(0)
    
    # Run full repair workflow
    result = coordinator.check_and_repair()
    
    # Export log if requested
    if '--export-log' in sys.argv:
        coordinator.export_repair_log('repair_log.json')
    
    # Print final status
    print("\n" + "=" * 80)
    print("[FINAL STATUS]")
    print("=" * 80)
    
    if result['final_summary']['blank_pages'] == 0:
        print("✅ 所有空白页已处理")
        sys.exit(0)
    else:
        print(f"⚠️ 仍有 {result['final_summary']['blank_pages']} 个空白页")
        sys.exit(2)


if __name__ == '__main__':
    main()
