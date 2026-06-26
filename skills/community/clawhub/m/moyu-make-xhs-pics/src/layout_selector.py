"""
布局选择器
"""

from .types import Article, LAYOUTS


class LayoutSelector:
    """布局选择器"""
    
    VALID_LAYOUTS = list(LAYOUTS.keys())
    
    # 关键词映射
    COMPARISON_KEYWORDS = ['对比', '比较', '差异', '优缺点', '好坏', 'vs', 'versus', '不同', '区别']
    FLOW_KEYWORDS = ['首先', '然后', '接着', '最后', '步骤', '流程', '阶段', '原因', '结果', '导致', '为了']
    LIST_KEYWORDS = ['1.', '2.', '3.', '第一', '第二', '第三', '第四', '要点', '包括', '以下', '有以下几个方面']
    
    @staticmethod
    def auto_select(article: Article) -> str:
        """
        根据文章内容自动选择布局
        
        Args:
            article: 文章对象
            
        Returns:
            布局类型
        """
        # 合并所有内容进行判断
        all_content = ""
        for section in article["sections"]:
            all_content += section["title"] + section["content"]
        
        # 检查对比类
        if any(kw in all_content for kw in LayoutSelector.COMPARISON_KEYWORDS):
            return "comparison"
        
        # 检查流程/步骤类
        if any(kw in all_content for kw in LayoutSelector.FLOW_KEYWORDS):
            return "flow"
        
        # 检查列表类
        if any(kw in all_content for kw in LayoutSelector.LIST_KEYWORDS):
            return "list"
        
        # 默认
        return "balanced"
    
    @staticmethod
    def is_valid_layout(layout: str) -> bool:
        """
        验证布局是否有效
        
        Args:
            layout: 布局类型
            
        Returns:
            是否有效
        """
        return layout in LayoutSelector.VALID_LAYOUTS or layout == "auto"
    
    @staticmethod
    def resolve_layout(layout: str, article: Article) -> str:
        """
        解析布局（如果是 auto，则自动选择）
        
        Args:
            layout: 布局类型
            article: 文章对象
            
        Returns:
            解析后的布局类型
        """
        if layout == "auto":
            return LayoutSelector.auto_select(article)
        return layout
