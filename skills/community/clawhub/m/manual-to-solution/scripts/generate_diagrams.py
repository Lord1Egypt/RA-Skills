#!/usr/bin/env python3
"""
generate_diagrams.py - 生成解决方案建议书的标准配图

用法：
  python3 generate_diagrams.py <output_dir> [--font <font_name>]

生成6张PNG配图：
  01_architecture.png  - 技术架构图
  02_process_flow.png  - 业务流程图
  03_roadmap.png       - 实施路线图
  04_roi.png           - 投资回报分析
  05_value_map.png     - 痛点→功能→价值映射图
  06_security.png      - 安全架构图

可通过修改顶部 CONFIG 字典自定义颜色、数据和布局。
"""

import sys, os, argparse

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    print("ERROR: matplotlib not installed. Run: pip install matplotlib --break-system-packages")
    sys.exit(1)

# ============================================================
# CONFIG - 修改这里自定义图表
# ============================================================

CONFIG = {
    # 调色板
    'colors': {
        'blue':    '#1a73e8',
        'green':   '#34a853',
        'yellow':  '#f9ab00',
        'red':     '#ea4335',
        'purple':  '#7b1fa2',
        'pink':    '#e91e63',
    },
    'bg_colors': {
        'blue':    '#e8f0fe',
        'green':   '#e6f4ea',
        'yellow':  '#fef7e0',
        'red':     '#fce8e6',
        'purple':  '#f3e5f5',
        'gray':    '#f1f3f4',
    },

    # === 架构图配置 ===
    'architecture': {
        'title': '系统技术架构图',
        'layers': [
            {'name': '用户接入层', 'color': 'blue',
             'items': ['Web浏览器\n(PC端管理)', '移动APP', '大屏展示', '开放API']},
            {'name': '应用服务层', 'color': 'green',
             'items': ['业务模块A', '业务模块B', '业务模块C', '业务模块D',
                       '业务模块E', '业务模块F', '业务模块G', '权限管理']},
            {'name': '支撑服务层', 'color': 'green',
             'items': ['消息推送引擎', '工作流引擎', '安全审计引擎']},
            {'name': '数据服务层', 'color': 'yellow',
             'items': ['业务数据库', '空间数据', '数据仓库/报表']},
            {'name': '集成对接层', 'color': 'red',
             'items': ['终端设备', 'OA系统', '财务系统', '上级平台']},
            {'name': '基础设施层', 'color': 'gray',
             'items': ['云部署', '加密传输', '安全合规']},
        ]
    },

    # === 流程图配置 ===
    'process_flow': {
        'title': '核心业务流程',
        'flows': [
            {'name': '标准流程', 'color': 'blue',
             'steps': ['发起申请', '部门审核', '管理员派车', '执行出车', '确认收车', '完成']},
            {'name': '紧急流程', 'color': 'green',
             'steps': ['直接派车', '执行出车', '确认收车', '完成']},
            {'name': '补录流程', 'color': 'yellow',
             'steps': ['补录单据', '系统归档', '纳入统计']},
        ]
    },

    # === 路线图配置 ===
    'roadmap': {
        'title': '实施路线图 — 三阶段推进',
        'phases': [
            {'name': 'Phase 1\n第1-2月', 'subtitle': '核心上线', 'color': 'blue',
             'tasks': ['环境部署', '数据录入', '终端调试', '流程配置', '试点运行', '基础培训']},
            {'name': 'Phase 2\n第3-4月', 'subtitle': '数据治理', 'color': 'green',
             'tasks': ['数据迁移', '报表定制', '费用体系', '策略部署', '管理层培训', '全面推广']},
            {'name': 'Phase 3\n第5-6月', 'subtitle': '深化集成', 'color': 'yellow',
             'tasks': ['OA集成', '财务对接', '新模块上线', '驾驶舱', '上级对接', '运维完善']},
        ]
    },

    # === ROI配置 ===
    'roi': {
        'title': '投资回报分析',
        'costs': {
            'labels': ['软件许可', '实施部署', '终端设备', '服务器', '运维'],
            'values': [8, 5, 6, 4, 3],
        },
        'savings': {
            'labels': ['人力节约', '费用管控', '维修优化', '效率提升', '合计'],
            'values': [3, 24, 7, 5, 39],
        },
        'summary': '★ 投资回报周期：约 4-8 个月  |  3年净收益：约 91 万元',
    },

    # === 价值映射图配置 ===
    'value_map': {
        'title': '业务痛点 → 功能模块 → 业务价值 映射图',
        'mappings': [
            {'pain': '痛点A', 'func': '功能A1\n功能A2', 'value': '价值A', 'color': 'red'},
            {'pain': '痛点B', 'func': '功能B1\n功能B2', 'value': '价值B', 'color': 'blue'},
            {'pain': '痛点C', 'func': '功能C1\n功能C2', 'value': '价值C', 'color': 'green'},
            {'pain': '痛点D', 'func': '功能D1\n功能D2', 'value': '价值D', 'color': 'yellow'},
            {'pain': '痛点E', 'func': '功能E1\n功能E2', 'value': '价值E', 'color': 'purple'},
            {'pain': '痛点F', 'func': '功能F1\n功能F2', 'value': '价值F', 'color': 'pink'},
        ]
    },

    # === 安全架构配置 ===
    'security': {
        'title': '安全与合规体系架构',
        'pillars': [
            {'name': '身份认证', 'color': 'blue',
             'items': ['账号密码认证', '多因素认证(可选)', '密码重置机制', '会话超时管理']},
            {'name': '访问控制', 'color': 'green',
             'items': ['RBAC角色权限', '功能级控制', '按钮级控制', '数据范围隔离']},
            {'name': '数据安全', 'color': 'yellow',
             'items': ['传输加密', '数据库加密', '定期备份', '敏感字段脱敏']},
            {'name': '审计追溯', 'color': 'red',
             'items': ['操作日志', '登录审计', '变更追踪', '日志保留≥6月']},
            {'name': '合规适配', 'color': 'purple',
             'items': ['等保2.0', '数据安全法', '行业法规', '管理办法']},
        ]
    },
}


