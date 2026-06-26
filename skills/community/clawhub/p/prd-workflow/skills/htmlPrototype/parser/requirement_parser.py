#!/usr/bin/env python3
"""
需求文档解析器

功能：
1. 读取 PRD/需求文档
2. 提取页面类型、功能需求、组件需求
3. 转换为原型生成参数
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

class RequirementParser:
    """需求文档解析器"""
    
    def __init__(self):
        self.page_type_keywords = {
            'list': ['列表', '清单', '表格', 'list', 'table'],
            'form': ['表单', '填写', '输入', 'form', 'input'],
            'dashboard': ['仪表盘', '看板', '仪表板', 'dashboard', '统计'],
            'detail': ['详情', '明细', 'detail', '查看'],
            'login': ['登录', '登陆', 'login', 'signin']
        }
        
        self.component_keywords = {
            '表格': ['表格', '列表', '数据展示'],
            '筛选': ['筛选', '过滤', '搜索'],
            '分页': ['分页', '翻页'],
            '按钮': ['按钮', '操作'],
            '图表': ['图表', '统计图', '趋势'],
            '卡片': ['卡片', '数据卡片', '指标']
        }
    
    def parse_file(self, file_path: str) -> Dict:
        """
        解析需求文档文件
        
        Args:
            file_path: 文件路径（.md/.txt/.docx）
        
        Returns:
            解析结果字典
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        content = self._read_file(file_path)
        return self.parse_content(content, file_path.name)
    
    def _read_file(self, file_path: Path) -> str:
        """读取文件内容"""
        ext = file_path.suffix.lower()
        
        if ext in ['.md', '.txt', '.text']:
            return file_path.read_text(encoding='utf-8')
        elif ext == '.docx':
            try:
                import docx
                doc = docx.Document(file_path)
                return '\n'.join([p.text for p in doc.paragraphs])
            except ImportError:
                print("⚠️ 需要安装 python-docx: pip install python-docx")
                return file_path.read_text(encoding='utf-8', errors='ignore')
        elif ext == '.pdf':
            print("⚠️ PDF 文件需要额外处理，请转换为文本格式")
            return ""
        else:
            return file_path.read_text(encoding='utf-8', errors='ignore')
    
    def parse_content(self, content: str, filename: str = "") -> Dict:
        """
        解析文本内容
        
        Args:
            content: 文本内容
            filename: 文件名（可选）
        
        Returns:
            解析结果
        """
        result = {
            'page_type': self._detect_page_type(content),
            'keywords': self._extract_keywords(content),
            'components': self._extract_components(content),
            'features': self._extract_features(content),
            'style_preference': self._detect_style(content),
            'source_file': filename
        }
        
        return result
    
    def _detect_page_type(self, content: str) -> str:
        """检测页面类型"""
        content_lower = content.lower()
        
        scores = {}
        for page_type, keywords in self.page_type_keywords.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            scores[page_type] = score
        
        # 返回得分最高的类型
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'list'  # 默认
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取业务关键词"""
        keywords = []
        
        business_domains = {
            '产品': ['产品', '商品', '物品'],
            '用户': ['用户', '客户', '会员', '账号'],
            '订单': ['订单', '订购', '下单'],
            '销售': ['销售', '销售额', '成交'],
            '电商': ['电商', '商城', '店铺'],
            '财务': ['财务', '资金', '账单'],
            '库存': ['库存', '仓储', '存货']
        }
        
        for domain, terms in business_domains.items():
            if any(term in content for term in terms):
                keywords.append(domain)
        
        return keywords
    
    def _extract_components(self, content: str) -> List[str]:
        """提取组件需求"""
        components = []
        
        for comp, terms in self.component_keywords.items():
            if any(term in content for term in terms):
                components.append(comp)
        
        return components
    
    def _extract_features(self, content: str) -> List[str]:
        """提取功能需求"""
        features = []
        
        # 常见功能关键词
        feature_patterns = [
            r'(支持 | 需要 | 包含 | 具备).*?(筛选 | 搜索 | 过滤)',
            r'(支持 | 需要 | 包含 | 具备).*?(导出 | 导入)',
            r'(支持 | 需要 | 包含 | 具备).*?(分页 | 翻页)',
            r'(支持 | 需要 | 包含 | 具备).*?(编辑 | 修改 | 删除)',
            r'(支持 | 需要 | 包含 | 具备).*?(统计 | 分析)',
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, content)
            features.extend(matches)
        
        return list(set(features))
    
    def _detect_style(self, content: str) -> str:
        """检测风格偏好"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['商务', '专业', '企业', '正式']):
            return 'business'
        elif any(word in content_lower for word in ['活泼', '清新', '年轻', '活力']):
            return 'fresh'
        else:
            return 'modern'  # 默认现代简约
    
    def generate_suggestions(self, parsed: Dict) -> List[str]:
        """
        根据解析结果生成建议
        
        Args:
            parsed: 解析结果
        
        Returns:
            建议列表
        """
        suggestions = []
        
        # 根据页面类型建议
        if parsed['page_type'] == 'list':
            suggestions.append("建议包含：搜索框、表格、分页器、操作按钮")
        elif parsed['page_type'] == 'dashboard':
            suggestions.append("建议包含：数据卡片、图表、趋势分析")
        elif parsed['page_type'] == 'form':
            suggestions.append("建议包含：表单字段、验证、提交按钮")
        
        # 根据组件建议
        if '表格' in parsed['components']:
            suggestions.append("表格建议显示：名称、状态、时间、操作列")
        
        if '筛选' in parsed['components']:
            suggestions.append("筛选条件：关键词搜索、状态下拉、日期范围")
        
        # 根据业务领域建议
        if '产品' in parsed['keywords']:
            suggestions.append("产品相关字段：名称、价格、库存、状态")
        elif '用户' in parsed['keywords']:
            suggestions.append("用户相关字段：用户名、邮箱、手机号、注册时间")
        
        return suggestions


def parse_requirement_doc(file_path: str) -> Dict:
    """
    解析需求文档的便捷函数
    
    Args:
        file_path: 文件路径
    
    Returns:
        解析结果
    """
    parser = RequirementParser()
    result = parser.parse_file(file_path)
    
    # 生成建议
    result['suggestions'] = parser.generate_suggestions(result)
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 requirement_parser.py <需求文档路径>")
        print("支持格式：.md .txt .docx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        result = parse_requirement_doc(file_path)
        
        print("\n" + "=" * 60)
        print("📋 需求文档解析结果")
        print("=" * 60)
        print(f"📁 源文件：{result['source_file']}")
        print(f"📄 页面类型：{result['page_type']}")
        print(f"🔑 关键词：{', '.join(result['keywords'])}")
        print(f"🧩 组件：{', '.join(result['components'])}")
        print(f"⚙️  功能：{', '.join(result['features'])}")
        print(f"🎨 风格：{result['style_preference']}")
        
        if result['suggestions']:
            print("\n💡 建议:")
            for i, sug in enumerate(result['suggestions'], 1):
                print(f"  {i}. {sug}")
        
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 解析失败：{e}")
        sys.exit(1)
