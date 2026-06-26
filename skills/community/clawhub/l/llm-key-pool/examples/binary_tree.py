"""
二叉搜索树（Binary Search Tree）实现

支持操作：
- 插入节点
- 查找节点
- 删除节点
- 前序/中序/后序/层序遍历
- 获取最小/最大值
- 获取树的高度
- 检查是否为二叉搜索树
"""


class TreeNode:
    """二叉树节点"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.size = 1  # 以该节点为根的子树节点总数

    def update_size(self):
        """更新以该节点为根的子树大小"""
        self.size = 1
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size


class BinarySearchTree:
    """二叉搜索树实现"""

    def __init__(self):
        """初始化空二叉搜索树"""
        self.root = None

    def size(self) -> int:
        """返回树中节点总数"""
        if self.root is None:
            return 0
        return self.root.size

    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self.root is None

    def put(self, key, value) -> None:
        """插入或更新键值对"""
        self.root = self._put(self.root, key, value)

    def _put(self, node: TreeNode, key, value) -> TreeNode:
        """递归插入辅助函数"""
        if node is None:
            return TreeNode(key, value)

        if key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            # 键已存在，更新值
            node.value = value

        node.update_size()
        return node

    def get(self, key):
        """根据键查找值，键不存在返回None"""
        return self._get(self.root, key)

    def _get(self, node: TreeNode, key):
        """递归查找辅助函数"""
        if node is None:
            return None

        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        else:
            return node.value

    def contains(self, key) -> bool:
        """检查键是否存在"""
        return self.get(key) is not None

    def delete(self, key) -> bool:
        """删除键对应的节点，返回是否删除成功"""
        if not self.contains(key):
            return False
        self.root = self._delete(self.root, key)
        return True

    def _delete(self, node: TreeNode, key) -> TreeNode:
        """递归删除辅助函数"""
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # 找到要删除的节点
            # 情况1：没有子节点或只有一个子节点
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # 情况2：有两个子节点
            # 找到右子树中的最小节点替代当前节点
            successor = self._find_min(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete(node.right, successor.key)

        node.update_size()
        return node

    def _find_min(self, node: TreeNode) -> TreeNode:
        """找到以node为根的子树中的最小节点"""
        while node.left is not None:
            node = node.left
        return node

    def _find_max(self, node: TreeNode) -> TreeNode:
        """找到以node为根的子树中的最大节点"""
        while node.right is not None:
            node = node.right
        return node

    def min_key(self):
        """返回树中的最小键，树为空返回None"""
        if self.root is None:
            return None
        return self._find_min(self.root).key

    def max_key(self):
        """返回树中的最大键，树为空返回None"""
        if self.root is None:
            return None
        return self._find_max(self.root).key

    def height(self) -> int:
        """返回树的高度（空树返回0，只有根节点返回1）"""
        return self._height(self.root)

    def _height(self, node: TreeNode) -> int:
        """递归计算高度"""
        if node is None:
            return 0
        left_height = self._height(node.left)
        right_height = self._height(node.right)
        return 1 + max(left_height, right_height)

    # ========== 遍历方法 ==========

    def pre_order(self) -> list:
        """前序遍历（根-左-右）"""
        result = []
        self._pre_order(self.root, result)
        return result

    def _pre_order(self, node: TreeNode, result: list):
        if node is not None:
            result.append((node.key, node.value))
            self._pre_order(node.left, result)
            self._pre_order(node.right, result)
        return result

    def in_order(self) -> list:
        """中序遍历（左-根-右），二叉搜索树的中序遍历是有序的"""
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node: TreeNode, result: list):
        if node is not None:
            self._in_order(node.left, result)
            result.append((node.key, node.value))
            self._in_order(node.right, result)
        return result

    def post_order(self) -> list:
        """后序遍历（左-右-根）"""
        result = []
        self._post_order(self.root, result)
        return result

    def _post_order(self, node: TreeNode, result: list):
        if node is not None:
            self._post_order(node.left, result)
            self._post_order(node.right, result)
            result.append((node.key, node.value))
        return result

    def level_order(self) -> list:
        """层序遍历（广度优先）"""
        if self.root is None:
            return []

        result = []
        from collections import deque
        queue = deque()
        queue.append(self.root)

        while queue:
            node = queue.popleft()
            result.append((node.key, node.value))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def is_valid_bst(self) -> bool:
        """验证是否为合法的二叉搜索树"""
        return self._is_valid_bst(self.root, None, None)

    def _is_valid_bst(self, node: TreeNode, min_key, max_key) -> bool:
        if node is None:
            return True

        # 当前节点必须在(min_key, max_key)范围内
        if min_key is not None and node.key <= min_key:
            return False
        if max_key is not None and node.key >= max_key:
            return False

        # 递归验证左右子树
        return (self._is_valid_bst(node.left, min_key, node.key) and
                self._is_valid_bst(node.right, node.key, max_key))

    def __contains__(self, key):
        """支持 'in' 运算符"""
        return self.contains(key)

    def __len__(self):
        """支持 len() 函数"""
        return self.size()

    def print_structure(self) -> None:
        """以树形结构打印（用于调试）"""
        if self.root is None:
            print("Empty tree")
            return

        lines = self._get_tree_lines(self.root)
        for line in lines:
            print(line)

    def _get_tree_lines(self, node: TreeNode) -> list:
        """生成树形结构字符串（用于打印）"""
        if node.right is None and node.left is None:
            return [f"{node.key}"]

        if node.right is None:
            left_lines = self._get_tree_lines(node.left)
            result = [f"{node.key}"]
            result.append("└── " + left_lines[0])
            prefix = "    "
            for line in left_lines[1:]:
                result.append(prefix + line)
            return result

        if node.left is None:
            right_lines = self._get_tree_lines(node.right)
            result = [f"{node.key}"]
            result.append("├── " + right_lines[0])
            prefix = "    "
            for line in right_lines[1:]:
                result.append(prefix + line)
            return result

        left_lines = self._get_tree_lines(node.left)
        right_lines = self._get_tree_lines(node.right)
        result = [f"{node.key}"]
        result.append("├── " + right_lines[0])
        prefix_right = "│   "
        for line in right_lines[1:]:
            result.append(prefix_right + line)
        result.append("└── " + left_lines[0])
        prefix_left = "    "
        for line in left_lines[1:]:
            result.append(prefix_left + line)
        return result


if __name__ == "__main__":
    # 使用示例
    bst = BinarySearchTree()

    # 插入测试数据
    print("=== 插入测试数据 ===")
    data = [(50, "fifty"), (30, "thirty"), (70, "seventy"),
            (20, "twenty"), (40, "forty"), (60, "sixty"), (80, "eighty")]

    for key, value in data:
        bst.put(key, value)
        print(f"Inserted: {key} => {value}")

    print(f"\n树大小: {len(bst)}")
    print(f"树高度: {bst.height()}")
    print(f"Is valid BST: {bst.is_valid_bst()}")

    # 打印树形结构
    print("\n=== 树形结构 ===")
    bst.print_structure()

    # 查找测试
    print("\n=== 查找测试 ===")
    for key in [30, 50, 90]:
        value = bst.get(key)
        print(f"Get {key}: {value}")

    # 最小最大键
    print("\n=== 最小/最大键 ===")
    print(f"Min key: {bst.min_key()}")
    print(f"Max key: {bst.max_key()}")

    # 遍历测试
    print("\n=== 遍历测试 ===")
    print(f"Pre-order:  {bst.pre_order()}")
    print(f"In-order:   {bst.in_order()}  (should be sorted)")
    print(f"Post-order: {bst.post_order()}")
    print(f"Level-order:{bst.level_order()}")

    # 删除测试 - 删除叶子节点
    print("\n=== 删除叶子节点 (20) ===")
    print(f"Delete 20: {bst.delete(20)}")
    print(f"Tree size: {len(bst)}")
    print("In-order:", bst.in_order())
    bst.print_structure()

    # 删除测试 - 删除有一个子节点的节点
    print("\n=== 删除有一个子节点的节点 (30) ===")
    print(f"Delete 30: {bst.delete(30)}")
    print(f"Tree size: {len(bst)}")
    print("In-order:", bst.in_order())
    bst.print_structure()

    # 删除测试 - 删除有两个子节点的节点（根节点）
    print("\n=== 删除根节点 (50) ===")
    print(f"Delete 50: {bst.delete(50)}")
    print(f"Tree size: {len(bst)}")
    print(f"Is valid BST: {bst.is_valid_bst()}")
    print("In-order:", bst.in_order())
    bst.print_structure()

    # 包含测试
    print("\n=== 包含测试 ===")
    print(f"50 in bst: {50 in bst}")
    print(f"60 in bst: {60 in bst}")
