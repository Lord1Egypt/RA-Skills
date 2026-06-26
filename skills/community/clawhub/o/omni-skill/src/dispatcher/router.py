"""
哈希与前缀树路由模块 (Router Module)
用于精准匹配技能触发路径。
"""

class RadixNode:
    """前缀树节点"""
    def __init__(self):
        self.children = {}  # 子节点
        self.is_end = False # 是否为路径终点
        self.skill_id = None # 绑定的技能标识

class RadixRouter:
    """前缀树路由器"""
    def __init__(self):
        self.root = RadixNode()

    def add_route(self, path: str, skill_id: str):
        """添加路由"""
        node = self.root
        for char in path:
            if char not in node.children:
                node.children[char] = RadixNode()
            node = node.children[char]
        node.is_end = True
        node.skill_id = skill_id

    def match(self, path: str) -> str:
        """匹配路由"""
        node = self.root
        for char in path:
            if char not in node.children:
                return None
            node = node.children[char]
        if node.is_end:
            return node.skill_id
        return None

class HashRouter:
    """哈希路由器"""
    def __init__(self):
        self.routes = {} # 路由映射

    def add_route(self, trigger_key: str, skill_id: str):
        """精确匹配注册"""
        self.routes[trigger_key] = skill_id

    def match(self, trigger_key: str) -> str:
        """精确匹配触发"""
        return self.routes.get(trigger_key)