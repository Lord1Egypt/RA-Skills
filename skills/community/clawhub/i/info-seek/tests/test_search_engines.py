#!/usr/bin/env python3
"""Infoseek v1.1.0 搜索链测试（并行合并 + 质量门控 + 动态保留）

验证（无网络依赖，monkeypatch 引擎函数）：
  - 并行合并：url 去重 / 组间权重/组内保序 / top-N
  - 质量门控：结果不足触发保留引擎兜底
  - 动态保留：md5 轮换 / 默认模式保留池=限量引擎（配额保护）
  - AI 模式：AI 层优先 / 保留池=免费引擎 / 回退默认层
  - 顺序回退：INFOSEEK_SEARCH_PARALLEL=0
  - CN 兜底：默认关闭 / opt-in 生效
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

# v1.8.2 测试隔离：禁用平台 WebSearch 引擎注册（防 WorkBuddy sidecar 自动
# spawn 真实抓取污染 stub 场景；环境重置会回滚历史隔离，故内联固化为默认值）
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')

import infoseek_pipeline as p

# v1.2.x 环境隔离：避免 ~/.infoseek/engine_state.json 历史禁用状态（如真实搜索
# 超时写入的 DDG/Jina fail_count=3）污染测试结果（get_active 过滤导致断言失真）
os.environ['INFOSEEK_DATA_DIR'] = tempfile.mkdtemp(prefix='tse_')
import engine_lifecycle as el
el.reset_instance()

passed, failed = 0, 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  [PASS] {name} {detail}")
    else:
        failed += 1
        print(f"  [FAIL] {name} {detail}")


def reset_env():
    for k in ('INFOSEEK_SEARCH_ENGINE', 'INFOSEEK_SEARCH_PARALLEL',
              'INFOSEEK_SEARCH_RESERVED', 'INFOSEEK_RESERVE_QUOTA',
              'INFOSEEK_SEARCH_MIN_RESULTS', 'INFOSEEK_CN_AI_SEARCH',
              'EXA_API_KEY', 'TAVILY_API_KEY', 'TINYFISH_API_KEY',
              'ZHIPU_API_KEY', 'METASO_API_KEY'):
        os.environ.pop(k, None)


def stub_engines():
    """免费引擎 stub：DDG 2 条、Bing 2 条（与 DDG 重叠 1）、Jina 1 条、Wiki 空。"""
    p._search_duckduckgo_html = lambda q, m=10: [
        {'url': 'https://a.com', 'title': '测试 DDG 结果', 'snippet': ''},
        {'url': 'https://b.com', 'title': 'B-DDG', 'snippet': ''}]
    p._search_bing_rss = lambda q, m=10: [
        {'url': 'https://b.com', 'title': '测试 BING 结果', 'snippet': ''},
        {'url': 'https://c.com', 'title': '测试 BING 结果', 'snippet': ''}]
    p._search_jina = lambda q, m=5: [
        {'url': 'https://d.com', 'title': '测试 JINA 结果', 'snippet': ''}]
    p._search_wikipedia = lambda q, m=10: []
    # AI 引擎 stub：Exa/Tavily/智谱/秘塔/TinyFish
    p._search_exa = lambda q, m=5: [{'url': 'https://e.com', 'title': '测试 EXA 结果', 'snippet': ''}]
    p._search_tavily = lambda q, m=5: []
    p._search_zhipu = lambda q, m=5: [{'url': 'https://z.com', 'title': '测试 ZHIPU 结果', 'snippet': ''}]
    p._search_metaso = lambda q, m=5: []
    p._search_tinyfish = lambda q, m=5: []


print("=" * 70)
print("v1.1.0 搜索链测试（并行合并 + 质量门控 + 动态保留）")
print("=" * 70)

# ── 1. 并行合并：去重 + 组间权重/组内保序 ──
reset_env()
stub_engines()
r = p._parallel_merge(p._default_layer(), '测试', 10)
urls = [x['url'] for x in r]
check("并行合并去重", len(urls) == len(set(urls)), f"{urls}")
check("组间权重序（DDG 1.0 优先）", urls[0] == 'https://a.com', f"{urls}")
check("组内保序（DDG 的 a,b 连续）",
      urls.index('https://a.com') + 1 == urls.index('https://b.com'), f"{urls}")

# ── 2. top-N 截断 ──
r2 = p._parallel_merge(p._default_layer(), '测试', 2)
check("top-N 截断", len(r2) == 2, f"len={len(r2)}")

# ── 3. 质量门控触发保留兜底（默认模式：保留池=限量引擎） ──
reset_env()
stub_engines()
os.environ['ZHIPU_API_KEY'] = 'k'          # 智谱限量引擎已配 key
# 主并行免费引擎只返回 1 条（< min_expected=3）→ 触发智谱兜底
p._search_duckduckgo_html = lambda q, m=10: [{'url': 'https://a.com', 'title': '测试 A 结果', 'snippet': ''}]
p._search_bing_rss = lambda q, m=10: []
p._search_jina = lambda q, m=5: []
r = p.search_web('测试')
check("质量门控触发智谱兜底", any('https://z.com' in x['url'] for x in r),
      f"{[x['url'] for x in r]}")

# ── 4. 结果充足不触发兜底（配额保护） ──
reset_env()
stub_engines()
os.environ['ZHIPU_API_KEY'] = 'k'
r = p.search_web('测试')
check("结果充足不触发兜底（配额保护）", not any('https://z.com' in x['url'] for x in r),
      f"{[x['url'] for x in r]}")

# ── 5. 动态保留轮换（不同查询保留不同限量引擎） ──
reset_env()
stub_engines()
os.environ['EXA_API_KEY'] = 'k'
os.environ['ZHIPU_API_KEY'] = 'k'
pool = p._reserve_pool(False, p._default_layer())
import hashlib
names = set()
for q in ('主题A', '主题B', '主题C', '主题D'):
    idx = int(hashlib.md5(q.encode()).hexdigest(), 16) % len(pool)
    names.add(pool[idx][0])
check("保留池=限量引擎", all(n in ('Exa', 'Zhipu') for n, _ in pool), f"{[n for n,_ in pool]}")
check("池内轮换多引擎", len(names) >= 2, f"{sorted(names)}")

# ── 6. AI 模式：AI 层优先 + 保留池=免费引擎 ──
reset_env()
stub_engines()
os.environ['INFOSEEK_SEARCH_ENGINE'] = 'ai'
os.environ['EXA_API_KEY'] = 'k'
pool_ai = p._reserve_pool(True, p._ai_engines() + p._free_engines())
check("AI 模式保留池=免费引擎", all(n in ('DuckDuckGo-HTML', 'Bing-RSS', 'Jina-AI', 'Wikipedia')
                                  for n, _ in pool_ai), f"{[n for n,_ in pool_ai]}")
r = p.search_web('测试')
check("AI 模式返回合并结果", len(r) >= 3, f"len={len(r)}")

# ── 7. 固定保留 env ──
reset_env()
stub_engines()
os.environ['INFOSEEK_SEARCH_RESERVED'] = 'Wikipedia'
pool_f = p._reserve_pool(False, p._default_layer())
check("RESERVED 固定保留", [n for n, _ in pool_f] == ['Wikipedia'], f"{[n for n,_ in pool_f]}")

# ── 8. RESERVE_QUOTA=0 关闭配额保护（全池轮换） ──
reset_env()
stub_engines()
os.environ['INFOSEEK_RESERVE_QUOTA'] = '0'
pool_q = p._reserve_pool(False, p._default_layer())
check("RESERVE_QUOTA=0 全池轮换", len(pool_q) == len(p._default_layer()),
      f"len={len(pool_q)}")

# ── 9. 顺序回退 PARALLEL=0 ──
reset_env()
stub_engines()
os.environ['INFOSEEK_SEARCH_PARALLEL'] = '0'
p._search_duckduckgo_html = lambda q, m=10: [{'url': 'https://serial.com', 'title': '测试 S 结果', 'snippet': ''}]
r = p.search_web('测试')
check("PARALLEL=0 顺序回退", r and r[0]['url'] == 'https://serial.com', f"{[x['url'] for x in r]}")

# ── 10. CN 网页兜底：默认关闭 / opt-in 生效 ──
reset_env()
check("CN 兜底默认关闭", p._search_cn_web('测试') == [])
os.environ['INFOSEEK_CN_AI_SEARCH'] = '1'
_html = ('<html><head><title>360AI搜-测试</title>'
         '<meta name="description" content="摘要"></head></html>').encode('utf-8')
p._http_get = lambda url, timeout=10: _html
import net_probe as _np_for_cn
_real_chk = _np_for_cn.check_hosts
_np_for_cn.check_hosts = lambda hosts, timeout=2.0, **k: {h: {'host': h, 'ok': True, 'elapsed': 0.001, 'err': ''} for h in hosts}
r = p._search_cn_web('测试', 1)
_np_for_cn.check_hosts = _real_chk
check("CN 兜底 opt-in 生效", r and '360AI搜' in r[0]['title'], f"{r[0]['title'][:16] if r else '空'}")
reset_env()

# ── 11. 全失败返回 []（不伪造） ──
reset_env()
stub_engines()
p._search_duckduckgo_html = lambda q, m=10: []
p._search_bing_rss = lambda q, m=10: []
p._search_jina = lambda q, m=5: []
p._search_wikipedia = lambda q, m=10: []
r = p.search_web('测试')
check("全失败返回空（不伪造）", r == [], f"{r}")

reset_env()
print("\n" + "=" * 70)
print(f"v1.1.0 搜索链: {passed} PASS / {failed} FAIL")
print("=" * 70)
if failed:
    print("❌ 存在失败")
    sys.exit(1)
print("✅ 并行合并 + 质量门控 + 动态保留验证通过")
