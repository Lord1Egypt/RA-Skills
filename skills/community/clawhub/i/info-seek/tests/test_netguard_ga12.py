#!/usr/bin/env python3
"""Infoseek GA12 守护：net_probe 正负分 TTL/SWR 缓存 + CN-AI-Web 薄壳三门控。

历史口径（CHANGELOG [2.4.1] 及 GA12 netguard）：
  第 1 部分 net_probe（37 断言）：host 规整、正项 600s/负项 30s 分 TTL、
    正项 SWR 陈旧立返+后台重验、负项不做 SWR、force 关键字探测、探测异常
    fail-open（ok=None 而非 False）、空批量返 {}、磁盘缓存读写与卷容裁剪。
  第 2 部分 TH 薄壳（9 断言，2.4.1 新增）：_is_thin_home 三重防误杀门 +
    _detect_cn_block 分层（静态只定 captcha/login，thin_home 延后 allow_thin）。
全离线、零真实网络（probe 底层全部 mock/桩）。
"""
import os
import sys
import time
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

for _k in [k for k in os.environ if k.startswith('INFOSEEK_')]:
    os.environ.pop(_k, None)

passed, failed = [], []


def ok(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  PASS {name} {extra}")
    else:
        failed.append(name); print(f"  FAIL {name} {extra}")


import net_probe as np  # noqa: E402
import infoseek_pipeline as p  # noqa: E402

# 隔离缓存：临时缓存文件 + 清内存
np.clear_disk_cache()
np.reset_cache()

print("\n═══ N 组 net_probe：规整与基础结构（零网络）═══")
ok("N1 _normalize_host 去 scheme/路径并小写",
   np._normalize_host('HTTPS://Example.COM/a/b?x=1') == 'example.com')
ok("N2 _normalize_host 去端口外空白", np._normalize_host('  cn.bing.com  ') == 'cn.bing.com')
ok("N3 _normalize_host 空串→''", np._normalize_host('') == '')
ok("N4 _env_int 合法值",
   (os.environ.update(INFOSEEK_NET_PROBE_TTL='123') or np._probe_ttl() == 123))
os.environ['INFOSEEK_NET_PROBE_TTL'] = 'abc'
ok("N5 _env_int 非法值回落默认", np._probe_ttl() == np._DEFAULT_TTL)
os.environ.pop('INFOSEEK_NET_PROBE_TTL', None)
ok("N6 默认正项 TTL=600", np._probe_ttl() == 600)
ok("N7 默认负项 TTL=30", np._probe_neg_ttl() == 30)
ok("N8 默认 SWR 窗口=3600", np._stale_ttl() == 3600)
ok("N9 env 负项 TTL 可调",
   (os.environ.update(INFOSEEK_NET_PROBE_NEG_TTL='15') or np._probe_neg_ttl() == 15))
os.environ.pop('INFOSEEK_NET_PROBE_NEG_TTL', None)
ok("N10 SWR=0 关闭陈旧窗口",
   (os.environ.update(INFOSEEK_NET_PROBE_STALE_TTL='0') or np._stale_ttl() == 0))
os.environ.pop('INFOSEEK_NET_PROBE_STALE_TTL', None)

print("\n═══ N 组：分 TTL / SWR（注入缓存条目，零真实探测）═══")
now = time.time()
pos = {"host": "h-pos", "ok": True, "elapsed": 0.1, "err": "", "ts": now}
neg = {"host": "h-neg", "ok": False, "elapsed": 0.1, "err": "timeout", "ts": now}
unknown = {"host": "h-unk", "ok": None, "elapsed": 0.0, "err": "probe_error", "ts": now}
ok("N11 正项 TTL 取 600", np._entry_ttl(pos) == 600)
ok("N12 负项 TTL 取 30", np._entry_ttl(neg) == 30)
ok("N13 未知项(ok=None)走负项短 TTL", np._entry_ttl(unknown) == 30)
ok("N14 ttl override 优先", np._entry_ttl(pos, override=7) == 7)
ok("N15 正项新鲜（age=0）_stale_fresh=False（未过 TTL）",
   np._stale_fresh(pos, now) is False)
ok("N16 正项过 TTL 但在 SWR 窗口内 _stale_fresh=True",
   np._stale_fresh({**pos, "ts": now - 700}, now) is True)
ok("N17 正项超 SWR 窗口 _stale_fresh=False",
   np._stale_fresh({**pos, "ts": now - 5000}, now) is False)
ok("N18 负项永不 SWR（即使年龄落在窗口）",
   np._stale_fresh({**neg, "ts": now - 700}, now) is False)

print("\n═══ N 组：probe_host 缓存命中/过期/force ═══")
np.reset_cache(); np.clear_disk_cache()
np._MEM["fresh.com"] = {**pos, "host": "fresh.com", "ts": now}
with mock.patch.object(np, '_reach', return_value=(True, 0.2, '')) as m_reach:
    r = np.probe_host('fresh.com', timeout=1)
    ok("N19 TTL 内命中缓存 cached=True", r.get("cached") is True and m_reach.call_count == 0)
# 过期正项：非 force 且超 SWR → 真实重探
np._MEM["old-pos.com"] = {**pos, "host": "old-pos.com", "ts": now - 5000}
with mock.patch.object(np, '_reach', return_value=(True, 0.3, '')) as m_reach:
    r = np.probe_host('old-pos.com', timeout=1)
    ok("N20 过期正项超 SWR → 同步重探 cached=False",
       r.get("cached") is False and m_reach.call_count >= 1)
# force=True 关键字：忽略缓存强制探测
np._MEM["force.com"] = {**pos, "host": "force.com", "ts": now}
with mock.patch.object(np, '_reach', return_value=(True, 0.4, '')) as m_reach:
    r = np.probe_host('force.com', timeout=1, force=True)
    ok("N21 force=True 忽略缓存强制探测",
       r.get("cached") is False and m_reach.call_count >= 1)
# SWR：陈旧正项立返 stale=True 且后台重验
np._MEM["swr.com"] = {**pos, "host": "swr.com", "ts": now - 700}
with mock.patch.object(np, '_revalidate_async') as m_rev, \
     mock.patch.object(np, '_reach') as m_reach:
    r = np.probe_host('swr.com', timeout=1)
    ok("N22 正项 SWR 立返 cached=True/stale=True",
       r.get("cached") is True and r.get("stale") is True)
    ok("N23 SWR 触发后台异步重验", m_rev.call_count == 1)
    ok("N24 SWR 立返路径不做同步探测", m_reach.call_count == 0)

print("\n═══ N 组：check_hosts 批量与 fail-open ═══")
ok("N25 空 host 列表返 {}", np.check_hosts([]) == {})
ok("N26 全空白/非法 host 返 {}", np.check_hosts(['', '   ']) == {})
# 全部缓存命中不起线程
np.reset_cache()
np._MEM["a.com"] = {**pos, "host": "a.com", "ts": now}
np._MEM["b.com"] = {**pos, "host": "b.com", "ts": now}
batch = np.check_hosts(['https://a.com/x', 'b.com'], timeout=1)
ok("N27 批量规整去重且命中缓存",
    set(batch.keys()) == {'a.com', 'b.com'}
    and all(v.get('cached') for v in batch.values()))
# miss 且探测成功
np.reset_cache()
with mock.patch.object(np, 'probe_host',
                       return_value={"host": "new.com", "ok": True, "elapsed": 0.1,
                                     "err": "", "ts": now, "cached": False}) as m_ph:
    batch = np.check_hosts(['new.com'], timeout=1)
    ok("N28 miss 时调用 probe_host 并收录",
       m_ph.call_count == 1 and batch['new.com']['ok'] is True)
# 探测抛异常 → fail-open ok=None（不是 False）
np.reset_cache()
def _boom(*a, **k):
    raise RuntimeError("simulated probe crash")
with mock.patch.object(np, 'probe_host', side_effect=_boom):
    batch = np.check_hosts(['crash.com'], timeout=1)
ok("N29 探测异常 fail-open：ok=None（非 False），不炸调用方",
   batch['crash.com']['ok'] is None)
ok("N30 fail-open 条目带 err 前缀 probe_error",
   str(batch['crash.com'].get('err', '')).startswith('probe_error'))
# force 关键字透传到 ThreadPoolExecutor 提交（GA12 根因回归：位置传参 TypeError）
np.reset_cache()
with mock.patch.object(np, 'probe_host',
                       return_value={"host": "f.com", "ok": True, "elapsed": 0.1,
                                     "err": "", "ts": now, "cached": False}) as m_ph:
    np.check_hosts(['f.com'], timeout=1, force=True)
    ok("N31 check_hosts(force=True) 以 force 关键字透传 probe_host",
       m_ph.call_args.kwargs.get('force') is True)

print("\n═══ N 组：磁盘缓存 ═══")
np.clear_disk_cache()
np._save_disk("disk.com", {**pos, "host": "disk.com"})
ok("N32 _save_disk 后 _load_disk 可读回", np._load_disk().get("disk.com", {}).get("ok") is True)
# 卷容裁剪：写 >200 条只留最近 200
np.clear_disk_cache()
for i in range(205):
    np._save_disk(f"h{i:03d}.com", {"host": f"h{i:03d}.com", "ok": True,
                                    "elapsed": 0.0, "err": "", "ts": now + i})
disk = np._load_disk()
ok("N33 磁盘缓存卷容裁剪至 ≤200 条", len(disk) == 200)
ok("N34 裁剪保留最新（h204 留、h000 弃）",
   "h204.com" in disk and "h000.com" not in disk)
np.reset_cache(); np.clear_disk_cache()
ok("N35 reset_cache 清空内存", np._MEM == {})
ok("N36 clear_disk_cache 后磁盘为空", np._load_disk() == {})
ok("N37 空 host probe_host 返 ok=False 不抛",
   np.probe_host('')['ok'] is False)

print("\n═══ TH 组：薄壳三门控（2.4.1 新增 9 断言）═══")
ok("TH1 品牌强壳词标题命中即判（正文可长）",
   p._is_thin_home('Kimi 智能体先行者', '', '欢迎体验' * 100, '板栗价格') is True)
ok("TH2 通用官网词 + 短正文（<600）判薄壳",
   p._is_thin_home('天工官网', 'AI助手', '你好世界', '板栗') is True)
ok("TH3 通用官网词但正文≥600 不判（防误杀长内容）",
   p._is_thin_home('天工官网', '', 'x' * 700, '板栗') is False)
ok("TH4 门1：title/desc 回显查询词 → 结果页不判",
   p._is_thin_home('板栗价格_官网', '板栗价格最新报价', '', '板栗价格') is False)
ok("TH5 门2：正文含搜索结果列表结构词不判",
   p._is_thin_home('某官网首页', '', '为您推荐 相关搜索 共找到100条结果', '板栗') is False)
ok("TH6 空标题不判", p._is_thin_home('', 'x', 'y') is False)
ok("TH7 静态阶段 allow_thin=False 只定 captcha/login，不定 thin_home",
   p._detect_cn_block('天工官网', 'AI', '短正文', allow_thin=False) == '')
ok("TH8 渲染后 allow_thin=True 对最终页补判 thin_home",
   p._detect_cn_block('天工官网', 'AI', '短正文', allow_thin=True) == 'thin_home')
ok("TH9 captcha/login 静态即可定，优先级高于 thin_home",
   p._detect_cn_block('请登录 官网首页', '', '短', allow_thin=False) == 'login'
   and p._detect_cn_block('请完成滑块验证码 官网', '', '短') == 'captcha')

print(f"\ntest_netguard_ga12: {len(passed)} PASS / {len(failed)} FAIL（目标 46 断言）")
if failed:
    print("未通过：" + ", ".join(failed))
    sys.exit(1)
print("ALL GREEN")
