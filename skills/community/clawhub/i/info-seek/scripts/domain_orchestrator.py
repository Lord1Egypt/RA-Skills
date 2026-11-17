#!/usr/bin/env python3
"""
domain_orchestrator.py — Infoseek 领域调度器（v1.9.0）

整合 domain_router + domain profile + Jinja2 模板 + Anchor_Score 领域加权，
端到端完成"主题 → 领域 → 模板 → 评分 → 报告"全流程。

调用链：
  1. detect_domain(subject) → 选定 profile
  2. 加载 profile YAML（信任源 + 关键词模板）
  3. 加载 Jinja2 模板（每领域一个）
  4. 应用 profile 权重 → 给每个 source 打分
  5. 渲染模板 → 输出 Markdown 报告
  6. 返回渲染结果 + 领域元数据

CLI 用法:
  python domain_orchestrator.py "<subject>" < sources.json > out.md
"""

import os
import re
import sys
import json
import yaml
from pathlib import Path
from typing import Optional

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / 'infoseek')))
INFOSEEK_ROOT = Path(os.environ.get('INFOSEEK_ROOT', str(Path(__file__).parent.parent)))

# ── S7：dep_registry 事实层惰性 accessor（外部依赖可用性统一求值，零漂移）──
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _cand = Path(__file__).resolve().parent.parent / "core"
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        import dep_registry as _mod
        _dr = _mod
    return _dr


def _excerpt(text, limit: int = 600) -> str:
    """正文摘要（P2 内容链中枢字段）：压缩空白/换行 → 取前 limit 字符

    s.text 为抓取正文，长度不定且含脏空白；统一在此归一，
    模板 / _render_simple / _render_fallback 三处消费同一 text_excerpt。
    """
    if not text:
        return ''
    norm = re.sub(r'\s+', ' ', str(text)).strip()
    if len(norm) <= limit:
        return norm
    return norm[:limit].rstrip() + '…'


# ─── DEF-14（v2.1.1 P2）：报告输出层注入清洗 ─────────────────────────
# 背景：Jinja2 Template 默认 autoescape=False（见 _render_jinja2），外部可控字段
#   （subject/title/platform/snippet）原样进 Markdown。已实测无 SSTI（{{7*7}} 不求值，
#   模板预编译固定），仅存输出层注入面：下游若把报告 Markdown→HTML 渲染且不转义，
#   <script> 会执行；[x](javascript:...) 在部分渲染器可触发。
# 处置（报告方案 B：输入清洗，保留正常 Markdown）：移除脚本/事件/危险协议，
#   不转义有意的 <details>、正常链接与中文，避免伤排版。仅清洗外部输入，
#   内部自生成的 filter_block（含自有 <details>）不过此函数。
_DANGEROUS_TAGS_RE = re.compile(
    r'<\s*/?\s*(script|iframe|object|embed|svg|img|link|meta|style)\b[^>]*>',
    re.IGNORECASE | re.DOTALL)
# 标签内事件处理器 on*=（保留标签本身，仅摘掉危险属性；含前导空白防误伤正常词）
_ON_EVENT_ATTR_RE = re.compile(r'\son\w+\s*=\s*"[^"]*"', re.IGNORECASE)
_ON_EVENT_ATTR_SQ_RE = re.compile(r"\son\w+\s*=\s*'[^']*'", re.IGNORECASE)
_ON_EVENT_ATTR_BARE_RE = re.compile(r'\son\w+\s*=\s*[^\s>]+', re.IGNORECASE)
# Markdown 链接 / 裸 URL 中的危险协议（javascript:/data:/vbscript:）
_DANGEROUS_PROTO_RE = re.compile(
    r'(javascript|data|vbscript)\s*:', re.IGNORECASE)


