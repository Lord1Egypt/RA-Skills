def add(a, b):
    return a + b


def concat(parts, sep=","):
    return sep.join(parts)


def average(nums):
    if not nums:
        return 0.0
    return sum(nums) / len(nums)
