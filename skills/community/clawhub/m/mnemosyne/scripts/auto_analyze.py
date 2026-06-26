#!/usr/bin/env python3
"""
auto_analyze.py - AI 自动分析触发脚本 v2.0
增强版：更懂 boss、更多触发场景、情感检测、偏好追踪
"""
import sys
import json
import os
import re
import time
from datetime import datetime

def load_config(config_manager_path):
    cfg_file = os.path.join(os.path.dirname(config_manager_path), '../config/user_config.json')
    if os.path.exists(cfg_file):
        with open(cfg_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"auto_trigger": True, "tier_rules": {}, "emotion_detection": True}

def get_tier(mtype, config):
    rules = config.get("tier_rules", {})
    return rules.get(mtype, rules.get("default", "current"))

def analyze(conversation, index_file, config_manager_path):
    """
    增强版分析：更多触发场景，更懂 boss
    """
    config = load_config(config_manager_path)
    results = []
    conversation = conversation.strip()

    if not conversation or len(conversation) < 3:
        return results

    text_lower = conversation.lower()
    text_lines = conversation.strip().split('\n')

    # ========== 场景1：明确指令 ==========
    for p in [r'记住[：:](.+)', r'记一下[：:](.+)', r'帮我记[一下]?[：:](.+)', r'这个要记住[：:](.+)']:
        m = re.search(p, conversation)
        if m:
            results.append({"type": "auto_detect", "importance": 10, "content": m.group(1).strip(), "action": "add"})
            break

    # ========== 场景2：boss 决策 ==========
    decision_triggers = [
        (r'(?:就|就按|就定|就选)(?:这个|它|这样)(?:了|吧)', 'boss_direct_decision'),
        (r'决定了[：:]?(.*)', 'boss_decision'),
        (r'已经把(.+?)定下来了', 'boss_decision'),
        (r'(.+)已[经]?(?:决定|确定|敲定)', 'boss_decision'),
        (r'最后选了(.+)', 'boss_decision'),
        (r'目标[是为](.*)', 'boss_decision'),
    ]
    for pattern, mtype in decision_triggers:
        for m in re.finditer(pattern, text_lower):
            content = m.group(1).strip() if m.lastindex else conversation.strip()
            if len(content) > 2 and len(content) < 200:
                results.append({"type": mtype, "importance": 9, "content": content, "action": "add"})
                break

    # ========== 场景3：boss 偏好（喜欢/讨厌）============
    likes = re.findall(r'(?:喜欢|爱|偏好|偏向|更?喜欢|中意)([^。，,\n]{1,100})', conversation)
    dislikes = re.findall(r'(?:不喜欢|讨厌|厌恶|排斥|不想|不要)([^。，,\n]{1,100})', conversation)
    for l in likes:
        l = l.strip()
        if len(l) > 1 and len(l) < 100:
            results.append({"type": "boss_preference", "importance": 8, "content": f"boss 喜欢：{l}", "action": "add"})
    for d in dislikes:
        d = d.strip()
        if len(d) > 1 and len(d) < 100:
            results.append({"type": "boss_preference", "importance": 8, "content": f"boss 不喜欢：{d}", "action": "add"})

    # ========== 场景4：偏好变化（重要！更懂 boss 的关键）===========
    # 之前A，现在B → 重要变化，要记
    change_patterns = [
        r'之前(?:喜欢|觉得|认为)(.+?)，现在(.+?)[。\n]',
        r'原来(.+?)，(?:但|不过|可是|现在)(.+)',
        r'不过(?:现在|其实)(.+?)更?(.+)',
        r'(.+?)其实(?:更|比较|比较)(.+)',
    ]
    for p in change_patterns:
        for m in re.finditer(p, conversation):
            if m.lastindex and m.lastindex >= 2:
                old = m.group(1).strip()
                new = m.group(2).strip()
                if len(old) > 1 and len(new) > 1:
                    results.append({
                        "type": "boss_preference_change",
                        "importance": 9,
                        "content": f"boss 偏好变化：之前「{old}」→ 现在「{new}」",
                        "action": "add"
                    })

    # ========== 场景5：boss 信息 ==========
    info_patterns = [
        (r'我叫(.+)', 'boss_name'),
        (r'我是(.+?公司|.+?医院|.+?厂|.+?银行)', 'boss_company'),
        (r'我是(.+?的)(?:老板|总)', 'boss_role'),
        (r'我的(.+?)[是](.+)', 'boss_property'),
        (r'我(?:们公司|公司)(?:叫|名)(.+)', 'boss_company_name'),
    ]
    for p, mtype in info_patterns:
        m = re.search(p, conversation)
        if m:
            content = m.group(0).strip()
            if len(content) > 3:
                results.append({"type": "boss_info", "importance": 9, "content": content, "action": "add"})

    # ========== 场景6：数字/日期/金额（重要上下文）===========
    number_patterns = [
        (r'\d+[人个只台件条]', '数量', 6),
        (r'\d+万[元块]?', '金额', 7),
        (r'\d+亿[元块]?', '金额', 8),
        (r'((?:下|上|这)个?(?:周|月|年|天))', '时间', 6),
        (r'(\d{4}年\d{1,2}月\d{0,2}[日号]?)', '日期', 7),
        (r'(?:报价|价格|市值|估值)[是为]?(\d+)', '估值', 8),
    ]
    for p, label, imp in number_patterns:
        for m in re.finditer(p, text_lower):
            content = f"[{label}]{m.group(0).strip()}"
            if len(m.group(0)) > 2:
                results.append({"type": "work_context", "importance": imp, "content": content, "action": "add"})

    # ========== 场景7：任务完成 ==========
    completion = re.findall(r'(?:完成了?|搞定了?|做好了?|已经|搞完)(.+)', conversation)
    for c in completion:
        c = c.strip()
        if len(c) > 2 and len(c) < 100:
            results.append({"type": "work_context", "importance": 7, "content": f"已完成：{c}", "action": "add"})

    # ========== 场景8：学到/发现 ==========
    learning = re.findall(r'(?:学到?|学会|发现?|原来|才知)[道了](.+)', conversation)
    for l in learning:
        l = l.strip()
        if len(l) > 2 and len(l) < 150:
            results.append({"type": "learning", "importance": 8, "content": l, "action": "add"})

    # ========== 场景9：boss 情绪/状态（"更懂 boss" 关键）==========
    emotion_patterns = [
        (r'(?:今天|最近|这几天)(?:感觉|觉得|心情)([^。，\n]{1,50})', 'boss_emotion'),
        (r'(?:开心|高兴|满意|兴奋|激动)([^。，\n]{0,50})', 'boss_positive'),
        (r'(?:不爽|郁闷|烦躁|焦虑|担心|压力)([^。，\n]{0,50})', 'boss_negative'),
        (r'(?:累|疲惫|困|疲倦)([^。，\n]{0,50})', 'boss_negative'),
        (r'太难了|搞不定|没办法|无解', 'boss_frustration'),
    ]
    for p, mtype in emotion_patterns:
        for m in re.finditer(p, text_lower):
            content = m.group(0).strip()
            imp = 6 if mtype == 'boss_emotion' else 5
            results.append({"type": mtype, "importance": imp, "content": f"boss 情绪：{content}", "action": "add"})

    # ========== 场景10：对某事的评价/看法（理解 boss 的判断标准）==========
    eval_patterns = [
        (r'觉得(.+?)(?:不行|不好|有问题|不行)', 'boss_evaluation'),
        (r'(?:还行|可以|不错|很好|棒)(.+)', 'boss_positive_eval'),
        (r'太(.+?)(?:了吧|了呗|了呀)', 'boss_comment'),
    ]
    for p, mtype in eval_patterns:
        for m in re.finditer(p, text_lower):
            content = m.group(0).strip()
            if len(content) > 3:
                results.append({"type": mtype, "importance": 7, "content": f"boss 评价：{content}", "action": "add"})

    # ========== 场景11：重复提到的词（暗示重要）==========
    words = re.findall(r'[\u4e00-\u9fff]{2,}', conversation)
    word_count = {}
    for w in words:
        if len(w) > 2:
            word_count[w] = word_count.get(w, 0) + 1
    for word, count in word_count.items():
        if count >= 3 and len(word) > 2:
            results.append({
                "type": "insight",
                "importance": 6,
                "content": f"boss 反复提到「{word}」（出现{count}次），可能是当前关注重点",
                "action": "add"
            })

    # ========== 场景12：冲突检测（旧记忆 vs 新内容）=========
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)

        for existing in index.get('memories', [])[-30:]:
            old = existing.get('content', '')
            old_type = existing.get('type', '')
            # 检测新内容是否和旧记忆矛盾
            for result in results:
                new = result.get('content', '')
                if old_type == result.get('type') and old and new:
                    # 内容相似但不完全相同 → 可能是变化
                    if any(w in new for w in old.split() if len(w) > 3) and old != new:
                        result['action'] = 'conflict'
                        result['old_memory'] = old
                        print(f"[CONFLICT] 旧: {old[:40]}... 新: {new[:40]}...")

    # ========== 去重 ==========
    seen = set()
    unique = []
    for r in results:
        key = (r.get('type'), r.get('content', ''))
        if key not in seen and len(r.get('content', '')) > 2:
            seen.add(key)
            unique.append(r)

    return unique

def main():
    if len(sys.argv) < 3:
        print("Usage: auto_analyze.py <conversation> <index_file> <config_manager_path>")
        sys.exit(1)

    conversation = sys.argv[1]
    index_file = sys.argv[2]
    config_manager_path = sys.argv[3]

    results = analyze(conversation, index_file, config_manager_path)

    if not results:
        print("[AUTO_ANALYZE] 未检测到需要记忆的内容")
        return

    print(f"[AUTO_ANALYZE] 检测到 {len(results)} 条可记忆内容：")
    config = load_config(config_manager_path)

    for r in results:
        tier = get_tier(r.get('type', 'default'), config)
        action = r.get('action', 'add')
        symbol = "⚠️" if action == 'conflict' else "✅"

        print(f"\n{symbol} [{action.upper()}] [{r['type']}] [{r['importance']}⭐] [Tier:{tier}]")
        print(f"   内容: {r['content'][:100]}{'...' if len(r['content'])>100 else ''}")

        if r.get('old_memory'):
            print(f"   ⚠️ 冲突旧记忆: {r['old_memory'][:50]}...")

    print(f"\n[JSON_OUTPUT]")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
