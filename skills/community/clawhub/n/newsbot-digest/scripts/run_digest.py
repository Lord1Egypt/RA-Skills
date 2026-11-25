#!/usr/bin/env python3
"""NewsBot digest — однократный полный прогон (замена Telegram-бота).

Сбор новостей -> отбор агентами (этап 1) -> итоговая выборка (этап 2) ->
извлечение статей (Camoufox headless) -> перевод -> PDF -> заголовки -> дайджест.

Пример:
    python scripts/run_digest.py --workdir ~/newsbot_data
Результат: <output-dir>/<YYYY-MM-DD>/{digest.md, digest.html, result.json, selected.xlsx, pdf/*.pdf}
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsbot.config import RunContext, load_env, set_ctx, setup_logger, status  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser(description="NewsBot: ежедневный дайджест новостей за один запуск")
    p.add_argument("--workdir", default=os.getenv("NEWSBOT_WORKDIR", "./newsbot_data"),
                   help="Папка состояния (история выборок для дедупликации). Должна сохраняться между запусками.")
    p.add_argument("--output-dir", default=os.getenv("NEWSBOT_OUTPUT_DIR"),
                   help="Куда класть дайджест и PDF (по умолчанию <workdir>/outputs)")
    p.add_argument("--env", default=None, help="Путь к .env с ключами")
    p.add_argument("--browser", choices=["headless", "virtual"], default=os.getenv("NEWSBOT_BROWSER", "headless"),
                   help="headless — без окна (по умолчанию); virtual — через Xvfb, тоже без окна")
    p.add_argument("--skip-telegram", action="store_true")
    p.add_argument("--skip-google", action="store_true")
    return p.parse_args()


async def pipeline(args) -> int:
    from newsbot import articles, collect, digest, selection

    # 0. сбор
    status("collect", "start")
    counts = {}
    for name, fn, skip in (("telegram", collect.collect_telegram, args.skip_telegram),
                           ("google_news", collect.collect_google_news, args.skip_google),
                           ("newsfeed", collect.collect_newsfeed, False)):
        if skip:
            status(f"collect:{name}", "skip")
            continue
        try:
            counts[name] = fn()
            status(f"collect:{name}", "ok", f"{counts[name]} шт.")
        except Exception as e:
            status(f"collect:{name}", "error", str(e))
    if not any(counts.values()):
        raise RuntimeError("Не удалось собрать ни одной новости")

    # 1. первичный отбор
    status("stage1_select", "start")
    n = await selection.stage1_select()
    status("stage1_select", "ok", f"{n} новостей в коллекции")

    # 2. итоговая выборка
    status("stage2_final", "start")
    n = await selection.stage2_final_select()
    status("stage2_final", "ok", f"{n} новостей в выборке")

    # 3. статьи
    status("articles", "start")
    try:
        stats = await articles.extract_and_save_articles()
        status("articles", "ok", str(stats))
    except Exception as e:
        status("articles", "error", str(e))

    status("translate", "start")
    try:
        status("translate", "ok", f"{articles.translate_articles()} PDF")
    except Exception as e:
        status("translate", "error", str(e))

    status("titles", "start")
    try:
        articles.add_titles()
        status("titles", "ok")
    except Exception as e:
        status("titles", "error", str(e))

    # 4. дайджест
    res = digest.build_digest()
    status("finish", "ok", res["digest_md"])

    print("\n" + "=" * 60)
    print(Path(res["digest_md"]).read_text(encoding="utf-8"))
    print("=" * 60)
    print(f"RESULT_JSON={Path(res['output_dir']) / 'result.json'}")
    return 0


def main() -> int:
    args = parse_args()
    workdir = Path(args.workdir).expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    load_env(Path(args.env) if args.env else None, workdir)
    output_root = Path(args.output_dir).expanduser().resolve() if args.output_dir else workdir / "outputs"

    c = RunContext(workdir=workdir, output_root=output_root,
                   headless=True if args.browser == "headless" else "virtual")
    set_ctx(c)
    setup_logger(c)

    if not (os.getenv("CLOUD_API") or os.getenv("API_DEEPSEEK")):
        status("finish", "error", "Нет ключей CLOUD_API / API_DEEPSEEK (см. .env.example)")
        return 2
    try:
        return asyncio.run(pipeline(args))
    except Exception as e:
        status("finish", "error", f"{e}\n{traceback.format_exc()}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
