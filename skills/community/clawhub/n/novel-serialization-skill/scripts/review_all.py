# -*- coding: utf-8 -*-
"""
综合审稿（review_all）—— 一次跑完门禁，输出一份审核报告；支持按三审制度分阶段执行

串联维度：
    humanizer   去 AI 痕迹（humanizer_check.py，FAIL 项必须改写）
    scale       规模审查（字数达标）
    continuity  一致性审稿（专名异写／角色属性／时间线／标题与正文）
    rationality 合理化审查（重复段落／对话占比／视角／伏笔／大纲覆盖）
    punctuation 标点审查（引号错位／半角标点／繁体／英文残留／密度）

三审制度（--stage）：
    first   初审 · 责任编辑   humanizer + scale + punctuation（机械层与文字层）
    second  复审 · 编辑部主任 continuity + rationality（内容层）
    final   终审 · 主编       全维回归确认 + 通读签发
    不带 --stage 时为「一次跑全部」的旧行为（等价于终审视角的全量报告）。
    审次只能单向流转：初审 FAIL 退回作者，复审 FAIL 退回初审，终审 FAIL 退回复审；
    后审有权推翻前审结论，前审不得推翻后审。

用法（在子项目根目录执行）：
    python "../GitHub Novel Serialization Skill/scripts/review_all.py"
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage first
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage second --chapters 031 034
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage final --batch "第9批" \
        --out .workbuddy/reports/终审签发_第9批.md
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --chapters 031 034 036
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --draft notes-personal/正文草稿.md --batch "第9批"
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --out .workbuddy/reports/草稿审核报告_2026-09-27.md
    python "../GitHub Novel Serialization Skill/scripts/review_all.py" --skip humanizer,scale

判定：任一维度 FAIL → 综合 FAIL（不得进定稿）；有 WARN → REVISE（人工复核）；否则 PASS。
终审 FAIL 未清零不得 promote；终审 WARN 须逐条裁决后由主编签发。
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _review_lib as L
import humanizer_check
import review_scale
import review_continuity
import review_rationality
import review_punctuation

DIMS = [('humanizer', '去 AI 痕迹'), ('scale', '规模审查'), ('continuity', '一致性审稿'),
        ('rationality', '合理化审查'), ('punctuation', '标点审查')]
DIM_KEYS = [k for k, _ in DIMS]
DIM_LABEL = dict(DIMS)


def run_humanizer(root, cfg):
    """复用 humanizer_check.check_file：定稿逐章单检，草稿按整份折算（等价章数）"""
    items = L.collect_items(root, cfg.get('chapters', ()), cfg.get('draft', ''))
    issues = []

    def collect(path, where):
        for lv, label, cnt, samples in humanizer_check.check_file(path)['issues']:
            loc = '、'.join('L%d:%s' % (a, b) for a, b in samples[:2])
            issues.append(L.Issue(lv, 'AI痕迹·%s' % label, '%s 处 %s' % (cnt, loc), where))

    if cfg.get('draft', ''):
        p = cfg['draft']
        collect(p if os.path.isabs(p) else os.path.join(root, p), '整份草稿')
    else:
        for it in items:
            collect(it.path, it.name)
    return issues


def run_dim(name, root, cfg):
    if name == 'humanizer':
        return run_humanizer(root, cfg)
    mod = {'scale': review_scale, 'continuity': review_continuity,
           'rationality': review_rationality, 'punctuation': review_punctuation}[name]
    results, _ = mod.run(root, cfg)
    issues = []
    for r in results:
        for i in r.issues:
            issues.append(L.Issue(i.level, i.category, i.detail, i.where or r.name))
    return issues


def todo_list(results):
    lines = []
    for r in results:
        for i in sorted(r.issues, key=lambda x: L.LEVEL_ORDER.get(x.level, 0), reverse=True):
            lines.append('- [ ] [%s] %s：%s —— %s' % (i.level, i.where or r.name, i.category, i.detail))
    return '\n'.join(lines) or '无待办。'


def main():
    ap = L.add_common_args(argparse.ArgumentParser(description='综合审稿：一次跑完门禁，支持三审分阶段'))
    ap.add_argument('--batch', default='', help='批次名（写入报告标题，如「第9批」）')
    ap.add_argument('--stage', default='', choices=('',) + L.STAGE_KEYS,
                    help='审次：first 初审／second 复审／final 终审；留空为一次跑全部（旧行为）')
    ap.add_argument('--skip', default='', help='跳过的维度，逗号分隔，如 humanizer,scale')
    ap.add_argument('--target', type=int, default=4000, help='每章目标字数（默认 4000）')
    ap.add_argument('--max', type=int, default=0, help='每章字数上限（0 = 不限）')
    a = ap.parse_args()
    root = L.find_root(a.root)
    skip = {s.strip() for s in a.skip.split(',') if s.strip()}
    cfg = {'chapters': a.chapters, 'draft': a.draft, 'root': root,
           'target': a.target, 'max': a.max}

    # 审次限定本审维度；留空则跑全部（旧行为）
    active = L.stage_dims(a.stage, DIM_KEYS) if a.stage else DIM_KEYS
    active = [k for k in DIM_KEYS if k in active and k not in skip]
    if a.stage and not active:
        raise SystemExit('审次「%s」无可审维度（是否被 --skip 全部跳过？）' % L.stage_label(a.stage))

    results, scale_sum = [], ''
    for key in active:
        issues = run_dim(key, root, cfg)
        results.append(L.make_result(DIM_LABEL[key], '', issues))
        if key == 'scale':
            _, scale_sum = review_scale.run(root, cfg)

    batch = '（%s）' % a.batch if a.batch else ''
    if a.stage:
        title = '%s审稿报告%s' % (L.stage_label(a.stage), batch)
    else:
        title = '综合审稿报告' + batch
    intro = ['- 审查范围：%s' % (a.draft or 'chapters/ 定稿')] + L.stage_intro(a.stage, DIM_KEYS) + [
        '- 参与维度：%s' % ('、'.join(r.name for r in results) or '（无）'),
        '- 门禁：任一 FAIL 不得同步定稿；WARN 需人工复核后方可送审']
    extra = []
    if scale_sum:
        extra.append(('规模概览', scale_sum))
    extra.append(('待办清单（按严重度排序）', todo_list(results)))
    md = L.render(title, results, intro=intro, extra_sections=extra,
                  obj_label='审查维度', stage=a.stage)
    L.emit(md, a.out or None)
    v = L.verdict(results)
    if a.stage:
        nxt = L.STAGE_KEYS[L.STAGE_KEYS.index(a.stage) + 1] if a.stage != 'final' else ''
        if v == 'FAIL':
            flow = '退回作者修改' if a.stage == 'first' else '退回上一审次'
        elif a.stage == 'final':
            flow = '签发通过，可 promote' if v == 'PASS' else 'WARN 须主编逐条裁决后签发'
        else:
            flow = '送%s（WARN 须先人工裁决）' % L.stage_label(nxt)
        print('\n>>> %s判定：%s ｜ 下一环节：%s' % (L.stage_label(a.stage), v, flow))
    else:
        print('\n>>> 综合判定：%s' % v)
    return 0 if v != 'FAIL' else 2


if __name__ == '__main__':
    sys.exit(main())
