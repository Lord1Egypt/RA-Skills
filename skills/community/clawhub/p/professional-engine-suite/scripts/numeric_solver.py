#!/usr/bin/env python3
"""数值通道兜底：常微分方程组 RK4 求解（供无解析解问题使用，如双摆、三体简化模型）。
用法: 修改本文件底部的 f(t, y) 与初值/步长，然后 python numeric_solver.py
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 末态与误差控制信息（步长减半对照）。
"""
import sys

def rk4(f, t0, y0, h, n):
    t, y = t0, list(y0)
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, [y[i] + h / 2 * k1[i] for i in range(len(y))])
        k3 = f(t + h / 2, [y[i] + h / 2 * k2[i] for i in range(len(y))])
        k4 = f(t + h, [y[i] + h * k3[i] for i in range(len(y))])
        y = [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]
        t += h
    return t, y

def solve_with_error(f, t0, y0, h, n):
    t1, y1 = rk4(f, t0, y0, h, n)
    t2, y2 = rk4(f, t0, y0, h / 2, n * 2)
    err = max(abs(a - b) for a, b in zip(y1, y2))
    return t2, y2, err

def demo():
    # 示例：指数衰减 y' = -y, y(0)=1（解析解 e^-t，用于验证求解器）
    f = lambda t, y: [-y[0]]
    t, y, err = solve_with_error(f, 0.0, [1.0], 0.05, 40)
    import math
    exact = math.exp(-t)
    print(f"t={t:.2f}  数值解={y[0]:.8f}  解析解={exact:.8f}  步长减半误差估计={err:.2e}")
    print("误差来源: RK4 截断误差 O(h^4)；控制参数: 步长 h=0.05（对照 h/2）")

if __name__ == "__main__":
    if "--demo" in sys.argv or len(sys.argv) == 1:
        demo()
