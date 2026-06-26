#!/usr/bin/env python3
"""
LLMCommand - CLI Integration for the LLM subsystem

Implements Phase 6 commands (PLAN_LLM_INTEGRATION.md):

  kb llm status                                — LLM-System Status
  kb llm generate essence <topic>              — Manuelle Essenz-Erstellung
    Option: --source-files für spezifische Quellen
    Option: --batch für mehrere Themen
  kb llm generate report <daily|weekly|monthly> — Manuelle Report-Erstellung
  kb llm watch start|stop|status               — File-Watcher Steuerung
  kb llm scheduler start|stop|list|trigger <job> — Scheduler Steuerung
  kb llm list essences                         — Liste alle Essenzen
    Option: --topic-filter
    Option: --date-range
  kb llm list reports                          — Liste alle Reports
  kb llm config [show|set <key> <value>]       — Zeigt/Aktualisiert LLM-Config
  kb llm engine status                         — Engine-Status (beide Engines)
  kb llm engine switch <ollama|huggingface|auto|compare> — Model-Source wechseln
  kb llm engine test                          — Kurzer Test beider Engines

Design:
  - Nested sub-subparsers for `kb llm <subcommand> [sub-subcommand]`
  - Async methods bridged via asyncio.run() in _execute()
  - Progress spinners for long operations
  - Exit codes: 0=success, 1=validation, 2=execution
  - Skips DB validation (LLM commands don't need KB SQLite)
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

from kb.base.command import BaseCommand
from kb.commands import register_command


# ─── Helpers ────────────────────────────────────────────────────────────────

def _run_async(coro):
    """Run an async coroutine from sync context, handling existing loops."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)


class ProgressSpinner:
    """Simple stderr spinner for long-running CLI operations."""

    FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")

    def __init__(self, message: str = "", enabled: bool = True):
        self._message = message
        self._enabled = enabled
        self._idx = 0

    def update(self, message: Optional[str] = None):
        if not self._enabled:
            return
        if message is not None:
            self._message = message
        frame = self.FRAMES[self._idx % len(self.FRAMES)]
        self._idx += 1
        sys.stderr.write(f"\r  {frame} {self._message}")
        sys.stderr.flush()

    def finish(self, message: str = ""):
        if not self._enabled:
            return
        if message:
            sys.stderr.write(f"\r  ✓ {message}\n")
        else:
            sys.stderr.write("\r" + " " * 60 + "\r")
        sys.stderr.flush()


def _fmt_essence(e: dict) -> str:
    """Format a single essence for display."""
    title = e.get("title", "Unbenannt")
    h = e.get("hash", "?")[:8]
    at = e.get("extracted_at", "—")[:19]
    model = e.get("model", "?")
    return f"  [{h}]  {title}  ({model}, {at})"


def _fmt_report(r: dict) -> str:
    """Format a single report for display."""
    title = r.get("title", "Unbenannt")
    rtype = r.get("report_type", "?")
    at = r.get("generated_at", "—")[:19]
    sources = r.get("sources_count", 0)
    return f"  [{rtype:7s}]  {title}  ({sources} Quellen, {at})"


def _parse_date_range(date_range: str):
    """Parse date range like '2026-04-01..2026-04-15' or '2026-04-01'."""
    start_dt = None
    end_dt = None
    if ".." in date_range:
        parts = date_range.split("..", 1)
        try:
            start_dt = datetime.fromisoformat(parts[0]).replace(tzinfo=timezone.utc)
        except (ValueError, IndexError):
            pass
        try:
            end_dt = datetime.fromisoformat(parts[1]).replace(tzinfo=timezone.utc)
        except (ValueError, IndexError):
            pass
    else:
        try:
            start_dt = datetime.fromisoformat(date_range).replace(tzinfo=timezone.utc)
            end_dt = start_dt + timedelta(days=1)
        except ValueError:
            pass
    return start_dt, end_dt


# Mutable config keys with expected types
_MUTABLE_CONFIG_KEYS = {
    "model": str,
    "ollama_url": str,
    "timeout": int,
    "temperature": float,
    "max_tokens": int,
    "batch_size": int,
    "max_retries": int,
    "retry_delay": float,
    "model_source": str,
    "parallel_mode": bool,
    "parallel_strategy": str,
    "ollama_model": str,
    "ollama_timeout": int,
    "ollama_temperature": float,
}

_CONFIG_KEY_TO_ENV = {
    "model": "KB_LLM_MODEL",
    "ollama_url": "KB_LLM_OLLAMA_URL",
    "timeout": "KB_LLM_TIMEOUT",
    "temperature": "KB_LLM_TEMPERATURE",
    "max_tokens": "KB_LLM_MAX_TOKENS",
    "batch_size": "KB_LLM_BATCH_SIZE",
    "max_retries": "KB_LLM_MAX_RETRIES",
    "retry_delay": "KB_LLM_RETRY_DELAY",
    "model_source": "KB_LLM_MODEL_SOURCE",
    "parallel_mode": "KB_LLM_PARALLEL_MODE",
    "parallel_strategy": "KB_LLM_PARALLEL_STRATEGY",
    "ollama_model": "KB_LLM_OLLAMA_MODEL",
    "ollama_timeout": "KB_LLM_OLLAMA_TIMEOUT",
    "ollama_temperature": "KB_LLM_OLLAMA_TEMPERATURE",
}


# ─── Command ────────────────────────────────────────────────────────────────

