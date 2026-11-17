#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEPRECATED] 旧 Orchestrator — 请使用 application/orchestrator.py 的 ChapterOrchestrator.

此文件保留用于向后兼容。Orchestrator 类仍然可用，但建议新代码使用 ChapterOrchestrator。
check_providers_available 函数已内联到 run.py。
"""

import os, sys, re, json, argparse
from pathlib import Path
import warnings as _warnings
_warnings.warn(
    "engine.orchestrator is deprecated. Use application.orchestrator.ChapterOrchestrator instead.",
    DeprecationWarning, stacklevel=2
)
from datetime import datetime
from engine.spec_builder import SpecBuilder
from engine.log import info, warn, error as log_error
from engine.circuit_breaker import CircuitBreaker
import logging
_log = logging.getLogger("orchestrator")
from engine.checkpoint_manager import CheckpointManager
from copy import deepcopy

def lazy_import(module_name):
    if module_name not in sys.modules:
        __import__(module_name)
    return sys.modules[module_name]

FAIL_TAGS = ["(生成失败)", "[TEMPLATE_FALLBACK]", "(生成失败:", "(模板参数缺失:", "(未知任务:"]
SKIP_NAMES = {"说","问","喊","叫","骂","答","应","听","胡","说",
    "不要","不能","可以","应该","需要","这么","那么","怎么","什么","因为","所以","如果",
    "不知","知道","笑道","说明","告诉","解释","回答","补充","提醒","警告","威胁",
    "理解","同意","反对","坚持","重复","强调","安慰","鼓励","催促",
    "追问","质问","审问","盘问","反问","提问","试问","笑问","自问","发问",
}
BAD_NAME_ADVS = {"不要","不能","可以","应该","需要","这么","那么","怎么","什么","因为","所以","如果","而且",
    "不知","知道","笑道","告诉","解释","回答","重复","强调","说明","安慰","鼓励"}

def check_providers_available(generator):
    """检查是否有可用的 LLM provider（不含 TemplateProvider）。返回 True/False。"""
    provider_details = []
    has_real_provider = False
    providers = getattr(generator, '_providers', [])
    if not providers:
        return False
    for name, p in providers:
        pname = p.__class__.__name__
        try:
            pavail = p.available()
        except Exception:
            pavail = False
        # TemplateProvider check: last provider is typically the fallback template
        last_provider = providers[-1][1] if providers else None
        is_template = last_provider is not None and isinstance(p, type(last_provider))
        provider_details.append(f"{pname}: {'available' if pavail else 'unavailable'}{'(template)' if is_template else ''}")
        if pavail and not is_template:
            has_real_provider = True
    if not has_real_provider:
        details = ", ".join(provider_details)
        log_error("orchestrator", f"没有可用的 LLM provider。详情: {details}")
        print(f"  [ERROR] 没有可用的 LLM provider。详情: {details}")
        print("    -> 请安装 Ollama (ollama run qwen3:1.7b) 或配置 OpenClaw Gateway token")
        return False
    return True



class Orchestrator:
    def __init__(self, book_dir, platform="番茄", genre="都市",
                 total_chapters=50, api_key="", local_mode=True, novel_state=None):
        self.book_dir = Path(book_dir); self.platform = platform; self.genre = genre
        self.total_chapters = total_chapters; self.api_key = api_key; self.local_mode = local_mode
        self.state = novel_state; self._init_state()
        self._generator = None; self._detector = None; self._planning = None; self._cb = CircuitBreaker()
        self._guard_enabled = True

    def _init_state(self):
        if self.state is not None:
            m = self.state.meta
        else:
            ns = lazy_import("engine.novel_state")
            self.state = ns.NovelState(str(self.book_dir))
            m = self.state.meta
        m["platform"] = self.platform; m["genre"] = self.genre; m["total_chapters"] = self.total_chapters
        self.state.save()

    @property
    def generator(self):
        if self._generator is None:
            g = lazy_import("engine.generator"); self._generator = g.TextGenerator()
        return self._generator

    @property
    def planning(self):
        if self._planning is None:
            from engine.engines_planning import PlanningEngine
            self._planning = PlanningEngine()
        return self._planning

    @property
    def detector(self):
        if self._detector is None:
            d = lazy_import("engine.detector_wrapper"); self._detector = d.DetectorWrapper()
        return self._detector

    def _get_style_lock(self):
        return self.generator.style_lock(self.platform)

    def run(self, start=1):
        """执行章节生成流程"""
        # 输入校验
        start = int(start) if not isinstance(start, int) else start
        if start < 1:
            _log.error(f"orchestrator: 无效的起始章节 {start}，使用 1")
            start = 1
        if not isinstance(start, (int, float)) or start < 1:
            import logging as _l
            _l.error("orchestrator", f"run() start={start} invalid, use next_chapter()")
            print(f"  [ERROR] run() start={start} invalid, use next_chapter()")
            start = self.state.next_chapter()
        elif isinstance(start, float):
            start = int(start)
        ch = max(int(start), self.state.next_chapter())
        already = self.state.written_chapters()
        if ch <= already:
            ch = already + 1
            info("orchestrator", f"已完成{already}章,从第{ch}章开始")
        start_ch = start
        print("\n" + "=" * 50)
        print("\n" + "=" * 50)
        info("orchestrator", f"启动: {self.platform}/{self.genre}  {self.total_chapters}章")
        info("orchestrator", f"目录: {self.book_dir}")
        info("orchestrator", f"时间: {datetime.now().strftime("%H:%M:%S")}")
        print("\n" + "=" * 50)

        if not check_providers_available(self.generator):
            return

        # 创建 GenerationPipeline 实例，委托核心生成管线
        # 注入 _update_state_in_hook 使追踪更新在 UoW 事务内执行
        from engine.pipeline import GenerationPipeline
        pipeline = GenerationPipeline(
            self.generator, self.detector, self.planning,
            self.state, str(self.book_dir),
            auto_correct_fn=self.auto_correct
        )

        error_count = 0
        start_time = datetime.now()

        # Forced rollback guard — reload state on unhandled exception
        _guard_enabled = True
        try:
            if self._guard_enabled:
                _log.debug('Rollback guard active')
        except AttributeError:
            pass

        while ch <= self.total_chapters:
            info("orchestrator", f"--- 第 {ch} 章 ---")
            # Idempotent skip
            from engine.circuit_breaker import check_idempotent_chapter
            if not check_idempotent_chapter(self.state, ch):
                ch += 1
                continue
            _cp = CheckpointManager(str(self.book_dir))
            _cp.snapshot(ch)

            pct = ch * 100 // self.total_chapters
            elapsed_est = (datetime.now() - start_time).total_seconds() * self.total_chapters / max(ch - start_ch, 1)
            print(f"  [{ch}/{self.total_chapters}] 第{ch}章 ({pct}%, 预计{elapsed_est:.0f}s)")
            print("  [生成/检测/写入]...")
            style = self._get_style_lock()

            try:
                # 委托给 GenerationPipeline.run_chapter()——包含完整的规划→规格→生成→检测→重写→持久化
                result = pipeline.run_chapter(
                    ch, self.total_chapters, self.platform, self.genre,
                    style_lock=style
                )

                if not result["success"]:
                    log_error("orchestrator", f"第{ch}章生成失败: {result.get('error', 'unknown')}")
                    error_count += 1
                    ch += 1
                    continue

                text = result["text"]
                print(f"  [写入] 第{ch:03d}章.txt ({len(text)}字)")
                if result.get("issues"):
                    print(f"  [质量] {result['classification']} | {len(result['issues'])} 问题 | 重写{result.get('rewrite_count',0)}次")

                # 追踪文件由本层在 pipeline 返回后补写
                self._update_state_in_hook(ch, text, self.state, None)
                self.state.save()  # 持久化 _apply_state_modifications 的内存变更
                # 一致性检查 每 10 章（只读，不需要 UoW）
                if ch % 10 == 0:
                    cs_issues = self._check_consistency()
                    if cs_issues:
                        print(f"  [一致性] {len(cs_issues)} 个问题:")
                        for ci in cs_issues[:5]:
                            print(f"    - {ci}")
                        if len(cs_issues) > 5:
                            print(f"    ...及其他 {len(cs_issues)-5} 个问题")
                # 架构节奏分析 每 10 章
                if ch % 10 == 0:
                    try:
                        from .engines_architecture import ArchitectureEngine
                        rhythm = ArchitectureEngine.calc_rhythm(ch, self.total_chapters)
                        if rhythm:
                            rhythm_str = str(rhythm) if isinstance(rhythm, str) else str(rhythm)
                            print(f"  [节奏] 第{ch}/{self.total_chapters}章: {rhythm_str[:60]}")
                    except Exception as _are:
                        pass
                    # 读者模拟 每 10 章
                    try:
                        from .simulation import SimulationEngine
                        sim = SimulationEngine.simulate_reader(ch, text, 0.7)
                        if sim and isinstance(sim, dict):
                            eng = sim.get("engagement", 0)
                            if isinstance(eng, (int, float)) and eng < 0.4:
                                print(f"  [模拟] 读者参与度 {eng:.2f} - 建议增强本章吸引力")
                    except Exception as _sme:
                        pass
                    # 发展引擎节奏审查 每 10 章
                    try:
                        from .engines_development import DevelopmentEngine
                        # 收集最近10章数据（仅元信息，非全文）
                        recent_chs = [c for c in range(max(1, ch-9), ch+1)]
                        pacing_issues = DevelopmentEngine.validate_pacing(recent_chs, [])
                        if pacing_issues:
                            for pi in (pacing_issues if isinstance(pacing_issues, list) else [str(pacing_issues)]):
                                if pi:
                                    print(f"  [节奏] {pi}")
                    except Exception as _dve:
                        pass
                ch += 1
            except Exception as _ch_err:
                log_error("orchestrator", f"第{ch}章异常: {_ch_err}，回滚状态")
                try:
                    _cp.rollback(ch)
                    self.state.rollback_state()
                except Exception as _rb_err:
                    log_error("orchestrator", f"Checkpoint 回滚失败: {_rb_err}")
                error_count += 1

        # Sync state from disk after batch to fix multi-engine drift
        try:
            from engine.compat import force_reload_from_disk, force_reset_engine_caches
            force_reload_from_disk(self.state)
        except Exception as _sync_e:
            info("orchestrator", f"state sync skipped: {_sync_e}")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n完成：{ch-start_ch}章（耗时{elapsed:.0f}秒，{error_count}个错误）\n")
        return {"chapters_written": ch - start_ch, "errors": error_count, "elapsed": elapsed}

    def _update_tracker_files(self, ch, uow=None):
        """更新追踪文件——通过 ChapterTransaction 进行幂等写入"""
        try:
            from .chapter_transaction import ChapterTransaction
            with ChapterTransaction(str(self.book_dir), self.state, ch) as txn:
                from detectors.update_tracker import read_spec
                sp = Path(str(self.book_dir)) / "规格" / f"第{ch:03d}章.json"
                if not sp.exists():
                    return
                spec = read_spec(sp)
                tracker_dir = Path(str(self.book_dir)) / "追踪"
                if not tracker_dir.exists():
                    return
                ch_label = f"#{ch:03d}"
                for char in spec.get("after_chars", []):
                    name = char["name"].partition("（")[0]
                    if char.get("location"):
                        txn.update_tracker(
                            f"追踪/角色状态.md",
                            f"## {name}",
                            f"- {name}: 位置变为 {char['location']} ({ch_label})"
                        )
                for hook in spec.get("new_hooks", []):
                    txn.update_tracker(
                        f"追踪/伏笔.md",
                        hook[:30] if isinstance(hook, str) else str(hook)[:30],
                        f"- 新伏笔: {hook} ({ch_label})" if isinstance(hook, str) else f"- 新伏笔: {str(hook)[:100]} ({ch_label})"
                    )
        except Exception as _te:
            _log.warning(f"追踪文件更新失败: {_te}")

    def _update_state_in_hook(self, ch, text, state, uow):
        """统一状态更新入口：角色提取 + 阅读率/时间线 + 追踪文件"""
        # 1. 角色提取
        known = set(self.state.all_characters().keys())
        for m in re.finditer(r"([一-鿿㐀-䶿]{1,6})(?:道|说|问|喊|叫|骂|答|等)[：:？?]", text):
            name = m.group(1)
            if name not in known and name not in BAD_NAME_ADVS and name not in SKIP_NAMES:
                known.add(name)
                self.state.set_character(name, {"state": "出场", "location": "未知"})
        # 2. 阅读率 + 时间线
        wc = len(text)
        self.state.update_readers(engagement=max(0.3, min(1.0, wc / 2500) * 0.9))
        self.state.add_timeline_event(ch, f"第{ch}章完成，{wc}字")
        # 3. 追踪文件
        self._update_tracker_files(ch, uow=uow)

    def _check_consistency(self):
        issues = []
        tf = Path(self.book_dir) / "追踪" / "角色状态.md"
        if not tf.exists(): return []
        try:
            st = tf.read_text(encoding="utf-8", errors="replace")
            td = Path(self.book_dir) / "正文"
            if not td.exists(): return []
            for cf in sorted(td.glob("第*.txt"))[-3:]:
                ct = cf.read_text(encoding="utf-8", errors="replace")[:1000]
                for l in st.split("\n"):
                    if l.startswith("## "):
                        n = l[3:].partition("：")[0].strip()
                        if n and n not in ct and len(n) >= 2:
                            issues.append(f"'{n}' 在角色状态md中但不在最近3章正文中")
                for m in re.finditer(r"([\u4e00-\u9fff]{2,3})(?:道|说|问)[：:]", ct):
                    n = m.group(1)
                    if n not in st and n not in SKIP_NAMES and n not in BAD_NAME_ADVS and n not in st:
                        issues.append(f"'{n}' 在正文说话但不在角色状态md中")
        except Exception as e:
            issues.append(f"一致性扫描异常: {e}")
        return issues

    def auto_correct(self, text, ch=1, max_retries=2):
        if not text: return text
        try:
            bd = Path(self.book_dir) / "_backup"; bd.mkdir(parents=True, exist_ok=True)
            (bd / f"ch{ch:03d}.original.txt").write_text(text, encoding="utf-8")
        except Exception as _e:
            log_error("orchestrator", f"备份写入失败: {_e}")
        try:
            from detectors.run_all_detectors import BANNED_P0, BANNED_ENDINGS
        except ImportError:
            BANNED_P0 = ["毋庸置疑","不可否认","值得一提的是","总而言之","众所周知","命运的齿轮","从某种意义上说","在某种程度上","由此可见","综上所述","不可忽视的是"]
            BANNED_ENDINGS = ["他终于明白了","她终于懂了","他不知道的是","更大的挑战还在后面","总的来说"]
        from engine.engines_utils import build_quote_mask
        fixed_text = text; issues = []; in_quote = build_quote_mask(fixed_text)
        for w in BANNED_P0:
            wlen = len(w)
            if fixed_text.count(w) == 0: continue
            deleted = 0; buf = []; i = 0
            while i < len(fixed_text):
                pos = fixed_text.find(w, i)
                if pos == -1 or pos > len(fixed_text) - wlen:
                    buf.append(fixed_text[i:]); break
                if pos > i: buf.append(fixed_text[i:pos])
                if not any(in_quote[pos:pos + wlen]):
                    deleted += 1; buf.append("")
                else: buf.append(w)
                i = pos + wlen
            fixed_text = "".join(buf)
            if deleted > 0: issues.append(f"P0'{w}'x{deleted}(已删除)")
        if len(fixed_text) >= 200:
            tail = fixed_text[max(0, len(fixed_text) - 300):]
            for ending in BANNED_ENDINGS:
                epos = tail.find(ending)
                if epos != -1:
                    ap = max(0, len(fixed_text) - 300) + epos
                    fixed_text = fixed_text[:ap] + f"[P0_FLAGGED: {ending}]" + fixed_text[ap + len(ending):]
                    issues.append(f"P0结尾'{ending}' -> [P0_FLAGGED]")
        if issues:
            print(f"  [auto_correct] 修正 {len(issues)} 个P0问题:")
            for iss in issues: print(f"    - {iss}")
        return fixed_text