# ============================================================
# DRAWING FUNCTIONS
# ============================================================

def setup_font(font_name=None):
    """配置中文字体"""
    if font_name:
        plt.rcParams['font.sans-serif'] = [font_name]
    else:
        # 自动检测
        import subprocess
        try:
            result = subprocess.run(['fc-list', ':lang=zh'], capture_output=True, text=True)
            if 'Noto Sans CJK' in result.stdout:
                plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC']
            elif 'WenQuanYi' in result.stdout:
                plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
            else:
                plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        except FileNotFoundError:
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


def _c(color_key, cfg=CONFIG):
    """获取颜色"""
    return cfg['colors'].get(color_key, color_key)

def _bg(color_key, cfg=CONFIG):
    """获取背景色"""
    return cfg['bg_colors'].get(color_key, '#f5f5f5')


def draw_architecture(out_dir, cfg=CONFIG):
    """技术架构图"""
    c = cfg['architecture']
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.axis('off')
    ax.text(8, 10.6, c['title'], fontsize=18, ha='center', fontweight='bold',
            color='#1a1a2e', fontfamily='sans-serif')

    layers = c['layers']
    n_layers = len(layers)
    layer_h = 1.3
    gap = 0.15
    total_h = n_layers * layer_h + (n_layers - 1) * gap
    start_y = 9.5

    for i, layer in enumerate(layers):
        y = start_y - i * (layer_h + gap)
        color = _c(layer['color'])
        bg = _bg(layer['color'])

        rect = FancyBboxPatch((0.3, y - layer_h + 0.1), 15.4, layer_h,
                               boxstyle="round,pad=0.1", facecolor=bg,
                               edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(0.8, y - 0.15, layer['name'], fontsize=13, fontweight='bold',
                color=color, va='top', fontfamily='sans-serif')

        items = layer['items']
        n = len(items)
        sx = 1.2
        sp = (14.5 - sx) / n
        for j, item in enumerate(items):
            ix = sx + j * sp + sp / 2
            box = FancyBboxPatch((ix - sp*0.42, y - layer_h + 0.25), sp*0.84, layer_h - 0.5,
                                  boxstyle="round,pad=0.08", facecolor='white',
                                  edgecolor=color, linewidth=1.2, alpha=0.9)
            ax.add_patch(box)
            ax.text(ix, y - layer_h/2 + 0.05, item, fontsize=8.5, ha='center',
                    va='center', fontfamily='sans-serif', linespacing=1.4)

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '01_architecture.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()


def draw_process_flow(out_dir, cfg=CONFIG):
    """业务流程图"""
    c = cfg['process_flow']
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 16); ax.set_ylim(0, 9); ax.axis('off')
    ax.text(8, 8.5, c['title'], fontsize=18, ha='center', fontweight='bold',
            color='#1a1a2e', fontfamily='sans-serif')

    for fi, flow in enumerate(c['flows']):
        y_center = 7.0 - fi * 2.2
        color = _c(flow['color'])
        bg = _bg(flow['color'])

        ax.text(0.5, y_center + 0.85, flow['name'], fontsize=12, fontweight='bold',
                color=color, fontfamily='sans-serif')

        steps = flow['steps']
        n = len(steps)
        sp = 14.0 / max(n, 1)
        for i, step in enumerate(steps):
            cx = 1.0 + i * sp + sp * 0.5
            box = FancyBboxPatch((cx - 0.95, y_center - 0.55), 1.9, 1.1,
                                  boxstyle="round,pad=0.1", facecolor=bg,
                                  edgecolor=color, linewidth=1.5)
            ax.add_patch(box)
            ax.text(cx, y_center, step, fontsize=9, ha='center', va='center',
                    fontfamily='sans-serif', color='#333', linespacing=1.3)
            if i < n - 1:
                ax.annotate('', xy=(cx + sp - 0.95, y_center),
                            xytext=(cx + 0.95, y_center),
                            arrowprops=dict(arrowstyle='->', color=color, lw=2))

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '02_process_flow.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()


