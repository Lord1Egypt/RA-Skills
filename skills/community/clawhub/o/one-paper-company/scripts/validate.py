#!/usr/bin/env python3
"""
validate.py - 校验 one-paper-company 产物 HTML
Usage: python validate.py <output.html> [--data data.json]

检查项：
  1. 结构完整性：hero/scrolly/outro/footer 四大区齐全
  2. 10 步联动：s1-s10 + 10 个 vp 面板
  3. 数据注入：15 个 var 声明齐全（PRE/CANDLES/FIN/SEG/...）
  4. 配色铁律：--green/--green-d 已替换，中性色未变
  5. 占位符：无 __PLACEHOLDER__ 残留（允许 ECharts 内部 ___EC__*___）
  6. 资产内联：ECharts + pixel-font + base64 图片
  7. 体积：< 3 MB
  8. 信源三层：数组注释 + vp-foot + outro footgrid
"""
import sys, re, pathlib, argparse, json

def check(label, condition, detail=''):
    status = '✓' if condition else '✗'
    print(f'  {status} {label}' + (f' — {detail}' if detail and not condition else ''))
    return condition

def validate(html_path, data_path=None):
    html = pathlib.Path(html_path).read_text(encoding='utf-8')
    size_mb = len(html.encode('utf-8')) / 1024 / 1024
    print(f'\n=== Validating: {html_path} ({size_mb:.2f} MB) ===\n')

    all_pass = True

    # 1. 结构完整性
    print('[1/8] 结构完整性')
    all_pass &= check('hero 区', '<header class="hero">' in html)
    all_pass &= check('scrolly 主区', '<main class="scrolly">' in html)
    all_pass &= check('outro 区', '<section class="outro">' in html)
    all_pass &= check('footer', '<footer>' in html)

    # 2. 10 步联动（注：Step 4/5 共享 vp-kline，故 9 个 vp 面板）
    print('\n[2/8] 10 步联动')
    step_count = len(re.findall(r'<section class="step" id="s\d+"', html))
    all_pass &= check(f'10 个 step（找到 {step_count}）', step_count == 10)
    vp_count = len(re.findall(r'<div class="vp" id="vp-', html))
    all_pass &= check(f'9 个 vp 面板（Step4/5 共享 vp-kline，找到 {vp_count}）', vp_count == 9)

    # 3. 数据注入
    print('\n[3/8] 数据注入（15 个核心 var）')
    required_vars = ['PRE', 'CLOSES', 'CANDLES', 'EVENTS', 'FIN', 'SEG', 'HF', 'INV',
                     'WALL', 'FATE_CLASS', 'SCORES', 'EXCLUDED', 'RADAR', 'STAGES', 'CLOCK', 'SIGNALS']
    missing = [v for v in required_vars if f'var {v} =' not in html and f'var {v}=' not in html]
    all_pass &= check(f'15+ 数据 var 齐全（缺失: {missing or "无"}）', len(missing) == 0)

    # 4. 配色铁律
    print('\n[4/8] 配色铁律')
    # 检查 --green 不是占位符
    green_match = re.search(r'--green:\s*(#[0-9a-fA-F]{6})', html)
    all_pass &= check('--green 已替换为真实色值', green_match and green_match.group(1) != '__BRAND_GREEN__',
                       f'当前: {green_match.group(1) if green_match else "未找到"}')
    # 检查中性色未变
    neutral_fixed = '--bg:#f7f5f0' in html and '--ink:#20242b' in html and '--line:#e4e0d6' in html
    all_pass &= check('中性色未变（--bg/--ink/--line）', neutral_fixed)

    # 5. 占位符
    print('\n[5/8] 占位符残留')
    # 真实占位符格式：__WORD__（前后各 2 个下划线，中间纯大写字母+下划线）
    # ECharts 内部 token 格式：___EC__WORD__或__WORD___（3+ 下划线），需排除
    all_placeholders = re.findall(r'__[A-Z][A-Z_]{2,}__', html)
    real_remaining = [p for p in all_placeholders if not (p.startswith('___') or p.endswith('___'))]
    # 进一步排除被三下划线包裹的（如 ___EC__COMPONENT__ 中的 __COMPONENT__）
    real_remaining = [p for p in real_remaining if f'___{p}' not in html and f'{p}___' not in html]
    all_pass &= check(f'无真实占位符残留（{len(real_remaining)} 个）', len(real_remaining) == 0,
                       f'残留: {set(real_remaining)}')
    ec_internal = [p for p in all_placeholders if p not in real_remaining]
    if ec_internal:
        print(f'      ℹ ECharts 内部 token 忽略: {len(set(ec_internal))} 种')

    # 6. 资产内联
    print('\n[6/8] 资产内联')
    all_pass &= check('ECharts 内联', 'echarts' in html.lower() and 'var echarts' in html.lower() or 'function' in html)
    all_pass &= check('pixel-font 内联（var FONT）', 'var FONT' in html or 'FONT={' in html)
    img_count = len(re.findall(r'data:image/', html))
    all_pass &= check(f'base64 图片（{img_count} 张）', img_count > 0)

    # 7. 体积
    print('\n[7/8] 体积')
    all_pass &= check(f'< 3 MB（当前 {size_mb:.2f} MB）', size_mb < 3)

    # 8. 信源三层
    print('\n[8/8] 信源三层标注')
    vp_foot_count = len(re.findall(r'class="vp-foot"', html))
    all_pass &= check(f'vp-foot 信源注（{vp_foot_count} 个，需 ≥7）', vp_foot_count >= 7)
    all_pass &= check('outro footgrid', 'class="footgrid"' in html)
    all_pass &= check('数据数组注释', '// 稀疏史前点' in html or '// 月线 K' in html)

    # 如果提供了 data.json，对比数据完整性
    if data_path:
        print('\n[附加] data.json 对比')
        data = json.loads(pathlib.Path(data_path).read_text(encoding='utf-8'))
        for key in ['pre', 'candles', 'fin', 'scores', 'signals']:
            if key in data:
                expected_len = len(data[key])
                # 在 HTML 中找对应 var 的长度（粗略）
                pattern = rf'var {key.upper()} = \['
                m = re.search(pattern, html)
                all_pass &= check(f'data.{key} 已注入', m is not None)

    # 总结
    print('\n' + '='*50)
    if all_pass:
        print(f'✓ ALL CHECKS PASSED ({size_mb:.2f} MB)')
    else:
        print(f'✗ SOME CHECKS FAILED — review above')
    print('='*50)
    return 0 if all_pass else 1

def main():
    parser = argparse.ArgumentParser(description='Validate one-paper-company output HTML')
    parser.add_argument('html', help='Path to output HTML')
    parser.add_argument('--data', default=None, help='Path to data.json for comparison')
    args = parser.parse_args()
    sys.exit(validate(args.html, args.data))

if __name__ == '__main__':
    main()
