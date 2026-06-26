"""
哈希表和二叉树使用示例演示

这个文件展示了如何使用 hash_table.py 和 binary_tree.py 中的数据结构
"""

from hash_table import HashTable
from binary_tree import BinarySearchTree


def demo_hash_table():
    print("=" * 50)
    print("哈希表 (Hash Table) 演示")
    print("=" * 50)

    # 创建哈希表
    ht = HashTable(capacity=8)

    # 添加学生成绩
    students = {
        "Alice": 95,
        "Bob": 82,
        "Charlie": 78,
        "David": 90,
        "Eve": 88
    }

    for name, score in students.items():
        ht.put(name, score)

    print(f"1. 添加了 {len(ht)} 个学生成绩")
    print(f"   所有学生: {ht.keys()}")

    # 查询
    print(f"\n2. 查询成绩:")
    for name in ["Alice", "Bob", "Frank"]:
        score = ht.get(name, "未找到")
        print(f"   {name}: {score}")

    # 更新
    print(f"\n3. 更新 Bob 的成绩: {ht.get('Bob')} -> 85")
    ht.put("Bob", 85)
    print(f"   Bob 的新成绩: {ht.get('Bob')}")

    # 删除
    print(f"\n4. 删除 Charlie")
    ht.remove("Charlie")
    print(f"   Charlie 在哈希表中吗? {'Charlie' in ht}")
    print(f"   当前大小: {len(ht)}")

    # 遍历所有键值对
    print(f"\n5. 遍历所有成绩:")
    for name, score in ht.items():
        print(f"   {name}: {score}")

    # 统计信息
    print(f"\n6. 哈希表统计:")
    ht.print_stats()

    print()


def demo_binary_search_tree():
    print("=" * 50)
    print("二叉搜索树 (Binary Search Tree) 演示")
    print("=" * 50)

    # 创建二叉搜索树
    bst = BinarySearchTree()

    # 插入商品价格
    products = {
        150: "Apple",
        80: "Banana",
        200: "Cherry",
        50: "Date",
        100: "Elderberry",
        180: "Fig",
        250: "Grape"
    }

    for price, name in products.items():
        bst.put(price, name)

    print(f"1. 插入了 {len(bst)} 个商品")
    print(f"   树高度: {bst.height()}")
    print(f"   是否为合法BST: {bst.is_valid_bst()}")

    # 树形结构
    print("\n2. 树形结构:")
    bst.print_structure()

    # 查找
    print("\n3. 查找商品:")
    for price in [100, 200, 300]:
        name = bst.get(price)
        if name:
            print(f"   价格 {price}: {name}")
        else:
            print(f"   价格 {price}: 未找到")

    # 最值
    print(f"\n4. 价格范围:")
    print(f"   最低价格: {bst.min_key()}")
    print(f"   最高价格: {bst.max_key()}")

    # 不同遍历方式
    print(f"\n5. 各种遍历结果 (价格, 商品名):")
    print(f"   前序遍历: {bst.pre_order()}")
    print(f"   中序遍历: {bst.in_order()}  (价格递增)")
    print(f"   后序遍历: {bst.post_order()}")
    print(f"   层序遍历: {bst.level_order()}")

    # 删除操作
    print("\n6. 删除价格 150 (根节点):")
    bst.delete(150)
    print(f"   当前节点数: {len(bst)}")
    print(f"   是否仍然是合法BST: {bst.is_valid_bst()}")
    print("\n   删除后的树结构:")
    bst.print_structure()

    print()


if __name__ == "__main__":
    demo_hash_table()
    demo_binary_search_tree()

    print("演示完成！")
    print("\n文件位置:")
    print("- 哈希表实现: examples/hash_table.py")
    print("- 二叉搜索树实现: examples/binary_tree.py")
    print("- 演示代码: examples/demo.py")