def draw_roadmap(out_dir, cfg=CONFIG):
    """实施路线图"""
    c = cfg['roadmap']
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(0, 16); ax.set_ylim(0, 7); ax.axis('off')
    ax.text(8, 6.5, c['title'], fontsize=18, ha='center', fontweight='bold',
            color='#1a1a2e', fontfamily='sans-serif')

    phases = c['phases']
    n = len(phases)
    pw = (15.0 - (n-1)*0.2) / n
    for i, phase in enumerate(phases):
        x = 0.5 + i * (pw + 0.2)
        color = _c(phase['color'])
        bg = _bg(phase['color'])

        header = FancyBboxPatch((x, 4.8), pw, 1.2, boxstyle="round,pad=0.1",
                                 facecolor=color, edgecolor=color, linewidth=2)
        ax.add_patch(header)
        ax.text(x + pw/2, 5.55, phase['name'], fontsize=12, ha='center', va='center',
                fontweight='bold', color='white', fontfamily='sans-serif', linespacing=1.3)
        ax.text(x + pw/2, 4.95, phase['subtitle'], fontsize=10, ha='center',
                va='center', color='white', fontfamily='sans-serif')

        for j, task in enumerate(phase['tasks']):
            ty = 4.3 - j * 0.65
            tb = FancyBboxPatch((x + 0.15, ty - 0.22), pw - 0.3, 0.5,
                                 boxstyle="round,pad=0.08", facecolor=bg,
                                 edgecolor=color, linewidth=1, alpha=0.9)
            ax.add_patch(tb)
            ax.text(x + pw/2, ty, task, fontsize=9, ha='center', va='center',
                    fontfamily='sans-serif', color='#333')

        if i < n - 1:
            ax.annotate('', xy=(x + pw + 0.05, 5.4), xytext=(x + pw - 0.05, 5.4),
                        arrowprops=dict(arrowstyle='->', color='#666', lw=2.5))

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '03_roadmap.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()


