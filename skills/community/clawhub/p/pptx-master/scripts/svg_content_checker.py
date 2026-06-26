#!/usr/bin/env python3
"""
PPT Master - SVG Content Completeness Checker

Checks whether SVG files have sufficient content (not blank pages).

Usage:
    python3 scripts/svg_content_checker.py <svg_file>
    python3 scripts/svg_content_checker.py <directory>
    python3 scripts/svg_content_checker.py --project <project_path>

This tool focuses on content completeness, complementing svg_quality_checker.py
which handles technical specification compliance.
"""

import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict
from datetime import datetime


class SVGContentChecker:
    """SVG content completeness checker"""
    
    # Thresholds for blank page detection
    MIN_TEXT_ELEMENTS = 2
    MIN_FILE_SIZE_BYTES = 500
    MIN_CONTENT_DENSITY = 0.3  # 30% of viewBox area should have content
    
    def __init__(self):
        self.results = []
        self.summary = {
            'total': 0,
            'passed': 0,
            'warnings': 0,
            'errors': 0,
            'blank_pages': 0,
            'low_content': 0
        }
        self.design_spec = None
    
    def load_design_spec(self, project_path: Path) -> bool:
        """Load design specification from project directory"""
        design_spec_file = project_path / 'design-spec.md'
        if not design_spec_file.exists():
            design_spec_file = project_path / 'design_spec.md'
        
        if design_spec_file.exists():
            self.design_spec = self._parse_design_spec(design_spec_file.read_text())
            return True
        
        return False
    
    def _parse_design_spec(self, content: str) -> Dict:
        """Parse design specification to extract color scheme and fonts"""
        spec = {
            'colors': [],
            'fonts': []
        }
        
        # Extract colors (hex format)
        colors = re.findall(r'#[0-9A-Fa-f]{6}', content)
        spec['colors'] = list(set(colors))
        
        # Extract fonts
        font_match = re.search(r'font-family[:\s]*["\']([^"\']+)["\']', content, re.IGNORECASE)
        if font_match:
            spec['fonts'].append(font_match.group(1))
        
        return spec
    
    def check_file(self, svg_file: Path) -> Dict:
        """
        Check a single SVG file for content completeness
        
        Args:
            svg_file: Path to SVG file
            
        Returns:
            Check result dictionary
        """
        if not svg_file.exists():
            return {
                'file': svg_file.name,
                'exists': False,
                'errors': ['File does not exist'],
                'warnings': [],
                'passed': False
            }
        
        result = {
            'file': svg_file.name,
            'path': str(svg_file),
            'exists': True,
            'errors': [],
            'warnings': [],
            'info': {},
            'passed': True,
            'is_blank': False,
            'content_score': 0.0
        }
        
        try:
            content = svg_file.read_text(encoding='utf-8')
            file_size = svg_file.stat().st_size
            
            # Store basic info
            result['info']['file_size'] = file_size
            
            # 1. Check content elements
            self._check_content_elements(content, result)
            
            # 2. Check content density
            self._check_content_density(content, result)
            
            # 3. Check structure completeness
            self._check_structure(content, result)
            
            # 4. Check design consistency (if design spec loaded)
            if self.design_spec:
                self._check_design_consistency(content, result)
            
            # Determine if blank page
            result['is_blank'] = self._is_blank_page(result)
            
            if result['is_blank']:
                result['errors'].append('空白页：内容缺失或过于稀疏')
                result['passed'] = False
            
            # Calculate content score
            result['content_score'] = self._calculate_content_score(result)
            
            if result['content_score'] < 0.3:
                result['warnings'].append(f'内容密度较低 ({result["content_score"]:.0%})')
            
        except Exception as e:
            result['errors'].append(f"读取文件失败: {e}")
            result['passed'] = False
        
        # Update statistics
        self.summary['total'] += 1
        if result['passed']:
            if result['warnings']:
                self.summary['warnings'] += 1
            else:
                self.summary['passed'] += 1
        else:
            self.summary['errors'] += 1
            if result['is_blank']:
                self.summary['blank_pages'] += 1
        
        if result['content_score'] < 0.3:
            self.summary['low_content'] += 1
        
        self.results.append(result)
        return result
    
    def _check_content_elements(self, content: str, result: Dict):
        """Check for presence of content elements"""
        
        # XML parsing validation (CRITICAL)
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(content)
        except ET.ParseError as e:
            result['errors'].append(f'XML语法错误: {str(e)[:100]}')
            result['passed'] = False
            return  # Stop further checks if XML is invalid
        except Exception as e:
            result['errors'].append(f'XML解析失败: {str(e)[:100]}')
            result['passed'] = False
            return
        
        # Count text elements
        text_count = content.count('<text')
        tspan_count = content.count('<tspan')
        
        # Count graphic elements
        rect_count = content.count('<rect')
        circle_count = content.count('<circle')
        line_count = content.count('<line')
        path_count = content.count('<path')
        image_count = content.count('<image')
        
        result['info']['text_elements'] = text_count
        result['info']['tspan_elements'] = tspan_count
        result['info']['graphic_elements'] = rect_count + circle_count + line_count + path_count
        result['info']['image_elements'] = image_count
        
        # Check minimum text elements
        if text_count < self.MIN_TEXT_ELEMENTS:
            result['warnings'].append(
                f'文本元素较少 ({text_count} 个，建议至少 {self.MIN_TEXT_ELEMENTS} 个)'
            )
    
    def _check_content_density(self, content: str, result: Dict):
        """Check content density based on viewBox and actual content"""
        # Extract viewBox
        viewbox_match = re.search(r'viewBox="(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"', content)
        
        if viewbox_match:
            x, y, width, height = map(int, viewbox_match.groups())
            viewbox_area = width * height
            
            result['info']['viewbox_area'] = viewbox_area
            
            # Estimate content area by counting positioned elements
            # This is a rough estimation
            text_positions = re.findall(r'<text[^>]*x="(\d+)"[^>]*y="(\d+)"', content)
            
            if text_positions:
                # Rough estimate: each text element covers ~100x30 pixels
                estimated_content_area = len(text_positions) * 3000
                
                density = min(estimated_content_area / viewbox_area, 1.0)
                result['info']['content_density'] = density
            else:
                result['info']['content_density'] = 0.0
    
    def _check_structure(self, content: str, result: Dict):
        """Check if SVG has basic structure (title, body content)"""
        # Check for common structural patterns
        has_title = bool(re.search(r'font-size=["\'](?:3[2-9]|[4-9]\d|\d{3,})["\']', content))
        has_body = result['info'].get('text_elements', 0) >= 3
        has_visuals = result['info'].get('graphic_elements', 0) >= 1 or result['info'].get('image_elements', 0) >= 1
        
        result['info']['has_title'] = has_title
        result['info']['has_body'] = has_body
        result['info']['has_visuals'] = has_visuals
        
        # Structure completeness score
        structure_score = sum([has_title, has_body, has_visuals]) / 3.0
        result['info']['structure_score'] = structure_score
        
        if structure_score < 0.5:
            result['warnings'].append('页面结构不完整')
    
    def _check_design_consistency(self, content: str, result: Dict):
        """Check if design is consistent with design specification"""
        if not self.design_spec:
            return
        
        # Check color consistency
        colors_in_svg = set(re.findall(r'#[0-9A-Fa-f]{6}', content))
        expected_colors = set(self.design_spec.get('colors', []))
        
        if expected_colors:
            matching_colors = colors_in_svg & expected_colors
            color_consistency = len(matching_colors) / len(colors_in_svg) if colors_in_svg else 0
            
            result['info']['color_consistency'] = color_consistency
            
            if color_consistency < 0.5:
                result['warnings'].append(
                    f'颜色偏离设计规范 ({color_consistency:.0%} 匹配)'
                )
        
        # Check font consistency
        fonts_in_svg = re.findall(r'font-family[:\s]*["\']([^"\']+)["\']', content, re.IGNORECASE)
        expected_fonts = self.design_spec.get('fonts', [])
        
        if expected_fonts and fonts_in_svg:
            font_match = any(
                any(expected.lower() in font.lower() for expected in expected_fonts)
                for font in fonts_in_svg
            )
            
            result['info']['font_consistent'] = font_match
            
            if not font_match:
                result['warnings'].append('字体与设计规范不一致')
    
    def _is_blank_page(self, result: Dict) -> bool:
        """Determine if the page is blank"""
        # Criteria for blank page:
        # 1. Very few text elements AND small file size
        # 2. OR very low content density
        
        text_elements = result['info'].get('text_elements', 0)
        file_size = result['info'].get('file_size', 0)
        content_density = result['info'].get('content_density', 0)
        
        # Blank if: few text elements + small file
        if text_elements < self.MIN_TEXT_ELEMENTS and file_size < self.MIN_FILE_SIZE_BYTES:
            return True
        
        # Blank if: almost no content density
        if content_density < 0.05 and text_elements < 1:
            return True
        
        return False
    
    def _calculate_content_score(self, result: Dict) -> float:
        """Calculate overall content completeness score (0-1)"""
        scores = []
        
        # Text element score (0-1)
        text_elements = result['info'].get('text_elements', 0)
        text_score = min(text_elements / 5.0, 1.0)  # 5 elements = full score
        scores.append(text_score)
        
        # Structure score
        structure_score = result['info'].get('structure_score', 0)
        scores.append(structure_score)
        
        # Content density score
        density = result['info'].get('content_density', 0)
        density_score = min(density * 3, 1.0)  # 33% density = full score
        scores.append(density_score)
        
        # Visual elements score
        graphics = result['info'].get('graphic_elements', 0)
        images = result['info'].get('image_elements', 0)
        visual_score = min((graphics + images * 2) / 5.0, 1.0)
        scores.append(visual_score)
        
        return sum(scores) / len(scores)
    
    def check_directory(self, directory: Path) -> List[Dict]:
        """
        Check all SVG files in a directory
        
        Args:
            directory: Directory path (project path or svg_output path)
            
        Returns:
            List of check results
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            print(f"[ERROR] 目录不存在: {directory}")
            return []
        
        # Try to load design spec from project
        self.load_design_spec(dir_path)
        
        # Find SVG files
        if dir_path.is_file() and dir_path.suffix == '.svg':
            svg_files = [dir_path]
        else:
            # Check for svg_output subdirectory
            svg_output = dir_path / 'svg_output' if (dir_path / 'svg_output').exists() else dir_path
            svg_files = sorted(svg_output.glob('*.svg'))
        
        if not svg_files:
            print(f"[WARN] 未找到 SVG 文件")
            return []
        
        print(f"\n[SCAN] 检查 {len(svg_files)} 个 SVG 文件...\n")
        
        for svg_file in svg_files:
            result = self.check_file(svg_file)
            self._print_result(result)
        
        return self.results
    
    def _print_result(self, result: Dict):
        """Print check result for a single file"""
        if result['is_blank']:
            icon = "[BLANK]"
            status = "空白页"
            color_code = "\033[91m"  # Red
        elif result['passed']:
            if result['warnings']:
                icon = "[WARN]"
                status = "通过（有警告）"
                color_code = "\033[93m"  # Yellow
            else:
                icon = "[OK]"
                status = "通过"
                color_code = "\033[92m"  # Green
        else:
            icon = "[ERROR]"
            status = "失败"
            color_code = "\033[91m"  # Red
        
        reset_code = "\033[0m"
        
        # Print result
        print(f"{color_code}{icon}{reset_code} {result['file']} - {status}")
        
        # Print content score
        score = result.get('content_score', 0)
        score_icon = "█" * int(score * 5) + "░" * (5 - int(score * 5))
        print(f"     内容评分: [{score_icon}] {score:.0%}")
        
        # Print info
        if result['info']:
            info_parts = []
            if 'text_elements' in result['info']:
                info_parts.append(f"文本: {result['info']['text_elements']}")
            if 'graphic_elements' in result['info']:
                info_parts.append(f"图形: {result['info']['graphic_elements']}")
            if 'file_size' in result['info']:
                size_kb = result['info']['file_size'] / 1024
                info_parts.append(f"大小: {size_kb:.1f}KB")
            if info_parts:
                print(f"     {' | '.join(info_parts)}")
        
        # Print errors
        if result['errors']:
            for error in result['errors']:
                print(f"     [ERROR] {error}")
        
        # Print warnings
        if result['warnings']:
            for warning in result['warnings'][:2]:
                print(f"     [WARN] {warning}")
        
        print()
    
    def print_summary(self):
        """Print check summary"""
        print("=" * 80)
        print("[SUMMARY] 内容完整性检查报告")
        print("=" * 80)
        
        print(f"\n总页数: {self.summary['total']}")
        print(f"  ✅ 完全通过: {self.summary['passed']} ({self._percentage(self.summary['passed'])}%)")
        print(f"  ⚠️  有警告: {self.summary['warnings']} ({self._percentage(self.summary['warnings'])}%)")
        print(f"  ❌ 有错误: {self.summary['errors']} ({self._percentage(self.summary['errors'])}%)")
        print(f"  📄 空白页: {self.summary['blank_pages']}")
        print(f"  📉 内容稀疏: {self.summary['low_content']}")
        
        if self.summary['blank_pages'] > 0:
            print(f"\n[ALERT] 发现 {self.summary['blank_pages']} 个空白页，建议修复后再导出")
    
    def _percentage(self, count: int) -> int:
        """Calculate percentage"""
        if self.summary['total'] == 0:
            return 0
        return int(count / self.summary['total'] * 100)
    
    def get_blank_pages(self) -> List[Dict]:
        """Get list of blank pages"""
        return [r for r in self.results if r.get('is_blank')]
    
    def get_issues(self) -> List[Dict]:
        """Get list of files with issues"""
        return [r for r in self.results if not r['passed'] or r.get('is_blank')]
    
    def export_report(self, output_file: str = 'svg_content_report.json'):
        """Export check report as JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.summary,
            'results': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n[REPORT] 报告已导出: {output_file}")