def sanitize_markdown_input(value) -> str:
    """清洗进入报告 Markdown 的外部可控字符串（DEF-14）。

    - 非字符串 → 归一为字符串（None→''）；
    - 移除可执行/嵌入类危险标签；摘掉标签内 on*= 事件属性；
    - 中和危险协议（冒号前插入零宽空格阻断，不破坏可读文本）；
    - 保留正常 Markdown：<details>、[文字](https url)、中文、表格。
    """
    if value is None:
        return ''
    if not isinstance(value, str):
        value = str(value)
    text = _DANGEROUS_TAGS_RE.sub('', value)
    text = _ON_EVENT_ATTR_RE.sub('', text)
    text = _ON_EVENT_ATTR_SQ_RE.sub('', text)
    text = _ON_EVENT_ATTR_BARE_RE.sub('', text)
    text = _DANGEROUS_PROTO_RE.sub(lambda m: m.group(1) + '​:', text)
    return text


def sanitize_csv_cell(value) -> str:
    """CSV 单元格公式注入防护（DEF-14）：电子表格把 =/+/-/@ 开头单元格当公式执行。

    首字符命中 =、+、-、@、Tab、CR 时前置单引号强制按文本处理（OWASP CSV injection）。
    数值型（int/float）不处理，避免污染真实分数。
    """
    if value is None:
        return ''
    if isinstance(value, (int, float)):
        return value
    text = str(value)
    if text and text[0] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + text
    return text


