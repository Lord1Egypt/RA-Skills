"""
哈希表（Hash Table）实现
使用链地址法（Separate Chaining）解决哈希冲突

支持操作：
- 插入键值对
- 根据键获取值
- 删除键值对
- 检查键是否存在
- 获取哈希表大小
"""


class HashNode:
    """哈希表节点"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """哈希表实现"""

    def __init__(self, capacity: int = 16):
        """
        初始化哈希表
        :param capacity: 初始容量，默认为16
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key) -> int:
        """
        哈希函数，将键映射到桶索引
        使用多项式滚动哈希方法
        """
        if isinstance(key, int):
            # 整数直接取模
            return key % self.capacity
        elif isinstance(key, str):
            # 字符串使用多项式哈希
            hash_val = 0
            p = 31  # 基数
            m = self.capacity  # 模
            for i, char in enumerate(key):
                hash_val = (hash_val * p + ord(char)) % m
            return hash_val
        else:
            # 其他类型使用内置hash函数
            return hash(key) % self.capacity

    def put(self, key, value) -> None:
        """插入或更新键值对"""
        index = self._hash(key)
        current = self.buckets[index]

        # 检查键是否已存在，如果存在则更新
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # 不存在则插入新节点（头插法）
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        # 当负载因子超过0.7时扩容
        if self.size / self.capacity > 0.7:
            self._resize()

    def get(self, key, default=None):
        """根据键获取值，如果键不存在返回default"""
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return default

    def remove(self, key) -> bool:
        """删除键值对，返回是否删除成功"""
        index = self._hash(key)
        current = self.buckets[index]
        prev = None

        while current is not None:
            if current.key == key:
                if prev is None:
                    # 删除头节点
                    self.buckets[index] = current.next
                else:
                    # 删除中间或尾节点
                    prev.next = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next

        return False

    def contains(self, key) -> bool:
        """检查键是否存在"""
        return self.get(key) is not None

    def __len__(self) -> int:
        """返回哈希表大小"""
        return self.size

    def __contains__(self, key):
        """支持 'in' 运算符"""
        return self.contains(key)

    def _resize(self) -> None:
        """扩容为原来的2倍"""
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        # 重新哈希所有元素
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = new_buckets
        self.size = 0

        for bucket in old_buckets:
            current = bucket
            while current is not None:
                self.put(current.key, current.value)
                current = current.next

    def keys(self):
        """返回所有键"""
        all_keys = []
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                all_keys.append(current.key)
                current = current.next
        return all_keys

    def values(self):
        """返回所有值"""
        all_values = []
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                all_values.append(current.value)
                current = current.next
        return all_values

    def items(self):
        """返回所有键值对"""
        all_items = []
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                all_items.append((current.key, current.value))
                current = current.next
        return all_items

    def print_stats(self) -> None:
        """打印哈希表统计信息（用于调试）"""
        print(f"Capacity: {self.capacity}, Size: {self.size}")
        print(f"Load factor: {self.size / self.capacity:.2f}")
        max_chain = 0
        empty_buckets = 0
        for i, bucket in enumerate(self.buckets):
            if bucket is None:
                empty_buckets += 1
                continue
            length = 0
            current = bucket
            while current is not None:
                length += 1
                current = current.next
            max_chain = max(max_chain, length)
            print(f"  Bucket {i}: chain length = {length}")
        print(f"Empty buckets: {empty_buckets}, Max chain length: {max_chain}")


if __name__ == "__main__":
    # 使用示例
    ht = HashTable(capacity=8)

    # 插入一些数据
    print("=== 插入测试数据 ===")
    data = [
        ("apple", 100),
        ("banana", 200),
        ("cherry", 300),
        ("date", 400),
        ("elderberry", 500),
        (123, "one two three"),
        (456, "four five six"),
    ]

    for key, value in data:
        ht.put(key, value)
        print(f"Inserted: {key} => {value}")

    print(f"\n哈希表大小: {len(ht)}")

    # 查询测试
    print("\n=== 查询测试 ===")
    for key in ["apple", "banana", "not_exists", 123, 999]:
        value = ht.get(key)
        print(f"Get {key}: {value}")

    # 包含测试
    print("\n=== 包含测试 ===")
    print(f"'apple' in ht: {'apple' in ht}")
    print(f"'orange' in ht: {'orange' in ht}")

    # 更新测试
    print("\n=== 更新测试 ===")
    print(f"Original apple: {ht.get('apple')}")
    ht.put("apple", 999)
    print(f"Updated apple: {ht.get('apple')}")

    # 删除测试
    print("\n=== 删除测试 ===")
    print(f"Delete 'banana': {ht.remove('banana')}")
    print(f"Delete 'not_exists': {ht.remove('not_exists')}")
    print(f"Get 'banana' after delete: {ht.get('banana')}")
    print(f"Size after delete: {len(ht)}")

    # 遍历所有元素
    print("\n=== 遍历所有元素 ===")
    print(f"Keys: {ht.keys()}")
    print(f"Values: {ht.values()}")
    print(f"Items: {ht.items()}")

    # 统计信息
    print("\n=== 统计信息 ===")
    ht.print_stats()