def main() -> None:
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("PPT Master - SVG 内容完整性检查工具\n")
        print("用法:")
        print("  python3 scripts/svg_content_checker.py <svg_file>")
        print("  python3 scripts/svg_content_checker.py <directory>")
        print("  python3 scripts/svg_content_checker.py --project <project_path>")
        print("\n示例:")
        print("  python3 scripts/svg_content_checker.py svg_output/slide_01.svg")
        print("  python3 scripts/svg_content_checker.py projects/my_project")
        print("  python3 scripts/svg_content_checker.py svg_output --export report.json")
        sys.exit(0)
    
    checker = SVGContentChecker()
    
    # Parse arguments
    target = sys.argv[1]
    
    if target == '--project' and len(sys.argv) > 2:
        # Check project directory
        project_path = Path(sys.argv[2])
        checker.load_design_spec(project_path)
        checker.check_directory(project_path)
    else:
        # Check file or directory
        checker.check_directory(Path(target))
    
    # Print summary
    checker.print_summary()
    
    # Export report if requested
    if '--export' in sys.argv:
        idx = sys.argv.index('--export')
        output_file = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else 'svg_content_report.json'
        checker.export_report(output_file)
    
    # Return exit code
    if checker.summary['blank_pages'] > 0:
        sys.exit(2)  # Exit code 2 for blank pages
    elif checker.summary['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
