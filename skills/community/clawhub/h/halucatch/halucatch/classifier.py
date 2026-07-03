"""HaluCatch 分类器：根据文件内容判定 Skill 类型。"""

from .config import MESSAGES


def classify_skill(info):
    """判断 Skill 类型：代码工程型 / 纯方法论型。"""
    has_py = info['py'] is not None
    has_data = info['has_data']
    has_pd = info['skill_md'] and ('pd.read_' in info['skill_md'] or 'pandas' in info['skill_md'].lower())
    has_md_py = info['skill_md'] and ('```python' in info['skill_md'])

    if has_py or has_data or has_pd or has_md_py:
        return 'code-engineered'
    return 'methodology'


# =============================================================================
# 3. 评估函数
# =============================================================================