class DomainOrchestrator:
    """领域调度器（v1.9.0 主推①）"""

    def __init__(self, profile_dir: str = None, template_dir: str = None):
        self.profile_dir = Path(profile_dir) if profile_dir else INFOSEEK_ROOT / 'domains'
        self.template_dir = Path(template_dir) if template_dir else self.profile_dir / 'templates'
        self.profiles = self._load_all_profiles()
        self.templates = self._load_all_templates()

    def _load_all_profiles(self) -> dict:
        """加载所有领域 profile YAML"""
        profiles = {}
        for f in sorted(self.profile_dir.glob('*.yaml')):
            if f.stem == 'README':
                continue
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    profiles[f.stem] = {
                        'name': f.stem,
                        'raw': fp.read(),
                        'path': str(f),
                    }
            except Exception:
                pass
        return profiles

    def _load_all_templates(self) -> dict:
        """加载所有 Jinja2 模板（v2.0.0：模板并入 domains/templates.yaml）

        存储演进：
          v1.x：domains/templates/*.md.j2 独立文件（平台禁止 .j2 类型）
          v2.0：domains/templates.yaml 块标量合并（同文保真，兼容回退旧目录）
        """
        templates = {}
        yaml_file = self.profile_dir / 'templates.yaml'
        if yaml_file.exists():
            try:
                with open(yaml_file, 'r', encoding='utf-8') as fp:
                    data = yaml.safe_load(fp) or {}
                for name, raw in (data.get('templates') or {}).items():
                    if isinstance(raw, str):
                        templates[name] = {
                            'name': f'{name}.md',
                            'raw': raw,
                            'path': f'{yaml_file.name}#{name}',
                        }
            except Exception:
                pass
        # 回退：旧版独立 .md.j2 目录（兼容历史部署）
        if not templates and self.template_dir.exists():
            for f in sorted(self.template_dir.glob('*.md.j2')):
                try:
                    with open(f, 'r', encoding='utf-8') as fp:
                        template_text = fp.read()
                    templates[f.stem.replace('.md', '')] = {
                        'name': f.stem,
                        'raw': template_text,
                        'path': str(f),
                    }
                except Exception:
                    pass
        return templates

    def detect(self, subject: str) -> dict:
        """检测领域（包装 domain_router.detect_domain）"""
        sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
        try:
            from domain_router import detect_domain
            return detect_domain(subject)
        except ImportError:
            return {'domain': None, 'score': 0, 'is_default': True, 'profile_path': None}

    def apply_to_scoring(self, source: dict, subject: str) -> dict:
        """应用领域权重给单个源打分（包装 anchor_adapter.calculate_score）

        返回合并 dict：原 source 字段 + 评分结果
        """
        sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
        try:
            from anchor_adapter import calculate_score
        except ImportError:
            return source

        domain_result = self.detect(subject)
        profile = None
        if domain_result.get('profile_path'):
            profile = {
                'name': domain_result['domain'],
                'raw': open(domain_result['profile_path'], encoding='utf-8').read(),
            }

        score_result = calculate_score(
            source, subject,
            with_domain=bool(profile),
            domain_profile=profile,
            prefer_kb=bool(domain_result.get('prefer_kb')),
        )

        # 合并：保留原字段 + 评分结果
        merged = dict(source)
        merged['_scoring'] = score_result
        merged['final_score'] = score_result.get('after_whitelist', score_result.get('raw_score', 0))
        return merged

    def render_report(self, subject: str, sources: list,
                      min_score: int = 40,
                      domain_override: str = None) -> dict:
        """按领域模板渲染最终报告

        参数:
            subject: 调研主题
            sources: 来源列表 [{title, url, platform, score, snippet, ...}, ...]
            min_score: 最低分数阈值
            domain_override: 手动指定领域（默认 None = 自动检测）

        返回:
            {
                'subject': subject,
                'domain': 'tech-research',
                'template_used': '.../tech-research.md.j2',
                'markdown': '...',
                'qualified_count': N,
                'total_count': M,
                'is_default_template': False,
            }
        """
        # P1(G-04/G-05)：入参类型守卫。subject 为 None / 非字符串时归一为空串
        # （旧代码直接透传 detect → subject.lower() 抛 AttributeError 击穿渲染）。
        if not isinstance(subject, str):
            subject = '' if subject is None else str(subject)
        # sources 容错：丢弃非 dict 脏条目（字符串/数字/None 调 .get 会崩）。
        # total_count 按原始入参计数，仅过滤参与渲染，不静默改写调用方列表长度。
        total_input = len(sources) if isinstance(sources, (list, tuple)) else 0
        sources = [s for s in (sources or []) if isinstance(s, dict)]

        # 1. 检测 / 覆盖领域
        if domain_override:
            domain = domain_override
            is_default = False
        else:
            detect_result = self.detect(subject)
            domain = detect_result.get('domain')
            is_default = detect_result.get('is_default', True)

        # 2. 过滤低分源（P0-OPEN-04：同时收集被过滤清单 + 原因，核心源为 0 时禁止空骨架）
        def _num_score(x):
            try:
                return float(x) if x is not None else 0.0
            except (TypeError, ValueError):
                return 0.0

        all_zero = bool(sources) and all(
            _num_score(x.get('score', 0)) <= 0 for x in sources)
        qualified = []
        filtered_out = []
        for idx, s in enumerate(sources):
            sc = _num_score(s.get('score', 0))
            if sc >= min_score:
                qualified.append(s)
            else:
                if all_zero:
                    reason = '核心源评分为 0（评分缺失/未评分，疑似评分链断裂）'
                elif sc <= 0:
                    reason = '评分为 0/缺失（未通过评分或无文本可评分）'
                else:
                    reason = f'低于入围阈值（{sc:.0f} < {min_score}）'
                filtered_out.append({
                    'index': idx + 1,
                    'title': s.get('title') or s.get('url') or 'Untitled',
                    'url': s.get('url', ''),
                    'platform': s.get('platform', ''),
                    'score': sc,
                    'reason': reason,
                })

        # 3. 应用领域打分（可选；P1 G-05：单条脏源异常不击穿整份渲染）
        scored = []
        for s in qualified:
            try:
                scored.append(self.apply_to_scoring(s, subject))
            except Exception:
                scored.append(dict(s))

        # 4. 加载模板
        template_name = domain if domain and domain in self.templates else 'default'
        template_info = self.templates.get(template_name)
        is_default_template = template_name == 'default'

        # 5. 渲染 Markdown（用 final_score 替代 score 字段以兼容模板）
        rendered_sources = []
        for s in scored:
            rs = dict(s)
            if 'final_score' in rs and 'score' not in rs:
                rs['score'] = rs['final_score']
            # P2 内容链（2026-09-10）：正文摘要字段——渲染层消费 s.text 的中枢，
            # 模板 / _render_simple / _render_fallback 统一使用（长度归一 + 脏空白清洗）
            # DEF-14：text 先清洗注入载荷再摘要；其余外部可控字段渲染前统一清洗。
            for _f in ('title', 'url', 'platform', 'snippet'):
                if _f in rs and isinstance(rs[_f], str):
                    rs[_f] = sanitize_markdown_input(rs[_f])
            rs['text_excerpt'] = sanitize_markdown_input(_excerpt(rs.get('text')))
            rendered_sources.append(rs)

        # P0-OPEN-04：被过滤清单的 Markdown 块（核心源为 0 时前置告警，禁止空骨架）
        # DEF-14：filtered_out 的 title/platform 来自外部输入，渲染前清洗；url 仅进
        # markdown 链接，危险协议在 sanitize_markdown_input 内中和。
        for _fo in filtered_out:
            _fo['title'] = sanitize_markdown_input(_fo.get('title'))
            _fo['platform'] = sanitize_markdown_input(_fo.get('platform'))
            _fo['url'] = sanitize_markdown_input(_fo.get('url'))
        filter_block = self._render_filtered_block(filtered_out, all_zero, min_score)

        # DEF-14：渲染用 subject 副本做注入清洗（路由 detect / 评分 apply_to_scoring
        # 仍用原始 subject，保证语义匹配不变）。
        render_subject = sanitize_markdown_input(subject)

        # 6. 渲染模板
        if template_info:
            markdown = self._render_jinja2(template_info['raw'], {
                'subject': render_subject,
                'domain': domain,
                'sources': rendered_sources,
                'sources_count': len(rendered_sources),
                'is_default_template': is_default_template,
                'filtered_count': len(filtered_out),
                'filtered_out': filtered_out,
                'all_core_zero': all_zero,
                'filter_block': filter_block,
            })
        else:
            markdown = self._render_fallback(render_subject, domain, rendered_sources)

        # P0-OPEN-04：无核心源时禁止空骨架——把过滤清单与原因前置到报告顶部；
        # 有核心源但存在被滤源时，把清单附到报告末尾（可追溯，不干扰正文）。
        if filtered_out:
            if all_zero or not rendered_sources:
                markdown = filter_block + "\n---\n\n" + markdown
            else:
                markdown = markdown.rstrip() + "\n\n" + filter_block + "\n"

        return {
            'subject': subject,
            'domain': domain,
            'template_used': template_info['path'] if template_info else 'fallback',
            'markdown': markdown,
            'qualified_count': len(qualified),
            'total_count': total_input,
            'dropped_non_dict': total_input - len(sources),  # P1：被跳过的脏条目数
            'filtered_count': len(filtered_out),       # P0-OPEN-04
            'filtered_out': filtered_out,             # P0-OPEN-04：被过滤清单及原因
            'all_core_zero': all_zero,                # P0-OPEN-04：核心源全为 0
            'is_default_template': is_default_template,
        }

    @staticmethod
    def _render_filtered_block(filtered_out: list, all_zero: bool,
                               min_score: int) -> str:
        """P0-OPEN-04：渲染「被过滤来源清单及原因」Markdown 块。

        核心源全为 0 时输出醒目告警（禁止假装成功的空骨架）；
        常规低分过滤时输出可追溯清单。
        """
        if not filtered_out:
            return ''
        lines = []
        if all_zero:
            lines.append('## ⚠️ 无可用核心来源（评分链异常）')
            lines.append('')
            lines.append('输入的来源评分为 **0**，未产出任何入围核心源。'
                         '这通常意味着评分链断裂（未评分/抓取正文为空/量纲异常），'
                         '**而非"主题确实无资料"**。以下来源全部被过滤：')
        else:
            lines.append(f'<details><summary>📋 被过滤来源（{len(filtered_out)} 条，'
                         f'入围阈值 ≥ {min_score} 分）</summary>')
            lines.append('')
        lines.append('')
        lines.append('| # | 来源 | 平台 | 评分 | 过滤原因 |')
        lines.append('|:--|:-----|:-----|----:|:---------|')
        for item in filtered_out:
            title = str(item['title']).replace('|', '\\|')[:60]
            url = item.get('url') or ''
            label = f'[{title}]({url})' if url else title
            platform = str(item.get('platform') or '-').replace('|', '\\|')
            lines.append(f"| {item['index']} | {label} | {platform} | "
                         f"{item['score']:.0f} | {item['reason']} |")
        lines.append('')
        if not all_zero:
            lines.append('</details>')
        lines.append('')
        return '\n'.join(lines)

    def _render_jinja2(self, template_text: str, context: dict) -> str:
        """使用 Jinja2 渲染模板（P1 G-05：任何渲染异常都降级，禁止击穿 render_report）。

        降级链：Jinja2 → 缺 Jinja2(ImportError) 或模板渲染错(UndefinedError/TypeError
        等脏上下文) → _render_simple 简单替换 → 再失败 → _render_fallback 兜底列表。
        """
        try:
            if not _dep_reg().is_available("Jinja2"):
                return self._render_simple(template_text, context)
            from jinja2 import Template
            tmpl = Template(template_text)
            return tmpl.render(**context)
        except ImportError:
            return self._render_simple(template_text, context)
        except Exception:
            # P1(G-05)：模板引用了脏字段 / 上下文类型不符等渲染期错误——
            # 不应让单条畸形源或模板缺陷击穿整份报告，降级到无模板依赖的渲染。
            try:
                return self._render_simple(template_text, context)
            except Exception:
                return self._render_fallback(context.get('subject', ''),
                                             context.get('domain'),
                                             context.get('sources', []))

    def _render_simple(self, template_text: str, context: dict) -> str:
        """无 Jinja2 时的简易渲染（{{ var }} 形式）"""
        result = template_text
        result = result.replace('{{ subject }}', str(context.get('subject', '')))
        result = result.replace('{{ domain }}', str(context.get('domain', '')))
        # 简化：sources 列表只插入计数
        sources = context.get('sources', [])
        result = result.replace('{{ sources_count }}', str(len(sources)))
        # sources 列表：简易循环渲染
        if '{% for s in sources %}' in result:
            parts = result.split('{% for s in sources %}')
            if len(parts) == 2:
                head, rest = parts
                loop_body, tail = rest.split('{% endfor %}', 1)
                rendered_sources = ''.join(loop_body.replace('{{ s.title }}', str(s.get('title', '')))
                                          .replace('{{ s.score }}', str(s.get('score', 0)))
                                          .replace('{{ s.url }}', str(s.get('url', '')))
                                          .replace('{{ s.platform }}', str(s.get('platform', '')))
                                          .replace('{{ s.snippet }}', str(s.get('snippet', '')))
                                          for s in sources)
                result = head + rendered_sources + tail
        return result

    def _render_fallback(self, subject: str, domain: Optional[str], sources: list) -> str:
        """无模板时的兜底渲染"""
        lines = [f"# {subject}", ""]
        if domain:
            lines.append(f"> 领域：**{domain}**")
        lines.append(f"> 来源：{len(sources)} 条")
        lines.extend(["", "## 锚点列表", ""])
        for i, s in enumerate(sources, 1):
            lines.append(f"### {i}. {s.get('title', 'Untitled')} — {s.get('score', 0)}")
            lines.append(f"- **平台**: {s.get('platform', '')}")
            lines.append(f"- **链接**: {s.get('url', '')}")
            if s.get('snippet'):
                lines.append(f"\n> {s.get('snippet', '')[:300]}")
            if s.get('text_excerpt'):
                lines.append(f"\n> 📄 正文要点：{s['text_excerpt']}")
            lines.append("")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python domain_orchestrator.py <subject> [domain_override]")
        sys.exit(1)

    subject = sys.argv[1]
    domain_override = sys.argv[2] if len(sys.argv) > 2 else None

    # 从 stdin 读取 sources
    try:
        sources_data = json.loads(sys.stdin.read() or '{}')
    except json.JSONDecodeError:
        sources_data = {}

    sources = sources_data.get('sources', [])

    orchestrator = DomainOrchestrator()
    result = orchestrator.render_report(subject, sources, domain_override=domain_override)
    print(result['markdown'])
    sys.stderr.write(f"\n[orchestrator] domain={result['domain']} template={result['template_used']}\n")


if __name__ == '__main__':
    main()