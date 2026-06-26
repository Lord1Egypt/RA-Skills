#!/usr/bin/env python3
# Priority Evaluator

def evaluate(tech, market, competition, revenue):
    scores = [tech, market, competition, revenue]
    avg = sum(scores) / 4
    recommendation = "✅ 推荐" if avg >= 4.0 else ("🟡 谨慎" if avg >= 3.0 else "❌ 放弃")
    return avg, recommendation

if __name__ == '__main__':
    score, rec = evaluate(4, 5, 4, 5)
    print(f"综合评分：{score}/5 - {rec}")