@register_command
class LLMCommand(BaseCommand):
    """CLI-Integration für das LLM-Modul (Essenzen, Reports, Watcher, Scheduler, Config)."""

    name = "llm"
    help = "LLM-Integration: Essenzen, Reports, Watcher, Scheduler, Config"

    # Skip DB validation — LLM commands don't need KB SQLite
    def validate(self, args) -> bool:
        return True

    # ─── Argument setup ─────────────────────────────────────────────

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        sub = parser.add_subparsers(
            dest="llm_action",
            title="LLM-Aktionen",
            description="Subcommands für das LLM-Subsystem",
        )

        self._add_status_parser(sub)
        self._add_generate_parsers(gen=sub)
        self._add_watch_parser(sub)
        self._add_scheduler_parser(sub)
        self._add_list_parsers(lst=sub)
        self._add_config_parser(cfg=sub)
        self._add_engine_parsers(eng=sub)

    # ─── Argument parsers ──────────────────────────────────────────

    def _add_status_parser(self, sub):
        sub.add_parser("status", help="LLM-Status: Modell, Jobs, letzte Essenzen")

    def _add_generate_parsers(self, parser: argparse.ArgumentParser):
        gen_sub = parser.add_subparsers(dest="generate_what", help="Was generieren?")
        self._add_essence_parser(gen_sub)
        self._add_report_parser(gen_sub)

    def _add_essence_parser(self, gen_sub):
        ess = gen_sub.add_parser("essence", help="Essenz für ein Thema generieren")
        ess.add_argument("topic", help="Thema der Essenz")
        ess.add_argument("--source-files", nargs="+", dest="source_files",
                         help="Spezifische Quell-Dateipfade")
        ess.add_argument("--batch", nargs="+", dest="batch_topics",
                         help="Mehrere Themen für Batch-Erstellung")

    def _add_report_parser(self, gen_sub):
        rep = gen_sub.add_parser("report", help="Report generieren")
        rep.add_argument("period", choices=["daily", "weekly", "monthly"],
                         help="Berichtszeitraum")

    def _add_watch_parser(self, sub):
        watch = sub.add_parser("watch", help="FileWatcher steuern")
        watch.add_argument("watch_action", choices=["start", "stop", "status"],
                          help="Aktion für den FileWatcher")

    def _add_scheduler_parser(self, sub):
        sched = sub.add_parser("scheduler", help="TaskScheduler steuern")
        sched.add_argument("scheduler_action", choices=["start", "stop", "list", "trigger"],
                          help="Aktion für den TaskScheduler")
        sched.add_argument("job", nargs="?", default=None, help="Job-ID für trigger")

    def _add_list_parsers(self, lst):
        lst_sub = lst.add_subparsers(dest="list_what", help="Was auflisten?")
        self._add_essences_list_parser(lst_sub)
        self._add_reports_list_parser(lst_sub)

    def _add_essences_list_parser(self, lst_sub):
        le = lst_sub.add_parser("essences", help="Alle Essenzen auflisten")
        le.add_argument("--topic-filter", help="Nach Thema filtern (Substring)")
        le.add_argument("--date-range", help="Datumsbereich (z.B. 2026-04-01..2026-04-15)")
        le.add_argument("--limit", type=int, default=50, help="Max Ergebnisse (Standard: 50)")
        le.add_argument("--json", action="store_true", dest="json_output", help="JSON-Ausgabe")

    def _add_reports_list_parser(self, lst_sub):
        lr = lst_sub.add_parser("reports", help="Alle Reports auflisten")
        lr.add_argument("--type", dest="report_type_filter",
                       choices=["daily", "weekly", "monthly"],
                       help="Nach Report-Typ filtern")
        lr.add_argument("--limit", type=int, default=50, help="Max Ergebnisse (Standard: 50)")
        lr.add_argument("--json", action="store_true", dest="json_output", help="JSON-Ausgabe")

    def _add_config_parser(self, cfg):
        cfg.add_argument("config_action", nargs="?", default="show",
                        choices=["show", "set"], help="Aktion (Standard: show)")
        cfg.add_argument("config_key", nargs="?", default=None, help="Config-Key (für set)")
        cfg.add_argument("config_value", nargs="?", default=None, help="Config-Value (für set)")

    def _add_engine_parsers(self, eng):
        eng_sub = eng.add_subparsers(dest="engine_action", title="Engine-Aktionen",
                                     description="Verfügbare Engine-Aktionen")
        eng_sub.add_parser("status", help="Status beider Engines und aktive model_source")
        self._add_engine_switch_parser(eng_sub)
        self._add_engine_test_parser(eng_sub)

    def _add_engine_switch_parser(self, eng_sub):
        eng_sw = eng_sub.add_parser("switch", help="Model-Source wechseln")
        eng_sw.add_argument("source", choices=["ollama", "huggingface", "auto", "compare"],
                           help="Neue model_source")

    def _add_engine_test_parser(self, eng_sub):
        eng_test = eng_sub.add_parser("test", help="Kurzer Test beider Engines")
        eng_test.add_argument("--prompt", default="Sag Hallo in einem Satz.",
                             help="Test-Prompt (Standard: Kurz-Begrüßung)")
        eng_test.add_argument("--max-tokens", type=int, default=50, dest="max_tokens",
                             help="Max Tokens für Test (Standard: 50)")

    # ─── Execution dispatch ────────────────────────────────────────

    def _execute(self) -> int:
        action = getattr(self._args, "llm_action", None)
        if not action:
            self.print_error("Keine Aktion angegeben. Siehe: kb llm --help")
            return self.EXIT_VALIDATION_ERROR

        dispatch = {
            "status": self._cmd_status,
            "generate": self._cmd_generate,
            "watch": self._cmd_watch,
            "scheduler": self._cmd_scheduler,
            "list": self._cmd_list,
            "config": self._cmd_config,
            "engine": self._cmd_engine,
        }

        handler = dispatch.get(action)
        if not handler:
            self.print_error(f"Unbekannte Aktion: {action}")
            return self.EXIT_VALIDATION_ERROR

        try:
            return handler()
        except (KeyboardInterrupt, SystemExit):
            self.get_logger().warning("Interrupted by user")
            return 130
        except (TimeoutError, ConnectionError, OSError) as e:
            self.get_logger().error(f"Network error in LLM command: {e}")
            if self.get_logger().isEnabledFor(10):  # DEBUG
                import traceback
                traceback.print_exc()
            return self.EXIT_EXECUTION_ERROR
        except (ValueError, TypeError) as e:
            self.get_logger().error(f"Invalid input in LLM command: {e}")
            if self.get_logger().isEnabledFor(10):
                import traceback
                traceback.print_exc()
            return self.EXIT_EXECUTION_ERROR
        except Exception as e:
            self.get_logger().error(f"LLM command failed: {e}")
            if self.get_logger().isEnabledFor(10):  # DEBUG
                import traceback
                traceback.print_exc()
            return self.EXIT_EXECUTION_ERROR

    # ==================================================================
    # 1. kb llm status
    # ==================================================================

    def _cmd_status(self) -> int:
        """Zeigt: Model-Source, beide Engines, aktive Jobs, letzte Essenzen/Reports."""
        from kb.biblio.config import LLMConfig

        config = LLMConfig.get_instance()
        log = self.get_logger()

        print("\n🧠  LLM System Status")
        print("=" * 50)

        self._print_config_status(config)
        self._print_engine_status(config, log)
        self._print_scheduler_status()
        essences, reports = self._get_content_recent()
        self._print_essences_recent(essences)
        self._print_reports_recent(reports)
        self._print_watcher_status()
        self._print_paths(config)
        print()
        return self.EXIT_SUCCESS

    def _print_config_status(self, config):
        """Print model source and parallel mode config."""
        print(f"\n  🔀  Model Source:  {config.model_source}")
        print(f"     Parallel Mode:  {config.parallel_mode}")
        if config.parallel_mode:
            print(f"     Strategy:       {config.parallel_strategy}")

    def _print_engine_status(self, config, log):
        """Print primary and secondary engine status."""
        from kb.biblio.engine.registry import EngineRegistry
        try:
            registry = EngineRegistry.get_instance()
            status = registry.status()
            self._print_primary_engine(status.get("primary"))
            self._print_secondary_engine(status.get("secondary"))
        except (ImportError, RuntimeError, OSError) as e:
            log.debug(f"EngineRegistry status failed: {e}")
            self._print_engine_fallback(config)

    def _print_primary_engine(self, primary):
        print("\n  🔧  Primary Engine:")
        if primary:
            avail = "✅" if primary.get("available") else "❌"
            print(f"     Provider:   {primary.get('provider', '?')}")
            print(f"     Model:      {primary.get('model', '?')}")
            print(f"     Available:  {avail}  {primary.get('available', False)}")
        else:
            print("     — nicht verfügbar")

    def _print_secondary_engine(self, secondary):
        if secondary:
            print("\n  🔧  Secondary Engine:")
            avail = "✅" if secondary.get("available") else "❌"
            print(f"     Provider:   {secondary.get('provider', '?')}")
            print(f"     Model:      {secondary.get('model', '?')}")
            print(f"     Available:  {avail}  {secondary.get('available', False)}")

    def _print_engine_fallback(self, config):
        """Fallback when EngineRegistry is unavailable."""
        from kb.biblio.engine.ollama_engine import OllamaEngine
        ollama_ok = False
        try:
            ollama_ok = OllamaEngine.get_instance(config).is_available()
        except (ImportError, OSError):
            pass
        icon = "✅" if ollama_ok else "❌"
        print(f"\n  {icon}  Modell:    {config.model}")
        print(f"     URL:       {config.ollama_url}")
        print(f"     Available: {ollama_ok}")

    def _print_scheduler_status(self):
        """Print scheduler status."""
        try:
            from kb.biblio.scheduler import TaskScheduler
            scheduler = TaskScheduler()
            stats = scheduler.get_stats()
            sched_running = stats.get("is_running", False)
            sched_icon = "🟢" if sched_running else "🔴"
            print(f"\n  {sched_icon}  Scheduler: {'läuft' if sched_running else 'gestoppt'}")
            print(f"     Jobs:      {stats.get('registered_jobs', 0)} registriert")
            print(f"     Läufe:     {stats.get('total_runs', 0)} "
                  f"(✅ {stats.get('success_count', 0)} ❌ {stats.get('failure_count', 0)})")
        except (ImportError, RuntimeError, OSError):
            print(f"\n  ⚠️  Scheduler: nicht verfügbar")

    def _get_content_recent(self):
        """Get recent essences and reports."""
        try:
            from kb.biblio.content_manager import LLMContentManager
            manager = LLMContentManager()
            essences = _run_async(manager.list_essences(limit=3))
            reports = _run_async(manager.list_reports(limit=3))
        except (ValueError, TypeError, ImportError):
            essences, reports = [], []
        return essences, reports

    def _print_essences_recent(self, essences):
        """Print recent essences."""
        print(f"\n  📦  Letzte Essenzen ({len(essences)}):")
        if essences:
            for e in essences:
                print(_fmt_essence(e))
        else:
            print("     — keine vorhanden")

    def _print_reports_recent(self, reports):
        """Print recent reports."""
        print(f"\n  📊  Letzte Reports ({len(reports)}):")
        if reports:
            for r in reports:
                print(_fmt_report(r))
        else:
            print("     — keine vorhanden")

    def _print_watcher_status(self):
        """Print FileWatcher status."""
        try:
            from kb.biblio.watcher import FileWatcher
            watcher = FileWatcher()
            w_stats = watcher.get_stats()
            running = w_stats.get("is_running", False)
            total = w_stats.get("total_tracked", 0)
            w_icon = "🟢" if running else "🔴"
            print(f"\n  {w_icon}  FileWatcher: {'läuft' if running else 'gestoppt'} "
                  f"({total} Dateien getrackt)")
        except Exception:
            print(f"\n  ⚠️  FileWatcher: nicht verfügbar")

    def _print_paths(self, config):
        """Print configured paths."""
        print(f"\n  📁  Essences: {config.essences_path}")
        print(f"  📁  Reports:   {config.reports_path}")
        print(f"  📁  Graph:     {config.graph_path}")

    # ==================================================================
    # 7. kb llm engine <status|switch|test>
    # ==================================================================

    def _cmd_engine(self) -> int:
        """Engine-Aktionen: status, switch, test."""
        action = getattr(self._args, "engine_action", None)
        if not action:
            self.print_error("Keine Engine-Aktion angegeben. Siehe: kb llm engine --help")
            return self.EXIT_VALIDATION_ERROR

        dispatch = {
            "status": self._engine_status,
            "switch": self._engine_switch,
            "test": self._engine_test,
        }
        handler = dispatch.get(action)
        if not handler:
            self.print_error(f"Unbekannte Engine-Aktion: {action}")
            return self.EXIT_VALIDATION_ERROR

        try:
            return handler()
        except KeyboardInterrupt:
            self.get_logger().warning("Interrupted by user")
            return 130
        except Exception as e:
            self.get_logger().error(f"Engine command failed: {e}")
            if self.get_logger().isEnabledFor(10):
                import traceback
                traceback.print_exc()
            return self.EXIT_EXECUTION_ERROR

    def _engine_status(self) -> int:
        """Zeigt detaillierten Status beider Engines und Registry."""
        from kb.biblio.config import LLMConfig
        from kb.biblio.engine.registry import EngineRegistry

        config = LLMConfig.get_instance()

        print("\n🔧  LLM Engine Status")
        print("=" * 50)

        # Model-Source
        print(f"\n  🔀  Model Source:    {config.model_source}")
        print(f"     Parallel Mode:    {config.parallel_mode}")
        if config.parallel_mode:
            print(f"     Parallel Strategy: {config.parallel_strategy}")

        # Engine Registry
        try:
            registry = EngineRegistry.get_instance()
            status = registry.status()

            print("\n  📌  Primary Engine:")
            primary = status.get("primary")
            if primary:
                avail_icon = "✅" if primary.get("available") else "❌"
                print(f"     Provider:   {primary.get('provider', '?')}")
                print(f"     Model:      {primary.get('model', '?')}")
                print(f"     Available:  {avail_icon}  {primary.get('available', False)}")
            else:
                print("     — nicht konfiguriert")

            secondary = status.get("secondary")
            if secondary:
                print("\n  📌  Secondary Engine:")
                avail_icon = "✅" if secondary.get("available") else "❌"
                print(f"     Provider:   {secondary.get('provider', '?')}")
                print(f"     Model:      {secondary.get('model', '?')}")
                print(f"     Available:  {avail_icon}  {secondary.get('available', False)}")
            else:
                print("\n  📌  Secondary Engine: — nicht konfiguriert")

            print(f"\n  Has Secondary: {registry.has_secondary}")

        except (ValueError, TypeError, ImportError) as e:
            print(f"\n  ⚠️  EngineRegistry Fehler: {e}")
            # Einzelne Engines prüfen
            for source, name, url in [
                ("ollama", "Ollama", config.ollama_url),
                ("huggingface", "HuggingFace", config.hf_model_name),
            ]:
                try:
                    from kb.biblio.engine.registry import EngineRegistry as ER
                    er = ER.get_instance()
                    avail = er.is_engine_available(source)
                    icon = "✅" if avail else "❌"
                    print(f"  {icon}  {name}: {url}  (available={avail})")
                except (ImportError, RuntimeError, OSError):
                    print(f"  ❌  {name}: nicht verfügbar")

        # Config-Übersicht
        print("\n  ⚙️  Engine-Konfiguration:")
        print(f"     Ollama Model:      {config.ollama_model}")
        print(f"     Ollama URL:        {config.ollama_url}")
        print(f"     Ollama Timeout:    {config.ollama_timeout}s")
        print(f"     Ollama Temp:       {config.ollama_temperature}")
        print(f"     HF Model:          {config.hf_model_name}")
        print(f"     HF Device:         {config.hf_device}")
        print()
        return self.EXIT_SUCCESS

    def _engine_switch(self) -> int:
        """Wechselt model_source und resettet Engine Registry."""
        from kb.biblio.config import LLMConfig
        from kb.biblio.engine.registry import EngineRegistry

        source = self._args.source
        log = self.get_logger()

        print(f"\n  🔀  Wechsle model_source → {source} …")

        # 1. Aktuellen Zustand sichern
        old_source = LLMConfig.get_instance().model_source
        print(f"     Alt: {old_source}")

        # 2. Engine Registry zurücksetzen (bevor Config neu geladen wird)
        try:
            EngineRegistry.reset()
            print("     Registry zurückgesetzt ✓")
        except (ImportError, RuntimeError, OSError) as e:
            log.warning(f"EngineRegistry.reset() fehlgeschlagen: {e}")
            print(f"     ⚠️  Registry-Reset fehlgeschlagen: {e}")

        # 3. Config neu laden mit neuer model_source
        try:
            LLMConfig.reload(model_source=source)
            print(f"     Neu: {LLMConfig.get_instance().model_source}")
        except (ValueError, ImportError, RuntimeError) as e:
            log.error(f"Config-Reload fehlgeschlagen: {e}")
            # Versuche Rollback
            try:
                LLMConfig.reload(model_source=old_source)
                print(f"     ❌  Switch fehlgeschlagen, zurück auf {old_source}")
            except (ValueError, ImportError, RuntimeError):
                pass
            return self.EXIT_EXECUTION_ERROR

        # 4. Neue Registry validieren
        try:
            registry = EngineRegistry.get_instance()
            status = registry.status()
            primary = status.get("primary")
            if primary:
                avail_icon = "✅" if primary.get("available") else "❌"
                print(f"     Primary: {primary.get('provider')} / {primary.get('model')} {avail_icon}")
            secondary = status.get("secondary")
            if secondary:
                avail_icon = "✅" if secondary.get("available") else "❌"
                print(f"     Secondary: {secondary.get('provider')} / {secondary.get('model')} {avail_icon}")
        except Exception as e:
            log.warning(f"Registry-Validierung fehlgeschlagen: {e}")
            print(f"     ⚠️  Registry-Validierung fehlgeschlagen: {e}")

        env_hint = "KB_LLM_MODEL_SOURCE"
        print(f"\n  ✅  model_source = {source}")
        print(f"     Hinweis: Änderung ist nur in-memory. "
              f"Setze {env_hint} für Persistenz.\n")
        return self.EXIT_SUCCESS

    def _engine_test(self) -> int:
        """Testet beide Engines mit einem kurzen Prompt."""
        from kb.biblio.config import LLMConfig
        from kb.biblio.engine.registry import EngineRegistry
        from kb.biblio.engine.base import LLMProvider

        prompt = self._args.prompt
        max_tokens = self._args.max_tokens
        config = LLMConfig.get_instance()
        log = self.get_logger()

        print(f"\n  🧪  Engine Test")
        print(f"     Prompt: \"{prompt}\"")
        print(f"     Max Tokens: {max_tokens}")
        print()

        results = []

        # Primary Engine testen
        try:
            registry = EngineRegistry.get_instance()
            primary = registry.get_primary()
            provider_name = primary.get_provider().value
            model_name = primary.get_model_name()
            print(f"  ▶️  Primary ({provider_name}/{model_name}) …", end=" ")
            try:
                response = primary.generate(prompt, max_tokens=max_tokens)
                if response.success:
                    content_preview = response.content[:100].replace("\n", " ")
                    print(f"✅")
                    print(f"     Antwort: {content_preview}")
                    print(f"     Dauer:   {response.total_duration or '?'} ns")
                    results.append(("primary", True, None))
                else:
                    print(f"❌")
                    print(f"     Fehler:  {response.error}")
                    results.append(("primary", False, response.error))
            except (ValueError, TypeError, ImportError) as e:
                print(f"❌")
                print(f"     Fehler:  {e}")
                results.append(("primary", False, str(e)))
        except (ImportError, RuntimeError, OSError) as e:
            print(f"  ⚠️  Primary Engine nicht verfügbar: {e}")
            results.append(("primary", False, str(e)))

        # Secondary Engine testen
        try:
            secondary = registry.get_secondary()
            if secondary:
                provider_name = secondary.get_provider().value
                model_name = secondary.get_model_name()
                print(f"  ▶️  Secondary ({provider_name}/{model_name}) …", end=" ")
                try:
                    response = secondary.generate(prompt, max_tokens=max_tokens)
                    if response.success:
                        content_preview = response.content[:100].replace("\n", " ")
                        print(f"✅")
                        print(f"     Antwort: {content_preview}")
                        print(f"     Dauer:   {response.total_duration or '?'} ns")
                        results.append(("secondary", True, None))
                    else:
                        print(f"❌")
                        print(f"     Fehler:  {response.error}")
                        results.append(("secondary", False, response.error))
                except (ValueError, TypeError, ImportError) as e:
                    print(f"❌")
                    print(f"     Fehler:  {e}")
                    results.append(("secondary", False, str(e)))
            else:
                print(f"  ℹ️  Keine Secondary Engine konfiguriert")
        except (ImportError, RuntimeError, OSError) as e:
            print(f"  ℹ️  Secondary Engine nicht konfiguriert: {e}")

        # Zusammenfassung
        successes = sum(1 for _, ok, _ in results if ok)
        failures = len(results) - successes
        print(f"\n  📊  Ergebnis: {successes} erfolgreich, {failures} fehlgeschlagen\n")
        return self.EXIT_SUCCESS if failures == 0 else self.EXIT_EXECUTION_ERROR

    # ==================================================================
    # 2. kb llm generate essence|report
    # ==================================================================

    def _cmd_generate(self) -> int:
        """Ruft EssenzGenerator oder ReportGenerator auf."""
        what = getattr(self._args, "generate_what", None)
        if what == "essence":
            return self._generate_essence()
        elif what == "report":
            return self._generate_report()
        else:
            self.print_error("Was soll generiert werden? essence | report")
            return self.EXIT_VALIDATION_ERROR

    def _generate_essence(self) -> int:
        """Ruft EssenzGenerator.generate_essence() auf — einzel oder batch."""
        from kb.biblio.generator import EssenzGenerator

        log = self.get_logger()
        topic = self._args.topic
        source_files = getattr(self._args, "source_files", None) or []
        batch_topics = getattr(self._args, "batch_topics", None) or []

        # Build topic list
        topics = batch_topics if batch_topics else [topic]

        spinner = ProgressSpinner(f"Generiere Essenz: {topics[0]}…")

        async def _generate_all():
            generator = EssenzGenerator()
            results = []
            total = len(topics)
            for i, t in enumerate(topics, 1):
                spinner.update(f"[{i}/{total}] Generiere: {t}…")
                result = await generator.generate_essence(
                    topic=t,
                    source_files=source_files,
                )
                results.append(result)
            return results

        try:
            results = _run_async(_generate_all())
        except Exception as e:
            spinner.finish()
            log.error(f"Essenz-Erstellung fehlgeschlagen: {e}")
            return self.EXIT_EXECUTION_ERROR

        spinner.finish()

        # Print results
        successes = sum(1 for r in results if r.success)
        failures = len(results) - successes

        print(f"\n  Essenz-Erstellung: {successes} erfolgreich, {failures} fehlgeschlagen\n")
        for r in results:
            icon = "✅" if r.success else "❌"
            print(f"  {icon}  {r.topic}")
            if r.success:
                print(f"     Hash:   {r.essence_hash}")
                print(f"     Pfad:   {r.essence_path}")
                print(f"     Modell: {r.model_used}")
                print(f"     Dauer:  {r.duration_ms}ms")
                if hasattr(r, "hotspot_score") and r.hotspot_score is not None:
                    print(f"     Hotspot: {r.hotspot_score}")
            else:
                print(f"     Fehler: {r.error}")
            print()

        return self.EXIT_SUCCESS if failures == 0 else self.EXIT_EXECUTION_ERROR

    def _generate_report(self) -> int:
        """Ruft ReportGenerator auf."""
        from kb.biblio.generator import ReportGenerator

        log = self.get_logger()
        period = self._args.period

        spinner = ProgressSpinner(f"Generiere {period} Report…")

        def _progress(stage: str, detail: str):
            spinner.update(f"{stage}: {detail}")

        async def _generate():
            generator = ReportGenerator()
            if period == "daily":
                return await generator.generate_daily_report(on_progress=_progress)
            elif period == "weekly":
                return await generator.generate_weekly_report(on_progress=_progress)
            else:
                return await generator.generate_monthly_report(on_progress=_progress)

        try:
            result = _run_async(_generate())
        except Exception as e:
            spinner.finish()
            log.error(f"Report-Erstellung fehlgeschlagen: {e}")
            return self.EXIT_EXECUTION_ERROR

        spinner.finish()

        icon = "✅" if result.success else "❌"
        print(f"\n  {icon}  {period.capitalize()} Report")
        if result.success:
            print(f"     Pfad:      {result.report_path}")
            print(f"     Zeitraum:  {result.period_start} – {result.period_end}")
            print(f"     Quellen:   {result.sources_count}")
            print(f"     Dauer:     {result.duration_ms}ms")
            if hasattr(result, "sections_included") and result.sections_included:
                print(f"     Sektionen: {', '.join(result.sections_included)}")
        else:
            print(f"     Fehler: {result.error}")
        print()
        return self.EXIT_SUCCESS if result.success else self.EXIT_EXECUTION_ERROR

    # ==================================================================
    # 3. kb llm watch start|stop|status
    # ==================================================================

    def _cmd_watch(self) -> int:
        """FileWatcher starten/stoppen/status."""
        action = self._args.watch_action

        if action == "status":
            return self._watch_status()
        elif action == "start":
            return self._watch_start()
        elif action == "stop":
            return self._watch_stop()
        else:
            self.print_error(f"Unbekannte watch-Aktion: {action}")
            return self.EXIT_VALIDATION_ERROR

    def _watch_status(self) -> int:
        try:
            from kb.biblio.watcher import FileWatcher
            watcher = FileWatcher()
            stats = watcher.get_stats()
        except Exception as e:
            self.get_logger().error(f"FileWatcher-Status fehlgeschlagen: {e}")
            return self.EXIT_EXECUTION_ERROR

        running = stats.get("is_running", False)
        total = stats.get("total_tracked", 0)
        by_status = stats.get("by_status", {})
        last_scan = stats.get("last_scan_at", "—")

        icon = "🟢" if running else "🔴"
        print(f"\n  {icon}  FileWatcher Status")
        print("  " + "-" * 40)
        print(f"  Zustand:      {'läuft' if running else 'gestoppt'}")
        print(f"  Getrackt:     {total} Dateien")
        print(f"  Letzter Scan: {last_scan[:19] if last_scan and last_scan != '—' else '—'}")

        if by_status:
            print("  Nach Status:")
            for status_name, count in sorted(by_status.items()):
                print(f"    {status_name}: {count}")

        # Recent scans
        recent = stats.get("recent_scans", [])
        if recent:
            print(f"\n  Letzte Scans ({len(recent)}):")
            for s in recent[:5]:
                print(f"    {s.get('scan_at', '?')[:19]}  "
                      f"found={s.get('files_found', 0)}  "
                      f"new={s.get('files_new', 0)}  "
                      f"processed={s.get('files_processed', 0)}  "
                      f"errors={s.get('errors', 0)}")

        print()
        return self.EXIT_SUCCESS

    def _watch_start(self) -> int:
        from kb.biblio.watcher import FileWatcher

        watcher = FileWatcher()
        interval = watcher._llm_config.watcher_interval

        print(f"\n  👁  Starte FileWatcher (Intervall: {interval}min) …")
        print("     (Drücke Ctrl+C zum Stoppen)\n")

        try:
            _run_async(watcher.run(interval_minutes=interval))
        except KeyboardInterrupt:
            watcher.stop()
            print("\n\n  👁  FileWatcher gestoppt.")
        return self.EXIT_SUCCESS

    def _watch_stop(self) -> int:
        from kb.biblio.watcher import FileWatcher

        watcher = FileWatcher()
        try:
            watcher.stop()
            print("\n  👁  FileWatcher gestoppt.\n")
        except Exception as e:
            # Watcher might not be running — that's fine
            self.get_logger().debug(f"watcher.stop() error (probably not running): {e}")
            print("\n  ℹ️  FileWatcher war nicht aktiv.\n")
        return self.EXIT_SUCCESS

    # ==================================================================
    # 4. kb llm scheduler start|stop|list|trigger <job>
    # ==================================================================

    def _cmd_scheduler(self) -> int:
        """TaskScheduler steuern."""
        action = self._args.scheduler_action

        if action == "list":
            return self._scheduler_list()
        elif action == "trigger":
            return self._scheduler_trigger()
        elif action == "start":
            return self._scheduler_start()
        elif action == "stop":
            return self._scheduler_stop()
        else:
            self.print_error(f"Unbekannte scheduler-Aktion: {action}")
            return self.EXIT_VALIDATION_ERROR

    def _scheduler_list(self) -> int:
        try:
            from kb.biblio.scheduler import TaskScheduler
            scheduler = TaskScheduler()
            jobs = scheduler.list_jobs()
            stats = scheduler.get_stats()
        except Exception as e:
            self.get_logger().error(f"Scheduler-Status fehlgeschlagen: {e}")
            return self.EXIT_EXECUTION_ERROR

        running = stats.get("is_running", False)
        icon = "🟢" if running else "🔴"

        print(f"\n  {icon}  TaskScheduler")
        print("  " + "-" * 60)
        print(f"  Zustand:  {'läuft' if running else 'gestoppt'}")
        print(f"  Läufe:    {stats.get('total_runs', 0)} "
              f"(✅ {stats.get('success_count', 0)} ❌ {stats.get('failure_count', 0)})")
        print()

        for j in jobs:
            state = j.get("state") or {}
            enabled = j.get("enabled", True)
            enabled_icon = "✅" if enabled else "⏸️"
            last = state.get("last_run", "—")
            last_status = state.get("last_status", "—")
            run_count = state.get("run_count", 0)

            print(f"  {enabled_icon}  {j.get('job_id', '?'):16s}  "
                  f"[{j.get('cron_expression', '?')}]")
            print(f"     {j.get('description', '')}")
            print(f"     Last: {last_status}  {str(last)[:19]}  "
                  f"(runs: {run_count})")
            print()

        return self.EXIT_SUCCESS

    def _scheduler_trigger(self) -> int:
        from kb.biblio.scheduler import TaskScheduler, TaskSchedulerError

        job_id = getattr(self._args, "job", None)
        if not job_id:
            self.print_error("Job-ID angeben: kb llm scheduler trigger <job>")
            return self.EXIT_VALIDATION_ERROR

        spinner = ProgressSpinner(f"Triggere Job: {job_id}…")

        async def _trigger():
            scheduler = TaskScheduler()
            return await scheduler.run_job(job_id, triggered_by="manual")

        try:
            result = _run_async(_trigger())
        except TaskSchedulerError:
            spinner.finish()
            self.get_logger().error(f"Unbekannter Job: {job_id}")
            return self.EXIT_VALIDATION_ERROR
        except Exception as e:
            spinner.finish()
            self.get_logger().error(f"Job-Trigger fehlgeschlagen: {e}")
            return self.EXIT_EXECUTION_ERROR

        spinner.finish()

        icon = "✅" if result.status.value == "success" else "❌"
        print(f"\n  {icon}  Job: {result.job_id}")
        print(f"     Status:  {result.status.value}")
        print(f"     Dauer:   {result.duration_ms}ms")
        if result.message:
            print(f"     Message: {result.message}")
        if result.error:
            print(f"     Fehler:  {result.error}")
        if result.data:
            print(f"     Data:    {json.dumps(result.data, indent=2, ensure_ascii=False)}")
        print()
        return self.EXIT_SUCCESS if result.status.value == "success" else self.EXIT_EXECUTION_ERROR

    def _scheduler_start(self) -> int:
        from kb.biblio.scheduler import TaskScheduler

        print("\n  ⏰  Starte TaskScheduler …")
        print("     (Drücke Ctrl+C zum Stoppen)\n")

        async def _run():
            scheduler = TaskScheduler()
            await scheduler.start()

        try:
            _run_async(_run())
        except KeyboardInterrupt:
            print("\n\n  ⏰  TaskScheduler gestoppt.")
        return self.EXIT_SUCCESS

    def _scheduler_stop(self) -> int:
        from kb.biblio.scheduler import TaskScheduler

        try:
            scheduler = TaskScheduler()
            _run_async(scheduler.shutdown())
            print("\n  ⏰  TaskScheduler gestoppt.\n")
        except Exception as e:
            self.get_logger().debug(f"scheduler.shutdown() error: {e}")
            print("\n  ℹ️  TaskScheduler war nicht aktiv.\n")
        return self.EXIT_SUCCESS

    # ==================================================================
    # 5. kb llm list essences|reports
    # ==================================================================

    def _cmd_list(self) -> int:
        """Listet Essenzen oder Reports auf."""
        what = getattr(self._args, "list_what", None)
        if what == "essences":
            return self._list_essences()
        elif what == "reports":
            return self._list_reports()
        else:
            self.print_error("Was auflisten? essences | reports")
            return self.EXIT_VALIDATION_ERROR

    def _list_essences(self) -> int:
        from kb.biblio.content_manager import LLMContentManager

        log = self.get_logger()
        limit = getattr(self._args, "limit", 50)
        topic_filter = getattr(self._args, "topic_filter", None)
        date_range = getattr(self._args, "date_range", None)
        json_output = getattr(self._args, "json_output", False)

        try:
            manager = LLMContentManager()
            # Fetch more for filtering
            essences = _run_async(manager.list_essences(limit=limit * 3))
        except Exception as e:
            log.error(f"Cannot list essences: {e}")
            return self.EXIT_EXECUTION_ERROR

        # Apply topic filter
        if topic_filter:
            topic_lower = topic_filter.lower()
            essences = [e for e in essences
                        if topic_lower in e.get("title", "").lower()]

        # Apply date range filter
        if date_range:
            start_dt, end_dt = _parse_date_range(date_range)
            if start_dt or end_dt:
                filtered = []
                for e in essences:
                    at = e.get("extracted_at", "")
                    try:
                        dt = datetime.fromisoformat(at.replace("Z", "+00:00"))
                        if start_dt and dt < start_dt:
                            continue
                        if end_dt and dt > end_dt:
                            continue
                        filtered.append(e)
                    except (ValueError, TypeError):
                        continue
                essences = filtered

        essences = essences[:limit]

        if json_output:
            print(json.dumps(essences, indent=2, ensure_ascii=False))
        else:
            print(f"\n  📦  Essenzen ({len(essences)} angezeigt)\n")
            if not essences:
                print("     — keine vorhanden")
            for e in essences:
                print(_fmt_essence(e))
            print()

        return self.EXIT_SUCCESS

    def _list_reports(self) -> int:
        from kb.biblio.content_manager import LLMContentManager

        log = self.get_logger()
        limit = getattr(self._args, "limit", 50)
        rtype_filter = getattr(self._args, "report_type_filter", None)
        json_output = getattr(self._args, "json_output", False)

        try:
            manager = LLMContentManager()
            reports = _run_async(manager.list_reports(
                report_type=rtype_filter, limit=limit
            ))
        except Exception as e:
            log.error(f"Cannot list reports: {e}")
            return self.EXIT_EXECUTION_ERROR

        if json_output:
            print(json.dumps(reports, indent=2, ensure_ascii=False))
        else:
            print(f"\n  📊  Reports ({len(reports)} angezeigt)\n")
            if not reports:
                print("     — keine vorhanden")
            for r in reports:
                print(_fmt_report(r))
            print()

        return self.EXIT_SUCCESS

    # ==================================================================
    # 6. kb llm config [show|set <key> <value>]
    # ==================================================================

    def _cmd_config(self) -> int:
        """Zeigt oder setzt LLMConfig."""
        action = getattr(self._args, "config_action", "show")

        if action == "set":
            return self._config_set()
        return self._config_show()

    def _config_show(self) -> int:
        from kb.biblio.config import LLMConfig

        config = LLMConfig.get_instance()
        d = config.to_dict()

        print("\n  ⚙️  LLM Konfiguration")
        print("  " + "-" * 40)
        for key, value in sorted(d.items()):
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            print(f"  {key:25s}  {value}")
        print()
        return self.EXIT_SUCCESS

    def _config_set(self) -> int:
        """Setzt einen LLMConfig-Wert (in-memory)."""
        from kb.biblio.config import LLMConfig

        log = self.get_logger()
        key = getattr(self._args, "config_key", None)
        value = getattr(self._args, "config_value", None)

        if not key or value is None:
            self.print_error("Usage: kb llm config set <key> <value>")
            return self.EXIT_VALIDATION_ERROR

        if key not in _MUTABLE_CONFIG_KEYS:
            log.error(
                f"Cannot set '{key}'. Erlaubte Keys: "
                f"{', '.join(sorted(_MUTABLE_CONFIG_KEYS))}"
            )
            return self.EXIT_VALIDATION_ERROR

        expected_type = _MUTABLE_CONFIG_KEYS[key]

        # Bool-Parsing: akzeptiert true/false/1/0/yes/no
        if expected_type is bool:
            if value.lower() in ("true", "1", "yes"):
                parsed = True
            elif value.lower() in ("false", "0", "no"):
                parsed = False
            else:
                log.error(
                    f"Ungültiger Wert für {key}: '{value}'. "
                    f"Erwarte bool (true/false/1/0/yes/no)"
                )
                return self.EXIT_VALIDATION_ERROR
        elif expected_type is int:
            try:
                parsed = int(value)
            except ValueError:
                log.error(f"Ungültiger Wert für {key}: erwartet int")
                return self.EXIT_VALIDATION_ERROR
        elif expected_type is float:
            try:
                parsed = float(value)
            except ValueError:
                log.error(f"Ungültiger Wert für {key}: erwartet float")
                return self.EXIT_VALIDATION_ERROR
        else:
            parsed = str(value)

        # Bei model_source-Wechsel: Engine Registry zurücksetzen
        needs_registry_reset = (key == "model_source")

        # Apply via LLMConfig.reload
        config = LLMConfig.get_instance()
        try:
            LLMConfig.reload(**{key: parsed})
        except Exception as e:
            log.error(f"Config-Update fehlgeschlagen: {e}")
            return self.EXIT_EXECUTION_ERROR

        # Engine Registry zurücksetzen wenn model_source geändert
        if needs_registry_reset:
            try:
                from kb.biblio.engine.registry import EngineRegistry
                EngineRegistry.reset()
                log.info("EngineRegistry zurückgesetzt nach model_source-Wechsel")
            except Exception as e:
                log.warning(f"EngineRegistry.reset() fehlgeschlagen: {e}")

        env_hint = _CONFIG_KEY_TO_ENV.get(key, f"KB_LLM_{key.upper()}")
        print(f"\n  ✅  {key} = {parsed}")
        print(f"     Hinweis: Änderung ist nur in-memory. "
              f"Setze {env_hint} für Persistenz.\n")
        return self.EXIT_SUCCESS