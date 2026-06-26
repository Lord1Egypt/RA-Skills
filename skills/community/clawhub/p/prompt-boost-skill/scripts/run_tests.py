#!/usr/bin/env python3
"""批量运行 prompt-boost-skill 测试用例"""
import json, sys, re

SKILL_MD = "/workspace/skills/prompt-boost-skill/SKILL.md"
TEST_JSON = "/workspace/skills/prompt-boost-skill/test_cases.json"
OUT_TXT   = "/workspace/skills/prompt-boost-skill/test_results.txt"

def load_tests():
    with open(TEST_JSON) as f:
        return json.load(f)

def build_prompt(test_cases, skill_md):
    lines = [
        "你是一个严格遵循 SKILL.md 规则的嘴替技能引擎。",
        "## SKILL.md 全文\n" + skill_md.strip(),
        "",
        "## 测试用例（JSON）：",
        json.dumps(test_cases, ensure_ascii=False, indent=2),
        "",
        "## 要求",
        "对每个测试用例，严格按 SKILL.md 中的【输出格式】输出结果。",
        "判断放行还是追问（基于5槽位标准）：",
        "  - 追问：缺任务目标 OR 缺受众 OR 缺输出形式 OR 缺关键约束",
        "  - 放行：至少4个槽位明确",
        "输出格式：",
        "```",
        "## Case N: <原始输入>",
        "【判断】追问 / 放行",
        "【理解确认】...",
        "【澄清问题】1. ... 2. ... 3. ...   （如为追问）",
        "【输出类型】Need Clarification / Approved",
        "---",
        "```",
        "请逐条输出，不要省略任何 Case。",
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    tests = load_tests()
    with open(SKILL_MD) as f:
        skill_md = f.read()
    prompt = build_prompt(tests, skill_md)
    with open("/tmp/pboost_test_prompt.txt", "w") as f:
        f.write(prompt)
    print(f"已生成测试提示词，共 {len(tests)} 个用例，写入 /tmp/pboost_test_prompt.txt")
