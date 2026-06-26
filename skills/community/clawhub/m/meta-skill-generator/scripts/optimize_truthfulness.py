"""
优化 truthfulness 技能
"""
import sys
from pathlib import Path

# 获取项目根目录
SCRIPT_DIR = Path(__file__).parent
SKILLS_ROOT = SCRIPT_DIR.parent / "skills"

sys.path.append(str(SCRIPT_DIR))

from optimizer import auto_optimize, suggest_improvements, get_best_optimization

# 读取 truthfulness SKILL.md
truthfulness_path = SKILLS_ROOT / "truthfulness" / "SKILL.md"
content = truthfulness_path.read_text(encoding="utf-8")

print("=== 当前 truthfulness 评分: 0.65 ===\n")

# 分析问题
print("1. 分析问题...")
suggestions = suggest_improvements(content)
print(f"   发现 {len(suggestions)} 个改进建议:")
for s in suggestions:
    print(f"   - [{s['priority']}] {s['suggestion']}")

# 自动优化
print("\n2. 自动优化...")
result = auto_optimize("truthfulness", content, score=0.65)

# 获取最佳版本
best_code = get_best_optimization(result)
print(f"   优化后代码行数: {len(best_code.split(chr(10)))}")

# 保存优化结果
GENERATED_DIR = SKILLS_ROOT / "meta-skill-generator" / "generated"
output_path = GENERATED_DIR / "truthfulness_optimized.md"
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(best_code, encoding="utf-8")

print(f"\n[OK] Optimized saved to: {output_path}")
