#!/usr/bin/env python3
"""
明析分析框架引擎 — 一键启动结构化分析
"""
import sys, os, json
from datetime import datetime, timedelta

MODES = {
    "ocgs": "OCGS六维系统诊断",
    "contradiction": "矛盾分析（三态+性质+临界条件）",
    "five-layer": "五层推演法",
    "policy": "政策信号解读法",
    "six-prism": "灵感六棱镜内容评估",
    "credibility": "信度等级标注",
    "full": "全流程分析（第0步→1→2→3→4→5→6）",
}

def show_help():
    print("明析分析框架引擎")
    print(f"\n用法: python3 {sys.argv[0]} --mode <模式> --target <分析对象>")
    print("\n模式:")
    for k, v in MODES.items():
        print(f"  {k:15s} {v}")
    print("\n示例:")
    print(f"  python3 {sys.argv[0]} --mode ocgs --target \"华为鸿蒙生态\"")
    print(f"  python3 {sys.argv[0]} --mode contradiction --problem \"多Agent协作效率低\"")
    print("\n可选参数:")
    print("  --output <file>  输出到文件")
    print("  --register       自动登记判断回查")
    sys.exit(0)

def main():
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 3:
        show_help()
    
    mode = None
    target = None
    problem = None
    output_file = None
    
    for i, arg in enumerate(sys.argv):
        if arg == "--mode" and i+1 < len(sys.argv):
            mode = sys.argv[i+1]
        elif arg == "--target" and i+1 < len(sys.argv):
            target = sys.argv[i+1]
        elif arg == "--problem" and i+1 < len(sys.argv):
            problem = sys.argv[i+1]
        elif arg == "--output" and i+1 < len(sys.argv):
            output_file = sys.argv[i+1]
    
    if mode not in MODES:
        print(f"❌ 未知模式: {mode}")
        show_help()
    
    print(f"🔍 分析模式: {MODES[mode]}")
    print(f"📌 分析对象: {target or problem or '(未指定)'}")
    print()
    
    # 生成分析模板
    now = datetime.now()
    check_date = (now + timedelta(days=7)).strftime("%Y-%m-%d")
    
    output = f"# {MODES[mode]} — {target or problem or '未知对象'}\n"
    output += f"\n**分析时间**: {now.strftime('%Y-%m-%d %H:%M')}"
    output += f"\n**回查日期**: {check_date}\n\n"
    
    if mode == "ocgs":
        output += """## OCGS六维诊断

| 维度 | 评估 | 关键发现 | 证据 |
|:----|:----|:---------|:-----|
| **开放度** | 🟡 | （信息通道评估） | |
| **多样性** | 🟢 | （备选方案评估） | |
| **耦合度** | 🔴 | （依赖关系评估） | |
| **冗余度** | 🟡 | （容错能力评估） | |
| **自适应** | 🔴 | （自我调整能力） | |
| **响应速度** | 🟡 | （变化速度对比） | |

### 综合判断
- **最强维度**：
- **最弱维度**：
- **风险排序**（最需优先处理）：

### 核心判断
TBD

### 失效条件
TBD
"""
    elif mode == "contradiction":
        output += """## 矛盾分析

### 矛盾性质判定
- 性质：对抗性 / 非对抗性 / 结构张力
- 判定依据：

### 主要矛盾

### 矛盾的主要方面

### 三态分析
- 当前状态：固化态(+1) / 待定态(0) / 爆发态(-1)
- 临界条件（待定→爆发的触发条件）：

### 是否已转化
- 转化状态：未转化 / 已转化
- 转化方向：

### 矛盾特殊性
- 这个问题与同类问题不同的关键点：

### 核心判断
TBD
"""
    elif mode == "five-layer":
        output += """## 五层推演

### L1 信息层
（谁做了什么？）

### L2 意图层
（他为什么这么做？说的 vs 做的）

### L3 对手模型层
- 视角1（对手A看我们）：
- 视角2（对手B看我们）：

### L4 博弈约束层
（什么不可能变？硬资源/时间/政策约束）

### L4.5 趋势层（可选）
（可能的演化路径和概率分布）

### L5 棋盘尺度层
（这盘棋在更大的局里是什么位���？）

### 核心判断
TBD

### 失效条件
TBD
"""
    elif mode == "full":
        output += """## 全流程分析

### 第0步：安全闸
- 外部硬约束：
- 框架适用度：
- 第三方因素：

### 第1步：事实收集
（主要事实，标注信度）

### 第2步：框架选择
（选用1-2个框架，说明理由）

### 第3步：矛盾定位
（主要矛盾？主要方面？转化？）

### 第4步：输出

**核心判断**：

**否定了**：

**不变量**：

### 第5步：失效条件
### 第6步：复盘
"""
    output += f"\n---\n*由明析分析框架引擎生成 | 回查日期: {check_date}*\n"
    
    if output_file:
        with open(output_file, "w") as f:
            f.write(output)
        print(f"✅ 分析模板已写入 {output_file}")
    else:
        print(output)

if __name__ == "__main__":
    main()
