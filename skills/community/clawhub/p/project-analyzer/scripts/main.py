"""
Project Analyzer - SDD 软件设计文档生成器
核心入口脚本
"""

import argparse
import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from harness_engine import HarnessEngine
from project_scanner import ProjectScanner
from database_scanner import DatabaseScanner
from api_scanner import APIScanner
from doc_generator import DocumentGenerator
from constraint_checker import ConstraintChecker
from feedback_loop import FeedbackLoop
from entropy_manager import EntropyManager


class ProjectAnalyzer:
    """SDD 文档分析生成器"""
    
    def __init__(self, project_path: str, output_dir: str = "docs/sdd"):
        self.project_path = Path(project_path)
        self.output_dir = Path(output_dir)
        self.context = {}
        
        # 初始化组件
        self.scanner = ProjectScanner(project_path)
        self.db_scanner = DatabaseScanner(project_path)
        self.api_scanner = APIScanner(project_path)
        self.generator = DocumentGenerator()
        self.constraint_checker = ConstraintChecker()
        self.feedback_loop = FeedbackLoop()
        self.entropy_manager = EntropyManager()
        
    def analyze(self) -> dict:
        """执行完整分析"""
        print(f"🔍 开始分析项目: {self.project_path}")
        
        # Phase 1: 项目扫描
        print("\n📦 Phase 1: 项目结构扫描...")
        project_info = self.scanner.scan()
        self.context['project'] = project_info
        print(f"   ✅ 项目类型: {project_info.get('type', 'unknown')}")
        print(f"   ✅ 技术栈: {project_info.get('tech_stack', {})}")
        
        # Phase 2: 数据库扫描
        print("\n🗄️ Phase 2: 数据库结构扫描...")
        db_info = self.db_scanner.scan()
        self.context['database'] = db_info
        print(f"   ✅ 数据库类型: {db_info.get('db_type', 'unknown')}")
        print(f"   ✅ 表数量: {len(db_info.get('tables', []))}")
        
        # Phase 3: API 扫描
        print("\n📡 Phase 3: API 接口扫描...")
        api_info = self.api_scanner.scan()
        self.context['api'] = api_info
        print(f"   ✅ Controller 数量: {api_info.get('controller_count', 0)}")
        print(f"   ✅ 接口数量: {api_info.get('endpoint_count', 0)}")
        
        # Phase 4: 生成文档
        print("\n📝 Phase 4: 文档生成...")
        docs = self._generate_documents()
        
        # Phase 5: 质量校验
        print("\n✅ Phase 5: 质量校验...")
        quality_report = self._validate_quality(docs)
        
        return {
            'context': self.context,
            'documents': docs,
            'quality_report': quality_report
        }
    
    def _generate_documents(self) -> dict:
        """生成所有文档"""
        docs = {}
        
        # 定义要生成的文档类型
        doc_types = ['srs', 'sad', 'sdd', 'dbd', 'apid', 'tsd']
        
        for doc_type in doc_types:
            print(f"   📄 生成 {doc_type.upper()} 文档...")
            
            # 生成文档内容
            content = self.generator.generate(doc_type, self.context)
            
            # 约束检查
            passed, fixed = self.constraint_checker.enforce(content)
            if not passed:
                print(f"      ⚠️ 约束检查未通过，自动修复...")
            
            # 熵管理 - 清理输出
            final_content = self.entropy_manager.clean(fixed)
            
            # 保存文档
            output_file = self.output_dir / f"01-{doc_type}.md"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(final_content, encoding='utf-8')
            
            docs[doc_type] = {
                'content': final_content,
                'file': str(output_file),
                'constraint_passed': passed
            }
            
            print(f"      ✅ {output_file}")
        
        return docs
    
    def _validate_quality(self, docs: dict) -> dict:
        """质量校验"""
        report = {
            'total_docs': len(docs),
            'passed_docs': 0,
            'issues': [],
            'summary': {}
        }
        
        for doc_type, doc_info in docs.items():
            validation = self.feedback_loop.validate({
                'type': doc_type,
                'content': doc_info['content']
            })
            
            report['summary'][doc_type] = validation
            
            if validation['passed']:
                report['passed_docs'] += 1
            else:
                report['issues'].extend(validation.get('issues', []))
        
        report['pass_rate'] = report['passed_docs'] / report['total_docs'] * 100
        
        return report
    
    def generate_report(self) -> str:
        """生成分析报告"""
        report = f"""
================================================================================
                         SDD 文档生成报告
================================================================================

📁 项目路径: {self.project_path}
📂 输出目录: {self.output_dir}

--------------------------------------------------------------------------------
                              项目概况
--------------------------------------------------------------------------------

项目类型: {self.context.get('project', {}).get('type', 'unknown')}
技术栈: {self.context.get('project', {}).get('tech_stack', {})}
数据库: {self.context.get('database', {}).get('db_type', 'unknown')} ({len(self.context.get('database', {}).get('tables', []))} 张表)
接口数: {self.context.get('api', {}).get('endpoint_count', 0)} 个

--------------------------------------------------------------------------------
                              文档生成
--------------------------------------------------------------------------------

"""
        for doc_type, doc_info in self.context.get('documents', {}).items():
            status = "✅" if doc_info.get('constraint_passed') else "⚠️"
            report += f" {status} {doc_type.upper()} 文档\n"
        
        report += f"""
--------------------------------------------------------------------------------
                              质量报告
--------------------------------------------------------------------------------

总文档数: {self.context.get('quality_report', {}).get('total_docs', 0)}
通过数: {self.context.get('quality_report', {}).get('passed_docs', 0)}
通过率: {self.context.get('quality_report', {}).get('pass_rate', 0):.1f}%

================================================================================
"""
        return report


def main():
    parser = argparse.ArgumentParser(
        description='SDD 软件设计文档生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --project-path /path/to/project
  python main.py --project-path /path/to/project --output docs/sdd
  python main.py --project-path /path/to/project --type srs --type sad
        """
    )
    
    parser.add_argument(
        '--project-path', '-p',
        required=True,
        help='项目路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='docs/sdd',
        help='输出目录 (默认: docs/sdd)'
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['srs', 'sad', 'sdd', 'dbd', 'apid', 'tsd'],
        action='append',
        help='指定要生成的文档类型'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='约束配置文件路径'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细输出'
    )
    
    args = parser.parse_args()
    
    # 验证项目路径
    if not Path(args.project_path).exists():
        print(f"❌ 项目路径不存在: {args.project_path}")
        sys.exit(1)
    
    # 执行分析
    analyzer = ProjectAnalyzer(args.project_path, args.output)
    result = analyzer.analyze()
    
    # 输出报告
    print(analyzer.generate_report())
    
    print("\n📖 文档已生成，请查阅输出目录")


if __name__ == '__main__':
    main()
