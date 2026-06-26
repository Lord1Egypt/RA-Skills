"""simple web-service-like module."""


def compute(n):
    # naive: 每次重新计算平方和
    return sum(i * i for i in range(n))