def draw_roi(out_dir, cfg=CONFIG):
    """投资回报分析"""
    c = cfg['roi']
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))
    fig.suptitle(c['title'], fontsize=18, fontweight='bold',
                 fontfamily='sans-serif', y=0.98)

    # 左：成本饼图
    ax1 = axes[0]
    colors = [_c(k) for k in ['blue','green','yellow','red','purple']]
    wedges, texts, at = ax1.pie(
        c['costs']['values'], labels=c['costs']['labels'],
        autopct='%1.0f%%', colors=colors, startangle=90,
        textprops={'fontsize': 11, 'fontfamily': 'sans-serif'})
    for t in at:
        t.set_fontsize(10); t.set_fontweight('bold')
    ax1.set_title('成本构成', fontsize=14, fontweight='bold',
                  fontfamily='sans-serif', pad=15)

    # 右：收益柱图
    ax2 = axes[1]
    bars = ax2.bar(c['savings']['labels'], c['savings']['values'],
                   color=colors, width=0.6, edgecolor='white', linewidth=1.5)
    for bar, val in zip(bars, c['savings']['values']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                 f'{val}万', ha='center', fontsize=12, fontweight='bold',
                 fontfamily='sans-serif')
    ax2.set_ylabel('年化收益（万元）', fontsize=12, fontfamily='sans-serif')
    ax2.set_title('年化收益估算', fontsize=14, fontweight='bold',
                  fontfamily='sans-serif', pad=15)
    max_val = max(c['savings']['values'])
    ax2.set_ylim(0, max_val * 1.2)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.text(0.5, 0.02, c['summary'], ha='center', fontsize=14,
             fontweight='bold', color=_c('blue'), fontfamily='sans-serif',
             bbox=dict(boxstyle='round,pad=0.5', facecolor=_bg('blue'),
                       edgecolor=_c('blue')))

    fig.tight_layout(rect=[0, 0.08, 1, 0.95])
    fig.savefig(os.path.join(out_dir, '04_roi.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()


def draw_value_map(out_dir, cfg=CONFIG):
    """痛点→功能→价值映射图"""
    c = cfg['value_map']
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16); ax.set_ylim(0, 8); ax.axis('off')
    ax.text(8, 7.5, c['title'], fontsize=18, ha='center', fontweight='bold',
            color='#1a1a2e', fontfamily='sans-serif')

    mappings = c['mappings']
    n = len(mappings)
    cw = (15.0 - (n-1)*0.2) / n

    for i, m in enumerate(mappings):
        x = 0.5 + i * (cw + 0.2)
        color = _c(m['color'])
        bg = _bg(m['color'])

        # 痛点
        pb = FancyBboxPatch((x, 5.4), cw, 1.3, boxstyle="round,pad=0.1",
                             facecolor=_bg('red'), edgecolor=color, linewidth=2)
        ax.add_patch(pb)
        ax.text(x + cw/2, 6.05, m['pain'], fontsize=9.5, ha='center', va='center',
                fontweight='bold', color='#333', fontfamily='sans-serif')

        ax.annotate('', xy=(x + cw/2, 5.2), xytext=(x + cw/2, 5.4),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))

        # 功能
        fb = FancyBboxPatch((x, 3.0), cw, 2.2, boxstyle="round,pad=0.1",
                             facecolor=_bg('blue'), edgecolor=color, linewidth=1.5)
        ax.add_patch(fb)
        ax.text(x + cw/2, 4.1, m['func'], fontsize=8.5, ha='center', va='center',
                color='#333', fontfamily='sans-serif', linespacing=1.4)

        ax.annotate('', xy=(x + cw/2, 2.8), xytext=(x + cw/2, 3.0),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))

        # 价值
        vb = FancyBboxPatch((x, 0.8), cw, 2.0, boxstyle="round,pad=0.1",
                             facecolor=_bg('green'), edgecolor=color, linewidth=2)
        ax.add_patch(vb)
        ax.text(x + cw/2, 1.8, m['value'], fontsize=9, ha='center', va='center',
                color=_c('blue'), fontweight='bold', fontfamily='sans-serif')

    # 侧标签
    if n > 0:
        ax.text(0.2, 6.05, '痛\n点', fontsize=10, va='center', color=_c('red'),
                fontweight='bold', fontfamily='sans-serif')
        ax.text(0.2, 4.1, '功\n能', fontsize=10, va='center', color=_c('blue'),
                fontweight='bold', fontfamily='sans-serif')
        ax.text(0.2, 1.8, '价\n值', fontsize=10, va='center', color=_c('green'),
                fontweight='bold', fontfamily='sans-serif')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '05_value_map.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()


def draw_security(out_dir, cfg=CONFIG):
    """安全架构图"""
    c = cfg['security']
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(0, 16); ax.set_ylim(0, 7); ax.axis('off')
    ax.text(8, 6.5, c['title'], fontsize=18, ha='center', fontweight='bold',
            color='#1a1a2e', fontfamily='sans-serif')

    pillars = c['pillars']
    n = len(pillars)
    pw = (15.0 - (n-1)*0.1) / n
    for i, p in enumerate(pillars):
        x = 0.5 + i * (pw + 0.1)
        color = _c(p['color'])
        bg = _bg(p['color'])

        tb = FancyBboxPatch((x, 5.0), pw, 0.8, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor=color, linewidth=2)
        ax.add_patch(tb)
        ax.text(x + pw/2, 5.4, p['name'], fontsize=13, ha='center', va='center',
                fontweight='bold', color='white', fontfamily='sans-serif')

        for j, item in enumerate(p['items']):
            iy = 4.3 - j * 0.85
            ib = FancyBboxPatch((x + 0.1, iy - 0.28), pw - 0.2, 0.56,
                                 boxstyle="round,pad=0.08", facecolor=bg,
                                 edgecolor=color, linewidth=1, alpha=0.9)
            ax.add_patch(ib)
            ax.text(x + pw/2, iy, item, fontsize=9, ha='center', va='center',
                    fontfamily='sans-serif', color='#333')

    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, '06_security.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成解决方案建议书标准配图')
    parser.add_argument('output_dir', help='PNG输出目录')
    parser.add_argument('--font', default=None, help='中文字体名称（如 "Noto Sans CJK SC"）')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    setup_font(args.font)

    draw_architecture(args.output_dir)
    draw_process_flow(args.output_dir)
    draw_roadmap(args.output_dir)
    draw_roi(args.output_dir)
    draw_value_map(args.output_dir)
    draw_security(args.output_dir)

    print(f'✓ 6张配图已生成到 {args.output_dir}/')
    for f in sorted(os.listdir(args.output_dir)):
        if f.endswith('.png'):
            size = os.path.getsize(os.path.join(args.output_dir, f))
            print(f'  {f} ({size//1024}KB)')
